<script lang="ts">
  // A show's first photo as a small print, pinned beside a link to that show's page.
  // Decorative: the link text names the show, so the picture stays out of the accessible name.
  import { sitePath } from '$lib/paths';
  import type { Photo } from '$lib/types';

  let { photo }: { photo: Photo } = $props();
</script>

<span class="cover-print" aria-hidden="true">
  <img src={sitePath(`/media/${photo.file}`)} alt="" width={photo.width} height={photo.height} loading="lazy" decoding="async" />
</span>
