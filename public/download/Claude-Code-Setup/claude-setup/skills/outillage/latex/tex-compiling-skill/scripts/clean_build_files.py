#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour nettoyer les fichiers de build dans un répertoire.
Contient la logique complète de nettoyage sans dépendance au serveur MCP.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List


# Extensions par défaut à nettoyer
DEFAULT_AUX_EXTENSIONS = [
    ".aux", ".log", ".toc", ".lof", ".lot", ".out",
    ".bbl", ".blg", ".synctex.gz", ".fls", ".fdb_latexmk",
    ".nav", ".snm", ".vrb"  # Beamer
]


def clean_build_files(directory: Path, extensions: List[str]) -> List[str]:
    """
    Nettoie les fichiers de build dans un répertoire.

    Args:
        directory: Répertoire à nettoyer
        extensions: Liste d'extensions à supprimer

    Returns:
        Liste des fichiers supprimés
    """
    cleaned_files = []

    if not directory.exists():
        return cleaned_files

    # Parcourir tous les fichiers avec les extensions spécifiées
    for ext in extensions:
        pattern = f"*{ext}"
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                try:
                    file_path.unlink()
                    cleaned_files.append(str(file_path))
                except Exception as e:
                    print(f"⚠️  Impossible de supprimer {file_path.name}: {e}", file=sys.stderr)

    return cleaned_files


def main():
    parser = argparse.ArgumentParser(
        description="Nettoie les fichiers de build LaTeX dans un répertoire",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python clean_build_files.py --directory "./Sequence-Vecteurs"
  python clean_build_files.py --directory "." --extensions ".aux" ".log" ".out"

Usage pour l'agent:
  python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "chemin/vers/repertoire"
  python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "1. Cours/1ere_spe/Sequence-Second_degre/Cours_Partie2_second_degre"

Extensions par défaut:
  .aux, .log, .toc, .lof, .lot, .out, .bbl, .blg, .synctex.gz, .fls, .fdb_latexmk, .nav, .snm, .vrb
        """
    )

    parser.add_argument(
        "--directory",
        required=True,
        help="Répertoire à nettoyer"
    )

    parser.add_argument(
        "--extensions",
        nargs='*',
        help="Extensions à supprimer (optionnel, utilise les extensions par défaut si non spécifié)"
    )

    args = parser.parse_args()

    # Vérifier le répertoire
    dir_path = Path(args.directory)
    if not dir_path.exists():
        print(f"❌ Répertoire non trouvé: {args.directory}", file=sys.stderr)
        print(f"\n💡 Usage correct:", file=sys.stderr)
        print(f'   python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "chemin/vers/repertoire"', file=sys.stderr)
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"❌ Le chemin spécifié n'est pas un répertoire: {args.directory}", file=sys.stderr)
        sys.exit(1)

    # Déterminer les extensions
    if args.extensions:
        # S'assurer que chaque extension commence par un point
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions]
    else:
        extensions = DEFAULT_AUX_EXTENSIONS

    print(f"🧹 Nettoyage du répertoire: {args.directory}", file=sys.stderr)
    print(f"   Extensions: {', '.join(extensions)}", file=sys.stderr)

    # Nettoyer
    cleaned_files = clean_build_files(dir_path, extensions)

    # Affichage
    if cleaned_files:
        print(f"\n✅ {len(cleaned_files)} fichier(s) supprimé(s)", file=sys.stderr)
        print(f"\n📝 Fichiers supprimés:", file=sys.stderr)
        for f in cleaned_files[:10]:  # Limiter l'affichage à 10
            print(f"   - {Path(f).name}", file=sys.stderr)
        if len(cleaned_files) > 10:
            print(f"   ... et {len(cleaned_files) - 10} autres", file=sys.stderr)
    else:
        print(f"\nℹ️  Aucun fichier à supprimer", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(json.dumps({
        "status": "success",
        "directory": str(dir_path),
        "cleaned_files": cleaned_files,
        "count": len(cleaned_files)
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
