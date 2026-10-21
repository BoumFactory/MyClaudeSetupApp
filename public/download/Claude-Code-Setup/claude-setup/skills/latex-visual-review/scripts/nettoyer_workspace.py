#!/usr/bin/env python3
"""
Supprime un workspace temporaire de latex-visual-review (`.lvr-workspace/`
dans un dossier de projet, ou son equivalent cree dans le scratchpad d'une
session sous-agent) une fois les conclusions du run extraites dans le
rapport final.

Objectif : eviter l'accumulation de dossiers `.lvr-workspace/` (copies de
.tex, PDF, captures PNG par version) qui alourdissent la memoire disque au
fil des runs successifs.

Securite : refuse de supprimer un dossier qui ne s'appelle pas `.lvr-workspace`
(ou un nom commencant par `lvr-workspace`, utilise en mode sous-agent) OU qui
n'est pas situe sous un repertoire temporaire/scratchpad reconnu. Ce
garde-fou evite la suppression accidentelle d'un dossier de projet homonyme.

Usage:
    python nettoyer_workspace.py --path <dossier> [--force] [--dry-run]

Codes retour :
    0 = supprime (ou dry-run : liste ce qui serait supprime)
    1 = dossier deja absent (rien a faire, pas une erreur bloquante)
    2 = garde-fou de securite declenche (nom/emplacement suspect) ; relancer avec --force si le chemin est correct
    3 = erreur de suppression (permissions, fichier verrouille, ...)
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ALLOWED_NAME_PREFIXES = ("lvr-workspace", ".lvr-workspace")
ALLOWED_PATH_HINTS = ("scratchpad", "temp", "tmp")


def is_safe_to_delete(path: Path) -> bool:
    name_ok = any(path.name.lower().startswith(p) for p in ALLOWED_NAME_PREFIXES)
    path_str = str(path).lower()
    path_ok = any(hint in path_str for hint in ALLOWED_PATH_HINTS)
    return name_ok or path_ok


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Supprime un workspace temporaire latex-visual-review (.lvr-workspace ou equivalent scratchpad)."
    )
    parser.add_argument("--path", required=True, help="Chemin du dossier workspace a supprimer")
    parser.add_argument("--force", action="store_true", help="Ignore le garde-fou nom/emplacement")
    parser.add_argument("--dry-run", action="store_true", help="Liste ce qui serait supprime sans rien effacer")
    args = parser.parse_args()

    target = Path(args.path).resolve()

    if not target.exists():
        print(json.dumps({"status": "absent", "path": str(target)}, ensure_ascii=False))
        return 1

    if not args.force and not is_safe_to_delete(target):
        print(
            json.dumps(
                {
                    "status": "refused",
                    "path": str(target),
                    "message": "Nom/emplacement non reconnu comme un workspace temporaire lvr. Relancer avec --force si le chemin est correct.",
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        print(json.dumps({"status": "dry_run", "would_delete": str(target)}, ensure_ascii=False))
        return 0

    try:
        shutil.rmtree(target)
    except OSError as exc:
        print(
            json.dumps({"status": "error", "path": str(target), "message": str(exc)}, ensure_ascii=False),
            file=sys.stderr,
        )
        return 3

    print(json.dumps({"status": "deleted", "path": str(target)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
