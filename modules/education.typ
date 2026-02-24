#import "../src/lib.typ": cvSection
#let metadata = toml("../metadata/metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Education")

#include "_education-content.typ"
