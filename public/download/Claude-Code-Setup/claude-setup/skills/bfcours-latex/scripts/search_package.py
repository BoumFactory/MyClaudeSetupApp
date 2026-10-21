"""Recherche de commandes dans un package LaTeX installe.

Utilise kpsewhich pour localiser le fichier .sty du package,
puis cherche les definitions de commandes et environnements.

Usage:
    python search_package.py --package tcolorbox --query "raster"
    python search_package.py --package siunitx --query "unit"
    python search_package.py --package pgfplots --list-commands
    python search_package.py --package tcolorbox --list-envs
    python search_package.py --locate tcolorbox
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.stdout.reconfigure(encoding="utf-8")


def locate_package(package_name: str) -> list[Path]:
    """Localise tous les fichiers .sty d'un package via kpsewhich."""
    files = []

    # Chercher le .sty principal
    try:
        result = subprocess.run(
            ["kpsewhich", f"{package_name}.sty"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            files.append(Path(result.stdout.strip()))
    except Exception:
        pass

    # Chercher aussi les fichiers lies (package-xxx.sty, etc.)
    if files:
        parent = files[0].parent
        for sty in parent.glob(f"{package_name}*.sty"):
            if sty not in files:
                files.append(sty)

    return files


def read_sty_file(filepath: Path) -> str:
    """Lit un fichier .sty en gerant les encodages."""
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return filepath.read_text(encoding=enc)
        except (UnicodeDecodeError, PermissionError):
            continue
    return ""


def extract_definitions(content: str) -> list[dict]:
    """Extrait les definitions de commandes et environnements."""
    defs = []

    # \newcommand, \renewcommand, \providecommand, \DeclareRobustCommand
    for m in re.finditer(
        r"(\\(?:new|renew|provide|Declare\w*)command\*?)\s*\{?(\\[a-zA-Z@]+)\}?"
        r"(?:\s*\[(\d+)\])?\s*(?:\[([^\]]*)\])?\s*\{",
        content
    ):
        line = content[:m.start()].count("\n") + 1
        defs.append({
            "type": "command",
            "name": m.group(2),
            "declaration": m.group(1),
            "args": int(m.group(3)) if m.group(3) else 0,
            "default": m.group(4) if m.group(4) else None,
            "line": line,
        })

    # \NewDocumentCommand, \RenewDocumentCommand
    for m in re.finditer(
        r"(\\(?:New|Renew|Provide|Declare)DocumentCommand)\s*\{?(\\[a-zA-Z@]+)\}?"
        r"\s*\{([^}]*)\}",
        content
    ):
        line = content[:m.start()].count("\n") + 1
        defs.append({
            "type": "command",
            "name": m.group(2),
            "declaration": m.group(1),
            "args_spec": m.group(3),
            "line": line,
        })

    # \NewDocumentEnvironment, \newenvironment, etc.
    for m in re.finditer(
        r"(\\(?:New|Renew|Provide|Declare)Document(?:Environment))\s*\{(\w+)\}"
        r"\s*\{([^}]*)\}",
        content
    ):
        line = content[:m.start()].count("\n") + 1
        defs.append({
            "type": "environment",
            "name": m.group(2),
            "declaration": m.group(1),
            "args_spec": m.group(3),
            "line": line,
        })

    for m in re.finditer(
        r"(\\new(?:environment|tcolorbox))\s*\{(\w+)\}",
        content
    ):
        line = content[:m.start()].count("\n") + 1
        defs.append({
            "type": "environment",
            "name": m.group(2),
            "declaration": m.group(1),
            "line": line,
        })

    # \tcbset keys (tcolorbox specific)
    for m in re.finditer(r"\\tcbset\s*\{%?\s*\n?\s*([a-zA-Z][a-zA-Z0-9 _-]*)/.style", content):
        line = content[:m.start()].count("\n") + 1
        defs.append({
            "type": "style",
            "name": m.group(1),
            "declaration": "\\tcbset",
            "line": line,
        })

    return defs


def search_in_content(query: str, content: str, context_lines: int = 3) -> list[dict]:
    """Cherche un pattern dans le contenu avec contexte."""
    results = []
    lines = content.splitlines()
    query_lower = query.lower()

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            start = max(0, i - 1)
            end = min(len(lines), i + context_lines + 1)
            results.append({
                "line": i + 1,
                "match": line.strip(),
                "context": "\n".join(lines[start:end]),
            })

    return results


def main():
    parser = argparse.ArgumentParser(description="Recherche dans un package LaTeX installe")
    parser.add_argument("--package", "-p", required=True, help="Nom du package (ex: tcolorbox)")
    parser.add_argument("--query", "-q", help="Recherche dans le contenu du package")
    parser.add_argument("--list-commands", action="store_true", help="Lister les commandes definies")
    parser.add_argument("--list-envs", action="store_true", help="Lister les environnements definis")
    parser.add_argument("--locate", action="store_true", help="Localiser les fichiers du package")
    parser.add_argument("--context", "-c", type=int, default=3, help="Lignes de contexte (defaut: 3)")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Nombre max de resultats (defaut: 20)")
    args = parser.parse_args()

    # Localiser le package
    files = locate_package(args.package)
    if not files:
        print(json.dumps({
            "error": f"Package '{args.package}' non trouve. Verifier qu'il est installe.",
            "hint": f"Essayer: kpsewhich {args.package}.sty"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.locate:
        output = {
            "package": args.package,
            "files": [str(f) for f in files],
            "count": len(files),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    # Lire tous les fichiers
    all_content = {}
    for f in files:
        content = read_sty_file(f)
        if content:
            all_content[str(f)] = content

    if not all_content:
        print(json.dumps({"error": "Impossible de lire les fichiers du package"}, ensure_ascii=False))
        sys.exit(1)

    if args.list_commands or args.list_envs:
        all_defs = []
        for filepath, content in all_content.items():
            defs = extract_definitions(content)
            for d in defs:
                d["file"] = Path(filepath).name
            all_defs.extend(defs)

        if args.list_commands:
            filtered = [d for d in all_defs if d["type"] == "command"]
        elif args.list_envs:
            filtered = [d for d in all_defs if d["type"] in ("environment", "style")]
        else:
            filtered = all_defs

        output = {
            "package": args.package,
            "mode": "list_commands" if args.list_commands else "list_environments",
            "count": len(filtered),
            "definitions": filtered[:args.limit],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if args.query:
        all_results = []
        for filepath, content in all_content.items():
            results = search_in_content(args.query, content, args.context)
            for r in results:
                r["file"] = Path(filepath).name
            all_results.extend(results)

        output = {
            "package": args.package,
            "mode": "search",
            "query": args.query,
            "total_matches": len(all_results),
            "results": all_results[:args.limit],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    parser.error("Specifier --query, --list-commands, --list-envs ou --locate")


if __name__ == "__main__":
    main()
