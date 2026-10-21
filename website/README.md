# Finn Rutis portfolio

SvelteKit with adapter-static. Run commands from this `website/` directory, with
Node >=22.12 and the repository's adjacent `metadata/`, `lib/`, and `variants.toml`
available. This is not a standalone copy of the canonical content.

| Command | Purpose |
| --- | --- |
| `npm ci` | Install the locked dependencies |
| `npm run dev -- --host 127.0.0.1` | Local development |
| `npm run check` | Generate SvelteKit types and check Svelte/TypeScript |
| `npm test` | Real-parser canonical ingestion and configuration checks |
| `npm run build` | Prerender five routes to `build/`, no SPA fallback |
| `env SITE_BASE=/resume npm run build` | Build for repository Pages rather than domain root |
| `env SITE_BASE=/resume npm run preview -- --host 127.0.0.1` | Preview that repository-base build |
| `npm run dev:fixture` | Separate, unshipped CurrentProjects browser test harness |

See [portfolio site handoff](../docs/portfolio-site.md) for artifact assembly,
font permissions, media-credit dependencies, and the assigned validation matrix.
Building the site alone does not create PDF/PNG downloads; Phase 3 assembles them.
