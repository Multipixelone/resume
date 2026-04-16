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

  npmDepsHash = "sha256-oCYjQ1Vj/bZ5IDmiroo4ccPyBG0ylUF3wu+71wBTRkM=";
}
