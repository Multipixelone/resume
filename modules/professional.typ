#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata.toml")
#let professional = toml("../professional.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Professional Theatre")

#cvPerformance(professional)
