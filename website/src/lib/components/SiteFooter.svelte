<script lang="ts">
  import { page } from '$app/state';
  import { sitePath } from '#lib/paths.js';
  import { footerLinks, repoUrl } from '#lib/footer.ts';
  import Icon from './Icon.svelte';

  // commit is "<sha>", "<sha>-dirty", or "" for builds outside Nix (see +layout.server.js).
  let { commit = '', year }: { commit?: string; year: number } = $props();
  const sha = $derived(commit.split('-')[0]);
  const dirty = $derived(commit.endsWith('-dirty'));
  const href = (path: string) => (path.startsWith('/') ? sitePath(path) : path);
  const id = $props.id();
</script>

<footer class="site-footer">
  <div class="footer-directory">
    <h2 id={`${id}-title`}>Stage door.</h2>
    <nav class="footer-links" aria-labelledby={`${id}-title`}>
      {#each footerLinks as link}
        <a
          href={href(link.href)}
          rel={link.rel}
          aria-current={page.url.pathname === href(link.href) ? 'page' : undefined}
        >
          <span class="footer-link-paper" aria-hidden="true"></span>
          <Icon name={link.icon} /><span class="footer-link-label">{link.name}</span>
        </a>
      {/each}
    </nav>
  </div>

  <p class="footer-meta">
    <span>&copy; {year} Finn Rutis</span>
    <a href={sitePath('/fonts/cooper/LICENSE.md')}>Cooper* license</a>
    <span class="build-credit">
      made by Finn with SvelteKit <span class="build-heart" role="img" aria-label="love">&lt;3</span>
    </span>
    {#if sha}
      <a class="build-source" href="{repoUrl}/commit/{sha}">
        <Icon name="commit" />
        <span>built from this commit</span>
        <code>{sha.slice(0, 7)}{dirty ? '-dirty' : ''}</code>
      </a>
    {:else}
      <a class="build-source" href={repoUrl}>
        <Icon name="commit" />
        <span>view source</span>
      </a>
    {/if}
  </p>
</footer>
