#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata/metadata.toml")
#let commercial = toml("../metadata/commercial.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Commercial")

#cvPerformance(commercial)
