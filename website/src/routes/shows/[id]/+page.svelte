<script lang="ts">
  import { afterNavigate, snapshot } from '$app/navigation';
  import { sitePath } from '#lib/paths.js';
  import Arrow from '#lib/components/Arrow.svelte';
  import CoverPrint from '#lib/components/CoverPrint.svelte';
  import PageHead from '#lib/components/PageHead.svelte';
  import PerformanceNextSteps from '#lib/components/PerformanceNextSteps.svelte';
  import Recording from '#lib/components/Recording.svelte';
  import ReelPrint from '#lib/components/ReelPrint.svelte';
  import type { PageProps } from './$types.js';

  let { data }: PageProps = $props();
  let reel = $derived(data.reel);
  type Origin = { kind: 'home' | 'credits'; key?: string };
  let origin = $state<Origin | null>(null);
  // A direct visit has a real link home, including without JavaScript. Once the
  // visitor arrives from a collection, remember that collection for this visit.
  let back = $derived(origin?.kind === 'credits'
    ? { href: `${sitePath('/resume/')}#credits-title`, label: 'Theatre credits' }
    : { href: sitePath('/'), label: 'Home' });

  snapshot<Origin | null>({
    id: 'show-return-origin',
    capture: () => origin,
    restore: value => { origin = value?.kind === 'home' || value?.kind === 'credits' ? value : null; }
  });

  afterNavigate(({ from, type }) => {
    // Kit restores this entry's snapshot after afterNavigate. If none exists,
    // use Home rather than carrying an unrelated visit's return destination.
    if (type === 'enter' || type === 'popstate') {
      origin = null;
      return;
    }
    const route = from?.route.id;
    if (from && (route === '/' || route === '/resume')) {
      const historyNavigation = window.navigation;
      const current = historyNavigation?.currentEntry;
      const previous = current && historyNavigation.entries().find(entry =>
        entry.index === current.index - 1 && entry.url === from.url.href);
      origin = { kind: route === '/' ? 'home' : 'credits', key: previous?.key };
    } else if (route !== '/shows/[id]') {
      origin = null;
    }
    // The show pager keeps the original collection, rather than making the
    // previous show the new return destination.
  });

  function returnToOrigin(event: MouseEvent) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey
      || event.shiftKey || event.altKey || !origin?.key) return;
    const historyNavigation = window.navigation;
    const current = historyNavigation?.currentEntry;
    const destination = historyNavigation?.entries().find(entry => entry.key === origin?.key);
    if (!current || !destination?.url || destination.index < 0 || destination.index >= current.index) return;
    const url = new URL(destination.url);
    const expected = new URL(back.href, location.href);
    if (url.origin !== expected.origin || url.pathname !== expected.pathname) return;
    // Traverse only a verified collection entry. Kit restores its scroll and
    // the shared photo transition, while modified clicks retain a normal link.
    event.preventDefault();
    history.go(destination.index - current.index);
  }
</script>

<PageHead title={`${reel.title} | Finn Rutis`} description={`Photos from ${reel.title} (${reel.company}).`} />

<header class="show-heading">
  <a class="text-link show-back" href={back.href} onclick={returnToOrigin}><Arrow dir="back" /> {back.label}</a>
  <h1>{reel.title}</h1>
  <dl class="now-credits">
    <!-- A cabaret singer billed as "Self" is the convention on paper, but says nothing here. -->
    {#if reel.character !== 'Self'}
      <div><dt>Role</dt><dd>{reel.character}</dd></div>
    {/if}
    <div><dt>Company</dt><dd>{reel.company}</dd></div>
    <div><dt>Directed by</dt><dd>{reel.director}</dd></div>
  </dl>
</header>

<div class="show-reel">
  {#each reel.photos as photo, index (photo.file)}
    <ReelPrint {photo} {index} solo={reel.photos.length === 1} />
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

<PerformanceNextSteps resume={data.resumeDownload} />
