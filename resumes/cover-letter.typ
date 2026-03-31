#import "../src/lib.typ": coverLetter
#let metadata = toml("../metadata/metadata.toml")

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
  profilePhoto: image("../metadata/qr-code.png"),
)

// ── Recipient ────────────────────────────────────────────────────────────────
#let recipientName = "Hiring Manager"
#let recipientTitle = "Title"
#let recipientCompany = "Company Name"
#let recipientAddress = "123 Main St, City, State 00000"

#displayDate

// #v(0.5em)
// #recipientName \
// #recipientTitle \
// #recipientCompany \
// #recipientAddress

#v(0.5em)
// Dear #recipientName,

I'm writing to apply for the Lead performer position for your live children's shows. With my background in musical theatre, teaching, and event logistics, this role feels like a great fit.

Performing for kids means being ready for anything. I recently played the Cat in the Hat for my senior show at CAP21/Molloy University, which involved a lot of direct improvisation with the young audiences. I spent a good portion of the show breaking the fourth wall and pulling the kids into little games to keep them engaged. I actually started doing this kind of work back in Portland at the Northwest Children's Theatre, where I spent time as both a performer and a student teacher. I really enjoy the challenge of matching a room's energy while still keeping the kids focused and on track.

Beyond the performance side, I know events like this need someone who can actually manage the flow of the day. As a former House & Facilities Manager for Bridgetown Conservatory and a current Student Ambassador at my university, I'm very comfortable taking charge of a space. I have plenty of experience wrangling large groups and acting as a professional point of contact for parents and clients when things get chaotic. I also leverage my background in improv to engage students and to adapt to anything when schedules inevitably change last minute.

Since I am wrapping up my degree this spring, your weekend-based schedule works perfectly for me. I have a valid driver's license to easily commute to different venues.

Thanks for your time and consideration. I'd love the opportunity to chat more about the role and how my background can help your events run smoothly.

Sincerely,

#metadata.personal.first_name #metadata.personal.last_name
