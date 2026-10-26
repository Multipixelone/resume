import { resolve } from '$app/paths';

/** Only site-local paths enter here. Encode filenames (including the composite's space). */
export function sitePath(path) {
  if (typeof path !== 'string' || !path.startsWith('/') || path.startsWith('//')
    || /[?#\\]/.test(path) || path.split('/').some(part => part === '.' || part === '..')) {
    throw new TypeError('Expected a site-local absolute path');
  }
  return resolve(path.slice(1).split('/').map(encodeURIComponent).join('/'));
}
