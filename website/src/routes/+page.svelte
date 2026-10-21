<script lang="ts">
  import { sitePath } from '$lib/paths';
  import CurrentProjects from '$lib/components/CurrentProjects.svelte';
  import PhotoSpread from '$lib/components/PhotoSpread.svelte';
  import type { PageProps } from './$types';

  let { data }: PageProps = $props();
</script>

<svelte:head>
  <title>Finn Rutis</title>
  <meta name="description" content="Finn Rutis is a New York City Based performance artist that is interested in using the magic of theatre to shine a light on unconscious parts of the human experience" />
</svelte:head>

<div class="home-hero">
  <div class="portrait-layers">
    <span class="portrait-backing" aria-hidden="true"></span>
    <div class="portrait-mat">
      <img src={sitePath('/media/portrait.jpg')} alt="Finn Rutis, smiling in a blue shirt against a warm brown background." width="2400" height="3000" fetchpriority="high" decoding="async" />
    </div>
  </div>
  <h1 class="artist-name"><span>Finn</span> <span>Rutis</span></h1>
</div>

<div class="bio-block">
  <p>Finn Rutis is a New York City Based performance artist that is interested in using the magic of theatre to shine a light on unconscious parts of the human experience</p>
</div>

<CurrentProjects shows={data.shows} />

<section class="performance-photos section-block" aria-labelledby="photos-title">
  <h2 id="photos-title">Performance photos</h2>
  <PhotoSpread photos={data.photos} />
</section>
