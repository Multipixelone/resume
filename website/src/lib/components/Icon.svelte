<script module lang="ts">
  export type IconName = 'instagram' | 'linkedin' | 'resume' | 'mail' | 'key' | 'blog' | 'rss' | 'commit' | 'download' | 'link';
</script>

<script lang="ts">
  // Inline SVG icon set, ported from the blog's templates/macros/icons.html; copy
  // new glyphs from there so both sites draw in one hand. 24x24 grid, painted with
  // currentColor; brand marks are solid and carry `icon-solid` (see site.css).
  // Decorative: every call site is a link that supplies its own aria-label.
  let { name }: { name: IconName } = $props();
</script>

{#if name === 'linkedin'}
  <svg class="icon icon-solid" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
{:else if name === 'instagram'}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3.2" y="3.2" width="17.6" height="17.6" rx="5"/><circle cx="12" cy="12" r="4.1"/><circle cx="17.2" cy="6.8" r="1.15" fill="currentColor" stroke="none"/></svg>
{:else if name === 'resume'}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M14 2.8H7a2 2 0 0 0-2 2v14.4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7.8z"/><path d="M14 2.8v5h5"/><path d="M8.6 13h6.8M8.6 16.6h4.4"/></svg>
{:else if name === 'mail'}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="2.8" y="4.8" width="18.4" height="14.4" rx="2.2"/><path d="m3.4 6.4 8.6 6.1 8.6-6.1"/></svg>
{:else if name === 'key'}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="7.6" cy="16.4" r="4.4"/><path d="M10.7 13.3 20.6 3.4"/><path d="m17.4 6.6 2.4 2.4"/><path d="m14.9 9.1 2.4 2.4"/></svg>
{:else if name === 'blog'}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15.4 4.4a2.2 2.2 0 0 1 3.1 3.1L8.2 17.8l-4.2 1.1 1.1-4.2z"/><path d="m13.6 6.2 3.1 3.1"/><path d="M12.8 20.2h7.4"/></svg>
{:else if name === 'rss'}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 4a15 15 0 0 1 15 15"/><path d="M5 11a8 8 0 0 1 8 8"/><circle cx="5.4" cy="18.6" r="1.6" fill="currentColor" stroke="none"/></svg>
{:else if name === 'commit'}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="3.6"/><path d="M2.6 12h5.8M15.6 12h5.8"/></svg>
{:else if name === 'download'}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3.4v11.4"/><path d="m7.6 10.4 4.4 4.4 4.4-4.4"/><path d="M4 17.6v1.4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-1.4"/></svg>
{:else}
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M10.4 13.6a4 4 0 0 0 5.7 0l3.1-3.1a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M13.6 10.4a4 4 0 0 0-5.7 0l-3.1 3.1a4 4 0 0 0 5.7 5.7l1-1"/></svg>
{/if}
