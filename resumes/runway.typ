#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let runway-metadata = makeMeta("runway-metadata.toml")

#show: cv.with(
  runway-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(runway-metadata)
#importModules(("education",))
#skills(runway-metadata)
#projects(runway-metadata)
