<script>
  import { page } from '$app/state';
  import { sitePath } from '$lib/paths';
</script>
<svelte:head><title>{page.status} | Finn Rutis</title></svelte:head>
<div class="page-heading">
  <h1>{page.status === 404 ? 'Page not found' : 'Page unavailable'}</h1>
  <a href={sitePath('/')}>Return home</a>
</div>
