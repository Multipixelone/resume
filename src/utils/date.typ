/// Shared Gregorian ISO date contract: exactly YYYY-MM-DD, years 0001..9999.
#let parseISODate(value, label: "date") = {
  let message = label + " must be a real ISO calendar date (YYYY-MM-DD)"
  assert(type(value) == str, message: message)
  assert(
    value.match(regex("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")) != none,
    message: message,
  )
  let parts = value.split("-")
  let year = int(parts.at(0))
  assert(year >= 1, message: message)
  datetime(year: year, month: int(parts.at(1)), day: int(parts.at(2)))
}

/// Explicit submission date for PDF lifecycle and footer, never source version.
/// Missing input is only for local/manual, nonreproducible quick compiles.
#let buildDate() = {
  let submission-date = sys.inputs.at("submission-date", default: none)
  if submission-date != none {
    parseISODate(submission-date, label: "submission-date")
  } else {
    datetime.today()
  }
}
