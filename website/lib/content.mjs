import { parse } from 'smol-toml';
import { normalizeShows, selectResumeShows } from '../../lib/shows.mjs';

/** Real TOML parsing and schema validation happen only at the server/build boundary. */
export function parseShows(source) {
  return normalizeShows(parse(source));
}

export function parseVariants(source) {
  const registry = parse(source);
  const destinations = new Set();
  return Object.entries(registry).map(([id, record]) => {
    if (!record || typeof record !== 'object' || Array.isArray(record)
      || typeof record.dest !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(record.dest)
      || (record.site_hidden !== undefined && typeof record.site_hidden !== 'boolean')
      || (record.title !== undefined && (typeof record.title !== 'string' || !record.title.trim()))
      || (record.subtitle !== undefined && typeof record.subtitle !== 'string')) {
      throw new TypeError(`Invalid download entry: ${id}`);
    }
    if (destinations.has(record.dest)) throw new TypeError(`Duplicate download destination: ${record.dest}`);
    destinations.add(record.dest);
    return {
      id,
      title: record.title ?? record.dest,
      subtitle: record.subtitle ?? '',
      hidden: record.site_hidden === true,
      pdf: `/resumes/${record.dest}.pdf`,
      preview: `/resumes/${record.dest}.png`
    };
  });
}

/** Explicit JSON-only projection; lifecycle helpers consume already-validated data.
 * @returns {import('../src/lib/types').Show}
 */
function projectShow(show) {
  const { id, title, character, company, director, on_resume, resume_order,
    rehearsal_start, performance_start, closing_night, ticket_url, photo, photo_alt } = show;
  return /** @type {import('../src/lib/types').Show} */ (Object.fromEntries(Object.entries({ id, title, character, company, director,
    on_resume, resume_order, rehearsal_start, performance_start, closing_night,
    ticket_url, photo, photo_alt }).filter(([, value]) => value !== undefined)));
}

export function portfolioContent(theatreSource, variantSource) {
  const shows = parseShows(theatreSource);
  const variants = parseVariants(variantSource);
  const theatreDownload = variants.find(variant => variant.id === 'cv');
  if (!theatreDownload) throw new TypeError('The cv variant is required for the theatre resume');
  return {
    shows: shows.map(projectShow),
    theatreCredits: selectResumeShows(shows).map(projectShow),
    theatreDownload,
    downloads: variants.filter(variant => !variant.hidden),
    // Separate package, not a second variant registry. Phase 3 assembles this file.
    composite: '/resumes/FINN RUTIS.pdf'
  };
}
