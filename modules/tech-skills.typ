#import "../src/lib.typ": cvSection, cvSkill
#import "../src/tech-meta.typ": tech-metadata

#let skills = toml("../metadata/tech-skills.toml")
#let cvSection = cvSection.with(metadata: tech-metadata)

#cvSection("Technical Skills")

#for (_, skill) in skills.skills {
  cvSkill(
    type: skill.type,
    info: skill.info,
  )
}
