#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let hebbia-metadata = makeMeta("hebbia-metadata.toml")

#show: cv.with(
  hebbia-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(hebbia-metadata)
#importModules(("education",))
#projects(hebbia-metadata)
#pagebreak(weak: true)
#experience(hebbia-metadata)
