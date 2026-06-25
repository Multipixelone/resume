---
name: render-job-url
description: Fallback fetcher for job posting URLs that webfetch can't render (LinkedIn, Indeed, Workday, or any board behind Cloudflare/Akamai). Loads when webfetch returned empty, blocked, or challenge content from a job URL. Renders the page with stealth Playwright (patchright) and dumps the plain text to stdout for the agent to reason about. No clicking, no applying, no structured extraction — the agent is the parser.
tools: Bash, Read
---

# Render Job URL (fallback text fetcher)

## When to load

Load this skill ONLY as a fallback, when you already tried `webfetch` (or `websearch` returned a URL whose content you couldn't fetch) on a job posting URL and got:
- an empty body,
- a Cloudflare/Akamai challenge page ("Just a moment...", "Access Denied"),
- a 403/429,
- or a login wall.

Do NOT load this skill for: Greenhouse/Lever/Ashby hosted ATS pages (webfetch works fine there), generic web research, news articles, or any non-job URL. The overhead of launching a stealth browser is wasteful when webfetch would do.

## The command

Run exactly this (the script lives in this repo; patchright lives in roomieorder's nix shell):

```bash
nix develop /home/tunnel/Documents/Git/roomieorder -c python /home/tunnel/Documents/Git/resume/scripts/fetch_job.py "<URL>"
```

The script prints the page's plain text to stdout (plus any embedded `<script type="application/ld+json">` block, delimited). Read stdout and reason about the job content directly — do not attempt structured extraction, the agent is the parser.

## Exit codes (read these before running)

- `0` — success. Plain text on stdout. Reason about it.
- `1` — bot-detected / challenge page. **NEVER retry.** A single retry against a flagged fingerprint can burn the profile. Tell the user the board blocked the fetch and they may need to wait or log in by hand (v1.1 feature).
- `2` — login wall. This board requires a logged-in profile for this URL. Tell the user; persistent profiles are a v1.1 feature.
- `3` — network/launch error. Check that `WAYLAND_DISPLAY` or `DISPLAY` is set (the script tries headless first, then escalates to a real window). A screenshot path is printed to stderr on failure.

## Rules (read these first)

1. **Never retry on exit code 1.** One retry against a flagged fingerprint makes it worse.
2. **Never run two fetches in parallel against the same domain.** Same fingerprint making concurrent requests is the signature that gets flagged.
3. **This skill only reads.** No clicking, no form-filling, no applying. If the job content isn't in the rendered text, it's not yours to get this way.
4. **Check `$DISPLAY`/`$WAYLAND_DISPLAY` before running** if there's any doubt (SSH, CI). The script tries headless first but may escalate to a headed window.

## Why not just webfetch

Most job boards (LinkedIn, Indeed, Workday) front their pages with Cloudflare or Akamai bot detection. `webfetch` has no JS execution, no cookies, no fingerprint — it gets blocked outright or returns a challenge page. This skill reuses roomieorder's anti-bot foundation (patchright, a stealth Playwright fork that closes the CDP leak stock Playwright leaves open) to render the page like a real visitor and dump the text.

## Reference

- `scripts/fetch_job.py` — the fetcher this skill invokes.
- `roomieorder.purchase.BasePurchaser._launch_context` (`purchase.py:537-567`) — the stealth launch config copied verbatim.
- `roomieorder.purchase.looks_like` / challenge markers — block/challenge detection logic imported by the script.
