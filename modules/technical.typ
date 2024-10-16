#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata.toml")
#let technical = toml("../technical.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Technical Theatre")

#cvPerformance(technical)
