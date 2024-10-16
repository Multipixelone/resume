#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata.toml")
#let commercial = toml("../commercial.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Commercial")

#cvPerformance(commercial)
