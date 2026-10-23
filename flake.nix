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
        "aarch64-darwin"
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
          # Archived snapshot date, independent of source/revision provenance.
          submissionDate = pkgs.lib.removeSuffix "\n" (builtins.readFile ./metadata/submission-date.txt);
          src = self;

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

          patchright = pkgs.python3Packages.callPackage (inputs.roomieorder.outPath + "/nix/patchright.nix") { };

          pythonEnv = pkgs.python3.withPackages (
            p:
            [
              p.playwright
              # website/scripts/gen_social_card.py draws the Open Graph card.
              p.pillow
              p.mypy
              p.pytest
              p.ruff
            ]
            ++ pkgs.lib.optional (!pkgs.stdenv.isDarwin) patchright
          );

          resume = pkgs.callPackage ./packages/resume.nix {
            inherit
              inputs
              version
              src
              commit
              submissionDate
              ;
          };
          finnRutis = pkgs.callPackage ./packages/finn-rutis.nix {
            inherit
              inputs
              version
              src
              commit
              submissionDate
              ;
          };
          website = pkgs.callPackage ./packages/website.nix {
            inherit version resume finnRutis;
            # Full rev for the footer's commit link; a dirty tree has only dirtyRev.
            commit = self.rev or self.dirtyRev or "";
          };
          businessCards = pkgs.callPackage ./packages/business-cards.nix { };
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
              pythonEnv
            ];

            shellHook = ''
              export PLAYWRIGHT_BROWSERS_PATH="${pkgs.playwright-driver.browsers}"
              export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS="true"
            '';
          };

          packages = {
            default = forceLocalBuild resume;
            resume = forceLocalBuild resume;
            finn-rutis = forceLocalBuild finnRutis;
            website = forceLocalBuild website;
            business-cards = businessCards;
          };

          apps.business-cards = {
            type = "app";
            program = "${businessCards}/bin/business-cards";
          };

          checks = {
            card-profiles = pkgs.runCommandLocal "check-card-profiles"
              { nativeBuildInputs = [ pkgs.python3 ]; }
              ''
                python3 ${./scripts/check_card_profiles.py} --root ${src}
                touch "$out"
              '';
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

    roomieorder = {
      url = "github:Multipixelone/roomieorder";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
}
