# Complete portfolio package

`packages/website.nix` builds the SvelteKit static application and assembles the
existing `resume` and `finn-rutis` package outputs. The flake passes those same
derivations to the website package. There is no separate CI assembly algorithm.

## Mount and output contract

The default `siteBase ? ""` builds for root/custom-domain hosting:

```sh
nix build .#website
```

For repository Pages, override the function argument, not only a shell variable:

```sh
nix build --impure --expr '(builtins.getFlake "git+file://${toString ./.}").packages.${builtins.currentSystem}.website.override { siteBase = "/resume"; }'
```

The argument becomes `SITE_BASE` during the npm build. Nix validates the same
empty-or-root-relative-path grammar as `website/lib/config.mjs`: ASCII letters,
digits, underscores and hyphens in nonempty segments; no trailing slash. The
site's existing validator also runs during Svelte configuration. A mount changes
URLs, not the on-disk directory layout: there is no extra `resume/` wrapper.

Link previews need absolute URLs, so the package also takes `siteOrigin ? ""`,
the scheme and host the Open Graph tags resolve against. Empty means
`https://finnrut.is`; the Pages workflow passes the configured origin, so a
repository mount on `github.io` previews its own copy of the social card.
`website/lib/config.mjs` validates the same scheme-and-host grammar.

The final derivation output is the static hosting root:

```text
index.html                       real Svelte homepage, not the old download index
resume/index.html                theatre page
performance-reel/index.html
booking/index.html
resumes/index.html               real Svelte download index
resumes/<registry dest>.pdf       every registry variant, including hidden entries
resumes/<registry dest>.png       first-page preview for every variant
resumes/FINN RUTIS.pdf            separate composite package's actual file
.nojekyll
_app/...                         plus the site's static fonts/media/assets
```

At the current registry size, assembly adds 83 documents (41 PDF/PNG pairs plus
the composite). `resumes/` also holds its HTML index and SvelteKit's
`__data.json` route data.
The UI's 7 listed variants expose 15 document links including the composite;
`site_hidden` only unlists an entry, so its PDF still answers at its direct link. These counts are
descriptive, not a second hard-coded registry.

## Minimal source and npm boundary

The npm source preserves repository layout but admits only:

- `website/`, excluding generated `node_modules`, `.svelte-kit`, `build`, `.git`
  and `__pycache__` directories;
- `lib/shows.mjs`;
- `metadata/theatre.toml`;
- `variants.toml`;
- `scripts/assemble-portfolio.py`.

PDF/Typst source, unrelated metadata, media archives, reports, workflows, and
repository tooling do not enter this source. PDF builds have their own existing
sources and are separate derivation dependencies, not npm inputs.

The pinned nixpkgs `buildNpmPackage` forwards `sourceRoot` to `fetchNpmDeps` but
does not forward `npmRoot`. Both dependency fetching and building therefore use
`sourceRoot = "source/website"` after unpacking the complete minimal tree. The
adjacent canonical inputs survive unpacking, so existing root-relative aliases
and imports need no patching. Node 24 satisfies the site's Node >=22.17 floor.
The npm lock determines the fixed-output dependency hash. Output comes from
SvelteKit's `build/`, not Astro's obsolete `dist/`.

## Assembly script interface

Python 3.11+ stdlib only, using the actual `tomllib` parser:

```sh
python3 scripts/assemble-portfolio.py \
  --website /path/to/website/build \
  --resume /path/to/resume-package-output \
  --composite '/path/to/composite-package-output/FINN RUTIS.pdf' \
  --registry variants.toml \
  --output /path/to/new-hosting-root
```

`--website` is the built static directory, not the site source. `--resume` is
the flat package directory containing `<dest>.pdf` and `<dest>.png` (not the
Typst `source` stem). `--composite` is a file, not its parent package directory.
`--output` must not already exist or be inside the website input directory.

Before copying, the script validates both real HTML indexes, parses the registry,
rejects unsafe/duplicate destination stems, checks every required PDF/PNG and
composite for existence and nonzero size, and rejects collisions with website
content. Website symlinks are rejected to avoid out-of-tree or dangling inputs.
Hidden variants use the same required-input checks. It copies the built site,
adds the validated artifacts and `.nojekyll`, and exits nonzero on errors.
Preflight prevents known bad inputs from producing partial output; unexpected
I/O errors during copying can still leave a partial directory and return failure.
Nix will not publish that failed derivation as a successful package.

## Focused test and validation ownership

```sh
python3 -B -m unittest discover -s tests -p test_portfolio_assembly.py -v
```

Tests use synthetic artifact bytes to exercise copying and fail-closed behavior;
they do not establish PDF/PNG validity. The actual registry test derives expected
destinations from canonical TOML rather than a second list. Independent full
package validation must build both mount configurations, inspect real artifacts
and HTTP paths, verify source isolation and Svelte output, and confirm the
override through the exported flake package. Follow `agent-run-long` for long
Linux validation. Font/media permissions and public publishing remain separate
gates; package implementation is not deployment approval.
