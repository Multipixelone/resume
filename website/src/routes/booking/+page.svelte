<script>
  import Arrow from '$lib/components/Arrow.svelte';
  import PageHead from '$lib/components/PageHead.svelte';
  import { sitePath } from '$lib/paths';
</script>

<PageHead title="Contact | Finn Rutis" />

<div class="contact-page">
  <header class="page-heading"><h1>Contact</h1></header>
  <div class="contact-note">
    <div class="contact-signature">
      <span>Finn Rutis</span>
      <span class="contact-pronouns">they / them</span>
    </div>
    <dl class="contact-links">
      <div class="contact-email">
        <dt>Email</dt>
        <dd><a href="mailto:me@finnrut.is"><span>me@finnrut.is</span><Arrow /></a></dd>
      </div>
      <div class="contact-instagram">
        <dt>Instagram</dt>
        <dd><a href="https://www.instagram.com/finnrutis/"><span>@finnrutis</span><Arrow /></a></dd>
      </div>
    </dl>
  </div>
  <nav class="contact-next" aria-label="More about Finn">
    <a class="text-link" href={sitePath('/performance-reel/')}>Performance reel <Arrow /></a>
    <a class="text-link" href={sitePath('/resume/')}>Resume <Arrow /></a>
  </nav>
</div>
