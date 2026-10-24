---
target: business card
total_score: 24
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 1
target_identity: "file:/Users/tunnel/Documents/Git/resume/website/src/lib/components/BusinessCard.svelte"
target_fingerprint: "sha256:280e92c710676b49262cc76f77f9fb6e9ffcbad48978d4e715beb5994c438f52"
target_path: /Users/tunnel/Documents/Git/resume/website/src/lib/components/BusinessCard.svelte
timestamp: 2026-10-24T05-37-10Z
slug: website-src-lib-components-businesscard-svelte
closed: true
---
Method: dual-agent (A: design review · B: detector + browser evidence), isolated and run in parallel.

## Finn's question: add a role line after the pronouns? Yes.

The front says who Finn is and how to reach them, never what they do. At the handover the room supplies that; a week later in a coat pocket nothing does, and the QR only helps someone already curious enough to scan. The card is also the one identity surface without a role: the artistic resume header (`metadata/metadata.toml:79`) and the site's social card (`website/scripts/gen_social_card.py:67`) both carry it.

Recommendation:
- Text: `musical theatre performer` (Finn's own phrase, lowercase, "theatre" spelling).
- Placement: own line directly under `they / them`, flush left with "Finn". Re-center the block (moves up about 5.5pt; margins stay legal).
- Type: identical to the pronoun line, 8pt PragmataPro in Program Ink (`scripts/business_cards.py:248`). 100pt wide, ends inside the right edge of "Rutis", about 30pt clear of the perforation.
- Not on the same line: `they / them · musical theatre performer` runs through the perforation at 8pt.
- Never a slash between roles: the pronoun line already uses ` / `.
- Voiceover: factual (REFERENCE.md, Fiverr VO since 2013) but left off this card; the QR lands on a site with no voiceover material. If wanted, stack `voiceover artist` as a third line (mock C) and add VO to the site first.
- `role` belongs under `[profiles.performance]`, not `[identity]`. Technology and Work stay without one until Finn writes theirs.
- Amend "No taglines" in `docs/business-cards.md:272` when decided.
- Real print render needs Sabon Next; `../blog/static/fonts/sabon/` is not on this machine.
- Mocks: scratchpad/assess-a/B-own-line-300.png (recommended), C-stacked-both-300.png, sheet-96.png.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Flip is announced ("QR back"), but the turn button's focus ring outlines the empty 736x518 stage, not the card, and nearly touches the h1 |
| 2 | Match System / Real World | 3 | Card skips the conventional title line; "Tap to flip" shown to mouse users |
| 3 | User Control and Freedom | 3 | Idle float never stops for keyboard focus |
| 4 | Consistency and Standards | 3 | Resume and social card name a role; the card doesn't |
| 5 | Error Prevention | 3 | Strong renderer/exporter checks; link hit areas are hard-coded artwork coordinates with no test against the PNG |
| 6 | Recognition Rather Than Recall | 2 | The holder has to remember what Finn does |
| 7 | Flexibility and Efficiency | n/a | A two-sided card with two links has no expert path |
| 8 | Aesthetic and Minimalist Design | 4 | Excellent restraint; minimal to a fault on one fact (scored under 6) |
| 9 | Error Recovery | 3 | Tilt errors plain and recoverable; no selectable address when mailto has no mail client |
| 10 | Help and Documentation | n/a | Nothing to document beyond the one-line instruction |
| **Total** | | **24/32** | **Good (75%)** |

## Design Specificity Verdict

**LLM assessment:** Visually unmistakably Finn's: Cooper playbill name with the indented rust surname, ticket-perforation rule, mono labels, rust QR, and a web card that behaves like uncoated stock in the hand. Semantically generic: swap the name and it could belong to a ceramicist. Nothing says theatre except a perforation most people won't read as a ticket tear. The role line fixes that without touching the look.

**Deterministic scan:** CLI on `BusinessCard.svelte` and `booking/+page.svelte`: 0 findings, but `.svelte` gets regex rules only (undercount). Rendered-page scan (1280px, 390px): 1 finding, `cream-palette` on `body` (`site.css:6`); false positive, the documented Playbill Paper token (DESIGN.md:7). The detector can't see text baked into the card PNGs; the forced-colors and pronoun issues came from pixel sampling and the accessibility tree.

**Visual overlays:** none. Chrome extension not connected; B used headless Chrome over CDP, so no `[Human]` tab.

## Overall Impression

A gorgeous, specific object that forgets to say what Finn does. Craft is high in print and web; the single biggest opportunity is the one Finn spotted.

## What's Working

1. Exact type system: 8pt mono x-height matches the 10pt Sabon contacts; the perforation sits centered between the end of "Rutis" and the icon column.
2. One artwork drives both surfaces: web front clipped from the approved PDF, paper texture in the renderer, exporter refuses to run if print text changes.
3. The web card holds up: WebGL on the real GPU, no console errors, no horizontal scroll at 390px, link targets at least 44px (97x48 on a phone), flat fallback flips under reduced motion.

## Priority Issues

1. **[P1] The front never says what Finn does.** Why: the card's job is recall days later. Fix: role line as above. Command: `/impeccable clarify`
2. **[P2] The email exists only as pixels and a mailto hotspot.** Why: card-only Contact page has no selectable address; webmail users get the Mail.app setup screen. Fix: one level, selectable address line under the card (Faded Ink mono, beside the instruction). Command: `/impeccable clarify`
3. **[P2] Dark forced-colors themes erase the card's ink.** Why: `.card-flat { background: Canvas }` (`BusinessCard.svelte:512`) puts #2b2520 lettering on black at about 1.3:1; the card is the only visible place for the contacts. Fix: `forced-color-adjust: none` on `.card-flat`, keep Ticket Stock background and CanvasText border. Command: `/impeccable harden`
4. **[P2] Screen readers never hear the pronouns.** Why: WebGL mode hides the image (`:427`); otherwise the button's `aria-label` (`:424`) replaces its alt. Fix: visually hidden figure description "Finn Rutis, they / them" (plus role once approved). Command: `/impeccable harden`
5. **[P2] The idle float never stops.** Why: ignores keyboard focus (`:77-78`) and loops forever; WCAG 2.2.2 risk. Fix: hold still while the card or its links have focus; settle after one 12s cycle until hover or touch wakes it. Command: `/impeccable animate`

## Persona Red Flags

- Casting director with a stack of cards: separated from the headshot, the card doesn't place Finn; card and resume disagree on what's worth saying.
- Sam (screen reader, keyboard): hears "Turn business card over, Drag to turnTap to flip, Contact front"; never hears "they / them"; card keeps floating while focused.
- Casey (phone): card 295 CSS px wide at 390px; pronoun/role lines around 9px; targets fine.
- Webmail user on a laptop: mailto opens an unused mail app; nothing to select and copy.

## Minor Observations

- "Drag to turn·Tap to flip": Svelte 5 trims the spaces in the separator span (`BusinessCard.svelte:446`); write `{' · '}`. "Tap" shown to mouse users; use "Click" for fine pointers.
- Print pronoun line is Program Ink, lowercase, untracked, departing from DESIGN.md's label rule; document as the card's exception.
- Resume says "&", social card says "and" for the same phrase.
- 1050px texture upsampled about 1.18x on 2x displays; a 600 DPI web export would be crisper.
- Contact no longer links to reel or resume in-page; nav still covers Principle 2.
- Physical-stock QR scan still pending.

## Questions to Consider

- When someone finds this card in a coat pocket, which word should they say out loud: "theatre" or "voice"?
- Should the Performance card send a voiceover producer to a site with no voiceover on it?
- Was "no taglines" protecting Finn from marketing copy, or from saying plainly what they do?

Run notes: Contact page changed mid-review (01:21 to 01:27, card-only with projected links; DESIGN.md updated to match); both passes reviewed the final state. Stale Impeccable live server from 2026-10-22 on :8400 (PID 38185) left as found.
