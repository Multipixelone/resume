#let metadata = toml("./metadata/metadata.toml")
#import "./src/utils/styles.typ": awesomeColors, regularColors, setAccentColor, latinFontList, latinHeaderFont, overwriteFonts

#let accentColor = setAccentColor(awesomeColors, metadata)
#let headerFont = overwriteFonts(metadata, latinFontList, latinHeaderFont).headerFont
#let firstName = metadata.personal.first_name
#let lastName = metadata.personal.last_name
#let pronouns = metadata.personal.pronouns

#set page(paper: "us-letter", margin: (x: 1.4cm, y: 1.1cm))

#v(1fr)
#align(center,
  table(
    columns: (auto,),
    inset: 0pt,
    stroke: none,
    row-gutter: 1em,
    align: left,
    [#image("./website/public/assets/portrait.jpg", height: 85%)],
    [#text(font: headerFont, size: 32pt, fill: regularColors.darkgray)[#firstName]
     #h(5pt)
     #text(font: headerFont, size: 32pt)[#lastName]
     #h(5pt)
     #text(size: 14pt, fill: accentColor)[#pronouns]],
  )
)
#v(1fr)
