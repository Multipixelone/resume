{
  lib,
  stdenv,
  typst,
  typstPackages,
  font-awesome,
  roboto,
  source-sans-pro,
  eb-garamond,
  poppler-utils,
  ghostscript,
  inputs,
  version ? "",
  commit ? "unknown",
  src ? null,
}:
let
  typstWithPackages = typst.withPackages (ps: [ typstPackages.fontawesome ]);
in
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

    typst compile --input commit="${commit}" --input version="${version}" --input no_footer=true resumes/cv.typ cv.pdf
    typst compile resumes/portrait-page.typ portrait-page.pdf
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
}
