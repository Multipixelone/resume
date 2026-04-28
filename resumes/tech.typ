#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects

#let tech-metadata = makeMeta("tech-metadata.toml")

#show: cv.with(
  tech-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#importModules(("tech-skills", "education"))
#projects(tech-metadata)
#experience(tech-metadata)
