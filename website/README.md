# Finn Rutis portfolio

SvelteKit with adapter-static. Run commands from this `website/` directory, with
Node >=22.12 and the repository's adjacent `metadata/`, `lib/`, and `variants.toml`
available. This is not a standalone copy of the canonical content.

| Command | Purpose |
| --- | --- |
| `npm ci` | Install the locked dependencies |
| `npm run dev -- --host 127.0.0.1` | Local development |
| `npm run check` | Generate SvelteKit types and check Svelte/TypeScript |
| `npm run inspect` | Capture the rendered page at desktop and mobile sizes, with font/load diagnostics |
| `npm test` | Real-parser canonical ingestion and configuration checks |
| `npm run build` | Prerender every route to `build/`, plus `404.html`; no SPA fallback |
| `env SITE_BASE=/resume npm run build` | Build for repository Pages rather than domain root |
| `env SITE_BASE=/resume npm run preview -- --host 127.0.0.1` | Preview that repository-base build |
| `npm run dev:fixture` | Separate, unshipped CurrentProjects browser test harness |
| `python3 scripts/gen_social_card.py` | Redraw `static/social-card.png` after changing its copy or palette (needs Pillow, in the dev shell) |

See [portfolio site handoff](../docs/portfolio-site.md) for artifact assembly,
font permissions, media-credit dependencies, and the assigned validation matrix.
Building the site alone does not create PDF/PNG downloads; Phase 3 assembles them.

Licensed `.woff2` files dropped into the gitignored `fonts-local/` (same names as in
`src/styles/fonts.css`) are served same-origin by both dev servers, so local pages and
impeccable live need no CORS grant from `fonts.finnrut.is`. Faces without a local copy
load remotely. Builds always use the remote URLs; restart dev after adding a file.

The Contact page's business card uses committed transparent Performance artwork
and a lazy Three.js scene. `npm test` includes its motion and orientation math.
See [business cards](../docs/business-cards.md#contact-page-rendering) for texture
refresh commands and mobile tilt behavior. Testing tilt from a phone requires an
HTTPS origin; a plain-HTTP LAN address cannot expose device orientation.

## Rendered page inspection

Inside the repo's Nix dev shell, run `npm run inspect` from `website/` (or
`npm --prefix website run inspect` from the repo root). Python Playwright and its
matching Chromium are already provided by the shell; no npm browser package or
browser download is needed.

The command reuses the server at `http://127.0.0.1:5173/` if present. Otherwise it
starts Vite and stops only that temporary server when finished. It captures a
viewport PNG and a `-full.png` at 1440x900 and 390x844 after scrolling lazy images
into view and waiting for images and fonts. Reduced motion keeps entrance
animations out of the capture. Open the viewport PNGs first for legible text,
then the full captures for the rest of the page, and read the printed
`report.json`: it includes loaded font faces, page errors, failed requests, HTTP
errors, broken images, overflow, and rendered text. A page error, failed font, or
broken image returns a nonzero status; request and console diagnostics remain in
the report for review.

```sh
npm run inspect -- /booking/
npm run inspect -- / --viewport 1280x800 --viewport 375x812
npm run inspect -- / --output test-results/home
# Start the static preview separately, then capture its actual base path:
npm run inspect -- /resume/ --base-url http://127.0.0.1:4173/
```

For interactive checks, keep Vite running separately and use Python Playwright
directly. This example reads the bio's actual layout and captures only that text:

```sh
python3 - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(channel="chromium")
    try:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("http://127.0.0.1:5173/", wait_until="load")
        page.wait_for_function("document.fonts.status === 'loaded'")
        bio = page.locator(".bio-block")
        print(bio.bounding_box())
        bio.screenshot(path="test-results/bio.png")
    finally:
        browser.close()
PY
```

On macOS, `npm run inspect -- --channel chrome` uses installed Google Chrome if needed.
This works independently of the browser tools attached to an agent session.

Licensed faces that fail remotely need their authorized local copies in
`fonts-local/`; see the font notes above. Review typography only when the report
shows the needed faces loaded.
