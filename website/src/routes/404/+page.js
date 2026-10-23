// GitHub Pages answers any unknown path with build/404.html. 'never' writes this page there
// instead of 404/index.html, and it ships without client script: it loads at whatever URL
// missed, so there is no route for it to hydrate.
export const trailingSlash = 'never';
export const csr = false;
