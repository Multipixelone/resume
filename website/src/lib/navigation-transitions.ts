import type { OnNavigate } from '$app/navigation';

const PHOTO = '[data-transition-photo]';

function visible(node: HTMLElement) {
  const box = node.getBoundingClientRect();
  return box.width > 0 && box.height > 0 && box.bottom > 0 && box.right > 0
    && box.top < innerHeight && box.left < innerWidth;
}

function findPhoto(file: string | undefined) {
  if (!file) return;
  return [...document.querySelectorAll<HTMLElement>(PHOTO)]
    .find(node => node.dataset.transitionPhoto === file && visible(node));
}

function namePhoto(node: HTMLElement | undefined, active: boolean) {
  if (!node) return;
  // Capture the photograph separately from its paper border: the hero print
  // has a name strip, so stretching the whole mat would double the image.
  for (const [element, name] of [[node, 'show-print'], [node.querySelector('img'), 'show-photo']] as const) {
    if (active) element?.style.setProperty('view-transition-name', name);
    else element?.style.removeProperty('view-transition-name');
  }
}

async function decodeVisibleImages() {
  const images = [...document.images].filter(image => visible(image));
  for (const image of images) image.loading = 'eager';
  let timer: ReturnType<typeof setTimeout> | undefined;
  // A lazy image may not start loading while the browser holds the old frame.
  // Warm only the visible images, with one budget for the whole new view.
  await Promise.race([
    Promise.allSettled(images.map(image => image.decode())),
    new Promise<void>(done => { timer = setTimeout(done, 120); })
  ]);
  clearTimeout(timer);
}

/** Let Kit own navigation, scroll and focus; carry one visible print between pages. */
export function createPageTransitions() {
  // Remember the chosen photograph for the return trip, including shows with
  // several homepage prints. Filenames identify photographs, not productions.
  const visits = new Map<string, string>();
  let stop: (() => void) | undefined;

  function navigate(navigation: OnNavigate) {
    stop?.();
    const { from, to } = navigation;
    if (!from || !to || navigation.shallow || from.url.pathname === to.url.pathname
      || !document.startViewTransition || document.hidden
      || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const trip = JSON.stringify([from.url.pathname, to.url.pathname]);
    const reverseTrip = JSON.stringify([to.url.pathname, from.url.pathname]);
    const link = navigation.type === 'link' && navigation.event.target instanceof Element
      ? navigation.event.target.closest<HTMLAnchorElement>('a') : null;
    const file = link?.dataset.transitionPhoto ?? link?.dataset.transitionLink
      ?? (navigation.type === 'popstate' ? visits.get(trip) : undefined);
    const candidate = findPhoto(file);
    const source = candidate?.querySelector('img')?.naturalWidth ? candidate : undefined;
    const root = document.documentElement;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    let target: HTMLElement | undefined;
    let transition: ViewTransition | undefined;
    let stopped = false;

    function cleanup() {
      if (stopped) return;
      stopped = true;
      namePhoto(source, false);
      namePhoto(target, false);
      reduced.removeEventListener('change', interrupt);
      document.removeEventListener('visibilitychange', interrupt);
      if (stop === cancel) {
        root.removeAttribute('data-page-transition');
        stop = undefined;
      }
    }

    function cancel() {
      transition?.skipTransition();
      cleanup();
    }

    function interrupt() {
      if (reduced.matches || document.hidden) cancel();
    }

    stop = cancel;
    root.setAttribute('data-page-transition', '');
    namePhoto(source, true);
    reduced.addEventListener('change', interrupt);
    document.addEventListener('visibilitychange', interrupt);

    return new Promise<void>(resolve => {
      try {
        transition = document.startViewTransition(async () => {
          // Release Kit only after the old page has been captured. Its complete
          // promise includes the DOM update and native scroll/focus restoration.
          resolve();
          await navigation.complete;
          if (stopped) return;
          await decodeVisibleImages();
          if (stopped || !source || !file) return;

          target = findPhoto(file);
          const image = target?.querySelector('img');
          if (!target || !image) return;

          if (!image.complete || !image.naturalWidth) return;

          namePhoto(target, true);
          visits.set(trip, file);
          visits.set(reverseTrip, file);
        });
        // Skipped and interrupted transitions are ordinary navigation outcomes.
        void transition.ready.catch(() => {});
        void transition.finished.then(cleanup, cleanup);
      } catch {
        cleanup();
        resolve();
      }
    });
  }

  return { navigate, destroy: () => stop?.() };
}
