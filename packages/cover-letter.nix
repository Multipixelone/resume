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
in
stdenv.mkDerivation {
  pname = "finn_cover_letter";
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

    typst compile --input commit="${commit}" --input version="${version}" cover-letter.typ

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out
    mv cover-letter.pdf $out/Cover_Letter_FinnRutis_${version}.pdf

    runHook postInstall
  '';
}
