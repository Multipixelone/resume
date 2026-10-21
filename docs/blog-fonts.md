Blog typography is three families: Cooper*, Sabon Next, and PragmataPro Mono Liga; portfolio styling should preserve that same family system, subject to the proprietary-font hosting/license constraints.

# Blog font inventory and portfolio handoff

Research date: 2026-10-21. Read-only source research. No font binaries were downloaded or added to this repository. Sources were checked at blog commit [`b12e850e12a71bc07240a74c91fc9bac5d569b59`](https://github.com/Multipixelone/blog/commit/b12e850e12a71bc07240a74c91fc9bac5d569b59), current `main` at research time; GitHub commit API identifies this as the October 8, 2026 commit “feat(new): first write of Album Graph.” The live `https://blog.finnrut.is/style.css` was also fetched and its ETag/content matched the pinned source CSS. Statements below distinguish declarations, CSS use, build use, and what has actually been verified.

## Inventory at a glance

| CSS family name (exact) | Role in blog | Declared faces / actual CSS weight use | Delivery and status |
|---|---|---|---|
| `Cooper*` (asterisk is part of the CSS family name) | Display/brand face: page `h1`, decorative header fleuron, post drop caps; all generated social-card typography also uses Cooper. | `Cooper-Black.woff2` weight 900 normal; `Cooper-Bold.woff2` 700 normal; `Cooper-Regular.woff2` 400 normal. CSS `h1` asks for 700, fleuron/drop cap ask for 400. OG card generator chooses Cooper Black for titles, Bold for site wordmark, Regular for description/meta/chips. Thus Black is available but not the blog's `h1` face under declared CSS. | Committed WOFF2 files under `static/fonts/cooper/`, served as same-origin `/fonts/cooper/...`; source has dedicated SIL OFL 1.1 license. |
| `Sabon Next` | Main body serif, body headings `h2`-`h6`, search UI, and general serif text; body face. | Regular 400 normal; Italic 400 italic; Demi 600 normal; Bold 700 normal. Body requests family with fallbacks; default normal body text 400. Strong/bold requests 700. `h2` uses 700, `h3` 500 (browser may synthesize/interpolate because no 500 face declared), `h4`-`h6` 600. | Proprietary and gitignored; site CSS references WOFF2 at `https://fonts.finnrut.is/`. Live stylesheet access confirms declaration, not that every browser/font request succeeds. README says locally subset/uploaded and served through R2; CSS comments say CORS locked to blog origin. |
| `PragmataPro Mono Liga` | Code, inline code, kbd/samp/var, code-block captions/buttons, archive dates, and other monospaced labels via `--font-mono`. | Regular 400 normal; Bold 700 normal; Italic 400 italic; BoldItalic 700 italic. CSS comment says regular, bold, and italic are reached in current built highlighting; no rule sets bold+italic together, so that face is currently declared but not exercised by a combined style. | Proprietary and gitignored; `local()` first, then WOFF2 at `https://fonts.finnrut.is/`. README/CSS say R2 with CORS restricted to `blog.finnrut.is`; preload only when a page contains code blocks. |

The family fallback stacks are part of the design. Cooper headings use `"Cooper*", Georgia, serif`; Sabon body uses `"Sabon Next", Georgia, "Times New Roman", serif`; mono uses `"PragmataPro Mono Liga", ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace`. If a face fails to load the fallback may render, so CSS declarations alone do not prove the font rendered on a visitor's device.

## Exact committed Cooper files

GitHub Contents API at the pinned revision lists exactly these three files under `static/fonts/cooper/`:

| File | API size | API blob SHA | Face mapping |
|---|---:|---|---|
| [`Cooper-Black.woff2`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/fonts/cooper/Cooper-Black.woff2) | 25,052 bytes | `1730e9c3bf88b9a5b5ca1bd90226fd851c881182` | `Cooper*`, 900 normal |
| [`Cooper-Bold.woff2`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/fonts/cooper/Cooper-Bold.woff2) | 25,412 bytes | `bd1baa9f1277c3e41a69d9e265b68c215d18752d` | `Cooper*`, 700 normal |
| [`Cooper-Regular.woff2`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/fonts/cooper/Cooper-Regular.woff2) | 23,704 bytes | `c5a68955a9a5bdc0482282eb6a731fc31d18d95b` | `Cooper*`, 400 normal |

The static CSS uses relative URLs `fonts/cooper/Cooper-*.woff2`; with the deployed stylesheet at `/style.css`, those resolve to the above same-origin files. Every Cooper face declares `font-display: swap`. CSS source provides the weight-to-file mapping; source CSS does not include an explicit `unicode-range`, and the font-subsetting script documents the committed Cooper files as already subset.

### How Cooper is actually used

- `body`: not Cooper. The body is Sabon Next.
- `h1`: `font-family: "Cooper*", Georgia, serif`, `font-weight: 700`; exact corresponding declared face is Cooper Bold, not Cooper Black. `h1` also requests common and discretionary ligatures.
- `h2`-`h6`: Sabon Next; these headings do not inherit Cooper because their selector sets a different family.
- Header fleuron (`header::after`, content `❦`): Cooper* weight 400, with `font-feature-settings: "swsh" 1` not used there.
- Blog article initial/drop cap: Cooper* weight 400; `swsh` feature enabled. CSS has a floated fallback for browsers without `initial-letter` and a native three-line initial-letter branch for browsers supporting it. Both select Cooper Regular and the swash feature.
- Generated OG/social cards: `scripts/gen_og_cards.py` uses Cooper Black for the title, Cooper Bold for site/domain wordmark, and Cooper Regular for description, metadata, and chips. This is build-time image rendering, not a live browser font use.
- No Cooper Italic face is declared in this family.

## Sabon Next exact web sources and usage

CSS uses these remote filenames (URL-encoded spaces shown exactly as in CSS):

| Face | CSS weight/style | URL |
|---|---|---|
| Regular | 400 normal | `https://fonts.finnrut.is/Sabon%20Next%20Regular.woff2` |
| Italic | 400 italic | `https://fonts.finnrut.is/Sabon%20Next%20Italic.woff2` |
| Demi | 600 normal | `https://fonts.finnrut.is/Sabon%20Next%20Demi.woff2` |
| Bold | 700 normal | `https://fonts.finnrut.is/Sabon%20Next%20Bold.woff2` |

All declare `font-display: swap`. Base template preloads the regular face on every page, with a `crossorigin` preload and preconnect to `fonts.finnrut.is`. CSS comments say this replaced an Adobe Fonts Linotype-Sabon kit; local copies under `static/fonts/sabon/` are gitignored due to Linotype EULA redistribution restrictions. README says Sabon Next is proprietary/gitignored and hosted on Cloudflare R2. CSS comments say CORS is locked to `blog.finnrut.is`. The remote stylesheet and live site were accessible in this research, but that proves only public CSS availability, not a license granting use on a different site or a successful cross-origin webfont load from the future portfolio origin.

## PragmataPro Mono Liga exact web sources and usage

CSS declares these four faces; each has a `local()` desktop font name first, followed by a remote WOFF2 URL, then `font-display: swap`:

| Face | CSS weight/style | `local()` name | Remote URL |
|---|---|---|---|
| Regular | 400 normal | `PragmataProMonoLiga-Regular` | `https://fonts.finnrut.is/PragmataPro_Mono_Regular_ligatures_0827.woff2` |
| Bold | 700 normal | `PragmataProMonoLiga-Bold` | `https://fonts.finnrut.is/PragmataPro_Mono_Bold_ligatures_0827.woff2` |
| Italic | 400 italic | `PragmataProMonoLiga-Italic` | `https://fonts.finnrut.is/PragmataPro_Mono_Italic_ligatures_0827.woff2` |
| Bold Italic | 700 italic | `PragmataProMonoLiga-BoldItalic` | `https://fonts.finnrut.is/PragmataPro_Mono__Bold_Italic_ligatures_0827.woff2` |

CSS's `--font-mono` stack applies to `code`, `pre`, `kbd`, `samp`, `var`, `.z-code-header`, `.copy-btn`, `.archive-year time`, `.elsewhere-handle`, `.related-meta`, plus other exact selectors using that custom property. The code styles use `0.85em`; code-block header uses 0.75rem/400; copy button 0.7rem; archive year dates 0.72rem; profile handles 0.72rem. The Zola page template conditionally invokes the mono preload macro only when rendered page content contains `.z-code`; this preload is the regular face. CSS comments say regular/bold/italic are encountered in built syntax-highlighted content; bold italic remains declared for possible future use but not currently selected by a combined rule.

## License and permission boundaries

### Cooper: file-specific public OFL 1.1

Pinned [`static/fonts/LICENSE.md`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/fonts/LICENSE.md) says:

> Copyright 2024 The Cooper* Project Authors
> (https://github.com/indestructible-type/Drafting)
>
> This Font Software is licensed under the SIL Open Font License, Version 1.1.

The license grant says permission is given to use, study, copy, merge, embed, modify, redistribute, and sell copies, subject to its conditions. Key conditions in this file: fonts/components cannot be sold by themselves; bundled font copies must include the copyright notice and OFL; names of copyright holders/authors cannot promote a modified version absent permission (acknowledgement is allowed); font software must remain entirely under OFL and not another license. The grant and notice/license are sufficient public evidence that the committed Cooper font software is permitted for embedding/redistribution under OFL terms. If portfolio usage copies the face, retain/include the Cooper copyright notice and license in the distributed asset/site notices, do not sell the font standalone, and do not relicense it. If modifying/subsetting/converting the font, keep it under OFL and follow the license's modified-version naming/notice requirements; using the unmodified committed WOFF2 avoids that extra question. Do not attribute unrelated blog source code's AGPL-3.0 license to font files; font-specific OFL is the applicable public font license.

### Sabon Next and PragmataPro: proprietary; separate site permission unresolved

The blog README explicitly states: “Sabon Next and PragmataPro are proprietary, gitignored, and served from Cloudflare R2 (`fonts.finnrut.is`).” The `.gitignore` gives additional source evidence: Sabon Next must not be committed to the public repo, citing Linotype EULA redistribution; PragmataPro must not be committed, citing FSD Web Site license §§5.2 and 7.1. CSS comments say both remote origins are CORS-locked to `blog.finnrut.is`. The font files themselves are not in the public repo. These sources do **not** grant permission to copy those files into the portfolio, to reuse the remote URLs from another domain, or to expand CORS. Do not infer a wider license from public access to CSS or successful current blog rendering. Reuse them for the artist site only if Finn verifies that the applicable paid/proprietary license covers another site/domain and the desired webfont embedding, and confirms legal delivery/CORS or another authorized source. Keep Sabon Next and PragmataPro as required design families in planning; do not silently substitute fallback families as an intentional portfolio design choice. Their native system fallbacks may appear if fonts cannot load, but that is degraded rendering, not equivalent use.

## What is verified versus not

- **Verified from pinned source:** exact CSS family identifiers, URLs, face declarations/weights/styles, `font-display`, actual selector roles, mobile font-size changes, conditional preload logic, OG font files/roles, Cooper license text, proprietary-font descriptions and CORS notes.
- **Verified from live public endpoint:** `blog.finnrut.is/style.css` returned successfully with the same CSS content/ETag as the pinned source fetched here; this is a live declaration check.
- **Not verified:** individual webfont network requests/response headers, cross-origin CORS result from the prospective portfolio domain, a browser's chosen/rendered face, exact current proprietary license terms for a second domain, whether local fonts on a visitor's machine match the CSS `local()` names, and whether blog maintainers' acquisition terms support reuse beyond the stated Cooper OFL text. No proprietary font binary was fetched.
- **Font CSS uses `font-display: swap`:** browser can initially show a fallback then replace it after font load. `local()` on PragmataPro may skip network fetch if a compatible local face exists. Therefore CSS declaration is not proof each visitor receives the named face.
- **Responsive typography:** under `@media (max-width: 600px)`, blog body falls from 18px to 17px; h1 from 2.3rem to 1.85rem; h2 from 1.75rem to 1.6rem; h3 from 1.35rem to 1.3rem. The font families/weight declarations do not change in that media query.

## Portfolio handoff

Use the same three family names, not merely the warm palette: Cooper* for display treatment, Sabon Next as body/editorial serif, and PragmataPro Mono Liga for monospace/code-style details where relevant. Preserve the asterisk in the Cooper CSS family name. Do not confuse “use Cooper Black” with the blog's exact current `h1` mapping: it uses Cooper Bold (700), whereas Black is declared at 900 and used for OG title art. The portfolio's requested heavier Cooper Black treatment would be an intentional role/weight change within the same Cooper* family, not a different font-family substitute. Use the committed Cooper files with their OFL notice/license. For Sabon Next and PragmataPro, coordinate authorized files, domain coverage and CORS with Finn before using blog R2 URLs or any copied local files; the web source does not establish those proprietary permissions.

## Pinned sources

- [Exact inspected commit](https://github.com/Multipixelone/blog/commit/b12e850e12a71bc07240a74c91fc9bac5d569b59) (API says current `main` at research time; authored/committed 2026-10-08).
- [`static/style.css`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/style.css): font faces, stacks, selectors, responsive rules and CORS comments.
- [Committed Cooper font directory](https://github.com/Multipixelone/blog/tree/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/fonts/cooper): exact three WOFF2 files.
- [`static/fonts/LICENSE.md`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/fonts/LICENSE.md): Cooper Project Authors copyright and SIL OFL 1.1.
- [`templates/base.html`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/templates/base.html): body template, stylesheet link and Sabon preload.
- [`templates/macros/fonts.html`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/templates/macros/fonts.html): exact regular serif and mono preload URLs.
- [`templates/page.html`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/templates/page.html): conditional mono preload for pages containing code blocks.
- [`scripts/gen_og_cards.py`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/scripts/gen_og_cards.py): Cooper face roles in generated cards.
- [`.gitignore`](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/.gitignore) and [README Fonts section](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/README.md): proprietary font handling, hosting and stated license restrictions.
- [Live deployed stylesheet](https://blog.finnrut.is/style.css): fetched October 21, 2026; content/ETag matched pinned `static/style.css`.
