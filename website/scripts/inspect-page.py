"""Capture the rendered site with the Playwright/Chromium in the Nix dev shell."""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen

WEBSITE = Path(__file__).resolve().parents[1]


def viewport(value):
    try:
        width, height = map(int, value.lower().split("x"))
        if width > 0 and height > 0:
            return {"width": width, "height": height}
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("use positive WIDTHxHEIGHT, e.g. 1440x900")


def reachable(url):
    try:
        with urlopen(url, timeout=1):
            return True
    except HTTPError:
        return True  # An HTTP error still means a server owns this port.
    except (URLError, OSError):
        return False


@contextmanager
def dev_server(base_url, output):
    if reachable(base_url):
        print(f"Using server at {base_url}")
        yield
        return

    address = urlsplit(base_url)
    if (
        address.scheme != "http"
        or address.hostname not in ("127.0.0.1", "localhost")
        or address.path not in ("", "/")
    ):
        raise RuntimeError(f"Start the preview server at {base_url}, then rerun.")
    vite = WEBSITE / "node_modules/vite/bin/vite.js"
    if not vite.is_file():
        raise RuntimeError("Install website dependencies with npm ci, then rerun.")

    log_path = output / "server.log"
    with log_path.open("w") as log:
        process = subprocess.Popen(
            [
                "node",
                str(vite),
                "--host",
                address.hostname,
                "--port",
                str(address.port or 80),
                "--strictPort",
            ],
            cwd=WEBSITE,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            deadline = time.monotonic() + 30
            while not reachable(base_url):
                if process.poll() is not None or time.monotonic() > deadline:
                    raise RuntimeError(f"Dev server did not start. Read {log_path}")
                time.sleep(0.1)
            print(f"Started temporary dev server at {base_url}")
            yield
        finally:
            # Only stop the process group created here; leave existing Vite alone.
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=5)
            except ProcessLookupError:
                pass
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()


def capture(browser, url, size, output):
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

    stem = f"page-{size['width']}x{size['height']}"
    report = {
        "url": url,
        "viewport": size,
        "errors": [],
        "console_errors": [],
        "failed_requests": [],
        "http_errors": [],
    }
    with browser.new_context(
        viewport=size, device_scale_factor=1, reduced_motion="reduce"
    ) as context:
        page = context.new_page()
        page.set_default_timeout(15_000)
        page.on("pageerror", lambda error: report["errors"].append(str(error)))
        page.on(
            "console",
            lambda message: (
                report["console_errors"].append(message.text)
                if message.type == "error"
                else None
            ),
        )
        page.on(
            "requestfailed",
            lambda request: report["failed_requests"].append(
                {
                    "url": request.url,
                    "type": request.resource_type,
                    "error": request.failure,
                }
            ),
        )
        page.on(
            "response",
            lambda response: (
                report["http_errors"].append(
                    {"url": response.url, "status": response.status}
                )
                if response.status >= 400
                else None
            ),
        )

        response = page.goto(url, wait_until="load", timeout=30_000)
        report["status"] = response.status if response else None
        if response is None or not response.ok:
            report["errors"].append(f"Page returned HTTP {report['status']}")
        # Scroll through the page to trigger lazy images, then restore the top.
        page.evaluate("""async () => {
          for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) {
            scrollTo(0, y);
            await new Promise(requestAnimationFrame);
            await new Promise(requestAnimationFrame);
          }
          scrollTo(0, 0);
        }""")
        try:
            page.wait_for_function("document.fonts.status === 'loaded'")
            page.wait_for_function(
                "Array.from(document.images).every(img => img.complete)"
            )
        except PlaywrightTimeoutError as error:
            report["errors"].append(f"Fonts/images did not settle: {error}")

        report.update(
            page.evaluate("""() => ({
          title: document.title,
          fonts: Array.from(document.fonts, f => ({
            family: f.family, weight: f.weight, style: f.style, status: f.status
          })).filter(f => f.status !== 'unloaded'),
          broken_images: Array.from(document.images).filter(i => !i.naturalWidth)
            .map(i => i.currentSrc || i.src),
          horizontal_overflow: document.documentElement.scrollWidth > innerWidth,
          text: document.body.innerText
        })""")
        )
        if any(font["status"] == "error" for font in report["fonts"]):
            report["errors"].append(
                "A font failed to load; typography uses a fallback."
            )
        if report["broken_images"]:
            report["errors"].append("Some images failed to load.")
        report["screenshot"] = str(output / f"{stem}.png")
        report["full_page_screenshot"] = str(output / f"{stem}-full.png")
        page.screenshot(path=report["screenshot"], animations="disabled")
        page.screenshot(
            path=report["full_page_screenshot"], full_page=True, animations="disabled"
        )
        print(report["screenshot"])
        print(report["full_page_screenshot"])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path", nargs="?", default="/", help="site route, e.g. /booking/"
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:5173/")
    parser.add_argument(
        "--viewport",
        type=viewport,
        action="append",
        help="WIDTHxHEIGHT; repeat for multiple sizes (default: desktop + mobile)",
    )
    parser.add_argument("--output", type=Path, default=WEBSITE / "test-results/inspect")
    parser.add_argument(
        "--channel",
        default="chromium",
        choices=("chromium", "chrome"),
        help="use Nix Chromium (default) or installed Google Chrome",
    )
    args = parser.parse_args()
    if urlsplit(args.path).scheme or urlsplit(args.path).netloc:
        parser.error("path must be a site route; choose the server with --base-url")
    if urlsplit(args.base_url).scheme not in ("http", "https"):
        parser.error("--base-url must use http or https")

    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(
            "Python Playwright is missing. Enter the repo's Nix dev shell and rerun."
        )

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    url = urljoin(args.base_url.rstrip("/") + "/", args.path.lstrip("/"))
    sizes = args.viewport or [viewport("1440x900"), viewport("390x844")]
    with dev_server(args.base_url, output), sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(channel=args.channel)
        except PlaywrightError as error:
            raise RuntimeError(
                "Chromium could not launch. Use the repo's Nix dev shell; "
                "on macOS, --channel chrome uses installed Google Chrome.\n"
                + str(error)
            ) from error
        try:
            reports = [capture(browser, url, size, output) for size in sizes]
            report_path = output / "report.json"
            report_path.write_text(
                json.dumps({"browser": browser.version, "pages": reports}, indent=2)
                + "\n"
            )
            print(report_path)
            for report in reports:
                for error in report["errors"]:
                    print(f"{report['viewport']}: {error}", file=sys.stderr)
            return int(any(report["errors"] for report in reports))
        finally:
            browser.close()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, KeyboardInterrupt) as error:
        sys.exit(str(error) or "Inspection interrupted.")
