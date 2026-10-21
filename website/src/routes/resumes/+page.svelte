<script lang="ts">
  import { sitePath } from '$lib/paths';
  import type { PageProps } from './$types';
  let { data }: PageProps = $props();
</script>

<svelte:head><title>All resumes | Finn Rutis</title></svelte:head>

<header class="page-heading">
  <h1>All resumes</h1>
  <a href={sitePath('/resume/')}>Theatre resume <span aria-hidden="true">↗</span></a>
</header>
<ul class="download-library">
  {#each data.downloads as item (item.id)}
    <li>
      <h2>{item.title}</h2>
      {#if item.subtitle}<p>{item.subtitle}</p>{/if}
      <div class="library-actions">
        <a href={sitePath(item.pdf)} rel="external" download aria-label={`Download ${item.title} (PDF)`}>Download <span class="file-label">PDF</span> <span aria-hidden="true">↓</span></a>
        <a href={sitePath(item.preview)} rel="external" aria-label={`Preview ${item.title}`}>Preview</a>
      </div>
    </li>
  {/each}
</ul>
<div class="composite-download">
  <a href={sitePath(data.composite)} rel="external" download>Resume with headshot <span class="file-label">(PDF)</span> <span aria-hidden="true">↓</span></a>
</div>
