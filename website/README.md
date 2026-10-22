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
| `npm run build` | Prerender six routes to `build/`, no SPA fallback |
| `env SITE_BASE=/resume npm run build` | Build for repository Pages rather than domain root |
| `env SITE_BASE=/resume npm run preview -- --host 127.0.0.1` | Preview that repository-base build |
| `npm run dev:fixture` | Separate, unshipped CurrentProjects browser test harness |
| `python3 scripts/gen_social_card.py` | Redraw `static/social-card.png` after changing its copy or palette (needs Pillow, in the dev shell) |

See [portfolio site handoff](../docs/portfolio-site.md) for artifact assembly,
font permissions, media-credit dependencies, and the assigned validation matrix.
Building the site alone does not create PDF/PNG downloads; Phase 3 assembles them.

Licensed `.woff2` files dropped into the gitignored `fonts-local/` (same names as in
`src/styles/fonts.css`) are served same-origin by both dev servers, so local pages and
impeccable live need no CORS grant from `fonts.finnrut.is`. Faces without a local copy
load remotely. Builds always use the remote URLs; restart dev after adding a file.
