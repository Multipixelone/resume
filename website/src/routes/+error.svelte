<script>
  import { page } from '$app/state';
  import { sitePath } from '$lib/paths';
  import PageHead from '$lib/components/PageHead.svelte';
</script>
<PageHead title={`${page.status} | Finn Rutis`} />
<div class="page-heading">
  <h1>{page.status === 404 ? 'Page not found' : 'Page unavailable'}</h1>
  <a href={sitePath('/')}>Return home</a>
</div>
