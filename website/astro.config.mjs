// @ts-check
import { defineConfig, fontProviders } from 'astro/config';

// https://astro.build/config
// export default defineConfig({});
export default defineConfig({
      experimental: {
        fonts: [{
            provider: fontProviders.google(),
            name: "Public Sans",
            cssVariable: "--font-public-sans"
        },
      {
        
            provider: fontProviders.google(),
            name: "Caprasimo",
            cssVariable: "--font-caprasimo"
      }
    ]
    },
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
