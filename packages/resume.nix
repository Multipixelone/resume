{
  lib,
  stdenv,
  typst,
  typstPackages,
  font-awesome,
  roboto,
  source-sans-pro,
  eb-garamond,
  inputs,
  version ? "",
  commit ? "unknown",
  submissionDate ? lib.removeSuffix "\n" (builtins.readFile ../metadata/submission-date.txt),
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
  variants = builtins.fromTOML (builtins.readFile ../variants.toml);

  typstFlags = ''--root . --ignore-system-fonts --input commit="${commit}" --input version="${version}" --input submission-date="${submissionDate}"'';

  compileVariant = _: v: ''
    typst compile ${typstFlags} resumes/${v.source}.typ
    typst compile ${typstFlags} --format png resumes/${v.source}.typ resumes/${v.source}-{p}.png
  '';

  installVariant = _: v: ''
    mv resumes/${v.source}.pdf $out/${v.dest}.pdf
    mv resumes/${v.source}-1.png $out/${v.dest}.png
  '';
in
assert lib.assertMsg validSubmissionDate "submissionDate must be a real ISO calendar date (YYYY-MM-DD)";
stdenv.mkDerivation {
  pname = "finn_cv";
  inherit src version;
  nativeBuildInputs = [ typstWithPackages ];

  postConfigure = ''
    ln -s ${font-awesome}/share/fonts/opentype/* src/fonts/
    ln -s ${eb-garamond}/share/fonts/opentype/* src/fonts/
    ln -s ${roboto}/share/fonts/truetype/* src/fonts/
    ln -s ${source-sans-pro}/share/fonts/truetype/* src/fonts/
  '';
  TYPST_FONT_PATHS = "src/fonts";

  configurePhase = ''
    runHook preConfigure
    runHook postConfigure
  '';

  buildPhase = ''
    runHook preBuild
    ${lib.concatStringsSep "\n" (lib.mapAttrsToList compileVariant variants)}
    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall
    mkdir -p $out
    ${lib.concatStringsSep "\n" (lib.mapAttrsToList installVariant variants)}
    runHook postInstall
  '';

  meta = {
    license = lib.licenses.gpl3Only;
  };
}
