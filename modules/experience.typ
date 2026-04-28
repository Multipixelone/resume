#import "../src/lib.typ": cvEntry, cvSection

/// Render an Experience section from `metadata.modules.experience_file`.
/// The TOML at that path must define a [jobs] table whose entries each have
/// title, company, date, location, and (optional) summary fields.
#let experience(metadata) = {
  let jobs = toml("../metadata/" + metadata.modules.experience_file)
  cvSection("Experience", metadata: metadata)
  for (_, job) in jobs.jobs {
    cvEntry(
      metadata: metadata,
      title: job.title,
      society: job.company,
      date: job.date,
      location: job.location,
      description: job.at("summary", default: ""),
    )
    v(8pt)
  }
}
