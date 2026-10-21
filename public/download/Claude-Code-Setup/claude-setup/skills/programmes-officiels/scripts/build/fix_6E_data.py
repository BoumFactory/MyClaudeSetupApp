"""6E : corrige les compétences tronquées (prolongements NB-025..029 + fraction
NB-035) et ajoute les automatismes « Les nombres entiers et décimaux » manquants
(fractions 2D détruites par le texte PDF → transcrites visuellement des PNG
cycle3 p13-14, autorisé par l'utilisateur pour ces cas).
"""
import json, re, shutil
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
J = ROOT / "data" / "json" / "6E.json"

# Prolongements (prose, cycle3 p14) — texte complet
COMP_FULL = {
    "6E-NB-025": "la découverte d’écritures des nombres à partir de lettres ou de dessins : numérations acrophoniques grecque, romaine, hiéroglyphique égyptienne",
    "6E-NB-026": "la découverte d’algorithmes opératoires, développés dans plusieurs traditions mathématiques, comme la multiplication par jalousies ou en tableau",
    "6E-NB-027": "la manipulation d’abaques à jetons ou de bouliers pour remobiliser le principe de la numération et la notion de base de numération",
    "6E-NB-028": "la découverte de la numération sexagésimale paléo-babylonienne, qui repose sur les mêmes principes mathématiques que le système utilisé pour exprimer des durées en heures, minutes et secondes. Le passage de ce système de numération au système décimal (et vice versa) est un autre contexte que celui des durées pour travailler la division euclidienne",
    "6E-NB-029": "la découverte de l’écriture des nombres décimaux utilisée par Simon Stevin de Bruges pour illustrer le lien entre numération décimale et fractions décimales",
    "6E-NB-035": "Savoir que la fraction a/b peut représenter un nombre entier, un nombre décimal non entier ou un nombre non décimal",
}

# Automatismes « Les nombres entiers et décimaux » (cycle3 p13) — fractions transcrites du PNG
AUTOS_NB = [
    "L’élève restitue de manière automatique les résultats suivants, relatifs aux relations entre 1/1000, 1/100, 1/10 et 1 : 1 = 10 × 1/10 ; 10 = 100 × 1/100 ; 100 = 1 000 × 1/1000 ; 1/10 = 10 × 1/100 ; 1/100 = 10 × 1/1000 ; 1 = 10 × 1/10 = 100 × 1/100 = 1 000 × 1/1000.",
    "L’élève restitue de manière automatique les équivalences d’écriture suivantes : 1/10 = 0,1 ; 1/100 = 0,01 ; 1/1000 = 0,001.",
    "L’élève passe de manière automatique d’une écriture sous forme de fraction décimale ou de somme de fractions décimales à une écriture décimale, et inversement.",
    "L’élève applique de manière automatique la procédure de multiplication d’un nombre décimal par 1, par 10, par 100 ou par 1 000, en lien avec la numération.",
    "Il applique de manière automatique la procédure de division d’un nombre décimal par 1, par 10, par 100 ou par 1 000.",
]


def slug(s):
    return re.sub(r"[^a-zA-Z0-9]+", "_", s.lower()).strip("_")[:50] or "x"


d = json.loads(J.read_text(encoding="utf-8"))
shutil.copy2(J, J.with_suffix(".json.bak2"))

# 1) compétences tronquées
nfix = 0
for dom, s in d["competences_by_theme"].items():
    for sd, cs in s.items():
        for c in cs:
            if c["code"] in COMP_FULL:
                full = COMP_FULL[c["code"]]
                c["intitule"] = full; c["formulation_bo"] = full; c["fingerprint"] = slug(full)
                c.get("extraction_meta", {}).pop("truncation_flag", None)
                c.setdefault("extraction_meta", {})["verified"] = True
                nfix += 1

# 2) automatismes Nombres ajoutés en tête
src = {"pdf": "cycle3.pdf", "page": 13, "bo_reference": d["meta"].get("bo_reference", ""),
       "bo_url": d["meta"].get("bo_url", ""), "page_image": "../pages/cycle3/page_013.png",
       "_note": "fractions transcrites visuellement du PNG (texte PDF illisible)"}
new = [{"text": t, "sous_domaine": "Les nombres entiers et décimaux", "domaine": "NB",
        "source": dict(src)} for t in AUTOS_NB]
d["automatismes_detailed"] = new + d.get("automatismes_detailed", [])
d["automatismes"] = [a["text"] for a in d["automatismes_detailed"]]

J.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
schema = json.loads((ROOT / "data" / "json" / "schema.json").read_text(encoding="utf-8"))
jsonschema.validate(d, schema)
print(f"[OK] 6E : {nfix} compétences détronquées, {len(AUTOS_NB)} automatismes Nombres ajoutés "
      f"(total auto {len(d['automatismes'])}). SCHEMA OK")
