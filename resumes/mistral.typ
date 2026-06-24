#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let mistral-metadata = makeMeta("mistral-metadata.toml")

#show: cv.with(
  mistral-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(mistral-metadata)
#importModules(("education",))
#projects(mistral-metadata)
#pagebreak(weak: true)
#experience(mistral-metadata)
