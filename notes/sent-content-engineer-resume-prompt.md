# Write Finn Rutis's resume for Sent's Content Engineer role

Create a tailored, interview-defensible resume for the role below. Optimize for a recruiter seeing the connection between technical work, content, and visual craft. Complete the resume, not just a critique or plan. Use the existing Typst repository if available; otherwise produce a complete Markdown resume using the confirmed evidence in this prompt and identify anything needed to finish the PDF.

## 1. Read the sources and establish scope

Repository: `/Users/tunnel/Documents/Git/resume`. Paths below are relative to that root if your checkout is elsewhere.

Read before writing:

- `AGENTS.md`: content voice, variant structure, build instructions and conventions.
- `REFERENCE.md`: authoritative biography. Read the entire Prem AI section, including the September 9 corrections, plus skills, creative credits, education and personal projects. Its concrete facts and corrections override older resume copy and this snapshot if updated.
- `variants.toml`: the only variant registry. Check for an existing Sent variant before creating one.
- `resumes/communications-systems.typ` and `metadata/communications-systems-{metadata,experience,projects,skills}.toml`: a recent layout and corrected claims baseline, not a template to copy unchanged.
- `src/lib.typ`, `src/cv.typ`, `src/meta.typ`, and the relevant modules as needed to implement the variant.

Older company-specific resumes are not independent evidence. In particular, do not inherit unsupported claims from older creative or technical variants just because their titles resemble this job.

Keep this task focused on the Sent resume and its local build. Preserve unrelated working-tree changes. Do not submit an application, contact the employer, publish, push, or create a cover letter unless separately requested.

## 2. Understand the target

[Official Sent Content Engineer posting](https://jobs.ashbyhq.com/sent/db6bbfaf-ba52-4cec-87c8-27bf1c5b7ca7)

Verified in the live employer browser on September 25, 2026: full-time, NYC on-site, $120,000-$145,000 plus equity, with an Apply link present. Recheck the employer page before tailoring if possible. If the posting has changed, explain material differences. If unavailable, use this dated summary without claiming it is still open.

Sent offers one API for SMS, WhatsApp and RCS messaging. This role combines working API examples with technical storytelling, visual content and marketing experiments. It owns content across social and other channels, product-launch messaging, brand presence, lightweight marketing tools and measurement connecting content to signups and activated accounts.

The posting asks for 2+ years in marketing, content or creative work; ability to read API documentation and write functional integrations independently; a creative portfolio; design/UX judgment; clear writing; and an experimental approach to measuring results. Messaging-industry experience is a bonus.

Position Finn through concrete work that combines technical judgment and creative output. The material gaps are independent integration implementation, sustained growth results, and the short duration of directly relevant corporate content work. Use adjacent experience honestly; do not write an apology section into the resume.

## 3. Select and write the evidence

The following facts are a portable summary of `REFERENCE.md`, not proposed resume copy. Prioritize them by relevance and available space. Verify exact dates and wording against the current reference when the repo is available.

### Identity and education

- Finn Rutis, they/them, based in Brooklyn, NY. Use NYC in the header if space is tight.
- Technical email: tech@finnrut.is. Phone: 503-267-5052. Website: https://www.finnrut.is. GitHub: https://github.com/Multipixelone.
- BFA in Musical Theatre, CAP21 / Molloy University, 2022-2026, completed in 2026. Exact conferral date is unrecorded.
- Prefers in-person work. Exact full-time start availability is unconfirmed; omit availability promises.

### Prem AI: Developer Relations Manager (Contract)

June 2026-September 2026, remote from New York. Preserve the actual title and contractor status. The reference says to display "June 2026 - Present" until 2026-09-29, then switch to "June 2026 - September 2026". Apply that rule to the actual drafting date.

**Visual production systems, a particularly relevant lead for Sent:** Built 25 HTML graphic-layout archetypes, a headless-Chrome renderer and an auditor checking about 30 brand rules against DOM and rendered pixels. Nine investor/social graphics shipped through the system, each with a checks manifest. Built a Remotion motion renderer in React/TypeScript driven by a beats definition, with 15 film/template definitions, schema validation, and tokens generated from a shared brand canon. Fifteen definitions are not 15 published films. Separated verbal guidelines from machine-readable design rules and generated assets. Describe these systems without exposing private repository names, URLs or contents.

**Technical content and video:** Planned, shot, edited and published four videos on Finn's personal X account, shared by the brand account: a mobile-app demo, skill drop, model announcement and security-scan demo. Developed a repeatable skill-drop format; six episodes were scripted and one shipped. Wrote an intro-film script, a 29-beat Figma storyboard and an external-editor brief. The completed intro film is not evidenced. Coordinated release/content work across marketing and engineering in Linear, with shot lists, staging datasets and rendered frame cards.

**Editorial judgment:** Checked messaging against official sources, corrected hosting geography, connector counts and model terminology. A live-docs check caught a false premise in a proposed demo before filming. These are concrete accuracy decisions, not audience-growth outcomes. If describing Fluso itself, use the reference's verified framings: open-weight, 50+ connectors, Swiss-hosted.

**API publishing workflow:** Specified, reviewed and operated a Python service using SQLite, Telegram approvals, Claude Agent SDK drafting and direct X API v2 posting with OAuth2. Coding agents wrote the implementation under Finn's specifications and review. Approval froze the text. Active publishing was July-August 2026. Only Finn's personal account had a working API posting grant; brand publishing used manual copy-paste. Describe ownership clearly in the relevant bullet rather than implying solo implementation or adding a vague disclaimer elsewhere.

**Quality and review:** Triaged an agent-driven audit with 33 findings, prioritized approval/duplicate-post risks, and reviewed and shipped fixes through lint, type-check and test gates. This is not 33 completed fixes, observed failure recovery or proof of universal reliability. For this role, a compact quality-control example is likely more useful than token-refresh mechanics.

**Public developer resources:** Contributed two merged Fluso skills plus GitHub Actions, pre-commit, JSON Schema and a Python validator for package consistency. The questionnaire skill includes a CSV/XLSX helper. The contributions were self-merged without recorded independent human review; Git attribution does not establish manual implementation authorship.

- [Questionnaire skill, PR 1](https://github.com/prem-research/fluso-skills/pull/1)
- [Second skill, PR 3](https://github.com/prem-research/fluso-skills/pull/3)
- [Schema and validator](https://github.com/prem-research/fluso-skills/commit/3175fed418475872afac4f8aeba12379567a5cce)

**Optional research example:** Directed API-based competitor research covering 11 accounts and produced dated calendars and a messaging matrix. This demonstrates a research workflow, not campaign performance or pipeline attribution.

### Supporting experience and projects

- Freelance Voiceover Artist, self-employed/Fiverr, 2013-Present: 1,000+ five-star reviews; recorded, edited and delivered audio; handled quotes, client communication, schedules, revisions and delivery. This is durable creative/client evidence, not years of B2B SaaS marketing.
- Video Editor & Sound Engineer, Oregon Children's Theatre, May-July 2020: on-site video/audio recording, multi-camera editing, audio mixing and final polish for two professional productions.
- Video Editor, Bridgetown Conservatory virtual choir, April 2020: combined recordings from 20 remote performers, synced audio/video and helped cast troubleshoot recording setups. One finished performance, not a recurring production business.
- Student Ambassador, Molloy, October 2022-May 2026: campus tours, unscripted questions, admissions outreach and welcome-event support. Useful communication evidence if space permits.
- Shift Coordinator, Salt & Straw, April 2026-Present as of this research: staffing stations, training, service adjustments and guest issues. A compact additional-experience line can explain current employment; creative/technical evidence deserves more room.
- Personal infrastructure: NixOS, Flakes, Home Manager, Docker, GitHub Actions, networking and self-hosting. Keep personal projects distinct from paid employment.
- This Typst resume system and the [personal blog source](https://github.com/Multipixelone/blog) provide build, validation and documentation artifacts. The blog README is a potential writing sample. The reference flags an overclaim in the resume-generator article about checks guaranteeing correctness; do not feature that article without resolving the issue. Repo authorship alone does not prove manual coding.

### Claim boundaries

Use concrete delivered artifacts, verified counts and accurate ownership. Omit unsupported audience growth, conversion/pipeline impact, community adoption, enterprise sales, customer integrations, developer support, product-code fixes, and independent authorship of the publishing service. Do not turn planned episodes into published work or ongoing personal projects into years of professional engineering. Existing graph and review-workflow counts are not marketing results. A new Sent API demo is not part of Finn's existing experience and must not be invented.

## 4. Produce the resume and validate it

Use a concise third-person implied voice, plain ASCII punctuation, direct verbs and specific artifacts. Avoid keyword piles, inflated impact and generic enthusiasm. Make the header summary about the actual combination of content, visual systems and technical work. Preserve factual job titles; "Content Engineer" may describe the target, not replace the Prem title.

Aim for one readable page. Give Prem the most space, balancing visual systems, shipped content and technical workflow ownership. Include selected creative/client experience, a compact skills section and education. Use two pages only if necessary to preserve valuable evidence without cramped typography. Choose public links selectively and verify destinations; do not invent video URLs or portfolio samples.

With repository access, create or update a dedicated `sent` variant using the existing layout and metadata patterns. Keep overrides and data in Sent-specific files, register it once in `variants.toml`, and set the expected page count to the rendered result. Prefer `tech@finnrut.is`; omit headshot and performance-only header details. Use `AGENTS.md` for the current build process. Compile, inspect every rendered PDF page and check text extraction for clipping, missing content and broken reading order. If a build dependency is unavailable, deliver the complete source and copy with the exact blocker rather than claiming the PDF passed.

Ask only material factual questions that remain after reading the sources, and continue drafting around unknowns. Examples are links to the four published videos or any separately verifiable integration coding. Those unknowns do not block a first complete resume.

Completion means delivering:

1. The finished resume and, with a working repo environment, the compiled PDF and editable variant files.
2. A short explanation of the positioning and the strongest remaining screening gaps, outside the resume.
3. Compact evidence notes mapping material claims to `REFERENCE.md` sections or the facts supplied here, plus the build/page-count/visual checks actually completed.

Leave employer submission and public sharing to a separate request.
