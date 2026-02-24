#import "../src/lib.typ": cvSection, cvEntry
#import "../src/work-meta.typ": work-metadata

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
  )
}
