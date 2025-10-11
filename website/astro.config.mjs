// @ts-check
import { defineConfig, fontProviders } from 'astro/config';

// https://astro.build/config
// export default defineConfig({});
export default defineConfig({
      experimental: {
        fonts: [{
      provider: "local",
            name: "Public Sans",
            cssVariable: "--font-public-sans",
          variants: [
        {
        src: [
              "./src/assets/fonts/open-sans-v44-latin-regular.woff2"
            ]  
        },
        
      ]
        },
      {
        
            provider: "local",
            name: "Caprasimo",
            cssVariable: "--font-caprasimo",
          variants: [
        {
        src: [
              "./src/assets/fonts/caprasimo-v6-latin-regular.woff2"
            ]  
        },
        
      ]
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
