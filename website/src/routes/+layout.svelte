<script lang="ts">
  import '../styles/site.css';
  import { page } from '$app/state';
  import { sitePath } from '$lib/paths';
  import { showAbout } from '$lib/about';
  import SiteFooter from '$lib/components/SiteFooter.svelte';

  let { children, data } = $props();
  const navigation = [
    { label: 'About', route: '/about', path: '/about/' },
    { label: 'Resume', route: '/resume', path: '/resume/' },
    { label: 'Reel', route: '/performance-reel', path: '/performance-reel/' },
    { label: 'Contact', route: '/booking', path: '/booking/' }
  ].filter(item => item.route !== '/about' || showAbout);
</script>

<a class="skip-link" href="#main">Skip to content</a>
<div class="site-shell">
  <header class="site-header">
    <nav aria-label="Main navigation">
      <a class="brand" href={sitePath('/')} aria-current={page.route.id === '/' ? 'page' : undefined}>
        <span class="brand-ticket" aria-hidden="true">
          <span class="ticket-card"><span class="ticket-seat">Orch &middot; Row F</span><span class="ticket-mark">Rutis</span></span>
        </span>
        <span class="brand-name">Finn Rutis</span>
      </a>
      <ul>
        {#each navigation as item}
          <li><a href={sitePath(item.path)} aria-current={page.route.id === item.route ? 'page' : undefined}>{item.label}</a></li>
        {/each}
      </ul>
    </nav>
  </header>

  <main id="main" tabindex="-1">{@render children()}</main>

  <SiteFooter commit={data.commit} year={data.year} />
</div>
