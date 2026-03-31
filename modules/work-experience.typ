#import "../src/lib.typ": cvEntry, cvSection
#import "../src/meta.typ": makeMeta
#let work-metadata = makeMeta("work-metadata.toml")

#let jobs = toml("../metadata/work-experience.toml")
#let cvSection = cvSection.with(metadata: work-metadata)
#let cvEntry = cvEntry.with(metadata: work-metadata)

#cvSection("Experience")

#for (_, job) in jobs.jobs {
  cvEntry(
    title: job.title,
    society: job.company,
    date: job.date,
    location: job.location,
    description: job.at("summary", default: ""),
  )
  v(8pt)
}
