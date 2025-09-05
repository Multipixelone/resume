#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata/metadata.toml")
#let training = toml("../metadata/training.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Training")

#cvPerformance(training)
