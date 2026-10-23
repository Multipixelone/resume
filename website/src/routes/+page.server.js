import { attachPhotoNotes } from '$content';
import { performancePhotos } from '$lib/media';
import { content } from '$lib/server/content';

export function load() {
  const spread = performancePhotos.filter(photo => photo.placement);
  return { shows: content.shows, photos: attachPhotoNotes(spread, content.shows) };
}
