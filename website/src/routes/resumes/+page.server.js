import { content } from '$lib/server/content';

export function load() {
  return { groups: content.downloadGroups };
}
