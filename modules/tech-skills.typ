#import "../src/lib.typ": cvSection, cvSkill
#import "../src/meta.typ": makeMeta
#let tech-metadata = makeMeta("tech-metadata.toml")

#let skills = toml("../metadata/tech-skills.toml")
#let cvSection = cvSection.with(metadata: tech-metadata)

#cvSection("Technical Skills")

#for (_, skill) in skills.skills {
  cvSkill(
    type: skill.type,
    info: skill.info,
  )
}
