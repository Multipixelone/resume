import { content, reels } from '#lib/server/content.js';

export function load() {
  const byId = new Map(reels.map(reel => [reel.id, reel]));
  // A credit with photos carries its show page, cover print and what the page holds.
  const credits = content.theatreCredits.map(show => {
    const reel = byId.get(show.id);
    return reel
      ? { ...show, reel: { path: reel.path, cover: reel.photos[0], photos: reel.photos.length, videos: reel.videos.length } }
      : show;
  });
  return { credits, download: content.theatreDownload, composite: content.composite };
}
