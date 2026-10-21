"""Installe le plugin « trois » (scènes 3D three.js) dans une capsule.

Usage :
    python installer_trois.py <dossier_capsule>

- copie three.min.js (r159, MIT), THREE-LICENSE et trois.js de assets/plugins-canvas/ dans
  <capsule>/plugins-canvas/ (sans toucher aux fichiers du plugin « blocs » déjà présents) ;
- ajoute en tête de spec.js la ligne de chargement de chargeur-trois.txt (idempotent) :
  le moteur n'est PAS modifié ; la ligne charge three.js et trois.js dans la page, l'aperçu
  ET les workers de rendu ;
- n'écrase jamais le spec.js : seule la ligne de chargement est insérée.

Peut se combiner avec installer_blocs.py (deux lignes de chargement indépendantes).
Relancer ce script après une évolution de assets/plugins-canvas/ (maj_moteur.py n'y touche pas).
"""
import pathlib
import shutil
import sys

ICI = pathlib.Path(__file__).resolve().parent
ASSETS = ICI.parent / "assets" / "plugins-canvas"
MARQUE = "Plugin trois (three.js"
FICHIERS = ["three.min.js", "THREE-LICENSE", "trois.js"]


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d = pathlib.Path(sys.argv[1])
    spec = d / "spec.js"
    if not spec.exists():
        sys.exit(f"spec.js introuvable dans {d} (créer la capsule avec nouvelle_capsule.py d'abord)")
    cible = d / "plugins-canvas"
    cible.mkdir(exist_ok=True)
    for f in FICHIERS:
        shutil.copy2(ASSETS / f, cible / f)
    texte = spec.read_text(encoding="utf-8")
    if MARQUE in texte:
        print(f"Plugin à jour dans {cible} (ligne de chargement déjà présente dans spec.js)")
        return
    chargeur = (ASSETS / "chargeur-trois.txt").read_text(encoding="utf-8")
    spec.write_text(chargeur + texte, encoding="utf-8")
    print(f"Plugin installé : {cible} ; ligne de chargement ajoutée en tête de {spec}")


if __name__ == "__main__":
    main()
