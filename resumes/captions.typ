#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let captions-metadata = makeMeta("captions-metadata.toml")

#show: cv.with(
  captions-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(captions-metadata)
#importModules(("education",))
#skills(captions-metadata)
