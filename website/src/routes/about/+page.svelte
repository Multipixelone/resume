<script lang="ts">
  import { sitePath } from '$lib/paths';
  import { escapades, statement } from '$lib/about';
  import { paperMotion } from '$lib/motion';
  import Arrow from '$lib/components/Arrow.svelte';
  import PageHead from '$lib/components/PageHead.svelte';

  const paragraphs = (text: string) => text.trim().split(/\n\s*\n/);
</script>

<PageHead title="About | Finn Rutis" />

<header class="page-heading"><h1>About</h1></header>

<section class="statement" aria-labelledby="statement-title">
  <h2 id="statement-title">Artist statement</h2>
  <div class="statement-body">
    {#each paragraphs(statement) as paragraph}<p>{paragraph}</p>{/each}
  </div>
</section>

{#if escapades.length}
  <section class="offstage section-block" aria-labelledby="offstage-title">
    <div class="spread-heading">
      <div><h2 id="offstage-title">Off stage.</h2></div>
      <a class="text-link" href="https://blog.finnrut.is/">More on the blog <Arrow /></a>
    </div>
    <div class="offstage-list">
      {#each escapades as item, index}
        <article class="offstage-item" class:offstage-item--slip={!item.photo}>
          {#if item.photo}
            <div class="photo-layers" use:paperMotion>
              <a class="photo-mat" href={sitePath(`/media/${item.photo.file}`)} aria-label={`View full photo: ${item.photo.alt}`}>
                <img src={sitePath(`/media/${item.photo.file}`)} alt={item.photo.alt} width={item.photo.width} height={item.photo.height} loading="lazy" decoding="async" />
              </a>
            </div>
          {/if}
          <div class="offstage-copy">
            <span class="photo-index" aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
            <div>
              {#if item.title}<h3>{item.title}</h3>{/if}
              {#each paragraphs(item.blurb) as paragraph}<p>{paragraph}</p>{/each}
              {#if item.link}<a class="text-link" href={item.link.href}>{item.link.label} <Arrow /></a>{/if}
            </div>
          </div>
        </article>
      {/each}
    </div>
  </section>
{/if}
