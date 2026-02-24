#import "./src/lib.typ": cv
#import "./src/work-meta.typ": work-metadata

#let importModules(modules) = {
  for module in modules {
    include {
      "modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  work-metadata,
  profilePhoto: image("./metadata/qr-code.png"),
)

#importModules((
  "work-experience",
  "training",
  "skills",
  // "technical",
  // Add more work-specific modules here
))
