#import "./src/lib.typ": cv, cvSection
#let metadata = toml("./metadata/rep-sheet.toml")
#let cvSection = cvSection.with(metadata: metadata)


#show: cv.with(
  metadata,
  // profilePhoto: image("./metadata/qr-code.png")
)

#set text(
  size: 10pt
)

#let repTable(metadata) = {
  let songStyle(str) = {
    align(left, text(size: 10pt, str))
  }
  let songs = metadata

  table(
    columns: (25%, 20%, 22%, 15%, 10%, 8%),
    inset: 3.5pt,
    column-gutter: 0pt,
    stroke: none,
    ..for (c) in songs {
      let song = c.at(1).title
      let source = c.at(1).source
      let composer = c.at(1).composer
      let type = c.at(1).type
      let time = c.at(1).time
      let bars = c.at(1).bars
      (songStyle(song), songStyle(source), songStyle(composer), songStyle(type), songStyle(time), songStyle(bars))
    }
  )
}

#cvSection("Golden Age")
#table(
    columns: (25%, 20%, 22%, 15%, 10%, 8%),
    inset: 3.5pt,
    column-gutter: 0pt,
    stroke: none,
    table.header(
      [*Song*], [*Source*], [*Composer*], [*Type*], [*Time*], [*Bars*],
    )
)
#repTable(metadata.songs.goldenage)

#cvSection("Contemporary")
#repTable(metadata.songs.contemporary)

#cvSection("Pop / Rock")
#repTable(metadata.songs.poprock)

#cvSection("Sondheim")
#repTable(metadata.songs.sondheim)

#cvSection("Specialty")
#repTable(metadata.songs.speciality)
