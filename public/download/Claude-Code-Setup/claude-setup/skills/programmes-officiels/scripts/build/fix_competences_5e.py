"""Corrige les 3 défauts de compétences 5e identifiés par vérification visuelle.

1. 5E-NB-012 tronqué -> texte complet ré-extrait mécaniquement de cycle4.pdf p7.
2. Repérage sur-découpé (6 fragments) -> 2 objectifs repliés (texte verbatim des
   bullets mécaniques page_012.json).
3. Probabilités : retire les 4 automatismes mal routés en compétences, garde les
   4 vrais objectifs d'apprentissage.
Puis renumérote chaque domaine en codes consécutifs et recalcule meta/stats.
Anti-régurgitation : tout texte vient d'une extraction PDF/bullets, jamais retapé par le LLM.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
J = ROOT / "data" / "json" / "5E.json"
CY = ROOT / "data" / "pdf" / "cycle4.pdf"
BUL12 = ROOT / "data" / "bullets" / "cycle4" / "page_012.json"


def slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.lower()).strip("_")
    return s[:50] or "x"


def extract_np() -> str:
    """Texte complet du prolongement 'Notion de nombre premier...' (cycle4 p7)."""
    doc = fitz.open(CY)
    txt = doc[6].get_text("text")  # page 7 = index 6
    doc.close()
    flat = re.sub(r"\s+", " ", txt)
    m = re.search(r"Notion de nombre premier.*?\)", flat)
    if not m:
        raise RuntimeError("NB-012 introuvable dans cycle4 p7")
    return m.group(0).strip()


def reperage_objectifs() -> list[str]:
    """Replie les 6 bullets Repérage en 2 objectifs (verbatim source)."""
    bj = json.loads(BUL12.read_text(encoding="utf-8"))
    bullets = []
    for sec in bj["page_data"]["sections"]:
        if sec["sous_domaine"] == "Repérage sur une droite et dans le plan" \
           and sec["title"].startswith("Objectifs"):
            bullets = [b["formulation_bo"] for b in sec["bullets"]]
    # 6 bullets -> 2 objectifs (colon-line + 2 sous-items chacun)
    assert len(bullets) == 6, f"attendu 6 bullets Repérage, vu {len(bullets)}"
    o1 = f"{bullets[0]} {bullets[1]} {bullets[2]}"
    o2 = f"{bullets[3]} {bullets[4]} {bullets[5]}"
    return [o1, o2]


def make_comp(model: dict, intitule: str, type_: str = "capacite") -> dict:
    """Construit une compétence en copiant la structure d'un modèle existant."""
    c = json.loads(json.dumps(model))  # deep copy
    c["intitule"] = intitule
    c["formulation_bo"] = intitule
    c["fingerprint"] = slug(intitule)
    c["type"] = type_
    c["tags"] = [type_]
    c.setdefault("extraction_meta", {})
    c["extraction_meta"]["verified"] = True
    c["extraction_meta"]["agent_version"] = "v2.1-visual-fix-s10"
    return c


PR_KEEP_PREFIXES = (
    "Aborder les questions relatives au hasard",
    "Utiliser le vocabulaire des probabilités",
    "Attribuer des probabilités dans des cas simples",
    "Répéter matériellement une expérience aléatoire",
)


def main() -> int:
    data = json.loads(J.read_text(encoding="utf-8"))
    shutil.copy2(J, J.with_suffix(".json.bak2"))
    cbt = data["competences_by_theme"]

    # --- 1) NB-012 : texte complet ---
    np_full = extract_np()
    for c in cbt["NB"]["Opérations"]:
        if c["code"] == "5E-NB-012":
            c["intitule"] = np_full
            c["formulation_bo"] = np_full
            c["fingerprint"] = slug(np_full)
            c["extraction_meta"]["verified"] = True

    # --- 2) Repérage : 6 -> 2 ---
    rep = cbt["GEO"]["Repérage sur une droite et dans le plan"]
    model = rep[0]
    o1, o2 = reperage_objectifs()
    cbt["GEO"]["Repérage sur une droite et dans le plan"] = [
        make_comp(model, o1), make_comp(model, o2)
    ]

    # --- 3) Probabilités : garder uniquement les 4 vrais objectifs ---
    pr = cbt["PR"]["Probabilités"]
    kept = [c for c in pr if c["intitule"].startswith(PR_KEEP_PREFIXES)]
    cbt["PR"]["Probabilités"] = kept

    # --- 4) Renumérotation consécutive par domaine + stats ---
    by_dom, by_type = {}, {}
    for dom, sousd in cbt.items():
        n = 0
        for sd, comps in sousd.items():
            for c in comps:
                n += 1
                c["code"] = f"5E-{dom}-{n:03d}"
                by_dom[dom] = by_dom.get(dom, 0) + 1
                by_type[c["type"]] = by_type.get(c["type"], 0) + 1

    total = sum(by_dom.values())
    data["meta"]["total_competences"] = total
    data["stats"]["by_domaine"] = by_dom
    data["stats"]["by_type"] = by_type

    J.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] 5E.json corrigé. total_competences = {total}")
    print(f"  NB-012 -> «{np_full[-45:]}»")
    print(f"  Repérage -> 2 objectifs (ex: «{o1[:60]}…»)")
    print(f"  Probabilités -> {len(kept)} objectifs gardés")
    print(f"  by_domaine = {by_dom}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
