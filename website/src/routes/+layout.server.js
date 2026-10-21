import { siteOrigin } from '../../lib/config.mjs';

// Footer build provenance, read once at prerender. Nix passes SITE_COMMIT as
// "<sha>" or "<sha>-dirty" (packages/website.nix); dev and plain npm builds
// leave it unset and the footer links the repo instead. SITE_ORIGIN makes the
// Open Graph URLs absolute (PageHead.svelte); unset means the custom domain.
export function load() {
  return {
    commit: process.env.SITE_COMMIT ?? '',
    year: new Date().getFullYear(),
    origin: siteOrigin(process.env.SITE_ORIGIN)
  };
}
