#import "../src/utils/date.typ": buildDate, parseISODate
#import "../src/utils/shows.typ": showUpcoming

#let mode = sys.inputs.at("mode", default: "build")
// JSON preserves literal whitespace that Typst's CLI trims from --input values.
#let input-date = if "date-json" in sys.inputs {
  json(bytes(sys.inputs.at("date-json")))
} else {
  sys.inputs.at("date", default: none)
}
#if mode == "build" {
  let chosen = buildDate()
  if "submission-date" in sys.inputs {
    assert.eq(chosen.display("[year]-[month]-[day]"), sys.inputs.at("expected"))
  } else {
    assert.eq(chosen, datetime.today())
  }
} else if mode == "upcoming" {
  let today = datetime(year: 2026, month: 10, day: 21)
  let credit = if input-date != none {
    (performance_start: input-date)
  } else {
    (:)
  }
  assert.eq(showUpcoming(credit, today), sys.inputs.at("expected") == "true")
} else if mode == "parse" {
  assert.eq(
    parseISODate(input-date).display("[year]-[month]-[day]"),
    sys.inputs.at("expected"),
  )
} else {
  panic("unknown date fixture mode")
}
