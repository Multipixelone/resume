#import "../src/lib.typ": cvPerformance, cvSection

/// Render shared theatre credits, optionally selecting keys in display order.
#let theatre(metadata, only: none, title: "Theatre") = {
  let data = toml("../metadata/theatre.toml")
  let shows = if only == none {
    data.shows
  } else {
    let selected = (:)
    for key in only {
      selected.insert(key, data.shows.at(key))
    }
    selected
  }
  block(breakable: false, {
    cvSection(title, metadata: metadata)
    cvPerformance((shows: shows))
  })
}
