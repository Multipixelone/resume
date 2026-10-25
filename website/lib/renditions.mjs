import { execFile } from 'node:child_process';
import { readdirSync, readFileSync } from 'node:fs';
import { basename, join, resolve } from 'node:path';

/** Rendition widths in CSS pixels. A master only gets the ones narrower than itself. */
export const RENDITION_WIDTHS = [480, 960, 1600];
export const MODULE_ID = 'virtual:media-renditions';
const RESOLVED_ID = `\0${MODULE_ID}`;
const SCRIPT = resolve('scripts/renditions.py');

/** Pixel size from a JPEG's first frame header, without decoding the image. */
export function jpegSize(bytes) {
  if (bytes[0] !== 0xff || bytes[1] !== 0xd8) throw new TypeError('Not a JPEG');
  let offset = 2;
  while (offset + 9 < bytes.length) {
    if (bytes[offset] !== 0xff) throw new TypeError('Corrupt JPEG marker');
    const marker = bytes[offset + 1];
    // SOF0 through SOF15, minus DHT (C4), JPG (C8) and DAC (CC).
    if (marker >= 0xc0 && marker <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marker)) {
      return { height: bytes.readUInt16BE(offset + 5), width: bytes.readUInt16BE(offset + 7) };
    }
    offset += 2 + bytes.readUInt16BE(offset + 2);
  }
  throw new TypeError('JPEG has no frame header');
}

/** Every width a master is offered at, ascending; the last is the master itself. */
export function renditionWidths(width) {
  return [...RENDITION_WIDTHS.filter(candidate => candidate < width), width];
}

/** `{ file: widths }` for every JPEG master in `dir`. */
export function mediaPlan(dir) {
  return Object.fromEntries(readdirSync(dir).filter(file => file.endsWith('.jpg')).sort()
    .map(file => [file, renditionWidths(jpegSize(readFileSync(join(dir, file))).width)]));
}

/** Downscale `master` to `width` with scripts/renditions.py (Pillow) and resolve the JPEG bytes. */
export function renderRendition(master, width) {
  return new Promise((done, fail) => {
    execFile('python3', [SCRIPT, master, String(width)], { encoding: 'buffer', maxBuffer: 32 * 1024 * 1024 },
      (error, stdout, stderr) => (error ? fail(new Error(`${basename(master)} at ${width}px: ${stderr || error.message}`)) : done(stdout)));
  });
}

/**
 * Exposes the plan for static/media as `virtual:media-renditions`, so srcset lists only
 * widths that exist. Adding or replacing a master in dev reloads the page with a fresh plan.
 */
export function mediaRenditions(dir = resolve('static/media')) {
  return {
    name: 'media-renditions',
    resolveId: id => (id === MODULE_ID ? RESOLVED_ID : undefined),
    load: id => (id === RESOLVED_ID ? `export default ${JSON.stringify(mediaPlan(dir))};` : undefined),
    configureServer(server) {
      server.watcher.add(dir);
      const refresh = path => {
        if (!path.startsWith(dir) || !path.endsWith('.jpg')) return;
        for (const environment of Object.values(server.environments)) {
          const module = environment.moduleGraph.getModuleById(RESOLVED_ID);
          if (module) environment.moduleGraph.invalidateModule(module);
        }
        server.ws.send({ type: 'full-reload' });
      };
      for (const event of ['add', 'change', 'unlink']) server.watcher.on(event, refresh);
    }
  };
}
