import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { fileURLToPath } from 'node:url';
import { localFonts } from '../../lib/local-fonts.mjs';

export default defineConfig({
  root: fileURLToPath(new URL('.', import.meta.url)),
  publicDir: fileURLToPath(new URL('../../static', import.meta.url)),
  plugins: [localFonts(), svelte({ configFile: false })],
  resolve: { alias: {
    '#lib': fileURLToPath(new URL('../../src/lib', import.meta.url)),
    '$shows': fileURLToPath(new URL('../../../lib/shows.mjs', import.meta.url)),
    '$app/paths': fileURLToPath(new URL('./app-paths.mjs', import.meta.url))
  } },
  server: { fs: { allow: [
    fileURLToPath(new URL('../..', import.meta.url)),
    fileURLToPath(new URL('../../../lib/shows.mjs', import.meta.url))
  ] } }
});
