#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let metadata = makeMeta("saltandstraw-agm-metadata.toml")

#show: cv.with(metadata)

#experience(
  metadata,
  title: "Management & Operations",
  only: (
    "house-manager",
    "developer-relations",
    "voiceover",
    "shift-coordinator",
  ),
)
#experience(
  metadata,
  title: "Event Experience",
  only: ("student-ambassador", "virtual-choir"),
)
#skills(metadata)
#importModules(("education",))
