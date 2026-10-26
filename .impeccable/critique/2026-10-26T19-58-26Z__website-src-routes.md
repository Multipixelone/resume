---
target: whole portfolio site
total_score: 28
max_score: 36
na_heuristics: 10
p0_count: 0
p1_count: 0
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes"
timestamp: 2026-10-26T19-58-26Z
slug: website-src-routes
---
Method: dual-agent (A: design-review fork · B: detector fork)

## Critique: finnrut.is portfolio (`website/src/routes`)

### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Current-page slips and focus moving into the player are clear; `/resumes/` and `/shows/*` light no nav item |
| 2 | Match System / Real World | 3 | Callboard vocabulary is native; the bio says "performance artist" where every other surface says "musical theatre performer" |
| 3 | User Control and Freedom | 3 | Back restores scroll and reverses the photo handoff; the show page's back-styled link goes to `/resume/` even after arriving from `/` |
| 4 | Consistency and Standards | 3 | Cohesive system; "Director:" vs "Directed by", two "Watch me perform" links on `/` with different targets |
| 5 | Error Prevention | 3 | "(PDF)" labels and named downloads; "Preview" on `/resumes/` opens a bare PNG with no type label |
| 6 | Recognition Rather Than Recall | 4 | Labelled icons, prints say what they open ("3 photos · 2 videos"), "Start here" removes the first choice |
| 7 | Flexibility and Efficiency | 3 | Skip link and a PDF path from every page; the reel has no index to jump to a clip |
| 8 | Aesthetic and Minimalist Design | 3 | The paper world earns its pixels; the homepage middle stacks three display-scale headings and the start card has an empty band |
| 9 | Error Recovery | 3 | The 404 recovers to reel, PDF and home; the resume preview and video posters have fallbacks |
| 10 | Help and Documentation | n/a | No multi-step tasks; the one novel control (the card) carries its own hint |
| **Total** | | **28/36** | **Good (78%)** |

### Design Specificity Verdict

**LLM assessment:** Authored, not interchangeable. The callboard is built from Finn's own artifacts and real data: the "Orch · Row F" brand ticket, an "Admit one" stub driven by show dates, matted prints held by tape, a pushpin and photo corners, the Cooper playbill name, "On stage." / "Off stage." / "Stage door.", and a business card that turns in 3D. The new photo handoff from a homepage print into its show page works forward and back. Sameness lives on the supporting pages, which all reduce to big Cooper title plus content, and the reel, the site's destination, is the plainest of them: six identical sheets in one column.

**Deterministic scan:** `impeccable detect` on `website/src` (48 files) found 2 issues, both `broken-image` false positives at `website/src/lib/components/CoverPrint.svelte:11` and `website/src/routes/about/+page.svelte:41` (the same `responsive()` spread already ignored for `+page.svelte` and `PhotoPrint.svelte`; both masters load). The in-page overlay on 5 pages flagged `cream-palette` (every page), `organic-clip-path` (torn ticket and tape ends), `repeating-stripes-gradient` (ticket perforations) and `kicker-above-heading` twice ("Start here" on `/`, "Film" on the reel). Every one is a DESIGN.md commitment, so the brief wins. The one place the detector and the review meet is the homepage start card (issue 4). The detector caught nothing the review missed; the review's main issues (content, IA, wayfinding) are outside its reach.

**Visual overlays:** injection worked (no CSP). The [Human] tab in the in-app browser is left on `/` with the overlay; it shows only the brief-pinned patterns above.

### Overall Impression

A theatre maker's callboard, not an actor template, with a high craft floor. What lets it down is content and wayfinding, not decoration: the reel (half of the success metric) is the least informative page, and the facts a casting director filters on first sit inside a PDF. Cognitive load is low (2 of 8 checks fail, mildly: the 6-link footer and the unindexed reel). A cold casting director peaks on the first viewport, the Start-here clip and the live ticket stub, dips at the bio's category label and the thin clip context, and ends on the "Reel & resume" slip, so peak-end holds.

Biggest opportunity: give the reel a running order and real context per clip.

### What's Working

1. **Decoration that carries information.** The stub says "One night only · Livestream available · Get tickets" from real show data; prints say what their page holds. Nothing on the board is filler.
2. **Reel and resume are always one move away.** Hero slips, the closing slip on `/`, `/resume/`, every show page and the reel, the reel header's download, and a 404 that recovers to both.
3. **Accessibility craft holds up.** One 3px rust ring at 5px across 31 tab stops on `/`, 44px targets, no overflow at 200% text, reduced motion handled, the photo transition degrades cleanly, and Cooper, Sabon Next and PragmataPro all loaded on every route.

### Priority Issues

**[P2] The reel, the site's destination, is its least authored page**
- Why it matters: reel views are one of the two outcomes that count. Six full sheets run about 5,000px on desktop and 5,900px on a phone with no overview. Two clips, "I Love to Sing-a & Love Me, Love Me Not" and "No One Has to Know" (`website/src/lib/media.js:196-197`), show only a duration, and REFERENCE.md has no source for either. "She Loves Me" shares its name with the musical; its only context is 11px mono.
- Fix: a program-style running order at the top (number, song, source, duration, anchor). A source line for every clip: wire `show:` where `theatre.toml` has the production; Finn supplies the rest. Mark songs as songs (quotes, or a label like the film's "Film").
- Suggested command: /impeccable layout, then /impeccable clarify

**[P2] Casting vitals and training live only inside the PDF**
- Why it matters: voice part (Tenor), height (6') and the CAP21/Molloy BFA (`REFERENCE.md:22-23`, `:438-439`) are a casting director's first filters, and no site HTML carries them. The `/resume/` preview is a PNG in an `<object>` with only an aria-label (`website/src/routes/resume/+page.svelte:24`), and at 390px its text is about 6.5px.
- Fix: an HTML vitals and training block beside the downloads, sourced from canonical data (a new shared input: `server.fs.allow` plus the Nix source filter). Under 40em, replace the preview with the PDF action or link it to the full image. Leave union and representation out; they aren't on hand.
- Suggested command: /impeccable layout

**[P2] The positioning label disagrees across surfaces (Finn's call)**
- Why it matters: the bio (`website/src/routes/+page.svelte:63`) and page description (`website/src/lib/components/PageHead.svelte:8`) say "performance artist"; the card's alt and sr-only text (`website/src/lib/components/BusinessCard.svelte:487, 503`) say "musical theatre performer"; `og:image:alt` (`PageHead.svelte:26`) adds "and voiceover artist". In casting, performance art is a different discipline, and the description is what search results and link previews show.
- Fix: Finn picks the lead label; the structural strings (alt text, og alt) follow it. No agent rewrite of the bio or description.
- Suggested command: /impeccable clarify (structural strings only, after Finn decides)

**[P3] The homepage middle stacks three display voices, and the start card has a hole**
- Why it matters: "Watch me perform" lands here. "She Loves Me" in two-line Cooper Black, then "Current project.", then "On stage." are three display headings in consecutive viewports, and the Start-here card stretches to the video's height, leaving an empty band between caption and links. The detector's `kicker-above-heading` flags the same block (`website/src/lib/components/Recording.svelte:35`).
- Fix: set the start clip's song at title-show scale so the spread headings keep the headline voice; size the card to its content or lift the links under the meta line.
- Suggested command: /impeccable layout

**[P3] The show page's back link returns somewhere you didn't come from**
- Why it matters: the back-arrowed "Theatre credits" link (`website/src/routes/shows/[id]/+page.svelte:14-16`) always goes to `/resume/`, even after the new photo handoff made the show page feel like a drill-down from `/`.
- Fix: drop the back arrow and style it as a destination, or return to the origin section when the visitor came from `/` (the static link stays as the no-JS fallback).
- Suggested command: /impeccable polish

### Persona Red Flags

- **Casting director (project persona):** meets "performance artist" in the first viewport; can't learn voice part, height or training without downloading; two reel clips have no context; no running order.
- **Non-theatre hiring manager via direct link (project persona):** from `/`, their field is three steps away (Resume, then All resumes; by design). On `/resumes/` no nav item is current, "Preview" opens a bare PNG, and "Download PDF" underlines "PDF" separately, so it reads as two links.
- **Sam (screen reader, keyboard):** the resume preview is an aria-label with no text; the 7 print links have very long accessible names (prefix plus full alt); the two "Watch me perform" links on `/` go to `#start-here` and `/performance-reel/`; captions and transcripts are still pending.
- **Casey (phone):** resume preview text about 6.5px; the card's email about 9px with a 10-11px mono repeat below; the reel is about 5,900px with no way to jump.
- **Jordan (first-timer):** "She Loves Me" at headline scale reads as a production, not a song; the card's flip hint is 11px mono; "Theatre credits" exits to a different page than the one they came from.

### Minor Observations

- "Director:" in resume credits (`website/src/routes/resume/+page.svelte:48`) vs "Directed by" in the current-project notice (`website/src/lib/components/CurrentProjects.svelte:57`).
- The spread repeats Composer Project Revue (prints 03 and 07); Song & Dance Revue's "1 photo" page holds the same photo already on `/`.
- The current project mounts after hydration (`CurrentProjects.svelte:18`) and pushes the page about 450px; it's below the fold at first paint, but a fast scroller on a slow phone sees the jump.
- At 200% text the arrow after "Download resume (PDF)" wraps alone.
- On phones the Contact column sits inset from the header and footer edges; the 3D card's projected link underlines break into dashes at DPR 1.
- DESIGN.md drift: its Footer section still describes the blog's icon tiles (the shipped footer is the "Stage door." slip list, `website/src/lib/components/SiteFooter.svelte:17`, on the global ring), and it says video captions sit below their sheet while `Recording.svelte` renders them above. Update the doc, not the code (/impeccable document).
- The bio has no closing full stop and the description writes "City Based": Finn's copy, Finn's call.
- Add `broken-image` ignores for `CoverPrint.svelte` and `about/+page.svelte` so the detector stops re-flagging the `responsive()` spread.

### Questions to Consider

- What if the reel opened like a program's list of musical numbers, so a casting director picks a clip in five seconds?
- Should voice part and height ride on the headshot's name strip, where real headshot labels carry them?
- Does the start clip need headline scale, or would a ticket-sized slip let "Current project." and "On stage." own the display voice?
- If the photo handoff makes a show page feel like a drill-down from the homepage, should its back link honor that path?

### Run Notes

- Fresh dev server on port 5175, stopped after the run. The `/resume/` PDF/PNG 404s are dev-only; the preview was judged against `result/resume.png`.
- Some full-page captures show blank prints (a capture artifact; the images load and paint in viewport captures).
- B saw the 3D card idle at a 300x150 canvas; a recheck in a visible tab showed the scene running (three.js loaded, 2048x1451 canvas). Not a finding.
- Other Claude sessions were editing `navigation-transitions.ts` and its tests during the run; the transition was judged as it stood then.
