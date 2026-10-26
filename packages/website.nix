{
  lib,
  buildNpmPackage,
  nodejs_24,
  python3,
  version ? "",
  # "<rev>", "<rev>-dirty", or "" (footer then links the repo, not a commit).
  commit ? "",
  resume,
  finnRutis,
  siteBase ? "",
  # Scheme and host for absolute Open Graph URLs; "" means https://finnrut.is.
  siteOrigin ? "",
}:
assert lib.assertMsg (
  builtins.isString siteBase
  && (siteBase == "" || builtins.match "/[A-Za-z0-9_-]+(/[A-Za-z0-9_-]+)*" siteBase != null)
) "siteBase must be empty or a root-relative path without a trailing slash";
assert lib.assertMsg (
  builtins.isString siteOrigin
  && (siteOrigin == "" || builtins.match "https?://[A-Za-z0-9-]+([.][A-Za-z0-9-]+)+" siteOrigin != null)
) "siteOrigin must be empty or a scheme and host without a path or trailing slash";
buildNpmPackage {
  pname = "finnrut.is";
  inherit version;
  nodejs = nodejs_24;

  # Keep repository-relative imports, without admitting the PDF sources, archive,
  # reports, or other repository content into the npm sandbox.
  src = lib.cleanSourceWith {
    name = "source";
    src = ../.;
    filter = path: type:
      let
        relative = lib.removePrefix (toString ../. + "/") (toString path);
        parts = lib.splitString "/" relative;
      in
      (relative == "website" || lib.hasPrefix "website/" relative
        || builtins.elem relative [ "lib" "lib/shows.mjs" "metadata" "metadata/theatre.toml" "metadata/film.toml" "variants.toml" "scripts" "scripts/assemble-portfolio.py" ])
      && !lib.any (part: builtins.elem part [ "node_modules" ".svelte-kit" "build" ".git" "__pycache__" "test-results" "playwright-report" ]) parts;
  };
  # Both fetchNpmDeps and the build unpack the same tree and enter website/.
  # npmRoot is not forwarded to fetchNpmDeps by this pinned buildNpmPackage.
  sourceRoot = "source/website";
  npmDepsHash = "sha256-3Mju/IYqEwm/teBIbN/zk/cnWEmCS74rbWjRyQ7y4co=";
  env.SITE_BASE = siteBase;
  env.SITE_ORIGIN = siteOrigin;
  env.SITE_COMMIT = commit;
  nativeBuildInputs = [ (python3.withPackages (p: [ p.pillow ])) ];

  installPhase = ''
    runHook preInstall
    python3 ../scripts/assemble-portfolio.py \
      --website build \
      --resume ${resume} \
      --composite ${lib.escapeShellArg "${finnRutis}/FINN RUTIS.pdf"} \
      --registry ../variants.toml \
      --output "$out"
    runHook postInstall
  '';

  meta.license = lib.licenses.gpl3Only;
}
