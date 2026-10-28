<script lang="ts">
  // The error page in dev and the prerendered build/404.html (routes/404): a wrong turn
  // still leads to the reel and the theatre resume.
  import { page } from '$app/state';
  import { sitePath } from '#lib/paths.js';
  import Arrow from '#lib/components/Arrow.svelte';
  import PageHead from '#lib/components/PageHead.svelte';
  import type { Download } from '#lib/types.ts';

  let { status }: { status: number } = $props();
  let heading = $derived(status === 404 ? 'Page not found' : 'Page unavailable');
  let resume = $derived(page.data.resumeDownload as Download | undefined);
</script>

<PageHead title={`${heading} | Finn Rutis`} />
<svelte:head><meta name="robots" content="noindex" /></svelte:head>

<header class="page-heading"><h1>{heading}</h1></header>
<div class="error-links">
  <a class="text-link" href={sitePath('/performance-reel/')}>Watch me perform <Arrow /></a>
  {#if resume}
    <a class="text-link" href={sitePath(resume.pdf)} rel="external" download={resume.filename}>Download resume <span class="file-label">(PDF)</span> <Arrow dir="down" /></a>
  {/if}
  <a class="text-link" href={sitePath('/')}><Arrow dir="back" /> Return home</a>
</div>
