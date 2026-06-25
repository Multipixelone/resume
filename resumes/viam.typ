#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let viam-metadata = makeMeta("viam-metadata.toml")

#show: cv.with(
  viam-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(viam-metadata)
#importModules(("education",))
#pagebreak(weak: true)
#skills(viam-metadata)
#projects(viam-metadata)
