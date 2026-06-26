#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let sofi-metadata = makeMeta("sofi-metadata.toml")

#show: cv.with(
  sofi-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(sofi-metadata)
#projects(sofi-metadata)
#skills(sofi-metadata)
#importModules(("education",))
