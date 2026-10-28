{
  lib,
  stdenv,
  typst,
  typstPackages,
  font-awesome,
  roboto,
  source-sans-pro,
  texlivePackages,
  poppler-utils,
  ghostscript,
  inputs,
  version ? "",
  commit ? "unknown",
  submissionDate ? lib.removeSuffix "\n" (builtins.readFile ../metadata/submission-date.txt),
  # Out-of-tree licensed fonts (see docs/fonts.md); null falls back to EB Garamond.
  extraFonts ? null,
  src ? null,
}:
let
  decimal = value: builtins.foldl' (n: digit: n * 10 + builtins.fromJSON digit) 0 (lib.stringToCharacters value);
  dateParts = if builtins.isString submissionDate then builtins.match "([0-9]{4})-([0-9]{2})-([0-9]{2})" submissionDate else null;
  validSubmissionDate = dateParts != null && (
    let
      year = decimal (builtins.elemAt dateParts 0);
      month = decimal (builtins.elemAt dateParts 1);
      day = decimal (builtins.elemAt dateParts 2);
      leap = lib.mod year 4 == 0 && (lib.mod year 100 != 0 || lib.mod year 400 == 0);
      days = [ 31 (if leap then 29 else 28) 31 30 31 30 31 31 30 31 30 31 ];
    in
    year >= 1 && month >= 1 && month <= 12 && day >= 1 && day <= builtins.elemAt days (month - 1)
  );
  typstWithPackages = typst.withPackages (ps: [ typstPackages.fontawesome_0_6_2 ]);
in
assert lib.assertMsg validSubmissionDate "submissionDate must be a real ISO calendar date (YYYY-MM-DD)";
stdenv.mkDerivation {
  pname = "finn_rutis";
  inherit src version;
  nativeBuildInputs = [
    typstWithPackages
    poppler-utils
    ghostscript
  ];

  postConfigure = ''
    ln -s ${font-awesome}/share/fonts/opentype/* src/fonts/
    ln -s ${texlivePackages.ebgaramond.tex}/fonts/opentype/public/ebgaramond/* src/fonts/
    ln -s ${roboto}/share/fonts/truetype/* src/fonts/
    ln -s ${source-sans-pro}/share/fonts/truetype/* src/fonts/
  ''
  + lib.optionalString (extraFonts != null) ''
    find ${extraFonts} -name '*.otf' -exec ln -s {} src/fonts/ \;
  '';
  TYPST_FONT_PATHS = "src/fonts";

  configurePhase = ''
    runHook preConfigure


    runHook postConfigure
  '';

  buildPhase = ''
    runHook preBuild

    typst compile --root . --input commit="${commit}" --input version="${version}" --input submission-date="${submissionDate}" --input no_footer=true resumes/cv.typ cv.pdf
    typst compile --root . --input submission-date="${submissionDate}" resumes/portrait-page.typ portrait-page.pdf
    gs -q -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
      -dFIXEDMEDIA -dDEVICEWIDTHPOINTS=576 -dDEVICEHEIGHTPOINTS=720 \
      -sOutputFile=cv_cropped.pdf \
      -c "<< /PageOffset [-18 -52] >> setpagedevice" \
      -f cv.pdf
    pdfunite cv_cropped.pdf portrait-page.pdf "FINN RUTIS.pdf"

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out
    mv "FINN RUTIS.pdf" "$out/FINN RUTIS.pdf"

    runHook postInstall
  '';

  # A supplied font directory that Typst silently ignored would ship EB Garamond.
  postInstall = lib.optionalString (extraFonts != null) ''
    grep -aq SabonNextLTPro "$out/FINN RUTIS.pdf" || { echo "Sabon Next not embedded" >&2; exit 1; }
  '';

  meta = {
    license = lib.licenses.gpl3Only;
  };
}
