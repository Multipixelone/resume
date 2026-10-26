import { content } from '#lib/server/content.js';

export function load() {
  return { groups: content.downloadGroups };
}
