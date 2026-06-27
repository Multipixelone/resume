#import "../src/lib.typ": cvEntry, cvSection

/// Render an Experience section from `metadata.modules.experience_file`.
/// The TOML at that path must define a [jobs] table whose entries each have
/// title, company, date, location, and (optional) summary fields.
#let experience(metadata) = {
  let jobs = toml("../metadata/" + metadata.modules.experience_file)
  let heading = cvSection("Experience", metadata: metadata)
  let first = true
  for (_, job) in jobs.jobs {
    let entry = cvEntry(
      metadata: metadata,
      title: job.title,
      society: job.company,
      date: job.date,
      location: job.location,
      description: job.at("summary", default: ""),
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