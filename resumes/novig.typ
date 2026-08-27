#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let novig-metadata = makeMeta("novig-metadata.toml")

#show: cv.with(
  novig-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(novig-metadata)
#experience(novig-metadata)
#pagebreak(weak: true)
#projects(novig-metadata)
#importModules(("education",))
