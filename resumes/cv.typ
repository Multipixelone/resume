#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/skills.typ": skills

#let metadata = makeMeta(none)

#show: cv.with(
  metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#importModules((
  "professional",
  "educational",
  "film",
  "training",
))
#skills(metadata)
