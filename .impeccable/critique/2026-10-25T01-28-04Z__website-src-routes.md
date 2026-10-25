---
target: website/src/routes (whole site)
total_score: 24
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 1
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes"
timestamp: 2026-10-25T01-28-04Z
slug: website-src-routes
closed: true
---
Method: dual-agent (A: design-review sub-agent · B: detector sub-agent). Target: the whole site (`website/src/routes`), judged as Experience mode; `/resumes/` and the `/resume/` download block judged as Operate.

### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Current page shows as a lifted nav slip (`aria-current`); Play swaps in the player and moves focus. Gallery prints give no sign, and none on touch, that they open show pages. |
| 2 | Match System / Real World | 3 | Tickets, "Admit one" and credit rows speak theatre. "Venue" labels producing companies ("CAP21 / Molloy Univ."). |
| 3 | User Control and Freedom | 3 | Nav on every page, back link and pager on show pages, 404 offers reel and PDF. Prints on show pages and `/about/` open a bare JPEG with no site around it. |
| 4 | Consistency and Standards | 3 | One visual system throughout. Labels drift: "Self" only under gallery prints, "Director:" vs "Directed by", ↗ on internal links. |
| 5 | Error Prevention | 3 | No forms. Card drag is told apart from a contact tap; the about build gate keeps placeholders out of production. |
| 6 | Recognition Rather Than Recall | 3 | Nav and CTAs are text. The footer is six icon-only links (a key, a pen). |
| 7 | Flexibility and Efficiency | n/a | Experience surface; no accelerators expected, keyboard works. |
| 8 | Aesthetic and Minimalist Design | 3 | Disciplined palette and paper vocabulary. The homepage runs three display-scale headings back to back (name, "Current project.", "On stage."). |
| 9 | Error Recovery | 3 | 404 routes to reel, PDF and home; a failed poster says "Preview unavailable. Select to play." |
| 10 | Help and Documentation | n/a | Portfolio; the card's "Drag to turn · Click to flip" is the only help needed. |
| **Total** | | **24/32 (75%)** | **Good** |

### Design Specificity Verdict

**LLM assessment:** Authored, not interchangeable. The callboard works through objects with jobs: the "Orch · Row F" brand ticket, a current-project stub that exists only from first rehearsal to closing night, the "Start here" ticket on the reel, cover prints with computed photo/video counts, tape/pin/corner fastenings, and the real business card on Contact. One rust hue, square paper, warm shadows and level text hold on every page, and it avoids all three rejected looks. Weakest: `/resumes/` and the 404 (a generic h1-plus-list shell), and the ported blog footer, a dev-blog pattern that closes every page. Missed: reel views are the metric but the homepage is all stills, and nothing shows which ensemble member is Finn.

**Deterministic scan:** CLI on `website/src/routes` and `website/src/lib/components`: 0 findings, text-pattern rules only (element rules need a rendered page). In-page detector: 25 findings across 6 pages.
- 16 false positives, all deliberate in DESIGN.md: `cream-palette` x6 (Playbill Paper), `organic-clip-path` x5 (torn ticket edge and tape, site.css:138/195/275), `repeating-stripes-gradient` x4 (ticket perforations), `kicker-above-heading` x1 (the specified "Film" label).
- 9 real, all minor: `straggler` x2 (orphaned last word in the bio and the artist statement), `undersized-ui-text` x4 (`.credit-reel-count` at 10px, site.css:334), `bounce-easing` x3 (`.photo-mat` overshoots at `cubic-bezier(.2,.8,.2,1.15)`, site.css:258).
- The detector caught the stragglers and the overshoot the review missed. The review caught the worst bug (P1), which the detector and the 375px overflow check both passed: `overflow-wrap: anywhere` turns overflow into letter-stacking, so nothing scrolls.
- Otherwise clean: no contrast failures, no horizontal overflow at 375px, no missing alt, no unexpected console errors.

**Visual overlays:** injected on 6 pages; left visible in the Browser pane's "[Human] Finn Rutis" tab on `/` (straggler outline on the bio plus the page banner). Dev server stopped afterwards, so the tab is a static snapshot.

### Overall Impression

A coherent, specific world that handles its highest-stakes moment well: "Watch me perform" is the first CTA, and "Start here" plays in place in one click. What fails: the two-column layouts break at mid widths and large text, and the pull toward reel and PDF fades past the first viewport (show pages with video sit behind uncued prints, the reel stops orienting after clip one, the PDF sits at the bottom of the reel, `/about/` dead-ends). Biggest opportunity: carry the "Start here" clarity through the rest of the site.

### What's Working

1. **One physical logic, held with restraint.** One tear for every ticket, one shadow family for every paper object, words never tilt, and supporting pages calm down as the brief asks.
2. **The watch moment.** "Start here" removes the choice; Play swaps poster for player in place and moves focus into it (Recording.svelte:23-30); modifier-click still opens a tab; a failed poster has a fallback.
3. **Data drives the UI.** The ticket appears only during a run, credit counts are computed, show pages exist only where photos exist, and focus was visible on every stop tabbed.

### Priority Issues

**[P1] Two-column layouts crush text into letter stacks at 640-700px and under large text**
- **What:** On `/resumes/` at 640px every document title column is 40px wide ("Arti/stic/Res/ume", "Res/ume/wit/h/hea/dsh/ot"). At 1280px with 200% root text, "Current project." on `/` breaks as "Curren / t / project / .". Both verified in the browser.
- **Why it matters:** `/resumes/` is where people take PDFs, a half-screen laptop window (about 683px) lands in the broken band, and PRODUCT.md sets 200% text reflow as the bar.
- **Cause:** `.download-group` keeps a `minmax(14rem, 1fr)` label column and `.download-library` an `auto` action column until the px breakpoint at site.css:487 (`max-width: 639px`); `.now-showing` reserves 19rem for the ticket (site.css:222); `overflow-wrap: anywhere` on those headings (site.css:237, :424, :429) lets a title shrink to one letter.
- **Fix:** Em breakpoints or container queries so text size triggers stacking; let `.library-actions` drop under the title when narrow; stack notice above ticket when the copy column falls under about 20ch; `overflow-wrap: break-word` on headings.
- **Suggested command:** /impeccable adapt

**[P2] The reel stops orienting after the first clip**
- **What:** "I Love to Sing-a & Love Me, Love Me Not" and "No One Has to Know" have no context line (media.js:196-197 carry no `show`). The film shows only "Film / All Over Everywhere", though its credit (Stoner 2, Alcove Productions, dir. Katie O'Grady) is in `metadata/film.toml`. No durations. The resume download sits at y about 4417 of 4865. The "How Lucky You Are" poster 404s at `hq720` and falls back to a 480x360 still stretched to about 900px.
- **Why it matters:** A casting director can't budget time or tell which clips matter.
- **Fix:** Caption the film from `film.toml` (add it to `server.fs.allow` and the `packages/website.nix` filter; it is not one of the three shared inputs). Add `duration` to media.js and print it in the credit line. Ask Finn what the two showless clips are. Put a compact "Download resume (PDF)" beside the h1 (performance-reel/+page.svelte:13). Self-host a poster for "How Lucky You Are".
- **Suggested command:** /impeccable clarify

**[P2] Show pages, where the videos live, are hidden; gallery captions print "Self"**
- **What:** Homepage prints link to show pages with no visible cue (no underline or count; nothing on touch). Revue captions read "Self" because `attachPhotoNotes` passes `show.character` straight through (website/lib/content.mjs:61), while the current-project notice drops "Self" by design. On `/shows/seussical/` the first video starts at y about 1589 at 1440x900, after all the prints.
- **Why it matters:** Reel views are the metric, and nobody is told those pages hold video.
- **Fix:** Filter "Self" in `attachPhotoNotes`. Give gallery captions an underlined title and the credit rows' "3 photos · 2 videos" count at 0.6875rem or larger (the detector already flags 10px). Put a show's first recording directly under its notice.
- **Suggested command:** /impeccable clarify, then /impeccable layout

**[P2] Contact details exist only as raster lettering at phone size**
- **What:** At 375px the card is 283px wide, so the printed email and handle are about 10-11px and can't grow with text settings. The only live text is the 11px Faded Ink mono address (BusinessCard.svelte:508, :552); the Instagram handle has none. Tapping the blank card flips it and hides both links (:495). The focus ring wraps the larger stage, not the card, and clips into the h1.
- **Why it matters:** This page's job is two strings of text, and Principle 5 requires large-text support.
- **Fix:** Set address and handle under the card at body size in Program Ink, still with no action row; fit the focus ring to the card; record the changed card rule in DESIGN.md.
- **Suggested command:** /impeccable adapt

**[P3] `/about/` dead-ends, and "Theatre credits" lands on the preview**
- **What:** `/about/` has no Performance Next Steps slip and ends on the footer. The homepage "Theatre credits" link (+page.svelte:70) goes to `/resume/` without an anchor; credits start about 1355px down, below the preview sheet.
- **Why it matters:** Principle 2: every page keeps a short path to watching Finn and taking the PDF.
- **Fix:** Add the slip to `/about/`; point the link at the credits heading.
- **Suggested command:** /impeccable layout

### Persona Red Flags

**Jordan (first-timer):** Footer "PGP key" (key) and "Blog" (pen) have no visible label and no tooltip on touch. The ↗ on "Watch me perform" and "All resumes" reads as leaving the site. Nothing says a gallery print opens a page with videos, and on a show page a print opens a bare JPEG. Tapping the blank contact card hides the contacts until it's flipped back.

**Sam (screen reader, keyboard, 200% zoom):** `/resumes/` titles stack one letter per line; "Current project." splits mid-word. Contact lettering is raster on phones and can't scale. Footer meta links measure 112x22 and 184x27, under the site's own 44px rule. Alt text on ensemble prints never says which performer is Finn (only Finn can say). Works: skip link, rust focus ring on every stop, card side announced in a live region, fastenings aria-hidden.

**Casey (phone, one-handed):** Nav only at the top; on the 4926px homepage the next direct PDF link is at y about 4476. No `srcset` (PhotoPrint.svelte:25): prints ship 1920px masters (joseph-ensemble.jpg is 668KB) into about 335px slots. Works: mid-screen hero CTAs, 44px nav targets, 94x50 card contact targets.

**Morgan (casting associate, 90 seconds between auditions, browser split beside the breakdown at about 683px):** Wins: name, face and "Watch me perform" in the first viewport; "Start here" plays in one click. Fails: `/resumes/` is broken at exactly this width; no voice part or height anywhere in the HTML; can't find Finn in the Joseph or Song & Dance ensembles; after the 1:16 start clip no durations, and the film never says which role is Finn's; the PDF is at the bottom of the reel.

### Minor Observations

- **Stragglers** (detector): "experience" alone on the bio's last line, "havoc." on the statement's. `text-wrap: pretty` on body paragraphs fixes it in CSS (site.css:32 balances headings only); the copy stays Finn's.
- **Overshoot** (detector): `.photo-mat` lifts on `cubic-bezier(.2,.8,.2,1.15)` (site.css:258), the only overshooting curve; every other paper transition settles at 1. Keep only if the spring is intended, and record it in DESIGN.md.
- **10px counts** (detector): `.credit-reel-count` is 0.625rem (site.css:334) and serves as the credit links' `aria-describedby`. DESIGN.md sanctions the size, but it's functional text.
- **"Venue"** holds producing companies (CurrentProjects.svelte:56, shows/[id]/+page.svelte:29). "Company" matches the data and resume convention; a renameable structural label.
- **↗ on internal CTAs** reads as external. It is the documented Arrow.svelte default: a convention call, not a bug.
- **Latent contrast:** Marquee Rust on Callboard Card is 4.43:1, under AA. An off-stage slip with a `link` would render exactly that (about/+page.svelte:49); none has one today.
- **Duplicate captions:** Composer Project Revue appears twice in the spread with identical captions (03 and 07).
- **Bio capitalization:** "City Based" (PageHead.svelte:8) vs "City based" (+page.svelte:59). Finn's words, Finn's call.
- **Card flash:** `.webgl .card-flat { opacity: 0 }` (BusinessCard.svelte:535) hides the flat card before the first WebGL frame; a throttled pane showed an empty stage. Unverified on devices. (/impeccable harden)
- **404** is the least crafted page; a pinned notice would bring it onto the callboard.
- **DESIGN.md drift:** the hero now has two equal slips, not the lead slip plus dotted line at DESIGN.md:278; and the "fonts fail on localhost" note is stale, since `website/lib/local-fonts.mjs` serves Sabon Next and PragmataPro in dev. (/impeccable document)

### Questions to Consider

- If reel views are the metric, why is the homepage all stills? What if the "Start here" clip sat under the hero as a playable flyer?
- Could the ballpoint doodle layer do real work: an arrow beside Finn (never over a face) in each ensemble print?
- Should "Tenor · 6'" (REFERENCE.md:22-23) appear as a mono line on the headshot strip or `/resume/`? It needs `metadata/metadata.toml` as a new shared input.
- Does a one-night cabaret need playbill-scale "Current project.", or should it sit at slip scale so "On stage." keeps the climax?
