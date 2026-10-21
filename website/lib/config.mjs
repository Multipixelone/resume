/** Empty for custom-domain/root hosting; /resume for repository Pages. */
export function siteBase(value = '') {
  if (value !== '' && !/^\/[A-Za-z0-9_-]+(?:\/[A-Za-z0-9_-]+)*$/.test(value)) {
    throw new TypeError('SITE_BASE must be empty or a root-relative path without a trailing slash');
  }
  return value;
}
