#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let tavily-metadata = makeMeta("tavily-metadata.toml")

#show: cv.with(
  tavily-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(tavily-metadata)
#skills(tavily-metadata)
#importModules(("education",))
#projects(tavily-metadata)
