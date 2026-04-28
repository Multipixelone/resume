#import "../src/lib.typ": coverLetter
#import "../src/meta.typ": makeMeta
#import "../src/utils/date.typ": buildDate
#let metadata = makeMeta("saltandstraw-metadata.toml")
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
#let recipientCompany = "Salt & Straw"
#let recipientAddress = "Hudson, New York City, NY 10014"

#displayDate

#v(0.5em)
#recipientCompany \
#recipientAddress

#v(0.5em)
Dear #recipientName,

I am writing to express my interest in the Shift Coordinator position at Salt & Straw's new New York City location. My connection to your brand is personal, and I think that history, combined with real experience keeping teams and guests on track, makes me a good fit for this role.

One of the fondest memories I have as a child was my mother surprising me and two of my friends in elementary school with a trip into the city. Growing up in Portland, that meant a hike through Forest Park, with our reward being a trip to the "hip new ice cream parlor" everyone was talking about. The line at that first, solitary shop was already legendary, stretching clear around the block. When we got to the front, my mind was immediately blown by all the eclectic flavors. The first cup I ever got was a scoop of the olive oil ice cream, and I fell in love with every flavor combination Salt & Straw was creating.

That day, I learned that Salt & Straw isn't just about ice cream. It's about the adventure to get there, the joy of discovery in every flavor, and the community you build while waiting in line. That experience shaped how I think about hospitality: the product matters, but the people running the room matter just as much.

I've spent the last few years doing exactly that. At Bridgetown Conservatory of Musical Theatre, I ran front-of-house solo for live shows: opening and closing the space, managing whatever came up mid-event, and making sure every patron left satisfied. That meant staying calm when things went sideways, making decisions on the fly, and keeping the whole operation moving without anyone else to hand problems off to. At Molloy University, I give campus tours and help run open houses, which means reading a room quickly and adjusting on the spot.

New York is my home now. Hearing Salt & Straw was coming here felt personal, a piece of where I'm from showing up in the place I've built my life. I want to be part of the team that opens this location right. Not just on the floor, but helping make sure the shift runs well and the people working it feel supported.

Thank you for your time. I'd love to talk about how I can contribute to your New York team.

Sincerely,

#metadata.personal.first_name #metadata.personal.last_name
