<script lang="ts">
  import '../styles/site.css';
  import { page } from '$app/state';
  import { sitePath } from '$lib/paths';

  let { children } = $props();
  const navigation = [
    { label: 'Resume', route: '/resume', path: '/resume/' },
    { label: 'Performance reel', route: '/performance-reel', path: '/performance-reel/' },
    { label: 'Contact', route: '/booking', path: '/booking/' }
  ];
</script>

<a class="skip-link" href="#main">Skip to content</a>
<div class="site-shell">
  <header class="site-header">
    <nav aria-label="Main navigation">
      <a class="home-link" href={sitePath('/')} aria-current={page.route.id === '/' ? 'page' : undefined}>Home</a>
      <ul>
        {#each navigation as item}
          <li><a href={sitePath(item.path)} aria-current={page.route.id === item.route ? 'page' : undefined}>{item.label}</a></li>
        {/each}
      </ul>
    </nav>
  </header>

  <main id="main" tabindex="-1">{@render children()}</main>

  <footer class="site-footer">
    <nav aria-label="More links">
      <a href={sitePath('/resumes/')} aria-current={page.route.id === '/resumes' ? 'page' : undefined}>All resumes</a>
      <a href="https://blog.finnrut.is/">Blog</a>
      <a href="mailto:me@finnrut.is">me@finnrut.is</a>
      <a href="https://www.instagram.com/finnrutis/">Instagram <span>@finnrutis</span></a>
    </nav>
    <small class="font-notice">Cooper* font: <a href={sitePath('/fonts/cooper/LICENSE.md')}>copyright and license</a></small>
  </footer>
</div>
