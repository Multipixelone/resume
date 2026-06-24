#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let sierra-metadata = makeMeta("sierra-metadata.toml")

#show: cv.with(
  sierra-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(sierra-metadata)
#importModules(("education",))
#projects(sierra-metadata)
#pagebreak(weak: true)
#experience(sierra-metadata)
