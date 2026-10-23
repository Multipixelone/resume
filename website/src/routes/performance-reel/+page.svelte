<script lang="ts">
  import { film } from '$lib/media';
  import PerformanceNextSteps from '$lib/components/PerformanceNextSteps.svelte';
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

<PerformanceNextSteps variant="resume" resumePdf={data.download.pdf} composite={data.composite} />
