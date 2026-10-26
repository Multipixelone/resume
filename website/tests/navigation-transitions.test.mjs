import test from 'node:test';
import assert from 'node:assert/strict';
import { createPageTransitions } from '../src/lib/navigation-transitions.ts';

const deferred = () => {
  const { promise, resolve, reject } = Promise.withResolvers();
  return { promise, resolve, reject };
};
const flush = () => new Promise(setImmediate);
const url = path => new URL(path, 'https://example.test');

class Element extends EventTarget {
  dataset = {};
  properties = new Map();
  attributes = new Map();
  style = {
    setProperty: (name, value) => this.properties.set(name, value),
    removeProperty: name => this.properties.delete(name)
  };
  box = { width: 100, height: 100, top: 0, bottom: 100, left: 0, right: 100 };
  getBoundingClientRect() { return this.box; }
  querySelector() { return this.image; }
  closest() { return this; }
  setAttribute(name, value) { this.attributes.set(name, value); }
  removeAttribute(name) { this.attributes.delete(name); }
}

function photo(file, options = {}) {
  const print = new Element();
  print.dataset.transitionPhoto = file;
  print.image = Object.assign(new Element(), {
    complete: true, naturalWidth: 100, decode: () => Promise.resolve(), ...options
  });
  return print;
}

function fixture(t) {
  const document = Object.assign(new EventTarget(), {
    hidden: false,
    documentElement: new Element(),
    photos: [],
    querySelectorAll() { return this.photos; }
  });
  Object.defineProperty(document, 'images', { get: () => document.photos.map(print => print.image) });
  const reduced = Object.assign(new EventTarget(), { matches: false });
  const history = new EventTarget();
  const transitions = [];
  document.startViewTransition = callback => {
    const ready = deferred(), updated = deferred(), finished = deferred();
    const transition = {
      ready: ready.promise, updateCallbackDone: updated.promise, finished: finished.promise,
      skipped: false,
      skipTransition() { this.skipped = true; },
      failCapture() { ready.reject(new Error('capture skipped')); },
      finish() { finished.resolve(); },
      async update() {
        try {
          await callback();
          updated.resolve();
          ready.resolve();
        } catch (error) {
          updated.reject(error);
          ready.reject(error);
          finished.reject(error);
        }
      }
    };
    transitions.push(transition);
    return transition;
  };
  const globals = { document, window: { navigation: history }, Element,
    matchMedia: () => reduced, innerWidth: 1440, innerHeight: 900 };
  const originals = Object.fromEntries(Object.keys(globals).map(key => [key, Object.getOwnPropertyDescriptor(globalThis, key)]));
  for (const [key, value] of Object.entries(globals)) {
    Object.defineProperty(globalThis, key, { configurable: true, value });
  }
  const controller = createPageTransitions();
  t.after(() => {
    controller.destroy();
    for (const [key, descriptor] of Object.entries(originals)) {
      if (descriptor) Object.defineProperty(globalThis, key, descriptor);
      else delete globalThis[key];
    }
  });

  function navigate({ from = '/', to = '/shows/one/', fromKey = 'home', toKey = 'show',
    file = 'one.jpg', type = 'link', shallow = false } = {}) {
    const changed = new Event('currententrychange');
    changed.from = { key: fromKey, url: url(from).href };
    changed.navigationType = type === 'popstate' ? 'traverse' : 'push';
    history.currentEntry = { key: toKey, url: url(to).href };
    history.dispatchEvent(changed);
    const complete = deferred();
    const link = new Element();
    if (file) link.dataset.transitionPhoto = file;
    const gate = controller.navigate({ from: { url: url(from) }, to: { url: url(to) },
      shallow, type, event: { target: link }, complete: complete.promise });
    return { gate, complete, transition: transitions.at(-1) };
  }
  function clean(...prints) {
    assert.equal(document.documentElement.attributes.has('data-page-transition'), false);
    for (const print of prints) {
      assert.equal(print.properties.has('view-transition-name'), false);
      assert.equal(print.image.properties.has('view-transition-name'), false);
    }
  }
  return { document, reduced, controller, transitions, navigate, clean };
}

test('a stalled capture releases navigation within its budget, and its late callback does nothing', async t => {
  t.mock.timers.enable({ apis: ['setTimeout'] });
  const f = fixture(t), source = photo('one.jpg');
  f.document.photos = [source];
  const trip = f.navigate();
  t.mock.timers.tick(1000);
  await trip.gate;
  assert.equal(trip.transition.skipped, true);
  f.clean(source);
  // The route never settled. A callback arriving after cancellation must not wait for it.
  await trip.transition.update();
  f.clean(source);
});

test('capture failure releases the route before the browser invokes its update callback', async t => {
  const f = fixture(t), source = photo('one.jpg');
  f.document.photos = [source];
  const trip = f.navigate();
  trip.transition.failCapture();
  await trip.gate;
  f.clean(source);
  await trip.transition.update();
});

test('interrupting a stalled route also settles the browser update callback', async t => {
  const f = fixture(t);
  const trip = f.navigate();
  let updated = false;
  const update = trip.transition.update().then(() => { updated = true; });
  await trip.gate;
  f.controller.destroy();
  await flush();
  assert.equal(updated, true, 'a cancelled transition must not retain a pending route promise');
  await update;
  f.clean();
});

test('image decoding has one 120ms budget and navigation does not wait for the animation', async t => {
  t.mock.timers.enable({ apis: ['setTimeout'] });
  const f = fixture(t), source = photo('one.jpg');
  f.document.photos = [source];
  const trip = f.navigate();
  const update = trip.transition.update();
  await trip.gate;
  const target = photo('one.jpg', { decode: () => new Promise(() => {}) });
  f.document.photos = [target];
  trip.complete.resolve();
  await flush();
  t.mock.timers.tick(120);
  await update;
  assert.equal(target.properties.get('view-transition-name'), 'show-print');
  trip.transition.finish();
  await flush();
  f.clean(source, target);
});

test('a second navigation cancels decoding and late cleanup cannot erase its names', async t => {
  const f = fixture(t), source = photo('one.jpg');
  f.document.photos = [source];
  const first = f.navigate();
  const firstUpdate = first.transition.update();
  await first.gate;
  const target = photo('one.jpg', { decode: () => new Promise(() => {}) });
  f.document.photos = [target];
  first.complete.resolve();
  await flush();
  const second = f.navigate({ from: '/shows/one/', to: '/' });
  await firstUpdate;
  first.transition.finish();
  await flush();
  assert.equal(target.properties.get('view-transition-name'), 'show-print');
  assert.equal(f.document.documentElement.attributes.has('data-page-transition'), true);
  f.controller.destroy();
  await second.gate;
  f.clean(source, target);
});

test('an aborted route handles every transition rejection and removes temporary state', async t => {
  const f = fixture(t), source = photo('one.jpg');
  f.document.photos = [source];
  const trip = f.navigate();
  const update = trip.transition.update();
  await trip.gate;
  trip.complete.reject(new Error('navigation aborted'));
  await update;
  await flush();
  f.clean(source);
});

for (const interrupt of ['reduced motion', 'hidden document', 'destroy']) {
  test(`${interrupt} releases a pending capture and cleans both photo names`, async t => {
    const f = fixture(t), source = photo('one.jpg');
    f.document.photos = [source];
    const trip = f.navigate();
    if (interrupt === 'reduced motion') {
      f.reduced.matches = true;
      f.reduced.dispatchEvent(new Event('change'));
    } else if (interrupt === 'hidden document') {
      f.document.hidden = true;
      f.document.dispatchEvent(new Event('visibilitychange'));
    } else f.controller.destroy();
    await trip.gate;
    f.clean(source);
    assert.equal(trip.transition.skipped, true);
  });
}

test('unsupported and throwing transition APIs preserve ordinary navigation', async t => {
  const f = fixture(t), source = photo('one.jpg');
  f.document.photos = [source];
  f.document.startViewTransition = undefined;
  assert.equal(f.navigate().gate, undefined);
  f.clean(source);
  f.document.startViewTransition = () => { throw new Error('unavailable'); };
  await f.navigate().gate;
  f.clean(source);
});

test('shallow and same-page navigations do not capture a page', t => {
  const f = fixture(t);
  assert.equal(f.navigate({ shallow: true }).gate, undefined);
  assert.equal(f.navigate({ to: '/#photos-title' }).gate, undefined);
  assert.equal(f.transitions.length, 0);
});

test('broken, pending and offscreen images never become shared snapshots', async t => {
  const f = fixture(t);
  for (const options of [{ naturalWidth: 0 }, { complete: false }, { offscreen: true }]) {
    const source = photo('one.jpg', options);
    if (options.offscreen) source.box = { ...source.box, top: 1000, bottom: 1100 };
    f.document.photos = [source];
    const trip = f.navigate();
    assert.equal(source.properties.has('view-transition-name'), false);
    const update = trip.transition.update();
    await trip.gate;
    trip.complete.resolve();
    await update;
    trip.transition.finish();
    await flush();
    f.clean(source);
  }
});

test('Back and Forward choose the photo from that visit, including a visit with motion disabled', async t => {
  const f = fixture(t), first = photo('one.jpg'), second = photo('two.jpg');
  f.document.photos = [first, second];
  async function visit(options, expected) {
    const trip = f.navigate(options);
    const selected = f.document.photos.filter(print => print.properties.has('view-transition-name'));
    assert.deepEqual(selected.map(print => print.dataset.transitionPhoto), expected ? [expected] : []);
    const update = trip.gate ? trip.transition.update() : undefined;
    await trip.gate;
    trip.complete.resolve();
    await update;
    if (update) trip.transition.finish();
    await flush();
    f.clean(first, second);
  }
  // Both home entries and both show entries have identical URLs.
  f.reduced.matches = true;
  await visit({ fromKey: 'home-1', toKey: 'show-1', file: 'one.jpg' });
  f.reduced.matches = false;
  await visit({ from: '/shows/one/', to: '/', fromKey: 'show-1', toKey: 'home-2', file: null });
  await visit({ fromKey: 'home-2', toKey: 'show-2', file: 'two.jpg' }, 'two.jpg');
  await visit({ from: '/shows/one/', to: '/', fromKey: 'show-2', toKey: 'home-2', type: 'popstate' }, 'two.jpg');
  await visit({ fromKey: 'home-2', toKey: 'show-1', type: 'popstate' });
  await visit({ from: '/shows/one/', to: '/', fromKey: 'show-1', toKey: 'home-1', type: 'popstate' }, 'one.jpg');
  await visit({ fromKey: 'home-1', toKey: 'show-1', type: 'popstate' }, 'one.jpg');
});
