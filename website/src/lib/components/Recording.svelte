<script lang="ts">
  import { tick } from 'svelte';
  import { sitePath } from '$lib/paths';
  import Arrow from '$lib/components/Arrow.svelte';
  import type { Recording, ShowVideo } from '$lib/types';

  // A clip on its sheet, introduced by the song in Cooper Bold,
  // then small labels for the show, role and year. `label` sits above a title that is
  // not a song (the film). The clip to start with gets a ticket tucked under its sheet.
  let { video, label = '', eager = false }: { video: ShowVideo | Recording; label?: string; eager?: boolean } = $props();
  let start = $derived('start' in video && video.start);
  let credit = $derived('show' in video ? video.show : undefined);
  let loaded = $state(false);
  let posterFailed = $state(false);
  let posterQuality = $state('hq720');
  let player = $state<HTMLIFrameElement>();

  function fallbackPoster() {
    if (posterQuality === 'hq720') posterQuality = 'hqdefault';
    else posterFailed = true;
  }

  async function loadVideo(event: MouseEvent) {
    // Preserve native link behavior for new tabs and for visitors without JavaScript.
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    loaded = true;
    await tick();
    player?.focus();
  }
</script>

<section class="recording" class:recording--start={start} aria-labelledby={`recording-${video.id}`}>
  <div class="recording-caption">
    <hgroup>
      {#if label}<p class="recording-label">{label}</p>{/if}
      <h2 id={`recording-${video.id}`}>{video.title}</h2>
      {#if credit}
        <p class="recording-credits">
          {#if credit.path}<a href={sitePath(credit.path)}>{credit.title}</a>{:else}<span>{credit.title}</span>{/if}
          <!-- A cabaret singer billed as "Self" is the convention on paper, but says nothing here. -->
          {#if credit.character !== 'Self'}<span class="sep" aria-hidden="true">·</span><span>{credit.character}</span>{/if}
          {#if credit.year}<span class="sep" aria-hidden="true">·</span><span>{credit.year}</span>{/if}
        </p>
      {/if}
    </hgroup>
    <a class="recording-watch" href={`https://www.youtube.com/watch?v=${video.id}`} aria-label={`Watch ${video.title} on YouTube`}>Watch on YouTube <Arrow /></a>
  </div>
  {#if start}
    <p class="recording-start"><span class="ticket-card">Start here</span></p>
  {/if}
  <div class="video-mat">
    {#if loaded}
      <iframe
        bind:this={player}
        src={`https://www.youtube-nocookie.com/embed/${video.id}?autoplay=1`}
        title={video.title}
        allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
        referrerpolicy="strict-origin-when-cross-origin"
      ></iframe>
    {:else}
      <a class="recording-poster" href={`https://www.youtube.com/watch?v=${video.id}`} onclick={loadVideo} aria-label={`Play video: ${video.title}`}>
        <span class="recording-play" aria-hidden="true">
          <span class="recording-play-icon"><svg viewBox="0 0 24 24" width="22" height="22"><path d="m9 5 10 7-10 7Z" fill="currentColor" /></svg></span>
          <span class="recording-play-label">Play</span>
        </span>
        <span class="recording-still">
          {#if !posterFailed}
            <img
              src={`https://i.ytimg.com/vi/${video.id}/${posterQuality}.jpg`}
              alt=""
              loading={eager ? 'eager' : 'lazy'}
              fetchpriority={eager ? 'high' : 'auto'}
              class:recording-still--letterboxed={posterQuality === 'hqdefault'}
              onerror={fallbackPoster}
              onload={(event) => { if ((event.currentTarget as HTMLImageElement).naturalWidth <= 120) fallbackPoster(); }}
            />
          {:else}
            <span class="recording-no-preview">Preview unavailable. Select to play.</span>
          {/if}
        </span>
      </a>
    {/if}
  </div>
</section>
