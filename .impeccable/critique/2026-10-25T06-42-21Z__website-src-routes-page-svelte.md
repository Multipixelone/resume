---
target: portfolio homepage and main visitor paths
total_score: 26
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 0
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes/+page.svelte"
target_fingerprint: "sha256:c7c2351eb298adb2d26472826114874045474eecebefc8fe9572c350433ebff7"
target_path: /Users/tunnel/Documents/Git/resume/website/src/routes/+page.svelte
timestamp: 2026-10-25T06-42-21Z
slug: website-src-routes-page-svelte
---
Method: dual-agent (A: /root/design_review · B: /root/detector_evidence)

**The callboard design works. The next pass should make watching performances and reading contact details easier.** The huge Cooper name, warm stock, real production photographs and ticket motif feel specific to Finn. Preserve that visual direction.

Scope: the homepage and its reel, resume, contact and Seussical flows. Desktop and 390 x 844 mobile-width views were inspected.

**Design health: 26/32 (81%), Good.** No P0 or P1 issue was demonstrated.

| # | Heuristic | Score | Finding |
|---|---|---:|---|
| 1 | Visibility of system status | 2/4 | Video handoff has no loading feedback. |
| 2 | Match with the real world | 4/4 | Theatre language and physical materials fit the work. |
| 3 | User control and freedom | 4/4 | Native links, clear return paths and reversible card flipping. |
| 4 | Consistency and standards | 4/4 | Type, color, materials and interactions form a coherent system. |
| 5 | Error prevention | 3/4 | Explicit PDF labels and descriptive links reduce wrong turns. |
| 6 | Recognition rather than recall | 3/4 | Show pages give no early route to their recordings. |
| 7 | Flexibility and efficiency | n/a | Power-user controls are unnecessary for this portfolio. |
| 8 | Aesthetic and minimalist design | 3/4 | Strong hierarchy; contact lettering becomes too small on phones. |
| 9 | Error recognition and recovery | 3/4 | Direct YouTube fallback exists; stalled-player recovery is unverified. |
| 10 | Help and documentation | n/a | The core tasks do not require a help system. |
| | **Total** | **26/32** | **Good** |

**What works**

- The opening gives visitors Finn's face, name and two useful actions immediately. Both actions remain above the portrait at phone width.
- The gallery has rhythm: varied image sizes, offset compositions and level captions. The production photographs supply the character.
- The reel provides a clear starting point: “She Loves Me,” a 1:15 duration, a “Start here” ticket and a substantial Play target. Resume links at the top and end support the intended next step.

**Priority issues**

**1. [P2] The video handoff needs visible feedback.** [Recording.svelte:24](/Users/tunnel/Documents/Git/resume/website/src/lib/components/Recording.svelte:24) removes the poster as soon as it creates the iframe. A blank handoff was observed; the cause and reliability of external playback were not established. The source confirms that no pending state explains the transition. This creates uncertainty at the site's most important action.

Keep a useful poster or loading presentation until the player initializes, and keep the existing YouTube fallback obvious when loading takes too long. Suggested command: `$impeccable harden`.

**2. [P2] Show pages hide the route to their recordings.** The homepage advertises Seussical as “3 photos · 2 videos,” but [the show page](/Users/tunnel/Documents/Git/resume/website/src/routes/shows/[id]/+page.svelte:34) places both recordings after all three large photographs, with no early shortcut. A visitor who came to hear Finn has to scroll through the photo sequence.

Add a conditional “Watch performances” jump beside the show credits, leading to the recordings. Keep the photo composition. The proposed structural label is renameable. Suggested command: `$impeccable clarify`.

**3. [P2] The contact card's text gets too small on phones.** At 390px wide, the card is approximately 290px across. Its email and Instagram lettering shrink with the artwork, and the separate selectable email is only 11px. The measured link targets were approximately 98 x 50px, so the problem is reading the destination, not hitting it. See [BusinessCard.svelte:552](/Users/tunnel/Documents/Git/resume/website/src/lib/components/BusinessCard.svelte:552).

Increase the existing selectable address to around 15-16px on phones. If the on-card details still need enlargement, use a mobile artwork treatment that preserves the approved card and its native links. Suggested command: `$impeccable adapt`.

**Cognitive load and emotional journey**

Seven of the eight cognitive-load checks pass: single focus, chunking, grouping, hierarchy, sequential decisions, working-memory support and progressive disclosure. The six equally weighted footer icons exceed the checklist's four-choice threshold, but they are peripheral. Overall cognitive load is low; the four main navigation links are manageable.

The opening feels warm and confident. Stage photographs provide the emotional peak, and the closing reel/resume slip gives visitors a useful ending. Unexplained video loading interrupts that confidence; miniature contact text weakens the card's practical value.

**Persona checks**

- **Jordan, first-time visitor:** cannot tell what is happening during the blank video handoff.
- **Alex, time-constrained theatre maker:** can start the main reel quickly, but must scroll to find Seussical's promised recordings.
- **Casey, distracted phone visitor:** gets prominent homepage actions but has to squint at contact details.

**Detector reconciliation**

The scan emitted **five `broken-image` warnings across four files**: [CoverPrint.svelte:11](/Users/tunnel/Documents/Git/resume/website/src/lib/components/CoverPrint.svelte:11), [PhotoPrint.svelte:27](/Users/tunnel/Documents/Git/resume/website/src/lib/components/PhotoPrint.svelte:27), [homepage:33](/Users/tunnel/Documents/Git/resume/website/src/routes/+page.svelte:33) and line 46, and [About:41](/Users/tunnel/Documents/Git/resume/website/src/routes/about/+page.svelte:41).

**All five were false positives.** The scanner did not resolve Svelte's spread attributes; `responsive()` supplies real image sources, and browser checks confirmed they loaded. The detector added no verified defect. Its blank-player capture was also too brief to establish playback failure, so the video finding above concerns missing handoff feedback.

**Minor observations**

The footer's PGP and blog icons have accessible names but obscure visual meanings. This is secondary and does not obstruct the primary flow. About now contains Finn's writing; it is not an unfinished placeholder page. Missing PDF/PNG assets in the dev server were excluded because Nix supplies them in the assembled site.

**Questions to consider**

Could someone opening a production to hear Finn reach its recordings immediately? Can the contact card retain its physical character while its details remain comfortably readable on a phone?
