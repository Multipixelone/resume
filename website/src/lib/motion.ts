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

/** Paper responds to the hand. Scrolling never makes the reader wait for it. */
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
