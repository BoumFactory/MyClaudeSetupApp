"""Distingue les capacités « lire » et « placer » du repérage : un objectif/
automatisme par action, avec son contexte répété.

« {ctx} : lire … ; placer … »  ->  « {ctx} : lire …. »  +  « {ctx} : placer …. »

Ne s'applique QUE si toutes les sous-parties commencent par lire/placer
(garde-fou : ne casse pas les listes d'exemples type « angles : plein ; plat ; … »).
5E : compétences (GEO/Repérage) → renumérote GEO. 4E/3E : automatismes.
"""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.lower()).strip("_")
    return s[:50] or "x"


def split_ctx(text: str):
    if " : " not in text or " ; " not in text:
        return [text]
    ctx, rest = text.split(" : ", 1)
    parts = [p.strip() for p in rest.split(" ; ")]
    if not all(p.lower().startswith(("lire", "placer")) for p in parts):
        return [text]
    return [f"{ctx} : {p.rstrip('; .').strip()}." for p in parts]


def fix_5E():
    J = ROOT / "data" / "json" / "5E.json"
    data = json.loads(J.read_text(encoding="utf-8"))
    cbt = data["competences_by_theme"]
    rep = cbt["GEO"]["Repérage sur une droite et dans le plan"]
    newrep = []
    for c in rep:
        sp = split_ctx(c["intitule"])
        if len(sp) == 1:
            newrep.append(c)
        else:
            for s in sp:
                nc = deepcopy(c)
                nc["intitule"] = s; nc["formulation_bo"] = s; nc["fingerprint"] = slug(s)
                newrep.append(nc)
    cbt["GEO"]["Repérage sur une droite et dans le plan"] = newrep
    # renum + stats
    by_dom, by_type = {}, {}
    for dom, sousd in cbt.items():
        n = 0
        for sd, comps in sousd.items():
            for c in comps:
                n += 1
                c["code"] = f"5E-{dom}-{n:03d}"
                by_dom[dom] = by_dom.get(dom, 0) + 1
                by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    data["meta"]["total_competences"] = sum(by_dom.values())
    data["stats"]["by_domaine"] = by_dom
    data["stats"]["by_type"] = by_type
    J.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"5E : Repérage -> {len(newrep)} objectifs, total {sum(by_dom.values())} (GEO {by_dom['GEO']})")


def fix_autos(niv: str):
    J = ROOT / "data" / "json" / f"{niv}.json"
    data = json.loads(J.read_text(encoding="utf-8"))
    new = []
    changed = 0
    for a in data.get("automatismes_detailed", []):
        sp = split_ctx(a["text"])
        if len(sp) == 1:
            new.append(a)
        else:
            changed += 1
            for s in sp:
                na = deepcopy(a); na["text"] = s; new.append(na)
    data["automatismes_detailed"] = new
    data["automatismes"] = [a["text"] for a in new]
    J.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{niv} : automatismes -> {len(new)} ({changed} splitté)")


def main():
    fix_5E()
    fix_autos("4E")
    fix_autos("3E")
    # validation
    import jsonschema
    schema = json.loads((ROOT / "data" / "json" / "schema.json").read_text(encoding="utf-8"))
    for niv in ("5E", "4E", "3E"):
        d = json.loads((ROOT / "data" / "json" / f"{niv}.json").read_text(encoding="utf-8"))
        jsonschema.validate(d, schema)
    print("SCHEMA OK (5E/4E/3E)")


if __name__ == "__main__":
    main()
