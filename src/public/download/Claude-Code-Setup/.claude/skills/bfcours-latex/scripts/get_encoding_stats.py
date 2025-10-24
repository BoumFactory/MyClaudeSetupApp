#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour obtenir les informations sur les encodages supportés.
Utilise le serveur MCP encoding-fixer-server.
"""

import sys
import json
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from encoding_fixer_server import get_encoding_stats
except ImportError:
    print("❌ ERREUR: Impossible d'importer encoding_fixer_server", file=sys.stderr)
    sys.exit(1)


def main():
    print("📋 Informations sur les encodages supportés", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = get_encoding_stats()
    result = json.loads(result_json)

    # Affichage humain sur stderr
    encodings = result.get("supported_encodings", [])
    print(f"\n✅ Encodages supportés ({len(encodings)}):", file=sys.stderr)
    for enc in encodings:
        print(f"   - {enc}", file=sys.stderr)

    print(f"\n🎯 Encodage de sortie par défaut: {result.get('default_output', 'utf-8')}", file=sys.stderr)
    print(f"\n📝 {result.get('description', '')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0)


if __name__ == "__main__":
    main()
