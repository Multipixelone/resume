#import "../src/lib.typ": cv, cvEntry, cvSection
#import "../src/meta.typ": makeMeta
#import "../modules/theatre.typ": theatre
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let fao-schwarz-metadata = makeMeta("fao-schwarz-metadata.toml")

#show: cv.with(fao-schwarz-metadata)

#set par(leading: 0.6em, spacing: 0.9em)

#theatre(
  fao-schwarz-metadata,
  only: ("seussical", "midsummer", "matilda", "tuck"),
  title: "Selected Theatre",
)
#experience(fao-schwarz-metadata, title: "Guest Service & Youth Experience")
#cvSection("Education", metadata: fao-schwarz-metadata)
#cvEntry(
  metadata: fao-schwarz-metadata,
  title: "Bachelor of Fine Arts in Musical Theatre",
  society: "CAP21 / Molloy University",
  date: "2022 - 2026",
  location: "NYC",
)
#v(6pt)
#skills(fao-schwarz-metadata)
