/** Canonical TOML adapter and pure calendar rules. No parsing or browser imports. */
export const SHOW_TIME_ZONE = 'America/New_York';
const dates = ['rehearsal_start', 'performance_start', 'closing_night'];
const textFields = ['title', 'character', 'company', 'director'];
const optionalText = ['ticket_url', 'photo', 'photo_alt'];
const allowed = new Set([...dates, ...textFields, ...optionalText, 'on_resume', 'resume_order']);
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value)
  && (Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null);
const fail = message => { throw new TypeError(message); };

/** Strict Gregorian date-only string; absent lifecycle fields, not partial strings, are allowed. */
export function validateISODate(value, label = 'date') {
  if (typeof value !== 'string' || !/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/.test(value)) {
    fail(`${label} must be a YYYY-MM-DD string`);
  }
  const [year, month, day] = value.split('-').map(Number);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (year < 1 || month < 1 || month > 12 || day < 1 || day > days[month - 1]) {
    fail(`${label} is not an actual calendar date`);
  }
  return value;
}

/** Validate once at the build boundary. Returns frozen, JSON-serializable records with stable IDs. */
export function normalizeShows(data) {
  if (!object(data) || !object(data.shows)) fail('expected a parsed TOML object with a shows table');
  if (data.schema !== undefined && data.schema !== 'theatre-shows-v1') fail('unknown show schema');
  for (const key of Object.keys(data)) {
    if (!['schema', 'shows'].includes(key)) fail(`unknown show table field: ${key}`);
  }
  const orders = new Set();
  return Object.freeze(Object.entries(data.shows).map(([id, source]) => {
    if (!id.trim() || !object(source)) fail(`invalid show record: ${id}`);
    for (const key of Object.keys(source)) {
      if (!allowed.has(key)) fail(`${id}: unknown field ${key}`);
    }
    for (const key of [...textFields, ...optionalText.filter(key => key in source)]) {
      if (typeof source[key] !== 'string' || !source[key].trim()) fail(`${id}.${key} must be nonempty text`);
    }
    if (typeof source.on_resume !== 'boolean') fail(`${id}.on_resume must be boolean`);
    if (!Number.isSafeInteger(source.resume_order) || source.resume_order < 1) {
      fail(`${id}.resume_order must be a positive safe integer`);
    }
    if (orders.has(source.resume_order)) fail(`${id}: duplicate resume_order ${source.resume_order}`);
    orders.add(source.resume_order);
    let previous;
    for (const key of dates) {
      if (!(key in source)) continue;
      const value = validateISODate(source[key], `${id}.${key}`);
      if (previous && previous > value) fail(`${id}: lifecycle dates are out of chronological order`);
      previous = value;
    }
    if ('ticket_url' in source) {
      let url;
      try { url = new URL(source.ticket_url); } catch { fail(`${id}: invalid ticket_url`); }
      if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) {
        fail(`${id}: ticket_url must be an absolute HTTP(S) URL without credentials`);
      }
    }
    // Photos are local public asset paths, never arbitrary executable/remote URLs.
    if ('photo' in source && !/^\/(?!\/)[A-Za-z0-9_./-]+$/.test(source.photo)) {
      fail(`${id}: photo must be a root-relative public asset path`);
    }
    if (source.photo?.split('/').some(segment => segment === '.' || segment === '..')) {
      fail(`${id}: photo cannot traverse directories`);
    }
    return Object.freeze({ id, ...source });
  }));
}

export const validateShows = normalizeShows;
const byId = (a, b) => a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
const editorial = (a, b) => a.resume_order - b.resume_order || byId(a, b);
export function selectResumeShows(shows) {
  return shows.filter(show => show.on_resume === true).sort(editorial);
}
export function isUpcoming(show, submissionDate) {
  validateISODate(submissionDate, 'submissionDate');
  return show.performance_start !== undefined && submissionDate < show.performance_start;
}

const easternFormatter = new Intl.DateTimeFormat('en-US', {
  timeZone: SHOW_TIME_ZONE, year: 'numeric', month: '2-digit', day: '2-digit', era: 'short',
});
function instantMs(now) {
  const value = now instanceof Date ? now.getTime() : now;
  if (typeof value !== 'number' || !Number.isFinite(value) || !Number.isFinite(new Date(value).getTime())) {
    fail('now must be a valid Date or epoch milliseconds');
  }
  return value;
}
export function easternCalendarDate(now) {
  const parts = Object.fromEntries(easternFormatter.formatToParts(instantMs(now)).map(p => [p.type, p.value]));
  if (parts.era !== 'AD') fail('now must be in the supported Gregorian era');
  return validateISODate(`${parts.year.padStart(4, '0')}-${parts.month}-${parts.day}`);
}

/** Null excludes incomplete, pre-rehearsal, and closed shows. Inputs are normalized records. */
export function showStatus(show, today) {
  validateISODate(today, 'today');
  if (!dates.every(key => show[key] !== undefined)) return null;
  if (today < show.rehearsal_start || today > show.closing_night) return null;
  return today < show.performance_start ? 'rehearsing' : 'performing';
}
function calendarOrdinal(value) {
  // UTC is only an ordinal for Gregorian calendar-day distance, not Eastern elapsed time.
  const date = new Date(0);
  const [year, month, day] = value.split('-').map(Number);
  date.setUTCFullYear(year, month - 1, day);
  return date.getTime() / 86400000;
}
export function selectCurrentShows(shows, now) {
  const today = easternCalendarDate(now);
  const distance = show => Math.abs(calendarOrdinal(show.performance_start) - calendarOrdinal(today));
  return shows.flatMap(show => {
    const status = showStatus(show, today);
    return status ? [{ ...show, status }] : [];
  }).sort((a, b) => distance(a) - distance(b) || editorial(a, b));
}

/** Find the actual next Eastern date boundary, including 23/25-hour DST days.
 * Binary search uses calendar conversion, not a fixed-duration midnight increment.
 */
export function nextEasternMidnight(now) {
  const start = instantMs(now);
  const today = easternCalendarDate(start);
  let low = Math.floor(start);
  let high = low + 36 * 60 * 60 * 1000; // Search bound only, never a presumed day length.
  while (high - low > 1) {
    const mid = Math.floor((low + high) / 2);
    if (easternCalendarDate(mid) === today) low = mid;
    else high = mid;
  }
  return new Date(high);
}

/** Call from Svelte onMount; returns teardown for its timer and visibility listener.
 * onChange receives (currentShows, Eastern date). Injectable environment supports tests.
 */
export function watchCurrentShows(shows, onChange, {
  now = () => new Date(),
  setTimer = (callback, delay) => globalThis.setTimeout(callback, delay),
  clearTimer = timer => globalThis.clearTimeout(timer),
  visibilityTarget = globalThis.document,
} = {}) {
  let timer;
  let stopped = false;
  function refresh() {
    if (stopped) return;
    clearTimer(timer);
    const instant = instantMs(now());
    onChange(selectCurrentShows(shows, instant), easternCalendarDate(instant));
    if (!stopped) timer = setTimer(refresh, Math.max(1, nextEasternMidnight(instant).getTime() - instant));
  }
  const visible = () => { if (visibilityTarget.visibilityState === 'visible') refresh(); };
  visibilityTarget?.addEventListener('visibilitychange', visible);
  refresh();
  return () => {
    if (stopped) return;
    stopped = true;
    clearTimer(timer);
    visibilityTarget?.removeEventListener('visibilitychange', visible);
  };
}
