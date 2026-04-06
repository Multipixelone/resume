#import "../src/lib.typ": coverLetter
#import "../src/meta.typ": makeMeta
#let metadata = makeMeta("saltandstraw-metadata.toml")

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
  // profilePhoto: image("../metadata/qr-code.png"),
)

// ── Recipient ────────────────────────────────────────────────────────────────
#let recipientName = "Hiring Manager"
#let recipientTitle = ""
#let recipientCompany = "Salt & Straw"
#let recipientAddress = "Hudson, New York City, NY 10014"

#displayDate

#v(0.5em)
#recipientCompany \
#recipientAddress

#v(0.5em)
Dear #recipientName,

I am writing to express my enthusiastic interest in the scooper position for Salt & Straw's new New York City location. My connection to your brand is deeply personal, and I believe my passion for the experience you create makes me an ideal candidate to help introduce Salt & Straw to New York.

One of the fondest memories I have as a child was my mother surprising me and two of my friends in elementary school with a trip into the city. Growing up in Portland, that meant a hike through Forest Park, with our reward being a trip to the "hip new ice cream parlor" everyone was talking about. The line at that first, solitary shop was already legendary, stretching clear around the block. When we got to the front, my mind was immediately blown by all the eclectic flavors. The first cup I ever got was a scoop of the olive oil ice cream, and I immediately fell in love with all of the flavor combinations that Salt & Straw was creating.

That day, I learned that Salt & Straw isn't just about ice cream. It's about the adventure to get there, the joy of discovery in every flavor, and the community & excitement you build while waiting in line. This understanding is exactly what I would bring to your team. I am passionate about learning the stories behind each flavor and sharing them with customers, and I am dedicated to creating the same welcoming environment that I experienced all those years ago.

While I was born in Portland, New York is my home. Hearing that Salt & Straw was coming to this city wasn't just exciting, it felt personal. It means a piece of my past is becoming part of my future.

But this isn't just about enjoying my favorite flavors again. It's about introducing them to the people I hold dear on this coast. More than anything, I want to be on the front lines of that introduction. I want to be part of the team that gets to see the look of delight on a new customer's face---the same joy I felt as a kid. I am ready to help you share that experience, one scoop at a time, bringing my enthusiasm and customer-focused attitude to every shift.

Thank you for your time and consideration! I am eager to discuss how my lifelong appreciation for Salt & Straw can contribute to the success of your New York team for years to come.

Sincerely,

#metadata.personal.first_name #metadata.personal.last_name
