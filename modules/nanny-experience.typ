#import "../src/lib.typ": cvEntry, cvSection
#import "../src/meta.typ": makeMeta
#let nanny-metadata = makeMeta("nanny-metadata.toml")

#let jobs = toml("../metadata/nanny-experience.toml")
#let cvSection = cvSection.with(metadata: nanny-metadata)
#let cvEntry = cvEntry.with(metadata: nanny-metadata)

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
