#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
06_export_markdown.py — Export markdown miroir depuis les JSON niveau.

Phase 7 du pipeline. Pour chaque compétence d'un fichier data/json/{NIVEAU}.json,
produit data/markdown/{cycle}/{niveau}/{domaine_kebab}/{code}.md selon le
template de 03-ARCHITECTURE.md §4.

Idempotent : ré-exécuter ne change rien si le JSON n'a pas changé.

Usage :
    python scripts/build/06_export_markdown.py             # tous les niveaux
    python scripts/build/06_export_markdown.py --niveau 2GT
"""

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
JSON_DIR = DATA_DIR / "json"
MD_DIR = DATA_DIR / "markdown"

DOMAIN_KEBAB = {
    "NB": "nombres", "AL": "algebre", "AN": "analyse",
    "GEO": "geometrie", "GM": "grandeurs-mesures",
    "STA": "statistiques", "PR": "probabilites",
    "OGD": "organisation-gestion-donnees",
    "ALGO": "algorithmique", "TRG": "trigonometrie", "LOG": "logique"
}

CYCLE_OF_NIVEAU = {
    "CM1": "ecole/cycle3", "CM2": "ecole/cycle3", "6E": "ecole/cycle3",
    "5E": "college/cycle4", "4E": "college/cycle4", "3E": "college/cycle4",
    "2GT": "lycee", "1SPE": "lycee", "1ENS": "lycee", "1TEC": "lycee",
    "TSPE": "lycee", "TCOMP": "lycee", "TTEC": "lycee"
}


def render_yaml_list(items):
    if not items:
        return "[]"
    out = "\n"
    for it in items:
        out += f"  - {it}\n"
    return out.rstrip()


def render_md(c: dict) -> str:
    """Produit le markdown d'une compétence."""
    src = c.get("source", {})
    # Le chemin page_image dans le JSON est relatif depuis data/json/.
    # Pour le markdown placé en data/markdown/{cycle}/{niveau}/{dom}/file.md,
    # le chemin relatif vers data/pages/{folder}/page_NNN.png devient :
    # - depuis data/markdown/lycee/2GT/nombres/file.md → ../../../../pages/2GT/page_005.png
    # - depuis data/markdown/college/cycle4/4E/nombres/file.md → ../../../../../pages/cycle4/page_005.png
    # On déduit le chemin depuis JSON_DIR + img_rel, puis on calcule le relatif depuis le MD final.
    img_rel = src.get("page_image", "")

    fm_lines = [
        "---",
        f"code: {c['code']}",
        f"intitule: {json.dumps(c.get('intitule', ''), ensure_ascii=False)}",
        f"fingerprint: {c.get('fingerprint', '')}",
        f"niveau: {c['niveau']}",
        f"domaine: {c['domaine']}",
    ]
    if c.get("sous_domaine"):
        fm_lines.append(f"sous_domaine: {json.dumps(c['sous_domaine'], ensure_ascii=False)}")
    fm_lines.append(f"type: {c['type']}")
    fm_lines.append("source:")
    fm_lines.append(f"  pdf: {src.get('pdf', '')}")
    fm_lines.append(f"  page: {src.get('page', '')}")
    fm_lines.append(f"  bo_reference: {json.dumps(src.get('bo_reference', ''), ensure_ascii=False)}")
    if src.get("bo_url"):
        fm_lines.append(f"  bo_url: {src['bo_url']}")
    fm_lines.append(f"  page_image: {img_rel}")

    if c.get("prerequis"):
        fm_lines.append(f"prerequis:{render_yaml_list(c['prerequis'])}")
    if c.get("liens"):
        fm_lines.append(f"liens:{render_yaml_list(c['liens'])}")
    if c.get("tags"):
        fm_lines.append(f"tags:{render_yaml_list(c['tags'])}")
    em = c.get("extraction_meta", {})
    if em:
        fm_lines.append("extraction_meta:")
        for k, v in em.items():
            if isinstance(v, str):
                fm_lines.append(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
            elif isinstance(v, bool):
                fm_lines.append(f"  {k}: {'true' if v else 'false'}")
            else:
                fm_lines.append(f"  {k}: {v}")
    fm_lines.append("---")

    body = [f"\n# {c.get('intitule', c['code'])}\n"]
    body.append("## Formulation BO (citation exacte)\n")
    body.append(f"> {c.get('formulation_bo', '')}\n")

    if c.get("description_detaillee"):
        body.append("## Description détaillée\n")
        body.append(c["description_detaillee"] + "\n")

    if c.get("connaissances_associees"):
        body.append("## Connaissances associées\n")
        for k in c["connaissances_associees"]:
            body.append(f"- {k}")
        body.append("")

    if c.get("capacites_attendues"):
        body.append("## Capacités attendues\n")
        for k in c["capacites_attendues"]:
            body.append(f"- {k}")
        body.append("")

    if c.get("demonstrations_exigibles"):
        body.append("## Démonstrations exigibles\n")
        for d in c["demonstrations_exigibles"]:
            body.append(f"- {d}")
        body.append("")
    elif c["type"] == "demonstration":
        body.append("## Démonstrations exigibles\n\n*(corps de la démonstration à compléter)*\n")

    if c.get("algorithmes_attendus"):
        body.append("## Algorithmes / Programmes attendus\n")
        for a in c["algorithmes_attendus"]:
            body.append(f"### {a.get('titre', '')}\n")
            if a.get("description"):
                body.append(a["description"] + "\n")
            if a.get("code_python"):
                body.append("```python")
                body.append(a["code_python"])
                body.append("```\n")

    if c.get("exemples"):
        body.append("## Exemples / Applications\n")
        for e in c["exemples"]:
            body.append(f"- {e}")
        body.append("")

    if c.get("liens_transversaux"):
        body.append("## Liens transversaux\n")
        for l in c["liens_transversaux"]:
            body.append(f"- {l}")
        body.append("")

    # Source
    body.append("## Source\n")
    body.append(f"Programme officiel : *{src.get('pdf', '')}*, **{src.get('bo_reference', '')}**, page **{src.get('page', '')}**.\n")

    if img_rel:
        # Calcul du chemin relatif vers l'image depuis le MD final
        # JSON est à data/json/, MD est à data/markdown/{cycle}/{niveau}/{dom}/ → 4 ou 5 ../
        cycle = CYCLE_OF_NIVEAU.get(c["niveau"], "")
        # Profondeur : depuis data/markdown/{cycle}/{niveau}/{dom}/file.md vers data/ :
        #   cycle="lycee" (0 slash)            → 4 niveaux à remonter
        #   cycle="college/cycle4" (1 slash)   → 5 niveaux à remonter
        depth_md = cycle.count("/") + 4
        # img_rel est relatif depuis data/json/, donc :
        # data/json/ + img_rel = data/pages/...
        # Pour le MD : on remonte depuis data/markdown/.../ vers data/, puis on descend vers pages/
        # = ('../' * depth_md) + 'pages/{folder}/{file}'
        img_basename = Path(img_rel).name
        img_folder = Path(img_rel).parent.name  # ex: "2GT" depuis "../pages/2GT/page_005.png"
        if not img_folder or img_folder == "pages":
            img_folder = c["niveau"]
        img_md = ("../" * depth_md) + f"pages/{img_folder}/{img_basename}"
        body.append(f"![Page {src.get('page', '')} du BO {c['niveau']}]({img_md})\n")

    body.append("---")
    body.append(f"\n*Compétence extraite automatiquement le {em.get('date', '')}. Confiance : {em.get('confidence', '')}. Statut : {'vérifié' if em.get('verified') else 'non vérifié'}.*\n")

    return "\n".join(fm_lines) + "\n" + "\n".join(body)


def export_one(niveau_file: Path) -> int:
    data = json.load(open(niveau_file, encoding='utf-8'))
    niveau = data["meta"]["niveau"]
    cycle = CYCLE_OF_NIVEAU.get(niveau, "lycee")
    base = MD_DIR / cycle / niveau
    n = 0
    for dom, themes in data["competences_by_theme"].items():
        dom_dir = base / DOMAIN_KEBAB.get(dom, dom.lower())
        dom_dir.mkdir(parents=True, exist_ok=True)
        for theme, comps in themes.items():
            for c in comps:
                md_path = dom_dir / f"{c['code']}.md"
                md_path.write_text(render_md(c), encoding='utf-8', newline='\n')
                n += 1
    print(f"  {niveau} → {n} fichiers MD générés sous {base}")
    return n


def main():
    args = sys.argv[1:]
    target = None
    if "--niveau" in args:
        idx = args.index("--niveau")
        target = args[idx + 1] if idx + 1 < len(args) else None

    files = sorted(p for p in JSON_DIR.glob("*.json") if p.name not in ("schema.json", "all_flat.json"))
    if target:
        files = [f for f in files if f.stem.lower() == target.lower()]
    if not files:
        print("Aucun JSON niveau à exporter.")
        sys.exit(1)

    print(f"Export markdown miroir ({len(files)} niveau{'x' if len(files)>1 else ''})\n")
    total = 0
    for f in files:
        total += export_one(f)
    print(f"\nTotal : {total} fichiers MD exportés sous {MD_DIR}")


if __name__ == "__main__":
    main()
