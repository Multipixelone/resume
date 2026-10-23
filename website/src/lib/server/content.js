import theatreSource from '$canonical/theatre.toml?raw';
import variantSource from '../../../../variants.toml?raw';
import { portfolioContent, showReels } from '$content';
import { performancePhotos, recordings } from '$lib/media';

// Module-level ingestion: parse and normalize once, not per page or browser tick.
// Vite tracks canonical raw imports; no duplicated production JSON/Markdown.
export const content = portfolioContent(theatreSource, variantSource);

// Show pages, from the same photo list the homepage spread draws on.
export const reels = showReels(content.shows, performancePhotos, recordings);
