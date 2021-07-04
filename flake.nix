{
  description = "A tool to convert voice notes to an Org file.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    utils.url = "github:numtide/flake-utils";
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
            version = "1.0.0";
            src = ./.;
            propagatedBuildInputs = with pkgs.python3.pkgs ; [
              requests
              jsonpickle
              tqdm
            ];
          };

          pythonEnvironment = pkgs.python3.withPackages (ps: with ps; [
            org-voice-notes
            ipython
            requests
            jsonpickle
            tqdm
          ]);

          developmentEnvironment = pkgs.mkShell {
            buildInputs = [
              packages.pythonEnvironment
              packages.org-voice-notes
              pkgs.pre-commit
            ];
          };
        };

        defaultPackage = packages.org-voice-notes;
        devShell = packages.developmentEnvironment;
      }
    );

}
