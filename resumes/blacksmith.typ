#import "../src/lib.typ": cv, cvEntry, cvSection
#import "../src/meta.typ": makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let blacksmith-metadata = makeMeta("blacksmith-metadata.toml")

#show: cv.with(blacksmith-metadata)

#set par(leading: 0.6em, spacing: 0.9em)
#set smartquote(enabled: false)

#experience(
  blacksmith-metadata,
  only: ("prem-ai",),
  title: "Technical Experience",
)
#projects(blacksmith-metadata)
#experience(
  blacksmith-metadata,
  only: ("salt-and-straw", "virtual-choir"),
  title: "Customer Service & Technical Support",
)
#block[
  #set par(spacing: 1.4em)
  #skills(blacksmith-metadata)
]
#v(8pt)
#cvSection("Education", metadata: blacksmith-metadata)
#cvEntry(
  metadata: blacksmith-metadata,
  title: "BFA in Musical Theatre",
  society: "CAP21 / Molloy University",
  date: "2022 - 2026",
  location: "NYC | Completed 2026",
)
