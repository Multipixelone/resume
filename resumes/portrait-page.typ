#let metadata = toml("../metadata/metadata.toml")
#import "../src/utils/styles.typ": (
  awesomeColors, fs, latinFontList, latinHeaderFont, overwriteFonts,
  regularColors, setAccentColor,
)

#let accentColor = setAccentColor(awesomeColors, metadata)
#let fonts = overwriteFonts(metadata, latinFontList, latinHeaderFont)
#let headerFont = fonts.headerFont
#let firstName = metadata.personal.first_name
#let lastName = metadata.personal.last_name
#let pronouns = metadata.personal.pronouns

#set text(font: fonts.regularFonts)

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
  align: right,
  [#image("../src/headshot.jpg", height: 95%)],
  [#text(size: fs(14pt), fill: accentColor)[#pronouns]
    #h(5pt)
    #text(
      font: headerFont,
      size: fs(32pt),
      fill: regularColors.darkgray,
    )[#firstName]
    #h(5pt)
    #text(font: headerFont, size: fs(32pt))[#lastName]],
))
#v(0fr)
