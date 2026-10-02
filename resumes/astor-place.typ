#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let metadata = makeMeta("astor-place-metadata.toml")

#show: cv.with(metadata)

#experience(metadata, title: "Theatre & Guest Service Experience")
#importModules(("education",))
#skills(metadata)
