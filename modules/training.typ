#import "../src/lib.typ": cvSection, cvPerformance, cvSkill, hBar, cvEntry
#let metadata = toml("../metadata/metadata.toml")
#let training = toml("../metadata/training.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Training")

#cvEntry(
  title: [Bachelor of Fine Arts in Musical Theatre],
  society: [CAP21 / Molloy University],
  date: [2022 - 2026],
  location: [NYC],
  // logo: image("../src/logos/ucla.png"),
  // description: list(
  //   [Thesis: Predicting Customer Churn in Telecommunications Industry using Machine Learning Algorithms and Network Analysis],
  //   [Course: Big Data Systems and Technologies #hBar() Data Mining and Exploration #hBar() Natural Language Processing],
  // ),
)

#cvSkill(
  type: [Voice],
  info: [Julia Kershetsky #hBar() Farah Alvin #hBar() Rick Lewis],
)

#cvSkill(
  type: [Acting],
  info: [Andy Schneeflock #hBar() Helen Farmer #hBar() Aimée Francis #hBar() Melissa Firlit #hBar() Del Lewis #hBar() Sarah Jane Hardy],
)

#cvSkill(
  type: [Dance],
  info: [Kristyn Pope #hBar() Lori Leshner #hBar() James Bulleri #hBar() Laura Hizcynskyj],
)

// #cvPerformance(training)
