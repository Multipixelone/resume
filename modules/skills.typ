#import "../src/lib.typ": cvSection, cvSkill

/// Render a Skills section from `metadata.modules.skills_file`.
/// The TOML at that path must define `section_title` and a [skills] table
/// whose entries each have `type` and `info` fields.
#let skills(metadata) = {
  let data = toml("../metadata/" + metadata.modules.skills_file)
  cvSection(data.section_title, metadata: metadata)
  for (_, skill) in data.skills {
    cvSkill(type: skill.type, info: skill.info)
  }
}
