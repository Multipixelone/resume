# Canonical theatre show data

`metadata/theatre.toml` is the single production source for the theatre PDF and
the future portfolio. Its `schema = "theatre-shows-v1"` marker opts the shared
`cvPerformance` renderer into theatre filtering. Educational, technical, film,
and commercial credits retain their existing rendering and source files.

## Editing a record

The `[shows.<id>]` table key is a stable ID. Keep it when changing display text.
Every record requires nonempty strings `title`, `character`, `company`, and
`director`, a boolean `on_resume`, and a positive integer `resume_order`.
Existing conventions such as `Self`, slashes in role names, and abbreviated
company names are valid. Strings are preserved, not rewritten or trimmed.

Finn controls `resume_order`: smaller numbers appear first on the PDF. Gaps are
fine; duplicate numbers are rejected across **all** records, including records
not currently selected. Swap/reassign numbers together when editing order.
The initial migration selects all 12 existing credits in their original order.
`on_resume = false` hides a credit from the PDF only. It does not prevent a show
from appearing in Current projects. Closing never removes a selected PDF credit.

Optional fields, omitted entirely when unknown:

| Field | Contract |
| --- | --- |
| `rehearsal_start` | Quoted `YYYY-MM-DD` actual Gregorian date |
| `performance_start` | Quoted `YYYY-MM-DD` actual Gregorian date |
| `closing_night` | Quoted `YYYY-MM-DD` actual Gregorian date |
| `ticket_url` | Absolute HTTP(S) URL, without credentials |
| `livestream` | Boolean; `true` prints "Livestream available" on the Current projects stub |
| `photo` | Root-relative public asset path such as `/photos/show.jpg`, no traversal |
| `photo_alt` | Nonempty alternative text supplied for a future photo consumer |

Dates must be **strings**, not TOML native date values. Empty strings, null,
impossible dates, and truncated dates such as `2026-10` are invalid. A *partial
lifecycle record* means one or more complete date fields are missing, not a
partially specified date string. Every pair of known dates must agree with
`rehearsal_start <= performance_start <= closing_night`, even if another date
is absent. Equal dates are permitted. No dates are inferred. Frontend consumers
must render text normally, not as raw HTML, and supply appropriate photo
accessibility treatment. The module validates paths/URLs, not asset existence,
image rights, link availability, or the factual truth of dates.

## Migration provenance

Joseph previously had `upcoming_until = "2026-07-09"`. That legacy marker cutoff
is **not established evidence of performance start**. It was removed, not renamed
or converted into any lifecycle date. All 12 migrated records lack established
lifecycle dates; none currently produces an upcoming marker or a Current projects
card. This is intentional. Preserve missing dates until Finn supplies facts that
can be recorded in `REFERENCE.md`. No production claims or display strings were
changed. Older `metadata/professional.toml` is not another canonical source.

## PDF helper contract

`src/utils/shows.typ` exports:

- `resumeShows(shows)`: validates boolean selection and positive integer order,
  rejects duplicate order, returns selected `(id, record)` pairs in manual order.
- `showUpcoming(record, today)`: false if `performance_start` is missing; true
  only when the supplied Typst date precedes the known start. Closing is ignored.

The canonical mode in `cvPerformance` calls these helpers using `buildDate()`.
The footnote considers only selected credits. Legacy categories retain their
existing all-record behavior and legacy marker interpretation.
`tests/show-selection.typ` is a dependency-free Typst assertion fixture.
Full lifecycle schema validation belongs at the JS ingestion boundary; Typst's
focused helpers validate selection/order and the start date used by its marker.

`buildDate()` reads the explicit `submission-date` input, not source modification
time or `version`. Both PDF packages pass that input to every compile. The
submission wrapper resolves one Eastern date for the selected packages; plain
builds use the checked-in archive date. Direct manual Typst compiles without the
input retain `datetime.today()`. See [PDF submission dates](pdf-builds.md) for the
workflow and CLI normalization boundary. The shared `parseISODate` helper validates
both explicit submission dates and known performance starts as actual Gregorian
`YYYY-MM-DD` dates in years 0001 through 9999.

## JavaScript API

`lib/shows.mjs` has no dependencies and accepts parsed TOML, not raw TOML text.
The future SvelteKit build boundary must parse the canonical file once and call
`normalizeShows(parsed)` (alias `validateShows`) before serializing data to the
browser. It throws `TypeError` for invalid tables, unknown fields, wrong types,
invalid dates, contradictory known dates, unsafe optional URLs/paths, or duplicate
manual order. It returns a frozen array of frozen plain records with `id` added.
The optional root schema, if supplied, must equal `theatre-shows-v1`.

All downstream record helpers expect this validated projection, including after
JSON serialization. They do not revalidate the entire schema on every clock tick.
They do not mutate input arrays or records:

- `validateISODate(value, label?)`: validate and return a date-only string.
- `selectResumeShows(shows)`: selected records, ascending manual order.
- `isUpcoming(show, submissionDate)`: PDF marker against an explicit ISO date.
- `SHOW_TIME_ZONE`: `America/New_York`.
- `easternCalendarDate(now)`: ISO Eastern date for a `Date` or epoch milliseconds.
  Instant strings are deliberately not accepted; construct `new Date(isoInstant)`.
- `showStatus(show, today)`: `rehearsing`, `performing`, or `null`, with an explicit
  ISO Eastern calendar date. All three dates are required for a non-null result.
- `selectCurrentShows(shows, now)`: every eligible record with `status` added.
  Before rehearsal: excluded. Rehearsal start: included. Performance start:
  performing. Closing night: included until the next Eastern midnight.
  Order is absolute **calendar-day** distance from today to performance start,
  whether past or future, then `resume_order`, then stable ID (code-point order).
  Duplicate order is rejected at ingestion; the ID tie-break is defensive.
- `nextEasternMidnight(now)`: a `Date` at the next Eastern calendar boundary.
  It searches timezone-converted dates rather than adding 24 hours, so spring
  and fall DST days correctly last 23 or 25 hours.
- `watchCurrentShows(shows, onChange, options?)`: lightweight mount-time adapter.
  Calls `onChange(currentShows, easternDate)` immediately, at the next Eastern
  midnight, and when the document becomes visible. Re-arms after updates. Returns
  an idempotent cleanup function that clears the timer and removes the listener.
  Options inject `now`, `setTimer`, `clearTimer`, and `visibilityTarget` for tests.

Phase 2 should call the watcher inside Svelte `onMount` and return its cleanup.
Keep Current projects absent until browser evaluation; hide the whole section
when the result is empty. Do not prerender stale build-time lifecycle status as
current. Ordinary essential content remains static without JS. No component or
website build integration is supplied in this part.

The visitor clock can be incorrect, and background timers can be throttled.
Visibility return recomputes from the current clock, but this is presentation,
not an authoritative event service or a confidentiality boundary. No server,
scheduled rebuild, or timezone based on the visitor's settings is needed.

## Focused verification

Run `node --test tests/show-lifecycle.test.mjs` (native Node runner, no install).
Tests inject clocks and cover actual dates, partial records, chronology, order,
independent selection, overlapping shows, Eastern boundaries, visitor timezone,
DST midnight lengths, visibility refresh, and teardown. The canonical-file test
uses a narrow fixture reader for its existing simple values, not a production
TOML parser. Integrated validation must use a real TOML parser/build input.

Compile `tests/show-selection.typ` with repository root access to evaluate the
selection/order and pure marker assertions:

```sh
typst compile --root . tests/show-selection.typ /tmp/opencode/portfolio-typst-selection.pdf
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_typst_dates.py -v
```

The date suite uses `tests/date-input.typ` and the actual Typst executable to
exercise both date-helper paths, including year-zero rejection, leap dates,
submission-date precedence, and literal whitespace versus CLI normalization.
These fixtures do not replace rendered integration checks: compile the real CV
and legacy credit consumers with explicit dates and the required package/fonts,
inspect text and page counts against `variants.toml`, and check marker boundaries
when changing the renderer. Package/date wiring and output checks remain separate
Nix gates. Follow the repository's long-run helper instructions for long tests
and builds; a focused fixture pass alone does not establish package correctness
or PDF byte reproducibility.
