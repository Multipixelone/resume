#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let logrocket-metadata = makeMeta("logrocket-metadata.toml")

#show: cv.with(
  logrocket-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(logrocket-metadata)
#importModules(("education",))
#projects(logrocket-metadata)
#pagebreak(weak: true)
#experience(logrocket-metadata)
