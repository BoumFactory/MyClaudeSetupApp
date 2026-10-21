"""Dump compact d'un niveau (compétences + automatismes) par sous-domaine.
Usage: python _dump_level.py 4E
"""
import json
import sys
from pathlib import Path

niv = sys.argv[1]
J = Path(__file__).resolve().parents[2] / "data" / "json" / f"{niv}.json"
d = json.loads(J.read_text(encoding="utf-8"))
TERM = (".", "!", "?", ")", "…", "»", ":", ";", "°")

print(f"===== {niv} — COMPÉTENCES (total {d['meta']['total_competences']}) =====")
for dom, sous in d["competences_by_theme"].items():
    for sd, comps in sous.items():
        print(f"\n### [{dom}] {sd}  ({len(comps)})")
        for c in comps:
            it = c["intitule"]
            flag = "" if it.rstrip().endswith(TERM) else "  <<<TRONQUÉ?"
            print(f"  {c['code']} ({c['type'][:4]},p{c.get('source',{}).get('page','?')}) {it}{flag}")

ad = d.get("automatismes_detailed", [])
print(f"\n===== {niv} — AUTOMATISMES ({len(ad)}) =====")
cur = None
for a in ad:
    if a.get("sous_domaine") != cur:
        cur = a.get("sous_domaine")
        print(f"\n## {cur}")
    it = a["text"]
    flag = "" if it.rstrip().endswith(TERM) else "  <<<TRONQUÉ?"
    print(f"  (p{a.get('source',{}).get('page','?')}) {it}{flag}")
