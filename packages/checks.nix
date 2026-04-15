{
  lib,
  pkgs,
  resume,
  src,
}:
let
  python = pkgs.python3;
  variants = builtins.fromTOML (builtins.readFile ../variants.toml);

  # Every variant produces both PDF and PNG
  expectedOutputs = lib.concatLists (
    lib.mapAttrsToList (_: v: [
      "${v.dest}.pdf"
      "${v.dest}.png"
    ]) variants
  );

  # Override TOMLs that should be validated for key correctness
  overrideFilesJSON = builtins.toJSON (
    lib.filter (f: f != null) (lib.mapAttrsToList (_: v: v.override_toml or null) variants)
  );

  # Variants whose merged metadata should be checked for completeness
  variantsJSON = builtins.toJSON (
    lib.mapAttrs (_: v: v.override_toml or "") (lib.filterAttrs (_: v: v.check_metadata) variants)
  );

  # Split variants by page-count mode
  fixedPageVariants = lib.filterAttrs (_: v: v.expected_pages > 0) variants;
  multiPageVariants = lib.filterAttrs (_: v: v.expected_pages == 0) variants;

  expectedOutputsJSON = builtins.toJSON expectedOutputs;

  # ── Python scripts written as separate files to avoid Nix string escaping ──

  tomlValidityScript = pkgs.writeText "check-toml-validity.py" ''
    import tomllib, sys, pathlib, json

    base_path = pathlib.Path('metadata.toml')
    base = tomllib.loads(base_path.read_text())

    def all_keys(d, prefix=""):
        keys = set()
        for k, v in d.items():
            full = f"{prefix}.{k}" if prefix else k
            keys.add(full)
            if isinstance(v, dict):
                keys |= all_keys(v, full)
        return keys

    base_keys = all_keys(base)
    errors = []

    for f in sorted(pathlib.Path('.').glob('*.toml')):
        try:
            tomllib.loads(f.read_text())
        except Exception as e:
            errors.append(f'  {f}: parse error: {e}')

    override_files = json.loads(sys.argv[1])
    for name in override_files:
        p = pathlib.Path(name)
        if not p.exists():
            errors.append(f'  {name}: file not found')
            continue
        try:
            override = tomllib.loads(p.read_text())
        except Exception:
            continue
        override_keys = all_keys(override)
        unknown = override_keys - base_keys
        if unknown:
            unknown = {k for k in unknown if not k.startswith('personal.info.')}
        if unknown:
            errors.append(f'  {name}: unknown keys not in base metadata.toml: {sorted(unknown)}')

    if errors:
        print('TOML validation errors:')
        for e in errors:
            print(e)
        sys.exit(1)
    print('All TOML files are valid.')
  '';

  metadataCompletenessScript = pkgs.writeText "check-metadata-completeness.py" ''
    import tomllib, sys, pathlib, copy, json

    def merge(base, override):
        result = copy.deepcopy(base)
        for k, v in override.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = merge(result[k], v)
            else:
                result[k] = v
        return result

    def get_nested(d, path):
        for key in path:
            if not isinstance(d, dict) or key not in d:
                return None
            d = d[key]
        return d

    base = tomllib.loads(pathlib.Path('metadata.toml').read_text())

    required = [
        ('personal', 'first_name'),
        ('personal', 'last_name'),
        ('personal', 'info', 'email'),
        ('lang', 'en', 'header_quote'),
        ('lang', 'en', 'cv_footer'),
    ]

    variants = json.loads(sys.argv[1])
    errors = []
    for name, override_file in variants.items():
        if override_file:
            override = tomllib.loads(pathlib.Path(override_file).read_text())
            merged = merge(base, override)
        else:
            merged = base

        for path in required:
            val = get_nested(merged, path)
            dotpath = '.'.join(path)
            if val is None:
                errors.append(f'  {name}: missing {dotpath}')
            elif isinstance(val, str) and val.strip() == "":
                errors.append(f'  {name}: empty {dotpath}')

    if errors:
        print('Metadata completeness errors:')
        for e in errors:
            print(e)
        sys.exit(1)
    print('All variants have required metadata fields.')
  '';

  noUncheckedOutputsScript = pkgs.writeText "check-no-unchecked-outputs.py" ''
    import sys, json, pathlib, fnmatch

    expected_patterns = json.loads(sys.argv[1])
    output_dir = pathlib.Path(sys.argv[2])

    actual_files = sorted(f.name for f in output_dir.iterdir() if f.is_file())
    unchecked = []
    for filename in actual_files:
        if not any(fnmatch.fnmatch(filename, pat) for pat in expected_patterns):
            unchecked.append(filename)

    if unchecked:
        print("Files produced by resume build but not listed in expectedOutputs:")
        for f in unchecked:
            print(f"  {f}")
        print()
        print("Add these patterns to expectedOutputs in packages/checks.nix.")
        sys.exit(1)
    print("All resume outputs are covered by checks.")
  '';
in
{
  # ── 1. typstyle formatting ──────────────────────────────────────────────────
  typstyle =
    pkgs.runCommandLocal "check-typstyle"
      {
        nativeBuildInputs = [ pkgs.typstyle ];
      }
      ''
        cd ${src}
        failed=0
        for f in $(find . -name '*.typ' -type f); do
          if ! typstyle --check "$f" 2>/dev/null; then
            echo "FAIL: $f is not formatted"
            failed=1
          fi
        done
        if [ "$failed" -eq 1 ]; then
          echo ""
          echo "Run typstyle to fix formatting."
          exit 1
        fi
        echo "All .typ files are correctly formatted."
        touch $out
      '';

  # ── 2. TOML validity + override key check ───────────────────────────────────
  toml-validity =
    pkgs.runCommandLocal "check-toml-validity"
      {
        nativeBuildInputs = [ python ];
      }
      ''
        cd ${src}/metadata
        python3 ${tomlValidityScript} '${overrideFilesJSON}'
        touch $out
      '';

  # ── 3. Metadata completeness ────────────────────────────────────────────────
  metadata-completeness =
    pkgs.runCommandLocal "check-metadata-completeness"
      {
        nativeBuildInputs = [ python ];
      }
      ''
        cd ${src}/metadata
        python3 ${metadataCompletenessScript} '${variantsJSON}'
        touch $out
      '';

  # ── 4. Output file existence ────────────────────────────────────────────────
  output-files =
    pkgs.runCommandLocal "check-output-files"
      { }
      ''
        failed=0
        ${lib.concatMapStringsSep "\n" (
          filename: ''
            file=${resume}/${filename}
            if [ ! -f "$file" ]; then
              echo "FAIL: missing ${filename}"
              failed=1
            else
              size=$(stat -c%s "$file")
              if [ "$size" -eq 0 ]; then
                echo "FAIL: ${filename} is empty (0 bytes)"
                failed=1
              fi
            fi
          ''
        ) expectedOutputs}
        if [ "$failed" -eq 1 ]; then
          exit 1
        fi
        echo "All expected output files present and non-empty."
        touch $out
      '';

  # ── 5. PDF page count ──────────────────────────────────────────────────────
  pdf-page-count =
    pkgs.runCommandLocal "check-pdf-page-count"
      {
        nativeBuildInputs = [ pkgs.qpdf ];
      }
      ''
        failed=0

        ${lib.concatStringsSep "\n" (
          lib.mapAttrsToList (
            name: v: ''
              pdf=${resume}/${v.dest}.pdf
              if [ -f "$pdf" ]; then
                pages=$(qpdf --show-npages "$pdf")
                if [ "$pages" -ne ${toString v.expected_pages} ]; then
                  echo "FAIL: ${name} has $pages page(s), expected ${toString v.expected_pages}"
                  failed=1
                else
                  echo "OK: ${name} = $pages page(s)"
                fi
              else
                echo "SKIP: ${name} PDF not found (caught by output-files check)"
              fi
            ''
          ) fixedPageVariants
        )}

        ${lib.concatStringsSep "\n" (
          lib.mapAttrsToList (
            name: v: ''
              pdf=${resume}/${v.dest}.pdf
              if [ -f "$pdf" ]; then
                pages=$(qpdf --show-npages "$pdf")
                if [ "$pages" -lt 1 ]; then
                  echo "FAIL: ${name} has 0 pages"
                  failed=1
                else
                  echo "OK: ${name} = $pages page(s)"
                fi
              fi
            ''
          ) multiPageVariants
        )}

        if [ "$failed" -eq 1 ]; then
          exit 1
        fi
        echo "All PDF page counts match expectations."
        touch $out
      '';

  # ── 6. No unchecked outputs ─────────────────────────────────────────────────
  # Fails if the resume package produces files not listed in expectedOutputs.
  no-unchecked-outputs =
    pkgs.runCommandLocal "check-no-unchecked-outputs"
      {
        nativeBuildInputs = [ python ];
      }
      ''
        python3 ${noUncheckedOutputsScript} '${expectedOutputsJSON}' ${resume}
        touch $out
      '';
}
