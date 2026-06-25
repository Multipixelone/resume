#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let ramp-metadata = makeMeta("ramp-metadata.toml")

#show: cv.with(
  ramp-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(ramp-metadata)
#importModules(("education",))
#skills(ramp-metadata)
