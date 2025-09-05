#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata/metadata.toml")
#let film = toml("../metadata/film.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Film")

#cvPerformance(film)
