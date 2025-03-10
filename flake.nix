{
  description = "Django environment for residence-ivoir project";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            python312
            python312Packages.django
            python312Packages.pillow
            python312Packages.flake8
          ];

          shellHook = ''
             echo "Thanks y'all";
          '';
        };
      });
}
