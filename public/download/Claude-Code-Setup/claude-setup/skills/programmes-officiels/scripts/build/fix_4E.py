"""Corrige 4E : ré-extrait les automatismes (cycle4, niveau+exposants-conscient,
wrap-merge, repli sous-puces) et retire 2 compétences spurieuses absentes du BO
(4E-GEO-015 « Déterminer le centre du cercle circonscrit… », 4E-GEO-016
« Construire des rectangles sans équerre » — vérifié visuellement p14).
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
J = ROOT / "data" / "json" / "4E.json"
CY = ROOT / "data" / "pdf" / "cycle4.pdf"
NIV = "4E"

LEVELS = {"Cinquième": "5E", "Quatrième": "4E", "Troisième": "3E"}
MACROS = {"Nombres et calculs", "Espace et géométrie", "Géométrie",
          "Organisation et gestion de données et probabilités",
          "Proportionnalité, fonctions", "Pensée informatique"}
SOUS = {"Opérations", "Opérations sur les nombres relatifs", "Nombres relatifs",
        "Nombres rationnels", "Puissances", "Calcul littéral et algébrique",
        "Racine carrée", "Repérage sur une droite et dans le plan",
        "Représentation de l’espace", "Transformations", "Angles", "Triangles",
        "Parallélogrammes", "Parallélogrammes et translations", "Translations",
        "Statistiques", "Probabilités", "Proportionnalité", "Fonctions",
        "Homothéties", "Trigonométrie"}
SUP = {str(i): c for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}
DOM = {"Opérations sur les nombres relatifs": "NB", "Nombres relatifs": "NB",
       "Nombres rationnels": "NB", "Puissances": "NB", "Racine carrée": "NB",
       "Calcul littéral et algébrique": "AL", "Transformations": "GEO",
       "Repérage sur une droite et dans le plan": "GEO",
       "Représentation de l’espace": "GEO", "Parallélogrammes et translations": "GEO",
       "Triangles": "GEO", "Angles": "GEO", "Statistiques": "STA",
       "Probabilités": "PR", "Proportionnalité": "AL", "Fonctions": "AN"}
# fractions 2D que le texte PDF rend mal -> à signaler
GARBLED = ("Savoir qu’une fraction est aussi le quotient",
           "Compléter : 20 % de 120")


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

    # --- compétences : retirer GEO-015 / GEO-016 spurieux ---
    tri = cbt["GEO"]["Triangles"]
    cbt["GEO"]["Triangles"] = [c for c in tri if c["code"] not in ("4E-GEO-015", "4E-GEO-016")]

    # --- automatismes : ré-extraction propre ---
    autos = extract_autos(NIV)
    detailed, flat = [], []
    n_garbled = 0
    for sd, txt, pg in autos:
        txt = re.sub(r"[ \t]{2,}", " ", txt).strip()
        flat.append(txt)
        entry = {
            "text": txt, "sous_domaine": sd, "domaine": DOM.get(sd, "NB"),
            "source": {"pdf": "cycle4.pdf", "page": pg,
                       "bo_reference": data["meta"].get("bo_reference", ""),
                       "bo_url": data["meta"].get("bo_url", ""),
                       "page_image": f"../pages/cycle4/page_{pg:03d}.png"},
        }
        if txt.startswith(GARBLED):
            entry["extraction_note"] = "fraction 2D rendue imparfaitement par le PDF — à vérifier visuellement"
            n_garbled += 1
        detailed.append(entry)
    data["automatismes"] = flat
    data["automatismes_detailed"] = detailed

    # --- renum + stats ---
    by_dom, by_type = {}, {}
    for dom, sousd in cbt.items():
        n = 0
        for sd, comps in sousd.items():
            for c in comps:
                n += 1
                c["code"] = f"4E-{dom}-{n:03d}"
                by_dom[dom] = by_dom.get(dom, 0) + 1
                by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    data["meta"]["total_competences"] = sum(by_dom.values())
    data["stats"]["by_domaine"] = by_dom
    data["stats"]["by_type"] = by_type

    J.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    import jsonschema
    schema = json.loads((ROOT / "data" / "json" / "schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(data, schema)
    print(f"[OK] 4E corrigé. compétences={sum(by_dom.values())} (GEO {by_dom.get('GEO')}), "
          f"automatismes={len(flat)} (dont {n_garbled} signalés fraction 2D). SCHEMA OK")
    print(f"  by_domaine={by_dom}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
