#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience

#let saltandstraw-sc-metadata = makeMeta("saltandstraw-sc-metadata.toml")

#show: cv.with(
  saltandstraw-sc-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(saltandstraw-sc-metadata)
#importModules(("education", "saltandstraw-sc-skills"))
