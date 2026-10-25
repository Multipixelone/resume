<script lang="ts">
  import { sitePath } from '$lib/paths';
  import Arrow from '$lib/components/Arrow.svelte';
  import PerformanceNextSteps from '$lib/components/PerformanceNextSteps.svelte';
  import PageHead from '$lib/components/PageHead.svelte';
  import Recording from '$lib/components/Recording.svelte';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
</script>

<PageHead title="Performance reel | Finn Rutis" />

<header class="page-heading reel-heading">
  <h1>Performance reel</h1>
  <a class="recording-watch" href={sitePath(data.download.pdf)} rel="external" download="Finn Rutis Artistic Resume.pdf">Download resume <span class="file-label">(PDF)</span> <Arrow dir="down" /></a>
</header>
<div class="recordings">
  {#each data.recordings as video, index (video.id)}
    <Recording {video} eager={index === 0} />
  {/each}
  <Recording video={data.film} label="Film" />
</div>

<PerformanceNextSteps variant="resume" resumePdf={data.download.pdf} composite={data.composite} />

<style>
  .reel-heading { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 1rem 2rem; }
</style>
