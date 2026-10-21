#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
compare.py — Compare deux niveaux par sous-domaine.

Distingue ce qui apparaît dans le niveau A uniquement, dans B uniquement, ou
dans les deux. La comparaison se fait sur les sous-domaines normalisés
(lowercase + sans accents) : un sous-domaine présent en CM2 mais absent en 6e
révèle une notion abandonnée ; présent en 6e mais pas en CM2 = nouveauté.

Note : la comparaison par code de compétence serait trompeuse (un CM2-NB-001
et un 6E-NB-001 ne se correspondent pas). Le grouping par sous-domaine est
pédagogiquement le plus parlant.

Usage :
    python scripts/compare.py CM2 6E
    python scripts/compare.py 5E 4E --domaine GEO
    python scripts/compare.py 1SPE 1TEC --domaine STA
    python scripts/compare.py CM1 CM2 --format json
"""

import argparse
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SKILL_DIR = Path(__file__).resolve().parent.parent
ALL_FLAT = SKILL_DIR / "data" / "json" / "all_flat.json"

NIVEAUX = ["CM1", "CM2", "6E", "5E", "4E", "3E", "2GT", "1SPE", "1ENS", "1TEC",
           "TSPE", "TCOMP", "TTEC"]
DOMAINES = ["NB", "AL", "AN", "GEO", "GM", "STA", "PR", "OGD", "ALGO", "TRG", "LOG"]


def norm(s: str) -> str:
    s = (s or "").lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def collect(all_comps: list[dict], niveau: str, domaine: str | None) -> dict[str, list[dict]]:
    """Retourne {sous_domaine_norm: [compétences]} pour un niveau (et domaine optionnel)."""
    out: dict[str, list[dict]] = {}
    for c in all_comps:
        if c["niveau"] != niveau:
            continue
        if domaine and c["domaine"] != domaine:
            continue
        key = norm(c.get("sous_domaine") or "a_classer")
        out.setdefault(key, []).append(c)
    return out


def representative_label(comps: list[dict]) -> str:
    """Étiquette représentative pour un sous-domaine (premier intitulé non normalisé)."""
    return comps[0].get("sous_domaine") or "(à classer)"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("niveau_a", choices=NIVEAUX)
    ap.add_argument("niveau_b", choices=NIVEAUX)
    ap.add_argument("--domaine", choices=DOMAINES, help="Filtrer sur un domaine")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    if args.niveau_a == args.niveau_b:
        print("Les deux niveaux doivent être différents.", file=sys.stderr)
        sys.exit(2)
    if not ALL_FLAT.exists():
        print("Erreur : data/json/all_flat.json absent.", file=sys.stderr)
        sys.exit(1)
    all_comps = json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]

    a = collect(all_comps, args.niveau_a, args.domaine)
    b = collect(all_comps, args.niveau_b, args.domaine)

    keys_a, keys_b = set(a), set(b)
    only_a = sorted(keys_a - keys_b)
    only_b = sorted(keys_b - keys_a)
    commun = sorted(keys_a & keys_b)

    if args.format == "json":
        out = {
            "niveau_a": args.niveau_a,
            "niveau_b": args.niveau_b,
            "domaine_filtre": args.domaine,
            "only_a": [{"sous_domaine": representative_label(a[k]), "n": len(a[k])} for k in only_a],
            "only_b": [{"sous_domaine": representative_label(b[k]), "n": len(b[k])} for k in only_b],
            "commun": [{"sous_domaine": representative_label(a[k]),
                        "n_a": len(a[k]), "n_b": len(b[k])} for k in commun],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    title_dom = f" / domaine={args.domaine}" if args.domaine else ""
    print(f"=== Comparaison {args.niveau_a} ↔ {args.niveau_b}{title_dom} ===\n")

    print(f"--- Sous-domaines uniquement en {args.niveau_a} ({len(only_a)}) ---")
    for k in only_a:
        print(f"  [{len(a[k]):3} comp.] {representative_label(a[k])}")
    print()

    print(f"--- Sous-domaines uniquement en {args.niveau_b} ({len(only_b)}) ---")
    for k in only_b:
        print(f"  [{len(b[k]):3} comp.] {representative_label(b[k])}")
    print()

    print(f"--- Sous-domaines communs ({len(commun)}) ---")
    for k in commun:
        na, nb = len(a[k]), len(b[k])
        diff = ""
        if na != nb:
            diff = f"  (Δ={nb - na:+d})"
        print(f"  {args.niveau_a}:{na:3} | {args.niveau_b}:{nb:3}  {representative_label(a[k])}{diff}")


if __name__ == "__main__":
    main()
