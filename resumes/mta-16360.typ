#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let mta-metadata = makeMeta("mta-16360-metadata.toml")

#show: cv.with(
  mta-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#skills(mta-metadata)
#projects(mta-metadata)
#experience(mta-metadata)
#importModules(("education",))
