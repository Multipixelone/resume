import { content } from '$lib/server/content';

export function load() {
  return { credits: content.theatreCredits, download: content.theatreDownload, composite: content.composite };
}
