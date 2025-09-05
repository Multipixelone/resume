#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata/metadata.toml")
#let educational = toml("../metadata/educational.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Educational Theatre")

#cvPerformance(educational)
