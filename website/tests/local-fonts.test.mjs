import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { localFonts } from '../lib/local-fonts.mjs';

const dir = await mkdtemp(join(tmpdir(), 'local-fonts-'));
await writeFile(join(dir, 'Sabon Next Regular.woff2'), '');
const { apply, transform } = localFonts(dir);

test('dev CSS swaps only faces that have a local copy', () => {
  const css = [
    'src: url("https://fonts.finnrut.is/Sabon%20Next%20Regular.woff2") format("woff2");',
    'src: url("https://fonts.finnrut.is/Sabon%20Next%20Bold.woff2") format("woff2");',
    'src: url("https://fonts.finnrut.is/..%2Fpackage.json") format("woff2");'
  ].join('\n');
  assert.equal(transform(css, '/site/src/styles/site.css?direct'), [
    'src: url("/__fonts/Sabon%20Next%20Regular.woff2") format("woff2");',
    'src: url("https://fonts.finnrut.is/Sabon%20Next%20Bold.woff2") format("woff2");',
    'src: url("https://fonts.finnrut.is/..%2Fpackage.json") format("woff2");'
  ].join('\n'));
});

test('the swap is dev-server only and leaves non-CSS modules alone', () => {
  assert.equal(apply, 'serve');
  assert.equal(transform('"https://fonts.finnrut.is/Sabon%20Next%20Regular.woff2"', '/site/src/lib/a.js'), undefined);
});
