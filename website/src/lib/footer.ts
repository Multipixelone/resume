import type { IconName } from '$lib/components/Icon.svelte';

export interface FooterLink {
  /** Accessible name and hover title; the icon itself is aria-hidden. */
  name: string;
  /** Site-local paths start with "/" and go through sitePath(). */
  href: string;
  icon: IconName;
  /** "me" marks a profile of the same person (IndieWeb rel-me). */
  rel?: string;
}

/** Footer icon row, in display order. Add a link here; add a glyph to Icon.svelte. */
export const footerLinks: FooterLink[] = [
  { name: 'Instagram', href: 'https://www.instagram.com/finnrutis/', icon: 'instagram', rel: 'me' },
  { name: 'LinkedIn', href: 'https://www.linkedin.com/in/finn-rutis-44a951304/', icon: 'linkedin', rel: 'me' },
  { name: 'All resumes', href: '/resumes/', icon: 'resume' },
  { name: 'Email', href: 'mailto:me@finnrut.is', icon: 'mail' },
  { name: 'PGP key', href: 'https://blog.finnrut.is/pgp/', icon: 'key' },
  { name: 'Blog', href: 'https://blog.finnrut.is/', icon: 'blog', rel: 'me' }
];

export const repoUrl = 'https://github.com/Multipixelone/resume';
