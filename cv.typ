#import "./src/lib.typ": cv
#let metadata = toml("metadata.toml")
#let importModules(modules) = {
  for module in modules {
    include {
      "modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  metadata,
  profilePhoto: image("./headshot.png")
)
#importModules((
  "film",
  "commercial",
  "professional",
  "educational",
  "technical",
))

