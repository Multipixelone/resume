<script>
  import { recordings } from '$lib/media';
  import Arrow from '$lib/components/Arrow.svelte';
  import PageHead from '$lib/components/PageHead.svelte';
</script>

<PageHead title="Performance reel | Finn Rutis" />

<header class="page-heading"><h1>Performance reel</h1></header>
<div class="recordings">
  {#each recordings as video, index (video.id)}
    <section class="recording" aria-labelledby={`recording-${video.id}`}>
      <div class="recording-heading">
        <h2 id={`recording-${video.id}`}>{video.title}</h2>
        <a href={`https://www.youtube.com/watch?v=${video.id}`} aria-label={`Watch ${video.title} on YouTube`}>Watch on YouTube <Arrow /></a>
      </div>
      <div class="video-mat">
        <iframe
          src={`https://www.youtube-nocookie.com/embed/${video.id}?autoplay=0`}
          title={video.title}
          loading={index === 0 ? 'eager' : 'lazy'}
          allow="encrypted-media; picture-in-picture; fullscreen"
          allowfullscreen
          referrerpolicy="strict-origin-when-cross-origin"
        ></iframe>
      </div>
    </section>
  {/each}
</div>
