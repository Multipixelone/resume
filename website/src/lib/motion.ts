import type { Action } from 'svelte/action';

type PaperMotionOptions = { delay?: number };

/** A visible, static composition first; only its marked paper layers move. */
export const paperMotion: Action<HTMLElement, PaperMotionOptions | undefined> = (node, options) => {
  if (typeof matchMedia !== 'function') return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const animations = new Set<Animation>();
  let observer: IntersectionObserver | undefined;
  let frame = 0;
  let pointerX = 0;
  let pointerY = 0;
  let entered = reduced.matches;
  let delay = arrivalDelay(options);

  function arrivalDelay(value: PaperMotionOptions | undefined) {
    const requested = value?.delay ?? 0;
    return Number.isFinite(requested) ? Math.min(160, Math.max(0, requested)) : 0;
  }

  function resetPointer() {
    cancelAnimationFrame(frame);
    frame = 0;
    pointerX = pointerY = 0;
    for (const property of ['--pointer-x', '--pointer-y', '--pointer-rx', '--pointer-ry']) {
      node.style.removeProperty(property);
    }
  }

  function cancelArrival() {
    for (const animation of animations) {
      animation.onfinish = null;
      animation.cancel();
    }
    animations.clear();
  }

  function arrive() {
    if (entered || reduced.matches) return;
    entered = true;
    observer?.disconnect();

    for (const layer of node.querySelectorAll<HTMLElement>('[data-paper-arrival]')) {
      if (typeof layer.animate !== 'function') continue;
      const animation = layer.animate([
        { translate: '0 18px', rotate: '1deg', offset: 0 },
        { translate: '0 -2px', rotate: '-0.15deg', offset: 0.76 },
        { translate: '0 0', rotate: '0deg', offset: 1 }
      ], {
        duration: 700,
        delay,
        easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
        fill: 'backwards'
      });
      animations.add(animation);
      animation.onfinish = () => {
        animations.delete(animation);
        animation.onfinish = null;
      };
    }
  }

  function paintPointer() {
    frame = 0;
    if (reduced.matches || !finePointer.matches) return;
    node.style.setProperty('--pointer-x', `${pointerX * 5}px`);
    node.style.setProperty('--pointer-y', `${pointerY * 4}px`);
    node.style.setProperty('--pointer-rx', `${-pointerY * 1.5}deg`);
    node.style.setProperty('--pointer-ry', `${pointerX * 2}deg`);
  }

  function move(event: PointerEvent) {
    if (reduced.matches || !finePointer.matches || event.pointerType === 'touch') return;
    const bounds = node.getBoundingClientRect();
    if (!bounds.width || !bounds.height) return;
    pointerX = Math.max(-1, Math.min(1, (event.clientX - bounds.left) / bounds.width * 2 - 1));
    pointerY = Math.max(-1, Math.min(1, (event.clientY - bounds.top) / bounds.height * 2 - 1));
    if (!frame) frame = requestAnimationFrame(paintPointer);
  }

  function syncPreference() {
    resetPointer();
    if (reduced.matches) {
      // Switching to reduced motion settles immediately and never replays entry.
      entered = true;
      observer?.disconnect();
      cancelArrival();
    }
  }

  if (!entered && typeof IntersectionObserver === 'function') {
    observer = new IntersectionObserver((entries) => {
      if (entries.some(entry => entry.isIntersecting)) arrive();
    }, { threshold: 0.12 });
    observer.observe(node);
  }

  node.addEventListener('pointermove', move, { passive: true });
  node.addEventListener('pointerleave', resetPointer);
  node.addEventListener('pointercancel', resetPointer);
  reduced.addEventListener('change', syncPreference);
  finePointer.addEventListener('change', syncPreference);

  return {
    update(next) { delay = arrivalDelay(next); },
    destroy() {
      entered = true;
      observer?.disconnect();
      node.removeEventListener('pointermove', move);
      node.removeEventListener('pointerleave', resetPointer);
      node.removeEventListener('pointercancel', resetPointer);
      reduced.removeEventListener('change', syncPreference);
      finePointer.removeEventListener('change', syncPreference);
      resetPointer();
      cancelArrival();
    }
  };
};
