#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let nanny-metadata = makeMeta("nanny-metadata.toml")

#show: cv.with(
  nanny-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(nanny-metadata)
#importModules(("education",))
#skills(nanny-metadata)
