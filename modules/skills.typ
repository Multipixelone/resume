#import "../src/lib.typ": cvPerformance, cvSection, cvSkill, hBar
#let metadata = toml("../metadata/metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Skills")

#cvSkill(
  type: [Special Skills],
  info: [Ukulele, Fantastic Whistler, Beatboxing, Driver's License & Passport, Manual Transmission Driving, Home Studio (Scarlett 8i6, Blue Bluebird, Adobe Audition), G2-G4 vocal range, falsetto to C5],
)

#cvSkill(
  type: [Technical Theatre],
  info: [Audio Production, Video Editing, Programming, Website Design],
)

#cvSkill(
  type: [Dialects],
  info: [PNW, Australian, Generic British],
)

#cvSkill(
  type: [Languages],
  info: [English, Intermediate ASL],
)
