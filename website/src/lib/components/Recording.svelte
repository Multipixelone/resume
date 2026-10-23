<script lang="ts">
  import { sitePath } from '$lib/paths';
  import Arrow from '$lib/components/Arrow.svelte';
  import type { Recording, ShowVideo } from '$lib/types';

  // A clip on its sheet, captioned below like a gallery print: the song in Cooper Bold,
  // then small labels for the show, role and year. `label` sits above a title that is
  // not a song (the film). The clip to start with gets a ticket tucked under its sheet.
  let { video, label = '', eager = false }: { video: ShowVideo | Recording; label?: string; eager?: boolean } = $props();
  let start = $derived('start' in video && video.start);
  let credit = $derived('show' in video ? video.show : undefined);
</script>

<section class="recording" class:recording--start={start} aria-labelledby={`recording-${video.id}`}>
  {#if start}
    <p class="recording-start"><span class="ticket-card">Start here</span></p>
  {/if}
  <div class="video-mat">
    <iframe
      src={`https://www.youtube-nocookie.com/embed/${video.id}?autoplay=0`}
      title={video.title}
      loading={eager ? 'eager' : 'lazy'}
      allow="encrypted-media; picture-in-picture; fullscreen"
      allowfullscreen
      referrerpolicy="strict-origin-when-cross-origin"
    ></iframe>
  </div>
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
</section>
