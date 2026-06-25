#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let anthropic-social-metadata = makeMeta("anthropic-social-metadata.toml")

#show: cv.with(
  anthropic-social-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(anthropic-social-metadata)
#importModules(("education",))
#projects(anthropic-social-metadata)
#experience(anthropic-social-metadata)
