#import "./src/lib.typ": cv
#import "./src/tech-meta.typ": tech-metadata

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
  "work-experience",
  "tech-projects",
  "tech-skills",
  "education",
))
