#import "../src/lib.typ": cvEntry, cvSection

/// Render an Experience section from `metadata.modules.experience_file`.
/// The TOML at that path must define a [jobs] table whose entries each have
/// title, company, date, location, and optional summary, highlights, and links.
/// `only` selects job keys in display order; omitted, all jobs are rendered.
#let experience(metadata, only: none, title: "Experience") = {
  let jobs = toml("../metadata/" + metadata.modules.experience_file)
  let selected = if only == none {
    jobs.jobs.values()
  } else {
    only.map(key => jobs.jobs.at(key))
  }
  let heading = cvSection(title, metadata: metadata)
  let first = true
  for job in selected {
    let summary = job.at("summary", default: "")
    let highlights = job.at("highlights", default: ())
    let links = job.at("links", default: ())
    let description = if highlights.len() == 0 and links.len() == 0 {
      summary
    } else {
      if summary != "" { summary }
      if highlights.len() > 0 {
        set par(leading: 5.5pt, spacing: 9.5pt)
        list(..highlights, tight: false, spacing: 9.5pt)
      }
      if links.len() > 0 {
        parbreak()
        text(
          size: 8pt,
          links
            .map(item => link(item.url, underline(item.label)))
            .join(h(10pt)),
        )
      }
    }
    let entry = cvEntry(
      metadata: metadata,
      title: job.title,
      society: job.company,
      date: job.date,
      location: job.location,
      description: description,
    )
    if first {
      block(breakable: false, heading + entry)
      first = false
    } else {
      entry
    }
    v(8pt)
  }
}
