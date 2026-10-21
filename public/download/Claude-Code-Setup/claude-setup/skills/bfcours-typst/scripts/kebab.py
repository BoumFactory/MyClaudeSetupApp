"""Passage des noms LaTeX / anciens noms Typst aux noms publics actuels (kebab-case) de la suite bfcours-typst.

Depuis le 16/10/2026, les fonctions de la suite portent des noms en kebab-case : `Definition` → `definition`,
`EXO` → `exo`, `MultiColonnes` → `multi-colonnes`, `Vecteur` (maths) → `vect`… Les NOMS LaTeX ne changent pas
(`\\begin{Definition}`, `\\EXO`) : le convertisseur les traduit vers les nouveaux noms Typst grâce à ce module.

La table (`donnees/kebab.json`) est une copie de `outils/kebab/table-finale.json` de la suite ; le skill
fonctionne donc sans la suite. Pour la rafraîchir : `python scripts/kebab.py --maj [chemin/table-finale.json]`.

Usage en ligne de commande :
    python scripts/kebab.py MultiColonnes tcbtab Vecteur     # ancien nom → nom actuel
    python scripts/kebab.py --inverse multi-colonnes         # nom actuel → ancien(s) nom(s)
    python scripts/kebab.py --maj                            # relit la table de la suite
"""
from __future__ import annotations

import json
import sys
from functools import lru_cache
from pathlib import Path

ICI = Path(__file__).resolve().parent
FICHIER = ICI / "donnees" / "kebab.json"


@lru_cache(maxsize=None)
def _table() -> dict:
    if not FICHIER.is_file():
        return {"global": {}, "par_paquet": {}, "cles": {}, "maths": []}
    return json.loads(FICHIER.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _nouveaux() -> frozenset:
    t = _table()
    noms = set(t["global"].values())
    for d in t["par_paquet"].values():
        noms.update(d.values())
    return frozenset(noms)


def nom_typst(nom: str, paquet: str | None = None) -> str:
    """Nom actuel de la fonction Typst qui portait l'ancien nom `nom` (inchangé s'il n'a pas été renommé).

    `paquet` départage les homonymes (`vecteur` de farfadet-geom → `fleche`, `exemple` de bfdoc → `exemple-bfdoc`)
    et n'est utile que pour lire l'index ; sans lui, seuls les renommages sans ambiguïté s'appliquent."""
    t = _table()
    if paquet and nom in t["par_paquet"].get(paquet, {}):
        return t["par_paquet"][paquet][nom]
    return t["global"].get(nom, nom)


def est_ancien(nom: str) -> bool:
    """`nom` est-il un ancien nom (renommé sans ambiguïté) ?"""
    return nom in _table()["global"]


def est_nouveau(nom: str) -> bool:
    """`nom` est-il un nom produit par le renommage (donc pas un nom LaTeX à chercher tel quel) ?"""
    return nom in _nouveaux()


def anciens(nom: str) -> list[str]:
    """Ancien(s) nom(s) d'une fonction actuelle (pour la recherche par habitude)."""
    t = _table()
    sortie = [a for a, n in t["global"].items() if n == nom]
    for d in t["par_paquet"].values():
        sortie += [a for a, n in d.items() if n == nom]
    return sortie


def cle_rdtime(cle: str) -> str:
    return _table()["cles"].get(cle, cle)


def normaliser_index(data: dict) -> dict:
    """Met à niveau, en place, un index des fonctions produit AVANT le passage au kebab-case (idempotent)."""
    for r in data.get("fonctions", []):
        paquet = r.get("paquet")
        for champ in ("nom", "appel"):
            v = r.get(champ)
            if not v:
                continue
            tete, point, queue = v.rpartition(".")
            r[champ] = tete + point + nom_typst(queue, paquet)
        sig = r.get("signature")
        if sig and r.get("nom"):
            nouveau = r["nom"]
            ancien_nom_ = nouveau
            for a in anciens(nouveau):
                if sig.lstrip("#").startswith(a + "("):
                    ancien_nom_ = a
            if ancien_nom_ != nouveau:
                r["signature"] = sig.replace(ancien_nom_, nouveau, 1)
    for p in list(data.get("paquets", {})):
        d = data["paquets"][p]
        if isinstance(d.get("noms_facade"), list):
            d["noms_facade"] = [nom_typst(n, p) for n in d["noms_facade"]]
    return data


def maj(source: Path | None = None) -> None:
    if source is None:
        racine = ICI.parent
        import localiser  # noqa: WPS433
        s = localiser.suite()
        source = (s / "outils" / "kebab" / "table-finale.json") if s else None
    if not source or not Path(source).is_file():
        raise SystemExit("table-finale.json introuvable : donner son chemin en argument.")
    d = json.loads(Path(source).read_text(encoding="utf-8"))
    glob, par_paquet, maths = {}, {}, []
    for e in d["entrees"]:
        if e.get("portee"):
            # la table du 16/10/2026 nomme encore les paquets `bfcours-*` ; ils s'appellent `farfadet-*` depuis le 21/10/2026
            paquet = e["paquet"]
            paquet = "farfadet-" + paquet[len("bfcours-"):] if paquet.startswith("bfcours-") else paquet
            par_paquet.setdefault(paquet, {})[e["ancien"]] = e["nouveau"]
        else:
            glob[e["ancien"]] = e["nouveau"]
        if e.get("maths"):
            maths.append(e["ancien"])
    FICHIER.write_text(json.dumps(
        {"source": "outils/kebab/table-finale.json de la suite farfadet (16/10/2026)",
         "global": glob, "par_paquet": par_paquet, "cles": d.get("cles", {}), "maths": maths},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(glob)} renommages globaux, {sum(len(v) for v in par_paquet.values())} par paquet → {FICHIER}")


def main(argv: list[str]) -> int:
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8")
    if argv and argv[0] == "--maj":
        maj(Path(argv[1]) if len(argv) > 1 else None)
        return 0
    if argv and argv[0] == "--inverse":
        for n in argv[1:]:
            print(n, "←", ", ".join(anciens(n)) or "(pas de renommage)")
        return 0
    for n in argv:
        print(n, "→", nom_typst(n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
