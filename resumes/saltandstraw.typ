#import "../src/lib.typ": cv
#import "../src/meta.typ": makeMeta
#let saltandstraw-metadata = makeMeta("saltandstraw-metadata.toml")

#let importModules(modules) = {
  for module in modules {
    include {
      "../modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  saltandstraw-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#importModules((
  "saltandstraw-experience",
  "education",
  "saltandstraw-skills",
))
