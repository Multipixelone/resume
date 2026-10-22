import type { Action } from 'svelte/action';

const SETTLE = 'cubic-bezier(.16, 1, .3, 1)';
const SWING: [number, number][] = [[0, 0], [.18, 1], [.42, -.45], [.65, .18], [.84, -.06], [1, 0]];

/** One opening gesture: lay down a headshot, then let its taped photo catch. */
export const callboardEntrance: Action<HTMLElement> = (node) => {
  if (typeof matchMedia !== 'function') return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const animations = new Set<Animation>();
  const print = node.querySelector<HTMLElement>('.hero-contact-print .photo-mat');
  let observer: IntersectionObserver | undefined;
  let entered = reduced.matches;

  function play(layer: Element | null, frames: Keyframe[], timing: KeyframeAnimationOptions) {
    if (!layer || typeof layer.animate !== 'function' || reduced.matches) return;
    const animation = layer.animate(frames, { fill: 'backwards', ...timing });
    animations.add(animation);
    const release = () => {
      animations.delete(animation);
      animation.onfinish = animation.oncancel = null;
    };
    animation.onfinish = animation.oncancel = release;
  }

  function settle() {
    for (const animation of animations) {
      animation.onfinish = animation.oncancel = null;
      animation.cancel();
    }
    animations.clear();
  }

  function arrive() {
    if (entered || reduced.matches || document.hidden) return;
    entered = true;
    observer?.disconnect();
    play(node.querySelector('.portrait-backing'), [
      { translate: '-10px 6px', rotate: '-2deg' },
      { translate: '0 0', rotate: '0deg' }
    ], { id: 'callboard-backing', duration: 440, easing: SETTLE });
    play(node.querySelector('.portrait-assembly'), [
      { translate: '16px -12px', rotate: '-3deg', scale: '1.025' },
      { translate: '0 0', rotate: '0deg', scale: '1' }
    ], { id: 'callboard-portrait', duration: 620, delay: 60, easing: SETTLE });
    // The shadow contracts as the print meets the board. It is the only painted
    // part of the opening, bounded to one card for less than a second.
    const card = node.querySelector('.portrait-card');
    if (card) play(card, [
      { boxShadow: '0 8px 12px rgb(43 37 32 / .06), 0 30px 42px -12px rgb(43 37 32 / .22)' },
      { boxShadow: getComputedStyle(card).boxShadow }
    ], { id: 'callboard-weight', duration: 620, delay: 60, easing: SETTLE });
    play(print, [
      { rotate: '7deg', offset: 0 },
      { rotate: '-2.5deg', offset: .4 },
      { rotate: '.8deg', offset: .7 },
      { rotate: '0deg', offset: 1 }
    ], { id: 'callboard-stage', duration: 640, delay: 140, easing: 'ease-in-out' });
  }

  function swing(direction = 1) {
    if (!print || reduced.matches || document.hidden) return;
    if ([...animations].some(animation => animation.id === 'tape-swing')) return;
    for (const animation of animations) {
      if (animation.id === 'callboard-stage') animation.cancel();
    }
    play(print, SWING.map(([offset, turn]) => ({
      offset, rotate: `${turn * 5 * direction}deg`, easing: 'cubic-bezier(.37, 0, .63, 1)'
    })), { id: 'tape-swing', duration: 920 });
  }

  function touchPrint(event: PointerEvent) {
    if (event.pointerType === 'touch' || !finePointer.matches || !print) return;
    const bounds = print.getBoundingClientRect();
    swing(event.clientX < bounds.left + bounds.width / 2 ? 1 : -1);
  }

  function focusPrint() {
    if (print?.matches(':focus-visible')) swing();
  }

  function syncPreference() {
    if (reduced.matches || document.hidden) {
      // A hidden tab or a preference change settles the whole composition,
      // including its Web Animations, and does not replay it on return.
      entered = true;
      observer?.disconnect();
      settle();
    }
  }

  if (!entered && typeof IntersectionObserver === 'function') {
    observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) arrive();
    }, { threshold: .15 });
    observer.observe(node);
  }

  print?.addEventListener('pointerenter', touchPrint);
  print?.addEventListener('focus', focusPrint);
  reduced.addEventListener('change', syncPreference);
  document.addEventListener('visibilitychange', syncPreference);

  return {
    destroy() {
      observer?.disconnect();
      print?.removeEventListener('pointerenter', touchPrint);
      print?.removeEventListener('focus', focusPrint);
      reduced.removeEventListener('change', syncPreference);
      document.removeEventListener('visibilitychange', syncPreference);
      settle();
    }
  };
};

/** Gallery prints land corner-first, then flatten against the callboard. */
export const printEntrance: Action<HTMLElement> = (node) => {
  if (typeof matchMedia !== 'function' || typeof IntersectionObserver !== 'function'
    || typeof node.animate !== 'function') return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  if (reduced.matches || document.hidden) return;

  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const shadow = node.querySelector<HTMLElement>('.photo-arrival-shadow');
  const animations = new Set<Animation>();
  let entered = false;

  function release() {
    observer.disconnect();
    reduced.removeEventListener('change', syncPreference);
    document.removeEventListener('visibilitychange', syncPreference);
    node.removeEventListener('focusin', settle);
    node.removeEventListener('pointerdown', settle);
  }

  function settle() {
    entered = true;
    release();
    for (const animation of animations) {
      animation.onfinish = animation.oncancel = null;
      animation.cancel();
    }
    animations.clear();
  }

  function play(layer: HTMLElement, frames: Keyframe[], duration: number) {
    const animation = layer.animate(frames, {
      id: layer === node ? 'print-landing' : 'print-contact-shadow',
      duration,
      easing: 'linear'
    });
    animations.add(animation);
    animation.onfinish = animation.oncancel = () => {
      animations.delete(animation);
      animation.onfinish = animation.oncancel = null;
      if (!animations.size) release();
    };
  }

  function arrive() {
    if (entered || reduced.matches || document.hidden) return;
    entered = true;
    if (node.contains(document.activeElement)) {
      settle();
      return;
    }

    // The existing print owns hover/focus transforms. Its outer layer supplies
    // the landing, keeping the caption and the pointer response independent.
    const direction = parseFloat(getComputedStyle(node).getPropertyValue('--rotation')) < 0 ? -1 : 1;
    const compact = !finePointer.matches || window.innerWidth < 640;
    const travel = compact ? 14 : 28;
    const turn = compact ? 1.2 : 3;
    const duration = compact ? 580 : 740;
    play(node, [
      {
        transform: `perspective(1000px) translate3d(${-direction * travel * .4}px, ${-travel}px, 0) rotateX(${compact ? 5 : 9}deg) rotateY(${-direction * turn}deg) rotateZ(${direction * turn}deg) scale(${compact ? .99 : 1.025})`,
        offset: 0, easing: 'cubic-bezier(.2, .75, .25, 1)'
      },
      {
        transform: `perspective(1000px) translate3d(0, 0, 0) rotateX(-.6deg) rotateY(0deg) rotateZ(${-direction * .18}deg) scale(1)`,
        offset: .72, easing: SETTLE
      },
      { transform: 'perspective(1000px) translate3d(0, 0, 0) rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(1)', offset: 1 }
    ], duration);

    // A prepainted shadow loses weight as the paper makes contact. Only opacity
    // animates, so scrolling never repaints a large blurred shadow each frame.
    if (shadow) play(shadow, [
      { opacity: .8, offset: 0, easing: SETTLE },
      { opacity: .12, offset: .72 },
      { opacity: 0, offset: 1 }
    ], duration);
  }

  function syncPreference() {
    if (reduced.matches || document.hidden) settle();
  }

  // Let enough paper enter the viewport to see it land. A capped pixel inset
  // works even for tall prints and at high zoom. Keep observing during the
  // landing so a quick scroll past it also cancels the animation.
  const inset = Math.round(Math.min(160, window.innerHeight * .18));
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) arrive();
      else if (entered) settle();
    }
  }, { rootMargin: `0px 0px -${inset}px 0px`, threshold: 0 });

  observer.observe(node);
  reduced.addEventListener('change', syncPreference);
  document.addEventListener('visibilitychange', syncPreference);
  node.addEventListener('focusin', settle);
  node.addEventListener('pointerdown', settle, { passive: true });

  return { destroy: settle };
};

/** Paper responds to the hand, independently of its arrival. */
export const paperMotion: Action<HTMLElement> = (node) => {
  if (typeof matchMedia !== 'function') return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  let frame = 0;
  let clientX = 0;
  let clientY = 0;

  function resetPointer() {
    cancelAnimationFrame(frame);
    frame = 0;
    for (const property of ['--pointer-x', '--pointer-y', '--pointer-rx', '--pointer-ry']) {
      node.style.removeProperty(property);
    }
  }

  function paintPointer() {
    frame = 0;
    if (reduced.matches || !finePointer.matches || document.hidden) return;
    const bounds = node.getBoundingClientRect();
    if (!bounds.width || !bounds.height) return;
    const x = Math.max(-1, Math.min(1, (clientX - bounds.left) / bounds.width * 2 - 1));
    const y = Math.max(-1, Math.min(1, (clientY - bounds.top) / bounds.height * 2 - 1));
    node.style.setProperty('--pointer-x', `${x * 5}px`);
    node.style.setProperty('--pointer-y', `${y * 4}px`);
    node.style.setProperty('--pointer-rx', `${-y * 1.5}deg`);
    node.style.setProperty('--pointer-ry', `${x * 2}deg`);
  }

  function move(event: PointerEvent) {
    if (reduced.matches || !finePointer.matches || event.pointerType === 'touch') return;
    clientX = event.clientX;
    clientY = event.clientY;
    if (!frame) frame = requestAnimationFrame(paintPointer);
  }

  node.addEventListener('pointermove', move, { passive: true });
  node.addEventListener('pointerleave', resetPointer);
  node.addEventListener('pointercancel', resetPointer);
  reduced.addEventListener('change', resetPointer);
  finePointer.addEventListener('change', resetPointer);
  document.addEventListener('visibilitychange', resetPointer);

  return {
    destroy() {
      node.removeEventListener('pointermove', move);
      node.removeEventListener('pointerleave', resetPointer);
      node.removeEventListener('pointercancel', resetPointer);
      reduced.removeEventListener('change', resetPointer);
      finePointer.removeEventListener('change', resetPointer);
      document.removeEventListener('visibilitychange', resetPointer);
      resetPointer();
    }
  };
};
