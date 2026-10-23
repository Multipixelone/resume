<script lang="ts">
  import { film } from '$lib/media';
  import { sitePath } from '$lib/paths';
  import Arrow from '$lib/components/Arrow.svelte';
  import PageHead from '$lib/components/PageHead.svelte';
  import Recording from '$lib/components/Recording.svelte';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
</script>

<PageHead title="Performance reel | Finn Rutis" />

<header class="page-heading"><h1>Performance reel</h1></header>
<div class="recordings">
  {#each data.recordings as video, index (video.id)}
    <Recording {video} eager={index === 0} />
  {/each}
  <Recording video={film} label="Film" />
</div>

<!-- Watching leads to the resume: the reel ends on the theatre PDF. -->
<section class="reel-resume" aria-labelledby="reel-resume-title">
  <h2 id="reel-resume-title">Resume</h2>
  <div class="download-actions">
    <a class="primary-link" href={sitePath(data.download.pdf)} rel="external" download>Download resume <span class="file-label">(PDF)</span> <Arrow dir="down" /></a>
    <a href={sitePath(data.composite)} rel="external" download>Resume with headshot <span class="file-label">(PDF)</span></a>
  </div>
</section>
