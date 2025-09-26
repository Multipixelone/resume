#import "./src/lib.typ": cv
#let metadata = toml("./metadata/metadata.toml")
#let importModules(modules) = {
  for module in modules {
    include {
      "modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  metadata,
  profilePhoto: image("./metadata/headshot.png")
)
#importModules((
  "professional",
  // "technical",
  "educational",
  "film",
  "commercial",
  "training",
  "skills",
))

