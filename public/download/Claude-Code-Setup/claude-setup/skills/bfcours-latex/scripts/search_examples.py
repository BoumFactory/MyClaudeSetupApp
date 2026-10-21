"""Recherche de patterns dans les exemples usecase bfcours.

Cherche dans les fichiers .tex du dossier assets/usecase/ pour trouver
des exemples reels d'utilisation d'environnements, commandes, etc.

Usage:
    python search_examples.py --pattern "\\begin{EXO}"
    python search_examples.py --pattern "\\tcbtab" --context 10
    python search_examples.py --pattern "\\exocorrection" --context 20
    python search_examples.py --list-envs
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

USECASE_DIR = Path(__file__).parent.parent / "assets" / "usecase"


def search_pattern(pattern: str, context: int = 5) -> list[dict]:
    """Cherche un pattern dans tous les fichiers .tex des usecases."""
    if not USECASE_DIR.exists():
        return []

    results = []
    for tex_file in sorted(USECASE_DIR.rglob("*.tex")):
        if not tex_file.is_file():
            continue
        try:
            lines = tex_file.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, PermissionError):
            try:
                lines = tex_file.read_text(encoding="latin-1").splitlines()
            except Exception:
                continue

        for i, line in enumerate(lines):
            if re.search(re.escape(pattern), line):
                start = max(0, i - 1)
                end = min(len(lines), i + context + 1)
                excerpt = "\n".join(lines[start:end])

                rel_path = tex_file.relative_to(USECASE_DIR)
                results.append({
                    "file": str(rel_path),
                    "line": i + 1,
                    "match": line.strip(),
                    "excerpt": excerpt,
                })

    return results


def list_environments() -> dict:
    """Liste tous les environnements bfcours utilises dans les exemples."""
    if not USECASE_DIR.exists():
        return {}

    env_counts: dict[str, int] = {}
    for tex_file in USECASE_DIR.rglob("*.tex"):
        if not tex_file.is_file():
            continue
        try:
            content = tex_file.read_text(encoding="utf-8")
        except Exception:
            continue

        envs = re.findall(r"\\begin\{(\w+)\}", content)
        for env in envs:
            env_counts[env] = env_counts.get(env, 0) + 1

    return dict(sorted(env_counts.items(), key=lambda x: x[1], reverse=True))


def main():
    parser = argparse.ArgumentParser(description="Recherche dans les exemples bfcours")
    parser.add_argument("--pattern", "-p", help="Pattern LaTeX a chercher")
    parser.add_argument("--context", "-c", type=int, default=5, help="Lignes de contexte apres le match")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Nombre max de resultats")
    parser.add_argument("--list-envs", action="store_true", help="Lister tous les environnements utilises")
    args = parser.parse_args()

    if not args.pattern and not args.list_envs:
        parser.error("Specifier --pattern ou --list-envs")

    if args.list_envs:
        envs = list_environments()
        output = {
            "mode": "list_environments",
            "total_unique": len(envs),
            "environments": envs,
        }
    else:
        results = search_pattern(args.pattern, args.context)
        output = {
            "mode": "search",
            "pattern": args.pattern,
            "results_count": len(results),
            "results": results[:args.limit],
            "total_matches": len(results),
        }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
