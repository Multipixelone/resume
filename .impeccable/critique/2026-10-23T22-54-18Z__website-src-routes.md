---
target: whole site (website/src/routes)
total_score: 27
max_score: 36
na_heuristics: 10
p0_count: 0
p1_count: 1
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes"
timestamp: 2026-10-23T22-54-18Z
slug: website-src-routes
---
Method: dual-agent (A: isolated design-review sub-agent · B: isolated detector sub-agent). Both were interrupted by a network error and resumed from their own transcripts; neither saw the other's output.

Target: the whole site (`website/src/routes`), assessed on the Nix production build of 697b6ec served locally, at 1440x900, 768x1024 and 375x812. Uncommitted Contact and business-card work was not in that build.

### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Current nav slip and live "In rehearsal" status work; show pages mark no nav section, and the current project pops in after hydration |
| 2 | Match System / Real World | 3 | Theatre language is native (Admit one, One night only, Directed by); "Self" as a role, "Cooper* license", "built from 697b6ec" and "PGP key" leak through |
| 3 | User Control and Freedom | 3 | Nav, back link and pager everywhere; PDFs are forced downloads with no view-first option |
| 4 | Consistency and Standards | 3 | Tight tokens; "Self" is suppressed in three components but printed by PhotoPrint; the closing reel/PDF slip is on 3 of 5 page types |
| 5 | Error Prevention | 3 | Little to get wrong; email is mailto only |
| 6 | Recognition Rather Than Recall | 3 | Footer is six icon-only links named only in `title`; homepage prints give no cue that they open show pages |
| 7 | Flexibility and Efficiency | 3 | Scored for the supporting pages: deep links per show, YouTube fallback per clip, skip link; "Watch me perform" lands at the reel top, not on the start clip |
| 8 | Aesthetic and Minimalist Design | 3 | Hero and supporting pages are focused; two 88px headings share one desktop viewport, and every page ends on developer meta |
| 9 | Error Recovery | 3 | 404 offers the reel, the PDF and home, but no context line for old Squarespace paths |
| 10 | Help and Documentation | n/a | A portfolio has no task that needs documentation |
| **Total** | | **27/36** | **Good (75%)** |

### Design Specificity Verdict

**LLM assessment:** Authored for Finn, not interchangeable. The Callboard is built as objects with behavior, not as a texture: the torn "Orch · Row F" brand ticket, the current-project stub with its "Admit one" end and perforated "Get tickets" band (it flexes on keyboard focus too), tape, a photographed pushpin, folded corners, a "Start here" ticket on the reel, credits under a dashed tear-off. The hero (Cooper Black name top left, tilted matted headshot right, the taped Cat in the Hat print swinging off it) shows range in one glance and avoids every rejection in DESIGN.md. Supporting pages calm down as asked. It goes generic where content is thin: the Song & Dance show page holds one print, the same one the homepage shows largest; the reel is six identical sheets in a column; the 404 is "Page not found" plus links; every page's last words are "Cooper* license · built from 697b6ec". The ticket also does four jobs (brand, stub, "Start here", the Play control on all six video sheets), which spends the signature.

**Deterministic scan:** CLI `impeccable detect --json website/src`: exit 0, 0 primary findings, 1 advisory (`bounce-easing`, site.css:258). The CLI is regex-only on source, so element rules ran in the browser pass instead:
- Real: `undersized-ui-text` on the four "N PHOTOS / N VIDEOS" counts on `/resume/` (10px, `.credit-reel-count`, site.css:334). The design review flagged the same 10-11px labels independently.
- Real but mild: `bounce-easing` on the loose prints' hover lift, `cubic-bezier(.2, .8, .2, 1.15)` (one 3.4% overshoot, not an elastic bounce). The review missed it. Fastened prints already use a non-overshoot curve (site.css:271-272), so loose and fastened prints answer the hand differently.
- Intentional here: `cream-palette` (Playbill Paper is the brief), `organic-clip-path` x3 (the ticket tear and tape are documented signature shapes), `kicker-above-heading` on "Film" (documented). The kicker flag lands on the same element as priority issue 2: the kicker isn't the problem, it's the only context the film gets.
- False positive: `repeating-stripes-gradient`. All three sources are 1px dashed perforations.

The detector reads the core moves (cream stock, torn clip-paths) as category tells. They are documented here, but the warning is fair: warm paper plus Cooper plus torn edges is a known craft-site look, and what keeps this specific is the theatre objects. Grow those, not generic paper texture.

**Visual overlays:** The detector ran in-page on `/`, `/resume/`, `/performance-reel/`, `/booking/` and `/shows/seussical/`; the overlay was left on the homepage in the [Human] tab of the Browser pane. The critique server was stopped afterward.

### Overall Impression

At the first viewport this is about as strong as an actor site gets for this brief: confident, warm, specific, and accessible underneath. The weak points are all downstream of the hero: the reel (the main destination) under-explains half of what it plays, show pages (where interest peaks) end without the reel/PDF ask, and the type visitors get is not the type Finn sees. Biggest opportunity: make the reel as authored as the homepage.

### What's Working

1. **A physical system, not a skin.** Shadows by object type, square paper corners, fastenings that never cover a face, words that never tilt. It separates the site from template actor sites while keeping every caption readable.
2. **Live data as design.** The stub appears from first rehearsal through closing in Eastern time, and right now correctly shows the Nov 15 cabaret with livestream. Credit rows link to each show's evidence with a cover print and a count. Nothing can drift from the PDF.
3. **Accessibility and motion craft well above typical portfolios.** A visible 3px rust focus ring that tilts with its print, focus equals hover everywhere, a composed accessible name for the ticket stub, 44px targets, a skip link, reduced motion in both CSS (site.css:579-581) and motion.ts, forced-colors flattening, and no-JS fallbacks for posters and the resume preview.

### Priority Issues

**[P1] Visitors get a different type system than the one Finn reviews**
- **What:** Sabon Next fails CORS from fonts.finnrut.is on this origin, so body, bio, links and h2/h3 render in Georgia. PragmataPro fails too but renders on Finn's Mac because it's installed locally (fonts.css lists `local()` first), so the reviewers' screenshots, and Finn's own view, show a label voice visitors never get; they see SF Mono or Consolas. The eight remote declarations are in the built CSS and on `origin/main`, which `website.yml` deploys on every push, although PRODUCT.md and docs/portfolio-site.md:214 say not to deploy them until the license is confirmed.
- **Why it matters:** Georgia Bold h2s ("Theatre credits", the /resumes/ field headings) sit heavy beside Cooper, and tracked caps in SF Mono/Consolas push the labels toward the terminal look DESIGN.md rejects. The deploy also contradicts a stated release gate.
- **Fix:** Gate the remote faces out of production builds (as about.ts gates /about/) until Finn confirms coverage. Then design the fallback on purpose: metric overrides (`size-adjust`, `ascent-override`) on `local("Georgia")` so the 36ch bio doesn't reflow when Sabon arrives, and check tickets and labels at SF Mono/Consolas widths (6-10% wider). Review screenshots with the local PragmataPro disabled.
- **Suggested command:** /impeccable typeset (plus /impeccable harden for the build gate)

**[P2] The reel, the main destination, doesn't say what half of it is**
- **What:** Two of five clips ("I Love to Sing-a & Love Me, Love Me Not", "No One Has to Know") have no `show` in media.js:196-197, so they get a title and nothing else. The film gets only a "Film" kicker: its role, company and director are in REFERENCE.md:491 but not in theatre.toml, so the site can't read them. Its YouTube auto-poster doesn't show Finn, and "How Lucky You Are" falls back to a letterboxed 480x360 poster (hq720 404s).
- **Why it matters:** Success is the visitor watching Finn perform. A casting director choosing a second clip needs to know what it is, where and when.
- **Fix:** Add the film to theatre.toml and caption it like the theatre clips. Give recordings an optional context line and a custom poster in media.js, filled from REFERENCE.md or by Finn, blank rather than guessed. Pick poster stills that show Finn for the film and the low-res clip.
- **Suggested command:** /impeccable clarify

**[P2] The ask disappears where interest peaks**
- **What:** Home, /resume/ and the reel close on the reel/PDF slip. Show pages end on the pager and footer (shows/[id]/+page.svelte:44-59), and Contact links to the reel and resume pages but not the PDF (still true in the uncommitted rework).
- **Why it matters:** A show page is where a "tell me more" click lands; it should end on the outcome PRODUCT.md counts, the PDF download.
- **Fix:** Render `PerformanceNextSteps` after the pager (`data.resumePdf` is already in layout data, +layout.server.js:14), and add the PDF download to Contact.
- **Suggested command:** /impeccable layout

**[P2] The homepage spread hides its depth and breaks its own caption rule**
- **What:** Prints link to show pages, but only the image is the link (PhotoPrint.svelte:23-26) and nothing says so; touch gets no hover lift. 13 of 21 photos live only on show pages. Captions print "Self" for prints 01, 03 and 07 (PhotoPrint.svelte:45), though CurrentProjects, Recording and the show page suppress it. Composer Project Revue appears twice with identical captions.
- **Why it matters:** Most of the visual evidence is reachable from the homepage only by guessing a photo is a link, and "Self" three times reads as filler.
- **Fix:** Add a mono "N photos" line under each caption (the /resume/ count pattern) or link the caption title; suppress "Self" in PhotoPrint; drop the repeated caption on the second Composer print.
- **Suggested command:** /impeccable clarify, then /impeccable polish

**[P2] Information-bearing labels fall below a legible size**
- **What:** The "3 PHOTOS / 2 VIDEOS" counts on /resume/ are 10px uppercase mono (site.css:334) and describe their links via `aria-describedby`; credit labels and "One night only" are 11px; "Orch · Row F" is 8px (site.css:51). Detector and design review both flagged these.
- **Why it matters:** These are the cues that a credit has evidence behind it. 10px tracked caps are hard to read for low-vision visitors and on non-retina screens, and the fallback mono makes them worse.
- **Fix:** Set a floor in DESIGN.md: 0.75rem for any label that carries information, 0.6875rem for purely decorative print. Raise `.credit-reel-count` and the credit labels to it.
- **Suggested command:** /impeccable typeset

### Persona Red Flags

**Dana, casting associate** (from PRODUCT.md Users: dozens of performers at 60-90 seconds each, watches the start of one clip, files the PDF)
- "Watch me perform" lands at the top of the reel page, not on the "Start here" clip.
- Vocal part and height (REFERENCE.md:22-23) exist only inside the PDF and PNG.
- In ensemble prints (Joseph's matching shirts, Kiss Me Kate's fedoras) nothing tells Dana which performer is Finn. A cue would need Finn's verification, not an alt-text guess.
- Show pages end with no PDF (issue 3).

**Jordan (first-timer)**
- The footer is six icon-only links (SiteFooter.svelte:17-23); the key and pen glyphs don't explain themselves, and "PGP key" is jargon.
- The homepage "Theatre credits" link lands on the resume image; the list starts about 1355px down.
- Each clip has two play paths ("Play" and "Watch on YouTube") with no difference explained; "back" is a ↙ glyph.

**Casey (distracted mobile)**
- At 375x812 the homepage is 4926px tall; the closing slip starts after seven prints, at 4476px.
- Images ship at one size: the nine homepage photos total 2.59MB, up to 1920px wide, drawn at 327px on a phone, with no `srcset` and no AVIF/WebP.
- CurrentProjects mounts client-side, so on slow loads the stub pops in and shifts the spread.
- Good: no horizontal scroll at 320 or 375, 44px targets, and the stub is one big tap target.

**Sam (accessibility)**
- Videos have no captions or transcripts yet, so the main destination is closed to deaf visitors.
- The resume preview is an `<object>` with an aria-label (resume/+page.svelte:24), unevenly supported; an `<img alt>` with the same fallback links is sturdier.
- "Cooper* license" (105x22) and the build badge (166x27) are under the 44px rule.
- Homepage print link names are long alt sentences plus an `aria-describedby` that repeats the title and role.

### Minor Observations

- "Current project." uses the 88px headline for a one-show block, so two 88px headings share one screen at 1440x900 (site.css:237).
- At 1440x900 the hero ends at 794px and the next rule starts at 906px, so the first screen closes on blank paper.
- DESIGN.md:278 describes one reel slip plus a dotted resume/about/contact line; the build has two equal slips (+page.svelte:20-23). Reconcile one or the other.
- Three left edges on the reel and show pages at 1440 (h1 at 120px, recordings at 256px, closing slip at 271px).
- ↗ marks internal routes and external sites alike; reserve it for off-site links.
- "Resume with headshot (PDF)" has no arrow on /resume/ but a ↓ in the closing slip.
- Loose prints overshoot on hover and fastened prints don't; pick one curve.
- A window exactly 768px wide falls between the 769px and 767px queries (site.css:221, 509): fine today, fragile.
- /resumes/ "Preview" opens a bare PNG outside the site.

### Questions to Consider

- If a casting director watches one clip, why not land "Watch me perform" directly on it (still user-played)?
- In how many of the seven homepage prints can a stranger find Finn within two seconds? Would choosing prints where Finn is the focal point beat covering every production?
- Should the board post the facts a breakdown asks for (vocal part, height, NYC) as a stage-manager label by the name, or is keeping them in the PDF a deliberate "watch first" choice?
- If everything is a ticket, is anything? Would the stub feel more like the signature if the six Play controls were plain?
- Between productions the stub disappears. What real, already-dated item could hold that spot without inventing dates?

**Run notes:** One design-review claim was corrected (photos ship at up to 1920px, not 4996px). The impeccable live server on port 8400 is from an earlier session and was left running.

### Follow-up after the user's answers

- The P1 font gate is withdrawn. fonts.finnrut.is returns `Access-Control-Allow-Origin: https://finnrut.is`, so Sabon Next and PragmataPro load on the production domain. They fail only on localhost and on the github.io Pages origin before DNS cutover. The Georgia observations in this run describe those origins, not production.
- User priorities: endings and photo cues first, all five issues in scope, Contact left alone until the uncommitted rework lands.
