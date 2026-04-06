#import "../src/lib.typ": cvSection, cvSkill
#import "../src/meta.typ": makeMeta
#let saltandstraw-metadata = makeMeta("saltandstraw-metadata.toml")

#let cvSection = cvSection.with(metadata: saltandstraw-metadata)

#cvSection("Skills & Qualifications")

#cvSkill(
  type: [Hospitality],
  info: [Front-of-house operations, Guest interaction, Event setup & breakdown, POS systems, Cash handling],
)

#cvSkill(
  type: [Food Service],
  info: [Food handler's card (can obtain within 30 days), Comfortable working around common allergens, Kitchen cleanliness & food safety awareness],
)

#cvSkill(
  type: [Communication],
  info: [English (Native), Intermediate ASL, Public speaking, Storytelling, Improv],
)

#cvSkill(
  type: [Work Style],
  info: [Flexible schedule (evenings, weekends, holidays), Comfortable on my feet for long shifts, Works well solo or on a team],
)
