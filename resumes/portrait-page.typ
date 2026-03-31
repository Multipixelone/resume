#let metadata = toml("../metadata/metadata.toml")
#import "../src/utils/styles.typ": (
  awesomeColors, latinFontList, latinHeaderFont, overwriteFonts, regularColors,
  setAccentColor,
)

#let accentColor = setAccentColor(awesomeColors, metadata)
#let headerFont = overwriteFonts(
  metadata,
  latinFontList,
  latinHeaderFont,
).headerFont
#let firstName = metadata.personal.first_name
#let lastName = metadata.personal.last_name
#let pronouns = metadata.personal.pronouns

#set page(
  width: 8in,
  height: 10in,
  margin: (x: 0.5cm, y: 0.5cm),
)

#v(0fr)
#align(center, table(
  columns: (auto,),
  inset: 0pt,
  stroke: none,
  row-gutter: 1em,
  align: left,
  [#image("../src/headshot.jpg", height: 95%)],
  [#text(font: headerFont, size: 32pt, fill: regularColors.darkgray)[#firstName]
    #h(5pt)
    #text(font: headerFont, size: 32pt)[#lastName]
    #h(5pt)
    #text(size: 14pt, fill: accentColor)[#pronouns]],
))
#v(0fr)
