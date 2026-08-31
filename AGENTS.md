# Resume Builder

Typst-based multi-variant resume system built with Nix. Produces tailored PDFs for different job types from shared metadata and modular sections.

## Source-of-truth files

Read these before writing; they hold what the code cannot tell you.

- `REFERENCE.md` is the biographical source of truth: real jobs, dates, skills, theatre credits, tech projects, and a voice/tone section with sample copy. Every claim in any resume traces back to a line in here. If it is not in `REFERENCE.md`, it does not go on a resume.
- `variants.toml` is the variant registry. `packages/resume.nix`, `packages/checks.nix`, and `.github/workflows/_build.yml` all read it. It lists every variant; do not maintain a second list anywhere.

## Build Commands

```bash
nix build '.#resume'       # All resume PDFs
nix build '.#finn-rutis'   # Composite headshot PDF (cropped CV + portrait page)
nix build '.#website'      # Portfolio website

# Local dev (requires nix develop shell)
typst compile resumes/cv.typ                  # Quick single-file compile
typst compile --input commit="dev" --input version="2025-01-01" resumes/tech.typ
typst watch resumes/cv.typ                    # Live preview
```

Every resume PDF comes out of the single `resume` package (`packages/resume.nix`). `finn-rutis` stays separate because it needs ghostscript and pdfunite for cropping and merging.

The `--input commit=` and `--input version=` flags are supplied by Nix during a real build. Pass them by hand when compiling directly, or `src/utils/date.typ::buildDate()` falls back to today.

## How Resume Variants Work

Each variant is a thin entry file in `resumes/` that loads base metadata merged with a variant override, selects modules, and hands the result to the shared `cv` layout.

```
resumes/<variant>.typ --> imports src/meta.typ::makeMeta("override.toml")
                      --> merges metadata/metadata.toml + metadata/<variant>-metadata.toml
                      --> passes merged metadata to src/lib.typ::cv()
                      --> includes selected modules/ sections
```

Function-style modules (`experience`, `projects`, `skills`) take metadata explicitly. Legacy include-style modules (`education`, `professional`, `film`, `training`, `educational`) load via `importModules`.

## Creating a New Resume Variant

### 1. Create the metadata override TOML

Create `metadata/<variant>-metadata.toml` holding only the fields that differ from base `metadata/metadata.toml`:

```toml
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
instagram = ""      # empty string hides a field
vocal-part = ""
union = ""
height = ""
```

Key override fields:

- `header_quote` sets the tagline under the name; tailor it to the job
- `cv_footer` sets the footer label (e.g. "Technical Resume")
- `display_profile_photo` takes true/false
- `display_entry_society_first` true bolds the company first, false bolds the role first
- `email` picks which contact address shows
- Any `personal.info` field set to `""` is hidden

### 2. Point at data files

The generic `experience`, `projects`, and `skills` modules read their data file from `[modules]` keys in the merged metadata:

```toml
[modules]
experience_file = "<variant>-experience.toml"
projects_file = "<variant>-projects.toml"
skills_file = "<variant>-skills.toml"
```

### 3. Create the data files

- `metadata/<variant>-experience.toml`: a `[jobs]` table whose entries have `title`, `company`, `date`, `location`, optional `summary`.
- `metadata/<variant>-skills.toml`: a top-level `section_title` plus a `[skills]` table whose entries have `type` and `info`.
- `metadata/<variant>-projects.toml`: a `[projects]` table.

### 4. Create the entry .typ file

```typst
#import "../src/lib.typ": cv
#import "../src/meta.typ": importModules, makeMeta
#import "../modules/experience.typ": experience
#import "../modules/skills.typ": skills

#let variant-metadata = makeMeta("<variant>-metadata.toml")

#show: cv.with(
  variant-metadata,
  profilePhoto: image("../metadata/qr-code.png"),
)

#experience(variant-metadata)
#importModules(("education",))
#skills(variant-metadata)
```

### 5. Add a new module, if the job needs a section that does not exist

Prefer the function-style pattern in `modules/<section>.typ`:

```typst
#import "../src/lib.typ": cvEntry, cvSection

#let mySection(metadata) = {
  let data = toml("../metadata/" + metadata.modules.my_section_file)
  cvSection("Section Title", metadata: metadata)
  // render entries from `data`
}
```

Then add `my_section_file = "..."` to the override TOML and import and call `mySection(metadata)` from the entry file.

### 6. Register the variant

Add a section to `variants.toml`:

```toml
[my-variant]
source = "my-variant"                          # stem of resumes/<source>.typ
dest = "my-variant"                            # output filename stem and Pages basename
expected_pages = 1                             # exact page count (0 = multi-page, checks >= 1)
check_metadata = true                          # validate merged metadata for completeness
# override_toml = "my-variant-metadata.toml"   # only if step 1 created an override
```

Build and confirm the page count matches `expected_pages`; the check fails the build otherwise.

## Writing Resume Content

Applies to job descriptions, summaries, header quotes, and cover letter body text. The goal is copy that reads like a capable person wrote it at midnight with a glass of wine, not like it was extruded from a language model.

### Voice and tone

- **Write like a human, not a hiring-advice blog.** Vary sentence length. Start a sentence with "and" or "but" where it sounds natural. Use contractions. Let the occasional short fragment stand on its own.
- **Match formality to the audience, not to a universal "resume voice."** A nanny resume sounds warm and grounded. A tech resume is direct and precise. An events resume feels energetic and competent. None of them sound like a LinkedIn post.
- **Default register: confident and specific, slightly casual.** Aim for someone explaining what they did to a friend who works in the field. Not a cover letter, not a text message. `metadata/work-experience.toml` is the reference voice.
- **Pick one grammatical person per variant and hold it.** Third-person implied subject ("Ran the front desk", "Designed lighting for...") is standard for professional variants. First person is fine in nanny and cover-letter variants.

### Tailoring to a job posting

- **Echo the posting's concepts, not its exact phrases.** Where a posting says "cross-functional collaboration," write "worked across teams." Mirror the idea; use your own words.
- **Foreground relevant experience, and keep it true.** Reorder bullets, emphasize different aspects of the same role, expand details that align with the target. Every responsibility and skill traces back to `REFERENCE.md`.
- **Cap keyword echoes at one or two per description.** More trips ATS-gaming detectors and human suspicion alike. Scatter them across entries rather than clustering.
- **Adjust `header_quote` to the posting's core need**, phrased as something the candidate would actually say about themselves rather than a rephrased job title.

### AI tells to rewrite

Each entry names the tell, then the replacement. Apply the replacement.

- **Hollow intensifiers** ("leveraged", "utilized", "spearheaded", "orchestrated", "facilitated", "architected" as a verb) become plain verbs: ran, built, designed, set up, handled, wrote, fixed, managed.
- **Stacked buzzwords** ("Engineered scalable cloud-native microservice architecture") become a statement of what was built and what it does.
- **Symmetrical structure**, where every bullet runs `[past-tense verb] [object] [prepositional phrase] [result clause]`, becomes varied structure: some bullets two sentences, some ending without a result.
- **Vague impact claims** ("resulting in improved efficiency", "driving significant growth") become a real number, or the claim comes off entirely.
- **Thesaurus cycling** across "oversaw", "directed", "coordinated", "supervised" becomes repeating "managed" wherever "managed" is the accurate word.
- **Acronym drops with parenthetical expansion on every mention** ("Infrastructure as Code (IaC)") become one spelled-out first use, then the bare acronym.
- **Punctuation and dressing**: use plain ASCII text, commas, colons, and parentheses. Hard guardrail: this repo ships no em dashes, in resume copy or in this file. Use a comma, a colon, parentheses, or a full stop instead.

### Before finalizing

1. **Read it aloud.** If it sounds like a press release, rewrite it.
2. **Could you picture the person saying this in an interview?** If not, it is too stiff.
3. **Does every sentence carry a concrete detail** (a tool name, a number, a specific task)? If it is all abstract, it is filler.
4. **More than two adjectives in a sentence?** Cut some.
5. **Would a recruiter reading 200 resumes a day notice anything unusual?** That is the bar: invisible competence, not performance.

## Layout and Components

Layouts live in `src/lib.typ` (`cv`, `coverLetter`, `letter`); entry and row components in `src/cv.typ` (`cvSection`, `cvEntry`, `cvSkill`, `cvTraining`, `cvPerformance`, `cvHonor`); metadata merging in `src/meta.typ` (`makeMeta`, `importModules`) over `src/utils/merge.typ::mergeDicts`. Grep for a name to get its current signature.

## Commit Conventions

Conventional Commits, so `git-cliff` can group changes.

- `type(scope): short summary`, or `type(scope)!:` for breaking changes
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- Preferred scopes: `reformat` (layout/formatting), `template` (template/module structure), `content` (resume text)

```
feat(template): add reusable project entry block
fix(content): correct work experience date
style(reformat): tighten section spacing
```

Release: `just bump <patch|minor|major>` triggers the GitHub Actions release workflow.
