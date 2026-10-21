<script lang="ts">
  import { page } from '$app/state';
  import { sitePath } from '$lib/paths';
  import { footerLinks, repoUrl } from '$lib/footer';
  import Icon from './Icon.svelte';

  // commit is "<sha>", "<sha>-dirty", or "" for builds outside Nix (see +layout.server.js).
  let { commit = '', year }: { commit?: string; year: number } = $props();
  const sha = $derived(commit.split('-')[0]);
  const dirty = $derived(commit.endsWith('-dirty'));
  const href = (path: string) => (path.startsWith('/') ? sitePath(path) : path);
</script>

<footer class="site-footer">
  <nav class="footer-links" aria-label="Elsewhere">
    {#each footerLinks as link}
      <a
        href={href(link.href)}
        rel={link.rel}
        title={link.name}
        aria-label={link.name}
        aria-current={page.url.pathname === href(link.href) ? 'page' : undefined}
      ><Icon name={link.icon} /></a>
    {/each}
  </nav>

  <p class="footer-meta">
    <span>&copy; {year} Finn Rutis</span>
    <span class="sep" aria-hidden="true">&middot;</span>
    <a href={sitePath('/fonts/cooper/LICENSE.md')}>Cooper* license</a>
    <span class="sep sep-badge" aria-hidden="true">&middot;</span>
    {#if sha}
      <a class="build-badge" href="{repoUrl}/commit/{sha}">
        <Icon name="commit" />
        <span>built from</span>
        <code>{sha.slice(0, 7)}{dirty ? '-dirty' : ''}</code>
      </a>
    {:else}
      <a class="build-badge" href={repoUrl}>
        <Icon name="commit" />
        <span>built from this repo</span>
      </a>
    {/if}
  </p>
</footer>
