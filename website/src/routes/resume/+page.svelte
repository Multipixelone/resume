<script lang="ts">
  import { sitePath } from '$lib/paths';
  import Arrow from '$lib/components/Arrow.svelte';
  import CoverPrint from '$lib/components/CoverPrint.svelte';
  import PageHead from '$lib/components/PageHead.svelte';
  import PerformanceNextSteps from '$lib/components/PerformanceNextSteps.svelte';
  import type { PageProps } from './$types';
  let { data }: PageProps = $props();
  const plural = (count: number, noun: string) => `${count} ${noun}${count === 1 ? '' : 's'}`;
</script>

<PageHead title="Resume | Finn Rutis" />

<header class="page-heading"><h1>Resume</h1></header>
<div class="resume-intro">
  <div class="download-actions">
    <a class="primary-link" href={sitePath(data.download.pdf)} rel="external" download="Finn Rutis Artistic Resume.pdf">Download resume <span class="file-label">(PDF)</span> <Arrow dir="down" /></a>
    <a href={sitePath(data.composite)} rel="external" download="Finn Rutis Resume with headshot.pdf">Resume with headshot <span class="file-label">(PDF)</span></a>
    <a href={sitePath('/resumes/')}>All resumes <Arrow /></a>
  </div>
  <div class="resume-sheet">
    <span class="photo-fastener photo-tape" aria-hidden="true"></span>
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
      <li class:has-reel={show.reel}>
        <div class="credit-production">
          {#if show.reel}
            <!-- The link stretches over the row, so the whole credit and its print open the show. -->
            <h3><a class="credit-reel-link" href={sitePath(show.reel.path)} aria-describedby={`reel-${show.id}`}>{show.title}</a></h3>
          {:else}
            <h3>{show.title}</h3>
          {/if}
          <p>{show.character}</p>
        </div>
        <div class="credit-company"><p>{show.company}</p><p class="credit-director">Director: {show.director}</p></div>
        {#if show.reel}
          <div class="credit-reel">
            <CoverPrint photo={show.reel.cover} />
            <span class="credit-reel-count" id={`reel-${show.id}`}>{plural(show.reel.photos, 'photo')}{#if show.reel.videos}<br />{plural(show.reel.videos, 'video')}{/if}</span>
          </div>
        {/if}
      </li>
    {/each}
  </ol>
</section>

<PerformanceNextSteps resumePdf={data.download.pdf} />
