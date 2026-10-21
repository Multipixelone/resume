import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { parse } from 'smol-toml';
import { attachPhotoNotes, parseShows, parseVariants, portfolioContent } from '../lib/content.mjs';
import { performancePhotos } from '../src/lib/media.js';
import { siteBase } from '../lib/config.mjs';
import { selectResumeShows } from '../../lib/shows.mjs';

const theatre = await readFile(new URL('../../metadata/theatre.toml', import.meta.url), 'utf8');
const variants = await readFile(new URL('../../variants.toml', import.meta.url), 'utf8');

test('actual canonical TOML parses through smol-toml and the production normalization boundary', () => {
  const parsed = parse(theatre);
  const normalized = parseShows(theatre);
  assert.equal(parsed.schema, 'theatre-shows-v1');
  assert.equal(normalized.length, Object.keys(parsed.shows).length);
  for (const show of normalized) {
    assert.deepEqual(show, { id: show.id, ...parsed.shows[show.id] });
    assert.equal(Object.isFrozen(show), true);
  }
  const content = portfolioContent(theatre, variants);
  assert.deepEqual(content.shows, JSON.parse(JSON.stringify(normalized)));
  assert.deepEqual(content.theatreCredits, JSON.parse(JSON.stringify(selectResumeShows(normalized))));
  assert.deepEqual(content, JSON.parse(JSON.stringify(content)));
});

test('download entries come from the actual registry; hidden entries stay out', () => {
  const registry = parse(variants);
  const { downloads, theatreDownload, composite } = portfolioContent(theatre, variants);
  assert.deepEqual(downloads.map(entry => entry.id), Object.keys(registry).filter(id => registry[id].site_hidden !== true));
  for (const entry of downloads) {
    assert.equal(entry.pdf, `/resumes/${registry[entry.id].dest}.pdf`);
    assert.equal(entry.preview, `/resumes/${registry[entry.id].dest}.png`);
    assert.equal(entry.title, registry[entry.id].title ?? registry[entry.id].dest);
  }
  assert.equal(theatreDownload.pdf, `/resumes/${registry.cv.dest}.pdf`);
  assert.equal(composite, '/resumes/FINN RUTIS.pdf');
});

const fixture = `schema = "theatre-shows-v1"
[shows.fixture]
title = "Fixture production"
character = "Fixture role"
company = "Fixture company"
director = "Fixture director"
on_resume = true
resume_order = 1
`;

test('real parser preserves quoted date strings and multiline text', () => {
  const [show] = parseShows(fixture.replace('"Fixture production"', '"""Fixture\nproduction"""')
    + 'rehearsal_start = "2026-10-01"\nperformance_start = "2026-10-21"\nclosing_night = "2026-10-25"\n');
  assert.equal(show.title, 'Fixture\nproduction');
  assert.equal(show.performance_start, '2026-10-21');
});

test('TOML native dates, wrong field types, bad chronology and unknown fields fail ingestion', () => {
  assert.throws(() => parseShows(fixture + 'performance_start = 2026-10-21\n'), /YYYY-MM-DD/);
  assert.throws(() => parseShows(fixture.replace('on_resume = true', 'on_resume = "true"')), /boolean/);
  assert.throws(() => parseShows(fixture + 'rehearsal_start = "2026-10-25"\nperformance_start = "2026-10-21"\n'), /chronological/);
  assert.throws(() => parseShows(fixture + 'description = "not a canonical field"\n'), /unknown field/);
  assert.throws(() => parseShows(fixture + 'photo = "/../private.jpg"\n'), /traverse/);
  assert.throws(() => parseShows(fixture + 'ticket_url = "javascript:alert(1)"\n'), /HTTP/);
});

test('registry filenames and flags cannot become paths or accidental public entries', () => {
  assert.throws(() => parseVariants('[test]\ndest = "../private"'), /Invalid/);
  assert.throws(() => parseVariants('[test]\ndest = "safe"\nsite_hidden = "true"'), /Invalid/);
  assert.throws(() => parseVariants('[one]\ndest = "same"\n[two]\ndest = "same"'), /Duplicate/);
});

test('photo hover notes read title and role from canonical shows', () => {
  const { shows } = portfolioContent(theatre, variants);
  const photos = attachPhotoNotes(performancePhotos, shows);
  performancePhotos.forEach((source, index) => {
    const show = shows.find(entry => entry.id === source.show);
    if (source.show) assert.equal(photos[index].note?.title, show?.title);
    assert.equal('show' in photos[index] || 'blurb' in photos[index], false);
  });
  const [seussical] = attachPhotoNotes([{ file: 'x.jpg', show: 'seussical', blurb: ' Mine. ' }], shows);
  assert.deepEqual(seussical.note, { title: 'Seussical', role: 'Cat in the Hat', blurb: 'Mine.' });
  assert.deepEqual(attachPhotoNotes([{ file: 'x.jpg', show: '', blurb: '  ' }], shows), [{ file: 'x.jpg' }]);
  assert.throws(() => attachPhotoNotes([{ file: 'x.jpg', show: 'not-a-show' }], shows), /unknown show/);
});

test('base configuration accepts root and repository Pages, rejects ambiguous paths', () => {
  assert.equal(siteBase(), '');
  assert.equal(siteBase('/resume'), '/resume');
  for (const value of ['/', 'resume', '/resume/', '//host', '/..', '/resume?x=1']) {
    assert.throws(() => siteBase(value), /SITE_BASE/);
  }
});
