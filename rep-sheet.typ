#import "./src/lib.typ": cv, cvSection
#import "./src/utils/merge.typ": mergeDicts
#let baseMetadata = toml("./metadata/metadata.toml")
#let repSheetMetadata = toml("./metadata/rep-sheet.toml")
#let metadata = mergeDicts(baseMetadata, repSheetMetadata)
#let cvSection = cvSection.with(metadata: metadata)

#show: cv.with(
  metadata,
  // profilePhoto: image("./metadata/qr-code.png")
)
#let repTable(metadata) = {
  let songStyle(str) = {
    align(left, text(size: 10pt, str))
  }
  let songs = metadata

  table(
    columns: (28%, 25%, 29%, 12%, 8%),
    inset: 3.5pt,
    column-gutter: 0pt,
    stroke: none,
    ..for (c) in songs {
      let song = c.at(1).title
      let source = c.at(1).source
      let composer = c.at(1).composer
      let type = c.at(1).type
      // let time = c.at(1).time
      let bars = c.at(1).bars
      (
        songStyle(song),
        songStyle(source),
        songStyle(composer),
        songStyle(type),
        songStyle(bars),
      )
    }
  )
}
#cvSection("Golden Age")
// #table(
//     columns: (28%, 25%, 29%, 12%, 8%),
//     inset: 3.5pt,
//     column-gutter: 0pt,
//     stroke: none,
//     table.header(
//       [*Song*], [*Source*], [*Composer*], [*Type*], [*Bars*],
//     )
// )
#repTable(metadata.songs.goldenage)

#cvSection("Contemporary")
#repTable(metadata.songs.contemporary)

#cvSection("Pop / Rock")
#repTable(metadata.songs.poprock)

#cvSection("Sondheim")
#repTable(metadata.songs.sondheim)

#cvSection("Specialty")
#repTable(metadata.songs.speciality)
