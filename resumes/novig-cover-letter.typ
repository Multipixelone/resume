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
#let recipientName = "Novig Team"
#let recipientTitle = ""
#let recipientCompany = "Novig"
#let recipientAddress = "Union Square, New York, NY"

#displayDate

#v(0.5em)
#recipientCompany \
#recipientAddress

#v(0.5em)
Dear #recipientName,

At Prem AI, I've contributed to public developer tooling and helped coordinate work between marketing and engineering. That includes two merged skills in Prem's public Fluso repository, including a questionnaire helper with Python tooling for CSV and XLSX files, plus a Python validator and CI checks for package consistency.

But the thing I enjoy the most is being a liaison between people who approach a problem differently. Working in theatre has taught me to understand when an explanation isn't landing, ask questions, and adjust my communication style. I like working through that confusion with someone until we both understand what needs to happen next.

I also specified and operated a Python publishing service using the X API. It helped me seed drafts for tweets to post on Twitter, and would send five to me each morning. I'd revise them in my own words and it would store concrete learnings about how I like to tweet. Over time, I had more and more drafts able to be posted without any revision at all.

I'd bring that combination of technical review and communication to Novig's Developer Relations Engineer role, staying involved from a partner's question through the engineering work needed to resolve it.

I haven't worked with prediction-market APIs or market makers, so I'd have a lot to learn about that part of the role. I'd welcome a conversation about how my experience in developer tooling, code review, and working across teams could contribute. I prefer working in person and am comfortable with at least four NYC office days and occasional nights and weekends.

Sincerely,

#metadata.personal.first_name #metadata.personal.last_name
