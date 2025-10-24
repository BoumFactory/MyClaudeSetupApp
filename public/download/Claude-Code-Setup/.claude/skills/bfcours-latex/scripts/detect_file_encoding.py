#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour détecter l'encodage d'un fichier LaTeX.
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
    from encoding_fixer_server import detect_file_encoding
except ImportError:
    print("❌ ERREUR: Impossible d'importer encoding_fixer_server", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Détecte l'encodage d'un fichier sans le modifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python detect_file_encoding.py --file "mon_cours.tex"
        """
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Chemin du fichier à analyser"
    )

    args = parser.parse_args()

    # Affichage humain sur stderr
    print(f"🔍 Détection d'encodage: {args.file}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = detect_file_encoding(file_path=args.file)
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("success"):
        encoding = result.get("detected_encoding", "inconnu")
        is_utf8 = result.get("is_utf8", False)
        needs_conversion = result.get("needs_conversion", False)
        stats = result.get("statistics", {})

        print(f"✅ Encodage détecté: {encoding}", file=sys.stderr)
        print(f"   {'✓' if is_utf8 else '✗'} UTF-8", file=sys.stderr)
        print(f"   {'⚠️' if needs_conversion else '✓'} {'Conversion nécessaire' if needs_conversion else 'Déjà UTF-8'}", file=sys.stderr)
        print(f"   📊 Statistiques:", file=sys.stderr)
        print(f"      - Caractères: {stats.get('total_chars', 0)}", file=sys.stderr)
        print(f"      - Lignes: {stats.get('lines', 0)}", file=sys.stderr)
        print(f"      - Caractères accentués: {stats.get('accented_chars', 0)}", file=sys.stderr)
    else:
        print(f"❌ Échec: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
