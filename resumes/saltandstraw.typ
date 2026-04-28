#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience

#let saltandstraw-metadata = makeMeta("saltandstraw-metadata.toml")

#show: cv.with(
  saltandstraw-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(saltandstraw-metadata)
#importModules(("education", "saltandstraw-skills"))
