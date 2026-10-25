import { error } from '@sveltejs/kit';
import { building } from '$app/environment';
import { resolve } from 'node:path';
import { readFile, stat } from 'node:fs/promises';
import { renderRendition } from '$renditions';
import plan from 'virtual:media-renditions';

// Downscaled copies of static/media masters at /media/w<width>/<file>. The prerender
// crawler follows each srcset candidate here, so the build writes exactly the copies
// the pages reference and fails on any reference without a master.
export const prerender = true;
export const trailingSlash = 'never';

const cache = new Map();
let warned = false;

export async function GET({ params }) {
  const widths = plan[params.file];
  const width = Number(/^w(\d+)$/.exec(params.width)?.[1]);
  if (!widths || !widths.slice(0, -1).includes(width)) error(404, 'No such rendition');
  const master = resolve('static/media', params.file);
  const key = `${params.file}@${width}`;
  const modified = building ? 0 : (await stat(master)).mtimeMs;
  if (cache.get(key)?.modified !== modified) cache.delete(key);
  if (!cache.has(key)) {
    cache.set(key, { modified, bytes: renderRendition(master, width).catch(failure => {
      // The dev server falls back to the master so a shell without Pillow still shows every photo.
      if (building) throw failure;
      if (!warned) console.warn(`Serving photo masters in place of renditions: ${failure.message}`);
      warned = true;
      return readFile(master);
    }) });
  }
  return new Response(await cache.get(key).bytes, { headers: { 'content-type': 'image/jpeg' } });
}
