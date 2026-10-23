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

The six route files are `build/index.html`, `build/about/index.html`,
`build/resume/index.html`, `build/performance-reel/index.html`,
`build/booking/index.html`, and `build/resumes/index.html`. Under a repository mount their URLs begin with
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
- `/resumes` comes from `variants.toml`, excludes `site_hidden = true`, and
  groups the rest under their `field`: the cv's field (theatre) first with the
  composite after the cv, then every other field in registry order. A listed
  entry without a `title` or `field` fails the build. Employer-tailored resumes
  and cover letters are `site_hidden`; their PDFs still ship, so direct links
  work. No second variant list is maintained. The composite is a separate
  package/artifact, as before.
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
formats date labels in UTC to preserve date-only display, and words the status
from the watcher's Eastern date (opening, closing, tonight); it contains no second
lifecycle implementation.

The section is a compact playbill notice under a light rule. A single show gets
the singular "Current project" label; several become ruled listings under
"Current projects". Titles stay smaller than the next section heading. Each
show's opening date sits on a landscape ticket with a vertical "Admit one" rail,
a small paper tear, an optional "Livestream available" line under the run, and
an optional "Get tickets" band below the date. When a
booking URL exists, the whole stub is one native link with a visible hover and
keyboard focus treatment. Stubs without a URL stay non-interactive. The header ticket
shares its stock and tear. The layout stacks below 768px, with the same readable
ticket labels for single and multiple shows. A role of `Self` is
left out, since it tells a visitor nothing. Optional photos without supplied
alternative text are treated as decorative within the already-labeled show.
Supply useful `photo_alt` in canonical data when the photo communicates more.

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
assembly; do not waive those checks because the six HTML pages build.

## Design, fonts, and media

The exact approved light tokens are in `src/styles/site.css`. No theme toggle or
system-dark rule is added. The homepage pairs a large Cooper Black name with a
portrait and an overlapping Seussical print. The portrait has a printed bottom
strip with Finn's name in Cooper Black and smaller Pragmata pronouns on the same
left-aligned line, flush with the photograph's left edge. The photograph and name
strip move together as one printed headshot. Its tan backing stays fixed. The
Seussical print hinges above the label while its tape travels with the headshot. The bio and reel/contact links sit
under the name. Production photos use varied sizes, borders and resting angles,
with one shared angular paper shape behind the first group. Show titles and roles
stay visible in fixed captions. At narrow widths the name leads, the portrait
pair follows, and the performance photos become a single column with varied
widths. Text never overlays a face. Photos retain their full proportions; no
backgrounds are removed or cutouts generated.

`src/lib/motion.ts` supplies the `callboardEntrance`, `printEntrance`, and
`paperMotion` actions.
The homepage has one opening gesture: the backing seats, the headshot is laid
down with a contracting shadow, and the taped Seussical print catches and settles.
The sequence finishes within 780ms, with all content visible throughout. The
headshot, tape and small photo share one pointer transform so their attachment
stays intact. The small print swings around its tape on pointer entry or keyboard
focus, with no cursor-follow twist of its own. Touch follows its photo-spread link.

Fine-pointer movement gives photos a bounded tilt and translation, with one
animation frame queued for pointer work and no idle render loop. CSS adds a
lift/straighten response on hover or keyboard focus. Gallery captions and page
headings stay fixed. Gallery prints land corner-first once they enter view, then
flatten into their resting angles over 740ms (580ms with a smaller gesture on
phones and coarse pointers). A prepainted contact shadow fades with opacity;
the landing itself uses transforms, without a scroll listener or per-frame
shadow painting. Photos remain visible before, during, and after the entrance.
Supporting-page photos stay still, and the broad backing paper has no parallax.
Navigation slips respond to keyboard focus as well as hover. The ticket's rust end flexes around its perforation while
the whole ticket remains one link.

The gallery uses three physical fastenings: translucent torn tape on the wide
and small prints, a photographic rust pushpin on the tall print, and two folded corners on
the tall-left print's backing card. A shared resting wrapper keeps each
attachment fixed while the paper flexes at its grip. Taped prints hinge from
their top edge; the pinned print also pivots under its tack. The corner-mounted
print stays flat, and the two loose prints keep their lift and pointer follow.
These decorations do not intercept pointer events or enter the accessibility
tree, and forced colors hides them.
The pushpin is a transparent PNG derived from a public-domain photograph in
`static/decorations/`, served through `sitePath()` and anchored by its base.
The 20px-wide near-axis view hides the grip behind the cap and has no visible
needle. The source photograph and color, background, and viewpoint edits are
documented in `docs/portfolio-media.md`.

Reduced motion cancels active opening, tape, and gallery animations, clears pointer
offsets, and disables spatial feedback. Static color and focus states remain.
Focus or a pointer press settles an arriving gallery print immediately; prints
scrolled past also settle and never replay on return. Hidden tabs settle
immediately; observers, listeners, frames and animations are cleaned up on
navigation. Scrolling remains native; all essential content works without JavaScript.

Current-project ticket actions use `--accent-hover` on `--selection-bg`, changing
to light text on `--accent-hover` when hovered or focused. The weekday and year
on the stub also use `--accent-hover`. The link wraps the cut paper so its
keyboard focus outline stays visible around the entire ticket.

Cooper* Black 900 is the name, Bold 700 is the other page titles. Local OFL faces
and LICENSE.md are supplied by the parallel media lane, not rewritten here.
Sabon Next and PragmataPro Mono Liga use the exact documented family names and
remote declarations in `src/styles/fonts.css`, with the blog fallback stacks.
No proprietary binary was downloaded or committed by this lane. Domain license
coverage and delivery/CORS remain unresolved final-delivery dependencies. These
declarations may trigger browser requests; they are not evidence of permission
or successful rendering. Do not deploy them before that permission is confirmed.
A fallback-only screenshot is not an exact-font approval.

`src/lib/media.js` selects six existing performance photos and keeps the three
verified reel IDs/titles/order. Each photo's optional `show` (a `theatre.toml` id)
and `blurb` (Finn's own words) become a fixed figure caption for pointer, touch,
no-JS and screen-reader visitors alike. An unknown `show` id fails the build.
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
2. Screenshot all six routes at 320, 390, 768, 1024 and 1440px, with actual
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
