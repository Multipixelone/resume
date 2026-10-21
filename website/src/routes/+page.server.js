import { content } from '$lib/server/content';

export function load() {
  return { shows: content.shows };
}
