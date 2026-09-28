# Sent resume: evidence and validation

Drafted September 25, 2026 for Sent's Content Engineer role.

## Positioning

The resume leads with visual systems and delivered content: nine graphics, a Remotion renderer, and four published videos. The publishing-service bullet identifies specifications, review, and operation as Finn's work and names coding agents as the implementers. Voiceover and theatre video production provide longer-running creative and client evidence. Personal blog documentation is labeled as a personal project.

The [official employer posting](https://jobs.ashbyhq.com/sent/db6bbfaf-ba52-4cec-87c8-27bf1c5b7ca7) was rechecked in the browser on September 25. It still displayed full-time, NYC on-site, $120,000-$145,000 plus equity, and an Apply link. No material differences from the supplied prompt were found. Its emphasis remains API examples, technical storytelling, visual craft, marketing experiments, and measurement through signups and activated accounts.

## Claim map

Line numbers refer to [REFERENCE.md](../REFERENCE.md) as read on September 25. The September 9 corrections govern the Prem claims.

| Resume claim | Reference | Scope retained |
| --- | --- | --- |
| Name, pronouns, phone, technical email, GitHub, Brooklyn | Personal, lines 8-22 | No availability promise. |
| Prem title and contractor status | Prem AI, lines 51-55 | June 2026 - Present is correct on the drafting date. Change to June 2026 - September 2026 on September 29. |
| 25 HTML layouts, headless Chrome, about 30 brand checks, nine shipped graphics | Prem concrete tasks, line 74 | Checks cover DOM and pixels; manifests record checks. No claim of general correctness or marketing results. |
| Remotion, React/TypeScript, 15 definitions, schema and tokens; separate writing/design rules | Prem concrete tasks, lines 75-76 | Fifteen definitions, not fifteen published films. Private repository names and URLs omitted. |
| Four product videos on a personal X account, shared by brand | Prem concrete tasks, line 81 | Four published videos. Planned series and undelivered films omitted. |
| Release coordination and checking scripts against sources | Prem concrete tasks, lines 65-67 and 84 | Live-docs check caught a false demo premise; no developer-support claim. |
| Python/SQLite publishing service, Telegram approvals, X API v2, OAuth2, Claude Agent SDK | Prem concrete tasks, lines 69-70; corrections, lines 99-104 | Agents implemented; Finn specified, reviewed and operated. Personal account posting only; active publishing July-August. |
| Two merged Fluso skills, CSV/XLSX helper, CI and package validation | Prem concrete tasks, lines 77-78 | Contributions, not independently reviewed PRs or proven manual implementation. |
| Voiceover since 2013, 1,000+ five-star reviews, audio and client workflow | Freelance Voiceover Artist, lines 285-299 | Creative/client work, not years of SaaS marketing. |
| Two theatre productions, recording, multi-camera editing, audio and color polish | Oregon Children's Theatre, lines 240-258 | May-July 2020; specific production work. |
| Production and technical skills | Skills, lines 328-350; Prem tasks, lines 69 and 74-84 | Figma is used for storyboards; React/TypeScript is supported through Remotion. |
| Blog build and API documentation | Personal Technical Blog, lines 510-522 | Links to the reviewed README. No claim of independent manual coding or live API reliability. |
| Completed BFA, CAP21 / Molloy University, 2022-2026 | Education, lines 27-34 | Completed in 2026; no exact conferral date invented. |

## Links and screening gaps

Verified public destinations:

- [GitHub profile](https://github.com/Multipixelone), opened through web retrieval.
- [Questionnaire skill and helper](https://github.com/prem-research/fluso-skills/pull/1), opened through web retrieval; the PR is merged.
- [Blog README at the reviewed revision](https://github.com/Multipixelone/blog/blob/36ce65753f99d39a025f4ebed9893b10000b86f8/README.md), opened in the browser; build and Mastodon API documentation is visible.

The supplied https://www.finnrut.is address returned a certificate-name error in the browser. It is omitted from this variant. The underlying site and other variants were not changed. No public video URLs were supplied or invented; the flagged resume-generator blog article is not featured.

The strongest remaining screening gaps are independent API integration implementation, sustained audience/signup/activation results, and the short June-September corporate content tenure. A directly viewable visual portfolio and links to the four shipped videos would make the creative claims easier to assess. These limits are outside the resume; the resume contains the supported work.

## Files and local build

- PDF: `output/pdf/sent-resume.pdf` (ignored by the repository's existing PDF rule).
- Entry: [resumes/sent.typ](../resumes/sent.typ).
- Data: [sent-metadata.toml](../metadata/sent-metadata.toml), [sent-experience.toml](../metadata/sent-experience.toml), [sent-skills.toml](../metadata/sent-skills.toml).
- Registration: one `[sent]` entry in [variants.toml](../variants.toml), with `expected_pages = 1` and `site_hidden = true`.

Used the installed Nix-managed Typst 0.15.0 and typstyle 0.15.0 directly for the single-variant build. Fetched Font Awesome 7.2.0 through the repository's pinned Nix input to resolve missing header glyphs. No system configuration was changed.

```sh
/nix/store/b0zv8qifidz1cbs47m46y5zylxqqd5yb-typstyle-0.15.0/bin/typstyle --check resumes/sent.typ

/nix/store/vry9xf6a0r9jxzzzdyrkgqqvfk5fm6gp-typst-0.15.0/bin/typst compile \
  --root . --ignore-system-fonts \
  --font-path src/fonts \
  --font-path /nix/store/f9bcl239dia95pkgdrpfcsprlibkkjyy-font-awesome-7.2.0/share/fonts/opentype \
  --input commit=local --input version=2026-09-25 \
  resumes/sent.typ output/pdf/sent-resume.pdf
```

Completed checks:

- Final compile succeeded without warnings.
- PDF has exactly one US Letter page, matching the registry.
- Rendered the final PDF with Poppler at 150 DPI and visually inspected the entire page: no clipping, overlaps, missing glyphs, or cramped skills rows.
- Extracted text using pypdf and pdfplumber, checked section/bullet reading order and key claims, and confirmed all 2,362 characters lie inside the page bounds. Header icon codepoints remain decorative; contact text extracts correctly.
- Checked the four PDF link annotations: email, GitHub profile, questionnaire PR and blog README.
- Ran the existing TOML-validity/override-key and metadata-completeness Python scripts from `packages/checks.nix` against the registry, including Sent. Both passed.
- `typstyle --check resumes/sent.typ`, `git diff --check`, and ASCII checks on all Sent Typst/TOML source passed.
- Independent review found no unsupported claims or ownership/date errors in the draft; final changes separated the graphics and motion bullets using the same reference evidence.

The full all-variant Nix package and flake checks were not run. This validation covers the local Sent PDF, its source formatting, and the shared metadata checks. No application, cover letter, commit, push, publication, or employer contact was made. Pre-existing untracked job-search notes were preserved.
