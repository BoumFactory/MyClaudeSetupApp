"""Ce que la suite farfadet sait faire, lu dans l'index des fonctions (jamais écrit à la main).

L'index (`index.json`) est produit à partir des paquets de la suite ; les clés documentées dans
les guides (`donnees/cles-guides.json`) le complètent pour les fonctions à arguments variadiques (`EXO`,
`tcbenumerate`, `setrdexo`…). Quand un paquet change, `regenerer.py` remet les deux à jour et le
convertisseur suit sans modification.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

import kebab
import localiser
from . import regles

DONNEES = Path(__file__).resolve().parent.parent / "donnees"


@dataclass
class Fonction:
    nom: str
    genre: str  # "fonction" | "valeur"
    paquet: str
    positionnels: List[Dict] = field(default_factory=list)  # [{nom, type}]
    cles: Set[str] = field(default_factory=set)
    latex_vers_cle: Dict[str, str] = field(default_factory=dict)  # option LaTeX → clé Typst
    variadique: bool = False
    noms_latex: List[str] = field(default_factory=list)

    def type_positionnel(self, rang: int) -> str:
        return (self.positionnels[rang].get("type") or "") if rang < len(self.positionnels) else ""


class Catalogue:
    def __init__(self):
        chemin = localiser.index_fonctions()
        if not chemin:
            raise SystemExit("Index des fonctions introuvable (ni dans la suite, ni dans le skill) : "
                             "lancer scripts/regenerer.py.")
        data = kebab.normaliser_index(json.loads(Path(chemin).read_text(encoding="utf-8")))  # noms kebab-case
        guides_f = DONNEES / "cles-guides.json"
        guides = json.loads(guides_f.read_text(encoding="utf-8")) if guides_f.exists() else {}
        guides = {kebab.nom_typst(k): v for k, v in guides.items()}
        self.fonctions: Dict[str, Fonction] = {}
        self.par_latex: Dict[str, str] = {}
        for r in data["fonctions"]:
            if r["paquet"] in ("farfadet-docs",):
                continue
            nom = r["appel"]
            f = self.fonctions.get(nom) or Fonction(nom, r.get("genre", "fonction"), r["paquet"])
            for p in r["parametres"]:
                if p.get("variadique"):
                    f.variadique = True
                    continue
                if p.get("positionnel"):
                    f.positionnels.append({"nom": p["nom"], "type": p.get("type") or ""})
                else:
                    f.cles.add(p["nom"])
                for lt in re.split(r"\s*,\s*", p.get("latex") or ""):
                    lt = lt.strip()
                    if lt and not lt.startswith("\\") and " de " not in lt and len(lt) < 40:
                        f.latex_vers_cle.setdefault(lt, p["nom"])
            g = guides.get(nom)
            if g:
                for p in g.get("params", []):
                    if not p.get("positionnel") and not p["nom"].startswith(".."):
                        for n in re.split(r",\s*", p["nom"]):
                            f.cles.add(n.strip())
            f.noms_latex = list(r.get("latex") or [])
            for lt in f.noms_latex:
                self.par_latex.setdefault(lt.rstrip("*"), nom)
            self.fonctions[nom] = f
        self.version = localiser.version_suite() or localiser.VERSION_PAR_DEFAUT

    # ------------------------------------------------------------------ noms
    def fonction(self, nom: str) -> Optional[Fonction]:
        """Fonction par son nom Typst actuel (kebab-case) ; un ancien nom (`McqQuest`) est traduit."""
        return self.fonctions.get(kebab.nom_typst(nom))

    def pour_latex(self, nom_latex: str):
        """(fonction Typst, clés imposées) pour une commande LaTeX, ou (None, {}).

        Le nom LaTeX ne change jamais (`Definition`, `EXO`) ; la fonction Typst a un nom kebab-case
        (`definition`, `exo`). Un nom LaTeX qui coïncide avec un nouveau nom Typst (`\\si` de siunitx,
        `\\dd`) n'est PAS une correspondance : seul l'index (champ `latex`) peut la déclarer."""
        if nom_latex in regles.RENOMMAGES:
            cible, cles = regles.RENOMMAGES[nom_latex]
            if cible in self.fonctions:
                return self.fonctions[cible], dict(cles)
        direct = kebab.nom_typst(nom_latex) if kebab.est_ancien(nom_latex) else (
            None if kebab.est_nouveau(nom_latex) else nom_latex)
        if direct in self.fonctions and self.fonctions[direct].genre in ("fonction", "valeur"):
            return self.fonctions[direct], {}
        cible = self.par_latex.get(nom_latex)
        if cible and cible in self.fonctions:
            return self.fonctions[cible], {}
        return None, {}

    # ------------------------------------------------------------------ clés
    def cle(self, f: Fonction, option_latex: str) -> Optional[str]:
        """Clé Typst d'une option LaTeX (`display score` → `display-score`), ou None si la fonction l'ignore."""
        o = option_latex.strip()
        if o in f.latex_vers_cle:
            return f.latex_vers_cle[o]
        tiret = re.sub(r"\s+", "-", o)
        if tiret in f.cles:
            return tiret
        if o in f.cles:
            return o
        return None

    def accepte_tout(self, f: Fonction) -> bool:
        """Fonction qui accepte des clés libres (`..cles`, `..options`) sans liste connue."""
        return f.variadique and not f.cles
