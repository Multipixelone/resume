"""Compare cold photo downloads, restoring master-only img tags for the baseline.

Run from website/: python3 scripts/measure-images.py build
Requires Playwright and Chromium. JavaScript is disabled in both runs to isolate
image selection in the same prerendered HTML; scroll the whole page for lazy photos.
"""
import functools
import http.server
import json
import re
import sys
import threading
from playwright.sync_api import sync_playwright

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=sys.argv[1]))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height, dpr in ((375, 812, 2), (1440, 900, 1), (375, 812, 3), (1440, 900, 2)):
        for baseline in (True, False):
            context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=dpr, java_script_enabled=False)
            page = context.new_page()
            if baseline:
                def restore_master(route):
                    response = route.fetch()
                    body = re.sub(r' (?:srcset|sizes)="[^"]*"', '', response.text())
                    route.fulfill(response=response, body=body)
                page.route(url, restore_master)
            photos = {}
            def record(response):
                if '/media/' in response.url and response.request.resource_type == 'image':
                    assert response.status == 200, response.url
                    photos[response.url] = len(response.body())
            page.on('response', record)
            page.goto(url, wait_until='networkidle')
            initial = sum(photos.values())
            for y in range(0, page.evaluate('document.documentElement.scrollHeight') + height, height // 2):
                page.evaluate('(y) => window.scrollTo(0, y)', y)
                page.wait_for_timeout(100)
            page.wait_for_load_state('networkidle')
            assert page.locator('img[srcset]').count() > 0 or baseline
            assert page.locator('img').evaluate_all('(imgs) => imgs.every(i => i.complete && i.naturalWidth > 0)')
            print(json.dumps(dict(width=width, dpr=dpr, mode='before' if baseline else 'after', initial_bytes=initial, full_page_bytes=sum(photos.values()), files=len(photos))))
            if not baseline and dpr in (1, 2):
                page.screenshot(path=f'/tmp/resume-{width}-{dpr}.png', full_page=True)
                # Resolve the active sizes expression as a CSS width and compare to layout.
                print(page.locator('img[srcset]').evaluate_all('''imgs => imgs.map(i => {
                  const sizes = i.sizes.split(/, (?![^()]*\\))/);
                  const active = sizes.find(s => !s.startsWith('(') || matchMedia(s.slice(0, s.indexOf(')') + 1)).matches);
                  const expr = active.startsWith('(') ? active.slice(active.indexOf(')') + 2) : active;
                  const probe = document.createElement('div'); probe.style.width = expr;
                  document.body.append(probe); const expected = probe.getBoundingClientRect().width; probe.remove();
                  return {file: i.currentSrc.split('/media/')[1], actual: i.clientWidth, sizes: expected};
                })'''))
            context.close()
    browser.close()
server.shutdown()
