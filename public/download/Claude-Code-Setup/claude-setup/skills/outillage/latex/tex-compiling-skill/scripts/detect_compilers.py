#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour détecter les compilateurs LaTeX disponibles.
Utilise le serveur MCP latex-compiler-server.
"""

import sys
import json
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from latex_compiler_server import detect_compilers
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    print("🔍 Détection des compilateurs LaTeX", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = detect_compilers()
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        compilers = result.get("compilers", {})

        print(f"\n📋 Compilateurs détectés:\n", file=sys.stderr)

        for name, info in compilers.items():
            status = "✅" if info.get("available") else "❌"
            enabled = "🟢" if info.get("enabled") else "🔴"

            print(f"   {status} {name} {enabled}", file=sys.stderr)

            if info.get("version"):
                print(f"      {info['version']}", file=sys.stderr)

            if info.get("configured"):
                print(f"      Configuré: Oui", file=sys.stderr)

            print("", file=sys.stderr)

        print(f"💡 {result.get('recommendation', '')}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
