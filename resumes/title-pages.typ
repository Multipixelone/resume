#import "../src/lib.typ": cv
#import "../src/utils/merge.typ": mergeDicts
#let base = toml("../metadata/metadata.toml")
#let repSheetMetadata = toml("../metadata/rep-sheet.toml")
#let titlePagesOverride = toml("../metadata/title-pages-metadata.toml")
#let metadata = mergeDicts(
  mergeDicts(base, repSheetMetadata),
  titlePagesOverride,
)

// The website's Callboard palette (website/src/styles/site.css). Keep this
// treatment local to the song dividers, not the resume or letter templates.
#let paper = rgb("#f7f4ed")
#let ink = rgb("#2b2520")
#let muted = rgb("#6f6456")
#let rust = rgb("#b54a00")
#let rule = rgb("#ddd6c6")

#show: cv.with(metadata)
#set page(fill: paper, margin: (x: 0.75in, y: 0.65in))
#set text(fill: ink, hyphenate: false)

// Balance a two-line title without hard-coded breaks in the song data. A
// future title too long for two lines falls back to normal paragraph wrapping.
#let songTitle(title) = {
  set text(font: "Cooper*", weight: 900, size: 44pt, tracking: -0.025em)
  set block(above: 0pt, below: 0pt)
  layout(size => {
    let words = title.split(" ")
    let split = none
    let imbalance = none
    if measure(title).width > size.width {
      for i in range(1, words.len()) {
        let first = measure(words.slice(0, i).join(" ")).width
        let last = measure(words.slice(i).join(" ")).width
        let difference = calc.abs(first - last)
        if (
          calc.max(first, last) <= size.width
            and (
              imbalance == none or difference < imbalance
            )
        ) {
          split = i
          imbalance = difference
        }
      }
    }
    if split == none { title } else {
      [#words.slice(0, split).join(" ")\ #words.slice(split).join(" ")]
    }
  })
}

#let titlePage(song) = {
  set page(header: none)
  // A level playbill heading with generous space. Long song and show titles
  // may wrap.
  align(left + horizon, block(width: 100%)[
    #set par(leading: 0.12em)
    #songTitle(song.title)
    #if song.source != "" [
      #v(16pt)
      #text(size: 14pt, fill: muted, style: "italic")[#if (
        song.source_type == "musical"
      ) [from] else [by]]
      #v(5pt)
      #block[
        #text(
          size: 22pt,
          fill: rust,
          song.at("source_full", default: song.source),
        )
      ]
    ]
  ])
  align(left + bottom, block(width: 100%)[
    #pad(bottom: 36pt)[
      #line(length: 100%, stroke: (
        paint: rule,
        thickness: 0.7pt,
        dash: "dashed",
      ))
      #v(12pt)
      #text(size: 17pt, song.composer)
      #v(6pt)
      #text(
        size: 11pt,
        fill: muted,
      )[#song.type #h(6pt) · #h(6pt) #song.bars bars]
    ]
  ])
  // No footer-only sheet after the last song.
  pagebreak(weak: true)
}

#for (_, category) in metadata.songs {
  for (_, song) in category {
    titlePage(song)
  }
}
