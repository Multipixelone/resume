import { attachPhotoNotes } from '$content';
import { performancePhotos } from '$lib/media';
import { content } from '$lib/server/content';

export function load() {
  return { shows: content.shows, photos: attachPhotoNotes(performancePhotos, content.shows) };
}
