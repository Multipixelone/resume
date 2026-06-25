#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let nyt-metadata = makeMeta("nyt-tech-specialist-metadata.toml")

#show: cv.with(
  nyt-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(nyt-metadata)
#importModules(("education",))
#projects(nyt-metadata)
#experience(nyt-metadata)
