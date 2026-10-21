"""Recherche de commandes et environnements dans le package bfcours.

Cherche dans bfcours-conventions.md par nom de commande ou mot-cle.
Retourne les sections pertinentes avec contexte.

Usage:
    python search_command.py --query "\\acc"
    python search_command.py --query "tableau"
    python search_command.py --exact "\\encadrer"
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

CONVENTIONS_FILE = Path(__file__).parent.parent / "references" / "bfcours-conventions.md"


def load_sections(filepath: Path) -> list[dict]:
    """Parse le fichier conventions en sections (par ## ou ###)."""
    if not filepath.exists():
        return []

    text = filepath.read_text(encoding="utf-8")
    sections = []
    current = {"title": "", "level": 0, "content": "", "line": 0}

    for i, line in enumerate(text.splitlines(), 1):
        heading = re.match(r"^(#{2,4})\s+(.+)$", line)
        if heading:
            if current["content"].strip():
                sections.append(current)
            current = {
                "title": heading.group(2),
                "level": len(heading.group(1)),
                "content": "",
                "line": i,
            }
        else:
            current["content"] += line + "\n"

    if current["content"].strip():
        sections.append(current)

    return sections


def extract_commands(section: dict) -> list[str]:
    """Extrait les commandes LaTeX mentionnees dans une section."""
    commands = re.findall(r"\\[a-zA-Z]+", section["content"])
    envs = re.findall(r"\\begin\{(\w+)\}", section["content"])
    return list(set(commands)) + [f"env:{e}" for e in set(envs)]


def fuzzy_match(query: str, text: str) -> float:
    """Score de correspondance simple entre query et texte."""
    query_lower = query.lower().replace("\\", "")
    text_lower = text.lower()

    # Match exact = score max
    if query.lower() in text_lower:
        return 1.0

    # Match sans backslash
    if query_lower in text_lower:
        return 0.9

    # Match partiel par mots
    words = query_lower.split()
    matched = sum(1 for w in words if w in text_lower)
    if words:
        return 0.5 * (matched / len(words))

    return 0.0


def search_fuzzy(query: str, sections: list[dict], limit: int = 5) -> list[dict]:
    """Recherche floue dans les sections."""
    results = []
    for section in sections:
        searchable = section["title"] + " " + section["content"]
        score = fuzzy_match(query, searchable)
        if score > 0.1:
            results.append({
                "title": section["title"],
                "score": round(score, 2),
                "line": section["line"],
                "commands": extract_commands(section),
                "excerpt": section["content"].strip()[:300],
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def search_exact(command: str, sections: list[dict]) -> list[dict]:
    """Recherche exacte d'une commande specifique."""
    results = []
    cmd_clean = command.replace("\\", "")

    for section in sections:
        content = section["content"]
        # Cherche la commande exacte
        if re.search(rf"\\{re.escape(cmd_clean)}(?:\b|\{{|$)", content):
            results.append({
                "title": section["title"],
                "line": section["line"],
                "content": content.strip(),
            })

    return results


def main():
    parser = argparse.ArgumentParser(description="Recherche dans le package bfcours")
    parser.add_argument("--query", "-q", help="Recherche floue par mot-cle")
    parser.add_argument("--exact", "-e", help="Recherche exacte d'une commande")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Nombre max de resultats")
    args = parser.parse_args()

    if not args.query and not args.exact:
        parser.error("Specifier --query ou --exact")

    sections = load_sections(CONVENTIONS_FILE)
    if not sections:
        print(json.dumps({"error": f"Fichier non trouve: {CONVENTIONS_FILE}"}, ensure_ascii=False))
        sys.exit(1)

    if args.exact:
        results = search_exact(args.exact, sections)
        output = {
            "mode": "exact",
            "query": args.exact,
            "results_count": len(results),
            "results": results,
        }
    else:
        results = search_fuzzy(args.query, sections, args.limit)
        output = {
            "mode": "fuzzy",
            "query": args.query,
            "results_count": len(results),
            "results": results,
        }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
