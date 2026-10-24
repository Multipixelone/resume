// Business card artwork, front then back. scripts/business_cards.py stages
// this file with the fonts, the rust QR and an optional headshot, passes the
// profile as JSON in sys.inputs.data, and validates the PDF it gets back.
// Coordinates follow the approved proof: points from the trim's bottom left.

#let data = json(bytes(sys.inputs.data))
#let fonts = data.fonts

#let INK = rgb("#2b2520")
#let RUST = rgb("#b54a00")
#let MUTED = rgb("#6f6456")
#let TRIM = (252pt, 144pt)
#let BLEED = 9pt
#let MARGIN = 18pt
#let NAME = 40pt
#let CONTACT = 10pt
#let URL = 7pt
#let ROW = 24pt
#let NAME_CAP = 1434 / 2000
#let CONTACT_CAP = 685 / 1000
#let ROLE = 8pt
#let PRONOUNS = 8.5pt
#let UNDER_NAME = 9pt // From the surname baseline to the first small line's x-height.
#let LINE_STEP = 11pt
#let SMALL_CAP = 457 / 1000
#let ITALIC_X = 454 / 1000
#let SURNAME_RSB = 50 / 2000 // Cooper Black "s": the role ends on the surname's ink.
#let ROLE_TRACKING = (0.04, 0.14) // em
// The QR is 25 modules inside a four-module quiet zone. The address under it
// keeps two of those modules clear, so it reads as the code's caption.
#let QR_SIZE = 96pt
#let MODULE = QR_SIZE / 33
#let SYMBOL = 25 * MODULE
#let CAPTION_GAP = 2 * MODULE
#let URL_TOP = 1647 / 2048 // PragmataPro "i" dot, the address's tallest ink.
// A theatre 8x10 (4:5) at the full safe height, standing at the margins.
#let HEADSHOT = (MARGIN, MARGIN, 0.8 * (TRIM.at(1) - 2 * MARGIN), TRIM.at(1) - 2 * MARGIN)

#set document(
  title: "Finn Rutis - business card",
  author: "Finn Rutis",
  description: "Front then back; unprinted stock; 3.5 x 2 inch trim; 1/8 inch bleed",
  date: none,
)
#set page(width: TRIM.at(0) + 2 * BLEED, height: TRIM.at(1) + 2 * BLEED, margin: 0pt)
// A placed line's top edge is its baseline, so `at` takes proof baselines.
#set text(top-edge: "baseline", bottom-edge: "baseline", fill: INK, hyphenate: false)

// Place a body with its top left (a text baseline) at trim point (x, y).
#let at(x, y, body) = place(top + left, dx: BLEED + x, dy: BLEED + TRIM.at(1) - y, body)
#let width(body) = measure(box(body)).width

#let cooper(body, ..args) = text(font: fonts.name, size: NAME, ..args, body)
#let sabon(size, body, ..args) = text(font: fonts.body, size: size, ..args, body)

// Approved ten-point marks, plus a matching original GitHub cat outline, in
// the proof's 24-unit icon space (y down).
#let ICONS = (
  mail: ```
    <rect x="2.8" y="4.8" width="18.4" height="14.4" rx="2.2"/>
    <path d="M3.4 6.4 L12 12.5 L20.6 6.4"/>
  ```.text,
  phone: ```
    <path d="M21 16.5 L16 14 L13.5 16.5 C10.5 15 9 13.5 7.5 10.5 L10 8 L7.5 3 L4 3
             C1 3 4 12 8 16 C12 20 21 23 21 20 Z"/>
  ```.text,
  instagram: ```
    <rect x="3.2" y="3.2" width="17.6" height="17.6" rx="5"/>
    <circle cx="12" cy="12" r="4.1"/>
    <circle cx="17.2" cy="6.8" r="1.15" fill="currentColor" stroke="none"/>
  ```.text,
  // Cat ears, broad head, neck/legs and curling tail distinguish this from
  // Instagram's rounded camera.
  github: ```
    <path d="M9 21 L9 18 C9 16.6 9.6 15.8 10.1 15.5 C5.2 15.2 3.2 13.5 3.2 9.8
             C3.2 8.3 3.8 7.1 4.8 6.1 C4.4 5 4.5 3.4 5 2.5 C6.8 2.5 8.5 3.6 9.1 4.1
             C11 3.6 13 3.6 14.9 4.1 C15.5 3.6 17.2 2.5 19 2.5 C19.5 3.4 19.6 5 19.2 6.1
             C20.2 7.1 20.8 8.3 20.8 9.8 C20.8 13.5 18.8 15.2 13.9 15.5
             C14.4 15.8 15 16.6 15 18 L15 21 M9 18.7 C5.7 19.6 4.6 18.4 3.8 16.7
             C3.2 15.5 2.3 15.3 1.8 15.3"/>
  ```.text,
)

#let icon(kind) = {
  assert(kind in ICONS, message: "Unknown contact icon: " + kind)
  let svg = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24' "
      + "color='" + RUST.to-hex() + "' fill='none' stroke='" + RUST.to-hex() + "' "
      + "stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'>"
      + ICONS.at(kind)
      + "</svg>"
  )
  image(bytes(svg), format: "svg", width: 10pt)
}

#let contact-baselines(count) = {
  assert(count in (2, 3), message: "expected two or three contact rows")
  let middle = (TRIM.at(1) - CONTACT_CAP * CONTACT) / 2
  range(count).map(i => middle + ((count - 1) / 2 - i) * ROW)
}

// The name keeps the approved proof geometry. Below it, the role and the
// pronouns share the margin; the block is centred from the top of "Finn" to
// the pronoun baseline.
#let front() = {
  let leading = 0.87 * NAME
  let role = data.role
  let under = UNDER_NAME + if role != none { SMALL_CAP * ROLE + LINE_STEP } else { ITALIC_X * PRONOUNS }
  let top = (TRIM.at(1) + NAME_CAP * NAME + leading + under) / 2
  let finn = top - NAME_CAP * NAME
  let bottom = finn - leading - under
  let surname-x = MARGIN + 0.19 * NAME
  let surname-end = surname-x + width(cooper(data.last_name))
  at(MARGIN, finn, cooper(data.first_name))
  at(surname-x, finn - leading, cooper(data.last_name, fill: RUST))
  if role != none {
    // Letterspace the small caps so they run from the margin to the surname's ink.
    let natural = width(sabon(ROLE, smallcaps(role)))
    let tracking = (surname-end - SURNAME_RSB * NAME - MARGIN - natural) / calc.max(role.clusters().len() - 1, 1)
    if tracking < ROLE_TRACKING.at(0) * ROLE { panic("Role line is wider than the name; shorten it") }
    // A short role stays at the widest readable spacing and ends before the name.
    at(MARGIN, bottom + LINE_STEP, sabon(ROLE, smallcaps(role), tracking: calc.min(tracking, ROLE_TRACKING.at(1) * ROLE)))
  }
  at(MARGIN, bottom, sabon(PRONOUNS, data.pronouns, style: "italic", fill: MUTED))
  let contacts = data.contacts
  let text-x = TRIM.at(0) - MARGIN - calc.max(..contacts.map(((_, value)) => width(sabon(CONTACT, value))))
  let icon-x = text-x - 1.5 * CONTACT
  if icon-x <= surname-end + 2pt { panic("Contact column overlaps the name; review layout") }
  let rule-x = (surname-end + icon-x) / 2
  let dashes = calc.round((top - bottom + 2.7pt) / 4.2pt)
  let gap = (top - bottom - 1.5pt * dashes) / (dashes - 1)
  // Drawn upward from the pronoun baseline, as the proof's dash phase runs.
  at(rule-x, top, line(start: (0pt, top - bottom), end: (0pt, 0pt),
    stroke: (paint: RUST, thickness: 0.45pt, dash: (1.5pt, gap))))
  for ((kind, value), baseline) in contacts.zip(contact-baselines(contacts.len())) {
    at(icon-x, baseline + 8pt, icon(kind))
    at(text-x, baseline, sabon(CONTACT, value))
  }
}

// The code and its address are centred together on the card's height. A
// headshot stands at the safe margins, and the code then sits midway between
// the print and the card's right edge.
#let back() = {
  let url-y = (TRIM.at(1) - (SYMBOL + CAPTION_GAP + URL_TOP * URL)) / 2
  let middle = TRIM.at(0) / 2
  if data.headshot {
    let (x, y, w, h) = HEADSHOT
    at(x, y + h, image("headshot.jpg", width: w, height: h, fit: "stretch"))
    middle = (x + w + TRIM.at(0)) / 2
  }
  let qr-y = url-y + URL_TOP * URL + CAPTION_GAP - 4 * MODULE
  at(middle - QR_SIZE / 2, qr-y + QR_SIZE, image("qr.png", width: QR_SIZE, scaling: "pixelated"))
  let address = text(font: fonts.mono, size: URL, data.address)
  at(middle - width(address) / 2, url-y, address)
}

// Text widths come from measure(), so the layout runs in context.
#context front()
#pagebreak()
#context back()
