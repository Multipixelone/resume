#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata.toml")
#let film = toml("../film.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Film")

#cvPerformance(film)
