---
target: $impeccable critique
total_score: 25
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 0
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes"
timestamp: 2026-10-23T05-54-24Z
slug: website-src-routes
closed: true
---
Method: dual-agent (A: /root/critique_design · B: /root/critique_evidence)

**The callboard feels authored for you.** The Cooper name, intact performance photos, paper fastenings and current-show ticket form a coherent theatrical identity. The largest opportunity is making the transition from watching your work to taking your resume more immediate.

**Design health: 25/32 (78%), Good.** This is a heuristic review, with two categories inapplicable to this portfolio.

| # | Heuristic | Score | Assessment |
|---|---|---:|---|
| 1 | Visibility of status | 3/4 | Active navigation and player focus make state clear. |
| 2 | Match with the real world | 4/4 | Familiar theatre terminology and direct actions. |
| 3 | User control | 3/4 | Native navigation works; full photos leave the site's navigation. |
| 4 | Consistency | 3/4 | Cohesive visual language; similar prints lead to different destinations. |
| 5 | Error prevention | 3/4 | Download labels are clear; photo destinations need explanation. |
| 6 | Recognition over recall | 3/4 | Main actions are explicit; gallery links and footer icons need inference. |
| 7 | Flexibility and efficiency | n/a | Expert controls are unnecessary for this Experience surface. |
| 8 | Aesthetic and minimalist design | 3/4 | Strong hierarchy; the long reel gives later clips similar weight. |
| 9 | Error recovery | 3/4 | Useful fallbacks and 404 links; production downloads remain unverified. |
| 10 | Help and documentation | n/a | A help system is unnecessary for this portfolio. |
| | **Total** | **25/32** | **Good** |

**What works**

- The two main invitations appear before the portrait on mobile. Visitors can choose to watch or get the resume immediately.
- Photographs lead the visual experience. Level captions, selective fastenings and restrained supporting pages keep the paper treatment coherent.
- The lead video played on desktop and mobile. Keyboard focus, the skip link, direct YouTube links without JavaScript and reduced-motion behavior worked in the sampled checks.

**Priority issues**

1. **[P2] Enlarged text breaks the reel heading.** At 390px with the root font doubled from 16px to 32px, the page becomes 471px wide and clips "Performance" at the viewport edge. Make the heading wrap safely and verify enlarged-text layouts without hiding overflow. This was a text-size stress test, not native browser zoom. [Heading rule](/Users/tunnel/Documents/Git/resume/website/src/styles/site.css:33). Suggested command: `$impeccable adapt`.

2. **[P2] The resume handoff comes too late after watching.** The reel's direct PDF link follows all six recordings, roughly 2,600px down on mobile. Show pages finish with previous/next productions and footer icons. Add a compact PDF link beside or after the lead clip, and an explicit reel/resume invitation at the end of show pages. [Reel sequence](/Users/tunnel/Documents/Git/resume/website/src/routes/performance-reel/+page.svelte:14), [show ending](/Users/tunnel/Documents/Git/resume/website/src/routes/shows/[id]/+page.svelte:44). Suggested command: `$impeccable layout`.

3. **[P2] Similar photographs conceal different destinations.** The hero's Seussical print jumps to the homepage gallery; the gallery print opens Seussical; production photographs open raw image files. On touchscreens, plain captions give little indication of those actions. Add visible destination cues, such as linked production titles and "View full photo," and make the hero print's destination explicit. [Hero print](/Users/tunnel/Documents/Git/resume/website/src/routes/+page.svelte:44), [gallery captions](/Users/tunnel/Documents/Git/resume/website/src/lib/components/PhotoPrint.svelte:44). Suggested command: `$impeccable clarify`.

4. **[P2] Recordings hide their time commitment.** "Start here" establishes a useful first choice, but durations appear only after playback. Add verified runtimes beside titles and compact named jumps to the remaining clips. Keep the first performance dominant. [Recording captions](/Users/tunnel/Documents/Git/resume/website/src/lib/components/Recording.svelte:34). Suggested command: `$impeccable clarify`.

No P0 or P1 issue was established.

**Cognitive load and emotional journey.** The main routes have clear choices. The footer's six equal icon links fail two of eight checklist items, chunking and minimal choices, creating locally moderate load in secondary navigation. The portrait and production photos are the visual peaks; the long recording stack and indirect show-page ending weaken the final invitation to take the resume.

**Persona checks**

- **Impatient casting visitor:** Reaches the lead clip in two clicks, then has to scroll or navigate elsewhere for the PDF.
- **First-time visitor:** Understands the main actions, but cannot reliably predict what a photograph opens.
- **Distracted mobile visitor:** Gets generous primary links, but loses hover cues; small media labels and the enlarged-text overflow reduce readability.

**Detector results.** The source scan of `website/src` produced one `bounce-easing` advisory at [site.css:256](/Users/tunnel/Documents/Git/resume/website/src/styles/site.css:256). Browser scans produced 21 rule instances in 11 groups across five routes: cream palette (5), organic clip paths (5), undersized text (4), stripe gradients (3), bounce easing (2), straggler (1), and kicker above heading (1). Many are repeats of shared styling. The cream paper, torn edges, perforations and meaningful Film label fit the documented design; the easing is a deliberate interaction choice. The four small-text flags confirm the review's concern about 10px photo/video counts. The enlarged-text overflow was found by a separate browser check.

**Smaller refinements.** Increase the functional photo/video counts from 10px, enlarge the Contact links' approximately 24px hit areas to the project's 44px target, and adjust the bio's measure if you want to eliminate its single-word final line. Preserve the bio's wording. [Media counts](/Users/tunnel/Documents/Git/resume/website/src/styles/site.css:332), [Contact links](/Users/tunnel/Documents/Git/resume/website/src/styles/site.css:419).

**Questions to consider.** After the lead performance, should the next invitation favor taking the resume or watching another recording? Should every photograph visibly named Seussical lead to that production?
