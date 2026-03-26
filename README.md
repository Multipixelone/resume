# resume
resume and website builder in nix

The CI workflow publishes the resume PNG to GitHub Pages at `/resume.png` (for example: `https://<owner>.github.io/resume/resume.png`).
Deployments happen only when `VERSION` is changed on `main`; all commits still run the build jobs.

Use `just bump <patch|minor|major>` to trigger the `release.yml` workflow from the command line via GitHub CLI.
The default Nix dev shell includes both `just` and `gh`.
Nix builds are configured to avoid substituter caches (`--no-substitute` in CI and `substitute = "false"` in `flake.nix`) so resume artifacts are always built locally.

For changelog sorting with git-cliff, use conventional commit scopes to categorize template work:
- `type(reformat): ...` for formatting/layout reshaping changes
- `type(template): ...` for reusable template/module structure updates
- `type(content): ...` for actual resume text/content additions
