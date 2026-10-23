import { dev } from '$app/environment';

export interface Escapade {
  title: string;
  /** Blank lines split it into paragraphs. Backtick strings take apostrophes and line breaks as is. */
  blurb: string;
  /** Optional print beside the text, from static/media/. Without one the entry is a paper slip. */
  photo?: { file: string; width: number; height: number; alt: string };
  /** Optional link under the blurb: a blog post, a project. */
  link?: { href: string; label: string };
}

/** The artist statement on /about/. Blank lines split it into paragraphs. */
export const statement = `[Artist statement]`;

/** Off-stage notes on /about/, in display order. An empty list hides the section. */
export const escapades: Escapade[] = [
  { title: `[Escapade title]`, blurb: `[A paragraph or two]` },
  { title: `[Escapade title]`, blurb: `[A paragraph or two]` }
];

// A slot still reading like `[Artist statement]` is one Finn hasn't written. Builds leave
// /about/ and every link to it out until none is left; dev keeps the page for writing.
const unwritten = (text: string) => !text.trim() || /^\[[^\]]*\]$/.test(text.trim());
export const showAbout = dev || ![statement, ...escapades.flatMap(item => [item.title, item.blurb])].some(unwritten);
