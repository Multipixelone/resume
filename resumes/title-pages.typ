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

#let songStyle(str) = {
  text(
    font: headerFont,
    size: 32pt,
    fill: regularColors.darkgray,
    str,
  )
}

#let titlePage(song) = {
  align(center)[
    songStyle(#song.title) \
    #song.source \
    #song.composer \
    #song.type \
    #song.bars bars
  ]
  pagebreak()
}

#for (_, category) in metadata.songs {
  for (_, song) in category {
    titlePage(song)
  }
}
