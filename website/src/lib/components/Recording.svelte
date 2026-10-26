<script lang="ts">
  import { tick } from 'svelte';
  import { sitePath } from '#lib/paths.js';
  import Arrow from '#lib/components/Arrow.svelte';
  import type { Recording, ShowVideo } from '#lib/types.ts';

  // A clip on its sheet, introduced by the song in Cooper Bold,
  // then small labels for the show, role and year. `label` sits above a title that is
  // not a song (the film). The clip to start with gets a ticket tucked under its sheet.
  let { video, label = '', eager = false, flyer = false }: { video: ShowVideo | Recording; label?: string; eager?: boolean; flyer?: boolean } = $props();
  let start = $derived('start' in video && video.start);
  let credit = $derived('show' in video ? video.show : undefined);
  let loaded = $state(false);
  let posterFailed = $state(false);
  let posterQuality = $state('hq720');
  let player = $state<HTMLIFrameElement>();

  function fallbackPoster() {
    if (video.poster) posterFailed = true;
    else if (posterQuality === 'hq720') posterQuality = 'hqdefault';
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

{#snippet startTicket()}
  <p class="recording-start"><span class="ticket-card">Start here</span></p>
{/snippet}

{#snippet youtubeLink()}
  <a class="recording-watch" href={`https://www.youtube.com/watch?v=${video.id}`} aria-label={`Watch ${video.title} on YouTube`}>Watch on YouTube <Arrow /></a>
{/snippet}

<section class="recording" class:recording--start={start} class:recording--flyer={flyer} class:recording--playing={loaded} aria-labelledby={`recording-${video.id}`}>
  {#if flyer && start}{@render startTicket()}{/if}
  <div class="recording-caption">
    <hgroup>
      {#if label}<p class="recording-label">{label}</p>{/if}
      <h2 id={`recording-${video.id}`}>{video.title}</h2>
      {#if credit || video.film || video.duration}
        <p class="recording-credits">
          {#if credit}
            {#if credit.path}<a href={sitePath(credit.path)}>{credit.title}</a>{:else}<span>{credit.title}</span>{/if}
            <!-- A cabaret singer billed as "Self" is the convention on paper, but says nothing here. -->
            {#if credit.character !== 'Self'}<span class="sep" aria-hidden="true">·</span><span>{credit.character}</span>{/if}
            {#if credit.year}<span class="sep" aria-hidden="true">·</span><span>{credit.year}</span>{/if}
          {:else if video.film}
            <span>{video.film.character}</span><span class="sep" aria-hidden="true">·</span><span>{video.film.company}</span><span class="sep" aria-hidden="true">·</span><span>Directed by {video.film.director}</span>
          {/if}
          {#if video.duration}
            {#if credit || video.film}<span class="sep" aria-hidden="true">·</span>{/if}
            <span class="recording-duration" aria-label={`${Math.floor(video.duration / 60)} minutes ${video.duration % 60} seconds`}>{Math.floor(video.duration / 60)}:{String(video.duration % 60).padStart(2, '0')}</span>
          {/if}
        </p>
      {/if}
    </hgroup>
    {#if !flyer}{@render youtubeLink()}{/if}
  </div>
  {#if start && !flyer}{@render startTicket()}{/if}
  <div class="recording-media">
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
              src={video.poster ? sitePath(video.poster) : `https://i.ytimg.com/vi/${video.id}/${posterQuality}.jpg`}
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
    {#if flyer}<span class="photo-fastener photo-tape recording-tape" aria-hidden="true"></span>{/if}
  </div>
  {#if flyer}
    <div class="recording-links">
      <a class="text-link" href={sitePath('/performance-reel/')}>More performances <Arrow /></a>
      {@render youtubeLink()}
    </div>
  {/if}
</section>

<style>
  /* A programme slip tucked beneath a taped print. The caption stays level;
     the print flexes at its fastening, then lies flat for playback. */
  .recording--flyer {
    --flyer-gap: 1.5rem;
    --recording-angle: 2deg;
    position: relative;
    isolation: isolate;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: var(--flyer-gap);
    max-width: none;
    padding: clamp(1rem, 3cqi, 2.5rem);
  }
  .recording--flyer::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    background: var(--ticket-paper);
    box-shadow: 0 5px 15px var(--shadow);
    rotate: -2deg;
    pointer-events: none;
  }
  .recording--flyer .recording-start { margin: -.75rem 0 0; }
  .recording--flyer .recording-start .ticket-card { padding-bottom: .5rem; }
  .recording--flyer .recording-caption { padding: 0; }
  .recording--flyer .recording-caption h2 {
    max-width: 9ch;
    font-size: clamp(2.25rem, 5cqi, 3.5rem);
    font-weight: 900;
    line-height: 1.05;
    text-wrap: balance;
  }
  .recording--flyer .recording-credits { line-height: 1.8; }
  .recording--flyer .recording-media {
    position: relative;
    min-width: 0;
    margin-block: .5rem;
    rotate: var(--recording-angle);
    transform-origin: 50% .25rem;
  }
  .recording--flyer .video-mat {
    min-width: 0;
    padding: .5rem .5rem 1.5rem;
    border: 0;
    background: var(--paper);
    box-shadow: 0 2px 4px rgb(43 37 32 / .1), 0 12px 24px -12px rgb(43 37 32 / .32);
    transform-origin: 50% .25rem;
  }
  .recording-tape { left: 46%; }
  /* The ticket catches the lower print border, clear of the performance. */
  .recording--flyer .recording-play {
    inset-block-start: auto;
    inset-block-end: -1.25rem;
    inset-inline-start: .5rem;
    translate: none;
    rotate: calc(-1 * var(--recording-angle));
  }
  .recording-links {
    display: flex;
    flex-wrap: wrap;
    gap: .25rem 1.5rem;
    align-items: baseline;
    border-top: 1px dashed var(--muted);
    padding-top: .75rem;
  }
  .recording--flyer.recording--playing { --recording-angle: 0deg; }

  @container home-recording (width >= 48rem) {
    .recording--flyer {
      grid-template-columns: minmax(0, .85fr) minmax(0, 1.5fr);
      grid-template-rows: auto 1fr auto;
      column-gap: calc(var(--flyer-gap) * 2);
    }
    .recording--flyer::before {
      grid-area: 1 / 1 / 4 / 2;
      inset: -1.5rem -3rem -1.5rem -1.5rem;
    }
    .recording--flyer .recording-start { grid-area: 1 / 1; }
    .recording--flyer .recording-caption { grid-area: 2 / 1; align-self: start; }
    .recording--flyer .recording-media { grid-area: 1 / 2 / 4 / 3; align-self: center; }
    .recording-links { grid-area: 3 / 1; flex-direction: column; gap: 0; }
  }

  @media (prefers-reduced-motion: no-preference) {
    .recording--flyer .recording-media { transition: rotate 280ms cubic-bezier(.16, 1, .3, 1); }
    .recording--flyer .video-mat { transition: transform 280ms cubic-bezier(.16, 1, .3, 1), box-shadow 280ms ease; }
    .recording--flyer:not(.recording--playing):has(.recording-poster:focus-visible) .video-mat {
      transform: perspective(1000px) rotateX(6deg);
      box-shadow: 0 4px 8px rgb(43 37 32 / .08), 0 25px 35px -14px rgb(43 37 32 / .32);
    }
    .recording--flyer .recording-poster:is(:hover, :focus-visible) .recording-play { translate: 0 -3px; }
    .recording--flyer .recording-poster:active .recording-play { translate: none; }
  }
  @media (hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference) {
    .recording--flyer:not(.recording--playing):has(.recording-poster:hover) .video-mat {
      transform: perspective(1000px) rotateX(6deg);
      box-shadow: 0 4px 8px rgb(43 37 32 / .08), 0 25px 35px -14px rgb(43 37 32 / .32);
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .recording--flyer { --recording-angle: 0deg; }
  }
  @media (forced-colors: active) {
    .recording--flyer { --recording-angle: 0deg; }
    .recording--flyer::before { display: none; }
    .recording--flyer .video-mat { border: 1px solid CanvasText; box-shadow: none; transform: none !important; }
    .recording--flyer .recording-start { transform: none; filter: none; }
    .recording-links { border-color: CanvasText; }
  }
</style>
