import type { OnNavigate } from '$app/navigation';

const PHOTO = '[data-transition-photo]';
const TRANSITION_TIMEOUT = 1000;
const MAX_VISITS = 64;

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

async function decodeVisibleImages(signal: AbortSignal) {
  if (signal.aborted) return;
  const images = [...document.images].filter(image => visible(image));
  for (const image of images) image.loading = 'eager';
  let timer: ReturnType<typeof setTimeout> | undefined;
  let release: () => void = () => {};
  // A lazy image may not start loading while the browser holds the old frame.
  // Warm only the visible images, with one budget for the whole new view.
  try {
    await Promise.race([
      Promise.allSettled(images.map(image => image.decode())),
      new Promise<void>(done => {
        release = done;
        timer = setTimeout(done, 120);
        signal.addEventListener('abort', release, { once: true });
      })
    ]);
  } finally {
    clearTimeout(timer);
    signal.removeEventListener('abort', release);
  }
}

/** Let Kit own navigation, scroll and focus; carry one visible print between pages. */
export function createPageTransitions() {
  // Observe native entry identity without writing Kit's history state. A route
  // pair is not enough: two visits to one show can start at different prints.
  // Older browsers still animate clicked prints; history uses the page dissolve.
  const historyNavigation = typeof window !== 'undefined' ? window.navigation : undefined;
  let previousEntry: NavigationHistoryEntry | undefined;
  function entryChanged(event: NavigationCurrentEntryChangeEvent) {
    if (event.navigationType) previousEntry = event.from;
  }
  historyNavigation?.addEventListener('currententrychange', entryChanged);
  const visits = new Map<string, string>();
  let stop: (() => void) | undefined;
  let destroyed = false;

  function navigate(navigation: OnNavigate) {
    stop?.();
    const { from, to } = navigation;
    if (destroyed || !from || !to) return;

    const entry = historyNavigation?.currentEntry;
    let trip: string | undefined;
    let reverseTrip: string | undefined;
    if (previousEntry && entry && previousEntry.url === from.url.href && entry.url === to.url.href) {
      trip = JSON.stringify([previousEntry.key, from.url.href, entry.key, to.url.href]);
      reverseTrip = JSON.stringify([entry.key, to.url.href, previousEntry.key, from.url.href]);
    }
    const link = navigation.type === 'link' && navigation.event.target instanceof Element
      ? navigation.event.target.closest<HTMLAnchorElement>('a') : null;
    const clickedFile = link?.dataset.transitionPhoto ?? link?.dataset.transitionLink;
    const file = clickedFile ?? (navigation.type === 'popstate' && trip ? visits.get(trip) : undefined);
    // Remember successful visits even when motion is disabled or an image is
    // still loading. An interrupted animation does not undo a completed visit.
    if (clickedFile && trip && reverseTrip) {
      void navigation.complete.then(() => {
        if (destroyed) return;
        visits.set(trip, clickedFile);
        visits.set(reverseTrip, clickedFile);
        while (visits.size > MAX_VISITS) visits.delete(visits.keys().next().value!);
      }, () => {});
    }
    if (navigation.shallow || from.url.pathname === to.url.pathname
      || typeof document.startViewTransition !== 'function' || document.hidden
      || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const candidate = findPhoto(file);
    const sourceImage = candidate?.querySelector('img');
    const source = sourceImage?.complete && sourceImage.naturalWidth ? candidate : undefined;
    const root = document.documentElement;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const cancellation = new AbortController();
    const cancelled = new Promise<void>(resolve => {
      cancellation.signal.addEventListener('abort', () => resolve(), { once: true });
    });
    let target: HTMLElement | undefined;
    let transition: ViewTransition | undefined;
    let stopped = false;
    let releaseNavigation: () => void = () => {};
    let timer: ReturnType<typeof setTimeout> | undefined;

    function cleanup() {
      if (stopped) return;
      stopped = true;
      releaseNavigation();
      clearTimeout(timer);
      cancellation.abort();
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
      releaseNavigation = resolve;
      // Capturing the old frame is an enhancement, never an indefinite gate on
      // Kit. Also bound a stalled DOM update and release its image decode wait.
      timer = setTimeout(cancel, TRANSITION_TIMEOUT);
      try {
        transition = document.startViewTransition(async () => {
          // Release Kit only after the old page has been captured. Its complete
          // promise includes the DOM update and native scroll/focus restoration.
          resolve();
          if (stopped) return;
          await Promise.race([navigation.complete, cancelled]);
          if (stopped) return;
          await decodeVisibleImages(cancellation.signal);
          if (stopped || !source || !file) return;

          target = findPhoto(file);
          const image = target?.querySelector('img');
          if (!target || !image) return;

          if (!image.complete || !image.naturalWidth) return;

          namePhoto(target, true);
        });
        // Skipped and interrupted transitions are ordinary navigation outcomes.
        void transition.ready.catch(cancel);
        void transition.updateCallbackDone.catch(cancel);
        void transition.finished.then(cleanup, cleanup);
      } catch {
        cleanup();
        resolve();
      }
    });
  }

  return {
    navigate,
    destroy() {
      destroyed = true;
      stop?.();
      visits.clear();
      historyNavigation?.removeEventListener('currententrychange', entryChanged);
    }
  };
}
