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

#let rep-table(..songs) = table(
  // columns: (auto, auto, auto, auto, auto, auto, auto, auto),
  columns: (22%, 20%, 18%, 8%, 8%, 6%, 8%, 5%),
  stroke: none,
  inset: 3.5pt,
  column-gutter: 0pt,
  align: left,
  ..songs
)

#cvSection("Golden Age")

#rep-table(
  table.header(
    [*Song*], [*Source*], [*Composer*], [*Type*], [*Range*], [*Time*], [*Bars*], [*Notes*]
  ),
  [All The Things You Are], [Very Warm for May], [Hammerstein & Kern], [Ballad], [C4-D4], [1:15], [32-Bar], [],
  [I Love to Sing-a], [The Singing Kid], [Arlen & Yip], [Uptempo], [C4-D4], [1:15], [32, 16]
)

#cvSection("Contemporary")

#cvSection("Pop / Rock")

#cvSection("Sondheim")

#cvSection("Specialty")
