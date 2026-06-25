# Where to look + how to confirm a role is live

Two jobs: **discover** candidate roles, then **verify** each is actually open. Verification
is the part most job search gets wrong. Public ATS JSON APIs make it deterministic — no bot
detection, plain `curl`/`WebFetch` works, and you get structured fields to filter on.

## Live-check: public ATS JSON endpoints (verified working)

`<slug>` = the company's board name, usually visible in the source URL
(`jobs.ashbyhq.com/<slug>/…`, `jobs.lever.co/<slug>/…`,
`job-boards.greenhouse.io/<slug>/…`). For companies already in `nyc-job-targets.md`, mine
the slug from their `Source:` line. All four below returned `200` + real NYC roles on
2026-06-25.

```bash
# Greenhouse  (anthropic, voxmedia, thenewyorktimes)
curl -s "https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true"

# Lever  (mistral, logrocket)
curl -s "https://api.lever.co/v0/postings/<slug>?mode=json"

# Ashby  (notion, ramp, sierra, writer, agentio, elevenlabs)
curl -s "https://api.ashbyhq.com/posting-api/job-board/<slug>?includeCompensation=true"

# SmartRecruiters  (NBCUniversal3 and other large orgs)
curl -s "https://api.smartrecruiters.com/v1/companies/<slug>/postings"
```

How to use them:
- Pull the JSON, filter locally by title keywords (from `profile.md`) and location
  (NYC / New York / Brooklyn / Remote).
- A role you found via search but that is **absent** from the live board JSON is closed or
  pulled — drop it.
- These also work for **discovery on a known company**: list every open role and scan for new
  nexus fits, not just the one you searched for. This is how you catch a freshly posted DevRel
  role at a company you already track.
- Greenhouse `?content=true` and Ashby include the full description, so you often don't need a
  separate `WebFetch` for detail.

Known slugs already in the targets file: `anthropic`, `voxmedia`, `thenewyorktimes`
(Greenhouse); `mistral`, `logrocket` (Lever); `notion`, `ramp`, `sierra`, `writer`,
`agentio`, `elevenlabs` (Ashby); `NBCUniversal3` (SmartRecruiters).

## Discovery: aggregators

- **Built In NYC** — `builtinnyc.com` (used heavily in the file already). Tech + startup,
  NYC-scoped, good filters. Search via tavily/WebSearch with `site:builtinnyc.com`.
- **Tech:NYC jobs** — `jobs.technyc.org`. NYC tech ecosystem board.
- **Wellfound** (ex-AngelList) — `wellfound.com`. Startup roles; often remote-OK.
- **Hacker News "Who is Hiring?"** monthly thread, via the Algolia API (no scraping):
  ```bash
  # find this month's thread id
  curl -s "https://hn.algolia.com/api/v1/search_by_date?query=Ask%20HN%20Who%20is%20hiring&tags=story&numericFilters=points%3E100"
  # then pull its comments
  curl -s "https://hn.algolia.com/api/v1/search?tags=comment,story_<ID>&hitsPerPage=1000"
  ```
  Grep the comment text for `NYC` / `New York` / `Remote` plus role keywords.
- **Index Ventures startup-jobs** — `indexventures.com/startup-jobs` (already a source in the
  file for Hebbia). Good for funded-startup engineering roles.
- **Key Values** — `keyvalues.com` for eng-culture-forward startups.

## Discovery: company career pages (batch via tavily-map/crawl)

Companies the file flags to monitor — map their careers page to enumerate open roles, then
verify each via the ATS endpoint above:

- Perplexity — `perplexity.ai/hub/careers/new-york-city` (video/creative-technologist work)
- Synthesia — `synthesia.io/careers` (AI video, NYC office)
- Runway — `runwayml.com/careers` (Studios creative + DevRel)
- Anthropic — `job-boards.greenhouse.io/anthropic` (comms/events, all in the file)
- Mistral — `jobs.lever.co/mistral`

## Discovery: niche performance / AV / production boards

For the live-events/stage and video-production families:

- `offstagejobs.com` — technical theatre, stage management, production.
- `playbill.com/jobs` — theatre and live entertainment.
- `productionhub.com` — film/video/broadcast production crew.
- `mediabistro.com` — media, video, editorial production roles.
- ProductionHUB + Staff Me Up for freelance/contract video gigs.

## Blocked boards (do NOT scrape here)

LinkedIn, Indeed, Workday, Glassdoor front their pages with Cloudflare/Akamai. Use them only
as *discovery* signals: find the canonical posting URL via search, then either (a) verify
through the company's ATS endpoint, or (b) hand the URL to the **`render-job-url`** skill.
Never `curl`/`WebFetch` these directly, and never run two fetches in parallel against the
same domain (per render-job-url's rules).
