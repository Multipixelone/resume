#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let vox-metadata = makeMeta("vox-unexplainable-metadata.toml")

#show: cv.with(
  vox-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(vox-metadata)
#importModules(("education",))
#skills(vox-metadata)
