#import "../src/lib.typ": cvEntry, cvSection

/// Render a Projects section from `metadata.modules.projects_file`.
/// The TOML at that path must define a [projects] table.
#let projects(metadata) = {
  let projects = toml("../metadata/" + metadata.modules.projects_file)
  let heading = cvSection("Projects", metadata: metadata)
  let first = true
  for (_, project) in projects.projects {
    let entry = cvEntry(
      metadata: metadata,
      title: project.title,
      society: project.company,
      date: project.date,
      location: project.at("location", default: ""),
      description: project.at("summary", default: ""),
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
