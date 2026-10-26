import { content, reel, reelFilm } from '#lib/server/content.js';

export function load() {
  return { recordings: reel, film: reelFilm, download: content.theatreDownload, composite: content.composite };
}
