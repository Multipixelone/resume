# Resume Builder

Typst-based multi-variant resume system built with Nix. Produces tailored PDFs for different job types from shared metadata and modular sections.

## Build Commands

```bash
nix build '.#resume'       # Build all resume PDFs (acting, tech, work, nanny, saltandstraw, cover letter, rep sheet)
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

| File                       | Override TOML                | Modules                                                 | Purpose                     |
| -------------------------- | ---------------------------- | ------------------------------------------------------- | --------------------------- |
| `resumes/cv.typ`           | none (base only)             | professional, educational, film, training, skills       | Acting/performance resume   |
| `resumes/tech.typ`         | `tech-metadata.toml`         | tech-skills, education, tech-projects, work-experience  | Technology/IT resume        |
| `resumes/work.typ`         | `work-metadata.toml`         | work-experience, education, skills                      | Events/operations resume    |
| `resumes/nanny.typ`        | `nanny-metadata.toml`        | nanny-experience, education, nanny-skills               | Childcare resume            |
| `resumes/saltandstraw.typ` | `saltandstraw-metadata.toml` | saltandstraw-experience, education, saltandstraw-skills | Salt & Straw scooper resume |
| `resumes/saltandstraw-sc.typ` | `saltandstraw-sc-metadata.toml` | saltandstraw-experience, education, saltandstraw-skills | Salt & Straw (SC) resume |
| `resumes/cover-letter.typ` | none                         | (letter body)                                           | Cover letter                |
| `resumes/rep-sheet.typ`    | none                         | (rep-sheet data)                                        | Theatre repertory sheet     |
| `resumes/title-pages.typ`  | `title-pages-metadata.toml`  | (title pages)                                           | Audition title pages        |

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

### 4. Register the variant

Add an entry to `variants.toml` at the repo root:

```toml
[my-variant]
source = "my-variant"                          # stem of resumes/<source>.typ
dest = "my-variant"                            # output filename stem and GitHub Pages basename
expected_pages = 1                             # exact page count (0 = multi-page, just checks >= 1)
check_metadata = true                          # validate merged metadata for completeness
# override_toml = "my-variant-metadata.toml"   # only if step 1 created an override
```

That's it. `packages/resume.nix`, `packages/checks.nix`, and `.github/workflows/_build.yml` all read from this file.

## Writing Resume Content

When creating or editing job descriptions, summaries, and other resume text, follow these principles strictly. The goal is copy that reads like a capable person wrote it at midnight with a glass of wine — not like it was extruded from a language model.

### Voice & Tone

- **Write like a human, not a hiring-advice blog.** Vary sentence length. Start some sentences with "and" or "but" if it sounds natural. Use contractions. Let the occasional short fragment stand on its own.
- **Match formality to the audience, not to some universal "resume voice."** A nanny resume should sound warm and grounded. A tech resume can be more direct and precise. An events resume should feel energetic and competent. None of them should sound like a LinkedIn post.
- **Default register: confident and specific, slightly casual.** The sweet spot is someone explaining what they did to a friend who works in the field — not a cover letter, not a text message. Think the existing `work-experience.toml` voice.
- **First person is acceptable in informal variants** (nanny, cover letters). Third-person implied subject ("Ran the front desk", "Designed lighting for...") is standard for professional variants. Never mix the two in a single variant.

### Tailoring to a Job Posting

When a variant targets a specific job posting:

- **Echo the posting's language selectively, not systematically.** If the posting says "cross-functional collaboration," you might write "worked across teams" — do NOT parrot "cross-functional collaboration" back verbatim. Mirror the _concepts_, not the exact phrasing.
- **Foreground relevant experience; don't fabricate it.** Reorder bullet points, emphasize different aspects of the same role, or expand on details that align with the target job. Never invent responsibilities or skills that don't exist in the base data.
- **One or two keyword echoes per description is enough.** More than that trips ATS-gaming detectors and human suspicion alike. Scatter them across different entries rather than clustering them in one.
- **Adjust the header quote (`header_quote`) to match the posting's core need**, but phrase it as something the candidate would actually say about themselves — not a rephrased job title.

### What to Avoid (AI Tells)

These patterns are dead giveaways of machine-generated resume text. Do not produce them:

- **Hollow intensifiers**: "leveraged", "utilized", "spearheaded", "orchestrated", "facilitated", "architected" (as a verb). Use plain verbs: ran, built, designed, set up, handled, wrote, fixed, managed.
- **Stacked buzzwords**: "Engineered scalable cloud-native microservice architecture" — nobody talks like this. Say what was actually built and what it does.
- **Symmetrical sentence structure**: When every bullet follows the exact same `[Past-tense verb] [object] [prepositional phrase] [result clause]` template, it reads as generated. Vary the structure. Some bullets can be two sentences. Some can omit the result.
- **Vague impact claims**: "resulting in improved efficiency" or "driving significant growth" with no numbers or specifics. Either include a real metric or leave the claim off entirely.
- **Thesaurus cycling**: Using a different synonym for "managed" in every single bullet ("oversaw", "directed", "coordinated", "supervised") instead of just repeating "managed" when that's the accurate word.
- **Gratuitous acronym drops and parenthetical expansions**: "Infrastructure as Code (IaC)" in every mention. Spell it out once or use the acronym — don't do both every time.
- **Emoji or Unicode dressing**: No bullet-point Unicode symbols, no decorative characters. Plain text only. Important: No em dashes, ever.

### Practical Checklist

Before finalizing any resume text, verify:

1. **Read it aloud.** If it sounds like a press release, rewrite it.
2. **Could you picture the person saying this in an interview?** If not, it's too stiff.
3. **Does every sentence contain at least one concrete detail** (a tool name, a number, a specific task)? If it's all abstract, it's filler.
4. **Are there more than two adjectives in any single sentence?** Cut some.
5. **Would a recruiter who reads 200 resumes a day notice anything unusual?** That's the bar — invisible competence, not performance.

## Directory Structure

```
.
├── resumes/                                 # Resume entry files
│   ├── cv.typ                               # Acting/performance resume
│   ├── tech.typ                             # Technology/IT resume
│   ├── work.typ                             # Events/operations resume
│   ├── nanny.typ                            # Childcare resume
│   ├── saltandstraw.typ                     # Salt & Straw scooper resume
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
│   ├── saltandstraw-experience.typ # Salt & Straw experience (from saltandstraw-experience.toml)
│   ├── saltandstraw-skills.typ     # Salt & Straw skills
│   ├── _education-content.typ  # Shared education entry (included by education.typ & training.typ)
│   └── _training-content.typ   # Shared training content
├── metadata/
│   ├── metadata.toml           # Base metadata (personal info, layout, colors, fonts)
│   ├── tech-metadata.toml      # Tech resume overrides
│   ├── work-metadata.toml      # Work resume overrides
│   ├── nanny-metadata.toml     # Nanny resume overrides
│   ├── saltandstraw-metadata.toml  # Salt & Straw resume overrides
│   ├── saltandstraw-experience.toml # Salt & Straw experience data
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
├── variants.toml        # Variant registry (single source of truth for build + checks + CI)
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

Use Conventional Commits so `git-cliff` can parse and group changes correctly.

Format:

- `type(scope): short summary`
- `type(scope)!: short summary` for breaking changes

Supported `type` values include:

- `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

Preferred scopes for resume/template work:

- `reformat` - Layout/formatting changes
- `template` - Template/module structure changes
- `content` - Resume text/content changes

Examples:

- `feat(template): add reusable project entry block`
- `fix(content): correct work experience date`
- `style(reformat): tighten section spacing`

Release: `just bump <patch|minor|major>` triggers the GitHub Actions release workflow.
