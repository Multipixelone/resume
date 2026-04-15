{
  description = "Finn Rutis Resume";
  outputs =
    {
      self,
      nixpkgs,
      ...
    }@inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "x86_64-darwin"
      ];
      perSystem =
        {
          pkgs,
          ...
        }:
        let
          forceLocalBuild =
            pkg:
            pkg.overrideAttrs (_: {
              allowSubstitutes = false;
              preferLocalBuild = true;
            });

          versionFile = "${self}/VERSION";
          versionString = builtins.replaceStrings [ "\n" ] [ "" ] (builtins.readFile versionFile);
          commit = "v${versionString} (commit ${self.shortRev or "dirty"})";
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
          checks = import ./packages/checks.nix {
            inherit (pkgs) lib;
            inherit pkgs src resume;
          };
        in
        {
          devShells.default = pkgs.mkShell {
            packages = [
              pkgs.typst
              pkgs.typstyle
              tinymistWrapped
              pkgs.nodejs
              pkgs.git-cliff
              pkgs.just
            ];
          };

          packages = {
            default = forceLocalBuild resume;
            resume = forceLocalBuild resume;
            finn-rutis = forceLocalBuild finnRutis;
            website = forceLocalBuild website;
          };

          checks = {
            inherit (checks)
              typstyle
              toml-validity
              metadata-completeness
              output-files
              pdf-page-count
              no-unchecked-outputs
              ;
          };
        };
    };

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

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
