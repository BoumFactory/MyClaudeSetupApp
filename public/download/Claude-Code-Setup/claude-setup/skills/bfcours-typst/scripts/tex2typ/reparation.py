"""Réparation par compilation : tant que Typst refuse le document, le nœud fautif est replié.

Le convertisseur entoure chaque nœud repliable de marqueurs invisibles. Après écriture, on compile les deux
versions (professeur, élève) ; l'erreur donne une ligne et une colonne, qui désignent la plus petite région
qui les contient. Ce nœud est alors converti autrement : un bloc devient un extrait `#latex[…]` (rendu par
LaTeX, fidèle), un élément en ligne devient un marqueur orange `#a-reprendre("…")`. On recommence.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .ecriture import FER, OUV, SEP

LIEU = re.compile(r"┌─\s*(.+?):(\d+):(\d+)")


def retirer_marqueurs(brut: str) -> Tuple[str, Dict[int, Tuple[int, int, int, int]]]:
    """Texte sans marqueurs, et pour chaque région : (ligne début, colonne début, ligne fin, colonne fin)."""
    sortie: List[str] = []
    ouvertes: Dict[int, Tuple[int, int]] = {}
    spans: Dict[int, Tuple[int, int, int, int]] = {}
    ligne, col = 1, 1
    i, n = 0, len(brut)
    while i < n:
        c = brut[i]
        if c in (OUV, FER):
            j = brut.index(SEP, i)
            ident = int(brut[i + 1:j])
            if c == OUV:
                ouvertes[ident] = (ligne, col)
            else:
                l0, c0 = ouvertes.pop(ident, (ligne, col))
                spans[ident] = (l0, c0, ligne, col)
            i = j + 1
            continue
        sortie.append(c)
        if c == "\n":
            ligne += 1
            col = 1
        else:
            col += 1
        i += 1
    return "".join(sortie), spans


def _contient(span, ligne: int, col: int) -> bool:
    l0, c0, l1, c1 = span
    if ligne < l0 or ligne > l1:
        return False
    if ligne == l0 and col < c0:
        return False
    if ligne == l1 and col > c1:
        return False
    return True


def _taille(span) -> Tuple[int, int]:
    l0, c0, l1, c1 = span
    return (l1 - l0, (c1 - c0) if l1 == l0 else 10 ** 6)


def lieux_erreur(erreur, fichier: Path) -> List[Tuple[int, int]]:
    """Positions (ligne, colonne) dans `fichier` citées par l'erreur Typst (diagnostic et trace)."""
    textes = [getattr(erreur, "diagnostic", "") or str(erreur)]
    textes += [str(t) for t in (getattr(erreur, "trace", None) or [])]
    lieux = []
    for t in textes:
        for m in LIEU.finditer(t.replace("\\\\?\\", "").replace("\\?\\", "")):
            chemin = m.group(1).strip()
            if Path(chemin).name == fichier.name:
                lieux.append((int(m.group(2)), int(m.group(3))))
    return lieux


def assurer_index_rendus(fichier: Path) -> None:
    """Crée `rendus-tex/index.json` (vide) à côté d'un document qui lit ses rendus (`setbflatex(…, lire: …)`).

    Typst ne sait pas tester l'existence d'un fichier : sans lui, toute compilation du document échoue sur
    « file not found ». bfwatch le crée aussi ; ce repli sert aux compilations sans bfwatch."""
    try:
        texte = Path(fichier).read_text(encoding="utf-8", errors="replace")
        if "setbflatex" not in texte or not re.search(r"\blire\s*:", texte):
            return
        index = Path(fichier).parent / "rendus-tex" / "index.json"
        if not index.is_file():
            index.parent.mkdir(exist_ok=True)
            index.write_text('{"extraits": {}, "usage": {}, "version": 1}\n', encoding="utf-8")
    except OSError:
        pass


def compiler_versions(fichier: Path, polices: List[str], racine: Path):
    """Compile les deux versions ; renvoie la première erreur Typst, ou None."""
    import typst
    import localiser
    assurer_index_rendus(fichier)
    for correction in ("true", "false"):
        try:
            typst.compile(str(fichier), root=str(racine), font_paths=polices,
                          sys_inputs={"correction": correction, "prof": correction}, **localiser.options_paquets())
        except typst.TypstError as e:
            return e
    return None


def region_fautive(lieux, spans, regions, deja) -> Optional[int]:
    """Plus petite région (pas encore repliée) qui contient une position de l'erreur."""
    for ligne, col in lieux:
        candidats = [(k, s) for k, s in spans.items() if _contient(s, ligne, col) and k in regions
                     and regions[k].cle not in deja]
        if candidats:
            candidats.sort(key=lambda ks: _taille(ks[1]))
            return candidats[0][0]
    return None
