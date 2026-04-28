#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let tech-metadata = makeMeta("tech-metadata.toml")

#show: cv.with(
  tech-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(tech-metadata)
#importModules(("education",))
#projects(tech-metadata)
#experience(tech-metadata)
