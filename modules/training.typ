#import "../src/lib.typ": cvSection, cvPerformance
#let metadata = toml("../metadata.toml")
#let training = toml("../training.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Training")

#cvPerformance(training)
