#import "./src/lib.typ": cv, cvSection
#let metadata = toml("./metadata/rep-sheet.toml")
#let cvSection = cvSection.with(metadata: metadata)

#show: cv.with(
  metadata,
  // profilePhoto: image("./metadata/qr-code.png")
)

#cvSection("Golden Age")

#cvSection("Contemporary")

#cvSection("Pop / Rock")

#cvSection("Sondheim")

#cvSection("Specialty")
