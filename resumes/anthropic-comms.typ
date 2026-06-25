#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let anthropic-comms-metadata = makeMeta("anthropic-comms-metadata.toml")

#show: cv.with(
  anthropic-comms-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(anthropic-comms-metadata)
#importModules(("education",))
#projects(anthropic-comms-metadata)
#experience(anthropic-comms-metadata)
