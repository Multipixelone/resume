import { error } from '@sveltejs/kit';
import { showAbout } from '$lib/about';

// While a placeholder remains, builds answer 404 here, so the page never reaches build/
// (svelte.config.js lets this one 404 through). Dev renders it for writing.
export function load() {
  if (!showAbout) error(404, 'Not found');
}
