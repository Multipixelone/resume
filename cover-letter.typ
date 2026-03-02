#import "./src/lib.typ": coverLetter
#let metadata = toml("./metadata/metadata.toml")

// Build date from nix inputs (falls back to today)
#let version = sys.inputs.at("version", default: none)
#let buildDate = if version != none {
  let parts = version.split("-")
  datetime(year: int(parts.at(0)), month: int(parts.at(1)), day: int(
    parts.at(2),
  ))
} else {
  datetime.today()
}
#let displayDate = buildDate.display(
  "[month repr:long] [day padding:none], [year]",
)

#show: coverLetter.with(
  metadata,
  profilePhoto: image("./metadata/qr-code.png"),
)

// ── Recipient ────────────────────────────────────────────────────────────────
#let recipientName = "Hiring Manager"
#let recipientTitle = "Title"
#let recipientCompany = "Company Name"
#let recipientAddress = "123 Main St, City, State 00000"

#displayDate

#v(0.5em)
#recipientName \
#recipientTitle \
#recipientCompany \
#recipientAddress

#v(0.5em)
Dear #recipientName,

// Write your cover letter here.

Sincerely,

#metadata.personal.first_name #metadata.personal.last_name

