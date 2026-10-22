# Ballpoint doodles: design handoff

This is a plan for adding hand-drawn doodles to finnrut.is. It was written 2026-10-21, before any drawings existed, and nothing in `website/` has changed for it yet. A friend of Finn's (called "the artist" here) draws everything by hand. This doc covers what to ask them for, how their drawings get onto the site, and where each one goes.

Read `docs/portfolio-site.md` first. Its design and accessibility rules still apply, and this adds a layer on top of them.

## The idea

The look is blue ballpoint line art with a Y2K, Nintendo DS feel: one pen, a thin and slightly wobbly line, plain paper. It's the kind of thing that ends up in the margins of a school notebook.

The site is already a scrapbook: photo prints with mats and resting angles, torn ticket stubs, paper slips for the nav, all set in Cooper Black. The doodles are the next layer of that scrapbook, as if a friend in the house seats doodled all over your playbill, or an actor marked up their script. That gives two sources of subject matter:

- **Notebook doodles**: stars, sparkles, loopy arrows, underlines, circled words, spirals, paper airplanes.
- **Theatre markings**: blocking arrows and Xs, spike tape marks, breath marks and fermatas, a follow spot, the ghost light, a stick figure taking a bow.

The doodles **annotate**. Each one points at, circles, underlines or reacts to something already on the page. They aren't wallpaper or a repeating background pattern.

These references are for mood only. Don't copy their UI, characters or assets:

- PictoChat (DS, 2004): a faint ruled drawing area and one thin pen.
- Flipnote Studio (DSi, 2008): black, red and blue ink only, with frames that jitter like a flipbook.
- Line Rider: a single blue line on white paper.

## Hard rules

1. **Hand-drawn only.** Every doodle on the site is a scan of ink the artist put on paper. That rules out AI-generated images, AI upscaling, AI cleanup or inpainting, and doodle look-alikes drawn in SVG or CSS as stand-ins. Processing stays mechanical: crop, levels, alpha extraction, resize, and, if it's ever needed, a bitmap trace of an existing scan. If a drawing doesn't exist yet, its slot stays empty or shows a labelled placeholder box during development, and that box never ships.
2. **One ink.** The whole set uses the same blue ballpoint pen and renders on the site in a single color token.
3. **Decorative only.** A doodle never carries information and is hidden from assistive tech. It never covers a face, never covers or underlines body text, and never changes a link's hit area.
4. **Restraint.** Keep two or three doodles in view at once on desktop, and one or two on a phone. Not every photo gets one. The header ticket and the nav stay clean.
5. **Ink has no shadow.** Prints and tickets cast shadows, but ink drawn on them doesn't.

## Part 1: Brief for the artist

This section can go to the artist as it is. Have a look at finnrut.is first to get a feel for the site.

### Materials

- **Pen:** a blue Bic Cristal with a medium point. Use one pen for everything so the line and color match across drawings.
- **Paper:** plain white printer paper or smooth bristol. Avoid lined notebook paper, because the printed lines get scanned in and are hard to remove. The site adds notebook lines itself where it wants them.
- **No pencil sketch first.** Graphite shows up in the scan, and going straight to pen is the point anyway. Wobbles, scribbled-out mistakes and pen skips are all welcome. Don't use white-out.
- **Words:** if an item has words, write them in your normal handwriting. Lowercase is fine.

### Size

Draw at the size you'd doodle in a margin. **1 mm on paper is about 5 px on screen.** At that scale the ballpoint line comes out around 2 px, which is about the weight of the site's existing icons. Something drawn much bigger and then shrunk ends up with a hairline-thin line, and something drawn smaller and enlarged gets chunky. Sizes are listed for each item, and being within 20% either way is fine.

### Takes, spacing and boil frames

- Draw **2 or 3 takes** of each item. Finn and the design pass will pick the best.
- Leave **at least 2 cm** of blank paper between drawings. Write the item ID (like `A4`) in a corner of the sheet, well away from the drawings.
- Items marked **boil** need three matching frames. Draw it once, tape a fresh sheet over it on a bright window, and trace it twice. The three frames will cycle on the site like a Flipnote, so they should line up without matching exactly.

### Scanning

- Use a flatbed scanner at **600 dpi in color**, with every auto-enhance or "document" filter turned off. Save as **PNG or TIFF**, not JPEG.
- Without a scanner, a phone scan works: daylight, paper flat, camera straight overhead, no filters, highest quality. A flatbed is much better, though.
- Keep the originals. They're yours.

### The drawing list

Set A is the homepage and the priority. Set B covers the other pages. Set C is spares, which give the design pass room to compose.

| ID | Drawing | Size on paper | Where it goes |
|---|---|---|---|
| A1 | Underline: a fast, wobbly double underline, and the ends can overshoot. **Three lengths.** | 10 cm, 5 cm, 3 cm long | Under "Rutis" in the big name, one length per screen size |
| A2 | Sparkle: 3 to 5 little shine ticks, like a cartoon gleam. **boil** | 2.5 cm | Off a corner of the name or the headshot |
| A3 | Loopy arrow with "me!" written along it (the words are optional) | 6 cm | Pointing at the headshot |
| A4 | Circle: a quick loop that doesn't quite close, like circling a date on a calendar | 4 x 2 cm | Around the opening date on the ticket stub |
| A5 | Spotlight: a follow spot with a cone of light coming out of it (an outline plus a few hatch lines) | 4 x 6 cm | Shining down onto a photo in the "On stage." spread |
| A6 | Blocking notes: an X with an arrow, a curved arrow, and "X DSR" written small | 5 cm | In the gaps between photos |
| A7 | Spike marks: a few small T and X marks, like tape on a stage floor | 1.5 cm each | On the paper behind the photos |
| A8 | Star: the one-stroke kind. **Two sizes.** | 1 cm and 2 cm | Next to one or two show titles |
| A9 | Stick figure taking a bow. **boil** | 2 cm tall | Standing on the footer line, on every page |
| B1 | Two eighth notes, a fermata (the bird's eye) and a breath mark | 4 cm | Performance reel page heading |
| B2 | Paper airplane with a dotted loop-de-loop flight path | 8 cm path | Contact page, flying toward the email address |
| B3 | Ghost light: a bare bulb on a stand with a few glow lines. **boil** | 4 x 8 cm | The "page not found" page |
| B4 | Margin bracket: a curly brace with "(read this)" or "!!" | 3 x 6 cm | About page, beside the artist statement |
| B5 | Paperclip | 3 cm | About page, clipping a note |
| B6 | Small arrow with "this one" | 4 cm | Resume page, next to "Download resume" |
| C1 | Arrows: straight, curved and loopy, both short and long | 2 to 6 cm | Spares for composing |
| C2 | Fillers: a spiral, a loop-de-loop, "!!", a tiny smiley, a few dots | 1 to 3 cm | Spares |
| C3 | Two strips of drawn tape (a rectangle with ragged ends and a few hatch lines) | 3 x 1 cm | Spares, for the corners of a print |
| C4 | Anything else that feels like Finn | any | Artist's choice |

Please don't draw show logos or characters from licensed shows. Draw theatre in general instead.

## Part 2: For the design pass

### Where files live

| What | Path | Notes |
|---|---|---|
| Raw scans | `assets/doodle-scans/` | An archive that is never served. It sits outside the Nix website source filter, like `assets/portfolio-originals/`. Add a short `manifest.md` listing each file, its scan date, the artist, the IDs on the sheet and the usage OK (see Credit). |
| Processed doodles | `website/src/lib/doodles/<id>-<name>.png` | These go under `src/` so Vite hashes them and applies `SITE_BASE`. Don't use `static/`: a hard-coded `/doodles/x.png` in CSS breaks under the `/resume` Pages base, and CSS can't call `sitePath()`. Vite inlines files under 4 KB as data URIs automatically. |
| Processing script | `website/scripts/process_doodle.py` | Write it with Pillow, which the dev shell already has. It lives next to `gen_social_card.py`. |

Naming: a single take is `a4-circle.png`. A boil sprite is `a9-bow-boil.png`. The A1 lengths are `a1-underline-lg.png`, `-md` and `-sm`.

### Processing: scan to alpha mask

The goal is to keep the hand (pressure, skips, ink blobs) while making the color a CSS token. Each doodle becomes a gray+alpha PNG in which alpha is the ink density.

1. Crop each take out of the sheet with about 20 px of padding.
2. Take the **red channel**. Blue ink is darkest there, and paper tone and faint smudges aren't.
3. Invert, then apply levels. The black point clips paper texture to zero, and the white point sets how solid the heaviest ink gets. Start at 12% and 85%, then tune per sheet. A white point that's too low flattens the pressure variation, which is most of the charm.
4. Use that grayscale as the alpha channel over solid black, then trim.
5. Resize to 10 image px per mm of paper, which is 2x the 5 CSS px/mm rule. From a 600 dpi scan that's 42%. Use Lanczos.
6. Export as PNG, or as lossless WebP if that's smaller. Check the edges at 400% for dust and paper fibers.

For a quick manual test, ImageMagick works. It isn't in the dev shell, so run `nix shell nixpkgs#imagemagick` first:

```sh
magick crop.png -channel R -separate +channel -negate -level 12%,85% \
  -background black -alpha shape -trim +repage -resize 42% a4-circle.png
```

This pipeline was checked on a synthetic scan (noisy cream paper with two blue strokes of different darkness). The paper came out fully transparent and the ink opaque. It hasn't met a real scan yet, so expect to tune the levels.

For boil items, process all three frames with **identical** crop boxes and levels so they line up, then join them left to right into one sprite.

### Color

Add one token to `:root` in `src/styles/site.css`:

```css
--doodle-ink: #24409b; /* ballpoint blue: 8.4:1 on --paper, 7.7:1 on --paper-shade */
```

Treat that as a starting value. Sample the real scans and adjust it until it matches the pen. Keep it clearly apart from `--accent` and `--ink`. Links on this site are orange, so blue reads as ink here rather than as a link, but no doodle should sit where it could be mistaken for an underline of an orange link. Blue and the burnt orange are complements, so the two will pop against each other.

### Rendering

Use one element per doodle. It's CSS only, so it works with JavaScript off.

```svelte
<!-- src/lib/components/Doodle.svelte -->
<script lang="ts">
  let { name, class: extra = '' }: { name: string; class?: string } = $props();
</script>
<span class={`doodle doodle--${name} ${extra}`} aria-hidden="true"></span>
```

```css
.doodle {
  position: absolute;
  pointer-events: none;
  background-color: var(--doodle-ink);
  -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
  -webkit-mask-position: center; mask-position: center;
  -webkit-mask-size: contain; mask-size: contain;
}
.doodle--a4-circle {
  -webkit-mask-image: url('../lib/doodles/a4-circle.png');
  mask-image: url('../lib/doodles/a4-circle.png');
  width: 12.5rem;           /* PNG width / 2, since the PNG is 2x */
  aspect-ratio: 400 / 180;  /* the PNG's pixel size */
}
@media (forced-colors: active) { .doodle { display: none; } }
```

Keep each `url()` literal in the rule that uses it, rather than passing it through a custom property. Vite reliably rewrites literal URLs in `site.css` to hashed, base-aware paths.

Doodles render at a fixed size taken from their drawn size, not one that scales with `vw`. Where the anchor changes size a lot across breakpoints (the name, for example), swap takes (A1 lg, md, sm) instead of scaling. Keep any scaling between 0.8x and 1.25x so line weights stay consistent across a page.

### Two layers

**On the print.** These doodles are drawn on a photo, the headshot or the ticket. Each one lives inside the element that carries that print's transform, so it tilts and lifts with the print under the pointer. For photos, that means inside `.photo-mat`. That element is a link, which is fine for an `aria-hidden`, `pointer-events: none` child that stays inside the print's box. For the headshot, use `.portrait-card`. There are two traps:

- `clip-path` clips children. That affects `.now-stub` and `.ticket-card` (the ticket tear) and `.portrait-backing`.
- `filter: drop-shadow` shadows children, which would break rule 5. That affects `.now-stub-shadow` and `.brand-ticket`. For A4 on the stub, make the doodle a sibling of `.now-stub-shadow` inside `.now-aside` and give it the same transform declaration. `paperMotion` sets the `--pointer-*` vars on `.now-aside`, so the sibling inherits them. Its tilt has to match the stub's: 2deg by default, and -1.5deg on even shows and below 768px.

**On the page.** These are margin notes in the layout itself. They're static, so they don't follow the pointer, and they sit under the prints in z-order. On wide screens, `.photo-spread::before` (the shared paper shape) drifts 24px with scroll. Spike marks meant to sit "on" that paper either take the same scroll animation or sit outside it.

### Placement map

The breakpoints are the existing ones: 960, 768 and 640.

| ID | Page | Anchor | Layer | Desktop (960 and up) | Phone (under 640) |
|---|---|---|---|---|---|
| A1 | `/` | `.artist-name > span + span` ("Rutis") | page | lg take under the word, slightly rotated | sm take, since the name is one line here |
| A2 | `/` | A corner of `.portrait-card`, or the "Finn" span | page | One cluster, boiling | hide |
| A3 | `/` | From the end of `.bio-block` toward the headshot's lower-left corner | page | Must not cross `.hero-links` | hide |
| A4 | `/` | `.stub-day` on the current-project ticket | print (sibling, see above) | Circles the date | same |
| A5 | `/` | The empty top right of `.photo-spread`, above `.photo-print--tall` (cols 9 to 12, its 10rem top margin) | page | The beam stops at the print's top edge and never lands on the face | hide |
| A6 | `/` | The empty block above `.photo-print--tall-left` (cols 1 to 5, its 12rem top margin), aiming at `--wide-right` | page | One set of notes | One, between two prints |
| A7 | `/` | On the paper shape (`.photo-spread::before`), near `--small` | page | 2 or 3 marks | 1, in the side gap beside a 72% print |
| A8 | `/` | Beside one or two `.photo-note-title`s, which Finn picks | page | sm take | same |
| A9 | all | Standing on the `.site-footer` top border, just off center | page | Boiling | same |
| B1 | `/performance-reel/` | Beside the `h1` | page | | same |
| B2 | `/booking/` | In the empty left 25% of `.contact-links`, with the flight path ending short of the email | page | | hide (the margin is 0 here) |
| B3 | 404 | Beside the heading in `+error.svelte` | page | Boiling | same |
| B4 | `/about/` | Left of `.statement-body` | page | | hide |
| B5 | `/about/` | The top edge of an `.offstage-item--slip` | print | | same |
| B6 | `/resume/` | Beside the first `.download-actions` link | page | Optional, since this page is for casting and should stay clean | hide |

The About route is still uncommitted work in progress with placeholder text, so the B4 and B5 positions are provisional. `/resumes/` gets no doodles.

### Notebook paper

The notebook feel comes from the ink plus one new paper stock: a ruled notebook page drawn in CSS, not scanned. Don't rule whole pages, because that would fight the photos and the playbill type. The first candidates are the About page's `.offstage-item--slip` notes, and possibly the contact page.

```css
.notebook {
  --rule: rgb(36 64 155 / .14);
  --margin-line: rgb(181 74 0 / .3); /* the accent stands in for the pink margin line */
  background:
    linear-gradient(90deg, transparent 2.5rem, var(--margin-line) 2.5rem calc(2.5rem + 1px), transparent 0),
    repeating-linear-gradient(transparent 0 calc(1.6em - 1px), var(--rule) 0 1.6em),
    var(--ticket-paper);
}
```

Text sits on the rules only if its line height matches the rule spacing (body text uses 1.6) and the paper isn't rotated relative to the text. Right now the slips tilt their paper (`::before`) but not their words. Either drop the tilt for ruled slips, or accept that the words float over the rules like typing on a loose page. Punched holes are optional: three `radial-gradient` circles down the left edge.

### Motion

- Doodles are static by default.
- **Boil** (A2, A9, B3): put the three frames in one horizontal sprite and step through them at about 8 frames per second.

  ```css
  .doodle--a9-bow {
    -webkit-mask-size: 300% 100%; mask-size: 300% 100%;
    animation: boil 375ms steps(3) infinite;
  }
  @keyframes boil { to { -webkit-mask-position: 150% 0; mask-position: 150% 0; } }
  ```

  With a 300% mask, `steps(3)` up to 150% lands on 0%, 50% and 100%, which are frames 1, 2 and 3. Keep only one boiling doodle in view at a time. The global reduced-motion rule (`animation: none !important`) already freezes it on frame 1.
- **Optional draw-on:** wipe a doodle in the first time it enters view by animating `clip-path` from `inset(0 100% 0 0)` to `inset(0)` over about 400 ms. If you add this, extend `paperMotion` instead of adding a second observer. Use `fill: 'backwards'` and the same reduced-motion check, so nothing is hidden without JavaScript and the wipe is skipped under reduced motion.

### Accessibility and performance

- Use `aria-hidden="true"` with no alt text and no role. Words in a doodle must never be the only place a piece of information lives.
- Doodles are hidden in forced colors (rule above), the same way the paper backings are.
- They're pure CSS, so they're present with JavaScript off.
- They're absolutely positioned, so they cause no layout shift. Doodles near the edges can cause horizontal scrolling at 320 and 390 px. To prevent it, prefer `overflow-x: clip` on the containing section over `hidden`.
- Budget: under 15 KB per doodle, under 40 KB per boil sprite, and under 120 KB of doodles on the homepage in total.

### Order of work

1. Archive the scans and write the manifest.
2. Process Set A and pick takes with Finn.
3. Add the token, the `Doodle` component, and the base, forced-colors and boil rules.
4. Place Set A on the homepage at 1440 px, then at 390 px, then at the widths in between.
5. Place Set B on the other pages.
6. Add the credit line, then run the checks below.

### Checks

Add these to the validation list in `docs/portfolio-site.md`:

- At 320, 390, 768, 1024 and 1440 px: no doodle sits on a face or over text, none reads as an underline of a link, and there's no horizontal scroll.
- With pointer tilt and hover lift: on-print doodles move with their print, page doodles stay put, and ink never has a shadow.
- Every doodle on a page has the same line weight. One that reads heavier or thinner was drawn or scaled at the wrong size.
- With reduced motion, the boil freezes on its first frame and there's no draw-on. In forced colors, there are no doodles. With JavaScript off, every doodle is present.
- In a `SITE_BASE=/resume` build, every doodle loads, with no 404s in the network panel.
- A screen reader announces nothing for any doodle.

### Credit and permission

- Add a footer credit in `.footer-meta`, next to the Cooper license, along the lines of "Doodles by <name>". Link it wherever the artist wants, and ask them how they'd like to be credited.
- Get a short written OK (a text or an email is enough) that Finn can use the drawings on finnrut.is, the blog and social posts. The artist keeps the originals and the copyright. Record the OK in the scans manifest.

### Open questions for Finn

1. Should doodles include words (A3 "me!", B4, B6)?
2. Which show titles get stars (A8)?
3. Should the ink token match the scanned blue exactly, or be nudged?
4. Once scans exist, should a doodle go on the social card (`scripts/gen_social_card.py`)?
5. What credit wording and link does the artist want?
