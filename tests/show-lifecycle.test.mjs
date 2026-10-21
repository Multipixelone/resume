import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import {
  normalizeShows, validateShows, validateISODate, selectResumeShows, isUpcoming,
  easternCalendarDate, showStatus, selectCurrentShows, nextEasternMidnight, watchCurrentShows,
} from '../lib/shows.mjs';

const record = (overrides = {}) => ({
  title: 'Fixture production', character: 'Self / Ensemble', company: 'Fixture company',
  director: 'Fixture director', on_resume: true, resume_order: 1,
  rehearsal_start: '2026-10-01', performance_start: '2026-10-20', closing_night: '2026-10-25',
  ...overrides,
});
const normalize = entries => normalizeShows({ shows: entries });
const one = () => normalize({ fixture: record() });
const ids = shows => shows.map(show => show.id);
const at = value => new Date(value);

test('strict ISO calendar validation, including leap centuries', () => {
  for (const good of ['2024-02-29', '2000-02-29', '0001-01-01', '2026-12-31']) {
    assert.equal(validateISODate(good), good);
  }
  for (const bad of ['1900-02-29', '2026-02-29', '2026-04-31', '0000-01-01', '2026-00-01',
    '2026-13-01', '2026-01-00', '2026-1-01', '2026-01', '', null, undefined, 20261001,
    new Date(), '2026-01-01T00:00:00Z']) assert.throws(() => validateISODate(bad), TypeError);
});

test('schema types, required conventions, unknown fields, and duplicate order are explicit', () => {
  assert.equal(validateShows, normalizeShows);
  assert.equal(one()[0].character, 'Self / Ensemble');
  for (const bad of [null, [], {}, { shows: [] }, { shows: {}, schema: 'bad' }, { shows: {}, extra: true }]) {
    assert.throws(() => normalizeShows(bad), TypeError);
  }
  for (const field of ['title', 'character', 'company', 'director']) {
    for (const value of ['', '  ', false, null, 1]) {
      assert.throws(() => normalize({ a: record({ [field]: value }) }), TypeError);
    }
    const missing = record(); delete missing[field];
    assert.throws(() => normalize({ a: missing }), TypeError);
  }
  for (const value of [undefined, null, 'true', 1]) {
    assert.throws(() => normalize({ a: record({ on_resume: value }) }), /boolean/);
  }
  for (const value of [undefined, '1', 0, -1, 1.5, Infinity, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => normalize({ a: record({ resume_order: value }) }), /positive safe integer/);
  }
  assert.throws(() => normalize({ a: record(), b: record({ on_resume: false }) }), /duplicate resume_order/);
  assert.throws(() => normalize({ a: record({ upcoming_until: '2026-07-09' }) }), /unknown field/);
  assert.throws(() => normalize({ a: record({ performance_start: new Date() }) }), /YYYY-MM-DD/);
  const source = record();
  const result = normalize({ a: source });
  assert.ok(Object.isFrozen(result) && Object.isFrozen(result[0]));
  assert.equal(source.id, undefined);
});

test('missing/partial lifecycle records stay valid but never become current; known pairs remain chronological', () => {
  for (let mask = 0; mask < 7; mask++) {
    const partial = record();
    ['rehearsal_start', 'performance_start', 'closing_night'].forEach((field, index) => {
      if (!(mask & (1 << index))) delete partial[field];
    });
    const shows = normalize({ partial });
    assert.deepEqual(selectCurrentShows(shows, at('2026-10-21T12:00:00Z')), []);
    assert.equal(selectResumeShows(shows).length, 1);
  }
  for (const overrides of [
    { rehearsal_start: '2026-10-21' }, { performance_start: '2026-10-26' },
    { rehearsal_start: '2026-10-26', performance_start: undefined },
  ]) {
    const bad = record(overrides);
    if (bad.performance_start === undefined) delete bad.performance_start;
    assert.throws(() => normalize({ bad }), /chronological/);
  }
  const sameDay = record({ rehearsal_start: '2026-10-25', performance_start: '2026-10-25' });
  assert.equal(showStatus(normalize({ sameDay })[0], '2026-10-25'), 'performing');
});

test('every rehearsal, performance, close boundary uses Eastern date with inclusive starts and close', () => {
  const cases = [
    ['2026-10-01T03:59:59.999Z', null], ['2026-10-01T04:00:00Z', 'rehearsing'],
    ['2026-10-20T03:59:59.999Z', 'rehearsing'], ['2026-10-20T04:00:00Z', 'performing'],
    ['2026-10-25T03:59:59.999Z', 'performing'], ['2026-10-25T04:00:00Z', 'performing'],
    ['2026-10-26T03:59:59.999Z', 'performing'], ['2026-10-26T04:00:00Z', null],
    ['2026-10-26T04:00:00.001Z', null],
  ];
  for (const [instant, expected] of cases) {
    assert.equal(selectCurrentShows(one(), at(instant))[0]?.status ?? null, expected, instant);
  }
});

test('PDF editorial selection and start marker are independent of lifecycle eligibility and close', () => {
  const shows = normalize({
    later: record({ resume_order: 8 }),
    currentNotOnPdf: record({ resume_order: 1, on_resume: false }),
    earlier: record({ resume_order: 3, closing_night: '2026-10-20' }),
  });
  assert.deepEqual(ids(selectResumeShows(shows)), ['earlier', 'later']);
  assert.deepEqual(ids(selectCurrentShows(shows, at('2026-10-21T12:00:00Z'))), ['currentNotOnPdf', 'later']);
  assert.equal(isUpcoming(shows[0], '2026-10-19'), true);
  assert.equal(isUpcoming(shows[0], '2026-10-20'), false);
  assert.equal(isUpcoming(shows[0], '2026-10-26'), false);
  assert.equal(isUpcoming({}, '2026-10-19'), false);
  assert.throws(() => isUpcoming({}, '2026-02-29'));
  assert.equal(selectResumeShows(shows).length, 2);
});

test('all overlapping productions sort by absolute calendar proximity, then editorial order and stable ID', () => {
  const shows = normalize({
    past: record({ performance_start: '2026-10-19', resume_order: 3 }),
    future: record({ performance_start: '2026-10-23', resume_order: 2 }),
    nearest: record({ performance_start: '2026-10-22', resume_order: 5 }),
    farPast: record({ performance_start: '2026-10-15', resume_order: 1 }),
  });
  assert.deepEqual(ids(selectCurrentShows(shows, at('2026-10-21T12:00:00Z'))), ['nearest', 'future', 'past', 'farPast']);
  // Defensive deterministic tie-break even for externally projected equal-order records.
  const ties = [{ ...shows[0], id: 'z' }, { ...shows[0], id: 'a' }];
  assert.deepEqual(ids(selectCurrentShows(ties, at('2026-10-21T12:00:00Z'))), ['a', 'z']);
  const dst = normalize({
    past: record({ rehearsal_start: '2026-03-01', performance_start: '2026-03-07', closing_night: '2026-03-12', resume_order: 2 }),
    future: record({ rehearsal_start: '2026-03-01', performance_start: '2026-03-09', closing_night: '2026-03-12', resume_order: 1 }),
  });
  assert.deepEqual(ids(selectCurrentShows(dst, at('2026-03-08T16:00:00Z'))), ['future', 'past']);
});

test('frontend optional fields reject unsafe URLs and paths, omit rather than fill unknown values', () => {
  const safe = normalize({ a: record({ ticket_url: 'https://example.com/tickets', photo: '/photos/show.jpg', photo_alt: 'Fixture photo' }) });
  assert.equal(safe[0].photo, '/photos/show.jpg');
  assert.equal(one()[0].ticket_url, undefined);
  for (const ticket_url of ['javascript:alert(1)', 'data:text/html,hi', '//example.com', '/tickets', '', 1, 'https://user:pass@example.com']) {
    assert.throws(() => normalize({ a: record({ ticket_url }) }));
  }
  for (const photo of ['https://example.com/photo', '//example.com/photo', '/photos/../private', 'javascript:hi', '']) {
    assert.throws(() => normalize({ a: record({ photo }) }));
  }
});

test('next midnight handles normal day, October close, spring 23 hours and fall 25 hours', () => {
  for (const [start, end, hours] of [
    ['2026-10-25T04:00:00Z', '2026-10-26T04:00:00Z', 24],
    ['2026-03-08T05:00:00Z', '2026-03-09T04:00:00Z', 23],
    ['2026-11-01T04:00:00Z', '2026-11-02T05:00:00Z', 25],
  ]) {
    assert.equal(nextEasternMidnight(at(start)).toISOString(), at(end).toISOString());
    assert.equal((nextEasternMidnight(at(start)) - at(start)) / 3600000, hours);
    assert.equal(nextEasternMidnight(at(new Date(end).getTime() - 1)).toISOString(), at(end).toISOString());
  }
  for (const instant of ['2026-03-08T06:59:59Z', '2026-03-08T07:00:00Z']) {
    assert.equal(easternCalendarDate(at(instant)), '2026-03-08');
  }
  for (const instant of ['2026-11-01T05:59:59Z', '2026-11-01T06:00:00Z']) {
    assert.equal(easternCalendarDate(at(instant)), '2026-11-01');
  }
  for (const bad of ['2026-10-25', NaN, null, new Date(NaN)]) assert.throws(() => easternCalendarDate(bad));
});

test('visitor timezone cannot change calendar, selection or next midnight', () => {
  const moduleUrl = new URL('../lib/shows.mjs', import.meta.url).href;
  const code = `import {easternCalendarDate,nextEasternMidnight,selectCurrentShows} from ${JSON.stringify(moduleUrl)};
    const now = new Date('2026-10-26T03:30:00Z');
    console.log(JSON.stringify([easternCalendarDate(now),nextEasternMidnight(now).toISOString(),
      selectCurrentShows(${JSON.stringify(one())},now).map(show => show.id)]));`;
  for (const TZ of ['UTC', 'America/Los_Angeles', 'Asia/Tokyo', 'Pacific/Auckland']) {
    const run = spawnSync(process.execPath, ['--input-type=module', '-e', code], { env: { ...process.env, TZ }, encoding: 'utf8' });
    assert.equal(run.status, 0, run.stderr);
    assert.deepEqual(JSON.parse(run.stdout), ['2026-10-25', '2026-10-26T04:00:00.000Z', ['fixture']]);
  }
});

test('scheduler refreshes on mount, midnight and visible return; cleanup removes timer/listener', () => {
  let now = at('2026-10-25T23:00:00Z');
  let callback, delay, listener;
  const cleared = [], updates = [];
  const target = {
    visibilityState: 'visible',
    addEventListener(event, fn) { assert.equal(event, 'visibilitychange'); listener = fn; },
    removeEventListener(event, fn) { assert.equal(event, 'visibilitychange'); assert.equal(fn, listener); listener = undefined; },
  };
  const stop = watchCurrentShows(one(), (shows, date) => updates.push([shows.length, date]), {
    now: () => now, visibilityTarget: target,
    setTimer(fn, ms) { callback = fn; delay = ms; return 7; },
    clearTimer(id) { cleared.push(id); },
  });
  assert.deepEqual(updates, [[1, '2026-10-25']]);
  assert.equal(delay, 5 * 3600000);
  now = at('2026-10-26T04:00:00Z'); callback();
  assert.deepEqual(updates.at(-1), [0, '2026-10-26']);
  target.visibilityState = 'hidden'; now = at('2026-10-27T12:00:00Z'); listener();
  assert.equal(updates.length, 2);
  target.visibilityState = 'visible'; listener();
  assert.deepEqual(updates.at(-1), [0, '2026-10-27']);
  const pending = callback; stop(); stop(); pending();
  assert.equal(listener, undefined);
  assert.equal(updates.length, 3);
  assert.equal(cleared.at(-1), 7);
});

test('canonical TOML migration preserves all 12 credits and supplies no invented dates', () => {
  // Narrow fixture reader for this string/boolean/integer-only file, not a production TOML parser.
  const text = readFileSync(new URL('../metadata/theatre.toml', import.meta.url), 'utf8');
  const parsed = { schema: 'theatre-shows-v1', shows: {} };
  let current;
  for (const line of text.split('\n')) {
    const section = line.match(/^\[shows\.([^\]]+)\]$/);
    if (section) current = parsed.shows[section[1]] = {};
    else if (current && line.includes(' = ')) {
      const [key, value] = line.split(' = ');
      current[key] = JSON.parse(value);
    }
  }
  const shows = normalizeShows(parsed);
  assert.deepEqual(ids(selectResumeShows(shows)), ['joseph', 'wedding', 'seussical', 'kiss-me-kate', 'legally-blonde', 'pop', 'in-pieces', 'theory', 'tuck', 'curtains', 'midsummer', 'matilda']);
  assert.deepEqual(shows.map(show => show.resume_order), Array.from({ length: 12 }, (_, i) => i + 1));
  assert.ok(shows.every(show => !show.rehearsal_start && !show.performance_start && !show.closing_night));
  assert.ok(shows.every(show => !isUpcoming(show, '2026-07-01')));
  assert.deepEqual(selectCurrentShows(shows, at('2026-10-21T12:00:00Z')), []);
});
