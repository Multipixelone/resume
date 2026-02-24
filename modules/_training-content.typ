#import "../src/lib.typ": cvTraining
#let metadata = toml("../metadata/metadata.toml")
#let training = toml("../metadata/training.toml")

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
