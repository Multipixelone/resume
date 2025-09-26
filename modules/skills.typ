#import "../src/lib.typ": cvSection, cvPerformance, cvSkill, hBar
#let metadata = toml("../metadata/metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Skills")

#cvSkill(
  type: [Languages],
  info: [English #hBar() ASL],
)

#cvSkill(
  type: [Technical Theatre],
  info: [Audio Production #hBar() Video Editing #hBar() Programming #hBar() Website Design],
)

#cvSkill(
  type: [Special Skills],
  info: [Ukulele, fantastic whistler, can drive manual transmission],
)
