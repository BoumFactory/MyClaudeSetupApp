"""Corrige 3E : ré-extraction automatismes (SOUS complété : Multiples et diviseurs,
Translations et vecteurs) + nettoyage compétences (préambule AL-008/009, en-tête
GEO-009 « Prolongements possibles »), correction des pages 21/22 inexistantes,
flag des prolongements tronqués. Anti-régurgitation : textes issus d'extraction PDF.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
J = ROOT / "data" / "json" / "3E.json"
CY = ROOT / "data" / "pdf" / "cycle4.pdf"
NIV = "3E"

LEVELS = {"Cinquième": "5E", "Quatrième": "4E", "Troisième": "3E"}
MACROS = {"Nombres et calculs", "Espace et géométrie", "Géométrie",
          "Organisation et gestion de données et probabilités",
          "Proportionnalité, fonctions", "Pensée informatique"}
SOUS = {"Opérations sur les nombres relatifs", "Nombres relatifs",
        "Nombres rationnels", "Puissances", "Calcul littéral et algébrique",
        "Racine carrée", "Multiples et diviseurs", "Repérage sur une droite et dans le plan",
        "Représentation de l’espace", "Transformations", "Angles", "Triangles",
        "Parallélogrammes et translations", "Translations et vecteurs", "Translations",
        "Statistiques", "Probabilités", "Proportionnalité", "Fonctions",
        "Homothéties", "Trigonométrie"}
SUP = {str(i): c for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}
DOM = {"Nombres rationnels": "NB", "Puissances": "NB", "Racine carrée": "NB",
       "Multiples et diviseurs": "NB", "Calcul littéral et algébrique": "AL",
       "Repérage sur une droite et dans le plan": "GEO", "Représentation de l’espace": "GEO",
       "Triangles": "GEO", "Translations et vecteurs": "GEO", "Statistiques": "STA",
       "Probabilités": "PR", "Proportionnalité": "AL", "Fonctions": "AN"}
# page valide de repli par domaine (pour corriger les pages 21/22 inexistantes)
FALLBACK_PAGE = {"AN": 19, "GEO": 16, "NB": 11, "AL": 19, "STA": 17, "PR": 18, "ALGO": 20}
TERM = (".", "!", "?", ")", "…", "»", ":", ";", "°")


def line_text(line) -> str:
    out = []
    for s in line["spans"]:
        t = s["text"]
        if s["flags"] & 1:
            t = "".join(SUP.get(ch, ch) for ch in t)
        out.append(t)
    return "".join(out).strip()


def extract_autos(niv: str):
    doc = fitz.open(CY)
    niveau = sousdom = section = None
    res = []
    for pno in range(doc.page_count):
        for block in doc[pno].get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                if not line.get("spans"):
                    continue
                t = line_text(line)
                if not t:
                    continue
                if t in LEVELS:
                    niveau, sousdom, section = LEVELS[t], None, None; continue
                if t in MACROS:
                    section = None; continue
                if t in SOUS:
                    sousdom, section = t, None; continue
                if t.startswith("Automatismes"): section = "auto"; continue
                if t.startswith("Objectifs d"): section = "obj"; continue
                if t.startswith("Prolongements"): section = "prol"; continue
                if niveau == niv and section == "auto" and sousdom:
                    is_bullet = t.lstrip().startswith(("−", "–", "-"))
                    is_sub = t.lstrip().startswith("•")
                    stripped = t.lstrip("−–- ").strip()
                    if is_bullet:
                        res.append([sousdom, stripped, pno + 1])
                    elif res and (is_sub or t[:1].islower() or t[:1] in "(«"):
                        res[-1][1] += " " + (t.lstrip("• ").strip() if is_sub else t.strip())
                    elif res:
                        res[-1][1] += " " + t.strip()
    doc.close()
    return res


def main() -> int:
    data = json.loads(J.read_text(encoding="utf-8"))
    shutil.copy2(J, J.with_suffix(".json.bak"))
    cbt = data["competences_by_theme"]

    # --- compétences : retirer préambule + en-tête mal extraits ---
    if "Proportionnalité, fonctions" in cbt.get("AL", {}):
        del cbt["AL"]["Proportionnalité, fonctions"]  # AL-008/009 préambule
    if "Triangles" in cbt.get("GEO", {}):
        cbt["GEO"]["Triangles"] = [
            c for c in cbt["GEO"]["Triangles"]
            if not c["intitule"].startswith("Prolongements possibles")  # GEO-009 en-tête
        ]

    # --- corriger pages 21/22 inexistantes + flag prolongements tronqués ---
    fixed_pages = flagged = 0
    for dom, sousd in cbt.items():
        for sd, comps in sousd.items():
            for c in comps:
                pg = c.get("source", {}).get("page", 0)
                if isinstance(pg, int) and pg > 20:
                    newp = FALLBACK_PAGE.get(dom, 19)
                    c["source"]["page"] = newp
                    c["source"]["page_image"] = f"../pages/cycle4/page_{newp:03d}.png"
                    c["source"].setdefault("_note", "page corrigée (réf. d'origine hors PDF)")
                    fixed_pages += 1
                if not c["intitule"].rstrip().endswith(TERM):
                    c.setdefault("extraction_meta", {})["truncation_flag"] = True
                    flagged += 1

    # --- automatismes : ré-extraction propre ---
    autos = extract_autos(NIV)
    detailed, flat = [], []
    for sd, txt, pg in autos:
        txt = re.sub(r"[ \t]{2,}", " ", txt).strip()
        flat.append(txt)
        detailed.append({
            "text": txt, "sous_domaine": sd, "domaine": DOM.get(sd, "NB"),
            "source": {"pdf": "cycle4.pdf", "page": pg,
                       "bo_reference": data["meta"].get("bo_reference", ""),
                       "bo_url": data["meta"].get("bo_url", ""),
                       "page_image": f"../pages/cycle4/page_{pg:03d}.png"},
        })
    data["automatismes"] = flat
    data["automatismes_detailed"] = detailed

    # --- renum + stats ---
    by_dom, by_type = {}, {}
    for dom, sousd in cbt.items():
        n = 0
        for sd, comps in sousd.items():
            for c in comps:
                n += 1
                c["code"] = f"3E-{dom}-{n:03d}"
                by_dom[dom] = by_dom.get(dom, 0) + 1
                by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    data["meta"]["total_competences"] = sum(by_dom.values())
    data["stats"]["by_domaine"] = by_dom
    data["stats"]["by_type"] = by_type

    J.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    import jsonschema
    schema = json.loads((ROOT / "data" / "json" / "schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(data, schema)
    print(f"[OK] 3E corrigé. compétences={sum(by_dom.values())}, automatismes={len(flat)}, "
          f"pages_corrigées={fixed_pages}, prolongements_tronqués_signalés={flagged}. SCHEMA OK")
    print(f"  by_domaine={by_dom}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
