#import "../src/lib.typ": cvSection, cvSkill
#import "../src/meta.typ": makeMeta
#let nanny-metadata = makeMeta("nanny-metadata.toml")

#let cvSection = cvSection.with(metadata: nanny-metadata)

#cvSection("Skills & Qualifications")

#cvSkill(
  type: [Creative Arts],
  info: [Ukulele, Singing, Beatboxing, Whistling, Storytelling, Make-Believe & Pretend Play, Improv],
)

#cvSkill(
  type: [Communication],
  info: [Intermediate ASL, English (Native), Comfortable talking to kids and adults alike],
)

#cvSkill(
  type: [Child Engagement],
  info: [Art projects, Theatre games, Music activities, Making up games on the spot],
)

#cvSkill(
  type: [Safety & Logistics],
  info: [American Red Cross Certified (2022), Driver's License & Valid Passport, Can drive stick, Facility & event safety experience],
)

#cvSkill(
  type: [Technical],
  info: [Home Studio Recording, Video Editing, Audio Production, General A/V setup & fixing],
)
