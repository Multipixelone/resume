#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata.toml")
#let educational = toml("../educational.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Educational Theatre")

#cvPerformance(educational)
