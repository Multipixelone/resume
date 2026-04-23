{
  inputs,
  stdenv,
  hugo,
  buildNpmPackage,
  pkg-config,
  version ? "",
  websiteRoot ? null,
  nodejs,
}:
buildNpmPackage {
  pname = "finnrut.is";
  inherit version nodejs;

  src = websiteRoot;

  nativeBuildInputs = [
    pkg-config
  ];

  # buildPhase = ''
  #   runHook preBuild
  #   mkdir -p themes/hugo-resume
  #   cp -r ${inputs.resume-theme}/* themes/hugo-resume/

  #   hugo

  #   runHook postBuild
  # '';

  installPhase = "cp -pr --reflink=auto dist $out";

  npmDepsHash = "sha256-/FB1Tw4iX87I4nnYXbKPx7v3mGia4hDfJ5VlJ8yxBuU=";
}
