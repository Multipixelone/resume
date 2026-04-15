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
  src ? null,
}:
let
  typstWithPackages = typst.withPackages (ps: [ typstPackages.fontawesome ]);
  variants = builtins.fromTOML (builtins.readFile ../variants.toml);

  typstFlags = ''--root . --input commit="${commit}" --input version="${version}"'';

  compileVariant = _: v: ''
    typst compile ${typstFlags} resumes/${v.source}.typ
    typst compile ${typstFlags} --format png resumes/${v.source}.typ resumes/${v.source}-{p}.png
  '';

  installVariant = _: v: ''
    mv resumes/${v.source}.pdf $out/${v.dest}.pdf
    mv resumes/${v.source}-1.png $out/${v.dest}.png
  '';
in
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
}
