<script lang="ts">
  import { sitePath } from '#lib/paths.js';
  import Arrow from '#lib/components/Arrow.svelte';
  import PageHead from '#lib/components/PageHead.svelte';
  import type { PageProps } from './$types.js';
  let { data }: PageProps = $props();
</script>

<PageHead title="All resumes | Finn Rutis" />

<header class="page-heading"><h1>All resumes</h1></header>
{#each data.groups as group (group.field)}
  <section class="download-group">
    <h2>{group.field}</h2>
    <ul class="download-library">
      {#each group.downloads as item (item.id)}
        <li>
          <div>
            <h3>{item.title}</h3>
            {#if item.subtitle}<p>{item.subtitle}</p>{/if}
          </div>
          <div class="library-actions">
            <a href={sitePath(item.pdf)} rel="external" download={`Finn Rutis ${item.title}.pdf`} aria-label={`Download ${item.title} (PDF)`}>Download <span class="file-label">PDF</span> <Arrow dir="down" /></a>
            {#if item.preview}<a href={sitePath(item.preview)} rel="external" aria-label={`Preview ${item.title}`}>Preview</a>{/if}
          </div>
        </li>
      {/each}
    </ul>
  </section>
{/each}
