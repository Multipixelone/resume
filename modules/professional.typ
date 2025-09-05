#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata/metadata.toml")
#let professional = toml("../metadata/professional.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Professional Theatre")

#cvPerformance(professional)
