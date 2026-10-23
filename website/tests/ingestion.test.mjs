import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { parse } from 'smol-toml';
import { attachPhotoNotes, parseShows, parseVariants, portfolioContent, reelRecordings, showReels } from '../lib/content.mjs';
import { performancePhotos, recordings } from '../src/lib/media.js';
import { siteBase, siteOrigin } from '../lib/config.mjs';
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

test('downloads group by field from the actual registry, theatre first; hidden entries stay out', () => {
  const registry = parse(variants);
  const { downloadGroups, theatreDownload, composite } = portfolioContent(theatre, variants);
  const entries = downloadGroups.flatMap(group => group.downloads).filter(entry => entry.id !== 'composite');
  assert.deepEqual(entries.map(entry => entry.id).sort(), Object.keys(registry).filter(id => registry[id].site_hidden !== true).sort());
  assert.equal(downloadGroups[0].field, registry.cv.field);
  assert.deepEqual(downloadGroups[0].downloads.slice(0, 2).map(entry => entry.id), ['cv', 'composite']);
  assert.equal(downloadGroups[0].downloads[1].pdf, composite);
  assert.equal(new Set(downloadGroups.map(group => group.field)).size, downloadGroups.length);
  for (const group of downloadGroups) {
    for (const entry of group.downloads.filter(item => item.id !== 'composite')) {
      assert.equal(entry.field, group.field);
      assert.equal(entry.title, registry[entry.id].title);
      assert.equal(entry.pdf, `/resumes/${registry[entry.id].dest}.pdf`);
      assert.equal(entry.preview, `/resumes/${registry[entry.id].dest}.png`);
    }
  }
  assert.equal(theatreDownload.pdf, `/resumes/${registry.cv.dest}.pdf`);
  assert.equal(composite, '/resumes/FINN RUTIS.pdf');
});

test('cover letters stay unlisted', () => {
  for (const [id, record] of Object.entries(parse(variants))) {
    if (id.includes('cover-letter')) assert.equal(record.site_hidden, true, id);
  }
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
  assert.throws(() => parseShows(fixture + 'livestream = "true"\n'), /livestream must be boolean/);
  assert.throws(() => parseShows(fixture + 'rehearsal_start = "2026-10-25"\nperformance_start = "2026-10-21"\n'), /chronological/);
  assert.throws(() => parseShows(fixture + 'description = "not a canonical field"\n'), /unknown field/);
  assert.throws(() => parseShows(fixture + 'photo = "/../private.jpg"\n'), /traverse/);
  assert.throws(() => parseShows(fixture + 'ticket_url = "javascript:alert(1)"\n'), /HTTP/);
  assert.throws(() => parseShows(fixture + 'year = "2024"\n'), /four-digit/);
  assert.throws(() => parseShows(fixture + 'year = 24\n'), /four-digit/);
  assert.equal(parseShows(fixture + 'year = 2024\n')[0].year, 2024);
});

test('registry filenames and flags cannot become paths or accidental public entries', () => {
  assert.throws(() => parseVariants('[test]\ndest = "../private"'), /Invalid/);
  assert.throws(() => parseVariants('[test]\ndest = "safe"\nsite_hidden = "true"'), /Invalid/);
  assert.throws(() => parseVariants('[one]\ndest = "same"\nsite_hidden = true\n[two]\ndest = "same"\nsite_hidden = true'), /Duplicate/);
});

test('a listed variant without a title or field fails the build; a hidden one needs neither', () => {
  assert.throws(() => parseVariants('[test]\ndest = "safe"\nfield = "Tech"'), /no title: test/);
  assert.throws(() => parseVariants('[test]\ndest = "safe"\ntitle = "Safe"'), /no field: test/);
  assert.throws(() => parseVariants('[test]\ndest = "safe"\ntitle = "Safe"\nfield = " "'), /Invalid/);
  assert.doesNotThrow(() => parseVariants('[test]\ndest = "safe"\nsite_hidden = true'));
});

test('photo hover notes read title and role from canonical shows', () => {
  const { shows } = portfolioContent(theatre, variants);
  const photos = attachPhotoNotes(performancePhotos, shows);
  performancePhotos.forEach((source, index) => {
    const show = shows.find(entry => entry.id === source.show);
    if (source.show) assert.equal(photos[index].note?.title, show?.title);
    if (source.show) assert.equal(photos[index].reel, `/shows/${source.show}/`);
    assert.equal('show' in photos[index] || 'blurb' in photos[index], false);
  });
  const [seussical] = attachPhotoNotes([{ file: 'x.jpg', show: 'seussical', blurb: ' Mine. ' }], shows);
  assert.deepEqual(seussical.note, { title: 'Seussical', role: 'Cat in the Hat', blurb: 'Mine.' });
  assert.deepEqual(attachPhotoNotes([{ file: 'x.jpg', show: '', blurb: '  ' }], shows), [{ file: 'x.jpg' }]);
  assert.throws(() => attachPhotoNotes([{ file: 'x.jpg', show: 'not-a-show' }], shows), /unknown show/);
});

test('every show with a photo gets one page, in resume order, with only its own photos and videos', () => {
  const { shows } = portfolioContent(theatre, variants);
  const reels = showReels(shows, performancePhotos, recordings);
  const withPhotos = new Set(performancePhotos.map(photo => photo.show).filter(Boolean));
  assert.deepEqual(new Set(reels.map(reel => reel.id)), withPhotos);
  const order = reels.map(reel => shows.find(show => show.id === reel.id).resume_order);
  assert.deepEqual(order, order.toSorted((a, b) => a - b));
  for (const reel of reels) {
    assert.equal(reel.path, `/shows/${reel.id}/`);
    assert.equal(reel.photos.length, performancePhotos.filter(photo => photo.show === reel.id).length);
    assert.deepEqual(reel.videos.map(video => video.id), recordings.filter(video => video.show === reel.id).map(video => video.id));
  }
  assert.deepEqual(reels.find(reel => reel.id === 'seussical').videos.map(video => video.title), ['Circus McGurkus', 'How Lucky You Are']);
  // A reel-only photo (no homepage placement) still makes a page.
  assert.equal(showReels(shows, [{ file: 'x.jpg', show: 'joseph' }], []).length, 1);
  assert.throws(() => showReels(shows, [], [{ id: 'abc', title: 'X', show: 'not-a-show' }]), /abc: unknown show/);
  assert.throws(() => showReels(shows, [{ file: 'x.jpg', show: 'not-a-show' }], []), /x.jpg: unknown show/);
});

test('reel clips caption from their canonical show, the one start clip first', () => {
  const { shows } = portfolioContent(theatre, variants);
  const reels = showReels(shows, performancePhotos, recordings);
  const clips = reelRecordings(shows, recordings, reels);
  assert.equal(recordings.filter(video => video.start).length, 1);
  assert.equal(clips[0].start, true);
  assert.deepEqual(clips.slice(1).map(clip => clip.id), recordings.filter(video => !video.start).map(video => video.id));
  for (const source of recordings) {
    const clip = clips.find(entry => entry.id === source.id);
    const show = shows.find(entry => entry.id === source.show);
    assert.equal(clip.show?.title, show?.title);
    assert.equal(clip.show?.character, show?.character);
    assert.equal(clip.show?.year, show?.year);
    assert.equal(clip.show?.path, reels.find(reel => reel.id === source.show)?.path);
  }
  // A show without photos has no page, so its label stays plain text.
  const [lone] = reelRecordings([{ id: 'joseph', title: 'Joseph', character: 'Simeon', year: 2025 }], [{ id: 'abc', title: 'Song', show: 'joseph' }], []);
  assert.deepEqual(lone, { id: 'abc', title: 'Song', start: false, show: { title: 'Joseph', character: 'Simeon', year: 2025 } });
  assert.throws(() => reelRecordings(shows, [{ id: 'abc', title: 'X', show: 'not-a-show' }], []), /abc: unknown show/);
  assert.throws(() => reelRecordings(shows, [{ id: 'a', title: 'A', start: true }, { id: 'b', title: 'B', start: true }], []), /one recording/);
});

test('base configuration accepts root and repository Pages, rejects ambiguous paths', () => {
  assert.equal(siteBase(), '');
  assert.equal(siteBase('/resume'), '/resume');
  for (const value of ['/', 'resume', '/resume/', '//host', '/..', '/resume?x=1']) {
    assert.throws(() => siteBase(value), /SITE_BASE/);
  }
});

test('origin configuration defaults to the custom domain, rejects paths and slashes', () => {
  assert.equal(siteOrigin(), 'https://finnrut.is');
  assert.equal(siteOrigin('https://multipixelone.github.io'), 'https://multipixelone.github.io');
  for (const value of ['finnrut.is', 'https://finnrut.is/', 'https://finnrut.is/resume', 'https://localhost', 'ftp://finnrut.is', 'https://finnrut.is:8443']) {
    assert.throws(() => siteOrigin(value), /SITE_ORIGIN/);
  }
});
