#import "../src/lib.typ": cvEntry
#let metadata = toml("../metadata/metadata.toml")
#let cvEntry = cvEntry.with(metadata: metadata)

// Strings go through markup, as the hand-written entries did, so quotes stay typographic.
#for degree in toml("../metadata/education.toml").degrees {
  cvEntry(
    title: eval(degree.title, mode: "markup"),
    society: eval(degree.school, mode: "markup"),
    date: eval(degree.date, mode: "markup"),
    location: eval(degree.location, mode: "markup"),
    logo: if "logo" in degree { image("../src/logos/" + degree.logo) } else {
      ""
    },
  )
}
