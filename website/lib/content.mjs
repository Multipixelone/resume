import { parse } from 'smol-toml';
import { normalizeShows, selectResumeShows } from '../../lib/shows.mjs';

/** Real TOML parsing and schema validation happen only at the server/build boundary. */
export function parseShows(source) {
  return normalizeShows(parse(source));
}

// Saved downloads take the title the visitor clicked, not the build's file stem.
const savedAs = title => `Finn Rutis ${title}.pdf`;

export function parseVariants(source) {
  const registry = parse(source);
  const destinations = new Set();
  return Object.entries(registry).map(([id, record]) => {
    if (!record || typeof record !== 'object' || Array.isArray(record)
      || typeof record.dest !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(record.dest)
      || (record.site_hidden !== undefined && typeof record.site_hidden !== 'boolean')
      || (record.title !== undefined && (typeof record.title !== 'string' || !record.title.trim()))
      || (record.field !== undefined && (typeof record.field !== 'string' || !record.field.trim()))
      || (record.subtitle !== undefined && typeof record.subtitle !== 'string')) {
      throw new TypeError(`Invalid download entry: ${id}`);
    }
    const hidden = record.site_hidden === true;
    // A listed entry with no title would publish its file stem; fail the build instead.
    if (!hidden && record.title === undefined) throw new TypeError(`Listed variant has no title: ${id}`);
    if (!hidden && record.field === undefined) throw new TypeError(`Listed variant has no field: ${id}`);
    if (destinations.has(record.dest)) throw new TypeError(`Duplicate download destination: ${record.dest}`);
    destinations.add(record.dest);
    return {
      id,
      title: record.title ?? '',
      subtitle: record.subtitle ?? '',
      field: record.field ?? '',
      hidden,
      pdf: `/resumes/${record.dest}.pdf`,
      preview: `/resumes/${record.dest}.png`,
      filename: savedAs(record.title ?? record.dest)
    };
  });
}

/** Explicit JSON-only projection; lifecycle helpers consume already-validated data.
 * @returns {import('../src/lib/types').Show}
 */
function projectShow(show) {
  const { id, title, character, company, director, on_resume, resume_order, year,
    rehearsal_start, performance_start, closing_night, ticket_url, livestream, photo, photo_alt } = show;
  return /** @type {import('../src/lib/types').Show} */ (Object.fromEntries(Object.entries({ id, title, character, company, director,
    on_resume, resume_order, year, rehearsal_start, performance_start, closing_night,
    ticket_url, livestream, photo, photo_alt }).filter(([, value]) => value !== undefined)));
}

/** Resolve each photo's hover note against the canonical shows. Unknown ids fail the build.
 * A photo tied to a show also links to that show's page (`reel`).
 * @returns {import('../src/lib/types').Photo[]}
 */
export function attachPhotoNotes(photos, shows) {
  const byId = new Map(shows.map(show => [show.id, show]));
  return photos.map(({ show: id, blurb, ...photo }) => {
    const text = blurb?.trim();
    if (!id && !text) return photo;
    const show = id ? byId.get(id) : undefined;
    if (id && !show) throw new TypeError(`${photo.file}: unknown show ${id}`);
    // A cabaret singer billed as "Self" is the convention on paper, but says nothing in a caption.
    const role = show?.character === 'Self' ? undefined : show?.character;
    const note = Object.fromEntries(Object.entries({ title: show?.title, role, blurb: text || undefined })
      .filter(([, value]) => value !== undefined));
    return id ? { ...photo, note, reel: `/shows/${id}/` } : { ...photo, note };
  });
}

/** One page per show that has a photo, in Finn's resume order. A video joins a show
 * only by its explicit `show` id; unknown ids in either list fail the build.
 * @returns {import('../src/lib/types').ShowReel[]}
 */
export function showReels(shows, photos, recordings) {
  const known = new Set(shows.map(show => show.id));
  for (const item of [...photos, ...recordings]) {
    if (item.show && !known.has(item.show)) throw new TypeError(`${item.file ?? item.id}: unknown show ${item.show}`);
  }
  return shows.filter(show => photos.some(photo => photo.show === show.id))
    .toSorted((a, b) => a.resume_order - b.resume_order)
    .map(({ id, title, character, company, director, on_resume }) => ({
      id, title, character, company, director, on_resume,
      path: `/shows/${id}/`,
      photos: attachPhotoNotes(photos.filter(photo => photo.show === id), shows),
      videos: recordings.filter(video => video.show === id).map(video => ({ id: video.id, title: video.title, duration: video.duration, poster: video.poster }))
    }));
}

/** The reel's clips, the one marked `start` first, each captioned from its canonical show.
 * The show label links to the show's page only when the show has one.
 * @returns {import('../src/lib/types').Recording[]}
 */
export function reelRecordings(shows, recordings, reels) {
  const byId = new Map(shows.map(show => [show.id, show]));
  const pages = new Map(reels.map(reel => [reel.id, reel.path]));
  if (recordings.filter(video => video.start).length > 1) throw new TypeError('Only one recording can be the place to start');
  return recordings.toSorted((a, b) => Number(b.start === true) - Number(a.start === true))
    .map(({ show: showId, start, ...video }) => {
      const { id } = video;
      const show = showId ? byId.get(showId) : undefined;
      if (showId && !show) throw new TypeError(`${id}: unknown show ${showId}`);
      const credit = show && Object.fromEntries(Object.entries({ title: show.title, character: show.character,
        year: show.year, path: pages.get(show.id) }).filter(([, value]) => value !== undefined));
      return credit ? { ...video, start: start === true, show: credit } : { ...video, start: start === true };
    });
}

export function portfolioContent(theatreSource, variantSource) {
  const shows = parseShows(theatreSource);
  const variants = parseVariants(variantSource);
  const theatreDownload = variants.find(variant => variant.id === 'cv');
  if (!theatreDownload || theatreDownload.hidden) throw new TypeError('The cv variant is required and listed for the theatre resume');
  // Separate package, not a second variant registry. Phase 3 assembles this file.
  const composite = '/resumes/FINN RUTIS.pdf';
  const headshotTitle = 'Resume with headshot';
  const headshotDownload = { id: 'composite', title: headshotTitle, subtitle: '', field: theatreDownload.field,
    hidden: false, pdf: composite, preview: '', filename: savedAs(headshotTitle) };
  const listed = variants.filter(variant => !variant.hidden);
  // Theatre documents lead; every other field follows in registry order.
  const fields = [...new Set([theatreDownload.field, ...listed.map(variant => variant.field)])];
  return {
    shows: shows.map(projectShow),
    theatreCredits: selectResumeShows(shows).map(projectShow),
    theatreDownload,
    downloadGroups: fields.map(field => ({
      field,
      downloads: listed.filter(variant => variant.field === field)
        .flatMap(variant => (variant === theatreDownload ? [variant, headshotDownload] : [variant]))
    })),
    headshotDownload
  };
}

/** The vitals the theatre resume prints in its header, from the base metadata.
 * A field set to "" is hidden on the PDF, so it is left out here too.
 * @returns {import('../src/lib/types').ResumeVitals}
 */
export function resumeVitals(source) {
  const info = parse(source).personal?.info;
  if (!info || typeof info !== 'object') throw new TypeError('metadata.toml has no [personal.info] table');
  const field = key => {
    const value = info[key] ?? '';
    if (typeof value !== 'string') throw new TypeError(`personal.info.${key} must be a string`);
    return value.trim();
  };
  return Object.fromEntries(Object.entries({ voicePart: field('vocal-part'), height: field('height') })
    .filter(([, value]) => value));
}

/** Degrees and studio training, from the file the resume's Education and Training sections read.
 * Consecutive rows that share a discipline group under it, as the resume prints them.
 * @returns {{ degrees: import('../src/lib/types').Degree[], training: import('../src/lib/types').TrainingDiscipline[] }}
 */
export function resumeTraining(source) {
  const data = parse(source);
  const text = (value, where) => {
    if (typeof value !== 'string' || !value.trim()) throw new TypeError(`${where} must be a non-empty string`);
    return value.trim();
  };
  if (!Array.isArray(data.degrees) || !Array.isArray(data.training)) {
    throw new TypeError('education.toml needs [[degrees]] and [[training]] entries');
  }
  const degrees = data.degrees.map((degree, i) => ({
    title: text(degree.title, `degrees[${i}].title`),
    school: text(degree.school, `degrees[${i}].school`),
    location: text(degree.location, `degrees[${i}].location`),
    date: text(degree.date, `degrees[${i}].date`)
  }));
  /** @type {import('../src/lib/types').TrainingDiscipline[]} */
  const training = [];
  data.training.forEach((row, i) => {
    if (!Array.isArray(row.instructors) || !row.instructors.length) {
      throw new TypeError(`training[${i}].instructors must name at least one instructor`);
    }
    const discipline = text(row.discipline, `training[${i}].discipline`);
    const technique = { technique: text(row.technique, `training[${i}].technique`),
      instructors: row.instructors.map((name, j) => text(name, `training[${i}].instructors[${j}]`)) };
    const last = training.at(-1);
    if (last?.discipline === discipline) last.techniques.push(technique);
    else training.push({ discipline, techniques: [technique] });
  });
  return { degrees, training };
}

/** Resolve the film from the same credit used by the PDF. */
export function filmRecording(source, video) {
  const credit = parse(source).shows?.[video.credit];
  if (!credit || ['title', 'character', 'company', 'director'].some(key => typeof credit[key] !== 'string' || !credit[key].trim())) {
    throw new TypeError(`Invalid film credit: ${video.credit}`);
  }
  return { id: video.id, title: credit.title, duration: video.duration,
    film: { character: credit.character, company: credit.company, director: credit.director } };
}
