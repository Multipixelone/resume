import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { siteBase } from './lib/config.mjs';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';
import { localFonts } from './lib/local-fonts.mjs';
import { mediaRenditions } from './lib/renditions.mjs';

const base = siteBase(process.env.SITE_BASE);

export default defineConfig({
  plugins: [localFonts(), mediaRenditions(), sveltekit({
    preprocess: vitePreprocess(),
    adapter: adapter({ pages: 'build', assets: 'build', strict: true }),
    paths: { base, relative: false },
    alias: {
      $shows: fileURLToPath(new URL('../lib/shows.mjs', import.meta.url)),
      $content: fileURLToPath(new URL('./lib/content.mjs', import.meta.url)),
      $renditions: fileURLToPath(new URL('./lib/renditions.mjs', import.meta.url)),
      $canonical: fileURLToPath(new URL('../metadata', import.meta.url))
    },
    prerender: {
      entries: ['*'],
      // /about/ answers 404 while it still holds placeholders (src/lib/about.ts), which
      // keeps it out of build/. Any other failed page still fails the build.
      handleHttpError: ({ path, status, message }) => {
        if (status === 404 && path === `${base}/about/`) {
          console.warn('Leaving /about/ out of the build: src/lib/about.ts still has placeholders');
          return;
        }
        throw new Error(message);
      }
    }
  })],
  server: {
    // The site deliberately consumes canonical sources one directory above it.
    fs: { allow: [
      fileURLToPath(new URL('.', import.meta.url)),
      fileURLToPath(new URL('../lib/shows.mjs', import.meta.url)),
      fileURLToPath(new URL('../metadata/theatre.toml', import.meta.url)),
      fileURLToPath(new URL('../metadata/film.toml', import.meta.url)),
      fileURLToPath(new URL('../variants.toml', import.meta.url))
    ] }
  }
});
