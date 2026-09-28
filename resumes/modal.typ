#import "../src/lib.typ": cv, cvEntry, cvSection
#import "../src/meta.typ": makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let modal-metadata = makeMeta("modal-metadata.toml")

#show: cv.with(modal-metadata)

#set par(leading: 0.6em, spacing: 0.9em)
#set smartquote(enabled: false)

#experience(modal-metadata)
#projects(modal-metadata)
#text(size: 9pt)[
  Personal project / writing sample:
  #link(
    "https://github.com/Multipixelone/blog/blob/36ce65753f99d39a025f4ebed9893b10000b86f8/README.md",
  )[#underline[Technical blog build & API documentation]]
]
#block[
  #set par(spacing: 1.4em)
  #skills(modal-metadata)
]
#v(8pt)
#cvSection("Education", metadata: modal-metadata)
#cvEntry(
  metadata: modal-metadata,
  title: "BFA in Musical Theatre",
  society: "CAP21 / Molloy University",
  date: "2022 - 2026",
  location: "NYC | Completed 2026",
)
