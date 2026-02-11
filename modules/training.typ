#import "../src/lib.typ": cvSection, cvPerformance, cvTraining, hBar, cvEntry
#import "../src/utils/styles.typ": latinFontList, latinHeaderFont, awesomeColors, regularColors, setAccentColor, hBar
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
  logo: image("../src/logos/molloy.png"),
  // description: list(
  //   [Thesis: Predicting Customer Churn in Telecommunications Industry using Machine Learning Algorithms and Network Analysis],
  //   [Course: Big Data Systems and Technologies, Data Mining and Exploration, Natural Language Processing],
  // ),
)

#cvTraining(
  type: [Voice],
  info: [Linklater, VO Artist],
  instructors: [Julia Kershetsky, Chris Citera, Farah Alvin, Rick Lewis],
)

#cvTraining(
  type: [Acting],
  info: [Meisner, Improvisation],
  instructors: [Andy Schneeflock, Melissa Firlit, Helen Farmer, Aimée Francis, Michelle Beck, Peter Marciano, Del Lewis, Sarah Jane Hardy],
)

#cvTraining(
  type: [Dance],
  info: [Jazz (Int.)],
  instructors: [Kristyn Pope, Lori Leshner, Bethany Moore, Laura Hizcynskyj],
)
#cvTraining(
  type: [],
  info: [Ballet (Int.)],
  instructors: [Eureka Nakano, Marilyn D'Honau, James Bulleri],
)
#cvTraining(
  type: [],
  info: [Tap (Beginner)],
  instructors: [Kristyn Pope, John Scacchetti],
)

// #cvPerformance(training)
