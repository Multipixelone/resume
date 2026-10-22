import { existsSync, readFileSync } from 'node:fs';
import { basename, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const REMOTE = /https:\/\/fonts\.finnrut\.is\/([^"')\\\s]+)/g;
const ROUTE = '/__fonts/';

/**
 * Dev server only: swaps each fonts.finnrut.is URL in CSS for a same-origin copy from the
 * gitignored fonts-local/, so local pages (and impeccable live, which runs inside them) need no
 * CORS grant. A face with no local copy keeps its remote URL. Builds never see this plugin.
 */
export function localFonts(dir = fileURLToPath(new URL('../fonts-local/', import.meta.url))) {
  const localFile = encoded => {
    let name;
    try { name = decodeURIComponent(encoded); } catch { return null; }
    if (name !== basename(name) || !name.endsWith('.woff2')) return null;
    const file = join(dir, name);
    return existsSync(file) ? file : null;
  };
  return {
    name: 'local-fonts',
    apply: 'serve',
    configureServer(server) {
      server.middlewares.use(ROUTE, (req, res, next) => {
        const file = localFile(req.url.slice(1).split('?')[0]);
        if (!file) return next();
        res.setHeader('Content-Type', 'font/woff2');
        res.end(readFileSync(file));
      });
    },
    transform(code, id) {
      if (!id.split('?')[0].endsWith('.css') || !code.includes('fonts.finnrut.is')) return;
      return code.replace(REMOTE, (url, encoded) => (localFile(encoded) ? ROUTE + encoded : url));
    }
  };
}
