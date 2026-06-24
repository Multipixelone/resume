#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let notion-metadata = makeMeta("notion-metadata.toml")

#show: cv.with(
  notion-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(notion-metadata)
#importModules(("education",))
#projects(notion-metadata)
#pagebreak(weak: true)
#experience(notion-metadata)
