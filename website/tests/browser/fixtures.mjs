import { normalizeShows } from '../../../lib/shows.mjs';

// Deliberately fictional, test-only records. Never imported by src/ or a production route.
const record = (resume_order, dates = {}) => ({
  title: `Fixture production ${resume_order}`, character: 'Fixture role',
  company: 'Fixture company', director: 'Fixture director',
  on_resume: false, resume_order, ...dates
});
export const fixtures = {
  empty: normalizeShows({ shows: {} }),
  incomplete: normalizeShows({ shows: { incomplete: record(1, { performance_start: '2026-10-21' }) } }),
  single: normalizeShows({ shows: { performing: record(1, {
    rehearsal_start: '2026-10-01', performance_start: '2026-10-21', closing_night: '2026-10-25'
  }) } }),
  overlap: normalizeShows({ shows: {
    performing: record(1, { rehearsal_start: '2026-10-01', performance_start: '2026-10-21', closing_night: '2026-10-25' }),
    rehearsing: record(2, { rehearsal_start: '2026-10-20', performance_start: '2026-10-27', closing_night: '2026-11-02', ticket_url: 'https://example.com/tickets' }),
    later: record(3, { rehearsal_start: '2026-10-20', performance_start: '2026-10-29', closing_night: '2026-11-08' })
  } })
};
