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

Confirm before proceeding: you have read `profile.md` (queries + differentiators),
`boards.md` (ATS endpoints + discovery sources), and `nyc-job-targets.md` (existing
entries + numbering). If any are missing, stop and read them now.

## The loop

1. **Search** with `tavily_search` (available via MCP; check your tool list for the
   exact name, typically `mcp__websearch__tavily_search`) and `WebSearch`, using the
   query strings from `profile.md`. Other MCP search tools available: `tavily_extract`,
   `tavily_map`, `tavily_crawl`, `tavily_research`. Bias hard to recency: last 30–45
   days, "actively hiring", "open roles". Run the four role-family queries; add the
   infra fallback set only if asked for straight-engineering targets.
2. **Confirm live** before trusting any hit. Hit the public ATS JSON endpoint for the
   company (see `boards.md`) and check the role is actually present and open. A posting
   that 404s, is closed, or is absent from the board's live JSON is a dead lead — drop it,
   do not append it. For companies already in the targets file, the ATS slug is in their
   `Source:` line.
2b. **Find the ATS slug** if the company isn't already in the targets file. Extract
    it from the careers URL: Greenhouse follows `job-boards.greenhouse.io/<slug>/`,
    Ashby follows `jobs.ashbyhq.com/<slug>`, Lever follows `jobs.lever.co/<slug>`,
    SmartRecruiters follows `jobs.smartrecruiters.com/<slug>`. If the company uses
    none of these ATSes, fall back to WebFetch or `render-job-url` and mark the entry
    `_(soft lead — unverified)_`.
3. **Fetch detail** for survivors with `WebFetch`. On empty body / Cloudflare challenge /
   403 / 429 / login wall, hand the URL to the **`render-job-url`** skill. Never reimplement
   fetching here, and never scrape LinkedIn/Indeed/Workday directly — discover via search,
   then render-job-url.
4. **Dedupe** against `nyc-job-targets.md`:
   - Match on internal requisition ID first (Greenhouse: `id`, Lever: `id`,
     Ashby: `id`, SmartRecruiters: `id`) — the most reliable key.
   - Fall back: company + normalized role title + source domain.
   - Normalize titles by lowercasing and stripping parentheticals before comparison
     (e.g., "Developer Advocate, Events & Social (NYC)" → "developer advocate events social").
   - Skip anything already listed, including `APPLIED`, `No longer accepting`,
     honorable-mentions, and "also monitor" entries.
   - If an existing entry's status is not marked `APPLIED`, `REJECTED`, or
     `No longer accepting`, and it's >60 days old, re-verify it against the ATS
     endpoint before treating it as a dedupe match. Stale open entries may be closed.
5. **Rank** each new role with the rubric in `profile.md`: count genuine differentiator
   matches, reward postings that invite non-exact-match applicants, and be honest about
   seniority gaps. Drop anything that would need fabricated experience to fit.

   Before writing any "Why it fits" line, re-read the relevant sections of
   `metadata/work-experience.toml`, `metadata/tech-projects.toml`,
   `metadata/tech-skills.toml`, and any variant-specific TOML you plan to
   reference. Each claimed differentiator must map to a concrete entry in
   these files. If you cannot point to a specific entry, do not make the claim.

   Before finalizing any entry for an AI-video or creative-production role, verify
   no AI-video tool experience is claimed (Runway, Pika, CapCut AI — per `profile.md`).
   If the posting asks for these, flag it as a Gap, don't fabricate.

   After writing the entry, re-check each "Why it fits" claim against the TOML files
   one more time. If a claim doesn't correspond to a concrete entry, remove it.
6. **Append** each surviving role to `nyc-job-targets.md` (see format below).
6b. **Validate the Resume pointer.** Read `variants.toml`. If the slug you chose is
    already registered as a variant, write the `Resume:` line normally. If not, append
    `_(variant not yet created)_` to the Resume line so the user knows the `.typ` file
    needs to be built before `nix build` will include it.

## Append format (match the existing file exactly)

**Numbering rules by section type:**
- **Main numbered section** (1–22): continue with `## 23.`, `## 24.`, etc.
- **Lettered sub-sections** (e.g. Anthropic A–C): continue with the next letter for
  that company. A new company gets its own `# <Company> — <Theme> Targets` header
  and fresh `## A.` numbering.
- **"Additional … Targets" batches**: use the existing batch header convention
  (`## Additional … Targets (<Month YYYY> research)`) with sequential numbering
  continuing from the highest existing number.
- **Honorable mentions / Also monitor**: append bullets, not numbers or letters.

Each entry:

```
## N. <Company> — <Role> (<location>; <comp if known>) _(status if any)_

- <what the role is, in the posting's own framing — 1-2 bullets>
- Why it fits: <which real differentiators map on; selective keyword echo, never parroted>
- Gap: <always include; write "None — early-career-appropriate" when the role is
  genuinely junior/mid-level. Otherwise describe the honest gap.>
- Resume: `resumes/<slug>.typ` → `<slug>-resume.pdf`
- Source: <verified live URL; ATS slug if useful> _(verified live YYYY-MM-DD)_
```

Pick `<slug>` as a short company stem (e.g. `vercel`, `descript`), matching the file's
convention. The `Resume:` line is a pointer for the documented variant workflow — this
skill does NOT create the `.typ` file or touch `variants.toml`.

Slug convention: use the company stem alone (e.g. `vercel`, `descript`) when the
company has only one target role. Use `<company>-<role>` (e.g. `vox-unexplainable`,
`nyt-tech-specialist`) when the company has multiple distinct targets. Match the
existing file's pattern.

**Em-dash scope:** CLAUDE.md's "No em dashes, ever" rule applies to resume copy
(.typ files, TOML descriptions, header quotes). Em dashes are allowed and expected
in `nyc-job-targets.md` headings and entry body text to match existing file style.

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
