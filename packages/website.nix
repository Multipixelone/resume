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

    hugo

    runHook postBuild
  '';

  installPhase = "cp -r public $out";
}
