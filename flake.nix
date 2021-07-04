{
  description = "A tool to convert voice notes to an Org file.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    utils.url = "github.numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      rec {
        packages = rec {
          org-voice-notes = pkgs.python3.pkgs.buildPythonPackage {
            pname = "org_voice_notes";
            version = "0.0.1";
            src = ./.;
            propagatedBuildInputs = with pkgs.python3.pkgs ; [
              requests
              jsonpickle
              tqdm
            ];
          };

          pythonEnvironment = pkgs.python3.withPackages (ps: with ps; [
            requests
            jsonpickle
            tqdm
          ]);

          developmentEnvironment = pkgs.mkShell {
            buildInputs = [
              packages.pythonEnvironment
              pkgs.pre-commit
            ];
          };
        };

        defaultPackage = packages.org-voice-notes;
        devShell = packages.developmentEnvironment;
      }
    );

}
