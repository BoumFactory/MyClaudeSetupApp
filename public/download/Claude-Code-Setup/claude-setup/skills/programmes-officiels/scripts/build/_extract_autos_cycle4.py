"""Extrait les AUTOMATISMES d'un niveau (5E/4E/3E) depuis cycle4.pdf.

Niveau-conscient (ne prend que les sections du niveau cible), exposants-conscients
(spans superscript -> exposants Unicode), wrap-merge + repli des sous-puces.
Mode lecture seule : imprime le résultat pour vérification visuelle.

Usage: python _extract_autos_cycle4.py 4E
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

NIV = sys.argv[1]
CY = Path(__file__).resolve().parents[2] / "data" / "pdf" / "cycle4.pdf"

LEVELS = {"Cinquième": "5E", "Quatrième": "4E", "Troisième": "3E"}
MACROS = {
    "Nombres et calculs", "Espace et géométrie", "Géométrie",
    "Organisation et gestion de données et probabilités",
    "Proportionnalité, fonctions", "Pensée informatique",
}
SOUS = {
    "Opérations", "Opérations sur les nombres relatifs", "Nombres relatifs",
    "Nombres rationnels", "Puissances", "Calcul littéral et algébrique",
    "Racine carrée", "Repérage sur une droite et dans le plan",
    "Représentation de l’espace", "Transformations", "Angles", "Triangles",
    "Parallélogrammes", "Parallélogrammes et translations", "Translations",
    "Statistiques", "Probabilités", "Proportionnalité", "Fonctions",
    "Homothéties", "Trigonométrie",
}
SUP = {str(i): c for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}


def line_text(line) -> str:
    out = []
    for s in line["spans"]:
        t = s["text"]
        if s["flags"] & 1:  # superscript
            t = "".join(SUP.get(ch, ch) for ch in t)
        out.append(t)
    return "".join(out).strip()


def section_of(t: str):
    if t.startswith("Automatismes"):
        return "auto"
    if t.startswith("Objectifs d"):
        return "obj"
    if t.startswith("Prolongements"):
        return "prol"
    return None


def main() -> int:
    doc = fitz.open(CY)
    niveau = None
    sousdom = None
    section = None
    result: list[tuple[str, str]] = []  # (sousdom, automatisme)
    for pno in range(doc.page_count):
        for block in doc[pno].get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                if not line.get("spans"):
                    continue
                t = line_text(line)
                if not t:
                    continue
                if t in LEVELS:
                    niveau = LEVELS[t]; sousdom = None; section = None; continue
                if t in MACROS:
                    section = None; continue
                if t in SOUS:
                    sousdom = t; section = None; continue
                sec = section_of(t)
                if sec:
                    section = sec; continue
                # ligne de contenu
                if niveau == NIV and section == "auto" and sousdom:
                    stripped = t.lstrip("−–- ").strip()
                    is_bullet = t.lstrip().startswith(("−", "–", "-"))
                    is_sub = t.lstrip().startswith("•")
                    if is_bullet:
                        result.append([sousdom, stripped])
                    elif result and (is_sub or t[:1].islower() or t[:1] in "(«"):
                        result[-1][1] += " " + (t.lstrip("• ").strip() if is_sub else t.strip())
                    elif result:
                        result[-1][1] += " " + t.strip()
    doc.close()

    cur = None
    n = 0
    for sd, txt in result:
        if sd != cur:
            cur = sd; print(f"\n## {sd}")
        n += 1
        print(f"  - {txt}")
    print(f"\n[{NIV}] {n} automatismes extraits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
