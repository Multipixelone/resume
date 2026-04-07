#import "../src/lib.typ": cv, cvSection
#import "../src/utils/merge.typ": mergeDicts
#let baseMetadata = toml("../metadata/metadata.toml")
#let repSheetMetadata = toml("../metadata/rep-sheet.toml")
#let metadata = mergeDicts(baseMetadata, repSheetMetadata)
#let cvSection = cvSection.with(metadata: metadata)

#show: cv.with(
  metadata,
  // profilePhoto: image("../metadata/qr-code.png")
)
#let titlePage(song) = {
  align(center)[
    #song.title \
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
