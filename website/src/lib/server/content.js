import educationSource from '$canonical/education.toml?raw';
import filmSource from '$canonical/film.toml?raw';
import metadataSource from '$canonical/metadata.toml?raw';
import theatreSource from '$canonical/theatre.toml?raw';
import variantSource from '../../../../variants.toml?raw';
import { filmRecording, portfolioContent, reelRecordings, resumeTraining, resumeVitals, showReels } from '$content';
import { film, performancePhotos, recordings } from '#lib/media.js';

// Module-level ingestion: parse and normalize once, not per page or browser tick.
// Vite tracks canonical raw imports; no duplicated production JSON/Markdown.
export const content = portfolioContent(theatreSource, variantSource);

// Show pages, from the same photo list the homepage spread draws on.
export const reels = showReels(content.shows, performancePhotos, recordings);

// The performance reel, captioned from the same shows.
export const reel = reelRecordings(content.shows, recordings, reels);

export const reelFilm = filmRecording(filmSource, film);

// The theatre resume's header vitals and Training section, from the files the PDF reads.
export const resumeProfile = { vitals: resumeVitals(metadataSource), ...resumeTraining(educationSource) };
