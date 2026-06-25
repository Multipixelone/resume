#import "../src/lib.typ": coverLetter
#import "../src/meta.typ": makeMeta
#import "../src/utils/date.typ": buildDate
#let metadata = makeMeta("nyt-tech-specialist-metadata.toml")
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
#let recipientCompany = "The New York Times"
#let recipientAddress = "New York, NY"

#displayDate

#v(0.5em)
#recipientCompany \
#recipientAddress

#v(0.5em)
Dear #recipientName,

I'm applying for the News Technology Specialist role on the Video team. What I want is the work behind the journalism, keeping the cameras, the edit systems, and the feeds running so smoothly, nobody is even sure I've done anything at all. Things break at the worst moment and they have to be fixed now. That's the work I've already been doing, on a smaller stage.

In April 2020 I cut a virtual choir for Bridgetown Conservatory. Twenty performers, all recording alone at home on whatever they had, lockdown deadline. There was no workflow because nobody had needed one. I built the remote capture process, then handled dropped files, sync drift, out-of-spec recordings as they came in. Synced twenty isolated tracks. Delivered on schedule. Ingest, fix, produce, export. That's the discipline this role runs on.

A few months later I ran on-site video and audio capture for two productions at Oregon Children's Theatre. Camera positions, mics, a recording setup I could trust, then the full cut in Premiere with motion graphics in After Effects, handoff for digital release. I also designed and ran lighting for The Rosetta Project, hanging and focusing the rig and programming the cues, and mixed audio to broadcast delivery for the Portland Spirit. All live work, no second takes. Live theatre teaches you that everything breaks at showtime, so you build it to be fixable fast and you stay calm when it does. A Wednesday-to-Sunday news cycle with a Monday studio reset is a rhythm I already know.

On the facilities side, I ran front-of-house for a year at Bridgetown, keeping the theatre and rehearsal spaces show-ready and acting as the main contact for patrons, renters, and building management. Resetting the room and having the gear ready for the next thing is work I've done for a living. Weekend calls, rooms to reset, someone who needs gear at a weird hour. I've been that person.

The IT and networking side is another reason I'm writing. I run a homelab of dozens of internet-facing services on NixOS, built on a FortiGate firewall with separate DMZs and isolated VLANs. I understand ingest and transcode pipelines as a systems problem, not just a media one, because I've built infrastructure that follows the same ingest-process-export shape. Most of my stack is self-hosted, but the thinking is declarative and reproducible, which is the same muscle cloud work asks for. When a feed won't push or a transcode fails, I can read the network and the system, not just the editing app. Real production experience plus real IT depth in one person is rare.

I'm in New York and the Wednesday-to-Sunday hybrid schedule works great for me. Happy to talk through more of what I'd bring to the team.

Sincerely,

#metadata.personal.first_name #metadata.personal.last_name
