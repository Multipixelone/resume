#import "../src/lib.typ": cvSection, cvSkill
#import "../src/meta.typ": makeMeta
#let saltandstraw-sc-metadata = makeMeta("saltandstraw-sc-metadata.toml")

#let cvSection = cvSection.with(metadata: saltandstraw-sc-metadata)

#cvSection("Skills & Qualifications")

#cvSkill(
  type: [Leadership],
  info: [Team coaching, Shift coordination, Task delegation, Training new staff, Setting the tone on the floor],
)

#cvSkill(
  type: [Hospitality],
  info: [Front-of-house operations, Guest interaction, Opening & closing procedures, POS systems, Cash handling],
)

#cvSkill(
  type: [Food Service],
  info: [Food handler's card (can obtain within 30 days), Comfortable working around common allergens, Kitchen cleanliness & food safety awareness],
)

#cvSkill(
  type: [Communication],
  info: [English (Native), Intermediate ASL, Public speaking, Conflict resolution, Real-time coaching],
)

#cvSkill(
  type: [Work Style],
  info: [Flexible schedule (evenings, weekends, holidays), Comfortable on my feet for long shifts, Works well solo or on a team],
)
