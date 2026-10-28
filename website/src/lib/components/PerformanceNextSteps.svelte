<script lang="ts">
  import { sitePath } from '#lib/paths.js';
  import Arrow from './Arrow.svelte';
  import type { Download } from '#lib/types.ts';

  // The homepage offers the reel; the reel offers the optional headshot PDF.
  let { resume, variant = 'reel-and-resume', headshot }: {
    resume: Download;
    variant?: 'reel-and-resume' | 'resume';
    headshot?: Download;
  } = $props();
  const id = $props.id();
</script>

<section class="performance-next" aria-labelledby={`${id}-title`}>
  <h2 id={`${id}-title`}>{variant === 'resume' ? 'Resume' : 'Reel & resume'}</h2>
  <div class="next-actions">
    <svg class="perforation perforation-vertical" aria-hidden="true" focusable="false"><line x1="1" y1="0" x2="1" y2="100%" /></svg>
    <svg class="perforation perforation-horizontal" aria-hidden="true" focusable="false"><line x1="0" y1="1" x2="100%" y2="1" /></svg>
    {#if variant === 'reel-and-resume'}
      <a class="lead-link" href={sitePath('/performance-reel/')}><span>Full reel</span> <Arrow /></a>
    {/if}
    <a class:lead-link={variant === 'resume'} href={sitePath(resume.pdf)} rel="external" download={resume.filename}><span>Download resume <span class="file-label">(PDF)</span></span> <Arrow dir="down" /></a>
    {#if variant === 'resume' && headshot}
      <a href={sitePath(headshot.pdf)} rel="external" download={headshot.filename}><span>{headshot.title} <span class="file-label">(PDF)</span></span> <Arrow dir="down" /></a>
    {/if}
  </div>
</section>

<style>
  .performance-next {
    --paper-angle: -.65deg;
    /* The slip measures itself, so larger text stacks it as surely as a narrow window does. */
    container: performance-next / inline-size;
    position: relative;
    isolation: isolate;
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.3fr);
    align-items: center;
    /* The row gap only shows once the slip stacks. */
    gap: 1.25rem 2rem;
    max-width: 56rem;
    margin: var(--next-steps-space, var(--space-section)) auto 0;
    padding: clamp(1.5rem, 4vw, 3rem);
    /* Paper and perforation share one transform; only the words stay level. */
    rotate: var(--paper-angle);
  }

  .performance-next::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    background: var(--paper-shade);
    box-shadow: 0 5px 15px var(--shadow);
    pointer-events: none;
  }

  h2 {
    rotate: calc(-1 * var(--paper-angle));
    font-family: var(--font-display);
    font-size: clamp(1.875rem, 3vw, 2.5rem);
    letter-spacing: -.025em;
    max-width: 10ch;
    min-width: 0;
    overflow-wrap: anywhere;
  }

  .next-actions {
    position: relative;
    display: grid;
    gap: .5rem;
    padding-inline-start: 2rem;
    min-width: 0;
  }

  /* No viewBox scaling or border dash fitting: every mark is 2 CSS px,
     followed by a 4 CSS px gap, clipped at the end of the paper seam. */
  .perforation { position: absolute; inset-block-start: 0; inset-inline-start: 0; pointer-events: none; fill: none; stroke: var(--muted); stroke-width: 1; stroke-dasharray: 2 4; }
  .perforation-vertical { width: 2px; height: 100%; }
  .perforation-horizontal { display: none; width: 100%; height: 2px; }

  a {
    rotate: calc(-1 * var(--paper-angle));
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    min-height: 44px;
    padding-block: .5rem;
    color: var(--accent-hover);
  }

  a > span { min-width: 0; overflow-wrap: anywhere; }

  .lead-link { font-size: 1.25rem; font-weight: 600; }

  /* Under 35rem the links can't keep one line beside the heading. */
  @container performance-next (width < 35rem) {
    h2, .next-actions { grid-column: 1 / -1; }
    h2 { max-width: none; }
    .next-actions { padding: 1rem 0 0; }
    .perforation-vertical { display: none; }
    .perforation-horizontal { display: block; }
  }

  @media (forced-colors: active) {
    .performance-next { --paper-angle: 0deg; border: 1px solid CanvasText; }
    .performance-next::before { display: none; }
  }
</style>
