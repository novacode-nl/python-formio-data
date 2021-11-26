{
  pkgs ? import ./nix/pkgs.nix
}:

let pythonWithPackages = pkgs.python38.buildEnv.override {
    extraLibs = with pkgs.python38Packages; [
	requests
    ];
};
in

pkgs.mkShell {
  name = "xml-jats-converter-shell";
  buildInputs = with pkgs; [
    pythonWithPackages
  ];
}
