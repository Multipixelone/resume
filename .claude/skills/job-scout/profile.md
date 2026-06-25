# Finn's nexus: fit rubric + search queries

This is the search ammo and the ranking rubric. Every fact here is drawn from the repo's
own data (`metadata/tech-skills.toml`, `metadata/tech-projects.toml`,
`metadata/work-experience.toml`). Do not add skills or experience that aren't here.

## The nexus in one line

An infrastructure/security engineer who can also hold a room: runs a self-hosted NixOS
homelab and wires LLMs into reproducible automation, and has years on stage plus end-to-end
A/V production (record, edit, mix, master, light, stage-manage). The rare candidate who is
credible to developers *and* comfortable on camera / on a mic / in front of a crowd.

## Differentiators to match (the hooks worth more than a keyword)

Tag = which role family each one powers most. Match a posting against these; the more it
genuinely needs, the better the fit.

- **NixOS homelab + declarative infra** (dozens of internet-facing self-hosted services,
  FortiGate firewall, VLANs/DMZs, MetalLB, ESXi/KVM/Docker, Flakes/Home Manager). → DevRel,
  production-tech. Real engineering credibility, not a bootcamp resume.
- **LLM automation in Python** (tight system prompts, strict JSON schemas, reliable
  parse-and-act tooling). → DevRel at AI/dev-tool companies; "active Claude/LLM user" asks.
- **Audio mixing + mastering** (broadcast-ready theme song for Portland Spirit; Logic,
  Reaper, Audacity). → genuine audio credibility at audio companies (the ElevenLabs angle),
  podcast/audio production.
- **Virtual-choir remote A/V sync** (20 isolated performers, edited and synced to one
  concert on a tight pandemic deadline, working with cast + director). → AI video/creative
  production, podcast video, remote-host directing.
- **On-site video + audio recording & editing** (Oregon Children's Theatre, two pro
  productions; Final Cut, DaVinci, Premiere). → video producer/editor roles.
- **Lighting design + stage management** (Rosetta Project: hung, focused, programmed, ran
  cues live; Bridgetown front-of-house + facilities). → live events / stage, technical
  producer.
- **Improv + on-camera + voiceover** (musical theatre performer, voiceover artist). →
  talent coaching, hosting, on-camera teaching, "comfortable on camera" asks across all
  families.
- **Student Ambassador / event hosting** (guided tours, ran welcome events, daily
  outreach). → community engagement, experiential, devrel events.

Toolset confirmed (claim only these on the A/V side): Final Cut Pro, DaVinci Resolve,
Premiere Pro; Logic Pro, Reaper, Audacity. **No AI-video tool experience** (Runway, Pika,
CapCut AI) — never claim it.

## Geography filter

Keep: NYC, "New York", Brooklyn, NYC office/hub, hybrid-NYC, remote roles open to US/NYC.
Drop: roles requiring relocation away from NYC with no remote option, non-US-only.

For remote-US roles: verify the company allows NY-based employment (some remote roles
exclude NY due to tax-withholding complexity). If the posting says "remote US" but the
ATS JSON's location field excludes NY, drop it. Also check timezone expectations;
Pacific Time roles requiring 9am PT synchronous work are a stretch from ET.

## Per-family search queries

Run these through `tavily-search` and `WebSearch`. Echo the posting's *concepts*, not its
exact phrasing, when you later write the entry (see CLAUDE.md). Append a recency nudge like
`posted 2026` or `actively hiring` to bias fresh.

**1. DevRel / Developer Advocate** (strongest overlap)
```
("developer advocate" OR "developer relations" OR devrel OR "developer experience") (NYC OR "New York" OR remote) (AI OR LLM OR "developer tools" OR "developer platform")
```

**2. AI video / creative production**
```
("video producer" OR "content producer" OR "video editor" OR "creative producer") (AI OR startup OR "media company") (NYC OR "New York" OR Brooklyn)
```
Audio variant: `("podcast producer" OR "audio producer" OR "audio engineer") (NYC OR "New York")`

**3. Production-tech / AV-tech** (the NYT News Technology Specialist pattern — best
tech+production blend)
```
("technology specialist" OR "broadcast engineer" OR "production technology" OR "media systems engineer" OR "AV engineer" OR "production engineer") video (NYC OR "New York")
```

**4. Live events / stage**
```
("stage manager" OR "technical producer" OR "show caller" OR "event content manager" OR "experiential producer") (NYC OR "New York")
```

**Additional titles to search** (scatter across relevant families; surface roles that
match the profile but use titles not covered by the primary queries):
```
("technical writer" OR "solutions engineer" OR "community manager") (NYC OR "New York" OR remote)
("event producer" OR "production coordinator" OR "technical director") (NYC OR "New York")
("AV technician" OR "broadcast technician" OR "media technician") (NYC OR "New York")
```

**Infra fallback** (use only when straight-engineering high-pay targets are wanted — the
Hebbia/Runway-backend pattern):
```
("backend engineer" OR "platform engineer" OR "infrastructure engineer") (NYC OR "New York") (startup OR AI) (Python OR Linux OR Nix)
```

## Ranking rubric (apply per candidate role)

Score and order new finds by:

1. **Differentiator count** — how many hooks above the posting genuinely uses. Two or more
   real matches = strong. One = worth a variant. Zero = skip.
2. **Invites non-exact-match applicants** — postings that say "you don't need to check every
   box" rank up; Finn's profile is unconventional by design.
3. **Seniority honesty** — mechanical thresholds:
   - 0–4 yrs required: no guardrail (early-career-appropriate).
   - 5–7 yrs required: keep only if ≥2 genuine differentiators match AND the Gap
     field is non-empty with an honest assessment. Drop otherwise.
   - 8+ yrs required: keep only if ≥3 genuine differentiators match AND the Gap
     field is non-empty. Otherwise relegate to Honorable Mentions.
   Never paper over years-of-experience with fabrication.
4. **Performance is a real asset, not decoration** — prefer roles where on-camera / on-stage
   / talent-coaching is in the job description, not just nice-to-have.
5. **Tie-break** toward NYC-in-person > NYC-hybrid > remote-OK, and toward AI / dev-tool /
   media companies where the tech spine reads as on-mission.

## Never-fabricate guardrail

When you later write the entry's "why it fits" line, follow CLAUDE.md "Writing Resume
Content": plain verbs, no "leveraged/spearheaded/orchestrated", no stacked buzzwords, no em
dashes in resume copy, one or two keyword echoes max, concrete detail over abstraction. Foreground real
experience; never invent a responsibility, a tool, or a year of seniority that isn't above.

Before writing a "Why it fits" line, re-read the source TOML files. Cite the
specific entry (e.g., "work-experience.toml `[jobs.virtual-choir]`") that maps
to each differentiator. If no entry maps, don't claim the fit.
