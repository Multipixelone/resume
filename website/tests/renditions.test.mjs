import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { jpegSize, mediaPlan, renderRendition, renditionWidths } from '../lib/renditions.mjs';

test('renditions never upscale or duplicate the original width', () => {
  assert.deepEqual(renditionWidths(300), [300]);
  assert.deepEqual(renditionWidths(960), [480, 960]);
  assert.deepEqual(renditionWidths(1920), [480, 960, 1600, 1920]);
  for (const [file, widths] of Object.entries(mediaPlan('static/media'))) {
    const size = jpegSize(readFileSync(`static/media/${file}`));
    assert.equal(widths.at(-1), size.width);
    assert.equal(new Set(widths).size, widths.length);
  }
});

test('generated JPEG preserves proportions and leaves master bytes untouched', async () => {
  const master = 'static/media/joseph-ensemble.jpg';
  const before = readFileSync(master);
  const original = jpegSize(before);
  const copy = await renderRendition(master, 480);
  assert.deepEqual(jpegSize(copy), { width: 480, height: Math.round(original.height * 480 / original.width) });
  assert.ok(copy.length < before.length / 2);
  assert.deepEqual(readFileSync(master), before);
  await assert.rejects(renderRendition(master, original.width), /not narrower/);
});
