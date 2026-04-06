#import "../src/lib.typ": cvEntry, cvSection
#import "../src/meta.typ": makeMeta
#let saltandstraw-metadata = makeMeta("saltandstraw-metadata.toml")

#let jobs = toml("../metadata/saltandstraw-experience.toml")
#let cvSection = cvSection.with(metadata: saltandstraw-metadata)
#let cvEntry = cvEntry.with(metadata: saltandstraw-metadata)

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
