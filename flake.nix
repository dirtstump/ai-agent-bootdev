{
  description = "A very basic flake (python environment for boot.dev)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    devShell.x86_64-linux = let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in pkgs.mkShell {
      packages = with pkgs; [ (python313.withPackages (p: with p; [
        google-genai
        python-dotenv
      ])) ];
    };
  };
}
