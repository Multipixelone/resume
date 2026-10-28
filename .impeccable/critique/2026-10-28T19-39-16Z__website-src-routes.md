---
target: critique (whole site, website/src/routes)
total_score: 25
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 0
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes"
timestamp: 2026-10-28T19-39-16Z
slug: website-src-routes
---
Method: dual-agent (A: design-review sub-agent · B: detector sub-agent)

Target: the whole site (`website/src/routes`) on the Vite dev server, desktop 1440 and phone 375/390. Cooper, Sabon Next and PragmataPro all loaded (dev-local copies). Dev-only artifacts (404 PDFs, photo masters instead of renditions, ungated `/about/`) were excluded.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Ticket status is computed live and card state is announced, but the nav highlights nothing on `/shows/*` or `/resumes/` (`+layout.svelte:35`). |
| 2 | Match System / Real World | 3 | Fluent backstage language (Admit one, Directed by, Stage door). Breaks web convention: ↗ on internal links, ↙ for Back (`Arrow.svelte:7`). |
| 3 | User Control and Freedom | 4 | Show pages return to Home or Theatre credits with scroll restored; video is user-played; card flips and tilt are reversible. |
| 4 | Consistency and Standards | 3 | The two "Watch me perform" links on `/` go to different places (`+page.svelte:23` vs `PerformanceNextSteps.svelte:20`); "PDF" vs "(PDF)"; one download lacks its arrow. |
| 5 | Error Prevention | 3 | Little can go wrong. `download` forces a save prompt on phones instead of opening the PDF. |
| 6 | Recognition Rather Than Recall | 3 | Cover prints and media counts preview every link, but nothing visible says which performer in an ensemble photo is Finn. |
| 7 | Flexibility and Efficiency | n/a | A portfolio has no repeated expert workflow; speed to the outcomes is covered under personas. |
| 8 | Aesthetic and Minimalist Design | 3 | One hue, one paper vocabulary. Noise: a ~180px dead band inside the Start-here flyer, duplicate "Composer Project Revue" captions, "Use device tilt" outranking the contact details on phones. |
| 9 | Error Recovery | 3 | The 404 offers reel, PDF and Home; card and poster failures degrade with plain messages. It drops the callboard voice. |
| 10 | Help and Documentation | n/a | Nothing to document; the one interaction that needs instructions (the card) carries them inline. |
| **Total** | | **25/32** | **Good (78%)** |

Cognitive load is moderate: 2 of 8 checks fail (chunking on the reel's six equal sheets and the 12-row credit list; more than 4 options at the reel's ~15 actions and the 8-link footer). Peak-end is good: the homepage closes on "Reel & resume", then "Stage door." The valleys are the photo travel landing on unlabelled galleries, the end of `/about/`, Contact on a phone, and the 404.

## Design Specificity Verdict

**LLM assessment:** Authored, not templated. The torn "Orch · Row F" brand ticket, the die-cut stub whose status line is computed from real show dates, tape, a pushpin cut from a photograph, folded photo corners, credits that open show pages with cover prints and "3 photos · 2 videos" counts, and Finn's actual business card on Contact: no other performer could reuse this unchanged. The specificity lives in the object vocabulary and the data wiring, not the IA (hero, clip, news, gallery, call to action is the standard actor-site order, and that predictability is right for casting directors). It thins out where paper only wraps a list: the reel (six identical sheets), All resumes and the 404 could belong to anyone. The frame is finished down to the crease in the tape while every slot for Finn's own notes is empty (21 of 21 blurbs in `media.js`), so show pages read as unlabelled galleries.

**Deterministic scan:** `impeccable detect --json website/src` scanned 50 files and found 2 issues, both `broken-image` (`CoverPrint.svelte:11`, `about/+page.svelte:41`). Both are false positives: `responsive()` spreads `srcset`/`src` into the tag where the regex can't see it, and both images load. In the page (`/`, `/resume/`, `/performance-reel/`, `/shows/seussical/`, `/booking/`, at 1280 and 375):
- False positives, all documented in DESIGN.md: `cream-palette` (Playbill Paper), `organic-clip-path` (tape ends, the stub's tear), `repeating-stripes-gradient` (1px ticket perforations), `kicker-above-heading` and `text-occlusion` on the "Start here" ticket (a paper object whose tuck under the sheet is intended; hit-testing found its words unobstructed). The "Film" label is the one literal eyebrow, and DESIGN.md asks for it.
- Real, phones only: `undersized-ui-text` on the 10px "Seussical" caption on the hero print (`site.css:649`), and `straggler` in the `/resume/` training notes, because `text-wrap: pretty` covers `p` but not `dd` (`site.css:54`).
- Agreement: both assessments independently found a type floor that dips under 11px (detector: the hero caption; review: the 8px seat line and the ~10px card contacts). The detector found nothing structural, which matches the review: the build is clean, and the problems are in what the pages say and where the outcomes sit, which no scanner sees.

**Visual overlays:** Injection succeeded on all five pages. The [Human] tab in the browser pane holds `/` with 2 overlays and the page-level banner, injected at 1280x800. The dev server is now stopped, so that tab is a snapshot.

## Overall Impression

A finished, authored site, with unusually thorough engineering for no-JS, reduced motion, forced colors and 200% text. What falls short is the last mile to the two outcomes. The frame is built to the crease of the tape, but the things that make a casting director act (the PDF right after the clip, a reason to press play a second time, which person in the photo is Finn) are thin or a long scroll away. Biggest opportunity: put the resume beside the clip, and make every poster and photo find Finn.

## What's Working

- **The metaphor carries information.** The stub is a live status with a ticket link and a livestream line; credit rows and captions show a cover print and media counts before you click. The callboard is navigation that tells a casting director what is behind each link.
- **The path to performance is fast.** "Watch me perform ↓" lands on the 1:15 Start-here clip in the first scroll and hands keyboard focus to Play. Home, Resume, the reel, every show page and even the 404 close on both outcomes.
- **It holds up under stress.** No overflow at 320px or at 200% text; em breakpoints plus container queries; a flat card and native links without JavaScript; a visible focus ring on all 31 homepage tab stops, including the card links that follow its 3D projection.

## Priority Issues

**[P2] 1. The resume isn't there at the moment of highest intent**
- **Why it matters:** PRODUCT.md principle 2 promises a short path to the PDF from every page. A casting director decides to take the resume right after the clip, and the flyer (`Recording.svelte:104-108`) offers only "More performances" and "Watch on YouTube", which repeats the poster's own link (`:79`). From there the PDF is two clicks back up, or ~2,800px down on desktop (~3,900px on a phone). `/about/`, the most invested visitor's page, runs straight into a footer that lists Resume but not Reel (`footer.ts:14-21`), and the header doesn't stick.
- **Fix:** Put "Download resume (PDF) ↓" in the flyer's link group in place of "Watch on YouTube" (the poster and player still reach YouTube). Close `/about/` with `<PerformanceNextSteps>`. Add Reel to `footerLinks` beside Resume (needs a glyph in `Icon.svelte`).
- **Suggested command:** `/impeccable layout`

**[P2] 2. The reel is an archive, not an edit**
- **Why it matters:** Reel views are the outcome, and a casting director decides from the poster whether to press play a second time. `/performance-reel/` is ~5,000px of six identical sheets in one column. Two clips are captioned by duration alone ("2:49", "1:34"). Both Seussical posters are dim wide shots with Finn a small figure, and the film's poster shows two other actors under a "film SHORTAGE" watermark, 11:27 long, with no cue to Finn's scene.
- **Fix:** Keep the start clip full width and set the rest two-up on desktop under data-derived group labels (renameable). Use the existing `poster` field (`media.js:199`) for frames where Finn's face reads; picking the frames is Finn's call. If Finn supplies a start time for the film, pass `start=` and show it in the credit line.
- **Suggested command:** `/impeccable distill`

**[P2] 3. Show pages never say which one is Finn**
- **Why it matters:** Casting directors judge a performer by finding them in the frame, and the site's best transition (a print travelling into its show page) lands on an anticlimax. All 21 blurbs are empty, so show-page prints carry no caption (`ReelPrint.svelte:30-40`). `/shows/joseph/` is three ensemble shots with nothing visible locating Finn; the alt text does locate Finn, so screen-reader users get more than sighted ones. The homepage's largest print (Song & Dance Revue, "1 photo", not on the resume) opens a page holding that same single photo.
- **Fix** (no drafted copy): list the empty blurb slots for Finn, ensemble frames first. Until then, order each show's photos so the frame where Finn is the clear subject leads (`media.js` order controls it). Link a print to its show page only when the page holds more than that print; otherwise open the full photo (the existing fallback in `PhotoPrint.svelte:15`).
- **Suggested command:** `/impeccable harden`

**[P2] 4. On phones, Contact's contact details are its smallest text**
- **Why it matters:** Email and Instagram are lettering inside the card texture, sized to the viewport (`BusinessCard.svelte:538`): about 10px on a 375px phone, and still about 9px when the browser's text size is doubled. The caption repeats only the email, in 11px mono; @finnrutis appears nowhere else as visible text. Meanwhile "Use device tilt" is 16px rust with an icon, the loudest thing on the page. DESIGN.md deliberately omits a repeated contact row, but text baked into WebGL can't honour the visitor's text size, which breaks PRODUCT.md principle 5. The intent should yield here.
- **Fix:** Below 40em and whenever text is enlarged, show the email and @finnrutis as live body-size links in the caption, demote "Use device tilt" to a mono label after them, and let the card span the full content width (drop the 8.825% insets).
- **Suggested command:** `/impeccable adapt`

**[P3] 5. Link arrows and labels carry no meaning**
- **Why it matters:** ↗ marks internal links (See my resume, Theatre credits, All resumes) and links that leave the site (YouTube, tickets, blog) alike, so a first-timer hesitates on the main call to action. Back is ↗ turned 180 degrees (↙). The two homepage "Watch me perform" links go to different places. Downloads say "PDF" on All resumes and "(PDF)" elsewhere, and "Resume with headshot" on `/resume/` has no ↓ (`resume/+page.svelte:28`). The filename "Finn Rutis Artistic Resume.pdf" is hard-coded in four places while its title lives in `variants.toml`.
- **Fix:** → for internal links, ↗ only for external, ← for Back. Give the closing slip's reel link its own label (for example "Full reel"). One download pattern everywhere: label, (PDF), ↓. Derive the filename from the variant title.
- **Suggested command:** `/impeccable polish`

## Persona Red Flags

**Dana, a casting associate with 90 seconds between auditions (desktop, from a submission link):** 0-5s name, face, two calls to action: pass. 5-15s "Watch me perform ↓", Play, the 1:15 clip: pass. At 75s they want the PDF, and the flyer has none: it's two clicks back up, or ~2,800px down past "Current project." and seven prints. Fails at the decisive moment. Opening the Joseph print instead gives three ensemble shots and no way to find Finn in time.

**Casey (390px, one hand):** the homepage is 5,846px tall and the header doesn't stick; after the clip the PDF is ~3,900px away. On Contact the email is ~10px and "Use device tilt" is the biggest control. Every PDF link triggers a save prompt instead of opening.

**Jordan (first-timer):** "See my resume ↗" wears the same arrow as "Get tickets ↗" and reads as leaving the site. The same document is "Artistic Resume" on All resumes and "resume" everywhere else. On a show page the back link is "↙ Home" and the nav highlights nothing. On Contact the only cue that the card is interactive is "Drag to turn · Tap to flip" in 11px mono.

**Sam (accessibility):** card lettering ignores text-size settings, and the Instagram handle exists only in the artwork and an sr-only span. At 200% text on a phone, `overflow-wrap: anywhere` breaks words mid-word ("Downloa/d resume", "Compo/ser"; `site.css:355`). The rest is strong: skip link, logical order, visible ring, keyboard flip with a live announcement, forced colors and reduced motion handled.

**Riley (stress tester):** homepage captions 03 and 07 are identical ("Composer Project Revue · 6 photos"). The biggest print leads to a one-photo page for a show that isn't on the resume. With JavaScript off, "Current project." and the livestream line vanish (documented, but it is the only time-sensitive content).

## Minor Observations

- The Start-here flyer has a ~180px empty band between its credit line and links at desktop (the `auto 1fr auto` rows, `Recording.svelte:180-194`).
- Type floor: the 8px seat line (`site.css:76`, decorative) and the 10px hero-print caption on phones (`site.css:649`, labels a link).
- `/resume/` training notes strand single words on phones; extend `text-wrap: pretty` to `dd` (`site.css:54`).
- Odd-count show pages (Seussical, Joseph) leave a half-empty last row (`site.css:484-488`).
- "Current project." is set 2.2x larger than the show it names (88px vs 40px).
- The 404 is the one page where the callboard voice disappears.
- Downloads could say "(PDF, 1 page)" from `expected_pages` in `variants.toml`, a small reassurance on phones.
- DESIGN.md has drifted: its Footer section describes a centered icon-only row with hover tiles, but the build ships a "Stage door." heading with labelled links; the Overview omits the Start-here flyer. Run `/impeccable document` after fixes.
- The detector's `organic-clip-path` point and DESIGN.md's "Don't fake the hand" pull against each other: doodles must be real scans while tape and tears are drawn in CSS. One sentence in DESIGN.md should say where that line sits.
- The page description says "New York City Based" while the bio says "based": Finn's copy, Finn's call.

## Questions to Consider

- The spread's largest slot goes to a revue billed as "Self" that isn't on the resume, while credited roles (Kiss Me Kate, Legally Blonde) close the spread. Is that the order a casting director should read?
- Is "Current project." worth playbill-scale type for a one-night cabaret, or is its real value the livestream line, a second way to watch Finn, which could sit beside the Start-here clip?
- What would the reel look like as an edit: three clips with posters that show Finn's face, everything else behind "More"?
- Should Contact be the card, or should the card be the ornament on a page whose email is set as large as its heading?

## Run Notes

Not checked: Safari and Firefox (WebGL, view transitions, the stub's vertical "Admit one"), real device tilt, actual screen-reader speech, and the production build (PDFs, renditions, `/about/` gating, fonts from `fonts.finnrut.is`, whose licensing is still open). The dev server and the detector's live server are stopped; no project files were edited.
