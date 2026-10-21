<script lang="ts">
  import { sitePath } from '$lib/paths';

  let { photo }: { photo: {
    file: string; width: number; height: number; alt: string; placement: string;
    caption?: string; credit?: string; creditUrl?: string;
  } } = $props();
</script>

<figure class={`photo-print photo-print--${photo.placement}`}>
  <div class="photo-layers">
    <span class="photo-backing" aria-hidden="true"></span>
    <a class="photo-mat" href={sitePath(`/media/${photo.file}`)} aria-label={`View full photo: ${photo.alt}`}>
      <img src={sitePath(`/media/${photo.file}`)} alt={photo.alt} width={photo.width} height={photo.height} loading="lazy" decoding="async" />
    </a>
  </div>
  {#if photo.caption || photo.credit}
    <figcaption>
      {#if photo.caption}<span>{photo.caption}</span>{/if}
      {#if photo.credit}
        <span class="photo-credit">Photo: {#if photo.creditUrl}<a href={photo.creditUrl}>{photo.credit}</a>{:else}{photo.credit}{/if}</span>
      {/if}
    </figcaption>
  {/if}
</figure>
