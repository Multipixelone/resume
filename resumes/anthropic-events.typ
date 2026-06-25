#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let anthropic-events-metadata = makeMeta("anthropic-events-metadata.toml")

#show: cv.with(
  anthropic-events-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(anthropic-events-metadata)
#importModules(("education",))
#skills(anthropic-events-metadata)
#projects(anthropic-events-metadata)
