# Plan: render-job-url

## Goal

A fallback text fetcher for job posting URLs that `webfetch` can't render. The agent is the extractor: the script only renders the page with anti-bot stealth and dumps plain text to stdout.

Scope is intentionally narrow. This is NOT a resume-tailoring pipeline, NOT a selector catalog, and NOT a structured-JSON producer.

## v1 (shipped)

- `scripts/fetch_job.py` — anonymous stealth fetch using patchright in roomieorder's Nix shell.
- Plain text to stdout, plus delimited `application/ld+json` blocks when present.
- Exit codes: `0` success, `1` bot-detected/challenge, `2` login wall, `3` network/launch error.
- Temp profile per run; no persistent auth cookies in v1.
- Imports block/challenge markers from `roomieorder.purchase` so detection stays in sync.
- `SKILL.md` (~60 lines) — load only as a fallback after `webfetch` fails on a job URL.

## What was cut from the original plan and why

- **Per-platform selector catalog** — the agent reads the rendered text; selectors rot and over-fit.
- **Structured JSON schema** — the agent extracts what it needs; no rigid schema to maintain.
- **Multi-board profile setup** — v1 is anonymous-first. Logged-in boards are a v1.1 problem.
- **Resume-tailoring integration** — downstream consumer, not this skill's job.
- **`just scrape-job` wrapper** — direct invocation is one line already; wrappers add indirection.
- **Persistent profiles** — deferred to v1.1 to keep v1 small and safe.

## v1.1

- `roomieorder fetch-url <URL>` CLI command — single source of truth for launch config + block detection, imported from the same Python module the skill uses.
- Persistent logged-in profiles in `~/.local/share/jobscout/<site>/` (XDG, outside repo) for boards that require login.
- Profile locking so two agents can't race the same profile against the same domain.

## v2 (maybe never)

Per-platform extractors with regression fixtures — only if the agent consistently fails to parse a specific board's rendered text.

## Open questions

None blocking v1.
