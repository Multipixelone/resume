<script lang="ts">
  import { sitePath } from '#lib/paths.js';
  import Arrow from '#lib/components/Arrow.svelte';
  import CoverPrint from '#lib/components/CoverPrint.svelte';
  import PageHead from '#lib/components/PageHead.svelte';
  import PerformanceNextSteps from '#lib/components/PerformanceNextSteps.svelte';
  import type { PageProps } from './$types.js';
  let { data }: PageProps = $props();
  let { vitals, degrees, training } = $derived(data.profile);
  const plural = (count: number, noun: string) => `${count} ${noun}${count === 1 ? '' : 's'}`;
</script>

<PageHead title="Resume | Finn Rutis" />

<header class="page-heading"><h1>Resume</h1></header>
<div class="resume-intro">
  <div class="resume-intro-grid">
    <div class="resume-facts">
      {#if vitals.voicePart || vitals.height}
        <!-- The PDF header's vitals, perforated from the downloads like a ticket's tear-off. -->
        <dl class="resume-vitals">
          {#if vitals.voicePart}<div><dt>Voice part</dt><dd>{vitals.voicePart}</dd></div>{/if}
          {#if vitals.height}<div><dt>Height</dt><dd>{vitals.height}</dd></div>{/if}
        </dl>
      {/if}
      <div class="download-actions">
        <a class="primary-link" href={sitePath(data.download.pdf)} rel="external" download="Finn Rutis Artistic Resume.pdf">Download resume <span class="link-tail"><span class="file-label">(PDF)</span> <Arrow dir="down" /></span></a>
        <a href={sitePath(data.composite)} rel="external" download="Finn Rutis Resume with headshot.pdf">Resume with headshot <span class="file-label">(PDF)</span> <Arrow dir="down" /></a>
        <a class="all-resumes-link" href={sitePath('/resumes/')}>All resumes <Arrow /></a>
      </div>
    </div>
    <div class="resume-print">
      <div class="resume-sheet">
        <span class="photo-fastener photo-tape" aria-hidden="true"></span>
        <!-- Phase 3 supplies the actual PNG and PDFs. Object fallback works without JS. -->
        <object class="resume-preview" data={sitePath(data.download.preview)} type="image/png" aria-label="First-page preview of Finn Rutis's theatre resume">
          <p class="preview-fallback">Resume preview</p>
        </object>
      </div>
      <!-- Stretched over the sheet, so the whole page opens the PDF at a size a phone can read. -->
      <a class="text-link resume-print-link" href={sitePath(data.download.pdf)} rel="external" aria-label="View PDF of the resume">View PDF <Arrow dir="out" /></a>
    </div>
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

<section class="training section-block" aria-labelledby="training-title">
  <h2 id="training-title">Training</h2>
  <!-- The credit grid again, so degree and techniques line up with the credits above. -->
  <ul class="credit-list training-list">
    {#each degrees as degree}
      <li>
        <div><h3>{degree.title}</h3><p>{degree.school}</p></div>
        <div><p>{degree.location}</p><p class="training-note">{degree.date}</p></div>
      </li>
    {/each}
    {#each training as group}
      <li>
        <h3>{group.discipline}</h3>
        <dl class="training-techniques">
          {#each group.techniques as item}
            <div><dt>{item.technique}</dt><dd class="training-note">{item.instructors.join(', ')}</dd></div>
          {/each}
        </dl>
      </li>
    {/each}
  </ul>
</section>

<PerformanceNextSteps resumePdf={data.download.pdf} />
