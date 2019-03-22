{ python36Packages, fetchFromGitHub, uwsgi }:

let
  connexionPrPackages = import (builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/5509a5c.tar.gz";
    sha256 = "0wjqn4xn4hrgslvr952i8d8allnxpgiadvh0a0j4vg2ijzrxy249";
  }) {};

  connexionPrPackagesPatched =
    connexionPrPackages // {
      python36Packages = connexionPrPackages.python36Packages // {
        connexion = connexionPrPackages.python36Packages.connexion.overridePythonAttrs (oldAttrs: {
          src = fetchFromGitHub {
            owner = "zalando";
            repo = oldAttrs.pname;
            rev = oldAttrs.version;
            sha256 = "0kqqdhi57z04dqwrx426s5zrqllic2jqfjp3h3wrpxyhl9j0vppz";
          };
          doCheck = false;
        });
      };
    };

in
  python36Packages.buildPythonApplication {
    name = "alex-commute-skill";
    version = "0.1.0";

    src = ./.;

    propagatedBuildInputs =
      (with connexionPrPackagesPatched.python36Packages; [
        connexion
        pytest
        flask-cors
        gunicorn
      ]);
  }
