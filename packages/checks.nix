{
  lib,
  pkgs,
  resume,
  src,
}:
let
  python = pkgs.python3;

  # Expected page counts per PDF output.
  # Resumes and cover letter must be exactly 1 page.
  # Rep-sheet and title-pages are multi-page.
  expectedPages = {
    "cv" = 1;
    "tech" = 2;
    "work" = 1;
    "nanny" = 1;
    "saltandstraw" = 1;
    "saltandstraw-sc" = 1;
    "cover-letter" = 1;
    # rep-sheet and title-pages are variable length; checked as >= 1
  };

  # All files the resume package should produce.
  # When you add a new resume variant, add its outputs here AND to expectedPages.
  # The no-unchecked-outputs check will fail if you forget.
  expectedOutputs = [
    "CV_FinnRutis_*.pdf"
    "CV_FinnRutis_*.png"
    "Rep-Sheet_FinnRutis_*.pdf"
    "Title-Pages_FinnRutis_*.pdf"
    "Tech_CV_FinnRutis_*.pdf"
    "Work_CV_FinnRutis_*.pdf"
    "Work_CV_FinnRutis_*.png"
    "Nanny_CV_FinnRutis_*.pdf"
    "Nanny_CV_FinnRutis_*.png"
    "Cover_Letter_FinnRutis_*.pdf"
    "SaltAndStraw_CV_FinnRutis_*.pdf"
    "SaltAndStraw_CV_FinnRutis_*.png"
    "SaltAndStraw_SC_CV_FinnRutis_*.pdf"
    "SaltAndStraw_SC_CV_FinnRutis_*.png"
  ];

  overrideFilesJSON = builtins.toJSON [
    "tech-metadata.toml"
    "work-metadata.toml"
    "nanny-metadata.toml"
    "saltandstraw-metadata.toml"
    "saltandstraw-sc-metadata.toml"
    "title-pages-metadata.toml"
  ];

  variantsJSON = builtins.toJSON {
    "base" = "";
    "tech" = "tech-metadata.toml";
    "work" = "work-metadata.toml";
    "nanny" = "nanny-metadata.toml";
    "saltandstraw" = "saltandstraw-metadata.toml";
    "saltandstraw-sc" = "saltandstraw-sc-metadata.toml";
  };

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
        ${lib.concatMapStringsSep "\n" (pattern: ''
          count=$(ls ${resume}/${pattern} 2>/dev/null | wc -l)
          if [ "$count" -eq 0 ]; then
            echo "FAIL: no file matching ${pattern}"
            failed=1
          elif [ "$count" -gt 1 ]; then
            echo "FAIL: multiple files matching ${pattern}"
            failed=1
          else
            file=$(ls ${resume}/${pattern})
            size=$(stat -c%s "$file")
            if [ "$size" -eq 0 ]; then
              echo "FAIL: $file is empty (0 bytes)"
              failed=1
            fi
          fi
        '') expectedOutputs}
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
            stem: expected:
            let
              pdfPattern =
                {
                  "cv" = "CV_FinnRutis_*.pdf";
                  "tech" = "Tech_CV_FinnRutis_*.pdf";
                  "work" = "Work_CV_FinnRutis_*.pdf";
                  "nanny" = "Nanny_CV_FinnRutis_*.pdf";
                  "saltandstraw" = "SaltAndStraw_CV_FinnRutis_*.pdf";
                  "saltandstraw-sc" = "SaltAndStraw_SC_CV_FinnRutis_*.pdf";
                  "cover-letter" = "Cover_Letter_FinnRutis_*.pdf";
                }
                .${stem};
            in
            ''
              pdf=$(ls ${resume}/${pdfPattern} 2>/dev/null | head -1)
              if [ -n "$pdf" ]; then
                pages=$(qpdf --show-npages "$pdf")
                if [ "$pages" -ne ${toString expected} ]; then
                  echo "FAIL: ${stem} has $pages page(s), expected ${toString expected}"
                  failed=1
                else
                  echo "OK: ${stem} = $pages page(s)"
                fi
              else
                echo "SKIP: ${stem} PDF not found (caught by output-files check)"
              fi
            ''
          ) expectedPages
        )}

        # Multi-page PDFs: just check they have at least 1 page
        for pattern in "Rep-Sheet_FinnRutis_*.pdf" "Title-Pages_FinnRutis_*.pdf"; do
          pdf=$(ls ${resume}/$pattern 2>/dev/null | head -1)
          if [ -n "$pdf" ]; then
            pages=$(qpdf --show-npages "$pdf")
            if [ "$pages" -lt 1 ]; then
              echo "FAIL: $pattern has 0 pages"
              failed=1
            else
              echo "OK: $pattern = $pages page(s)"
            fi
          fi
        done

        if [ "$failed" -eq 1 ]; then
          exit 1
        fi
        echo "All PDF page counts match expectations."
        touch $out
      '';

  # ── 6. No unchecked outputs ─────────────────────────────────────────────────
  # Fails if the resume package produces files not listed in expectedOutputs.
  # This catches new variants added to resume.nix but not to checks.nix.
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
