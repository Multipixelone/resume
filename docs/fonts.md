# Resume fonts

Every resume, letter, and the finn-rutis composite set in Sabon Next LT Pro,
with EB Garamond as the open fallback. Both are listed in
`metadata/metadata.toml` under `[layout.fonts]`.

## Where Sabon comes from

Sabon Next is licensed, so it never enters this repository. The OTFs live in
the private repo `Multipixelone/fonts` under `sabon-next/`. Their OS/2 embedding
flag is "preview and print", which permits the subset embedding Typst does in
PDFs.

The flake reads `RESUME_FONT_DIR` with `builtins.getEnv`, so it only sees it in
an `--impure` evaluation. When set, `packages/resume.nix` and
`packages/finn-rutis.nix` link every `.otf` under that directory into the Typst
font path, and `postInstall` fails the build unless each PDF embeds
`SabonNextLTPro`. When unset (any pure build), the PDFs use EB Garamond from
`texlivePackages.ebgaramond`. The nixpkgs `eb-garamond` package is the old 0.016
cut, whose family is "EB Garamond 12" with no bold, so it cannot be the fallback.

Supplying the directory copies the fonts into the local Nix store. That is
acceptable on a licensed machine and on ephemeral CI runners; nothing here
pushes to a binary cache.

## Local builds

```sh
git clone git@github.com:Multipixelone/fonts.git ~/Documents/Git/fonts
RESUME_FONT_DIR=~/Documents/Git/fonts/sabon-next nix build --impure .#resume
RESUME_FONT_DIR=~/Documents/Git/fonts/sabon-next python3 scripts/build-resume.py
```

`scripts/build-resume.py` already evaluates with `--impure`, so it picks the
variable up. Plain `nix build .#resume` gives the EB Garamond fallback.

## CI

`.github/actions/licensed-fonts` checks out `Multipixelone/fonts` with the
`RESUME_FONTS_SSH_KEY` secret (a read-only deploy key on that repo) into
`.ci-fonts/` and exports `RESUME_FONT_DIR`. Builds then run with `--impure`.

| Workflow | Without the key |
|---|---|
| CI (`ci.yml`, `_build.yml` on push and PR) | Falls back to EB Garamond with a notice |
| Release PDFs (`post-release.yml`) | Fails |
| Pages deploy (`website.yml`) | Fails |

`nix flake check` stays pure, so it exercises the fallback.

## Size

Sabon's x-height (0.439 em) runs about 11% above a classic Garamond. Every
layout size goes through `fs()` in `src/utils/styles.typ`, which multiplies by
`typeScale = 0.95`, giving a 9.5pt body. Proofs comparing the Garamond
alternatives, normalized by x-height, informed that choice. The EB Garamond
fallback sets slightly smaller at the same scale.
