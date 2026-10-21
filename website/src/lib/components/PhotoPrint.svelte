<script lang="ts">
  import { sitePath } from '$lib/paths';
  import type { Photo } from '$lib/types';
  import { paperMotion } from '$lib/motion';

  let { photo, index = 0 }: { photo: Photo; index?: number } = $props();
  const noteId = $props.id();
</script>

<figure class={`photo-print photo-print--${photo.placement}`}>
  <div class="photo-layers" use:paperMotion={{ delay: (index % 3) * 70 }}>
    <span class="photo-backing" aria-hidden="true"></span>
    <div data-paper-arrival>
      <a class="photo-mat" href={sitePath(`/media/${photo.file}`)} aria-label={`View full photo: ${photo.alt}`}
        aria-describedby={photo.note ? noteId : undefined}>
        <img src={sitePath(`/media/${photo.file}`)} alt={photo.alt} width={photo.width} height={photo.height} loading="lazy" decoding="async" />
      </a>
    </div>
  </div>
  {#if photo.note || photo.caption || photo.credit}
    <figcaption>
      <span class="photo-index" aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
      <div class="photo-caption-copy">
        {#if photo.note}
          <span class="photo-note" id={noteId}>
            {#if photo.note.title}<span class="photo-note-title">{photo.note.title}</span>{/if}
            {#if photo.note.role}<span class="photo-note-role">{photo.note.role}</span>{/if}
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
