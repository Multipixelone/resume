#import "../src/utils/shows.typ": resumeShows, showUpcoming

#let credits = (
  later: (
    on_resume: true,
    resume_order: 8,
    performance_start: "2026-10-20",
    closing_night: "2026-10-25",
  ),
  hidden: (on_resume: false, resume_order: 1, performance_start: "2026-10-30"),
  historical: (on_resume: true, resume_order: 3),
)
#let selected = resumeShows(credits)
#assert.eq(selected.map(pair => pair.at(0)), ("historical", "later"))
#assert.eq(
  showUpcoming(credits.later, datetime(year: 2026, month: 10, day: 19)),
  true,
)
#assert.eq(
  showUpcoming(credits.later, datetime(year: 2026, month: 10, day: 20)),
  false,
)
#assert.eq(
  showUpcoming(credits.later, datetime(year: 2026, month: 10, day: 26)),
  false,
)
#assert.eq(
  showUpcoming(credits.historical, datetime(year: 2026, month: 10, day: 19)),
  false,
)
// Closing does not change PDF selection; only performance start controls the marker.
#assert.eq(resumeShows(credits), selected)
#let canonical = toml("../metadata/theatre.toml")
#assert.eq(canonical.schema, "theatre-shows-v1")
#assert.eq(resumeShows(canonical.shows).len(), 12)
#assert.eq(resumeShows(canonical.shows).map(pair => pair.at(0)), (
  "joseph",
  "wedding",
  "seussical",
  "kiss-me-kate",
  "legally-blonde",
  "pop",
  "in-pieces",
  "theory",
  "tuck",
  "curtains",
  "midsummer",
  "matilda",
))
