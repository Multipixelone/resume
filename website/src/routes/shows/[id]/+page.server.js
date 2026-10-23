import { error } from '@sveltejs/kit';
import { reels } from '$lib/server/content';

/** One prerendered page per show that has a photo. */
export function entries() {
  return reels.map(reel => ({ id: reel.id }));
}

export function load({ params }) {
  const index = reels.findIndex(reel => reel.id === params.id);
  if (index < 0) error(404, 'No photos for this show yet');
  const neighbor = reel => reel && { path: reel.path, title: reel.title, cover: reel.photos[0] };
  return { reel: reels[index], previous: neighbor(reels[index - 1]), next: neighbor(reels[index + 1]) };
}
