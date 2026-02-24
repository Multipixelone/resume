{
  description = "Finn Rutis Resume";
  outputs =
    {
      self,
      nixpkgs,
      devenv,
      ...
    }@inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "x86_64-darwin"
      ];
      imports = [
        inputs.devenv.flakeModule
      ];
      perSystem =
        {
          pkgs,
          config,
          ...
        }:
        let
          mkDate =
            longDate:
            with builtins;
            (concatStringsSep "-" [
              (substring 0 4 longDate)
              (substring 4 2 longDate)
              (substring 6 2 longDate)
            ]);
          version = mkDate (self.lastModifiedDate or "19700101");
          commit = self.shortRev or "dirty";
          src = self;
          websiteRoot = ./website;

          resume = pkgs.callPackage ./packages/resume.nix {
            inherit inputs version src commit;
          };
          workResume = pkgs.callPackage ./packages/work-resume.nix {
            inherit inputs version src commit;
          };
          website = pkgs.callPackage ./packages/website.nix {
            inherit inputs version websiteRoot;
          };
        in
        {
          devenv.shells.default = {
            packages = [
              pkgs.typst
              pkgs.typstyle
              pkgs.tinymist
              pkgs.nodejs
            ];
          };

          packages = {
            default = resume;
            resume = resume;
            work-resume = workResume;
            website = website;
          };
        };
    };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    devenv.url = "github:cachix/devenv";

    # resume-theme = {
    #   url = "github:eddiewebb/hugo-resume";
    #   flake = false;
    # };
    resume-theme = {
      url = "github:mansoorbarri/coming-soon";
      flake = false;
    };

    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };
}
