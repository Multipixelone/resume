<script lang="ts">
  import PhotoPrint from './PhotoPrint.svelte';
  import type { Photo } from '#lib/types.ts';

  let { photos }: { photos: Photo[] } = $props();
</script>

<div class="photo-spread">
  {#each photos as photo, index (photo.file)}
    <PhotoPrint {photo} {index} />
  {/each}
</div>
