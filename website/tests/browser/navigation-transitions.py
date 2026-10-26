"""Exercise real route transitions against a running dev or preview server.

Uses the same Python Playwright and browser as scripts/inspect-page.py.
"""

import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


INSTRUMENT = """(() => {
  window.trips = [];
  const native = document.startViewTransition?.bind(document);
  if (!native) return;
  const chosen = () => [...document.querySelectorAll('[data-transition-photo]')]
    .filter(node => node.style.viewTransitionName === 'show-print')
    .map(node => node.dataset.transitionPhoto);
  document.startViewTransition = update => {
    const row = {old: chosen(), started: performance.now()};
    window.trips.push(row);
    const transition = native(async () => {
      await update();
      row.new = chosen();
      row.updated = performance.now();
    });
    window.activeTransition = transition;
    transition.ready.then(() => row.ready = true, error => row.error = error.name);
    transition.finished.then(() => row.finished = true, error => row.error = error.name);
    return transition;
  };
})();"""
HERO = '2X9A9381-X4.jpg'
GALLERY = '2X9A9285-4K.jpg'


def print_selector(file):
    return f'[data-transition-photo="{file}"]'


def settled(page):
    page.wait_for_function("""!document.documentElement.hasAttribute('data-page-transition')
      && !document.querySelector('[style*="view-transition-name"]')""")


def traverse(page, destination, forward=False):
    count = page.evaluate('window.trips.length')
    if forward:
        page.go_forward()
    else:
        page.go_back()
    page.wait_for_url(destination)
    # History changes the URL before Kit has loaded the target route.
    page.wait_for_function('count => window.trips.length > count', arg=count)
    settled(page)


def open_home(page, base):
    page.goto(base, wait_until='networkidle')
    page.wait_for_function("document.fonts.status === 'loaded'")
    assert page.evaluate("typeof document.startViewTransition === 'function'")
    # Let the initial callboard arrival finish before moving its photograph.
    page.wait_for_timeout(900)


def activate(page, selector, keyboard=False, touch=False):
    link = page.locator(selector)
    link.scroll_into_view_if_needed()
    page.wait_for_timeout(800)  # A gallery print may have just entered the viewport.
    scroll = page.evaluate('scrollY')
    if keyboard:
        link.focus()
        link.press('Enter')
    elif touch:
        link.tap()
    else:
        link.click()
    return scroll


def history_check(browser, base, output, mobile):
    size = {'width': 390, 'height': 844} if mobile else {'width': 1440, 'height': 900}
    print(f'History and photo handoff at {size["width"]}px', flush=True)
    errors = []
    with browser.new_context(viewport=size, has_touch=mobile, is_mobile=mobile) as context:
        context.add_init_script(INSTRUMENT)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        open_home(page, base)
        activate(page, print_selector(HERO), keyboard=not mobile, touch=mobile)
        page.wait_for_url(base + 'shows/seussical/')
        page.wait_for_function('window.trips.at(-1).ready')
        assert page.evaluate('window.trips.at(-1).old') == [HERO]
        assert page.evaluate('window.trips.at(-1).new') == [HERO]
        # Sample every pseudo-element at the same elapsed time, preserving the
        # shorter page dissolve while the photo continues its 460ms journey.
        page.evaluate("""() => {
          for (const animation of document.getAnimations()) {
            if (animation.effect?.pseudoElement?.startsWith('::view-transition')) {
              animation.pause();
              animation.currentTime = 140;
            }
          }
        }""")
        page.screenshot(path=str(output / f'transition-{size["width"]}.png'))
        page.evaluate("window.activeTransition.skipTransition()")
        settled(page)
        assert page.evaluate('document.activeElement === document.body')
        activate(page, '.brand', touch=mobile)
        page.wait_for_url(base)
        settled(page)
        gallery_scroll = activate(page, print_selector(GALLERY), touch=mobile)
        page.wait_for_url(base + 'shows/seussical/')
        settled(page)
        assert page.evaluate('window.trips.at(-1).old') == [GALLERY]
        traverse(page, base)
        assert abs(page.evaluate('scrollY') - gallery_scroll) < 2
        # Back to the first show visit, then to the original home entry.
        traverse(page, base + 'shows/seussical/')
        traverse(page, base)
        assert page.evaluate('window.trips.at(-1).old') == [HERO]
        assert page.evaluate('window.trips.at(-1).new') == [HERO]
        assert page.evaluate('scrollY') < 5
        traverse(page, base + 'shows/seussical/', forward=True)
        assert page.evaluate('window.trips.at(-1).old') == [HERO]
        assert page.evaluate('window.trips.at(-1).new') == [HERO]
        assert not errors, errors
        return {'viewport': size, 'trips': page.evaluate('window.trips'), 'errors': errors}


def return_link_check(browser, base, output, mobile):
    size = {'width': 390, 'height': 844} if mobile else {'width': 1440, 'height': 900}
    print(f'Show return destinations at {size["width"]}px', flush=True)
    errors = []
    with browser.new_context(viewport=size, has_touch=mobile, is_mobile=mobile) as context:
        context.add_init_script(INSTRUMENT)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))

        def back_link(label, destination):
            expect(page.locator('.show-back')).to_have_text(label)
            assert page.locator('.show-back').evaluate('link => link.href') == destination

        def return_to(destination, key, scroll):
            count = page.evaluate('window.trips.length')
            activate(page, '.show-back', keyboard=not mobile, touch=mobile)
            page.wait_for_url(destination)
            page.wait_for_function('count => window.trips.length > count', arg=count)
            settled(page)
            assert page.evaluate('navigation.currentEntry.key') == key
            assert abs(page.evaluate('scrollY') - scroll) < 2

        open_home(page, base)
        for photo in (HERO, GALLERY, 'finn_photo_reel_2.jpg'):
            key = page.evaluate('navigation.currentEntry.key')
            selector = print_selector(photo)
            destination = page.locator(selector).evaluate('link => link.href')
            scroll = activate(page, selector, keyboard=not mobile, touch=mobile)
            page.wait_for_url(destination)
            settled(page)
            back_link('Home', base)
            if photo == HERO:
                page.screenshot(path=str(output / f'show-from-home-{size["width"]}.png'))
            if photo == GALLERY:
                # Browsing other shows retains the collection, even after reload.
                destination = page.locator('.pager-link--next').evaluate('link => link.href')
                activate(page, '.pager-link--next', touch=mobile)
                page.wait_for_url(destination)
                settled(page)
                page.reload(wait_until='networkidle')
                back_link('Home', base)
            return_to(base, key, scroll)
            if photo == HERO:
                assert page.evaluate('window.trips.at(-1).old') == [HERO]
                assert page.evaluate('window.trips.at(-1).new') == [HERO]

        page.locator('.site-header li a[href$="/resume/"]').click()
        page.wait_for_url(base + 'resume/')
        settled(page)
        key = page.evaluate('navigation.currentEntry.key')
        scroll = activate(page, '.credit-reel-link[href$="/shows/seussical/"]', touch=mobile)
        page.wait_for_url(base + 'shows/seussical/')
        settled(page)
        back_link('Theatre credits', base + 'resume/#credits-title')
        page.screenshot(path=str(output / f'show-from-credits-{size["width"]}.png'))
        page.reload(wait_until='networkidle')
        back_link('Theatre credits', base + 'resume/#credits-title')
        next_show = page.locator('.pager-link--next').evaluate('link => link.href')
        activate(page, '.pager-link--next', touch=mobile)
        page.wait_for_url(next_show)
        settled(page)
        back_link('Theatre credits', base + 'resume/#credits-title')
        return_to(base + 'resume/', key, scroll)

        # The same show can have different return destinations in its history.
        traverse(page, base + 'shows/seussical/', forward=True)
        back_link('Theatre credits', base + 'resume/#credits-title')
        traverse(page, next_show, forward=True)
        back_link('Theatre credits', base + 'resume/#credits-title')
        traverse(page, base + 'shows/seussical/')
        page.locator('.brand').click()
        page.wait_for_url(base)
        settled(page)
        activate(page, print_selector(HERO), touch=mobile)
        page.wait_for_url(base + 'shows/seussical/')
        settled(page)
        back_link('Home', base)
        traverse(page, base)
        traverse(page, base + 'shows/seussical/')
        back_link('Theatre credits', base + 'resume/#credits-title')

        # A fresh URL has a useful link home, even with an unrelated prior page.
        page.goto(base + 'booking/', wait_until='networkidle')
        page.goto(base + 'shows/seussical/', wait_until='networkidle')
        back_link('Home', base)
        page.locator('.show-back').click()
        page.wait_for_url(base)
        settled(page)
        assert not errors, errors
        return {'viewport': size, 'errors': errors}


def interruption_checks(browser, base):
    errors, results = [], []
    def checked(label):
        results.append(label)
        print(label, flush=True)

    with browser.new_context(viewport={'width': 1440, 'height': 900}) as context:
        context.add_init_script(INSTRUMENT)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))

        def start():
            open_home(page, base)
            activate(page, print_selector(HERO))
            page.wait_for_url(base + 'shows/seussical/')
            page.wait_for_function('window.trips.at(-1).ready')

        start()
        for index in range(10):
            route = 'performance-reel' if index % 2 == 0 else 'resume'
            page.locator(f'.site-header li a[href$="/{route}/"]').click()
        page.wait_for_url(base + 'resume/')
        settled(page)
        checked('ten rapid header navigations')

        start()
        page.emulate_media(reduced_motion='reduce')
        settled(page)
        count = page.evaluate('window.trips.length')
        page.locator('.brand').click()
        page.wait_for_url(base)
        assert page.evaluate('window.trips.length') == count
        page.emulate_media(reduced_motion='no-preference')
        checked('reduced motion during and before navigation')

        start()
        page.set_viewport_size({'width': 390, 'height': 844})
        settled(page)
        page.locator('.brand').click()
        page.wait_for_url(base)
        settled(page)
        page.set_viewport_size({'width': 1440, 'height': 900})
        checked('resize during animation and navigate again')

        open_home(page, base)
        page.evaluate('() => { HTMLImageElement.prototype.decode = () => new Promise(() => {}); }')
        activate(page, print_selector(HERO))
        page.wait_for_url(base + 'shows/seussical/')
        settled(page)
        trip = page.evaluate('window.trips.at(-1)')
        assert trip['updated'] - trip['started'] < 900, trip
        checked('stalled image decoding')

        context.route('**/media/**', lambda route: route.abort()
                      if route.request.url.endswith('/' + HERO) else route.continue_())
        open_home(page, base)
        assert page.locator(print_selector(HERO) + ' img').evaluate('(image) => image.naturalWidth') == 0
        activate(page, print_selector(HERO))
        page.wait_for_url(base + 'shows/seussical/')
        settled(page)
        assert page.evaluate('window.trips.at(-1).old') == []
        assert page.evaluate('window.trips.at(-1).new') == []
        context.unroute('**/media/**')
        checked('failed photo requests retain working links')

        for failure in ['unsupported', 'throws', 'duplicate name']:
            open_home(page, base)
            if failure == 'unsupported':
                page.evaluate('document.startViewTransition = undefined')
            elif failure == 'throws':
                page.evaluate("() => { document.startViewTransition = () => { throw new Error('unavailable'); }; }")
            else:
                page.evaluate("document.querySelector('main').style.viewTransitionName = 'show-print'")
            activate(page, print_selector(HERO))
            page.wait_for_url(base + 'shows/seussical/')
            page.evaluate("document.querySelector('main').style.removeProperty('view-transition-name')")
            settled(page)
            checked(f'{failure} fallback')

        open_home(page, base)
        page.locator('.hero-links a[href="#start-here"]').click()
        settled(page)
        assert page.evaluate('window.trips.length') == 0
        checked('same-page anchor keeps native navigation')
        assert not errors, errors

    with browser.new_context(java_script_enabled=False) as context:
        page = context.new_page()
        page.goto(base)
        page.locator(print_selector(HERO)).click()
        page.wait_for_url(base + 'shows/seussical/')
        assert page.locator('h1').inner_text() == 'Seussical'
        expect(page.locator('.show-back')).to_have_text('Home')
        page.locator('.show-back').click()
        page.wait_for_url(base)
        checked('photo and return links without JavaScript')
    with browser.new_context() as context:
        context.add_init_script("Object.defineProperty(window, 'navigation', { value: undefined })")
        context.add_init_script(INSTRUMENT)
        page = context.new_page()
        open_home(page, base)
        activate(page, print_selector(HERO))
        page.wait_for_url(base + 'shows/seussical/')
        settled(page)
        assert page.evaluate('window.trips.at(-1).old') == [HERO]
        traverse(page, base)
        assert page.evaluate('window.trips.at(-1).old') == []
        checked('no entry identity: clicked photo travels, Back dissolves')
        page.locator('.site-header li a[href$="/resume/"]').click()
        page.wait_for_url(base + 'resume/')
        settled(page)
        activate(page, '.credit-reel-link[href$="/shows/seussical/"]')
        page.wait_for_url(base + 'shows/seussical/')
        settled(page)
        expect(page.locator('.show-back')).to_have_text('Theatre credits')
        page.reload(wait_until='networkidle')
        expect(page.locator('.show-back')).to_have_text('Theatre credits')
        page.locator('.show-back').click()
        page.wait_for_url(base + 'resume/#credits-title')
        settled(page)
        checked('no entry identity: return link retains its collection after reload')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:5173/')
    parser.add_argument('--channel', choices=('chromium', 'chrome'), default='chromium')
    parser.add_argument('--output', type=Path, default=Path('test-results/navigation-transitions'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    base = args.base_url.rstrip('/') + '/'
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel=args.channel)
        try:
            report = {'browser': browser.version,
                      'history': [history_check(browser, base, args.output, mobile) for mobile in (False, True)],
                      'return_links': [return_link_check(browser, base, args.output, mobile) for mobile in (False, True)],
                      'checks': interruption_checks(browser, base)}
            path = args.output / 'report.json'
            path.write_text(json.dumps(report, indent=2) + '\n')
            print(path)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
