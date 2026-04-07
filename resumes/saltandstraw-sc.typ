#import "../src/lib.typ": cv
#import "../src/meta.typ": makeMeta
#let saltandstraw-sc-metadata = makeMeta("saltandstraw-sc-metadata.toml")

#let importModules(modules) = {
  for module in modules {
    include {
      "../modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  saltandstraw-sc-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#importModules((
  "saltandstraw-sc-experience",
  "education",
  "saltandstraw-sc-skills",
))
