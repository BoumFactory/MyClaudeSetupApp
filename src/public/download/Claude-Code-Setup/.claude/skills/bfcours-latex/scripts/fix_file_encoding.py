#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour corriger l'encodage d'un fichier LaTeX.
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
    from encoding_fixer_server import fix_file_encoding
except ImportError:
    print("❌ ERREUR: Impossible d'importer encoding_fixer_server", file=sys.stderr)
    print(f"   Vérifiez que le fichier existe dans: {MCP_SERVER_PATH}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Corrige l'encodage d'un fichier LaTeX vers UTF-8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python fix_file_encoding.py --file "mon_cours.tex"
  python fix_file_encoding.py --file "devoir.tex" --no-backup
  python fix_file_encoding.py --file "enonce.tex" --output "enonce_utf8.tex"
        """
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Chemin du fichier à corriger"
    )

    parser.add_argument(
        "--output",
        default="",
        help="Chemin du fichier de sortie (vide = écrase l'original)"
    )

    parser.add_argument(
        "--backup",
        dest="create_backup",
        action="store_true",
        default=True,
        help="Créer une sauvegarde (défaut: activé)"
    )

    parser.add_argument(
        "--no-backup",
        dest="create_backup",
        action="store_false",
        help="Ne pas créer de sauvegarde"
    )

    args = parser.parse_args()

    # Affichage humain sur stderr
    print(f"🔧 Correction d'encodage: {args.file}", file=sys.stderr)
    if args.create_backup:
        print("💾 Création d'une sauvegarde activée", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = fix_file_encoding(
        file_path=args.file,
        output_path=args.output,
        create_backup=args.create_backup
    )

    # Parser le résultat
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("success"):
        print(f"✅ Succès!", file=sys.stderr)
        print(f"   Encodage d'origine: {result.get('original_encoding', 'inconnu')}", file=sys.stderr)
        print(f"   Nouveau fichier: {result.get('file', '')}", file=sys.stderr)
        if result.get("backup_created"):
            print(f"   Backup: {result.get('backup_path', '')}", file=sys.stderr)
    else:
        print(f"❌ Échec: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent sur stdout
    print(result_json)

    # Code de retour
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
