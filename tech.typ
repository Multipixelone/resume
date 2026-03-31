#import "./src/lib.typ": cv
#import "./src/meta.typ": makeMeta
#let tech-metadata = makeMeta("tech-metadata.toml")

#let importModules(modules) = {
  for module in modules {
    include {
      "modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  tech-metadata,
  profilePhoto: image("./metadata/qr-code.png"),
)

#importModules((
  "tech-skills",
  "education",
  "tech-projects",
  "work-experience",
))
