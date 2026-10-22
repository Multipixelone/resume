export interface Escapade {
  title: string;
  /** Blank lines split it into paragraphs. Backtick strings take apostrophes and line breaks as is. */
  blurb: string;
  /** Optional print beside the text, from static/media/. Without one the entry is a paper slip. */
  photo?: { file: string; width: number; height: number; alt: string };
  /** Optional link under the blurb: a blog post, a project. */
  link?: { href: string; label: string };
}

/** Off-stage notes on /about/, in display order. An empty list hides the section. */
export const escapades: Escapade[] = [
  { title: `[Escapade title]`, blurb: `[A paragraph or two]` },
  { title: `[Escapade title]`, blurb: `[A paragraph or two]` }
];
