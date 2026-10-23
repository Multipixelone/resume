---
target: website (whole site, website/src/routes)
total_score: 28
max_score: 36
na_heuristics: 10
p0_count: 0
p1_count: 2
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes"
timestamp: 2026-10-23T05-19-39Z
slug: website-src-routes
closed: true
---
Method: dual-agent (A: design review sub-agent, B: detector sub-agent). Build reviewed: cc1643b (Nix production build, licensed fonts local). c41c543 and 661387b landed mid-run, not re-checked.

| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Nav slips mark page; show pages light no nav item |
| 2 | Match System / Real World | 4 | Theatre-native vocabulary |
| 3 | User Control and Freedom | 3 | Long pages end with no way onward |
| 4 | Consistency and Standards | 3 | "Self" only in homepage captions; hero print scrolls, others open pages; (PDF) vs PDF |
| 5 | Error Prevention | 3 | Resumes save under anonymous filenames |
| 6 | Recognition Rather Than Recall | 3 | Icon-only footer, no reel/PDF there |
| 7 | Flexibility and Efficiency | 3 | Reel page PDF at bottom of ~4,960px |
| 8 | Aesthetic and Minimalist Design | 3 | Duplicate Cat in the Hat photo; YouTube chrome |
| 9 | Error Recovery | 3 | Branded no-JS 404; failing embed shows black card |
| 10 | Help and Documentation | n/a | Portfolio, nothing to learn |
| Total | | 28/36 (78%) | Good |

Specificity: authored (Callboard system: torn tickets, fastening physics, level words). Weakest: footer icon row, reel page dominated by YouTube chrome.
Detector: CLI 0 findings (regex-only, 19 files). Overlay true positives: reel slip contrast 4.43:1 (both agree), bio straggler, 10px credit counts (site.css:346), 10px phone "Seussical" caption. False positives: cream-palette, organic-clip-path, Film kicker, Start-here occlusion. Unsettled: photo-mat 1.15 overshoot (site.css:270).

Priority issues:
1. [P1] Reel/resume CTAs at or below the fold (748-793px @1440x900, 732-777 @1366x768, 755-800 @375x812); resume link 15px dotted; slip contrast 4.43:1. Fix: hero-links under name (desktop), before .portrait-scene via order (phone), trim margins under ~850px tall, resume slip, Deep Marquee Rust label. /impeccable layout
2. [P1] Reel opens on YouTube overlay title "...Finn Rutis v1"; site caption below fold; film embed failed on localhost but oEmbed 200 (verify on finnrut.is). Fix: click-to-load posters on .video-mat. /impeccable harden
3. [P2] Long pages end without onward path (/ ~4,250px, /resume/ ~3,230px; footer lacks reel/PDF). Fix: reel page's closing block on spread and credits. /impeccable layout
4. [P2] Downloads save as resume.pdf (variants.toml:22; bare download attr resume/+page.svelte:16-17, performance-reel/+page.svelte:26-27, ErrorPage, /resumes/). Fix: download="Finn Rutis resume.pdf". /impeccable harden
5. [P2] Tab order: .portrait-scene before .bio-block (+page.svelte:22 vs :54), jump link before CTA. Fix: reorder markup, order on phones. /impeccable harden

Persona flags: casting director (fold, v1 title, resume.pdf, first production photo ~1,560px down); Casey (14px Reel nav at top, 2.45MB JPEGs no srcset, 22-27px footer targets); Sam (jump link first, "Sun / 2026" ticket name, 200% caption overflow); Jordan (icon-only footer, five document names, "Self").

Minor: "Self" role (content.mjs:61, PhotoPrint.svelte:45); hero reuses tall print (+page.svelte:12); ~550px spread hole (HEAD tall-bottom may fix); no text-wrap: pretty on bio; 768px gap (site.css:235/470); photo-mat overshoot; 10px functional counts; iframe allow+allowfullscreen warning (Recording.svelte:23-24); (PDF) vs PDF; Theatre credits link misses anchor; phone header shows only "Rutis".

Questions: hero print as reel still? spread lead with characters? six embeds before PDF? cabaret notice at Headline size?
