#import "../src/lib.typ": cv
#import "../src/meta.typ": makeMeta
#let work-metadata = makeMeta("work-metadata.toml")

#let importModules(modules) = {
  for module in modules {
    include {
      "../modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  work-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#importModules((
  "work-experience",
  "education",
  "skills",
  // "technical",
  // Add more work-specific modules here
))
