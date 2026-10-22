---
name: Finn Rutis
description: A performer's callboard on warm paper, with torn tickets, tilted photo prints and a playbill-sized name.
colors:
  accent: "#b54a00"
  accent-hover: "#8c3800"
  paper: "#f7f4ed"
  paper-shade: "#efeadd"
  ticket-paper: "#fcfaf5"
  ink: "#2b2520"
  muted: "#6f6456"
  border: "#ddd6c6"
  selection-bg: "#f5d9c4"
typography:
  display:
    fontFamily: '"Cooper*", Georgia, serif'
    fontSize: "clamp(6rem, 12.8vw, 11.5rem)"
    fontWeight: 900
    lineHeight: 0.87
    letterSpacing: "-0.055em"
  headline:
    fontFamily: '"Cooper*", Georgia, serif'
    fontSize: "clamp(3rem, 6.5vw, 5.5rem)"
    fontWeight: 900
    lineHeight: 1
    letterSpacing: "-0.04em"
  title:
    fontFamily: '"Cooper*", Georgia, serif'
    fontSize: "clamp(2.25rem, 5vw, 4rem)"
    fontWeight: 700
    lineHeight: 1.18
  title-show:
    fontFamily: '"Cooper*", Georgia, serif'
    fontSize: "clamp(1.875rem, 3vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.025em"
  subtitle:
    fontFamily: '"Sabon Next", Georgia, "Times New Roman", serif'
    fontSize: "clamp(1.75rem, 3vw, 2.25rem)"
    fontWeight: 700
    lineHeight: 1.18
  body:
    fontFamily: '"Sabon Next", Georgia, "Times New Roman", serif'
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.6
  body-lead:
    fontFamily: '"Sabon Next", Georgia, "Times New Roman", serif'
    fontSize: "clamp(1.2rem, 1.65vw, 1.4rem)"
    fontWeight: 400
    lineHeight: 1.5
  link:
    fontFamily: '"Sabon Next", Georgia, "Times New Roman", serif'
    fontSize: "1.0625rem"
    fontWeight: 600
  label:
    fontFamily: '"PragmataPro Mono Liga", ui-monospace, SFMono-Regular, Menlo, monospace'
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0.14em"
  caption-mono:
    fontFamily: '"PragmataPro Mono Liga", ui-monospace, SFMono-Regular, Menlo, monospace'
    fontSize: "0.6875rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0.05em"
rounded:
  none: "0px"
  sm: "6px"
  pill: "999px"
spacing:
  gutter: "1.5rem"
  gutter-md: "2.5rem"
  gutter-lg: "4rem"
  column: "3rem"
  section: "clamp(4rem, 8vw, 7rem)"
components:
  text-link:
    textColor: "{colors.accent}"
    typography: "{typography.link}"
    height: "44px"
  text-link-hover:
    textColor: "{colors.accent-hover}"
  nav-link:
    textColor: "{colors.ink}"
    height: "44px"
    padding: "0 0.75rem"
  nav-link-current:
    backgroundColor: "{colors.paper-shade}"
    textColor: "{colors.accent-hover}"
  reel-slip:
    backgroundColor: "{colors.paper-shade}"
    textColor: "{colors.accent}"
    typography: "{typography.link}"
    height: "44px"
    padding: "0.5rem 1.15rem 0.55rem 1rem"
  brand-ticket:
    backgroundColor: "{colors.ticket-paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.5rem 1rem 0.5rem 0.85rem"
  ticket-stub:
    backgroundColor: "{colors.ticket-paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    width: "19rem"
  ticket-stub-action:
    backgroundColor: "{colors.selection-bg}"
    textColor: "{colors.accent-hover}"
    height: "44px"
    padding: "0.7rem 1.75rem 0.7rem 1.25rem"
  ticket-stub-action-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.ticket-paper}"
  photo-mat:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0.45rem"
  paper-sheet:
    backgroundColor: "{colors.paper-shade}"
    rounded: "{rounded.none}"
    padding: "1rem"
  kicker:
    textColor: "{colors.muted}"
    typography: "{typography.label}"
  footer-icon:
    textColor: "{colors.muted}"
    rounded: "{rounded.sm}"
    size: "2.75rem"
  footer-icon-hover:
    backgroundColor: "{colors.paper-shade}"
    textColor: "{colors.accent}"
  build-badge:
    backgroundColor: "{colors.paper-shade}"
    textColor: "{colors.muted}"
    rounded: "{rounded.pill}"
    padding: "0.28rem 0.8rem 0.32rem"
  build-badge-hover:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.accent}"
---

# Design System: Finn Rutis

## Overview

**Creative North Star: "The Callboard"**

The site is the backstage callboard: the board by the stage door where the cast list, a ticket, a few production photos and someone's scribbled notes get pinned up. It is working theatre, not a keepsake album and not a marquee. Everything on the page is a physical piece of printed paper (a photo print with a mat, a torn ticket stub, a paper slip, a resume sheet) resting at a slight angle on warm stock, with the name set as large as a playbill title. Paper has weight and casts a soft shadow; type and captions stay level and readable beside it.

Density is generous. One idea per viewport on the homepage: the name and headshot, then the current project, then the "On stage." spread. Supporting pages (resume, reel, contact, all resumes) keep the same paper and type but calm down: fewer angles, ruled lists, and plain links, so a casting director can get the PDF or the video without wading through decoration.

Scrapbook texture is welcome when it is real. A planned layer of blue ballpoint doodles, drawn by hand by a friend of Finn's and scanned, will annotate the board like notes in a script margin. `docs/doodles.md` owns that layer's rules. Confirmed rejections: the generic actor template site (centered headshot, stock nav, slideshow), the tech portfolio look (dark mode, terminal motifs, gradients, developer cards), and glossy showbiz (black and gold, glitter, marquee bulbs, rendered spotlight glow).

**Key Characteristics:**

- Warm cream paper with one burnt-orange accent; light only.
- Cooper Black at playbill scale for the name and big headings; Sabon Next for reading; PragmataPro as the small, tracked, uppercase backstage label voice.
- Printed objects with square corners, mats, resting angles and soft layered shadows.
- A torn-ticket motif shared by the header logo and the current-project stub.
- Motion that gives printed photos a brief, theatrical landing, then lets the paper respond to a hand; all of it is removed under reduced motion.
- Every action is a link. No buttons, no forms.

## Colors

Cream paper stock and warm brown ink, with a single worn-orange accent doing all the pointing.

### Primary

- **Marquee Rust** (#b54a00): the only hue. Links and their underlines, the surname "Rutis" in the homepage name, the brand ticket's thin left stripe, and the focus ring (3px solid, 5px offset). 4.85:1 on Playbill Paper, so it holds AA for body-size links.
- **Deep Marquee Rust** (#8c3800): the pressed and hovered state of Marquee Rust, and the color of small status text that has to read as "live": the current-project status line, the ticket's weekday/year line, the "Livestream available" line, photo index numbers, and the current nav slip's label. It is also the one solid fill: the ticket stub's printed "Admit one" end, with Ticket Stock lettering. 7.13:1 on paper.

### Neutral

- **Playbill Paper** (#f7f4ed): the page background and the mat color of every photo print and headshot.
- **Callboard Card** (#efeadd): the heavier backing stock. Paper shapes behind the hero and photo spread, nav slips, paper sheets around the resume preview and videos, off-stage slips, footer icon hover.
- **Ticket Stock** (#fcfaf5): the brightest paper, reserved for tickets (header brand ticket and current-project stub).
- **Program Ink** (#2b2520): all body text and headings, and the 1px top rule over spread headings and the artist statement. 13.77:1 on paper.
- **Faded Ink** (#6f6456): secondary text: kickers, mono labels, pronouns, directors, footer icons and meta. 5.26:1 on paper, 4.81:1 on Callboard Card.
- **Rule Line** (#ddd6c6): 1px hairlines between list rows, borders on slips and sheets, dashed ticket perforations, footer separator dots. Decorative only; never the sole boundary of something interactive.
- **Stub Blush** (#f5d9c4): text selection and the "Get tickets" band at the bottom of the ticket stub, the one place the accent is used as a tint.

The blog palette this was ported from also defines `--code-bg`, `--code-border` and `--glow`. The site does not use them; leave them out of new work unless code blocks arrive.

### Named Rules

**The One Rust Rule.** Marquee Rust and its deep shade are the only hues in the interface. Everything else is paper and ink. The planned ballpoint blue is ink drawn on the board, not interface color; it never marks a link, state or control.

**The Daylight Rule.** The site is light paper only (`color-scheme: light`). There is no dark theme, no toggle and no system-dark substitution.

## Typography

**Display Font:** Cooper* (Cooper Black 900 and Cooper Bold 700, local OFL faces in `static/fonts/cooper/`), with Georgia
**Body Font:** Sabon Next (with Georgia, Times New Roman)
**Label/Mono Font:** PragmataPro Mono Liga (with ui-monospace, SF Mono, Menlo)

**Character:** Cooper Black is the playbill: soft, heavy, warm and a little 1970s, set tight and enormous for the name. Sabon Next is the program note underneath, a quiet book serif. PragmataPro is the stage manager's hand: tiny, tracked, uppercase labels on tickets and kickers.

Sabon Next and PragmataPro load from `fonts.finnrut.is` and currently fail on localhost and any domain without license and CORS coverage, so screenshots today render Georgia and the system mono. The named families are the intent; a fallback screenshot is not approval of the typography.

### Hierarchy

- **Display** (Cooper Black 900, clamp(6rem, 12.8vw, 11.5rem), line-height 0.87, -0.055em): the artist name on `/` only. Two stacked lines, "Rutis" indented 0.19em and set in Marquee Rust. Below 640px it becomes one inline line at clamp(3rem, 15vw, 5.5rem).
- **Headline** (Cooper Black 900, clamp(3rem, 6.5vw, 5.5rem), line-height 1, -0.04em): spread headings like "On stage.", "Off stage." and the homepage's "Current project.", always with a full stop and a 1px Program Ink rule above.
- **Title** (Cooper Bold 700, clamp(2.25rem, 5vw, 4rem), line-height 1.18): page `h1` on supporting pages (Resume, Contact, Performance reel).
- **Title, show** (Cooper Bold 700, clamp(1.875rem, 3vw, 2.5rem), -0.025em): current-project show titles; photo note titles and off-stage titles use the same face at 1.125 to 2rem. Ticket dates use Cooper Black at clamp(2.25rem, 3.5vw, 2.75rem).
- **Subtitle** (Sabon Next 700, clamp(1.75rem, 3vw, 2.25rem)): default `h2`; `h3` is Sabon 700 at 1.5rem, credit titles at 1.25rem.
- **Body** (Sabon Next 400, 1.125rem, line-height 1.6): all reading text. Statement and off-stage copy cap at about 38em and 60ch.
- **Body lead** (Sabon Next 400, clamp(1.2rem, 1.65vw, 1.4rem), line-height 1.5): the homepage bio (max 36ch) and the artist statement.
- **Link** (Sabon Next 600, 1.0625rem): text links with arrows and nav items.
- **Label** (PragmataPro 400, 0.75rem, 0.14em, uppercase): section kickers ("Artist statement") and the current-project status line. Smaller relatives at 0.6875rem and 0.625rem carry ticket metadata, credit labels ("Venue", "Directed by"), photo indices, pronouns and file labels like "(PDF)".

### Named Rules

**The Playbill Rule.** Cooper is for names and titles only: the artist name, spread headings, page titles, show and photo titles, ticket dates and the brand mark. Never body copy, never labels.

**The Stage Manager Rule.** PragmataPro is a label voice: small (0.75rem or less outside file labels), tracked, usually uppercase, usually Faded Ink or Deep Marquee Rust. It is not a terminal and never sets a heading or a paragraph.

## Layout

A single centered shell, `min(100% - 2 x gutter, 75rem)`. Gutters are 1.25rem a side under 640px, 1.5rem by default, 2.5rem from 640px and 4rem from 1280px. Sections are separated by `section` spacing (clamp(4rem, 8vw, 7rem)); the photo spread takes a larger clamp(5rem, 10vw, 9rem) unless it follows the current project.

- **Homepage hero:** a two-column grid (1.13fr / 1fr, 4rem gap). Name top left, bio and links below it, the headshot spanning both rows on the right, inset from the edge.
- **Photo spread:** a 12-column grid with six named placements (wide, tall, small, wide-right, tall-left, small-right), each with its own column span, top offset and resting angle, so prints overlap the grid unevenly like pinned photos. One shared Callboard Card shape sits behind the first group.
- **Supporting pages:** an asymmetric label column and content column (minmax(14rem, 1fr) / 2fr, 3rem gap) for the resume intro and the artist statement; contact links indent 25%; credits and resume downloads are ruled lists with 1px Rule Line tops and 1.5rem row padding (credits two columns, downloads a two-column grid).
- **Breakpoints:** 960px tightens the hero and spread; 768px stacks current projects and off-stage items; 640px is the phone layout: name inline, headshot at 73% width, the spread becomes one column of prints at 72 to 100% width alternating left and right, credit rows stack.
- Interactive targets are at least 44px tall. Horizontal overflow from rotated prints is contained by the layout, never by page scroll.

### Named Rules

**The Words Stay Level Rule.** Paper tilts; text never does. Captions sit below their print and stay fixed while the print lifts and tilts. Slips rotate their background layer, not their words. Headings never rotate.

## Elevation & Depth

Depth is physical. Printed objects (photo prints, the headshot, tickets, slips, sheets) lift off the page with soft, warm, two-layer shadows tinted from Program Ink; the page, text, rules and captions are flat. Layering comes from stacking paper: a Callboard Card backing under a print, a second print overlapping the headshot, a stub tucked under a show photo. Hover and focus lift a loose print toward the viewer (9px up, straightened to 0deg, 2.5% larger, deeper shadow). Fastened prints stay anchored: tape and pins hold the top edge while the paper flexes; corner mounts hold their photograph flat.

### Shadow Vocabulary

- **Print** (`box-shadow: 0 2px 4px rgb(43 37 32 / .1), 0 12px 24px -12px rgb(43 37 32 / .32)`): photo prints and the current-project photo at rest.
- **Print lifted** (`box-shadow: 0 4px 8px rgb(43 37 32 / .08), 0 25px 35px -14px rgb(43 37 32 / .32)`): a print under fine-pointer hover or keyboard focus.
- **Headshot** (`box-shadow: 0 3px 5px rgb(43 37 32 / .08), 0 18px 35px -16px rgb(43 37 32 / .28)`): the homepage portrait card.
- **Sheet** (`box-shadow: 0 5px 15px rgba(43, 37, 32, 0.06)`): the resume sheet, video mats and off-stage slips.
- **Slip** (`box-shadow: 0 2px 6px rgba(43, 37, 32, 0.06)`): nav slips when shown.
- **Ticket** (`filter: drop-shadow(0 1px 2px rgb(43 37 32 / .1)) drop-shadow(0 6px 5px rgb(43 37 32 / .06))`): the current-project stub. The brand ticket uses `drop-shadow(0 2px 2px rgb(43 37 32 / .1))`. Tickets are clipped by their tear, so the shadow goes on an unclipped wrapper as a filter.

### Named Rules

**The Prints Cast, Words Don't Rule.** Only paper objects get shadows. Text, captions, rules and icons never do, and neither will the ballpoint doodles: ink drawn on a print has no shadow of its own.

## Shapes

Paper is cut square. Prints, sheets, slips and tickets have no corner radius; their silhouettes come from rotation, mats and cut edges instead. The ticket's right edge is a jagged hand-torn line: the header ticket uses the shared `--ticket-tear` clip-path, and the stub repeats the same tear points in its own polygon, adding a V die-cut at the top and bottom of its perforation. Backing papers are irregular quadrilaterals (`polygon(3% 4%, 96% 0, 100% 94%, 0 100%)` and kin), never rectangles. Photo mats are 0.4 to 0.5rem, some with a deeper 1 to 1.1rem bottom edge like a print border.

Curves in the interface are functional: the footer icon hover tile (6px), the pill-shaped build badge, and the small round dot on the ticket's "Livestream available" line. The gallery's round thumbtack cap follows its physical shape; paper still has square corners.

### Named Rules

**The Square Paper Rule.** If it is paper, it has square corners. Rounding belongs only to small UI conveniences in the footer.

## Components

### Navigation

Character: a torn ticket and a row of paper slips.

- **Brand:** a small brand ticket (Ticket Stock, Rule Line border, Marquee Rust left stripe, torn right edge) reading "Orch · Row F" in tiny mono over "Rutis" in Cooper Black, rotated -3deg; beside it "Finn Rutis" in Cooper Bold. On the homepage the text name is visually hidden because the big name is already there. Hover or keyboard focus straightens the ticket to -1deg and lifts it 2px.
- **Links:** Sabon 600 in Program Ink, 44px tall. A Callboard Card slip (Rule Line border, slip shadow) sits behind each link, invisible at rest; on hover, keyboard focus or as the current page it appears at -2deg or 1.5deg (alternating) and the label turns Deep Marquee Rust.
- **Mobile (under 640px):** the seat line and text name hide, the ticket shrinks, links drop to 0.875rem with tight padding, and everything still fits on one or two rows.

### Text Links

Character: plain, underlined, with one shared arrow.

- Marquee Rust, 1px underline at 0.2em offset; hover turns Deep Marquee Rust with a 2px underline. Color transitions in 150ms.
- Calls to action ("Watch me perform", "Theatre credits") are Sabon 600, 44px tall, with the single arrow glyph from `Arrow.svelte` (out, down or back) that nudges 2px up and right on hover.
- **Hero links:** the reel link leads on its own paper slip at 1.1875rem: a Callboard Card layer with a Rule Line border and slip shadow, rotated 1.5deg behind level text, which settles to 0.45deg on hover or focus. Resume, about and contact follow on one line at 0.9375rem, separated by Faded Ink middle dots and without arrows, like the footer meta. When the bio column gets narrow the line tightens, then drops the dots and wraps on plain spacing rather than stranding a dot at a line end.
- Download links pair the label with a mono file label, "(PDF)". The primary resume download is 1.25rem.
- **Buttons and inputs:** none exist. Every action on the site is a link; keep it that way unless a real form is needed.

### Photo Print

Character: a real print with a mat, resting at an angle.

- Playbill Paper mat (0.4 to 0.5rem), no radius, print shadow, resting angle between -4deg and 4deg that alternates between neighbors.
- Fine pointer only: loose prints follow the cursor within ±5px / ±4px and tilt up to ±1.5deg / ±2deg; hover or focus lifts and straightens them. Touch gets the same composition without tilt.
- Gallery prints land once as they enter view: one corner leads, the paper flattens, and a soft shadow fades as it meets the board. Neighboring prints enter from different angles. The gesture is smaller on phones and touch devices.
- The caption sits below the print and never moves: a Deep Marquee Rust mono index ("01"), the show title in Cooper Bold, the role in small mono Faded Ink, and Finn's own blurb in body text. Images keep their full proportions; no cutouts, no background removal.

### Photo Fastenings

Character: practical ways of putting a print on the callboard, used selectively.

- The wide opening print and small composer print have translucent masking tape across the top edge, with torn ends and one faint crease. The tape stays fixed while the photo flexes up to 7deg from its grip on hover or keyboard focus, with a small additional pointer response.
- The tall Seussical print hangs from a rust-colored grip pushpin based on a real photograph, edited to face the viewer as if fully pressed into the paper. The near-axis view shows a thin circular cap covering most of the straight grip, with a small base crescent at the lower right and no visible needle. The canvas is 20px wide. The base's contact center meets the photo's pivot; the photo turns up to 2deg around that point while its bottom edge flexes toward the hand. The pin stays in place. The source photograph, edit prompts, and provenance are recorded in `docs/portfolio-media.md`.
- The tall-left print sits on heavier Callboard Card stock, held flat by two folded paper corners at opposite ends. Both mounts remain aligned with the photograph, including during interaction.
- The other two prints remain loose. Every fastening shares its print's resting angle and scroll arrival, while captions stay level. Fastenings are decorative, never cover a face, never intercept a click, and disappear in forced colors. Reduced motion keeps the physical details and removes their movement.

### Headshot

Character: a printed headshot with its own name strip.

- The portrait sits in a Playbill Paper card with a bottom strip: "Finn Rutis" in Cooper Black and "they / them" in small mono Faded Ink, left-aligned on one line. The strip moves with the photo as one object.
- A Callboard Card quadrilateral backing sits fixed behind it, rotated -5deg, with an inner Rule Line frame. A second print (the Seussical photo) overlaps the lower right at -9deg and links to the photo spread. It is taped at its top edge: the tape stays fixed to the headshot, and the print pivots at the tape's grip, swinging when a pointer arrives or the link receives keyboard focus, and hinging its bottom edge 10deg toward the hand. The headshot, tape and small print share one pointer response, so the tape stays attached. The small print has no separate cursor-follow tilt.

### Ticket Stub (signature)

Character: a real landscape theatre ticket you could tear off.

- Ticket Stock, Rule Line border, torn right edge, max 19rem wide, resting at 2deg (-1.5deg on even shows and on phones).
- A printed stub end on the left: solid Deep Marquee Rust running to the paper's edge, with "Admit one" set vertically in Ticket Stock mono. Its perforation shows as Ticket Stock dashes along the rust edge, and a V die-cut notches the ticket top and bottom where the stub end meets the body. No colored side rail. The body holds the opening date in Cooper Black, the weekday and year in Deep Marquee Rust mono, the run ("One night only", or "Through" plus the closing date) in Faded Ink mono, and an optional "Livestream available" line with a filled dot.
- With a booking URL, the whole stub is one link and gets a Stub Blush "Get tickets" band behind a dashed perforation. Hover or focus inverts the band to Deep Marquee Rust with Ticket Stock text and prints the date in Deep Marquee Rust; the border stays Rule Line. With a fine pointer and motion allowed, the stub also lifts 5px toward the hand, settles to a quarter of its resting angle and casts a deeper ticket shadow. The rust "Admit one" end flexes 28deg around its perforated right seam on fine-pointer hover or keyboard focus, while the link target stays whole. Reduced motion keeps the ink change and removes the flex; forced colors also keeps the strip flat. Without a URL the stub is not interactive.
- Beside it, the current-project notice: a plain Deep Marquee Rust mono status line with no marker (the words say whether it is in rehearsal or playing), the show title in Cooper Bold, then a Faded Ink dashed perforation and the mono-labelled credits (Role, Venue, Directed by) below it, so the credits read as the notice's tear-off. A role of "Self" is omitted.

### Paper Sheet and Slip

Character: heavier backing stock holding something.

- Callboard Card, 1px Rule Line border, sheet shadow, square corners. The resume preview sits on one (1rem padding, US Letter aspect), videos on another (0.75rem padding, 0.35rem on phones).
- Off-stage notes without a photo become slips: the card layer rotates half the item's angle behind level text.
- The homepage reel link and the nav links use the same slip, smaller: slip shadow, Rule Line border, only the backing rotates.

### Footer

Character: the blog's footer, ported.

- A centered row of 44px icon links (1.7 stroke outline icons, Faded Ink; hover shows a Callboard Card tile with 6px radius and Marquee Rust icon). Their focus ring is the one exception to the site ring: 2px Marquee Rust drawn inside the tile (-2px offset), so neighbors don't overlap.
- Below it, small-caps meta in Faded Ink: copyright, the Cooper license link, and a pill build badge with the commit SHA in mono that lifts 1px and borders in Marquee Rust on hover.

### Ballpoint Doodles (planned, not yet built)

Character: notes a friend scribbled on your playbill.

Hand-drawn blue ballpoint line art, scanned and rendered as CSS masks in one ink token (`--doodle-ink`, starting value #24409b, to be matched to the real pen). Doodles annotate something already on the page (circle the ticket date, underline "Rutis", a stick figure bowing on the footer line), never tile as a pattern. Two or three in view on desktop, one or two on a phone; never on the header or nav, never over a face or text, never under a link, decorative and hidden from assistive tech and forced colors. Boil animation steps through three hand-drawn frames at about 8fps and freezes under reduced motion. `docs/doodles.md` is the authority for drawing list, processing, placement and checks; add the token to the frontmatter when it lands in `site.css`.

### Motion

- **Focal moment:** the homepage portrait is assembled once on first entering view. Its backing seats over 440ms, the headshot and taped print settle together over 620ms with a 60ms offset, and the small print catches at its tape over 640ms with a 140ms offset. The complete gesture ends within 780ms. A contracting shadow gives the headshot weight; name, bio and links are readable throughout. The resting composition is the default, including without JavaScript.
- **Tape:** pointer entry or keyboard focus nudges the small print through a damped 920ms swing, at most 5deg either way. Its pivot stays at the tape. Repeated entry does not stack swings, and touch follows the link directly.
- **Feedback:** paper slips settle in 220ms, the ticket end flexes in 280ms, and bounded photo follow uses 450 to 500ms. These are responses to hover or focus, never idle loops. The shared portrait assembly keeps both photographs and the tape together.
- **Gallery:** each photo lands once after entering the bottom 18% of the viewport (capped at 160px), over 740ms (580ms on phones and coarse pointers). Its resting angle determines which corner leads. A brief perspective tilt flattens into the board while a prepainted contact shadow fades. Only the photo assembly moves; captions, headings and body copy stay level. Supporting pages remain still, and scrolling stays native with no parallax or delayed content.
- **Lifecycle:** reduced motion cancels active Web Animations and pointer offsets immediately, while color and focus states remain clear. Keyboard focus or a pointer press settles an arriving print immediately. Prints scrolled past stop animating and do not replay on return. Hidden tabs and navigation clear animations and pending frames. Pointer work is coalesced to one animation frame, with no idle render loop or added dependency.

## Do's and Don'ts

### Do:

- **Do** keep Marquee Rust (#b54a00) as the only interface hue, on links, the surname, the tickets (brand stripe, stub end) and focus.
- **Do** give every print a resting angle between -4deg and 4deg, varied between neighbors; the overlapping hero print at -9deg is the one exception.
- **Do** keep captions, headings and body copy level and outside the print, readable without hover or JavaScript.
- **Do** reuse the shared ticket tear and Ticket Stock for anything that is a ticket, with its shadow on an unclipped wrapper.
- **Do** use the shadow vocabulary above for paper objects, and the lifted print shadow only on hover or focus.
- **Do** keep interactive targets at least 44px tall and the focus ring a 3px Marquee Rust outline at 5px offset.
- **Do** hide decorative paper layers in forced colors and give prints, tickets and sheets a 1px CanvasText border there.
- **Do** add scrapbook texture as real hand-drawn ink, placed and limited as `docs/doodles.md` describes.

### Don't:

- **Don't** build the actor template site: a centered headshot hero, a stock nav and a slideshow.
- **Don't** borrow the tech portfolio look: dark mode, terminal motifs, gradients or developer-style cards. PragmataPro is a label voice, not a terminal.
- **Don't** go glossy showbiz: black and gold, glitter, marquee bulbs or rendered spotlight glow.
- **Don't** fake the hand: no SVG, CSS or AI-generated doodle stand-ins. If a drawing doesn't exist yet, its slot stays empty.
- **Don't** place text over a face, crop a photo into a cutout, or remove its background.
- **Don't** round the corners of paper, or add a second accent hue or a dark theme.
- **Don't** set body copy or labels in Cooper, or headings in PragmataPro.
- **Don't** put a shadow on text, captions, icons or ink.
