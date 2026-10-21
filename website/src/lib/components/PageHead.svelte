<script lang="ts">
  // Every page's <head>: title, description, and the Open Graph card link previews show.
  // Previews need absolute URLs, so the origin comes from the layout load (SITE_ORIGIN)
  // and sitePath keeps the mount. The card is drawn by scripts/gen_social_card.py.
  import { page } from '$app/state';
  import { sitePath } from '$lib/paths';

  const siteDescription = 'Finn Rutis is a New York City Based performance artist that is interested in using the magic of theatre to shine a light on unconscious parts of the human experience';
  let { title, description = siteDescription }: { title: string; description?: string } = $props();
  let origin = $derived(page.data.origin as string);
</script>

<svelte:head>
  <title>{title}</title>
  <meta name="description" content={description} />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Finn Rutis" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:url" content={origin + page.url.pathname} />
  <meta property="og:image" content={origin + sitePath('/social-card.png')} />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="2400" />
  <meta property="og:image:height" content="1260" />
  <meta property="og:image:alt" content="Finn Rutis, musical theatre performer and voiceover artist in New York City" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>
