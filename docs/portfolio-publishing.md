# Portfolio publishing

## Independent publication lanes

`website.yml` builds on every push to `main`, with no path filter that could miss
a Nix artifact input. It also supports manual dispatch on `main`. The workflow
does not depend on a release, tag, PDF workflow artifact, or scheduled rebuild.
Current-project status is calculated in the browser, not by a daily build.

The build reads the existing Pages configuration with `configure-pages@v6`.
Its `base_path` selects the empty root/custom-domain mount or the repository
mount (normally `/resume`). A single `/` is normalized to the empty string;
other nonempty values must be slash-separated ASCII letters, digits, underscores
or hyphens, with no trailing slash. The value travels through an environment
variable and `builtins.getEnv`, never interpolation into Nix source. `--impure`
permits those explicit environment reads; the flake is obtained from the absolute
checkout path in `GITHUB_WORKSPACE`.

The same step passes the Pages `origin` output as `siteOrigin`, which the Open
Graph tags use to make the social card URL absolute. It must be `http` or `https`
plus a host, with no path or trailing slash.

The workflow builds this package contract:

```nix
flake.packages.x86_64-linux.website.override { siteBase = ""; }
```

The package, not workflow assembly code, owns the complete static output:
five directory-based HTML routes, static assets, `.nojekyll`, all registry PDF
and PNG destinations under `resumes/`, and `resumes/FINN RUTIS.pdf`. The current
registry has 37 variants, including hidden variants whose artifacts remain
available. There is no second variant registry and no use of `site/index.html`.
The configured mount affects generated URLs, not an extra output directory.
The workflow uploads this output directly as a Pages artifact, then a separate
deployment job publishes it through the `github-pages` environment.

The workflow-level `pages` concurrency group serializes Pages publishing without
cancelling an in-progress deployment. Build permissions are `contents: read`
and `pages: read`; only deployment receives `pages: write` and `id-token: write`.
Both jobs require the intended push/manual event and `refs/heads/main`. Configure
the repository's Pages source as GitHub Actions and protect the `github-pages`
environment as appropriate before an authorized launch. This implementation does
not modify repository settings, DNS, custom domains, accounts, or add a CNAME.

## PDF releases and pull requests

`_build.yml` is now only a reusable PDF build/export workflow. Its explicit package
matrix contains `resume` and `finn-rutis`, not a second list of variants. When
`export_pdfs` is true, it reads `variants.toml`, requires every PDF and the
composite to exist and be nonempty, then exports a flat `release-pdfs` artifact
with the existing filenames. Missing files fail the job before upload. PNGs are
not release assets. PDF-only builds do not configure or deploy Pages.

`post-release.yml` still tags merged `release/v*` pull requests and creates the
GitHub release with its existing notes and PDF attachments. It still requests
`export_pdfs: true`, but has no Pages permissions or Pages concurrency lock.
Website changes can therefore publish independently of the PDF release cycle.

`ci.yml` retains flake checks and reusable PDF builds. A separate website matrix
builds the complete Nix website package with both empty and `/resume` mounts on
push, pull request, and manual CI runs. CI has only contents-read permission and
does not configure Pages, upload a Pages artifact, or deploy. Relevant package
checks remain owned by the Nix package/check definitions.

## Validation and launch boundaries

Independent validation should run actionlint on the four changed workflows,
inspect reusable workflow callers, and build the complete website package for
both mounts. Serve each output at its matching mount and verify all five direct
HTML routes, every registry PDF/PNG, the encoded composite URL, and `.nojekyll`.
Check the release export's complete flat filenames and its missing/empty failure
behavior separately. Use the repository's long-run helper for Nix validation.

No workflow has been executed or deployment attempted by the implementation lane.
Build/test success must be established after the parallel package changes are
reconciled. Font authorization/delivery, media rights/credits/captions, and other
public-launch gates in `docs/portfolio-site.md` remain unresolved by CI wiring.
Future pushes to `main` will trigger the implemented publisher once merged;
merging or dispatching it requires the appropriate launch authorization and
environment safeguards. No push, deploy, DNS/account action, or Squarespace
cancellation is authorized by this document.
