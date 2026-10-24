import { siteOrigin } from '../../lib/config.mjs';
import { content } from '$lib/server/content';

// Footer build provenance, read once at prerender. Nix passes SITE_COMMIT as
// "<sha>" or "<sha>-dirty" (packages/website.nix); dev and plain npm builds
// leave it unset and the footer links the repo instead. SITE_ORIGIN makes the
// Open Graph URLs absolute (PageHead.svelte); unset means the custom domain.
// resumePdf feeds the closing slip on the homepage and show pages, and the error
// pages (ErrorPage.svelte), which have no load of their own.
export function load() {
  return {
    commit: process.env.SITE_COMMIT ?? '',
    year: new Date().getFullYear(),
    origin: siteOrigin(process.env.SITE_ORIGIN),
    resumePdf: content.theatreDownload.pdf
  };
}
