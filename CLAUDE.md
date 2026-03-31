# Resume Builder

Typst-based multi-variant resume system built with Nix. Produces tailored PDFs for different job types from shared metadata and modular sections.

## Build Commands

```bash
nix build '.#resume'       # Build all resume PDFs (acting, tech, work, nanny, cover letter, rep sheet)
nix build '.#finn-rutis'   # Build composite headshot PDF (cropped CV + portrait page)
nix build '.#website'      # Build portfolio website

# Local dev (requires nix develop shell)
typst compile resumes/cv.typ                  # Quick single-file compile
typst compile --input commit="dev" --input version="2025-01-01" resumes/tech.typ
typst watch resumes/cv.typ                    # Live preview
```

All resume PDFs are built by the single `resume` Nix package (`packages/resume.nix`). The `finn-rutis` package stays separate because it needs ghostscript and pdfunite for PDF cropping/merging.

## How Resume Variants Work

Each variant is a thin entry file in `resumes/` that:
1. Loads base metadata (`metadata/metadata.toml`) merged with a variant-specific override TOML
2. Selects which modules to include
3. Passes the merged metadata to the shared `cv` layout from `src/lib.typ`

**Pattern:**
```
resumes/<variant>.typ --> imports src/meta.typ::makeMeta("override.toml")
                      --> merges metadata/metadata.toml + metadata/<variant>-metadata.toml
                      --> passes merged metadata to src/lib.typ::cv()
                      --> includes selected modules/ sections
```

### Current Variants

| File | Override TOML | Modules | Purpose |
|------|--------------|---------|---------|
| `resumes/cv.typ` | none (base only) | professional, educational, film, training, skills | Acting/performance resume |
| `resumes/tech.typ` | `tech-metadata.toml` | tech-skills, education, tech-projects, work-experience | Technology/IT resume |
| `resumes/work.typ` | `work-metadata.toml` | work-experience, education, skills | Events/operations resume |
| `resumes/nanny.typ` | `nanny-metadata.toml` | nanny-experience, education, nanny-skills | Childcare resume |
| `resumes/cover-letter.typ` | none | (letter body) | Cover letter |
| `resumes/rep-sheet.typ` | none | (rep-sheet data) | Theatre repertory sheet |

## Creating a New Resume Variant

To create a resume tailored for a specific job posting:

### 1. Create the metadata override TOML

Create `metadata/<variant>-metadata.toml`. Only include fields that differ from the base `metadata/metadata.toml`:

```toml
# metadata/example-metadata.toml
[lang.en]
header_quote = "One-line summary tailored to the job."
cv_footer = "Example Resume"

[layout]
before_entry_description_skip = "-4pt"

[layout.header]
display_profile_photo = false

[layout.entry]
display_entry_society_first = false
display_logo = false

[personal.info]
email = "relevant@finnrut.is"
# Set irrelevant fields to empty string to hide them
instagram = ""
vocal-part = ""
union = ""
height = ""
```

Key override fields:
- `header_quote` - Tagline shown under the name; tailor to the job
- `cv_footer` - Footer label (e.g. "Technical Resume")
- `display_profile_photo` - true/false
- `display_entry_society_first` - true = company bold first, false = role bold first
- `email` - Which contact email to show
- Set any `personal.info` field to `""` to hide it

### 2. Create the entry .typ file

Create `resumes/<variant>.typ`:

```typst
#import "../src/lib.typ": cv
#import "../src/meta.typ": makeMeta
#let variant-metadata = makeMeta("<variant>-metadata.toml")

#let importModules(modules) = {
  for module in modules {
    include {
      "../modules/" + module + ".typ"
    }
  }
}

#show: cv.with(
  variant-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#importModules((
  // Pick relevant modules from the list below
  "work-experience",
  "education",
  "skills",
))
```

### 3. Create new modules if needed

If the job needs a section that doesn't exist yet, create `modules/<section>.typ`:

```typst
#import "../src/lib.typ": cvSection, cvEntry
#let metadata = toml("../metadata/metadata.toml")

#cvSection("Section Title")

#cvEntry(
  title: [Role or Item],
  society: [Organization],
  date: [Date Range],
  location: [Location],
  description: [Optional description text.],
)
```

For data-driven modules, put the content in `metadata/<section>.toml` and load it with `toml()`.

### 4. Add to the build

Add the new typst compile command to `packages/resume.nix` in the `buildPhase` and `installPhase`.

## Directory Structure

```
.
├── resumes/                                 # Resume entry files
│   ├── cv.typ                               # Acting/performance resume
│   ├── tech.typ                             # Technology/IT resume
│   ├── work.typ                             # Events/operations resume
│   ├── nanny.typ                            # Childcare resume
│   ├── cover-letter.typ                     # Cover letter
│   ├── rep-sheet.typ                        # Repertory sheet
│   └── portrait-page.typ                    # Headshot page (for finn-rutis composite)
├── src/
│   ├── lib.typ              # Main layout templates (cv, coverLetter, letter)
│   ├── cv.typ               # CV component functions (cvSection, cvEntry, cvSkill, etc.)
│   ├── letter.typ           # Letter component functions
│   ├── meta.typ             # makeMeta() - merges base + override metadata
│   └── utils/
│       ├── styles.typ       # Colors, fonts, layout helpers (hBar, setAccentColor)
│       ├── merge.typ        # mergeDicts() - recursive dictionary merge
│       └── lang.typ         # Language/non-Latin font detection
├── modules/                 # Reusable resume sections
│   ├── professional.typ     # Theatre performances (from theatre.toml)
│   ├── work-experience.typ  # Job history (from work-experience.toml)
│   ├── education.typ        # Education (role-first layout)
│   ├── educational.typ      # Education (society-first layout, with logo)
│   ├── skills.typ           # General skills
│   ├── tech-skills.typ      # Technical skills (from tech-skills.toml)
│   ├── tech-projects.typ    # Tech projects (from tech-projects.toml)
│   ├── training.typ         # Training/workshops (from training.toml)
│   ├── film.typ             # Film/video work (from film.toml)
│   ├── commercial.typ       # Commercial work (from commercial.toml)
│   ├── voiceover.typ        # Voiceover work
│   ├── nanny-experience.typ # Childcare experience (from nanny-experience.toml)
│   ├── nanny-skills.typ     # Childcare skills
│   ├── _education-content.typ  # Shared education entry (included by education.typ & training.typ)
│   └── _training-content.typ   # Shared training content
├── metadata/
│   ├── metadata.toml           # Base metadata (personal info, layout, colors, fonts)
│   ├── tech-metadata.toml      # Tech resume overrides
│   ├── work-metadata.toml      # Work resume overrides
│   ├── nanny-metadata.toml     # Nanny resume overrides
│   ├── work-experience.toml    # Job history data
│   ├── tech-skills.toml        # Tech skills data
│   ├── tech-projects.toml      # Tech project entries
│   ├── theatre.toml            # Theatre performance data
│   ├── professional.toml       # Professional work data
│   ├── training.toml           # Training/workshop data
│   ├── film.toml               # Film project data
│   ├── commercial.toml         # Commercial work data
│   ├── educational.toml        # Education data
│   ├── nanny-experience.toml   # Childcare experience data
│   └── rep-sheet.toml          # Repertory song data
├── packages/
│   ├── resume.nix       # Builds ALL resume PDFs in one derivation
│   ├── finn-rutis.nix   # Composite headshot PDF (needs ghostscript)
│   └── website.nix      # Astro portfolio site
├── .github/workflows/
│   ├── ci.yml           # CI on push/PR
│   ├── _build.yml       # Reusable build workflow (matrix over packages)
│   └── release.yml      # Version bump + changelog + deploy
├── flake.nix            # Nix flake (build system entry point)
├── VERSION              # Semantic version (e.g. 1.4.0)
└── justfile             # just bump <patch|minor|major>
```

## Key Functions Reference

- `src/lib.typ::cv(metadata, profilePhoto, doc)` - Main CV page layout
- `src/lib.typ::coverLetter(metadata, profilePhoto, doc)` - Cover letter layout
- `src/cv.typ::cvSection(title)` - Section heading with accent line
- `src/cv.typ::cvEntry(title, society, date, location, description, logo, tags)` - Standard entry
- `src/cv.typ::cvSkill(type, info)` - Skill row (type label + info)
- `src/cv.typ::cvTraining(type, info, instructors)` - Training row
- `src/cv.typ::cvPerformance(metadata)` - Performance table from shows data
- `src/cv.typ::cvHonor(date, title, issuer, url, location)` - Honor/award entry
- `src/meta.typ::makeMeta(overrideFile)` - Merge base metadata with override TOML
- `src/utils/merge.typ::mergeDicts(base, override)` - Recursive dictionary merge
- `src/utils/styles.typ::hBar()` - Vertical separator bar for inline lists

## Commit Conventions

Uses conventional commits with these scopes for changelog organization:
- `type(reformat):` - Layout/formatting changes
- `type(template):` - Template structure changes
- `type(content):` - Resume text/content changes

Release: `just bump <patch|minor|major>` triggers the GitHub Actions release workflow.
