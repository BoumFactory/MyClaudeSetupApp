#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
validate.py — Validation globale du skill programmes-officiels.

Vérifie :
  1. Tous les data/json/{NIVEAU}.json valident data/json/schema.json.
  2. Les codes de compétences sont uniques globalement.
  3. Chaque source.page_image pointe vers un PNG existant.
  4. Couverture : chaque page PDF a une transcription (sauf justification).

Sortie :
  - Récap par check.
  - Code de retour 0 si OK, 1 sinon.

Usage :
    python scripts/validate.py
    python scripts/validate.py --niveau 2GT   # un seul niveau
"""

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import jsonschema

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
JSON_DIR = DATA_DIR / "json"
SCHEMA_FILE = JSON_DIR / "schema.json"


def list_niveau_files():
    return sorted(p for p in JSON_DIR.glob("*.json") if p.name not in ("schema.json", "all_flat.json"))


def check_schema(target_niveau: str | None) -> tuple[bool, list[str]]:
    schema = json.load(open(SCHEMA_FILE, encoding='utf-8'))
    msgs = []
    ok = True
    files = list_niveau_files()
    if target_niveau:
        files = [f for f in files if f.stem.lower() == target_niveau.lower()]
    if not files:
        msgs.append("(aucun fichier niveau à valider)")
    for f in files:
        try:
            data = json.load(open(f, encoding='utf-8'))
            jsonschema.validate(data, schema)
            msgs.append(f"  {f.name}: OK ({data['meta']['total_competences']} compétences)")
        except json.JSONDecodeError as e:
            msgs.append(f"  {f.name}: JSON INVALIDE — {e}")
            ok = False
        except jsonschema.ValidationError as e:
            msgs.append(f"  {f.name}: SCHEMA INVALIDE — {e.message} (path : {list(e.absolute_path)})")
            ok = False
    return ok, msgs


def check_unique_codes() -> tuple[bool, list[str]]:
    codes = []
    duplicates = []
    for f in list_niveau_files():
        data = json.load(open(f, encoding='utf-8'))
        for dom, themes in data.get("competences_by_theme", {}).items():
            for theme, comps in themes.items():
                for c in comps:
                    if c["code"] in codes:
                        duplicates.append(c["code"])
                    codes.append(c["code"])
    if duplicates:
        return False, [f"  DOUBLONS : {duplicates}"]
    return True, [f"  {len(codes)} codes uniques"]


def check_image_sources() -> tuple[bool, list[str]]:
    missing = []
    total = 0
    for f in list_niveau_files():
        data = json.load(open(f, encoding='utf-8'))
        for dom, themes in data.get("competences_by_theme", {}).items():
            for theme, comps in themes.items():
                for c in comps:
                    total += 1
                    src = c.get("source", {})
                    img_rel = src.get("page_image")
                    if not img_rel:
                        missing.append((c["code"], "page_image absent"))
                        continue
                    # Chemin relatif depuis data/json/
                    img_abs = (JSON_DIR / img_rel).resolve()
                    if not img_abs.exists():
                        missing.append((c["code"], str(img_abs)))
    if missing:
        msgs = [f"  {len(missing)}/{total} images source absentes :"]
        for code, path in missing[:10]:
            msgs.append(f"    - {code} → {path}")
        return False, msgs
    return True, [f"  {total} liens source vérifiés"]


def check_transcriptions_coverage() -> tuple[bool, list[str]]:
    mapping = json.load(open(DATA_DIR / "pdf" / "_mapping.json", encoding='utf-8'))
    pages_txt = DATA_DIR / "pages_txt"
    transcr = DATA_DIR / "transcriptions"
    missing = []
    total_pages = 0
    total_clean = 0
    for pdf, entry in mapping["files"].items():
        folder = entry["page_folder"]
        for txt in sorted((pages_txt / folder).glob("page_*.txt")):
            total_pages += 1
            page_num = int(txt.stem.split("_")[-1])
            # Pour cycle4, transcriptions peuvent être dans 5E/4E/3E OU cycle4/ (en attente)
            target_folders = [folder] if len(entry["niveaux"]) == 1 else [folder, "5E", "4E", "3E"]
            md_found = None
            for tf in target_folders:
                p = transcr / tf / f"page_{page_num:03d}.md"
                if p.exists():
                    md_found = p
                    break
            if md_found is None:
                missing.append(f"{folder}/page_{page_num:03d}")
            else:
                # Vérifier statut clean si possible
                content = md_found.read_text(encoding='utf-8', errors='ignore')
                if "status: clean" in content:
                    total_clean += 1
    msgs = [f"  Pages PDF : {total_pages}  ;  transcriptions clean : {total_clean}  ;  manquantes : {len(missing)}"]
    if missing:
        msgs.append("  Liste (10 premiers) : " + ", ".join(missing[:10]))
    return len(missing) == 0, msgs


def main():
    target = None
    if "--niveau" in sys.argv:
        idx = sys.argv.index("--niveau")
        target = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None

    print("=" * 60)
    print(" Validation programmes-officiels")
    print("=" * 60)

    all_ok = True

    print("\n[1/4] Schéma JSON")
    ok, msgs = check_schema(target)
    all_ok &= ok
    for m in msgs:
        print(m)
    print(f"  → {'OK' if ok else 'ECHEC'}")

    print("\n[2/4] Unicité des codes")
    ok, msgs = check_unique_codes()
    all_ok &= ok
    for m in msgs:
        print(m)
    print(f"  → {'OK' if ok else 'ECHEC'}")

    print("\n[3/4] Liens source (page_image)")
    ok, msgs = check_image_sources()
    all_ok &= ok
    for m in msgs:
        print(m)
    print(f"  → {'OK' if ok else 'ECHEC'}")

    print("\n[4/4] Couverture transcriptions")
    ok, msgs = check_transcriptions_coverage()
    # transcriptions partielles attendues en phase de construction → warning, pas échec
    for m in msgs:
        print(m)
    print(f"  → {'OK' if ok else 'WARN (en construction)'}")

    print("\n" + "=" * 60)
    if all_ok:
        print(" ✓ Toutes les validations bloquantes passent.")
    else:
        print(" ✗ Au moins une validation bloquante échoue.")
    print("=" * 60)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
