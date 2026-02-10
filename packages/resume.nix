{
  lib,
  stdenv,
  typst,
  typstPackages,
  font-awesome,
  roboto,
  source-sans-pro,
  eb-garamond,
  ibm-plex,
  inputs,
  version ? "",
  commit ? "unknown",
  src ? null,
}:
let
  # Create typst with the fontawesome package pre-installed
  typstWithPackages = typst.withPackages (ps: [ typstPackages.fontawesome ]);
in
stdenv.mkDerivation {
  pname = "finn_cv";
  inherit src version;
  nativeBuildInputs = [ typstWithPackages ];

  postConfigure = ''
    mkdir src/fonts
    ln -s ${font-awesome}/share/fonts/opentype/* src/fonts/
    ln -s ${eb-garamond}/share/fonts/opentype/* src/fonts/
    ln -s ${roboto}/share/fonts/truetype/* src/fonts/
    ln -s ${source-sans-pro}/share/fonts/truetype/* src/fonts/
    ln -s ${ibm-plex}/share/fonts/opentype/* src/fonts/
  '';
  TYPST_FONT_PATHS = "src/fonts";

  configurePhase = ''
    runHook preConfigure


    runHook postConfigure
  '';

  buildPhase = ''
    runHook preBuild

    typst compile --input commit="${commit}" --input version="${version}" cv.typ
    typst compile --input commit="${commit}" --input version="${version}" --format png cv.typ
    typst compile --input commit="${commit}" --input version="${version}" rep-sheet.typ

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out
    # cp cv.typ $out/cv_edited.typ
    mv *.pdf $out
    mv cv.png $out/CV_FinnRutis_${version}.png
    mv $out/cv.pdf $out/CV_FinnRutis_${version}.pdf
    mv $out/rep-sheet.pdf $out/Rep-Sheet_FinnRutis_${version}.pdf

    runHook postInstall
  '';
}
