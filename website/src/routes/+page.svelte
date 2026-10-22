<script lang="ts">
  import { sitePath } from '$lib/paths';
  import Arrow from '$lib/components/Arrow.svelte';
  import CurrentProjects from '$lib/components/CurrentProjects.svelte';
  import PageHead from '$lib/components/PageHead.svelte';
  import PhotoSpread from '$lib/components/PhotoSpread.svelte';
  import { paperMotion, swingFromTape } from '$lib/motion';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
  let stagePhoto = $derived(data.photos.find(photo => photo.placement === 'tall'));
</script>

<PageHead title="Finn Rutis" />

<section class="home-hero" aria-labelledby="artist-name">
  <div class="hero-heading">
    <h1 id="artist-name" class="artist-name"><span>Finn</span> <span>Rutis</span></h1>
  </div>

  <div class="portrait-scene">
    <div class="portrait-layers">
      <span class="portrait-backing" aria-hidden="true"></span>
      <div class="portrait-headshot" use:paperMotion>
        <div data-paper-arrival>
          <figure class="portrait-card">
            <img src={sitePath('/media/portrait.jpg')} alt="Finn Rutis, smiling in a blue shirt against a warm brown background." width="1536" height="1920" fetchpriority="high" decoding="async" />
            <figcaption class="portrait-caption">
              <span class="portrait-name">Finn Rutis</span>
              <span class="portrait-pronouns">they / them</span>
            </figcaption>
          </figure>
        </div>
      </div>
      {#if stagePhoto}
        <div class="portrait-overlay">
          <div class="hero-contact-print">
            <div class="photo-layers" use:paperMotion={{ delay: 140 }}>
              <div data-paper-arrival>
                <a class="photo-mat" href="#photos-title" aria-label={`Explore performance photos: ${stagePhoto.note?.title ?? 'On stage'}`} onpointerenter={swingFromTape}>
                  <img src={sitePath(`/media/${stagePhoto.file}`)} alt="" width={stagePhoto.width} height={stagePhoto.height} decoding="async" />
                  <span class="hero-print-caption">{stagePhoto.note?.title}</span>
                </a>
                <span class="hero-print-tape" aria-hidden="true"></span>
              </div>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>

  <div class="bio-block">
    <p>Finn Rutis is a New York City Based performance artist that is interested in using the magic of theatre to shine a light on unconscious parts of the human experience</p>
    <div class="hero-links">
      <a class="text-link hero-links-slip" href={sitePath('/performance-reel/')}>Watch me perform <Arrow /></a>
      <div class="hero-links-more">
        <a class="text-link" href={sitePath('/resume/')}>See my resume</a>
        <span class="hero-links-dot" aria-hidden="true">·</span>
        <a class="text-link" href={sitePath('/about/')}>More about me</a>
        <span class="hero-links-dot" aria-hidden="true">·</span>
        <a class="text-link" href={sitePath('/booking/')}>Get in touch</a>
      </div>
    </div>
  </div>
</section>

<CurrentProjects shows={data.shows} />

<section class="performance-photos section-block" aria-labelledby="photos-title">
  <div class="spread-heading">
    <div>
      <h2 id="photos-title">On stage.</h2>
    </div>
    <a class="text-link" href={sitePath('/resume/')}>Theatre credits <Arrow /></a>
  </div>
  <PhotoSpread photos={data.photos} />
</section>
