#import "../src/lib.typ": cvEntry, cvSection

/// Render a Projects section from `metadata.modules.projects_file`.
/// The TOML at that path must define a [projects] table.
#let projects(metadata) = {
  let projects = toml("../metadata/" + metadata.modules.projects_file)
  cvSection("Projects", metadata: metadata)
  for (_, project) in projects.projects {
    cvEntry(
      metadata: metadata,
      title: project.title,
      society: project.company,
      date: project.date,
      location: project.at("location", default: ""),
      description: project.at("summary", default: ""),
    )
    v(8pt)
  }
}
