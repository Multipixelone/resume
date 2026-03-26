#import "../src/lib.typ": cvPerformance, cvSection
#let metadata = toml("../metadata/metadata.toml")
#let professional = toml("../metadata/theatre.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Theatre")

#cvPerformance(professional)
