#import "./src/lib.typ": cv
#let metadata = toml("metadata.toml")

#show: cv.with(
  metadata,
)

