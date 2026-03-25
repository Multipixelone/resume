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
          versionFile = "${self}/VERSION";
          versionString = builtins.replaceStrings [ "\n" ] [ "" ] (builtins.readFile versionFile);
          commit = "v${versionString} ${self.shortRev or "dirty"}";
          mkDate =
            longDate:
            with builtins;
            (concatStringsSep "-" [
              (substring 0 4 longDate)
              (substring 4 2 longDate)
              (substring 6 2 longDate)
            ]);
          version = mkDate (self.lastModifiedDate or "19700101");
          src = self;
          websiteRoot = ./website;

          tinymistWrapped =
            let
              fakeXdg = pkgs.writeShellScriptBin "xdg-open" ''
                nohup chromium --app="$@" --hide-scrollbars --no-default-browser-check >/dev/null 2>&1 &
                exit 0
              '';
            in
            pkgs.writeShellApplication {
              name = "tinymist";
              runtimeInputs = [
                pkgs.tinymist
                fakeXdg
              ];
              text = ''
                exec tinymist "$@"
              '';
            };

          resume = pkgs.callPackage ./packages/resume.nix {
            inherit
              inputs
              version
              src
              commit
              ;
          };
          workResume = pkgs.callPackage ./packages/work-resume.nix {
            inherit
              inputs
              version
              src
              commit
              ;
          };
          techResume = pkgs.callPackage ./packages/tech-resume.nix {
            inherit
              inputs
              version
              src
              commit
              ;
          };
          coverLetter = pkgs.callPackage ./packages/cover-letter.nix {
            inherit
              inputs
              version
              src
              commit
              ;
          };
          finnRutis = pkgs.callPackage ./packages/finn-rutis.nix {
            inherit
              inputs
              version
              src
              commit
              ;
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
              tinymistWrapped
              pkgs.nodejs
              pkgs.git-cliff
              pkgs.just
              pkgs.gh
            ];
          };

          packages = {
            default = resume;
            resume = resume;
            work-resume = workResume;
            tech-resume = techResume;
            cover-letter = coverLetter;
            finn-rutis = finnRutis;
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
