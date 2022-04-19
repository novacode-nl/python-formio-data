{
  pkgs ? import ./nix/pkgs.nix
}:

pkgs.mkShell {
  name = "xml-jats-converter-shell";
  buildInputs = with pkgs; [
      python38
      poetry
  ];
}
