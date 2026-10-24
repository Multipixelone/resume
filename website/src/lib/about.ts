import { dev } from '$app/environment';

export interface Escapade {
  /** Optional heading over the blurb. Without one the entry is just its text. */
  title?: string;
  /** Blank lines split it into paragraphs. Backtick strings take apostrophes and line breaks as is. */
  blurb: string;
  /** Optional print beside the text, from static/media/. Without one the entry is a paper slip. */
  photo?: { file: string; width: number; height: number; alt: string };
  /** Optional link under the blurb: a blog post, a project. */
  link?: { href: string; label: string };
}

/** The artist statement on /about/. Blank lines split it into paragraphs. */
export const statement = `I believe that there exists a lot of humanity in the empty spaces and areas that our brains like to hide from us. Call it bottling stuff up, call it shadow work, but whatever you call it, I believe art is the most potent way in. Art has a way to reveal parts of ourselves even without being 100% cognizant of it. Art can work its way into the subconscious of your brain and wreak havoc.`;

/** Off-stage notes on /about/, in display order. An empty list hides the section. */
export const escapades: Escapade[] = [
  {
    blurb: `From a very young age, I was incredibly into computers. My dad gave me the family's old Dell Inspiron and that computer and its bloated Windows XP install became my stomping ground for years. Microsoft Publisher, setting up Minecraft servers, downloading bootleg software for my PDAs. In third grade, I'd speedrun my assignments so I could hop on the iBook G4s in the back of the classroom and fire up Scratch, a drag-and-drop programming language that became my home.`
  },
  {
    blurb: `When I first auditioned for theatre in middle school, I only really did it because the people who were doing it seemed really cool already. It was sort of an aspirational audition: "if I do this, maybe I'll be even half as cool as them." The people in theatre just seemed more unapologetically themselves than almost anyone else I knew, and I knew that the place for me was going to be like that.`
  },
  {
    blurb: `As soon as I fell in love with theatre, New York City was really the only option. I looked at universities in other states and even outside of the city, but every time they just didn't feel right. The thought that existing freely in those places basically mandated car ownership never sat right with me. There's something about a walkable city with easily accessible public transit that feels intrinsically more human to me, and I don't think it's an amenity I will allow any future places I live to lack.`
  }
];

// A slot still reading like `[Artist statement]` is one Finn hasn't written. Builds leave
// /about/ and every link to it out until none is left; dev keeps the page for writing.
const unwritten = (text: string) => !text.trim() || /^\[[^\]]*\]$/.test(text.trim());
export const showAbout = dev || ![statement, ...escapades.flatMap(item => (item.title ? [item.title, item.blurb] : [item.blurb]))].some(unwritten);
