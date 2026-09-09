# Novig cover-letter revision prompt

Paste the block below into the Astra agent you select with Ultra reasoning. This requests draft options first; it does not authorize submission or changes to the letter file.

```text
Help me revise my cover letter for Novig's Developer Relations Engineer role. Produce two honest, distinct options before editing the letter. Optimize for recruiter credibility and interview defensibility, not keyword matching. My name is Finn Rutis.

READ BEFORE DRAFTING

The repository is /Users/tunnel/Documents/Git/resume. Read AGENTS.md, then:
- resumes/novig-cover-letter.typ: existing draft, whose voice is useful but whose claims need correction.
- metadata/novig-experience.toml, novig-projects.toml, novig-skills.toml, and novig-metadata.toml: current resume content.
- REFERENCE.md: especially Prem AI, the September 9, 2026 corrections, Novig application context, and the blog evidence section. These corrections supersede earlier drafts and September 6 claims.
- dist/novig-review/novig-resume.pdf, if available, for what the recruiter will actually see.

If you cannot access these files, ask me for the current letter, current resume, and the relevant sanitized REFERENCE.md excerpts. Do not pretend to have reviewed unavailable files or ask for private interview notes. After receiving them, proceed without a broad questionnaire.

ROLE INTERPRETATION

Treat this as partner/solutions engineering for a live exchange: owning API integrations and technical relationships, reproducing issues in code, translating across partners, operations, and engineering, and contributing fixes. Content, advocacy, and community work are secondary. Novig wants prediction-market API experience, order-type fluency, and credibility with market makers and liquidity providers; an RFQ pricer is a plus.

Posting: https://novig.com/careers/developer-relations-engineer-719dc7
Official API documentation: https://docs.novig.com/

Verify current official sources if using specific company or API claims. Omit unnecessary funding, regulatory, and investor details. Reading documentation does not establish practical experience. Do not turn the observation that order acceptance differs from execution into an invented support incident, or assert that a particular integration issue will consume a partner's first week.

CONFIRMED EVIDENCE AND LIMITS

My Prem title is Developer Relations Manager (Contract), June 2026 to Present as of September 9. Follow REFERENCE.md's date instructions; do not silently alter titles or dates.

I specified and operated a Python publishing service with SQLite state, Telegram approvals, and a direct X API v2 client using OAuth2 user-context authentication. Coding agents wrote the implementation. I wrote specifications, reviewed the implementation, and operated the service. Approved posts used text frozen at approval. Active publishing was July-August 2026; do not imply current active posting.

I triaged 33 findings from an agent-driven audit, prioritized approval and duplicate-post risks, dispatched fixes, and reviewed and shipped fixes through lint, type-check, and test gates in CI. Mechanisms included compare-and-swap state transitions, crash reconciliation, and serialized token refresh with atomic persistence. Select only the details needed to explain my judgment and ownership. Thirty-three findings does not mean 33 completed fixes. Tested mechanisms do not prove successful recovery during a real incident, exactly-once delivery, or complete reliability.

I contributed two merged skills and CI/validation tooling to Prem's public Fluso repository:
- Questionnaire helper, including Python CSV/XLSX tooling: https://github.com/prem-research/fluso-skills/pull/1
- Second merged skill: https://github.com/prem-research/fluso-skills/pull/3
- Schema and validator: https://github.com/prem-research/fluso-skills/commit/3175fed418475872afac4f8aeba12379567a5cce
- CI workflow: https://github.com/prem-research/fluso-skills/commit/3e6244709899f440222499001f24d28f8f2cf88c
These were self-merged without recorded independent human reviews. Git attribution does not establish manual code authorship. I also coordinated across marketing and engineering and corrected inaccurate product claims before internal distribution.

My personal infrastructure and resume tooling provide supporting technical evidence. https://github.com/Multipixelone/blog provides public documentation, a Mastodon reader, and Python validators. The blog review establishes code and documentation artifacts, not manual authorship, observed debugging, adoption, or production reliability. Keep personal projects distinct from professional work.

I have no sports engagement or relevant community participation, and no evidenced prediction-market API work, trading-system operations, market-maker/LP relationships, or RFQ pricing. I prefer working in person and accept four NYC office days and occasional nights/weekends. My BFA was completed in 2026; exact full-time availability is unconfirmed.

REQUIRED CORRECTIONS

Remove the draft's MCP troubleshooting anecdote, personal authorship of token rotation, unofficial-to-official API migration, claims of two live posting grants, and unsupported production retry/rate-limit expertise. Do not imply customer integrations, developer support, partner ownership, or Prem product-code PRs/hotfixes. Do not cite codebase size or test counts as my output or as coverage. Do not promise a few weeks in a QA environment will close the domain gap.

You may retain the Victoria Ordeman/Salt & Straw encounter as stated in the existing draft. Do not add a job title for her or imply a referral, endorsement, interview invitation, or offer. If another source contradicts the name or encounter, omit the disputed detail and ask one concise question.

Never include private repository names/URLs, internal tickets, customer details, or private interview-preparation anecdotes. Do not add these to this repository. Do not invent sports enthusiasm or substitute generic enthusiasm for evidence.

DELIVERABLE

1. Briefly diagnose the existing draft's most consequential weaknesses.
2. Write two complete letters, each 180-250 words excluding salutation/signature: A leads with technical specifications, operation, and review; B leads with public developer tooling and communication across teams. Use one or two concrete examples, explain transferable relevance, and acknowledge the domain gap proportionately without an apology list or a claim it is trivial.
3. Recommend one and explain why. Include concise evidence notes outside the letters, citing exact file sections or public artifacts for material claims and distinguishing direct from transferable evidence.
4. Ask at most two material factual questions after drafting. Omit unconfirmed details from the drafts rather than filling them with guesses.

Keep the voice direct, human, slightly casual, and technically specific. Preserve useful warmth from my original without hype, flattery, em dashes, buzzwords, or bravado. Do not rewrite the resume. Do not edit the cover-letter file until I choose an option. Do not submit, contact anyone, publish, push, or make external changes.
```
