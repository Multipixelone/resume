---
target: the portfolio site (website/src/routes)
total_score: 23
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 2
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes"
timestamp: 2026-10-22T20-21-12Z
slug: website-src-routes
---
Method: dual-agent (A: design-review sub-agent · B: detector sub-agent)

## Critique: finnrut.is portfolio site (website/src/routes)

### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | The nav slip marks the current page, and the ticket's status line is exemplary. Current project mounts after hydration with no reserved space and pushes the gallery down |
| 2 | Match System / Real World | 3 | Theatre language throughout, but reel headings are bare song titles and the film is headed just "Film" |
| 3 | User Control and Freedom | 3 | No traps and a working skip link, but gallery prints and /resumes/ previews drop visitors on bare image files |
| 4 | Consistency and Standards | 3 | The visual system is tight, but labels drift: "Self" is shown in one place and hidden in another, "Directed by" vs "Director:", three names for one PDF |
| 5 | Error Prevention | 3 | The theatre PDF is clearly primary on /resume/, but 35 similar rows on /resumes/ invite the wrong pick |
| 6 | Recognition Rather Than Recall | 3 | Text nav and level captions, but the footer is icon-only and its title tooltips never show on touch |
| 7 | Flexibility and Efficiency | n/a | A portfolio has no repeat-use workflow to speed up |
| 8 | Aesthetic and Minimalist Design | 3 | The homepage is disciplined. The noise is in the /resumes/ wall and the developer-style footer meta |
| 9 | Error Recovery | 2 | The build ships no 404.html, so a bad URL in production gets GitHub's page. The site's own 404 offers only "Return home" |
| 10 | Help and Documentation | n/a | The content is the documentation |
| **Total** | | **23/32** | **Good (72%)** |

### Design Specificity Verdict

**LLM assessment:** This is designed for Finn, not a template, and the homepage proves it. The Callboard idea lives in objects only this site has:
- the torn "Orch · Row F" brand ticket;
- the playbill-scale name, with "Rutis" in rust;
- a headshot printed with its own name strip and pronouns;
- the taped Cat in the Hat print;
- gallery prints held by tape, a photographic pushpin and folded corners;
- a ticket stub computed from real show dates.

The type roles hold: Cooper for names, Sabon for reading, PragmataPro for labels. One accent color does all the pointing, and words never tilt.

The supporting pages slip from "calm" to "anonymous":
- The reel is six identical heading, link and iframe blocks.
- /resumes/ is a generic download list.
- Contact is a two-row list.
- The 404 is stock.

Strip the header and any portfolio template could have made these pages. That hurts most on the reel, the page the site exists to deliver.

Missed chances for character:
- the reel as a program's song list (the gallery captions already work this way);
- a 404 that reads as the ticket for a show that has closed;
- a footer that ends every page on a build badge instead of the reel or the PDF.

**Deterministic scan:**
- **CLI:** `impeccable detect --json website/src` exited 0 with one advisory finding, bounce-easing on the .photo-mat transition (website/src/styles/site.css:262).
- **Browser overlay:** 12 items across six routes at 1024px, 7 of them on /. A 375px pass added two more.
- **Both assessments caught:** "Watch me perform" is rust on Callboard Card at 4.43:1 (website/src/styles/site.css:143).
- **Only the detector caught:**
  - the bounce curve;
  - a last word left alone on its own line, in the bio at 1024px and in a /resumes/ subtitle at 375px;
  - the hero print caption dropping to 10px on phones (website/src/styles/site.css:425).
- **False positives:**
  - cream-palette on every route: that is Playbill Paper (#f7f4ed), which the light-only rule in DESIGN.md calls for;
  - organic-clip-path, three times: the stub's torn edge and two tape strips are meant to look like torn paper.
- The detector can't see the navigation, content and journey problems that lead this report.

**Visual overlays:** The overlays are live in the [Human] tab of the built-in Browser pane. There are two outlines: the bio's stray last word and the low-contrast reel link. The dev server is stopped, so the tab is a frozen snapshot.

### Overall Impression

The homepage is real design. It does the casting job in five seconds, with a point of view nobody else could reuse. The site around it isn't ready to go public:
- /resumes/ publishes a job search.
- About is unfinished scaffolding behind the first nav item.
- The reel, which the site exists to deliver, is its plainest page.

The biggest opportunity: give the reel the care the homepage got, and cut /resumes/ down to what a theatre maker needs.

### What's Working

1. **The ticket stub is character and function at once.**
   - Whether it shows, its status wording and its dates all come from theatre.toml (website/src/lib/components/CurrentProjects.svelte:34), so it can never show a stale "now playing".
   - The whole stub is one link.
   - Hover inverts the band and flexes "Admit one". Reduced motion keeps the ink change.
2. **The first viewport has a single, clear order of importance.**
   - The 11.5rem name owns the screen.
   - The headshot carries the name and pronouns as part of the print.
   - Exactly one CTA sits on a paper slip; resume, about and contact drop to a small dotted line.
   - On phones it reflows to name, face, bio, with no overflow down to 320px.
3. **Accessibility is built into the metaphor.**
   - All 27 homepage links get the 3px rust focus ring.
   - Fastenings are aria-hidden and disappear in forced colors.
   - Reduced motion is honored in the CSS and in every JS action.
   - No animation loops while idle.

### Priority Issues

**[P1] /resumes/ publishes the whole job search, one click from every page**
- **What:**
  - 35 entries in registry order, and 26 are tailored to a named employer: Anthropic four times, Mistral, Hebbia, ElevenLabs, NYT, Vox and more.
  - Two cover letters show raw slugs, "tavily-cover-letter" and "novig-cover-letter", because website/lib/content.mjs:24 falls back to dest when title is missing.
  - The Repertory Sheet and Title Pages sit at rows 32 and 33.
  - The footer's resume icon links here from every page (website/src/lib/footer.ts:17).
- **Why it matters:**
  - PRODUCT.md says the tech side is "a quiet signal, not a section"; this is the loudest section on the site.
  - A casting director who clicks it lands in a tech job hunt.
  - An employer who follows their link sees the applications to competitors.
  - The slug titles look broken.
- **Fix:**
  - List the theatre documents first, then the general field resumes grouped by field.
  - Unlist the employer-tailored versions and the cover letters with site_hidden; direct links keep working.
  - Fail the build when a listed variant has no title.
  - Point the footer icon at /resume/.
- **Suggested command:** /impeccable distill

**[P1] About is placeholder scaffolding behind the first nav item**
- **What:**
  - /about/ shows "[Artist statement]" and two "[Escapade title]" / "[A paragraph or two]" entries (website/src/routes/about/+page.svelte:19, website/src/lib/about.ts:13).
  - It is the first nav item on every page (website/src/routes/+layout.svelte:10), and "More about me" on the hero.
  - The Off stage section only checks that escapades is non-empty, and the placeholders pass that check.
- **Why it matters:** every push to main deploys, and the site is lined up to replace Squarespace. A casting director judging whether Finn is serious meets an unfinished page.
- **Fix:** hide the page; don't write the copy. Treat bracketed placeholders as "no content" at build time. Until Finn's words land, drop About from the nav and the hero, and skip prerendering /about/.
- **Suggested command:** /impeccable harden

**[P2] The main call to action misses the site's own accessibility bar**
- **What:**
  - **Contrast:** "Watch me perform" is 4.43:1, below 4.5:1 for 19px text at weight 600. DESIGN.md's 4.85:1 figure is for rust on paper, not on card.
  - **Focus order:** the overlapping Seussical print link (website/src/routes/+page.svelte:39) comes before the CTA (website/src/routes/+page.svelte:56) in the markup. Keyboard focus jumps right to a link that only scrolls to the gallery, then back left.
  - **Phones:** at 375x812 the slip sits at 755 to 801px, which falls below the first screen once the browser's toolbars take their space.
- **Why it matters:** reel views are the success metric, and this is the one link that delivers them. It's weakest for keyboard, low-vision and phone visitors (Principle 5).
- **Fix:**
  - Set the slip label in Deep Marquee Rust (6.52:1 on card), or put the slip on Playbill Paper, and update reel-slip in DESIGN.md.
  - Move the hero print link after the hero links in source order.
  - On phones, tighten the stack above the bio.
- **Suggested command:** /impeccable polish, then /impeccable adapt for the phone layout

**[P2] The reel is the page the site exists for, and it has had the least design work**
- **What:**
  - There are five recordings and a film, each the same heading, "Watch on YouTube" link and iframe.
  - The headings are bare song titles with no show, role or year (website/src/lib/media.js:65).
  - The film is headed "Film"; its real title appears only in the iframe's title attribute.
  - No clip is suggested as the place to start, and the page doesn't lead on to the PDF.
- **Why it matters:** a casting director has to play each clip to learn what it is, and after watching, the next step means going back to the nav.
- **Fix:**
  - Caption each clip the way the gallery captions its photos: the song in Cooper Bold, then small labels for show, character and year.
  - Link each recording to its theatre.toml id, as the photos already are.
  - Use the film's real title as its heading, with "Film" as the small label above it.
  - Mark one clip as the place to start, and end the page with the theatre resume download.
- **Suggested command:** /impeccable clarify

**[P2] Journeys dead-end: there's no production 404, and no page ends on the reel or the PDF**
- **What:**
  - The HEAD build has no 404.html (website/svelte.config.js:9). On GitHub Pages a bad URL gets GitHub's generic page instead of website/src/routes/+error.svelte, and that page only offers "Return home" anyway.
  - / ends on print 06 and an icon footer with no reel link.
  - "Theatre credits" (website/src/routes/+page.svelte:75) lands at the top of /resume/, not at the credits.
- **Why it matters:** Principle 2 promises a short path to the reel and the PDF from every page, but today that path exists only in the header. After cutover, stale links and typos will hit an unbranded page.
- **Fix:**
  - Prerender a not-found route, copy it to build/404.html during assembly, and give it Reel and Resume (PDF) links.
  - End / and the reel page with the same two links.
  - Retarget "Theatre credits" to /resume/#credits-title.
- **Suggested command:** /impeccable harden

### Persona Red Flags

**Dana, casting director (the primary user).** The first screen works at 1440 and 1024. After that:
- The link preview that brought Dana here says "musical theatre performer", but the bio says "performance artist".
- Voice part (Tenor, from metadata.toml) appears nowhere on the site.
- Range is hard to read from the photos:
  - the Cat in the Hat appears three times among seven prints;
  - two prints are revues captioned "Self";
  - Finn is never identified in ensemble shots.
- "All resumes" opens a tech job hunt, and About shows "[Artist statement]".

**Morgan, tech hiring manager arriving from a tailored PDF.**
- Morgan lands on a theatre homepage, which is the agreed "quiet signal" call. The footer (LinkedIn, blog, PGP key) hints at the tech side at the right volume.
- But the footer's resume icon shows Morgan their own resume beside ones for other employers, plus "tavily-cover-letter".

**Casey, on a phone (375x812).**
- The CTA sits right at the fold, and the resume, about and contact line is below it.
- Tapping a gallery print opens a bare JPG with no site around it (website/src/lib/components/PhotoPrint.svelte:20).
- /resume/ spends a full screen on a sheet preview 300px wide, too small to read, before the credits.
- /resumes/ is 7.8 screens long, and "Resume with headshot" is its last link.

**Sam, keyboard and screen reader user.**
- Focus goes from the nav to the far-right print, then back left to the CTA.
- The CTA's contrast is 4.43:1.
- The ticket is announced as "...Nov 15 Sun / 2026..." (website/src/lib/components/CurrentProjects.svelte:70).
- Links that leave the site (box office, YouTube, Instagram) give no cue that isn't visual.
- The resume preview is an object element with type image/png, which screen readers handle inconsistently.

**Riley, testing edge cases.**
- site_hidden means unlisted, not private. Six hidden PDFs, including astor-place-cover-letter.pdf, ship at guessable URLs.
- A variant added without a title goes public under its file name, with no warning.
- A fresh load of /#photos-title loses its scroll target: Current project appears above it once the page's JavaScript runs (website/src/lib/components/CurrentProjects.svelte:18).

### Minor Observations

- **One link preview, two Finns.** The bio and every meta description say "performance artist" (website/src/lib/components/PageHead.svelte:8). The social card and og:image:alt (website/src/lib/components/PageHead.svelte:26) say "musical theatre performer and voiceover artist". Finn picks which one is canonical; then generate both from one field.
- **Bio wording:** the capital "Based" and the missing full stop are flagged for Finn. I haven't rewritten them.
- **Bio line break:** text-wrap: pretty fixes the stray "experience" at 1024px without touching the words.
- **Bounce:** the 1.15 overshoot on .photo-mat is the only bounce on the site. It's about 0.3px of travel; remove it for consistency.
- **Label drift:**
  - "Self" is hidden on the current project but printed under prints 01 and 03.
  - "Directed by" vs "Director:".
  - One PDF goes by three names.
  - "Resume with headshot" lacks the verb and arrow its sibling link has (website/src/routes/resume/+page.svelte:15).
- **Links:** the same arrow marks internal links and links that leave the site. The ticket opens the box office in the same tab.
- **Livestream:** "Livestream available" says a stream exists but not where to find it.
- **Hierarchy:** the "Current project." heading is larger than the show title under it.
- **Small text:** photo index numbers are 10px, ticket labels 11px, and the hero print caption 10px on phones.
- **Gallery:** on desktop it ends lopsided, with an empty patch at lower left next to Kiss Me Kate.
- **Footer meta:** the "Cooper* license" link (22px) and the build badge (27px) are under the 44px minimum. The license link opens a raw LICENSE.md.
- **Social card:** it has no photo, only type.
- **Reel iframes:** they set both allow and allowfullscreen, which logs a console warning (website/src/routes/performance-reel/+page.svelte:22).
- **Docs drift:** PRODUCT.md and docs/portfolio-site.md say three recordings; media.js has five.
- **Motion, unverified:** this comes from reading the code only. printEntrance may snap a print that's already visible to its first keyframe (website/src/lib/motion.ts:173). Check it in a browser window in front.

### Questions to Consider

- If the reel is the destination, why is it the plainest page? What if it read like a program's song list, with one clip marked as the place to start?
- Who is /resumes/ for, if hiring managers arrive by direct link? Does a public index of every application belong in a theatre site's footer?
- Should About exist before Finn writes it?
- Which one description should a casting director leave with? Today the link preview gives two.
- Does the board show range? Three of the seven prints are the Cat in the Hat.

### Run notes

- **How it was checked:** the visuals came from the dev server, which serves the real fonts. The resume pages were checked against a fresh Nix build of HEAD. Motion was judged from the code only, because the Browser pane was hidden and that slows its animations.
- **Uncommitted layout change:** website/src/routes/+layout.svelte still carries an Impeccable live-mode injection. A live server from an earlier session is still running on port 8400, and it shows a "variant manifest 404" toast on page load. The injected file is gitignored, so committing the layout as it stands would break the CI build. I left both alone.
