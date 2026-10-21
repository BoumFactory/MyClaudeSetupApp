"""Met à jour le moteur canvas de capsules existantes : remplace <capsule>/moteur-canvas/ par assets/moteur-canvas/.

Usage :
    python maj_moteur.py <capsule> [<capsule> ...]

Refuse un dossier sans spec.js (ancienne capsule HTML ou dossier quelconque). Les fichiers de la
capsule (spec.js, index.html, data/, audio) ne sont pas touchés. Si la capsule avait modifié sa copie
du moteur, vérifier d'abord par diff : ces modifications sont écrasées.
"""
import pathlib
import shutil
import sys

MOTEUR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "moteur-canvas"


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    erreurs = 0
    for arg in sys.argv[1:]:
        d = pathlib.Path(arg)
        if not (d / "spec.js").is_file():
            print(f"REFUSÉ  {d} : pas de spec.js (pas une capsule canvas)")
            erreurs += 1
            continue
        cible = d / "moteur-canvas"
        if cible.exists():
            shutil.rmtree(cible)
        shutil.copytree(MOTEUR, cible)
        print(f"OK      {d} : moteur-canvas/ mis à jour")
    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()
