#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata/metadata.toml")
#let technical = toml("../metadata/technical.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Technical Theatre")

#cvPerformance(technical)
