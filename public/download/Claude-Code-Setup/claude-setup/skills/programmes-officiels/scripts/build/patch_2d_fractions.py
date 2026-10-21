"""Réinjecte les 6 textes dictés par l'utilisateur depuis le BO (fractions 2D +
prolongements tronqués que le texte PDF ne rendait pas). Source = lecture humaine
du BO (autoritaire), pas de génération LLM.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
A = "’"  # apostrophe typographique

AUTO = {
    "4E": [
        ("Savoir qu’une fraction est aussi le quotient",
         "Savoir qu’une fraction est aussi le quotient : 3/7 (le nombre qui, multiplié par 7, donne 3, donc savoir que 7 × 3/7 = 3)."),
        ("Compléter : 20 % de 120",
         "Compléter : 20 % de 120 = … ; 30 = …/100 × 1 000."),
    ],
    "3E": [
        ("Simplifier une fraction dont le numérateur",
         "Simplifier une fraction dont le numérateur et le dénominateur sont dans une même table de multiplication, par exemple 15/35 et 63/14."),
    ],
}
COMP_3E = [
    ("capter les chaines de",
     "Notion de parabole et de faisceaux convergents vers son foyer. Lien avec les paraboles pour capter les chaines de télévision."),
    ("Archimède comme étant",
     "La formule du volume, trouvée au IIIe siècle avant J.-C., d’après une intuition d’Archimède comme étant 2/3 du cylindre qui contient la boule."),
    ("De divina",
     "Les cinq polyèdres réguliers de l’espace et les illustrations de Léonard de Vinci pour le traité mathématique De divina proportione de Luca Pacioli."),
]


def slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.lower()).strip("_")
    return s[:50] or "x"


def patch_autos(niv: str):
    J = ROOT / "data" / "json" / f"{niv}.json"
    d = json.loads(J.read_text(encoding="utf-8"))
    hits = 0
    for a in d.get("automatismes_detailed", []):
        for key, full in AUTO.get(niv, []):
            if a["text"].startswith(key):
                a["text"] = full
                a.pop("extraction_note", None)
                a["source"]["_note"] = "fraction dictée par l’utilisateur depuis le BO"
                hits += 1
    d["automatismes"] = [a["text"] for a in d.get("automatismes_detailed", [])]
    J.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return hits


def patch_comps_3E():
    J = ROOT / "data" / "json" / "3E.json"
    d = json.loads(J.read_text(encoding="utf-8"))
    hits = 0
    for dom, sousd in d["competences_by_theme"].items():
        for sd, comps in sousd.items():
            for c in comps:
                for key, full in COMP_3E:
                    if key in c["intitule"]:
                        c["intitule"] = full
                        c["formulation_bo"] = full
                        c["fingerprint"] = slug(full)
                        c.get("extraction_meta", {}).pop("truncation_flag", None)
                        c.setdefault("extraction_meta", {})["verified"] = True
                        hits += 1
    J.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return hits


def main():
    h4 = patch_autos("4E")
    h3a = patch_autos("3E")
    h3c = patch_comps_3E()
    schema = json.loads((ROOT / "data" / "json" / "schema.json").read_text(encoding="utf-8"))
    for niv in ("4E", "3E"):
        jsonschema.validate(json.loads((ROOT / "data" / "json" / f"{niv}.json").read_text(encoding="utf-8")), schema)
    print(f"[OK] 4E autos patchés={h4} ; 3E autos patchés={h3a} ; 3E prolongements patchés={h3c}. SCHEMA OK")


if __name__ == "__main__":
    main()
