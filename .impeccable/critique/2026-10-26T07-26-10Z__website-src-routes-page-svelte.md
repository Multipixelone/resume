---
target: homepage Watch me perform versus More performances beside the new video
total_score: 23
max_score: 28
na_heuristics: 5,7,10
p0_count: 0
p1_count: 0
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/routes/+page.svelte"
target_fingerprint: "sha256:bf616d39324d9f6470c4cf6bb04a708e1e2968ecf0e5a109d1676d4185efbe9f"
target_path: /Users/tunnel/Documents/Git/resume/website/src/routes/+page.svelte
timestamp: 2026-10-26T07-26-10Z
slug: website-src-routes-page-svelte
---
Method: dual-agent (A: /root/cta_design_review; B: /root/cta_detector_evidence)

Keep "Watch me perform", but make it jump to the featured homepage video.

Both links currently open /performance-reel/. The new clip gives them an opportunity to do different jobs:

| Action | Recommended destination |
|---|---|
| Watch me perform, in the hero | The featured clip at #start-here |
| More performances, beside the clip | The full performance reel |
| Reel, in the navigation | The full performance reel |

The video falls below the first screen at both inspected sizes. At 1470 x 779, the feature starts at document y818; at 390 x 844, it starts at y932. On phone, the hero action is available at y215, while the video poster starts at y1134. The existing #start-here anchor was tested on phone and brings the complete feature, including its links, into one viewport.

The page feels authored for Finn: the playbill name, headshot, programme caption and ticket-shaped Play control belong to the same callboard. Three things work particularly well: the hero offers the two casting tasks of watching and reviewing a resume; the featured clip makes a clear 1:15 commitment; and "More performances" is a natural continuation after that sample. The name and portrait introduce the person, then the performance supplies the next meaningful moment.

Priority issue, P2: the hero's watch invitation bypasses the homepage's chosen sample and repeats the collection destination. Keep its label and styling, point it to #start-here when data.startRecording exists, and retain the reel URL as the fallback. A downward arrow would clarify the in-page destination. Suggested command: $impeccable clarify. Relevant source: website/src/routes/+page.svelte:23 and :66; website/src/lib/components/Recording.svelte:106.

Nielsen scores are scoped to this watch path, not the whole website:

| # | Heuristic | Score | Evidence or limitation |
|---|---|---|---|
| 1 | System status | 3 | Clear destinations; player loading untested |
| 2 | Familiar language | 4 | Plain watch/resume labels and recognizable Play |
| 3 | User control | 3 | User-initiated playback and YouTube alternative |
| 4 | Consistency | 3 | Cohesive controls; repeated collection destination |
| 5 | Error prevention | n/a | No input or destructive action in scope |
| 6 | Recognition | 4 | Explicit actions and a selected starting clip |
| 7 | Expert efficiency | n/a | No expert controls needed for this portfolio path |
| 8 | Minimalist design | 3 | Strong hierarchy; watch routes could be differentiated |
| 9 | Error recovery | 3 | Source has preview fallback and YouTube link; failure untested |
| 10 | Documentation | n/a | This action requires no documentation |
| | Total | 23/28 | Good, 82% |

Cognitive load is low: 0/8 definite checklist failures. There are two hero actions and three clip actions. The header has four destinations plus the home logo, with no overloaded task-choice cluster observed.

For a first-time casting visitor, the current hero route adds a page transition before the same starting clip. For a phone visitor, the hero link supplies an early shortcut before the portrait and bio. For a keyboard or assistive-technology visitor, the source includes named links and player focus handling; a full accessibility audit was outside this review.

The deterministic scans returned zero findings in both the homepage and Recording.svelte. There were no false positives to resolve. The detector does not judge whether the two destinations should differ, so the navigation recommendation comes from the design review, confirmed by browser measurements and actual link navigation.

Minor polish: use a downward arrow for the proposed in-page link and keep playback user initiated. One priority issue was found; no broader visual redesign is warranted by this question.

Questions skipped: one priority issue; the requested decision is resolved by the recommendation above.
