<script lang="ts">
  import { sitePath } from '$lib/paths';
  import type { PageProps } from './$types';
  let { data }: PageProps = $props();
</script>

<svelte:head><title>Resume | Finn Rutis</title></svelte:head>

<header class="page-heading"><h1>Resume</h1></header>
<div class="resume-intro">
  <div class="download-actions">
    <a class="primary-link" href={sitePath(data.download.pdf)} rel="external" download>Download resume <span class="file-label">(PDF)</span> <span aria-hidden="true">↓</span></a>
    <a href={sitePath(data.composite)} rel="external" download>Resume with headshot <span class="file-label">(PDF)</span></a>
    <a href={sitePath('/resumes/')}>All resumes <span aria-hidden="true">↗</span></a>
  </div>
  <div class="resume-sheet">
    <!-- Phase 3 supplies the actual PNG and PDFs. Object fallback works without JS. -->
    <object class="resume-preview" data={sitePath(data.download.preview)} type="image/png" aria-label="First-page preview of Finn Rutis's theatre resume">
      <div class="preview-fallback">
        <p>Resume preview</p>
        <a href={sitePath(data.download.preview)} rel="external">Open preview image</a>
        <a href={sitePath(data.download.pdf)} rel="external">Open resume (PDF)</a>
      </div>
    </object>
  </div>
</div>

<section class="theatre-credits section-block" aria-labelledby="credits-title">
  <h2 id="credits-title">Theatre credits</h2>
  <ol class="credit-list">
    {#each data.credits as show (show.id)}
      <li>
        <div class="credit-production"><h3>{show.title}</h3><p>{show.character}</p></div>
        <div class="credit-company"><p>{show.company}</p><p class="credit-director">Director: {show.director}</p></div>
      </li>
    {/each}
  </ol>
</section>
