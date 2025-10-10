// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
// export default defineConfig({});
export default defineConfig({
  vite: {
    // Vite-specific configurations go here
    plugins: [
      // your Vite plugins
    ],
  server: {
    allowedHosts: [
      'link.bun-hexatonic.ts.net',
    ],
    // Or, to allow all hosts (not recommended for security reasons):
    // allowedHosts: true,
  },
    },
});
