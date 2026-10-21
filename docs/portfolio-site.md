# Portfolio site implementation and validation handoff

The approved theatre-first scrapbook is implemented in `website/` with SvelteKit
and adapter-static. Phase 1's shared schema/calendar module stays at
`lib/shows.mjs`. This document describes implementation boundaries, not a claim
of passing builds, browser tests, deployment, or final font/media clearance.

## Local toolchain and output

Run from `website/`, using Node >=22.12 (the implementation environment reports
Node 24.16). Package versions and the npm lock are pinned. SvelteKit 2.55.0,
adapter-static 3.0.10, plugin-svelte 6.2.1, Svelte 5.57.2, Vite 7.3.1,
TypeScript 5.9.3, svelte-check 4.7.7, and smol-toml 1.9.1 are the selected
compatible family of versions. Newer major releases are not implicitly selected.

```sh
npm ci
npm run check
npm test
npm run build
npm run preview -- --host 127.0.0.1
```

`npm run check` includes SvelteKit type generation. There is deliberately no
install-time prepare/build hook. The implementation lane installed packages with
scripts/audit disabled and generated the lock; validation belongs to independent
fixers. Follow the repository's long-run helper/background validation instructions
for builds and test execution rather than treating these examples as permission
to broaden a lane's validation scope.

`SITE_BASE` defaults to the empty string for root/custom-domain hosting. For
repository Pages, build and preview with the same base:

```sh
env SITE_BASE=/resume npm run build
env SITE_BASE=/resume npm run preview -- --host 127.0.0.1
```

The five route files are `build/index.html`, `build/resume/index.html`,
`build/performance-reel/index.html`, `build/booking/index.html`, and
`build/resumes/index.html`. Under a repository mount their URLs begin with
`/resume`, so the theatre page is `/resume/resume/`. The base is a host mount,
not an extra directory to prepend inside the generated artifact.

The root layout declares `prerender = true` and `trailingSlash = 'always'`.
No SPA fallback is configured. `sitePath()` applies the configured base and
encodes each path segment, including the composite PDF's space. Local font URLs
use SvelteKit's `%sveltekit.assets%` substitution. Direct directory requests must
work on the eventual static host, not just through client navigation. Check both
slash spellings on the assigned Pages-like server. Unknown-path hosting behavior
is a separate host concern, not solved by an SPA shell.

## Shared content boundary

- `src/lib/server/content.js` imports canonical theatre and registry TOML as raw
  build inputs and calls `portfolioContent()` once at module initialization.
- `website/lib/content.mjs` uses the actual `smol-toml` parser, then invokes root
  `normalizeShows` once. It projects only validated fields into plain serialized
  objects. The browser never receives a filesystem reader or TOML parser.
- The homepage gets all normalized show records, not just resume-selected ones.
  `/resume` gets `selectResumeShows` in Finn's manual order, with no fabricated
  dates or static current/upcoming labels. The HTML section is theatre credits,
  not an invented complete transcription of all PDF sections.
- `/resumes` comes from `variants.toml`, excludes `site_hidden = true`, and uses
  the registry title/subtitle when present. Entries without a title use the
  existing destination stem as their functional label. No second variant list
  is maintained. The composite is a separate package/artifact, as before.
- `tests/ingestion.test.mjs` exercises the same real-parser boundary using the
  actual canonical files. It also covers native TOML dates versus required
  quoted date strings, multiline text, invalid types/chronology/fields/URLs,
  registry visibility/destinations, JSON projection, and base configuration.

The npm build needs the repository's adjacent `lib/shows.mjs`,
`metadata/theatre.toml`, and `variants.toml`. Vite aliases resolve them explicitly;
the dev server's filesystem allowance covers the site and those exact shared
inputs, not the whole parent repository. Phase 3 must widen the Nix input source
accordingly and update its dependency hash/output path. The old Nix website
package's website-only source and `dist` installation are not yet compatible.
No Nix or CI changes were made in the site lane.

## Current projects and browser fixture seam

`CurrentProjects.svelte` begins with an empty array, renders the whole section
only when nonempty, and calls `watchCurrentShows` inside Svelte `onMount`, returning
its cleanup. The shared helper alone determines eligibility, Eastern dates,
ordering, next-midnight timing, and tab-return refresh. Component code only
formats date labels in UTC to preserve date-only display; it contains no second
lifecycle implementation. Optional photos without supplied alternative text are
treated as decorative within the already-labeled production note. Supply useful
`photo_alt` in canonical data when the photo communicates more than that context.

`npm run dev:fixture` serves a separate Vite/Svelte harness rooted at
`tests/browser/`, not a production SvelteKit route. It mounts the real component
with normalized, clearly fictional test records. The production build never
imports this harness or its data. There is no shipped query parameter, debug
route, localStorage override, or fake canonical show.

The independent browser validator can install a browser clock at
`2026-10-21T16:00:00Z` before opening the harness, choose `single` or `overlap`,
and click Mount. Advance that clock through performance start, closing midnight,
and tab visibility return. Test `empty`, `incomplete`, unmount, and remount.
Unmount must clear timers/listeners; instrument the browser or mount the component
with its optional `watchOptions` prop to use the shared helper's injected clock,
timers, and visibility target. The harness's controls and fictional labels must
never appear in the production artifact. It has no Playwright dependency; the
validation owner chooses the browser runner and can add scoped tests later.

## PDF/preview assembly seam

The agreed destinations are `/resumes/<dest>.pdf`, `/resumes/<dest>.png`, and
`/resumes/FINN RUTIS.pdf`, with `SITE_BASE` applied by the browser link helper.
Phase 3 copies the real artifacts into `build/resumes/` alongside its index.
Building the portfolio alone does **not** create these documents or validate
that the files exist. Download links are ordinary static anchors marked
`rel="external"` to keep prerender crawling from treating not-yet-assembled
documents as Svelte routes. They are external to the app router, not a new tab.

The theatre preview is an image object with no-JS fallback links. Until Phase 3
assembly it may display its fallback and its destinations can return 404.
This is an explicit integration dependency, not a finished-download claim.
Verify every visible registry artifact and the encoded composite filename after
assembly; do not waive those checks because the five HTML pages build.

## Design, fonts, and media

The exact approved light tokens are in `src/styles/site.css`. No theme toggle or
system-dark rule is added. Desktop is portrait/name, then offset bio, independent
production notes, then a wide/tall/smaller photo spread. At narrow widths the
portrait comes before the name, the prints become unrotated and vertically
ordered, and links remain visible. Text never overlays a face. The supplied
rectangles retain their full proportions; no backgrounds are removed or cutouts
generated. A single backing entrance, fine-pointer photo-link lift, and optional
CSS scroll-linked backing drift are removed under reduced motion. Scrolling is
native. Essential content does not wait for JavaScript or visibility observers.

Production-note ticket links use the existing `--accent-hover` token even at
rest: its reported contrast on `--paper-shade` is 6.52:1, versus 4.43:1 for
`--accent`. No palette value changes. Underlines, thicker hover underlines and
the accent focus outline remain; paper-backed links retain their original colors.

Cooper* Black 900 is the name, Bold 700 is the other page titles. Local OFL faces
and LICENSE.md are supplied by the parallel media lane, not rewritten here.
Sabon Next and PragmataPro Mono Liga use the exact documented family names and
remote declarations in `src/styles/fonts.css`, with the blog fallback stacks.
No proprietary binary was downloaded or committed by this lane. Domain license
coverage and delivery/CORS remain unresolved final-delivery dependencies. These
declarations may trigger browser requests; they are not evidence of permission
or successful rendering. Do not deploy them before that permission is confirmed.
A fallback-only screenshot is not an exact-font approval.

`src/lib/media.js` selects three existing performance photos and keeps the three
verified reel IDs/titles/order. Each photo's optional `show` (a `theatre.toml` id)
and `blurb` (Finn's own words) become a note: on fine hover pointers the cursor
turns into a bubble showing it, and touch, no-JS and screen-reader visitors get
the same note as the figure caption. An unknown `show` id fails the build.
All seven images are preserved by the media lane.
The selected photo pixels were inspected for descriptive alt text; production
identifications and photographer credits were not guessed. `PhotoPrint` supports
caption/credit/creditUrl once supplied. No invented credit or public "credit
pending" filler is displayed. Confirm photo rights, final selection and credit
wording, portrait credit, video permissions and captions/transcripts before final
delivery. There is still no claim that the earlier fourth-video observation is
resolved, that CDN copies are camera originals, or that the media inventory is
complete. Embeds are user-played, no autoplay, with titled frames and static
direct YouTube links. No local video files were supplied.

## Independent verification still required

1. Install/check/ingestion tests and both root and `/resume` base builds. Confirm
   shared TOML inclusion and absence of Astro, fixtures, TOML parser, and server
   filesystem code in browser output. Check direct HTML routes under both bases.
2. Screenshot all five routes at 320, 390, 768, 1024 and 1440px, with actual
   rendered-font/network evidence. Inspect 200% text sizing, 400% zoom/reflow,
   large production titles, image proportions, focus visibility and no overflow.
3. Keyboard skip link/navigation/downloads, visible mobile navigation, tab order,
   link names, measured contrast, forced colors, reduced motion and normal scroll.
4. JavaScript disabled: exact bio, name, nav/footer, contact, HTML theatre credits,
   photo access, reel titles/direct links, and download anchors remain; no Current
   projects heading or stale lifecycle status. Check blocked player/image/font
   behavior. No-JS access does not establish that third-party video plays offline.
5. Fixture-driven single/multiple/empty/incomplete projects, rehearsal and
   performance transitions, inclusive closing, midnight removal, tab return,
   teardown, no duplicate timers, DOM order and layout shifts. Shared Phase 1 tests
   cover date math; these tests establish actual component wiring and presentation.
6. After Phase 3 assembly, verify real PDF/PNG responses and the composite, not
   just links. Font licensing, media credits and captions remain independent gates.

Designer owns the implementation and subsequent visual remediation. Independent
fixers own the assigned build/test/browser execution; the orchestrator owns the
phase gate, review and scoped commit. Nothing here authorizes pushes, deployment,
DNS/account changes, or Squarespace cancellation.
