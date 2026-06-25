import shutil
import sys
import tempfile
from datetime import datetime, timezone
try:
    from patchright.sync_api import sync_playwright  # type: ignore[assignment]
except ImportError:
    from playwright.sync_api import sync_playwright  # type: ignore[assignment]
    print("patchright not found, using playwright", file=sys.stderr)
try:
    from roomieorder.purchase import BasePurchaser, looks_like
    BLOCK_STATUS_CODES = BasePurchaser._BLOCK_STATUS_CODES
except Exception:
    def looks_like(text, url, markers):
        h = f"{text}\n{url}".lower()
        return any(m in h for m in markers)
    BLOCK_STATUS_CODES = (403, 429)
CHALLENGE_MARKERS = ("just a moment", "access denied", "are you a human", "verify you are human", "recaptcha", "cf-chl-bypass", "pardon our interruption", "enter the characters")
LOGIN_PATHS, CHALLENGE_URLS = ("/login", "/authwall", "/signin"), ("/cdn-cgi/challenge/", "cf-chl-bypass")
def is_blocked(page, response):
    try:
        status = response.status if response else 0
    except Exception:
        status = 0
    url = page.url.lower()
    if status in BLOCK_STATUS_CODES or any(x in url for x in CHALLENGE_URLS):
        return True
    try:
        text = page.title() + "\n" + page.locator("body").inner_text(timeout=3_000)
    except Exception:
        text = ""
    return looks_like(text, url, CHALLENGE_MARKERS)
def screenshot(page):
    path = f"/tmp/job_fetch_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.png"
    try:
        page.screenshot(path=path, full_page=True)
    except Exception as e:
        print(f"screenshot failed: {e}", file=sys.stderr)
    return path
def fetch(url, headless):
    profile = tempfile.mkdtemp(prefix="jobfetch_")
    try:
        with sync_playwright() as pw:
            ctx = pw.chromium.launch_persistent_context(
                user_data_dir=profile,
                headless=headless,
                args=["--disable-blink-features=AutomationControlled", "--disable-backgrounding-occluded-windows", "--disable-background-timer-throttling", "--disable-renderer-backgrounding"],
                ignore_default_args=["--enable-automation"],
                no_viewport=True,
            )
            try:
                page = ctx.new_page()
                resp = page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                try:
                    page.wait_for_load_state("networkidle", timeout=15_000)
                except Exception:
                    pass
                page.wait_for_timeout(3_000)
                if any(p in page.url.lower() for p in LOGIN_PATHS):
                    return "login", screenshot(page)
                if is_blocked(page, resp):
                    return "blocked", None
                print("--- JSON-LD ---")
                for raw in page.locator("script[type='application/ld+json']").all_inner_texts():
                    print(raw)
                print("--- BODY TEXT ---")
                print(page.inner_text("body"))
                return "ok", None
            finally:
                ctx.close()
    finally:
        shutil.rmtree(profile, ignore_errors=True)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: fetch_job.py <URL>", file=sys.stderr); sys.exit(3)
    url = sys.argv[1]
    try:
        status, shot = fetch(url, True)
        if status == "ok": sys.exit(0)
        if status == "login": print(shot, file=sys.stderr); sys.exit(2)
        print("blocked in headless, retrying headed", file=sys.stderr)
        status, shot = fetch(url, False)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr); sys.exit(3)
    if status == "ok": sys.exit(0)
    print(shot or "", file=sys.stderr); sys.exit(1 if status == "blocked" else 2)
