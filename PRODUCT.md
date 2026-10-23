# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: theatre makers vetting Finn as a performer. Casting directors, directors, agents and theatre companies deciding whether to call Finn in or cast them. They shape every decision on the site.

Secondary, served but never shaping the site:

- Hiring managers in other fields (tech, events, hospitality, childcare) who get a direct link to a tailored PDF, or find their field's general resume on `/resumes/`.
- People looking up a current show for tickets or the livestream.

## Product Purpose

finnrut.is is Finn Rutis's portfolio site, built from `website/`. It presents Finn as a musical theatre performer based in New York City. The Typst resume PDFs in this repo are a separate design surface with their own rules in `AGENTS.md`; the site shows and distributes them but does not redesign them.

Success: the visitor watches Finn perform and takes the resume away. Reel views and PDF downloads are the outcome that matters. Contact stays available, but it does not have to happen on the site in the same visit.

The site replaces the old Squarespace site at finnrut.is. DNS cutover and Squarespace cancellation have not happened yet and are not authorized by this file.

## Positioning

- **The site and the resumes share one source.** Theatre credits come from `metadata/theatre.toml`, the resume list from `variants.toml`, and current projects are computed in the browser from real show dates. The site cannot drift from the resume, and nothing on it is hand-copied.
- **The technologist is a quiet signal, not a section.** Finn also works in tech and production. On this site that shows only through the blog link, the PGP key, and the craft of the build itself. Confirmed by Finn: no tech section, no dual-identity pitch.
- The current bio on `/` and in the page description is Finn's own positioning statement. Do not rewrite it.

## Operating Context

Routes, all prerendered:

- `/`: name, portrait, bio, current projects (when any), performance photos.
- `/about/`: artist statement and "Off stage" escapades. Both are bracketed placeholders until Finn writes them.
- `/resume/`: theatre resume preview, PDF downloads (plain and with headshot), HTML theatre credits. A credit with photos links to its show page.
- `/shows/<id>/`: one page per show that has a photo in `website/src/lib/media.js`: the credit as a notice, every photo of that show, and any recording tagged to that production. Linked from its theatre credit and its homepage print.
- `/performance-reel/`: YouTube recordings plus a film section.
- `/booking/` (labelled "Contact"): email and Instagram.
- `/resumes/`: theatre documents (with the composite `FINN RUTIS.pdf`) first, then general resumes grouped by field. Employer-tailored resumes and cover letters are `site_hidden`: unlisted, still reachable by direct link.

Current projects appear from the first rehearsal day through closing night, computed in Eastern time in the browser. A show with a booking URL gets a linked ticket stub, with an optional "Livestream available" line. Show data and its rules live in `docs/show-data.md`.

Resume PDF and PNG downloads exist only in the Nix build (`nix build '.#website'`), never in `npm run dev`. The site deploys to GitHub Pages from `.github/workflows/website.yml` on push to `main`, at the domain root or under `/resume` (`SITE_BASE`).

## Capabilities and Constraints

- SvelteKit with adapter-static: prerendered pages, trailing slashes, no SPA fallback. Every essential piece of content works without JavaScript.
- The site may read only three shared inputs from the parent repo: `metadata/theatre.toml`, `variants.toml`, `lib/shows.mjs`. A new one must be added to `server.fs.allow` in `website/vite.config.js` and to the source filter in `packages/website.nix`.
- No second variant list. No fabricated show dates, static "current" labels, or invented credits.
- Existing terminology: "Current project(s)", "On stage", "Theatre credits", "Performance reel", "Resume with headshot", "All resumes", "Off stage", "Contact".
- Open, not decided:
  - Web font licensing for Sabon Next and PragmataPro on this domain. Do not deploy those remote declarations until permission is confirmed (`docs/portfolio-site.md`, `docs/blog-fonts.md`).
  - Photo rights, final photo selection, photographer and portrait credits.
  - Video permissions, captions and transcripts.
  - DNS cutover and Squarespace cancellation.

## Brand Commitments

- Name: Finn Rutis. Pronouns: they/them, shown alongside the name.
- **Finn's words are Finn's.** The artist statement, about page, bios, escapade blurbs and photo blurbs are written by Finn. Scaffold them with obviously bracketed placeholders such as `[Artist statement]`. Never draft, suggest or "improve" that copy, even as a starting point. Structural labels (headings, link text) are fine and should be flagged as renameable.
- Every factual claim (credits, roles, companies, directors, training) traces to a line in `REFERENCE.md`.
- No em dashes in shipped copy. Plain ASCII punctuation.
- The site shares its favicon and footer icon row with blog.finnrut.is.

## Evidence on Hand

- Theatre, cabaret and film credits: `metadata/theatre.toml`, mirrored in `REFERENCE.md`.
- Portrait and six performance photos in `website/static/media/`. These are Squarespace CDN renditions, not camera originals (`docs/portfolio-media.md`). Photographer credits are unknown and must never be guessed.
- Three YouTube recordings and one film (All Over Everywhere), in `website/src/lib/media.js` and the reel route.
- PDF and PNG previews for every registered resume variant plus the composite headshot PDF, assembled by the Nix build.
- Social card: `website/static/social-card.png`, drawn by `website/scripts/gen_social_card.py`.
- Not on hand, so never invent them: press quotes, reviews, testimonials, representation, union status, awards, audience or follower numbers.

## Product Principles

1. **The performance leads.** A theatre maker sees Finn's face, work and credits first. Material for other fields stays reachable and out of the way.
2. **Reel and resume are the destination.** Every page keeps a short path to watching Finn and taking the PDF.
3. **One source of truth.** Credits, resumes and current shows come from the repo's canonical data, never from hand copies.
4. **Finn's words are Finn's.** Personal copy stays a placeholder until Finn writes it.
5. **Complete for everyone.** The site works without JavaScript, at large text sizes, by keyboard, and with motion turned off.

## Accessibility & Inclusion

No formal WCAG level has been set. The working bar is the validation matrix in `docs/portfolio-site.md`:

- All essential content (bio, credits, reel titles and direct links, downloads, contact) works with JavaScript disabled.
- Skip link, keyboard navigation and visible focus on every interactive element, including ticket stubs.
- Reduced motion cancels all arrival, pointer and scroll motion.
- Reflow at 200% text size and 400% zoom; forced-colors support; measured contrast.
- Text never overlays a face. Photos carry descriptive alt text, or are decorative when a caption already labels them.
- Video is user-played with no autoplay. Captions and transcripts are still pending.
