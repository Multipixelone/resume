#import "../src/lib.typ": cv, cvEntry, cvSection
#import "../src/meta.typ": makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let sent-metadata = makeMeta("sent-metadata.toml")

#show: cv.with(sent-metadata)

#set par(leading: 0.6em, spacing: 0.9em)
#set smartquote(enabled: false)

#experience(
  sent-metadata,
  only: ("prem-ai",),
  title: "Technical Content Experience",
)
#experience(
  sent-metadata,
  only: ("voiceover", "oregon-childrens-theatre"),
  title: "Selected Creative Experience",
)
#block[
  #set par(spacing: 1.4em)
  #skills(sent-metadata)
]
#v(6pt)
#text(size: 9pt)[
  Personal project / writing sample:
  #link(
    "https://github.com/Multipixelone/blog/blob/36ce65753f99d39a025f4ebed9893b10000b86f8/README.md",
  )[#underline[Technical blog build & API documentation]]
]
#cvSection("Education", metadata: sent-metadata)
#cvEntry(
  metadata: sent-metadata,
  title: "BFA in Musical Theatre",
  society: "CAP21 / Molloy University",
  date: "2022 - 2026",
  location: "NYC | Completed 2026",
)
