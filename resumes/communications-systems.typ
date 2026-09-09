#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let communications-systems-metadata = makeMeta(
  "communications-systems-metadata.toml",
)

#show: cv.with(
  communications-systems-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#set par(leading: 0.6em, spacing: 0.9em)

#experience(
  communications-systems-metadata,
  only: ("prem-ai",),
  title: "Technical & Communications Experience",
)
#experience(
  communications-systems-metadata,
  only: ("salt-and-straw", "voiceover"),
  title: "Service & Operations Experience",
)
#projects(communications-systems-metadata)
#text(size: 8pt)[
  Additional code & documentation:
  #link(
    "https://github.com/Multipixelone/blog",
  )[#underline[Personal technical blog (Zola, Python, Mastodon API)]]
]
#skills(communications-systems-metadata)
#v(6pt)
#importModules(("education",))
