#import "../src/lib.typ": cvEntry, cvSection
#import "../src/meta.typ": makeMeta
#let tech-metadata = makeMeta("tech-metadata.toml")

#let projects = toml("../metadata/tech-projects.toml")
#let cvSection = cvSection.with(metadata: tech-metadata)
#let cvEntry = cvEntry.with(metadata: tech-metadata)

#cvSection("Projects")

#for (_, project) in projects.projects {
  cvEntry(
    title: project.title,
    society: project.company,
    date: project.date,
    location: project.at("location", default: ""),
    description: project.at("summary", default: ""),
  )
  v(8pt)
}
