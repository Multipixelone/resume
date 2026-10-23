import { content, reel } from '$lib/server/content';

export function load() {
  return { recordings: reel, download: content.theatreDownload, composite: content.composite };
}
