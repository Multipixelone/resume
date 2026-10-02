#import "../src/lib.typ": coverLetter
#import "../src/meta.typ": makeMeta
#import "../src/utils/date.typ": buildDate

#let metadata = makeMeta("astor-place-metadata.toml")
#let displayDate = buildDate().display(
  "[month repr:long] [day padding:none], [year]",
)

#show: coverLetter.with(metadata)

#displayDate

#v(0.5em)
Astor Place Theatre \
New York, NY

Dear Astor Place Theatre team,

I'm applying for the Assistant House Manager/Ticket-Taker position. I spent a year running front-of-house and facilities at Bridgetown Conservatory of Musical Theatre in Portland, and I now coordinate service shifts at Salt & Straw in the West Village. I'd like to bring that experience back into a theatre as you welcome new productions to Astor Place.

At Bridgetown, I handled ticketing, ushering, the lobby, and intermission. I opened and closed the venue, kept the spaces clean and stocked, and was the person patrons and renters came to when something went wrong. Most shifts were solo, so I got used to making decisions and taking responsibility for the building. At Salt & Straw, I assign stations, train new hires, and resolve guest issues while service is busy. I also open and close the shop solo on some shifts.

I also completed my BFA in Musical Theatre at CAP21 / Molloy University this year. I've worked on both sides of the curtain, and I like the practical work of getting a room ready and helping people feel welcome in it.

I'm based in Brooklyn, available evenings and weekends, and comfortable being the last person to close up. I use Word, Excel, and Outlook, and I'm willing to obtain the required F-03, F-07, and S-95 certificates. I'd welcome the chance to talk about joining your front-of-house team.

Thank you,

#metadata.personal.first_name #metadata.personal.last_name
