#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let writer-metadata = makeMeta("writer-metadata.toml")

#show: cv.with(
  writer-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(writer-metadata)
#importModules(("education",))
#projects(writer-metadata)
#pagebreak(weak: true)
#experience(writer-metadata)
