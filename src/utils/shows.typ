#import "date.typ": parseISODate

/// Canonical theatre selection only. Legacy credit categories do not use this.
#let resumeShows(shows) = {
  let entries = shows.pairs()
  let orders = ()
  for (_, credit) in entries {
    assert(type(credit.on_resume) == bool, message: "on_resume must be boolean")
    assert(
      type(credit.resume_order) == int and credit.resume_order > 0,
      message: "resume_order must be a positive integer",
    )
    assert(
      not orders.contains(credit.resume_order),
      message: "duplicate resume_order",
    )
    orders.push(credit.resume_order)
  }
  entries
    .filter(pair => pair.at(1).on_resume == true)
    .sorted(key: pair => pair.at(1).resume_order)
}

/// Unknown performance start means no marker; closing never affects the PDF.
#let showUpcoming(credit, today) = {
  let start = credit.at("performance_start", default: none)
  if start == none {
    false
  } else {
    today < parseISODate(start, label: "performance_start")
  }
}
