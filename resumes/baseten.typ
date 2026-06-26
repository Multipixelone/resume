#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let baseten-metadata = makeMeta("baseten-metadata.toml")

#show: cv.with(
  baseten-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#projects(baseten-metadata)
#skills(baseten-metadata)
#experience(baseten-metadata)
