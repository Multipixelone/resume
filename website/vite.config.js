import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    // The site deliberately consumes canonical sources one directory above it.
    fs: { allow: [
      fileURLToPath(new URL('.', import.meta.url)),
      fileURLToPath(new URL('../lib/shows.mjs', import.meta.url)),
      fileURLToPath(new URL('../metadata/theatre.toml', import.meta.url)),
      fileURLToPath(new URL('../variants.toml', import.meta.url))
    ] }
  }
});
