"""Fusionne les automatismes 5e reconstruits dans data/json/5E.json.

- Sauvegarde 5E.json avant écriture.
- Remplace `automatismes` (liste de strings) et `automatismes_detailed`.
- Normalisation typographique légère (espace avant point) — pas de modif de sens.
- Scan heuristique des compétences potentiellement tronquées (rapport).
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
J = ROOT / "data" / "json" / "5E.json"
CLEAN = Path(__file__).resolve().parents[1] / "data" / "_tmp" / "automatismes_5e_clean.json"


def norm(t: str) -> str:
    t = re.sub(r"\s+\.", ".", t)        # "7/1 ." -> "7/1."
    t = re.sub(r"\s+,", ",", t)          # "x ," -> "x,"
    t = re.sub(r"[ \t]{2,}", " ", t)     # espaces multiples
    return t.strip()


def main() -> int:
    data = json.loads(J.read_text(encoding="utf-8"))
    clean = json.loads(CLEAN.read_text(encoding="utf-8"))

    shutil.copy2(J, J.with_suffix(".json.bak"))

    detailed = []
    flat = []
    for a in clean:
        txt = norm(a["text"])
        flat.append(txt)
        detailed.append({
            "text": txt,
            "sous_domaine": a["sous_domaine"],
            "domaine": a["domaine"],
            "source": a["source"],
        })

    data["automatismes"] = flat
    data["automatismes_detailed"] = detailed
    data.setdefault("meta", {})["automatismes_source"] = (
        "Liste-des-automatismes-5e.pdf (extraction mécanique) ; sous-domaines & pages "
        "alignés BO cycle4.pdf, vérifiés visuellement (anti-régurgitation)."
    )

    # --- Scan heuristique compétences tronquées ---
    TERMINALS = (".", "!", "?", ")", "…", "»", ":", ";", "°")
    truncated = []
    for dom, sousd in data.get("competences_by_theme", {}).items():
        for sd, comps in sousd.items():
            for c in comps:
                fb = (c.get("formulation_bo") or "").rstrip()
                if fb and not fb.endswith(TERMINALS):
                    truncated.append((c.get("code"), fb[-55:]))

    J.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] 5E.json : {len(flat)} automatismes (detailed={len(detailed)})")
    print(f"[OK] backup : {J.with_suffix('.json.bak').name}")
    print(f"\n[SCAN] compétences potentiellement tronquées : {len(truncated)}")
    for code, tail in truncated:
        print(f"   {code} … «…{tail}»")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
