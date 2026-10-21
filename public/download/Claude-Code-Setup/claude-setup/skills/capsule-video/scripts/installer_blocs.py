"""Installe le plugin « blocs » (code qui s'écrit, terminal, compile, badge de voix) dans une capsule.

Usage :
    python installer_blocs.py <dossier_capsule>

- copie assets/plugins-canvas/ (blocs.js, polices JetBrains Mono) dans <capsule>/plugins-canvas/ ;
- ajoute en tête de spec.js la ligne de chargement (idempotent) : le moteur n'est PAS modifié ;
- n'écrase jamais le spec.js : seule la ligne de chargement est insérée.

Le dossier plugins-canvas/ de la capsule se met à jour en relançant ce script
(maj_moteur.py ne le touche pas).
"""
import pathlib
import shutil
import sys

ICI = pathlib.Path(__file__).resolve().parent
ASSETS = ICI.parent / "assets" / "plugins-canvas"
MARQUE = "Plugin blocs (code, terminal, compile)"


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
    # le plugin « trois » (three.js, 670 ko) a son propre installeur : installer_trois.py
    shutil.copytree(ASSETS, cible, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("three.min.js", "THREE-LICENSE", "trois.js", "chargeur-trois.txt"))
    (cible / "chargeur-spec.txt").unlink(missing_ok=True)
    texte = spec.read_text(encoding="utf-8")
    if MARQUE in texte:
        print(f"Plugin à jour dans {cible} (ligne de chargement déjà présente dans spec.js)")
        return
    chargeur = (ASSETS / "chargeur-spec.txt").read_text(encoding="utf-8")
    spec.write_text(chargeur + texte, encoding="utf-8")
    print(f"Plugin installé : {cible} ; ligne de chargement ajoutée en tête de {spec}")


if __name__ == "__main__":
    main()
