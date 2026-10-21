# -*- coding: utf-8 -*-
"""Routeur d'extraction de resource-to-skill.

Prend n'importe quelle ressource (fichier, dossier, URL), choisit la methode
adaptee, produit un workspace normalise et imprime un compte rendu JSON.

    python ingest.py <source> [--out DIR] [--visual auto|deep|off] [--lang fr]
    python ingest.py --list          # methodes disponibles, maturite, lacunes

Codes de sortie:
    0  extraction reussie
    3  aucune methode ne couvre ce type de ressource -> en creer une
    4  la methode existe mais a echoue -> la reparer ou l'ameliorer

Ces trois issues correspondent aux trois voies du skill: utiliser, creer,
ameliorer. Le JSON imprime porte toujours `status` et `next_action` pour que la
suite ne se devine pas.
"""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
import time
import traceback
import unicodedata
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
METHODS_DIR = SCRIPTS_DIR / "methods"
sys.path.insert(0, str(METHODS_DIR))

from base import ExtractionError, Workspace  # noqa: E402


def load_registry() -> dict:
    return json.loads((METHODS_DIR / "registry.json").read_text(encoding="utf-8"))


def slugify(value: str, fallback: str = "ressource") -> str:
    """Nom de dossier sans accent ni espace: les chemins accentues cassent les
    scripts Python sous Windows (codec cp1252)."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return (value or fallback)[:60]


def detect(source: str, registry: dict) -> tuple[str | None, str]:
    """Renvoie (nom_de_methode, type_detecte)."""
    methods = registry["methods"]
    is_url = bool(re.match(r"^https?://", source, re.I))

    if is_url:
        for name, spec in methods.items():
            for pattern in spec.get("url_patterns", []):
                if spec.get("fallback_for_urls"):
                    continue
                if re.search(pattern, source, re.I):
                    return name, name
        for name, spec in methods.items():
            if spec.get("fallback_for_urls"):
                return name, "web"
        return None, "url"

    path = Path(source)
    if not path.exists():
        return None, "introuvable"
    if path.is_dir():
        for name, spec in methods.items():
            if spec.get("handles_directories"):
                return name, name
        return None, "dossier"

    suffix = path.suffix.lower()
    for name, spec in methods.items():
        if suffix in [s.lower() for s in spec.get("extensions", [])]:
            return name, name
    return None, f"fichier {suffix or 'sans extension'}"


def method_info(spec: dict) -> dict:
    """Lit la maturite reelle dans le module (source de verite)."""
    try:
        mod = importlib.import_module(spec["module"])
        return {
            "version": getattr(mod, "VERSION", "?"),
            "maturity": getattr(mod, "MATURITY", "?"),
            "gaps": list(getattr(mod, "GAPS", [])),
        }
    except Exception as exc:
        return {"version": "?", "maturity": "casse", "gaps": [f"import impossible: {exc}"]}


def cmd_list(registry: dict) -> int:
    out = []
    for name, spec in registry["methods"].items():
        info = method_info(spec)
        out.append(
            {
                "name": name,
                "label": spec["label"],
                "maturity": info["maturity"],
                "version": info["version"],
                "gaps": info["gaps"],
                "extensions": spec.get("extensions", []),
                "url_patterns": spec.get("url_patterns", []),
            }
        )
    print(json.dumps({"methods": out}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Extrait une ressource vers un workspace normalise.")
    ap.add_argument("source", nargs="?", help="fichier, dossier ou URL")
    ap.add_argument("--out", help="dossier de sortie (defaut: ./.rts/<slug>)")
    ap.add_argument("--visual", choices=["auto", "deep", "off"], default="auto",
                    help="densite d'echantillonnage des images (defaut: auto)")
    ap.add_argument("--lang", help="langue preferee pour les sous-titres / la transcription")
    ap.add_argument("--method", help="forcer une methode du registre")
    ap.add_argument("--list", action="store_true", help="lister les methodes disponibles")
    args = ap.parse_args()

    registry = load_registry()
    if args.list:
        return cmd_list(registry)
    if not args.source:
        ap.error("indiquer une source, ou utiliser --list")

    source = args.source
    name, detected = (args.method, args.method) if args.method else detect(source, registry)

    if not name or name not in registry["methods"]:
        print(json.dumps({
            "status": "no_method",
            "source": source,
            "detected_type": detected,
            "available": sorted(registry["methods"]),
            "next_action": (
                "Aucune methode ne couvre ce type. Creer une methode avec "
                "`python scripts/new_method.py <nom>` puis l'enregistrer dans "
                "methods/registry.json (voir references/extraction-methods.md)."
            ),
        }, ensure_ascii=False, indent=2))
        return 3

    spec = registry["methods"][name]
    info = method_info(spec)

    label = slugify(Path(source).stem if not re.match(r"^https?://", source) else re.sub(r"^https?://", "", source))
    out_dir = Path(args.out) if args.out else Path.cwd() / ".rts" / label
    ws = Workspace(out_dir)

    started = time.time()
    manifest = {
        "schema": "resource-to-skill/extraction@1",
        "source": source,
        "resource_type": detected,
        "method": {"name": name, "label": spec["label"], **info},
        "options": {"visual": args.visual, "lang": args.lang},
    }

    try:
        mod = importlib.import_module(spec["module"])
        result = mod.extract(source, ws, {"visual": args.visual, "lang": args.lang}) or {}
    except ExtractionError as exc:
        manifest.update({"status": "method_failed", "error": str(exc),
                         "next_action": "Corriger ou completer la methode (references/extraction-methods.md), puis relancer."})
        (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 4
    except Exception as exc:  # bug inattendu: la trace part dans le workspace, pas dans le terminal
        (out_dir / "traceback.txt").write_text(traceback.format_exc(), encoding="utf-8")
        manifest.update({"status": "method_failed", "error": f"{type(exc).__name__}: {exc}",
                         "traceback": "traceback.txt",
                         "next_action": "Bug dans la methode: lire traceback.txt, corriger le module, relancer."})
        (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 4

    manifest.update({
        "status": "ok",
        "title": result.get("title", label),
        "coverage": result.get("coverage", {}),
        "stats": result.get("stats", {}),
        "extra": result.get("extra", {}),
        "artifacts": {
            "workspace": str(out_dir),
            "content": "content.md",
            "assets": ws.assets,
            "raw": ws.raw,
        },
        "warnings": ws.warnings,
        "next_steps": ws.next_steps,
        "elapsed_s": round(time.time() - started, 1),
    })

    # Une couverture partielle n'est pas un echec: c'est le signal qu'il faudra
    # soit completer a la main, soit ameliorer la methode pour la prochaine fois.
    weak = [dim for dim, val in manifest["coverage"].items() if val in ("partial", "missing")]
    if weak:
        manifest["next_action"] = (
            f"Couverture faible sur: {', '.join(weak)}. Completer par lecture directe, "
            "et si la lacune est structurelle, ameliorer la methode (voir GAPS)."
        )
    else:
        manifest["next_action"] = "Lire content.md, puis les planches contact / images signalees."

    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
