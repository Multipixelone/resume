# PDF submission dates

## Build before submitting

Run from the repository with Python 3 (standard library, including the
`America/New_York` timezone database) and Nix available:

```sh
python3 scripts/build-resume.py
python3 scripts/build-resume.py --date 2026-10-21
python3 scripts/build-resume.py --date 2026-10-21 resume
python3 scripts/build-resume.py finn-rutis
```

The default outputs are `resume` (all registered variants and previews) and
`finn-rutis` (cropped theatre CV plus portrait page). Supply either or both
positional output names to select them explicitly. The wrapper resolves today's
Eastern calendar date **once**, including daylight saving time, and prints it
before building. Both packages use that same date, including the portrait-page
compilation. An explicit `--date YYYY-MM-DD` skips the clock and validates the
actual calendar date, not just its spelling.

The wrapper uses one argv-based `nix build --impure --expr` invocation, a trusted
repository path resolved from the script location, `builtins.getFlake` on that
path as a `git+file://` URI (a bare path drops the commit rev and the footer
reads "commit dirty"), and the local `builtins.currentSystem`. Each selected
package receives `.override { submissionDate = "YYYY-MM-DD"; }`. No shell
interprets the command.
Repository strings are quoted with Nix interpolation disabled. `--no-link
--print-out-paths` prints store output directories without creating or overwriting
a shared `result` symlink. The subprocess runs from the repository and its exit
status is returned to the caller. `--impure` permits local flake/system evaluation;
there are no wall-clock reads inside the derivations.

## Plain builds are archived snapshots

```sh
nix build .#resume
nix build .#finn-rutis
```

These ordinary pure builds use the checked-in `metadata/submission-date.txt`:
**2026-10-21**. This is an explicit archived snapshot/build date, not today's
submission date and not a show date. Use the wrapper before submitting. Do not
advance the archive file merely to submit a current copy.

The flake reads the archive default once and passes it to both package functions;
each function also has that file as its standalone default. Both packages reject
invalid literal ISO dates. Their existing source version/revision provenance,
output names, and local-build scheduling settings remain separate and unchanged.
The submission date affects Typst commands and therefore derivation identity.

An explicit date is repeatable with the same source, locked dependencies, and
build environment. It alone does not pin source or tools. No source mtime,
`builtins.currentTime`, phase-time clock, or environment date controls lifecycle
or footer dates. `--input version=...` is provenance only, not a build-date input.

## Typst quick compiles

```sh
typst compile --root . --input submission-date=2026-10-21 resumes/cv.typ
```

`src/utils/date.typ::buildDate()` passes an explicit `submission-date` to the
shared `parseISODate` helper, which requires an actual Gregorian `YYYY-MM-DD`
date in years 0001 through 9999. Malformed, empty, and impossible dates fail.
This validation sees the value **after Typst CLI normalization**: Typst 0.15.0
trims a leading space or trailing newline from `--input` values before exposing
them through `sys.inputs`. Such raw CLI arguments therefore arrive as normalized
dates, not rejected whitespace-containing strings. Direct strings passed to
`parseISODate` or through `showUpcoming` remain strict and reject that whitespace.

Without the submission input, direct manual Typst compiles retain
`datetime.today()` for the repository's quick-preview
convention. That fallback is local/manual and **nonreproducible**, not the Eastern
submission workflow. Submission builds use the wrapper and always supply the
input; providing only `version` does not select a date.

The explicit date governs PDF upcoming markers and footer build dates. A
selected credit loses its upcoming marker at performance start; closing does not
remove selected credits. This plumbing does not add or infer show lifecycle dates.

## Focused tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_submission_date.py -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_typst_dates.py -v
```

The submission-wrapper suite mocks Nix and the clock. The Typst date suite invokes
the actual compiler with `tests/date-input.typ`, including JSON-encoded strings
that preserve literal whitespace inside Typst and separate normalized CLI cases.
It also covers year zero, impossible dates, valid leap dates, explicit-date
precedence, and manual fallback. Neither suite proves package evaluation,
rendered resume content, or byte reproducibility; those need separate integrated
Nix/PDF checks. Follow the repository's long-run helper instructions for long
tests and builds.
