/*
 * Entry point for the package
 */

/* Packages */
#import "./cv.typ": *
#import "./letter.typ": *
#import "./utils/lang.typ": isNonLatin
#import "./utils/styles.typ": latinFontList, latinHeaderFont, overwriteFonts

/// Resolve the (regularFonts, headerFont) pair for a given metadata.
/// Applies the metadata's [layout.fonts] override if present, then injects
/// a non-Latin font into both lists when the language requires it.
#let _resolveFonts(metadata) = {
  let resolved = overwriteFonts(metadata, latinFontList, latinHeaderFont)
  let regularFonts = resolved.regularFonts
  let headerFont = resolved.headerFont
  if isNonLatin(metadata.language) {
    let nl = metadata.lang.non_latin.font
    regularFonts.insert(2, nl)
    headerFont = nl
  }
  (regularFonts: regularFonts, headerFont: headerFont)
}

/* Layout */
#let cv(
  metadata,
  profilePhoto: image("./avatar.png"),
  doc,
) = {
  let fonts = _resolveFonts(metadata)

  set text(font: fonts.regularFonts, weight: "regular", size: 10pt)
  set align(left)
  set page(
    paper: "us-letter",
    margin: (left: 1.4cm, right: 1.4cm, top: 1.3cm, bottom: 1.3cm),
    footer: if sys.inputs.at("no_footer", default: "false") == "true" {
      none
    } else { _cvFooter(metadata) },
  )

  let showHeader = metadata.layout.header.at("display_header", default: true)
  if showHeader {
    _cvHeader(
      metadata,
      profilePhoto,
      fonts.headerFont,
      regularColors,
      awesomeColors,
    )
  }
  doc
}

#let coverLetter(
  metadata,
  profilePhoto: image("./avatar.png"),
  doc,
) = {
  let fonts = _resolveFonts(metadata)

  set text(font: fonts.regularFonts, weight: "regular", size: 11pt)
  set align(left)
  set page(
    paper: "us-letter",
    margin: (left: 1.4cm, right: 1.4cm, top: 1.1cm, bottom: 1.1cm),
    footer: _coverLetterFooter(metadata),
  )
  set par(leading: 0.75em, spacing: 1.4em)

  _cvHeader(
    metadata,
    profilePhoto,
    fonts.headerFont,
    regularColors,
    awesomeColors,
  )
  doc
}

#let letter(
  metadata,
  doc,
  myAddress: "Your Address Here",
  recipientName: "Company Name Here",
  recipientAddress: "Company Address Here",
  date: datetime.today().display(),
  subject: "Subject: Hey!",
  signature: "",
) = {
  let fonts = _resolveFonts(metadata)

  set text(font: fonts.regularFonts, weight: "regular", size: 9pt)
  set align(left)
  set page(
    paper: "us-letter",
    margin: (left: 1.4cm, right: 1.4cm, top: .8cm, bottom: .4cm),
    footer: letterHeader(
      myAddress: myAddress,
      recipientName: recipientName,
      recipientAddress: recipientAddress,
      date: date,
      subject: subject,
      metadata: metadata,
      awesomeColors: awesomeColors,
    ),
  )
  set text(size: 12pt)

  doc

  if signature != "" {
    letterSignature(signature)
  }
}
