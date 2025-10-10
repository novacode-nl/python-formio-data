{
  pkgs ? import ./nix/pkgs.nix
}:

pkgs.mkShell {
  name = "pyhon-formio-data";
  buildInputs = with pkgs; [
      python314
      poetry
  ];
}
