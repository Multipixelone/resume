# resume

I maintain several versions of my resume for different kinds of work — acting, tech, childcare, food service, and more. This system lets me keep all the content in one place and generate tailored PDFs from it. It's built with [Typst](https://typst.app/) for typesetting and [Nix flakes](https://nixos.wiki/wiki/Flakes) for reproducible builds, and it deploys to GitHub Pages on every versioned release.

[![Build](https://img.shields.io/github/actions/workflow/status/Multipixelone/resume/ci.yml?style=for-the-badge&logo=github&label=build&color=a6e3a1&labelColor=313244&logoColor=cdd6f4)](https://github.com/Multipixelone/resume/actions)
[![Version](https://img.shields.io/github/v/tag/Multipixelone/resume?style=for-the-badge&label=version&color=cba6f7&labelColor=313244)](VERSION)
[![License](https://img.shields.io/github/license/Multipixelone/resume?style=for-the-badge&color=b4befe&labelColor=313244)](LICENSE)
[![Pages](https://img.shields.io/website?url=https%3A//multipixelone.github.io/resume&style=for-the-badge&logo=githubpages&label=pages&color=fab387&labelColor=313244&logoColor=cdd6f4)](https://multipixelone.github.io/resume)
![Typst](https://img.shields.io/badge/typst-typesetting-94e2d5?style=for-the-badge&logo=typst&labelColor=313244&logoColor=cdd6f4)
![Nix](https://img.shields.io/badge/nix-flakes-89b4fa?style=for-the-badge&logo=nixos&labelColor=313244&logoColor=cdd6f4)

## Variants

Each variant is a thin entry file that merges base metadata with job-specific overrides, picks which content modules to include, and renders through a shared Typst layout. I only override what needs to change — email address, header tagline, which personal details to show or hide, layout tweaks.

| Variant | File | Purpose |
|---|---|---|
| Acting CV | `resumes/cv.typ` | Theatre and performance |
| Tech | `resumes/tech.typ` | Technology and IT positions |
| Work | `resumes/work.typ` | Events and operations |
| Nanny | `resumes/nanny.typ` | Childcare |
| Salt & Straw | `resumes/saltandstraw.typ` | Scooper |
| Salt & Straw SC | `resumes/saltandstraw-sc.typ` | Shift coordinator |
| Cover Letter | `resumes/cover-letter.typ` | General cover letter |
| Rep Sheet | `resumes/rep-sheet.typ` | Musical theatre repertory |
| Title Pages | `resumes/title-pages.typ` | Audition title pages |

## How It Works

The variant registry in `variants.toml` is the single source of truth — the Nix build, CI matrix, and quality checks all read from it. Every variant follows the same pattern:

```
resumes/<variant>.typ
  → meta.typ: merge metadata/metadata.toml + metadata/<variant>-metadata.toml
  → select modules from modules/
  → render via src/lib.typ::cv()
```

All resume content (job history, skills, theatre credits, training) lives in TOML files under `metadata/`. Modules in `modules/` load that data and format it into sections. The layout engine in `src/` handles page structure, styling, and typography.

## Building

Requires a Nix environment with flakes enabled.

```bash
nix build '.#resume'      # all resume PDFs
nix build '.#finn-rutis'  # composite headshot PDF
nix build '.#website'     # portfolio site
```

For local iteration without a full Nix build:

```bash
nix develop                  # enter dev shell (typst, typstyle, tinymist, etc.)
typst watch resumes/cv.typ   # live preview
typst compile --input commit="dev" --input version="2026-04-22" resumes/tech.typ
```

## Adding a Variant

1. **Create a metadata override** in `metadata/<variant>-metadata.toml`. Only include fields that differ from the base `metadata/metadata.toml` — everything else is inherited.

2. **Create an entry file** at `resumes/<variant>.typ` that imports the override, selects which modules to include, and passes the merged metadata to the shared layout.

3. **Create new modules** in `modules/` if the job needs a section that doesn't already exist.

4. **Register the variant** in `variants.toml` with the source filename, output name, expected page count, and whether metadata should be validated.

## CI/CD and Quality Checks

Builds run on every push. Deployments to GitHub Pages happen only when `VERSION` changes on `main`. I use `just bump <patch|minor|major>` to trigger releases, and [git-cliff](https://git-cliff.org/) generates changelogs from conventional commits.

The Nix flake runs these checks automatically:

- **typstyle** — consistent Typst formatting
- **TOML validity** — all metadata files parse correctly
- **Metadata completeness** — merged metadata has all required fields
- **Output files** — every registered variant produces a PDF
- **PDF page count** — each variant matches its expected page count

<details>
<summary>Project structure</summary>

```
resumes/          # entry files per variant
src/              # layout templates and utilities
  ├── lib.typ     #   main layout (cv, coverLetter)
  ├── cv.typ      #   section/entry components
  ├── meta.typ    #   metadata merging
  └── utils/      #   styles, dict merge, language detection
modules/          # reusable resume sections
metadata/         # base + override TOML data files
packages/         # Nix derivations (resume, finn-rutis, website)
.github/          # CI workflows
variants.toml     # variant registry (single source of truth)
```

</details>

## Commit Conventions

I use conventional commits so git-cliff can parse them:

```
feat(content): add new theatre credit
fix(reformat): tighten section spacing
refactor(template): simplify module loading
```

Scopes: `content` for resume text, `reformat` for layout changes, `template` for structural updates.
