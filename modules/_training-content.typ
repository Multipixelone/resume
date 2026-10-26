#import "../src/lib.typ": cvTraining
#let training = toml("../metadata/education.toml").training

// A row continuing the discipline above it leaves the discipline blank.
#for (i, row) in training.enumerate() {
  let continued = i > 0 and training.at(i - 1).discipline == row.discipline
  cvTraining(
    type: if continued { [] } else { eval(row.discipline, mode: "markup") },
    info: eval(row.technique, mode: "markup"),
    instructors: eval(row.instructors.join(", "), mode: "markup"),
  )
}
