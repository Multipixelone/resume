# Portfolio media and font preservation

Research and preservation run: 2026-10-21. Public-only source retrieval; no publishing, account operation, DNS change, Squarespace cancellation, or deployment. This document records files preserved under the user-authorized asset scope. It is not a claim that the complete Squarespace media library or source originals have been migrated.

## Image files

Seven distinct homepage image paths previously visible in public Squarespace HTML were fetched directly from their CDN URLs. Responses were HTTP 200, but all seven returned `Content-Type: image/webp` and decoded as WebP despite the `.jpg` URL suffix. `assets/portfolio-originals/<observed-name>.jpg` preserves each exact response byte-for-byte (WebP payload under the public URL's original path name). The archive is therefore a preserved CDN-served rendition, **not verified original camera files or clean source originals**.

`website/static/media/<same-observed-name>.jpg` holds derivative JPEGs decoded from those retained CDN WebP payloads, resized only when needed to maximum 1920px on the longest dimension and encoded at JPEG quality 88. No cutouts, generative fill, retouching, content alteration, or captions were added. Finn's cutout and Photoshop-fill workflow remains his own. The original payloads remain available separately.

| Observed filename (stable path) | Route association | Public source URL | Original archive payload (actual format/dimensions/bytes) | SHA-256 of archive bytes |
|---|---|---|---|---|
| `portrait.jpg` | `/`, portrait/hero block | https://images.squarespace-cdn.com/content/v1/693b77108e84b232a7bf4b84/c560cc7c-2937-4e66-a166-306fbc79fbaa/portrait.jpg | WEBP, 2400×3000, 349,998 | `766b4f0eb8d8b2e940933f5408fa5d02e7ee65abcf4726134035bc78ce1cbe2c` |
| `finn_photo_reel_2.jpg` | `/`, image block | https://images.squarespace-cdn.com/content/v1/693b77108e84b232a7bf4b84/e7e31854-a8d5-40fe-8c70-2b82c2f40b86/finn_photo_reel_2.jpg | WEBP, 2500×1735, 541,432 | `ac02b8b9474aeb58a0fe8d676104d635ebd6cba5f9db309f4711bf4acb1c9994` |
| `2X9A9381-X4.jpg` | `/`, image block | https://images.squarespace-cdn.com/content/v1/693b77108e84b232a7bf4b84/e44adf1d-c1d7-4183-9128-6699ed3d5813/2X9A9381-X4.jpg | WEBP, 1638×2048, 165,164 | `625b519011f56887fb438f8865ec867ec01b34803784ee7170c35d13722a1572` |
| `composer_singing.jpg` | `/`, image block | https://images.squarespace-cdn.com/content/v1/693b77108e84b232a7bf4b84/e8231d12-6fde-4adf-ad20-34e20bd6d1c1/composer_singing.jpg | WEBP, 1280×960, 100,426 | `d9f815c6f0a1209b741be0f0ee5f30210736a90f1c4817fc0f09e825f81d8a24` |
| `2X9A9285-4K.jpg` | `/`, image block | https://images.squarespace-cdn.com/content/v1/693b77108e84b232a7bf4b84/f9c08f0e-bf40-43bc-b8e8-e5c0e5e403aa/2X9A9285-4K.jpg | WEBP, 1420×1136, 155,242 | `d2837d6ae721b9aa6ead514ee4a6f914b0382ff5aa7018ff1c69412f652ee5d0` |
| `20250529_Molloy_University_Legally_Blonde_JRV_3462-X3.jpg` | `/`, image block | https://images.squarespace-cdn.com/content/v1/693b77108e84b232a7bf4b84/52f5f0f5-5762-48d4-a84b-4b8616fbaad8/20250529_Molloy_University_Legally_Blonde_JRV_3462-X3.jpg | WEBP, 655×893, 31,774 | `78ad6cc2b71a5dcc82ba0fafb869e7b900c537278801da832df3539b47486d83` |
| `_DSC2342-X3.jpg` | `/`, image block | https://images.squarespace-cdn.com/content/v1/693b77108e84b232a7bf4b84/9d20d773-aa09-4a36-bf73-e8f12322037c/_DSC2342-X3.jpg | WEBP, 739×721, 62,656 | `bcaf5db185c7980854a27dd13bdc9c7bbc81e78ad87accc34fafeb13707dacf7` |

Exact transport metadata and source list are in [`assets/portfolio-originals/manifest.json`](../assets/portfolio-originals/manifest.json). Website JPEG dimensions after optimization are: portrait 1536×1920; reel photo 1920×1332; `2X9A9381-X4` 1536×1920; composer singing 1280×960; `2X9A9285-4K` 1420×1136; Legally Blonde image 655×893; `_DSC2342-X3` 739×721. All saved JPEGs were verified by ImageMagick as JPEG, not HTML or an error page. SHA-256 values for website derivative bytes can be regenerated from the files; their hashes are intentionally distinct from the exact payload archive.

No reliable photo credits or content/alt descriptions were established by the source HTML (image alt attributes were blank). Filenames such as the Legally Blonde image are copied as observed source filenames, not independently verified credit, show identity, role, photographer, or permission. Rights/credit and meaningful alternative text remain to be confirmed.

## Decorative hardware

`website/static/decorations/pushpin-rust.png` derives from
[Haragayato's photograph of a pushpin](https://commons.wikimedia.org/wiki/File:Pin.JPG),
taken on 2006-07-09 and released by the photographer into the public domain.
The original 1254x1086 JPEG is preserved as
[`assets/portfolio-decor/pushpin-source.jpg`](../assets/portfolio-decor/pushpin-source.jpg).

On 2026-10-22 the built-in image editor removed the paper background and cast
shadow, and recolored the turquoise plastic to rust. A second edit changed the
viewpoint to look nearly along the pin's axis and buried the needle, so the
cap covers most of the grip and the base appears seated against the paper.
The result is an AI-assisted reinterpretation of the source photograph, not
an untouched photograph. The exact prompts are saved in
[`pushpin-rust.prompt.txt`](../assets/portfolio-decor/pushpin-rust.prompt.txt)
and [`pushpin-seated.prompt.txt`](../assets/portfolio-decor/pushpin-seated.prompt.txt).

The transparent result was trimmed with 16px of padding and proportionally
resized to 160x156 and palette-optimized to 13,660 bytes. It displays on a
20px-wide canvas, anchored by the projected base center, and is decorative
(`alt=""`, `aria-hidden="true"`). It is separate from the preserved performance
photography and does not enter the canonical performance-photo list.

## Reel videos and route inventory status

Current raw public `/performance-reel` HTML exposes these three YouTube blocks in this order:

| Order in source | Title from iframe metadata | Video ID | Embed URL | Route |
|---:|---|---|---|---|
| 1 | I Love to Sing-a & Love Me, Love Me Not | `DYrR7xup_Js` | https://www.youtube.com/embed/DYrR7xup_Js?feature=oembed | `/performance-reel` |
| 2 | No One Has to Know | `-QPog0QsJ9s` | https://www.youtube.com/embed/-QPog0QsJ9s?feature=oembed | `/performance-reel` |
| 3 | Circus McGurkus | `ZP38u-e76BY` | https://www.youtube.com/embed/ZP38u-e76BY?feature=oembed | `/performance-reel` |

These are retained as external YouTube references, not downloaded media. No YouTube masters or captions were downloaded. An older discovery note reported four YouTube embeds; the current fetched raw route source contains three blocks, so the earlier fourth remains unexplained. No claim of video-master preservation or complete account-wide inventory is made.

## Cooper fonts

Saved locally from public blog source at pinned commit [`b12e850e12a71bc07240a74c91fc9bac5d569b59`](https://github.com/Multipixelone/blog/commit/b12e850e12a71bc07240a74c91fc9bac5d569b59), without fetching/procuring any proprietary blog fonts:

| File under `website/static/fonts/cooper/` | Upstream size | Upstream Git blob | SHA-256 of locally saved bytes |
|---|---:|---|---|
| `Cooper-Regular.woff2` | 23,704 | `c5a68955a9a5bdc0482282eb6a731fc31d18d95b` | `e9bc8c3568bdc500ca34d0612a259b3d04fdce51d4f5232d054736528470bcdd` |
| `Cooper-Bold.woff2` | 25,412 | `bd1baa9f1277c3e41a69d9e265b68c215d18752d` | `d63707dac3ddef77a0910ec15933d10f78407b8c1680ee0e22cd4edadd57b726` |
| `Cooper-Black.woff2` | 25,052 | `1730e9c3bf88b9a5b5ca1bd90226fd851c881182` | `c517576258355769d03576da97562de530eb1d949c2cd58067cb0cec9fa92785` |
| `LICENSE.md` | 3,934 | `c8c81bbd07ad68fa7611e7ce0a4d547953d6128c` | `2381dcb6da8f3e0395b23957f381ecb55f25d4bad494a666c6b566075df1ea97` |

The font files were verified as WOFF2 and match reported upstream byte lengths; `LICENSE.md` is UTF-8 text. It states copyright 2024 The Cooper* Project Authors and licenses this Font Software under SIL Open Font License 1.1. The license permits use, copying, embedding, modification, and redistribution subject to terms including not selling the font alone, shipping the copyright/license notice with bundled font copies, and keeping font software under OFL. Keep this license available with the website font distribution. This does not convey rights to Sabon Next or PragmataPro Mono Liga: those remain proprietary/gitignored and must not be copied under this lane.

## Completeness, custody, and remaining gates

- Preserved: 7 CDN HTTP response bodies (exact byte archive) and 7 optimized JPEG web files, all under the same observed filenames; 3 Cooper WOFF2 faces and font license; current 3 YouTube embed metadata as URLs/titles/IDs only.
- Archive size: 1,406,692 bytes of image response payloads, plus font files/license. Website media JPEGs are derivatives and must not replace the archive.
- This bounded recheck was of the four public preview routes `/`, `/resume`, `/performance-reel`, `/booking`; only homepage yielded the seven known image block URLs, and current reel route yielded three video blocks. The prior report already notes extracted-source limitations; no private Squarespace media library, unpublished pages, all state variants, or resume-library subdomain crawl was conducted. Seven photos / three current embed IDs are not certified as total Squarespace inventory.
- Original clean camera/photo masters were not located or established. CDN bytes may be compressed/resized Squarespace representations. Finn must provide/verify source originals before canceling Squarespace; retain Squarespace until full media preservation and replacement verification, per the migration brief.
- No photo credit/release/ownership evidence or exact alt copy has been added. Confirm usage rights and credits, especially production photography, before public publishing.
- No video masters or subtitles were fetched; external YouTube video availability can change independently. Resolve fourth-embed discrepancy, source masters, captions/transcripts and intended download destinations. This remains a preservation/cancellation gate.
- Portfolio media filenames are now available to the separate website implementation owner. That owner should reference `website/static/media/<filename>` and use the stable observed names. Cooper web assets live at `website/static/fonts/cooper/`; preserve CSS family name `Cooper*`, and retain `LICENSE.md` when distributing those font files.
- No files outside the specifically allowed asset/report destinations were edited by this run; no package manifest, application source/config, index, build, commit, or remote service state was touched.

## Source references

- Requirements and prior route/image inventory: [`docs/portfolio-migration.md`](portfolio-migration.md).
- Prior public evidence and video IDs: [`.slim/deepwork/portfolio-migration/media-research.md`](../.slim/deepwork/portfolio-migration/media-research.md).
- Cooper exact files/license pinned source: [font directory](https://github.com/Multipixelone/blog/tree/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/fonts/cooper), [font license](https://github.com/Multipixelone/blog/blob/b12e850e12a71bc07240a74c91fc9bac5d569b59/static/fonts/LICENSE.md).
- Live public routes: [home](https://burgundy-seahorse-b69m.squarespace.com/), [resume](https://burgundy-seahorse-b69m.squarespace.com/resume), [performance reel](https://burgundy-seahorse-b69m.squarespace.com/performance-reel), [booking](https://burgundy-seahorse-b69m.squarespace.com/booking).
