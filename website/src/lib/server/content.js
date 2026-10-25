import filmSource from '$canonical/film.toml?raw';
import theatreSource from '$canonical/theatre.toml?raw';
import variantSource from '../../../../variants.toml?raw';
import { filmRecording, portfolioContent, reelRecordings, showReels } from '$content';
import { film, performancePhotos, recordings } from '$lib/media';

// Module-level ingestion: parse and normalize once, not per page or browser tick.
// Vite tracks canonical raw imports; no duplicated production JSON/Markdown.
export const content = portfolioContent(theatreSource, variantSource);

// Show pages, from the same photo list the homepage spread draws on.
export const reels = showReels(content.shows, performancePhotos, recordings);

// The performance reel, captioned from the same shows.
export const reel = reelRecordings(content.shows, recordings, reels);

export const reelFilm = filmRecording(filmSource, film);
