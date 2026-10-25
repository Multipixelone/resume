import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { fileURLToPath } from 'node:url';
import { siteBase } from './lib/config.mjs';

const base = siteBase(process.env.SITE_BASE);

export default {
  preprocess: vitePreprocess(),
  kit: {
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
  }
};
