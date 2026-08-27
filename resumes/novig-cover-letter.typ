#import "../src/lib.typ": coverLetter
#import "../src/meta.typ": makeMeta
#import "../src/utils/date.typ": buildDate
#let metadata = makeMeta("novig-metadata.toml")
#let displayDate = buildDate().display(
  "[month repr:long] [day padding:none], [year]",
)

#show: coverLetter.with(
  metadata,
  // profilePhoto: image("../metadata/qr-code.png"),
)

// ── Recipient ────────────────────────────────────────────────────────────────
#let recipientName = "Hiring Manager"
#let recipientTitle = ""
#let recipientCompany = "Novig"
#let recipientAddress = "Union Square, New York, NY"

#displayDate

#v(0.5em)
#recipientCompany \
#recipientAddress

#v(0.5em)
Dear #recipientName,

I met Victoria Ordeman at the Salt & Straw in the West Village, where I coordinate shifts. We got talking, I went and read what Novig was actually building, and the Developer Relations Engineer posting is the one I want. So here I am.

Most of this year I've been a contract DevRel manager at Prem AI, and the parts that map cleanest are the unglamorous ones. Before recommending five public MCP endpoints to anyone, I hit each one with real unauthenticated JSON-RPC calls instead of trusting the docs, and wrote up the exact argument shape that made one of them fail. I designed and ran a long-lived Python service against the X API v2, with a Telegram control surface and SQLite state, packaged in Nix and tested in CI, so I know what rate limits, expiring auth, and retries do to somebody in production. Two of my pull requests are merged into Prem's public skills repo, along with the JSON schema and validator that gate it.

I read your docs before writing this. The thing I'd expect to eat a partner's first week is that a 201 on place-order means queued, not filled, so you have to consume the tape to actually confirm execution. That is the class of ticket I like: reproduce it, find the real cause, ship the fix and the doc line that keeps it from recurring.

Translating between rooms is the other half of the job. At Prem I sat between engineering, marketing, and leadership, and caught a false claim about where our servers live before it shipped. Years of campus tours and a dinner rush at Salt & Straw taught me the same skill in real time.

What I don't have: prediction-market APIs, LP relationships, an RFQ pricer. I know limit orders and time-in-force from reading, not from running a book. That's a few weeks against your QA endpoint, not a career change.

Live sports means nights and weekends. I came up in live theatre.

I'd like to talk about how I could support your partners and your engineering team.

Sincerely,

#metadata.personal.first_name #metadata.personal.last_name
