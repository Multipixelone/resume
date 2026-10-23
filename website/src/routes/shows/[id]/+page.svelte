<script lang="ts">
  import { sitePath } from '$lib/paths';
  import Arrow from '$lib/components/Arrow.svelte';
  import CoverPrint from '$lib/components/CoverPrint.svelte';
  import PageHead from '$lib/components/PageHead.svelte';
  import Recording from '$lib/components/Recording.svelte';
  import ReelPrint from '$lib/components/ReelPrint.svelte';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
  let reel = $derived(data.reel);
  // Credits on the resume lead back there; revues are reached from the homepage spread.
  let back = $derived(reel.on_resume
    ? { href: `${sitePath('/resume/')}#credits-title`, label: 'Theatre credits' }
    : { href: `${sitePath('/')}#photos-title`, label: 'On stage' });
</script>

<PageHead title={`${reel.title} | Finn Rutis`} description={`Photos from ${reel.title} (${reel.company}).`} />

<header class="show-heading">
  <a class="text-link show-back" href={back.href}><Arrow dir="back" /> {back.label}</a>
  <h1>{reel.title}</h1>
  <dl class="now-credits">
    <!-- A cabaret singer billed as "Self" is the convention on paper, but says nothing here. -->
    {#if reel.character !== 'Self'}
      <div><dt>Role</dt><dd>{reel.character}</dd></div>
    {/if}
    <div><dt>Venue</dt><dd>{reel.company}</dd></div>
    <div><dt>Directed by</dt><dd>{reel.director}</dd></div>
  </dl>
</header>

<div class="show-reel">
  {#each reel.photos as photo, index (photo.file)}
    <ReelPrint {photo} {index} />
  {/each}
</div>

<!-- The page heading already names the show and role, so these carry only the song. -->
{#each reel.videos as video (video.id)}
  <Recording {video} />
{/each}

{#if data.previous || data.next}
  <nav class="show-pager" aria-label="More shows">
    {#if data.previous}
      <a class="pager-link pager-link--previous" href={sitePath(data.previous.path)}>
        <CoverPrint photo={data.previous.cover} />
        <span><span class="pager-label">Previous show</span><span class="pager-title">{data.previous.title}</span></span>
      </a>
    {/if}
    {#if data.next}
      <a class="pager-link pager-link--next" href={sitePath(data.next.path)}>
        <CoverPrint photo={data.next.cover} />
        <span><span class="pager-label">Next show</span><span class="pager-title">{data.next.title}</span></span>
      </a>
    {/if}
  </nav>
{/if}
