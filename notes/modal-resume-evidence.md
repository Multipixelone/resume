# Modal resume: evidence and validation

Drafted September 25, 2026 for the supplied Developer Relations Engineer, AI Sandbox Content role.

## Posting status

The matching employer listing is [Developer Relations Engineer, Sandboxes](https://jobs.ashbyhq.com/modal/5113f35e-988d-41bc-a899-3261a9454e40). Its indexed description remains available, but the live browser page returned "Job not found" on September 25. This resume does not establish that the role is still open.

The indexed employer description adds requirements absent from the supplied summary: building systems that execute generated code in isolated environments, at least one year with ML/LLMs/agentic systems, partner work, and measuring initiative impact. It listed NYC, San Francisco and Stockholm, on site.

The live [Modal careers board](https://jobs.ashbyhq.com/modal) instead lists a general [Developer Relations Engineer](https://jobs.ashbyhq.com/modal/546c9eb1-aaf7-47ba-8e9d-0bcd443b3e94) role in San Francisco and London. The resume remains tailored to the supplied Sandboxes role; no relocation commitment or availability was inferred.

## Positioning and claim map

The page leads with published demos and public developer resources, then explains specifications, review and operation of an agent-written service. Personal LLM tools and Linux infrastructure provide technical context. University tours supply live-presentation evidence in their actual setting.

All biographical claims trace to [REFERENCE.md](../REFERENCE.md), using these sections and line numbers as read on September 25:

| Resume material | Reference | Boundary |
| --- | --- | --- |
| Identity, technical email, GitHub and Brooklyn | Personal, 8-22 | No availability promise. |
| Prem title, contractor status and dates | Prem AI, 51-55 | June 2026 - Present until September 29; then use June 2026 - September 2026. |
| Four videos, skill-drop format and one shipped episode with skill file | Prem tasks, 81-82 | Personal X account, shared by brand. No additional published episodes implied. |
| Live documentation check before filming | Prem tasks, 65-68 | Accuracy decision, not developer support or integration troubleshooting. |
| Two public skills, CSV/XLSX helper, schema, validator and CI | Prem tasks, 77-78 | No inferred manual implementation or independent human PR review. |
| Release/content coordination in Linear | Prem tasks, 84 | Marketing and engineering coordination. |
| Python/SQLite, Claude Agent SDK, Telegram approvals, X API v2 and OAuth2 | Prem tasks, 69-70; corrections, 99-104 | Coding agents implemented; Finn specified, reviewed and operated. Personal-account posting, active July-August. |
| Audit with 33 findings and fixes through CI | Prem tasks, 71 | Findings, not 33 fixes. No observed recovery or universal reliability claim. |
| Campus tours, unscripted questions, outreach and welcome events | Student Ambassador, 147-169 | University work, not developer conferences or community management. |
| Personal Python/LLM tools, structured JSON, parsing and script generation | AI-Driven Automation Pipelines, 531-536 | Personal project since January 2023, not professional SWE tenure. |
| Personal services, Docker, ESXi, KVM, NixOS and Flakes | Personal Tech Projects, 494-500 | Self-hosting since November 2016, not AI-sandbox expertise. |
| Blog build/API documentation sample | Personal Technical Blog, 510-522 | Reviewed README, not the article flagged for an overclaim. |
| Technical/content skills and completed BFA | Skills, 328-350; Education, 27-34 | Completed 2026; no conferral date invented. |

The strongest screening gaps are unconfirmed three years of professional software engineering, independent implementation of the main agentic service, and work with Modal or isolated AI code execution. Developer-community support, conference talks and measured adoption outcomes are also not established. These gaps are kept outside the resume.

## Public links

The PDF includes the GitHub profile, [questionnaire PR](https://github.com/prem-research/fluso-skills/pull/1), [schema/validator commit](https://github.com/prem-research/fluso-skills/commit/3175fed418475872afac4f8aeba12379567a5cce), and [blog README](https://github.com/Multipixelone/blog/blob/36ce65753f99d39a025f4ebed9893b10000b86f8/README.md). All destinations were verified in this conversation; the validator commit was checked during the Modal task. The personal website remains omitted following its September 25 certificate-name error. No video links were invented.

## Files and checks

- PDF: `output/pdf/modal-resume.pdf` (ignored by the existing repository rule).
- Entry: [resumes/modal.typ](../resumes/modal.typ).
- Data: [metadata](../metadata/modal-metadata.toml), [experience](../metadata/modal-experience.toml), [projects](../metadata/modal-projects.toml), [skills](../metadata/modal-skills.toml).
- One `[modal]` entry in [variants.toml](../variants.toml), `expected_pages = 1`, `site_hidden = true`.

Built locally using the existing Nix-managed tools and fonts:

```sh
/nix/store/vry9xf6a0r9jxzzzdyrkgqqvfk5fm6gp-typst-0.15.0/bin/typst compile \
  --root . --ignore-system-fonts \
  --font-path src/fonts \
  --font-path /nix/store/f9bcl239dia95pkgdrpfcsprlibkkjyy-font-awesome-7.2.0/share/fonts/opentype \
  --input commit=local --input version=2026-09-25 \
  resumes/modal.typ output/pdf/modal-resume.pdf
```

Final compile passed without warnings. The PDF is one US Letter page, matching the registry. The full final page was rendered with Poppler at 150 DPI and visually reviewed for spacing, glyphs, clipping and overlap. Text extraction with pypdf and pdfplumber confirmed all 17 job/project/skill copy fields, correct section and bullet order, and all 2,441 characters within page bounds. Five link annotations match the intended destinations, including email.

`typstyle --check resumes/modal.typ`, ASCII source checks and `git diff --check` passed. The existing TOML-validity/override-key and metadata-completeness scripts from `packages/checks.nix` passed against the full registry. An independent factual review found no unsupported claims. The all-variant Nix package and full flake checks were not run.

Sent files and pre-existing job-search notes were preserved. No application, cover letter, commit, push, publication or employer contact was made.
