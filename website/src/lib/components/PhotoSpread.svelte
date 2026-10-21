<script lang="ts">
  import { onMount, tick } from 'svelte';
  import PhotoPrint from './PhotoPrint.svelte';
  import type { Photo, PhotoNote } from '$lib/types';

  let { photos }: { photos: Photo[] } = $props();

  // The bubble only replaces visible captions on fine hover pointers, after JS has run.
  let enhanced = $state(false);
  let note = $state<PhotoNote>();
  let spread: HTMLElement;
  let bubble: HTMLElement;

  const DOT = 7; // Collapsed dot radius; its center sits on the pointer.
  const EDGE = 12; // Keep the bubble this far from the viewport edge.
  const CLOSE_MS = 260; // Matches the clip-path transition in site.css.

  onMount(() => {
    const hover = matchMedia('(hover: hover) and (pointer: fine)');
    const still = matchMedia('(prefers-reduced-motion: reduce)');
    const pointer = { x: 0, y: 0 };
    const pos = { x: 0, y: 0 };
    let anchor: HTMLElement | null = null;
    let byFocus = false;
    let frame = 0;
    let last = 0;
    let hideTimer: ReturnType<typeof setTimeout> | undefined;

    const matFor = (target: EventTarget | null) =>
      target instanceof Element ? target.closest<HTMLElement>('.photo-mat[data-note]') : null;

    // Keyboard focus parks the bubble inside the photo's lower left corner instead of at the pointer.
    function goal() {
      if (!byFocus || !anchor) return pointer;
      const rect = anchor.getBoundingClientRect();
      return { x: rect.left + 28, y: rect.bottom - 28 };
    }

    // Grow down and right from the pointer, flipping when that would run off screen.
    function place(x: number, y: number) {
      const { offsetWidth: w, offsetHeight: h } = bubble;
      const flipX = x - DOT + w + EDGE > innerWidth;
      const flipY = y - DOT + h + EDGE > innerHeight;
      bubble.classList.toggle('flip-x', flipX);
      bubble.classList.toggle('flip-y', flipY);
      const left = Math.max(EDGE, flipX ? x + DOT - w : x - DOT);
      const top = Math.max(EDGE, flipY ? y + DOT - h : y - DOT);
      bubble.style.transform = `translate3d(${left}px, ${top}px, 0)`;
    }

    // Ease toward the target so the bubble trails the pointer a little, frame-rate independent.
    function step(now: number) {
      const ease = still.matches || !last ? 1 : 1 - Math.pow(0.55, (now - last) / 16.7);
      last = now;
      const { x, y } = goal();
      pos.x += (x - pos.x) * ease;
      pos.y += (y - pos.y) * ease;
      place(pos.x, pos.y);
      frame = requestAnimationFrame(step);
    }
    function run() {
      if (!frame) { last = 0; frame = requestAnimationFrame(step); }
    }
    function halt() {
      cancelAnimationFrame(frame);
      frame = 0;
    }

    async function show(mat: HTMLElement, focus: boolean) {
      clearTimeout(hideTimer);
      anchor?.classList.remove('is-bubbled');
      anchor = mat;
      byFocus = focus;
      if (!focus) mat.classList.add('is-bubbled');
      note = photos.find(photo => photo.file === mat.dataset.note)?.note;
      await tick();
      if (anchor !== mat) return;
      if (!bubble.classList.contains('is-shown')) {
        Object.assign(pos, goal());
        place(pos.x, pos.y);
        bubble.classList.add('is-shown');
        void bubble.offsetWidth; // Commit the collapsed dot so the open state transitions from it.
      }
      bubble.classList.add('is-open');
      run();
    }
    function hide(mat: HTMLElement | null) {
      if (!anchor || (mat && mat !== anchor)) return;
      anchor.classList.remove('is-bubbled');
      anchor = null;
      byFocus = false;
      bubble.classList.remove('is-open');
      clearTimeout(hideTimer);
      hideTimer = setTimeout(() => { bubble.classList.remove('is-shown'); halt(); }, still.matches ? 0 : CLOSE_MS);
    }

    const over = (event: PointerEvent) => {
      if (!hover.matches || event.pointerType === 'touch') return;
      pointer.x = event.clientX;
      pointer.y = event.clientY;
      const mat = matFor(event.target);
      if (mat && (mat !== anchor || byFocus)) show(mat, false);
    };
    const move = (event: PointerEvent) => {
      pointer.x = event.clientX;
      pointer.y = event.clientY;
    };
    const out = (event: PointerEvent) => {
      const mat = matFor(event.target);
      if (mat && !byFocus && !mat.contains(event.relatedTarget as Node | null)) hide(mat);
    };
    const focusIn = (event: FocusEvent) => {
      const mat = matFor(event.target);
      if (hover.matches && mat?.matches(':focus-visible')) show(mat, true);
    };
    const focusOut = () => { if (byFocus) hide(anchor); };
    const key = (event: KeyboardEvent) => { if (event.key === 'Escape') hide(anchor); };
    const sync = () => {
      enhanced = hover.matches;
      if (!enhanced) hide(anchor);
    };

    sync();
    hover.addEventListener('change', sync);
    spread.addEventListener('pointerover', over);
    spread.addEventListener('pointermove', move);
    spread.addEventListener('pointerout', out);
    spread.addEventListener('focusin', focusIn);
    spread.addEventListener('focusout', focusOut);
    addEventListener('keydown', key);
    return () => {
      hover.removeEventListener('change', sync);
      spread.removeEventListener('pointerover', over);
      spread.removeEventListener('pointermove', move);
      spread.removeEventListener('pointerout', out);
      spread.removeEventListener('focusin', focusIn);
      spread.removeEventListener('focusout', focusOut);
      removeEventListener('keydown', key);
      clearTimeout(hideTimer);
      halt();
    };
  });
</script>

<div class="photo-spread" class:photo-spread--bubbles={enhanced} bind:this={spread}>
  {#each photos as photo (photo.file)}<PhotoPrint {photo} />{/each}
</div>
<!-- Visual duplicate of the focused or hovered photo's caption note; assistive tech reads the caption. -->
<div class="photo-bubble" bind:this={bubble} aria-hidden="true">
  <div class="photo-bubble-body">
    {#if note?.title}<span class="photo-note-title">{note.title}</span>{/if}
    {#if note?.role}<span class="photo-note-role">{note.role}</span>{/if}
    {#if note?.blurb}<span class="photo-note-blurb">{note.blurb}</span>{/if}
  </div>
</div>
