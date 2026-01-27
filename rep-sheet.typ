#import "./src/lib.typ": cv
#let metadata = toml("./metadata/rep-sheet.toml")

#show: cv.with(
  metadata,
  profilePhoto: image("./metadata/qr-code.png")
)

