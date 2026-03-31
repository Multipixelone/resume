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

    typst compile --root . --input commit="${commit}" --input version="${version}" resumes/cv.typ
    typst compile --root . --input commit="${commit}" --input version="${version}" --format png resumes/cv.typ
    typst compile --root . --input commit="${commit}" --input version="${version}" resumes/rep-sheet.typ
    typst compile --root . --input commit="${commit}" --input version="${version}" resumes/tech.typ
    typst compile --root . --input commit="${commit}" --input version="${version}" resumes/work.typ
    typst compile --root . --input commit="${commit}" --input version="${version}" --format png resumes/work.typ
    typst compile --root . --input commit="${commit}" --input version="${version}" resumes/nanny.typ
    typst compile --root . --input commit="${commit}" --input version="${version}" --format png resumes/nanny.typ
    typst compile --root . --input commit="${commit}" --input version="${version}" resumes/cover-letter.typ

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out
    mv resumes/cv.pdf $out/CV_FinnRutis_${version}.pdf
    mv resumes/cv.png $out/CV_FinnRutis_${version}.png
    mv resumes/rep-sheet.pdf $out/Rep-Sheet_FinnRutis_${version}.pdf
    mv resumes/tech.pdf $out/Tech_CV_FinnRutis_${version}.pdf
    mv resumes/work.pdf $out/Work_CV_FinnRutis_${version}.pdf
    mv resumes/work.png $out/Work_CV_FinnRutis_${version}.png
    mv resumes/nanny.pdf $out/Nanny_CV_FinnRutis_${version}.pdf
    mv resumes/nanny.png $out/Nanny_CV_FinnRutis_${version}.png
    mv resumes/cover-letter.pdf $out/Cover_Letter_FinnRutis_${version}.pdf

    runHook postInstall
  '';
}
