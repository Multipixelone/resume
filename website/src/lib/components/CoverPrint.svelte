<script lang="ts">
  // A show's first photo as a small print, pinned beside a link to that show's page.
  // Decorative: the link text names the show, so the picture stays out of the accessible name.
  import { coverSizes, responsive } from '#lib/images.ts';
  import type { Photo } from '#lib/types.ts';

  let { photo }: { photo: Photo } = $props();
</script>

<span class="cover-print" aria-hidden="true">
  <img {...responsive(photo.file, coverSizes(photo.width, photo.height))} alt="" width={photo.width} height={photo.height} loading="lazy" decoding="async" />
</span>
