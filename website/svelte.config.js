import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { fileURLToPath } from 'node:url';
import { siteBase } from './lib/config.mjs';

export default {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({ pages: 'build', assets: 'build', strict: true }),
    paths: { base: siteBase(process.env.SITE_BASE), relative: false },
    alias: {
      $shows: fileURLToPath(new URL('../lib/shows.mjs', import.meta.url)),
      $content: fileURLToPath(new URL('./lib/content.mjs', import.meta.url)),
      $canonical: fileURLToPath(new URL('../metadata', import.meta.url))
    },
    prerender: { entries: ['*'] }
  }
};
