#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let elevenlabs-metadata = makeMeta("elevenlabs-metadata.toml")

#show: cv.with(
  elevenlabs-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(elevenlabs-metadata)
#importModules(("education",))
#projects(elevenlabs-metadata)
#experience(elevenlabs-metadata)
