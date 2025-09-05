{
  inputs,
  stdenv,
  hugo,
  version ? "",
  websiteRoot ? null,
}:
stdenv.mkDerivation {
  pname = "finnrut.is";
  inherit version;

  src = websiteRoot;

  nativeBuildInputs = [
    hugo
  ];

  buildPhase = ''
    runHook preBuild
    mkdir -p themes/hugo-resume
    cp -r ${inputs.resume-theme}/* themes/hugo-resume/

    hugo

    runHook postBuild
  '';

  installPhase = "cp -r public $out";
}
