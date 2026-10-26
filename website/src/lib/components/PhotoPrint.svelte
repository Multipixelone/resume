<script lang="ts">
  import { sitePath } from '#lib/paths.js';
  import { responsive, spreadSizes } from '#lib/images.ts';
  import type { Photo } from '#lib/types.ts';
  import { paperMotion, printEntrance } from '#lib/motion.ts';

  let { photo, index = 0 }: { photo: Photo; index?: number } = $props();
  const noteId = $props.id();
  // Fastenings belong to the composition, not the production's source data.
  const fastenings: Record<string, 'tape' | 'pin' | 'corners'> = {
    wide: 'tape', tall: 'pin', small: 'tape', 'tall-left': 'corners', 'tall-bottom': 'tape'
  };
  let fastening = $derived(photo.placement ? fastenings[photo.placement] : undefined);
  // A print from a known show opens that show's page; anything else opens the full photo.
  let href = $derived(sitePath(photo.reel ?? `/media/${photo.file}`));
  let label = $derived(photo.reel ? `More from ${photo.note?.title}: ${photo.alt}` : `View full photo: ${photo.alt}`);
  const plural = (count: number, noun: string) => `${count} ${noun}${count === 1 ? '' : 's'}`;
</script>

<figure class={`photo-print photo-print--${photo.placement}`} data-fastening={fastening}>
  <div class="photo-layers" use:paperMotion use:printEntrance>
    <span class="photo-backing" aria-hidden="true"></span>
    <span class="photo-arrival-shadow" aria-hidden="true"></span>
    <div class="photo-object">
      <a class="photo-mat" {href} aria-label={label} data-transition-photo={photo.file}
        aria-describedby={photo.note ? noteId : undefined}>
        <img {...responsive(photo.file, spreadSizes[photo.placement ?? 'wide'])} alt={photo.alt} width={photo.width} height={photo.height} loading="lazy" decoding="async" />
      </a>
      {#if fastening === 'tape'}
        <span class="photo-fastener photo-tape" aria-hidden="true"></span>
      {:else if fastening === 'pin'}
        <img class="photo-fastener photo-pin" src={sitePath('/decorations/pushpin-rust.png')}
          alt="" aria-hidden="true" width="160" height="156" decoding="async" draggable="false" />
      {:else if fastening === 'corners'}
        <span class="photo-fastener photo-corner photo-corner--top" aria-hidden="true"></span>
        <span class="photo-fastener photo-corner photo-corner--bottom" aria-hidden="true"></span>
      {/if}
    </div>
  </div>
  {#if photo.note || photo.caption || photo.credit}
    <figcaption>
      <span class="photo-index" aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
      <div class="photo-caption-copy">
        {#if photo.note}
          <span class="photo-note" id={noteId}>
            {#if photo.note.title}
              <!-- A second pointer and touch target for the print's own link, which already names the show. -->
              <span class="photo-note-title">{#if photo.reel}<a class="photo-note-link" {href} data-transition-link={photo.file} tabindex="-1" aria-hidden="true">{photo.note.title}</a>{:else}{photo.note.title}{/if}</span>
            {/if}
            {#if photo.note.role}<span class="photo-note-role">{photo.note.role}</span>{/if}
            {#if photo.reelCount}
              <span class="photo-note-count">{plural(photo.reelCount.photos, 'photo')}{#if photo.reelCount.videos}{' · '}{plural(photo.reelCount.videos, 'video')}{/if}</span>
            {/if}
            {#if photo.note.blurb}<span class="photo-note-blurb">{photo.note.blurb}</span>{/if}
          </span>
        {/if}
        {#if photo.caption}<span>{photo.caption}</span>{/if}
        {#if photo.credit}
          <span class="photo-credit">Photo: {#if photo.creditUrl}<a href={photo.creditUrl}>{photo.credit}</a>{:else}{photo.credit}{/if}</span>
        {/if}
      </div>
    </figcaption>
  {/if}
</figure>
