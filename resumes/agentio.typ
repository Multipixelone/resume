#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let agentio-metadata = makeMeta("agentio-metadata.toml")

#show: cv.with(
  agentio-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(agentio-metadata)
#importModules(("education",))
#skills(agentio-metadata)
