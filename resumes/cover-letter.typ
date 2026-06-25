#import "../src/lib.typ": coverLetter
#import "../src/meta.typ": makeMeta
#import "../src/utils/date.typ": buildDate
#let metadata = makeMeta("viam-metadata.toml")
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
#let recipientCompany = "Viam"
#let recipientAddress = "New York, NY"

#displayDate

#v(0.5em)
#recipientCompany \
#recipientAddress

#v(0.5em)
Dear #recipientName,

I'm applying for the video production role on Viam's Education team. The line in the posting that got me was "no inherited toolchain, no prior workflow to maintain. You'll build it." That's the work I've already done, and it's the work I want more of.

The clearest version of it: in April 2020, I edited a virtual choir for Bridgetown Conservatory of Musical Theatre. COVID so all twenty performers were recording alone at home on whatever equipment they had. There was no workflow for this because nobody had needed one before. I built the remote capture process, synced twenty isolated video tracks, mixed the separate audio stems into one clean concert, and delivered it on a tight deadline working directly with the cast and the director. That's the muscle I'd be flexing. Figure out the production function, then run it.

Before that, I ran on-site video and audio capture for two professional theatre productions at Oregon Children's Theatre. Camera and sound rigs on shoot days, then the full edit and mix for the theatre's digital release. End-to-end from rig to final cut. I've also designed and run lighting for a live stage production, hanging and focusing the rig myself and programming the cues, so I can light a shoot, not just operate a camera. And I've produced and mixed audio for broadcast delivery. Clean capture in a room I didn't control is a problem I've already solved. When clean capture on the day isn't possible, I have a lot of experience mastering audio in post as a voiceover artist.

The part that makes this role specifically right for me, though, is the audience. Viam is a robotics engineering platform, and the Education team makes content for developers. I run a homelab of self-hosted services on NixOS, I wire LLMs into private automation, and I write Python. I can sit with an engineering team and actually follow what they're building, which means I can make tutorials that don't dumb the material down or get the technical details wrong. That combination, production skills plus engineering fluency, is rare, and it's the reason I'm writing this letter.

The storyteller instinct the posting asks for is the other half. I came up in theatre. I think about why a viewer keeps watching, not just whether the footage is clean. Pacing, hook structure, where to cut and where to let a beat breathe, that's the same problem as staging a scene. I'd rather make a tutorial that holds a developer for ten minutes than one that's technically perfect and loses them in the first thirty seconds.

I'm in New York and can be in-office three days a week. I'd be happy to discuss more of what I'm able to bring to your team.

Sincerely,

#metadata.personal.first_name #metadata.personal.last_name
