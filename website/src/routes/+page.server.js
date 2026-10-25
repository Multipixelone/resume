import { attachPhotoNotes } from '$content';
import { performancePhotos } from '$lib/media';
import { content, reels } from '$lib/server/content';

export function load() {
  const counts = new Map(reels.map(reel => [reel.path, { photos: reel.photos.length, videos: reel.videos.length }]));
  // Each spread print says what its show page holds, so the videos behind it are not a secret.
  const spread = attachPhotoNotes(performancePhotos.filter(photo => photo.placement), content.shows)
    .map(photo => (photo.reel ? { ...photo, reelCount: counts.get(photo.reel) } : photo));
  const [stagePhoto] = attachPhotoNotes(performancePhotos.filter(photo => photo.hero), content.shows);
  return { shows: content.shows, photos: spread, stagePhoto };
}
