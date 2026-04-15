// @ts-check
import { defineConfig, fontProviders } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  fonts: [
    {
      provider: fontProviders.local(),
      name: "Public Sans",
      cssVariable: "--font-public-sans",
      options: {
        variants: [
          {
            src: ["./src/assets/fonts/open-sans-v44-latin-regular.woff2"],
          },
        ],
      },
    },
    {
      provider: fontProviders.local(),
      name: "Caprasimo",
      cssVariable: "--font-caprasimo",
      options: {
        variants: [
          {
            src: ["./src/assets/fonts/caprasimo-v6-latin-regular.woff2"],
          },
        ],
      },
    },
  ],
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
