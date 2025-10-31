#import "../src/lib.typ": cvSection, cvPerformance, cvSkill, hBar
#let metadata = toml("../metadata/metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Skills")

#cvSkill(
  type: [Technical Theatre],
  info: [Audio Production, Video Editing, Programming, Website Design],
)

#cvSkill(
  type: [Special Skills],
  info: [Ukulele, Fantastic Whistler, Improvisation, Manual Transmission Driving],
)

#cvSkill(
  type: [Languages],
  info: [English, ASL],
)

