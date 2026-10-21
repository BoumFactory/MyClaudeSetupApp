"""Retire les 21 automatismes 6E qui sont en réalité du PRÉAMBULE du BO cycle 3
(mal routés en automatismes par l'extraction : pages 2-4, codés AL). Garde les
vrais automatismes 6E (durées, configurations planes, proportionnalité).
"""
import json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
J = ROOT / "data" / "json" / "6E.json"
import shutil

PREAMBULE = {
    "Objectifs majeurs", "Organisation du travail des élèves",
    "Les écrits en mathématiques", "Les compétences psychosociales",
    "La résolution de problèmes", "Présentation",
}

d = json.loads(J.read_text(encoding="utf-8"))
shutil.copy2(J, J.with_suffix(".json.bak"))
ad = d.get("automatismes_detailed", [])
kept = [a for a in ad if a.get("sous_domaine") not in PREAMBULE]
removed = len(ad) - len(kept)
d["automatismes_detailed"] = kept
d["automatismes"] = [a["text"] for a in kept]
J.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

schema = json.loads((ROOT / "data" / "json" / "schema.json").read_text(encoding="utf-8"))
jsonschema.validate(d, schema)
print(f"[OK] 6E : {removed} automatismes de préambule retirés, {len(kept)} conservés. SCHEMA OK")
from collections import Counter
print("  sous-domaines restants:", dict(Counter(a['sous_domaine'] for a in kept)))
