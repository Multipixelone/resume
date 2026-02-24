#import "../src/lib.typ": cvEntry
#let metadata = toml("../metadata/metadata.toml")
#let cvEntry = cvEntry.with(metadata: metadata)

#cvEntry(
  title: [Bachelor of Fine Arts in Musical Theatre],
  society: [CAP21 / Molloy University],
  date: [2022 - 2026],
  location: [NYC],
  logo: image("../src/logos/molloy.png"),
  // description: list(
  //   [Thesis: Predicting Customer Churn in Telecommunications Industry using Machine Learning Algorithms and Network Analysis],
  //   [Course: Big Data Systems and Technologies, Data Mining and Exploration, Natural Language Processing],
  // ),
)
