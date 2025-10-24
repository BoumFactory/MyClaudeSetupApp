#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour corriger l'encodage de tous les fichiers d'un répertoire.
Utilise le serveur MCP encoding-fixer-server.
"""

import sys
import json
import argparse
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from encoding_fixer_server import fix_directory_encoding
except ImportError:
    print("❌ ERREUR: Impossible d'importer encoding_fixer_server", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Corrige l'encodage de tous les fichiers d'un répertoire",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python fix_directory_encoding.py --directory "./Sequence-Vecteurs"
  python fix_directory_encoding.py --directory "./cours" --pattern "*.tex" --recursive
  python fix_directory_encoding.py --directory "." --pattern "*.md" --no-backup
        """
    )

    parser.add_argument(
        "--directory",
        required=True,
        help="Répertoire à traiter"
    )

    parser.add_argument(
        "--pattern",
        default="*.tex",
        help="Pattern de fichiers (défaut: *.tex)"
    )

    parser.add_argument(
        "--backup",
        dest="create_backup",
        action="store_true",
        default=True,
        help="Créer des sauvegardes (défaut: activé)"
    )

    parser.add_argument(
        "--no-backup",
        dest="create_backup",
        action="store_false",
        help="Ne pas créer de sauvegardes"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        default=False,
        help="Traiter les sous-répertoires récursivement"
    )

    args = parser.parse_args()

    # Affichage humain sur stderr
    print(f"📁 Correction d'encodage du répertoire: {args.directory}", file=sys.stderr)
    print(f"   Pattern: {args.pattern}", file=sys.stderr)
    print(f"   Récursif: {'Oui' if args.recursive else 'Non'}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = fix_directory_encoding(
        directory_path=args.directory,
        pattern=args.pattern,
        create_backup=args.create_backup,
        recursive=args.recursive
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("success"):
        print(f"✅ Traitement terminé!", file=sys.stderr)
        print(f"   📊 Fichiers trouvés: {result.get('files_found', 0)}", file=sys.stderr)
        print(f"   ✓ Fichiers convertis: {result.get('files_converted', 0)}", file=sys.stderr)
        print(f"   ⏭️  Déjà UTF-8: {result.get('files_already_utf8', 0)}", file=sys.stderr)
        print(f"   ❌ Échecs: {result.get('files_failed', 0)}", file=sys.stderr)
    else:
        print(f"❌ Échec: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
