#import "../src/lib.typ": cvEntry, cvPerformance, cvSection, cvSkill, hBar
#let metadata = toml("../metadata/metadata.toml")
#let training = toml("../metadata/training.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Voiceover")

#cvEntry(
  title: [Over 1,000 5-star reviews from clients worldwide],
  society: [Freelance Voiceover Artist],
  date: [2013 - Present],
  location: [www.fiverr.com/tunnelmaker],
  // logo: image("../src/logos/ucla.png"),
  // description: list(
  //   [Thesis: Predicting Customer Churn in Telecommunications Industry using Machine Learning Algorithms and Network Analysis],
  //   [Course: Big Data Systems and Technologies #hBar() Data Mining and Exploration #hBar() Natural Language Processing],
  // ),
)

