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
            python312Packages.django
            python312Packages.pillow
            python312Packages.flake8
            python312Packages.gunicorn
            python312Packages.dj-database-url
            python312Packages.whitenoise
            python312Packages.psycopg2-binary
            python312Packages.pip
            python312Packages.python-lsp-server
            nodejs_23
            nodePackages.prettier
            # heroku
            postgresql
          ];

          shellHook = ''
             echo "Thanks y'all"
             export DEBUG=True
             export DEV=True
          '';
        };
      });
}
