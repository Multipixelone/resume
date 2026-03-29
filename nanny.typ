#import "./src/lib.typ": cv
#import "./src/nanny-meta.typ": nanny-metadata

#let importModules(modules) = {
  for module in modules {
    include {
      "modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  nanny-metadata,
  profilePhoto: image("./metadata/qr-code.png"),
)

#importModules((
  "nanny-experience",
  "education",
  "nanny-skills",
))
