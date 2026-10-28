#let hBar() = [#h(3pt) | #h(3pt)]

#let latinFontList = (
  "Source Sans Pro",
  "Source Sans 3",
  "Linux Libertine",
  "Font Awesome 7 Brands",
  "Font Awesome 7 Free",
)

#let latinHeaderFont = "Roboto"

/// Every layout type size passes through `fs`. Sabon Next, the resume face, has
/// an x-height about 11% taller than a classic Garamond, so 0.95 sets its body
/// at 9.5pt.
#let typeScale = 0.95
#let fs(size) = size * typeScale

#let awesomeColors = (
  skyblue: rgb("#0395DE"),
  red: rgb("#DC3522"),
  nephritis: rgb("#27AE60"),
  concrete: rgb("#606060"),
  darknight: rgb("#131A28"),
)

#let regularColors = (
  subtlegray: rgb("#ededee"),
  lightgray: rgb("#343a40"),
  darkgray: rgb("#212529"),
)

/// Set the accent color for the document
#let setAccentColor(awesomeColors, metadata) = {
  let param = metadata.layout.awesome_color
  return if param in awesomeColors {
    awesomeColors.at(param)
  } else {
    rgb(param)
  }
}

/// Overwrite the default fonts if the metadata has custom font values
///
/// - metadata (array): the metadata object
/// - latinFontList (array): the default list of latin fonts
/// - latinHeaderFont (string): the default header font
/// -> array
#let overwriteFonts(metadata, latinFontList, latinHeaderFont) = {
  let metadataFonts = metadata.layout.at("fonts", default: [])
  let regularFonts = latinFontList
  let headerFont = latinHeaderFont
  if metadataFonts.len() > 0 {
    regularFonts = metadataFonts.at("regular_fonts")
    headerFont = metadataFonts.at("header_font")
  }
  return (regularFonts: regularFonts, headerFont: headerFont)
}
