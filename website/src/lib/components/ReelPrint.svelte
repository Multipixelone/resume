<script lang="ts">
  import { sitePath } from '#lib/paths.js';
  import { reelSizes, responsive } from '#lib/images.ts';
  import type { Photo } from '#lib/types.ts';
  import { paperMotion, printEntrance } from '#lib/motion.ts';

  // On a show's own page the title and role are the page heading, so the caption
  // carries only Finn's blurb and any verified credit.
  // `solo` marks a show's only print, which spans the board instead of half of it.
  let { photo, index = 0, solo = false }: { photo: Photo; index?: number; solo?: boolean } = $props();
  const blurbId = $props.id();
  let orientation = $derived(photo.height > photo.width * 1.05 ? 'portrait' : 'landscape');
  // The first print is taped to the board; the rest rest loose.
  let taped = $derived(index === 0);
</script>

<figure class="photo-print reel-print" data-orientation={orientation} data-fastening={taped ? 'tape' : undefined}
  style:--print-width={`${photo.width}px`}>
  <div class="photo-layers" use:paperMotion use:printEntrance>
    <span class="photo-arrival-shadow" aria-hidden="true"></span>
    <div class="photo-object">
      <a class="photo-mat" href={sitePath(`/media/${photo.file}`)} aria-label={`View full photo: ${photo.alt}`} data-transition-photo={photo.file}
        aria-describedby={photo.note?.blurb ? blurbId : undefined}>
        <img {...responsive(photo.file, reelSizes(orientation === 'portrait', solo, photo.width))} alt={photo.alt} width={photo.width} height={photo.height}
          loading={index === 0 ? 'eager' : 'lazy'} decoding="async" />
      </a>
      {#if taped}<span class="photo-fastener photo-tape" aria-hidden="true"></span>{/if}
    </div>
  </div>
  {#if photo.note?.blurb || photo.caption || photo.credit}
    <figcaption>
      <div class="photo-caption-copy">
        {#if photo.note?.blurb}<span class="photo-note-blurb" id={blurbId}>{photo.note.blurb}</span>{/if}
        {#if photo.caption}<span>{photo.caption}</span>{/if}
        {#if photo.credit}
          <span class="photo-credit">Photo: {#if photo.creditUrl}<a href={photo.creditUrl}>{photo.credit}</a>{:else}{photo.credit}{/if}</span>
        {/if}
      </div>
    </figcaption>
  {/if}
</figure>
