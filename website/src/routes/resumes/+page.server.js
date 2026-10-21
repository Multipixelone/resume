import { content } from '$lib/server/content';

export function load() {
  return { downloads: content.downloads, composite: content.composite };
}
