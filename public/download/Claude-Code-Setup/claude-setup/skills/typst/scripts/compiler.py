"""Compile un document Typst avec le module pip `typst` et affiche des erreurs LISIBLES.

Pourquoi ce script : `str(erreur)` du module pip ne donne que le message (« expected content, found
array »), sans fichier, ligne ni indice. Ce script affiche le diagnostic complet (fichier:ligne:colonne,
extrait souligné, indices `hint:`) et les avertissements, comme la CLI `typst`.

Usage, avec le Python qui a le module `typst` (`pip install typst`) :
    python "<skill>/scripts/compiler.py" doc.typ
    ... doc.typ -o sortie.pdf --input correction=false
    ... doc.typ --png <dossier> [--ppi 110]        # une image PNG par page (page-01.png…) en plus du PDF
    ... doc.typ --police <dossier> --racine <dossier>
    ... doc.typ --sans-polices-bfcours              # ne pas ajouter les polices de la suite farfadet

Polices : le dossier des polices de la suite farfadet est ajouté par défaut quand il est trouvé
(variable d'environnement `BFCOURS_TYPST_POLICES`, sinon `localiser.py` du skill `bfcours-typst` installé
à côté de celui-ci). Recommandé pour le rendu Erewhon des paquets ; facultatif : sans lui, Typst utilise ses
polices intégrées et les maths ont la bonne taille ; sans effet sur un document qui n'utilise pas ces polices.
Racine (`--racine`, défaut : le dossier du fichier) : Typst refuse tout fichier lu (image, `read`,
`import` relatif) situé hors de la racine (« would escape the project root »).
Code de sortie : 0 si la compilation réussit, 1 sinon.
"""
import argparse
import os
import sys
from pathlib import Path

import typst


def _polices_farfadet():
    """Dossier des polices de la suite farfadet, ou un chemin inexistant s'il n'est pas trouvé."""
    env = os.environ.get("BFCOURS_TYPST_POLICES")
    if env:
        return Path(env)
    voisin = Path(__file__).resolve().parents[2] / "bfcours-typst" / "scripts"
    if (voisin / "localiser.py").exists():
        sys.path.insert(0, str(voisin))
        try:
            import localiser  # skill bfcours-typst installé à côté
            trouve = localiser.polices()
            if trouve:
                return Path(trouve)
        except Exception:
            pass
    return Path(__file__).resolve().parent / "_aucune_police"


POLICES_BFCOURS = _polices_farfadet()


def _diagnostic(x):
    """Texte complet d'une erreur ou d'un avertissement Typst."""
    d = getattr(x, "diagnostic", None)
    if d:
        return d.replace("\\\\?\\", "")
    return str(x)


def _dossiers_interdits():
    """Dossiers où aucune sortie ne doit atterrir directement : racines de disque, dossier personnel,
    Documents, Bureau, Téléchargements (un chemin raccourci tapé à la main, « C:/Users/NOMCOU~1/x.pdf »,
    y déposait des fichiers d'essai)."""
    maison = Path.home().resolve()
    interdits = {maison, maison / "Documents", maison / "Desktop", maison / "Downloads", maison.parent}
    interdits |= {Path(f"{l}:/").resolve() for l in "CDEFG" if Path(f"{l}:/").exists()}
    return interdits


def _verifier_destination(chemin, quoi):
    chemin = Path(chemin).resolve()
    parent = chemin if quoi == "dossier PNG" else chemin.parent
    interdits = _dossiers_interdits()
    if parent in interdits or (not parent.exists() and parent.parent in interdits):
        sys.exit(f"Refusé : la {quoi} « {chemin} » atterrirait directement dans « {parent} ».\n"
                 "Écrire les essais dans un dossier temporaire de session (chemin complet) ou dans le "
                 "dossier du document ; jamais de chemin raccourci (C:/NOMCOU~1/…).")


def compiler(source, sortie=None, entrees=None, polices=(), racine=None, png=None, ppi=110, bfcours=True):
    source = Path(source).resolve()
    sortie = Path(sortie).resolve() if sortie else source.with_suffix(".pdf")
    _verifier_destination(sortie, "sortie PDF")
    if png:
        _verifier_destination(png, "dossier PNG")
    fp = [str(Path(p).resolve()) for p in polices]
    if bfcours and POLICES_BFCOURS.exists():
        fp.insert(0, str(POLICES_BFCOURS))
    racine = str(Path(racine).resolve()) if racine else str(source.parent)
    options = dict(root=racine, font_paths=fp, sys_inputs=entrees or {})
    sortie.parent.mkdir(parents=True, exist_ok=True)
    _, avertissements = typst.compile_with_warnings(str(source), output=str(sortie), **options)
    if png:
        dossier = Path(png)
        dossier.mkdir(parents=True, exist_ok=True)
        for ancien in dossier.glob("page-*.png"):
            ancien.unlink()
        typst.compile(str(source), output=str(dossier / "page-{0p}.png"), format="png", ppi=ppi, **options)
    return sortie, avertissements


def main():
    p = argparse.ArgumentParser(description="Compile un .typ et affiche les erreurs avec leur position.")
    p.add_argument("source")
    p.add_argument("-o", "--sortie")
    p.add_argument("--input", action="append", default=[], help="clé=valeur, lu par sys.inputs (chaîne)")
    p.add_argument("--police", action="append", default=[], help="dossier de polices supplémentaire")
    p.add_argument("--racine", help="racine du projet Typst (défaut : dossier du fichier)")
    p.add_argument("--png", help="dossier : une image PNG par page, en plus du PDF")
    p.add_argument("--ppi", type=float, default=110)
    p.add_argument("--sans-polices-bfcours", action="store_true")
    a = p.parse_args()
    entrees = dict(x.split("=", 1) for x in a.input)
    try:
        sortie, avert = compiler(a.source, a.sortie, entrees, a.police, a.racine, a.png, a.ppi,
                                 bfcours=not a.sans_polices_bfcours)
    except typst.TypstError as e:
        print("ÉCHEC de la compilation\n")
        print(_diagnostic(e))
        for t in getattr(e, "trace", []) or []:
            print("  trace :", t)
        sys.exit(1)
    for w in avert:
        print("avertissement :", _diagnostic(w))
    print(f"PDF : {sortie}")
    if a.png:
        print(f"PNG : {Path(a.png).resolve()}")


if __name__ == "__main__":
    main()
