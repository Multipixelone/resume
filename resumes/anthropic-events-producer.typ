#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let metadata = makeMeta("anthropic-events-producer-metadata.toml")

#show: cv.with(
  metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(metadata)
#importModules(("education",))
#skills(metadata)
