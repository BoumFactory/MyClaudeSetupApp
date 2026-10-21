# -*- coding: utf-8 -*-
"""Cree une nouvelle methode d'extraction et l'enregistre dans le registre.

    python new_method.py notebook --extensions .ipynb --label "Notebook Jupyter"
    python new_method.py podcast --url-patterns "spotify\\.com/episode" --label "Podcast Spotify"

Le squelette genere est volontairement executable des la creation (il produit un
workspace valide en signalant qu'il est incomplet), pour qu'on puisse verifier le
routage avant d'ecrire la logique d'extraction.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

METHODS_DIR = Path(__file__).resolve().parent / "methods"

TEMPLATE = '''# -*- coding: utf-8 -*-
"""Methode: {label}."""

from __future__ import annotations

from pathlib import Path

from base import ExtractionError, Workspace

NAME = "{name}"
VERSION = "0.1"
MATURITY = "stub"   # stub -> partial -> full, a mettre a jour en meme temps que le code
GAPS = [
    "Squelette non implemente: aucune extraction reelle.",
]


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    """Remplit le workspace et renvoie le manifeste partiel.

    A implementer:
      1. lire la ressource `source`
      2. ws.write_content(markdown)  -> le texte structure, avec des ancres
      3. ws.add_asset(chemin) / ws.register_asset(nom)  -> ce qui doit etre regarde
      4. ws.warn(...) pour ce qui n'a pas pu etre capte, ws.suggest(...) pour la suite
      5. renvoyer title / coverage / stats
    """
    raise ExtractionError(
        "Methode `{name}` non implementee. Ecrire l'extraction dans methods/m_{name}.py."
    )

    # Squelette de retour attendu:
    # return {{
    #     "title": Path(source).stem,
    #     "coverage": {{"text": "ok", "visual": "n/a", "structure": "partial"}},
    #     "stats": {{}},
    #     "extra": {{}},
    # }}
'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="identifiant de la methode (minuscules, sans espace)")
    ap.add_argument("--label", help="description lisible")
    ap.add_argument("--extensions", nargs="*", default=[], help="ex: .ipynb .rmd")
    ap.add_argument("--url-patterns", nargs="*", default=[], help="regex d'URL")
    ap.add_argument("--requires", nargs="*", default=[], help="dependances externes")
    ap.add_argument("--handles-directories", action="store_true")
    args = ap.parse_args()

    name = re.sub(r"[^a-z0-9_]+", "_", args.name.lower()).strip("_")
    label = args.label or f"Ressource {name}"
    module = f"m_{name}"
    target = METHODS_DIR / f"{module}.py"

    if target.exists():
        print(f"[!] {target} existe deja: l'ameliorer plutot que la recreer.")
        return 1

    target.write_text(TEMPLATE.format(name=name, label=label), encoding="utf-8")

    registry_path = METHODS_DIR / "registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entry = {
        "module": module,
        "label": label,
        "url_patterns": args.url_patterns,
        "extensions": [e if e.startswith(".") else f".{e}" for e in args.extensions],
        "requires": args.requires,
    }
    if args.handles_directories:
        entry["handles_directories"] = True

    # Insertion avant la methode fallback web, sinon toute URL serait captee avant elle.
    methods = registry["methods"]
    fallback = {k: v for k, v in methods.items() if v.get("fallback_for_urls")}
    others = {k: v for k, v in methods.items() if not v.get("fallback_for_urls")}
    others[name] = entry
    registry["methods"] = {**others, **fallback}
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "created",
        "module": str(target),
        "registered_as": name,
        "next_action": f"Implementer extract() dans {target.name}, puis passer MATURITY a `partial` ou `full` "
                       "et vider GAPS des lacunes corrigees.",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
