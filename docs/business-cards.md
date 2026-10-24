# Business cards: implementation and approval history

## Current status (2026-10-23)

The user approved the latest tweaked Performance front/back proof and explicitly
authorized the full three-profile generator and separate build. A subsequent
request authorized the Contact page's 3D Performance card, including mobile
device tilt (see below). The separate sans-serif print test remains deferred. The earlier
proof-only approval boundary below records the historical decision, not the
current scope. Original proofs and local font assets remain user-owned.

Build integration now provides `packages/business-cards.nix`, the
`business-cards` flake package/app, explicit registry associations, and a
font-independent registry validator. The designer owns the renderer,
`cards/profiles.toml`, rendering tests, and card assets. The finalized renderer
passed 27 unit tests, and the packaged runtime successfully rendered all three
profiles to `/tmp/opencode/business-cards`. Structural and independent artifact
checks passed for all 24 files. The final visual observer returned SHIP with no
blockers: consistent identity and contacts, balanced Technology and Work fronts,
and no collisions. This is not press certification; a physical-stock scan remains
outstanding.

### Runnable separate build

From the repository checkout:

```bash
nix run "path:$PWD#business-cards" -- --root "$PWD" --output /tmp/business-cards --sabon "../blog/static/fonts/sabon/Sabon Next Regular.woff2"
# Equivalent convenience recipe:
just business-cards "../blog/static/fonts/sabon/Sabon Next Regular.woff2"
```

`nix build "path:$PWD#business-cards"` builds the CLI environment, not card artifacts. The
app runs the renderer against the explicit local checkout after the sandboxed
tool build. This permits the external, proprietary Sabon file to be supplied at
runtime without hidden environment reads, sandbox exceptions, a repository copy,
or a font substitution. Relative font/output paths are relative to the invoking
directory. The caller must have authorization to use and embed Sabon; the tool
does not certify licensing. Do not add the font to Nix inputs or this repository.

The explicit `path:` reference includes new, untracked integration files without
staging. A Git-backed `.#business-cards` reference omits untracked package/checker
files and works only after those required files are tracked. `path:` snapshots
untracked files too, so use a trusted checkout and keep proprietary Sabon outside
the repository as required above.

The Python environment declares ReportLab, PyMuPDF, Pillow, fontTools, Brotli
(WOFF2 decoding), and zxing-cpp. Nix MCP was unavailable in this session; the
pinned package attributes and runtime build were successfully validated using
the local Nix CLI instead.
No resume/site package depends on this CLI or on Sabon.

The agreed renderer interface is:

```bash
python scripts/business_cards.py --root PATH --output DIR --sabon FONT_PATH
```

`cards/profiles.toml` defines `[profiles.performance]`, `[profiles.technology]`,
and `[profiles.work]`. Each profile is emitted once, to
`performance/performance.pdf`, `technology/technology.pdf`, and `work/work.pdf`,
with front/back transparent ink, preview, actual-size PNGs, and a `validation.json`
per profile. The registry associates resumes with these shared outputs, not new
copies. PDF page order is front then back. Existing resume inventory is unchanged.

### Registry decisions and checks

Every registry entry requires `card_profile`: `performance`, `technology`,
`work`, or `none`. Performance covers the artistic CV and FAO performer role.
Work covers hospitality, childcare, front-of-house, general onsite events, and
both Anthropic live-event roles (including event narrative/run-of-show content).
Technology covers software, systems, DevRel, technical communication, product
video/education, and digital content. Metadata was inspected rather than using
employer names: product/social communications and product video are Technology,
while the live-event production and event-content offers are Work.

The user explicitly resolved the ambiguous Vox editorial video, SoFi
podcasts/video strategy, and NYT camera/network support variants as Technology
during integration. This extends the initial tech-product video wording to
editorial digital/video and video systems support without introducing a fourth
profile. Exact assignments live only in `variants.toml`.

Letters, repertory sheets, and title pages use `none`. The existing
`check_metadata = false` supporting-document classification is checked against
that exclusion; metadata-checked resumes cannot silently opt out. The validator
rejects missing/unknown associations and any profile set other than the three
agreed names. Its grouped result deduplicates by profile.

```bash
python scripts/check_card_profiles.py --root .
python -m pytest tests/test_card_profiles.py
nix build "path:$PWD#checks.x86_64-linux.card-profiles"
```

The flake registry check requires no fonts or renderer dependencies. Validation
confirmed the pinned runtime build, 14 registry tests, 27 renderer tests, and the
explicit-font render command. All three two-page PDFs passed front/back order,
270 x 162-point media/bleed boxes, 252 x 144-point trim, embedded-font, and
unprinted-background checks. Ink PNGs are RGBA at 1050 x 600 / 300 DPI; cream
previews are RGB at that size, and actual-size proxies are RGB at 336 x 192 /
96 DPI. Technology contains no phone number. All backs were then pixel-identical,
and their QR codes decode to `https://finnrut.is` at both resolutions.

After the 2026-10-24 back redraw (see Approved content), all three profiles
again passed the full render's structural, safe-area and digital QR checks. That
local run substituted Sabon Next LT, which lacks small caps, for the unchanged
fronts, so a render with the licensed Sabon Next remains the print source.
Minimum visible-ink margins on the backs are 0.25 inches for Performance (the
headshot) and 0.4133 inches for Technology and Work. Across 648 simulated camera
captures (size, blur, fading, tilt, JPEG and rotation), zxing decoded the new
backs about as often as the old one: 332 (Performance) and 328 (Technology)
against 336.

Measured minimum visible-ink margins (front/back) are 0.2567 / 0.3733 inches for
Performance and 0.2533 / 0.3733 inches for Technology and Work. All six Performance
PNG exports match the current approved proof exports pixel-for-pixel, with zero
different pixels; no proof rerender or geometry change was needed. Detailed
temporary evidence is `/tmp/opencode/business-cards-audit.json`, alongside the
per-profile `validation.json` files. Temporary evidence is not a durable archive.

Digital QR checks do not prove scanning on the chosen physical stock. Exports
remain subject to printer specifications, with no PDF/X, CMYK, licensing, or
press-ready certification.

## Contact-page rendering

The `/booking/` page displays a web edition of the approved Performance card.
At the user's request, the web front and contact actions omit the phone number;
the printable card retains it. The page remains
focused on theatre; Technology and Work are not selectors on this surface.
The card leads a single column. Its printed email and Instagram are native HTML
links, with rust underlines, keyboard focus, and normal browser link actions.
The former contact column and separate action row repeated the artwork's
details, so both were removed. Reel and resume stay in the main navigation.
The print generator and its proprietary font inputs are not website
build dependencies.

`website/static/cards/performance/front-web-ink.png` and `back-ink.png` are
transparent, trim-sized 1050 x 600 images derived from the approved PDF. The web
front omits the phone row and recenters email and Instagram using the original
vector lettering and icons. The identity, perforation, rust QR, and quiet zone
are preserved. The former phone-bearing `front-ink.png` is not shipped. Their
initial source was the user-owned
`business-cards/performance/performance-proof.pdf`, SHA-256
`306119b4698fdfd3a9ed49fe24bfdab1d8c50085e1ccf616e4c26aee040a1ea6`.
The source PDF is not changed or bundled into the website. Since the 2026-10-24
redraw, `back-ink.png` comes from the generated `performance.pdf` and carries the
headshot. That makes it about 360 KB (lossy WebP smeared the QR edges and the
face), so the component fetches it at low priority, behind the visible front.

To refresh the site artwork from an approved generator output, using Python with
PyMuPDF installed:

```sh
python website/scripts/export_business_card.py --pdf /tmp/business-cards/performance/performance.pdf
```

The exporter checks the Performance print contact text and trim geometry before
creating the phone-free web front and unchanged back. Review artwork changes
before replacing these snapshots.
Committed static textures work in both Vite and the Nix site build without a new
parent-directory filesystem allowance or Sabon dependency.

`BusinessCard.svelte` owns progressive enhancement, input, and lifecycle.
`business-card/scene.ts` is a dynamically imported Three.js scene: square stock
with a thin cut edge, a slight bow, fine pulp grain and fibers, warm diffuse light,
and a soft projected shadow. The matte Lambert material has no specular highlights;
the grain remains subtly visible in flat light, with mipmapped relief to avoid
shimmer during movement. The paper color, grain and lighting are material
properties, not changes to the exported ink. The stock uses the lighter Ticket
Stock color, with a warmer cut edge. A shallow resting tilt and a distant
perspective camera keep the near corner from appearing enlarged.
The flat image is present in the
prerendered HTML and stays available if WebGL or the module fails. A native button
behind the contact links turns the card: Enter and Space work without a separate
visible control. Pointer dragging snaps to a readable front or back, and a tap
on the blank card flips it. A contact tap follows its link; a drag beginning on
a contact turns the card and suppresses navigation.

`business-card/links.js` maps the artwork's coordinates through the same camera
and canvas bounds as the rendered card. The anchors and their underlines follow
that CSS projection without duplicating the printed text. They hide on the back
and near the edge, and their targets stay at least 44px tall. The two target
areas meet between the printed rows, so phone targets cannot overlap. Without
JavaScript, WebGL, or motion, the same anchors sit over the flat artwork using
CSS alone. The button and links are siblings, not nested interactive elements.

A gentle six-second vertical float shares a phase with a twelve-second
figure-eight tilt. The tilt adds about 3 degrees of yaw, 1.5 degrees of pitch
and a slight bank, keeping the face readable. A separate spring blends the
idle tilt out for hover, dragging, flips and device tilt, then restores it
gradually. Holding the card freezes the phase so release has no jump.
The broad, offset shadow softens and lightens as the card rises and fades as the
card turns edge-on. The canvas extends beyond the stage on all sides, with
horizontal bleed bounded by the viewport to prevent scrolling. The camera
matches those bounds so the card keeps its size, position and pointer bounds.

On touch devices, **Use device tilt** explicitly enables relative device
orientation. iOS-style permission is requested directly from that tap, without
requesting absolute compass orientation. The first valid sample calibrates the
hand's neutral position; portrait/landscape changes recalibrate. Angles are
bounded, spring-smoothed, and ignore small sensor jitter. Denied permission,
missing data, or unavailable sensors leave the ordinary controls usable. Device
orientation requires a secure context: HTTPS in production or localhost when
testing. A phone visiting a plain-HTTP LAN development address will not offer it.

Reduced motion and forced colors use a still card with instantaneous front/back
changes. The scene initializes only in view and uses at most 2x pixel density.
The idle float renders at 30fps; input and settling use the full display rate.
Hidden/offscreen cards stop frames and detach sensor listeners. Navigation
disposes GPU resources and listeners.
The mathematical tests cover spring convergence, side selection, device angle
wrapping, calibration, landscape axis mapping, contact projection through
resizes and canvas bleed, and hiding front links during a turn. A real phone is still needed
to assess the physical sensor feel and its native permission prompt.

Implementation references: [Three.js on-demand rendering](https://threejs.org/manual/pages/rendering-on-demand.html),
[diffuse paper material](https://threejs.org/docs/pages/MeshLambertMaterial.html),
and [device orientation](https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent).

## Historical proof-only handoff

The following records the original interview and proof gate. Current scope and
implementation status above supersede its deferral instructions.

## Status and approval boundary

Shared understanding is confirmed and the design interview is complete. The user
will begin Impeccable generation in a new context window. Generation is deliberately
deferred: this session is documentation only. No successful generation was
delivered in this session; this is not an independent audit of filesystem changes
from the earlier unsuccessful attempt.

The first authorized **next-session scope is a Performance front/back design proof
at actual size only**. Obtain explicit user approval before applying the design to
Technology or Work or finishing generator integration. Agreement on this brief is
not approval of a final layout or authorization for full implementation now.

Terms follow [CONTEXT.md](../CONTEXT.md), which remains unchanged. No ADR is needed:
no hard-to-reverse implementation tradeoff has been chosen.

## Sources of truth

- [AGENTS.md](../AGENTS.md): repository instructions and content guardrails.
- [REFERENCE.md](../REFERENCE.md): biographical and contact facts. Do not invent
  copy, credentials, taglines, or contact details.
- [variants.toml](../variants.toml): the sole resume variant registry. Do not
  maintain a second variant list in the card system.
- [DESIGN.md](../DESIGN.md): written Callboard design language. There is no
  existing business card to reproduce.
- [CONTEXT.md](../CONTEXT.md): resume variant, card profile, and business card
  glossary. Multiple resume variants may share a card profile.

## Profiles and audience mapping

There are three shared card profiles, not a card for each resume:

| Internal profile | Work offered |
| --- | --- |
| Performance | Acting and musical theatre |
| Technology | Software, developer education, and digital/video work for tech products |
| Work | Live events, onsite production, hospitality, and childcare |

Assign profiles explicitly by the work offered, not the employer. A tech-company
video role uses Technology; a live-event producer role at that company uses Work.
Employer-specific resumes inherit the suitable shared profile. Letters and
supporting documents do not generate extra cards.

Exact variant assignments belong to later integration and must be checked against
this rule and the registry. Escalate genuine exceptions rather than guessing from
the employer or title alone. Emit only three unique profiles, with no duplicate
per-variant or per-employer output and no new fourth profile.

## Approved content

These values were checked against the Personal section of REFERENCE.md. All fronts
carry **Finn Rutis** and **they / them**.

| Front | Role | Email | Phone | Social |
| --- | --- | --- | --- | --- |
| Performance | `musical theatre performer` | `me@finnrut.is` | `503-267-5052` | Instagram `@finnrutis` |
| Technology | None | `tech@finnrut.is` | None | GitHub `Multipixelone` |
| Work | None | `work@finnrut.is` | `503-267-5052` | None |

Profile names are internal only, not printed audience labels. On 2026-10-24 Finn
approved an optional per-profile `role` line: Finn's own words for what they do,
set directly under the name. A role is a category, not a tagline. Performance
uses "musical theatre performer" (voiceover was left off because the site has no
voiceover material). Technology and Work have no role until Finn writes one. No
taglines or extra social fields are approved. Typography and label treatment must
not introduce new content.

The same day, Finn asked for the role and pronoun lines to be redrawn; the first
treatment was a 10pt Sabon italic role over 8pt PragmataPro pronouns. The role is
now Sabon Next's true small caps at 8pt in Program Ink, letterspaced to run from
the left edge of "Finn" to the last ink of "Rutis" (about 0.1em on Performance).
Spacing stays between 0.04em and 0.14em; a role too long for that fails the
render, and a short one ends early. On every profile the pronouns follow in 8.5pt
Sabon Next italic, Faded Ink, on the same margin, so the name keeps its column and
perforation and only the block's vertical centre moves. PragmataPro remains on
the back for the website address. The renderer remaps a-z to the regular file's
`.sc` glyphs in memory and renames that face, because ReportLab merges fonts that
share a face name. It reads `Sabon Next Italic.woff2` beside the supplied
`--sabon` file.

All profiles share the back's code: a rust QR to `https://finnrut.is`, captioned
by the human-readable website address. REFERENCE.md records `www.finnrut.is`; the
intended QR destination is the confirmed HTTPS root above.

On 2026-10-24 Finn asked for the address closer to the code and for a headshot
on the back, and chose Performance only. The address's tallest ink now sits two
modules under the code (the source PNG's own quiet zone) instead of four; the
other three sides keep four. The Performance back adds `src/headshot.jpg`, the
composite resume's headshot, as a 4:5 print (a theatre 8x10) at the full safe
height: 1.2 x 1.5 inches, standing at the 0.25-inch margins and embedded as a
600 ppi JPEG. The code centres between the print and the card's right edge.
Technology and Work keep the centred code. The headshot is an optional
per-profile `headshot` path in `cards/profiles.toml`; the renderer trims the
sides evenly, keeps the top, and fails under 300 ppi.

## Physical format and material

- 3.5 x 2 inches at trim, landscape, square corners, two-sided.
- Warm, uncoated physical stock supplies the paper color. The print artwork
  background is unprinted, not a cream rectangle.
- Cream backgrounds belong only to preview images. Transparent artwork carries
  the ink without a paper-color fill.
- No faux paper textures, baked-in shadows, or perspective in the artwork.
- First pass: printable cards and flat image exports. Contact-page rendering,
  website publication/download wiring, and 3D paper material remain deferred.

## Visual direction and font decisions

Use a consistent identity across the three profiles, following the written
Callboard language: warm paper, dark ink, and rust. The actual-size Performance
proof must establish the layout before it is reused elsewhere.

- **Cooper:** name.
- **Sabon Next:** contact text, the site's body face. The user chose it over the
  provisional EB Garamond on 2026-10-23.
- **PragmataPro:** restrained labels. The user explicitly authorizes its use;
  this is user-confirmed permission, not independently documented license
  clearance. Profile names remain internal even when labels are used.

The designer's asymmetric, left-led front and ticket-divider treatment are
**advisory, not an approved layout**. Placement, hierarchy, exact sizes, and
readable safe margins are for the designer to propose in the proof. Do not treat
website decoration as a requirement to print simulated paper effects.

The user plans a separate future print test to choose a sans-serif. That test is
out of scope.

### Font evidence and remaining checks

- Local Cooper OFL assets are in `website/scripts/fonts/cooper` and the static
  equivalent under `website/static/fonts/cooper`. Inspect the relevant files and
  license when preparing the proof.
- A PragmataPro file is in `src/fonts`; use is user-authorized as noted above.
- Sabon Next (Linotype, proprietary) is gitignored in the sibling blog checkout at
  `../blog/static/fonts/sabon/`; do not copy it into this repository. Its
  embedding flag allows print and preview embedding. Use is user-directed, not
  independently documented license clearance. Garamond Premier permissions have
  not been established.
- An earlier online Nix lookup failed because of DNS. That is not evidence of a
  license failure.

## QR requirements and evidence

The existing asset is `metadata/qr-code.png`. Its destination is **user-confirmed**
as the intended website, not independently machine-decoded evidence.

Use rust for the QR. Preserve the module pattern and quiet zone when recoloring;
do not distort it or let decoration intrude. Validate the recolored QR at actual
size before final approval. Existing destination confirmation does not establish
that the new rust rendering will scan reliably on the chosen stock. At Finn's
request the website address keeps two modules clear under the code rather than
four; the other three sides keep four.

## Agreed working export defaults

These are working defaults accepted with the shared understanding, subject to
the eventual printer's specifications. They are not certification of press-ready,
PDF/X, or CMYK production compliance.

- Printer-ready PDF target: two pages, front then back, with 3.5 x 2-inch trim and
  1/8-inch bleed on each edge. No crop marks and no home-print sheets.
- Use readable safe text margins. No exact safe-margin measurement has been
  approved; the designer must choose and demonstrate it at actual size.
- PNGs: 300 DPI, flat, trim-sized (3.5 x 2 inches), with no bleed or crop marks.
- Export separate front and back PNGs in both forms: cream-backed previews and
  transparent ink artwork. These support the eventual contact-page/3D render;
  neither future feature is part of this scope.
- The PDF and transparent artwork must not bake in the preview cream background.

## Build and repository context for later integration

A **separate card build** is requested, but not implemented. No command name,
file schema, generator structure, or publication mechanism has been settled.
Do not turn these context pointers into integration work before proof approval.

- `packages/resume.nix`: registry-driven resume PDF and first-page PNG pipeline.
- `src/meta.typ`: `makeMeta` metadata merge.
- `src/lib.typ`: shared layouts.
- `src/cv.typ`: shared components.
- `metadata/metadata.toml` and variant overrides: existing contact metadata.
  REFERENCE.md remains the fact-checking authority.
- Website `/booking/`: relevant existing route to inspect only if later scope
  calls for it; no website publication is authorized here.
- `packages/website.nix` source filter and `website/vite.config.js` filesystem
  allowlist: shared inputs require explicit inclusion if website integration is
  later authorized. Consult AGENTS.md before changing those boundaries.

The card build should eventually emit the three unique profiles, not copies per
resume. Exact mapping and build checks follow later, after the proof gate.

## Future validation and approval sequence

1. Produce the Performance front/back proof only. Have an observer inspect both
   artifacts at actual size, including readability, hierarchy, safe margins, and
   the absence of unapproved labels or copy.
2. Check all text against REFERENCE.md and the approved fields above. Confirm no
   phone leaks onto Technology when that profile is eventually authorized.
3. Check PDF page order/count, trim dimensions, bleed, lack of crop marks, and
   embedded fonts. Check PNG resolution, trim-sized dimensions, cream previews,
   and transparent-artwork alpha.
4. Test the rust QR at actual size with its quiet zone intact. A physical scan on
   the actual stock may require the user's help; report that limitation rather
   than claiming a digital preview proves print reliability.
5. Obtain explicit user approval of the Performance proof before adapting the
   other profiles or finishing generator integration.
6. Later, validate explicit registry-to-profile assignments, deduplication, and
   the separate build. Website wiring remains a separately deferred task.

For any long Linux build or test, delegate to a background fixer and load the
`agent-run-long` skill before using its helper. Follow the skill's timeout and
reporting requirements. If delegation is unavailable, report that limitation.

## Next session: start here

1. Load the Impeccable skill available in that session. Read AGENTS.md (and any
   applicable CLAUDE.md), REFERENCE.md, variants.toml, DESIGN.md, this brief, and
   CONTEXT.md before work.
2. Delegate visual proof work to the designer. Start with Performance only, at
   actual size, using the confirmed content, material, fonts, and QR direction.
3. Preserve the explicit proof approval gate. Do not expand into other profiles,
   full generator integration, website wiring, 3D material, or the separate
   sans-serif print test before the required approval and scope authorization.
