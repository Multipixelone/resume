#import "../src/lib.typ": cv, cvSection
#import "../src/utils/merge.typ": mergeDicts
#import "../src/utils/styles.typ": (
  awesomeColors, latinFontList, latinHeaderFont, overwriteFonts, regularColors,
  setAccentColor,
)
#let base = toml("../metadata/metadata.toml")
#let repSheetMetadata = toml("../metadata/rep-sheet.toml")
#let titlePagesOverride = toml("../metadata/title-pages-metadata.toml")
#let metadata = mergeDicts(
  mergeDicts(base, repSheetMetadata),
  titlePagesOverride,
)

#let accentColor = setAccentColor(awesomeColors, metadata)
#let headerFont = overwriteFonts(
  metadata,
  latinFontList,
  latinHeaderFont,
).headerFont

#show: cv.with(
  metadata,
  // profilePhoto: image("../metadata/qr-code.png")
)

#let titlePage(song) = {
  set page(header: none)
  align(center + horizon)[
    #text(
      font: headerFont,
      size: 36pt,
      fill: regularColors.darkgray,
      song.title,
    )
    #if song.source != "" [
      \ #v(5pt)
      #text(size: 14pt, fill: regularColors.lightgray, style: "italic")[#if (
        song.source_type == "musical"
      ) [from] else [by]]
      \ #v(-11pt)
      #text(
        font: headerFont,
        size: 20pt,
        fill: regularColors.darkgray,
        song.source,
      )
    ]
    // #line(length: 30%, stroke: 0.9pt + accentColor)
  ]
  align(center + bottom)[
    #pad(bottom: 4em)[
      #text(size: 16pt, fill: regularColors.lightgray)[
        #song.composer \
        #context {
          let composerWidth = measure(text(size: 16pt)[#song.composer]).width
          line(length: composerWidth + 2.5em, stroke: 0.9pt + accentColor)
        }
        #text(size: 11pt)[#song.type #h(6pt) · #h(6pt) #song.bars bars]
      ]
    ]
  ]
  pagebreak()
}

#for (_, category) in metadata.songs {
  for (_, song) in category {
    titlePage(song)
  }
}
