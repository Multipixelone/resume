#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience

#let work-metadata = makeMeta("work-metadata.toml")

#show: cv.with(
  work-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(work-metadata)
#importModules(("education", "skills"))
