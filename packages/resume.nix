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
  # Create typst with the fontawesome package pre-installed
  typstWithPackages = typst.withPackages (ps: [ typstPackages.fontawesome ]);
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

    typst compile --input commit="${commit}" --input version="${version}" cv.typ
    typst compile --input commit="${commit}" --input version="${version}" --format png cv.typ
    typst compile --input commit="${commit}" --input version="${version}" rep-sheet.typ
    typst compile --input commit="${commit}" --input version="${version}" tech.typ
    typst compile --input commit="${commit}" --input version="${version}" work.typ
    typst compile --input commit="${commit}" --input version="${version}" --format png work.typ
    typst compile --input commit="${commit}" --input version="${version}" nanny.typ
    typst compile --input commit="${commit}" --input version="${version}" --format png nanny.typ
    typst compile --input commit="${commit}" --input version="${version}" cover-letter.typ

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out
    mv cv.pdf $out/CV_FinnRutis_${version}.pdf
    mv cv.png $out/CV_FinnRutis_${version}.png
    mv rep-sheet.pdf $out/Rep-Sheet_FinnRutis_${version}.pdf
    mv tech.pdf $out/Tech_CV_FinnRutis_${version}.pdf
    mv work.pdf $out/Work_CV_FinnRutis_${version}.pdf
    mv work.png $out/Work_CV_FinnRutis_${version}.png
    mv nanny.pdf $out/Nanny_CV_FinnRutis_${version}.pdf
    mv nanny.png $out/Nanny_CV_FinnRutis_${version}.png
    mv cover-letter.pdf $out/Cover_Letter_FinnRutis_${version}.pdf

    runHook postInstall
  '';
}
