---
name: job-scout
description: Locate currently-open jobs at Finn's performance×technology nexus (DevRel/dev advocate, AI video & content production, production-tech/AV-tech, live events & stage) in NYC, NYC-office, or remote-OK-to-NYC. Loads when the user wants to find/scout/locate current job listings, check "what's hiring", look for new openings, or update nyc-job-targets.md. Searches live sources, confirms roles are actively hiring via public ATS APIs, dedupes against existing targets, ranks by genuine fit, and appends new entries to nyc-job-targets.md. Hands blocked boards to the render-job-url skill; does not write resume copy or build PDFs.
tools: Bash, Read, Edit, WebSearch, WebFetch
---

# Job Scout (performance × tech, NYC)

Find the next batch of live job listings that fit Finn's unusual nexus: real tech
credibility (Python, NixOS homelab, LLM automation, networking/security) plus deep
performance/production (musical theatre, voiceover, improv, on-camera, A/V editing,
audio mastering, lighting, stage management). Locate, verify, dedupe, rank, append.

## When to load

Load when the user says any of: "find/scout/locate jobs", "what's hiring", "any new
openings", "look for [role family] roles", "update job targets". Do NOT load for editing
resume copy, building PDFs, or fetching a single already-known URL (that's plain
`WebFetch`, or `render-job-url` if blocked).

## Start of every run

1. Read `profile.md` (this dir) — the fit rubric and the per-family search queries.
2. Read `boards.md` (this dir) — where to look and the live-check ATS endpoints.
3. Read `../../../nyc-job-targets.md` — the existing targets, for dedupe and numbering.
   (Skill dir is `.claude/skills/job-scout/`; the file is at the repo root.)

## The loop

1. **Search** with `tavily-search` (the project's preferred web search,
   `mcp__…websearch__tavily-search`) and `WebSearch`, using the query strings from
   `profile.md`. Bias hard to recency: last 30–45 days, "actively hiring", "open roles".
   Run the four role-family queries; add the infra fallback set only if asked for
   straight-engineering targets.
2. **Confirm live** before trusting any hit. Hit the public ATS JSON endpoint for the
   company (see `boards.md`) and check the role is actually present and open. A posting
   that 404s, is closed, or is absent from the board's live JSON is a dead lead — drop it,
   do not append it. For companies already in the targets file, the ATS slug is in their
   `Source:` line.
3. **Fetch detail** for survivors with `WebFetch`. On empty body / Cloudflare challenge /
   403 / 429 / login wall, hand the URL to the **`render-job-url`** skill. Never reimplement
   fetching here, and never scrape LinkedIn/Indeed/Workday directly — discover via search,
   then render-job-url.
4. **Dedupe** against `nyc-job-targets.md` by company + role + source URL. Skip anything
   already listed, including entries marked `APPLIED`, `No longer accepting`, or in the
   honorable-mentions / "also monitor" tails.
5. **Rank** each new role with the rubric in `profile.md`: count genuine differentiator
   matches, reward postings that invite non-exact-match applicants, and be honest about
   seniority gaps. Drop anything that would need fabricated experience to fit.
6. **Append** each surviving role to `nyc-job-targets.md` (see format below).

## Append format (match the existing file exactly)

Continue the existing numbering. Add new finds under the most fitting existing section, or
open a new dated batch header like `## Additional … Targets (<Month YYYY> research)` when
adding a fresh batch — mirror how the file already groups batches. Each entry:

```
## N. <Company> — <Role> (<location>; <comp if known>) _(status if any)_

- <what the role is, in the posting's own framing — 1-2 bullets>
- Why it fits: <which real differentiators map on; selective keyword echo, never parroted>
- Gap: <honest seniority/experience gap, if any>
- Resume: `resumes/<slug>.typ` → `<slug>-resume.pdf`
- Source: <verified live URL; ATS slug if useful>
```

Pick `<slug>` as a short company stem (e.g. `vercel`, `descript`), matching the file's
convention. The `Resume:` line is a pointer for the documented variant workflow — this
skill does NOT create the `.typ` file or touch `variants.toml`.

## Hard rules

- **Never fabricate** a listing, a detail, or a fit. If a role can't be confirmed live,
  either drop it or mark it `_(soft lead — unverified)_` exactly as entry #22 does — never
  promote an unverified lead to a normal entry.
- **Append-only** to `nyc-job-targets.md`. Never rewrite, reorder, or delete existing
  entries. Use `Edit` to add; diff should show only additions.
- **Honesty over coverage.** Finn is early-career; flag every seniority stretch. The file's
  Anthropic/Vox entries are the model for honest gap-flagging.
- **Absolute dates.** Convert "this month" / "recently" to a concrete date (today's date is
  the reference) in anything written.
- **Stay in lane.** No resume copy, no PDF builds, no applying, no form-filling.

## Reference

- `profile.md` — Finn's differentiators, per-family queries, ranking rubric.
- `boards.md` — sources + live-check ATS endpoints.
- `../render-job-url/SKILL.md` — fallback fetcher for blocked boards.
- `../../../nyc-job-targets.md` — the file this skill reads and appends to.
- `../../../CLAUDE.md` "Writing Resume Content" — the voice rules any emitted copy follows.
