{
  lib,
  stdenv,
  typst,
  font-awesome,
  roboto,
  source-sans-pro,
  eb-garamond,
  inputs,
  version ? "",
  src ? null,
}:
stdenv.mkDerivation {
  pname = "finn_cv";
  inherit src version;
  nativeBuildInputs = [typst];

  postConfigure = ''
    mkdir src/fonts
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

    typst compile cv.typ

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out
    # cp cv.typ $out/cv_edited.typ
    mv *.pdf $out
    mv $out/cv.pdf $out/CV_FinnRutis.pdf

    runHook postInstall
  '';
}
