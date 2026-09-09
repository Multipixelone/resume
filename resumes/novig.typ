#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/projects.typ": projects
#import "../modules/skills.typ": skills

#let novig-metadata = makeMeta("novig-metadata.toml")

#show: cv.with(
  novig-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#set par(leading: 0.6em, spacing: 0.9em)

#experience(novig-metadata, only: ("prem-ai",), title: "Technical Experience")
#projects(novig-metadata)
#text(size: 8pt)[
  Additional code & documentation:
  #link(
    "https://github.com/Multipixelone/blog",
  )[#underline[Personal technical blog (Zola, Python, Mastodon API)]]
]
#skills(novig-metadata)
#v(6pt)
#experience(
  novig-metadata,
  only: ("voiceover", "salt-and-straw"),
  title: "Additional Experience",
)
#importModules(("education",))
