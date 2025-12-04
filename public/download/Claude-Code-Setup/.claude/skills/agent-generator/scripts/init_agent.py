#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation pour créer la structure d'un nouvel agent.

Usage:
    python init_agent.py <agent-name> --output-dir <path>

Exemple:
    python init_agent.py mathalea-scraper --output-dir .claude/agents
"""

import argparse
import os
import sys
from pathlib import Path

# Template pour le fichier agent
AGENT_TEMPLATE = """---
name: {agent_name}
description: TODO - Description concise de l'objectif de l'agent (50-150 mots). Expliquer quand l'utiliser et ce qu'il produit.
model: sonnet
tools:
  - Read
  - Write
  - Bash
  - WebFetch
---

# Rôle

TODO - Décrire le rôle principal de l'agent. Exemple :
Tu es un agent spécialisé dans [DOMAINE]. Ta mission est de [OBJECTIF].

# Contexte

TODO - Fournir le contexte nécessaire pour comprendre la tâche.

# Capacités

Tu disposes des outils suivants :
- **Read** : Lire des fichiers locaux
- **Write** : Écrire des fichiers locaux
- **Bash** : Exécuter des commandes shell
- **WebFetch** : Récupérer du contenu web

TODO - Adapter la liste selon les outils définis dans le frontmatter.

# Processus de travail

TODO - Décrire étape par étape le workflow de l'agent.

## Étape 1 : [NOM_ETAPE]

[Instructions précises sur ce que l'agent doit faire]

## Étape 2 : [NOM_ETAPE]

[Instructions précises]

## Étape 3 : [NOM_ETAPE]

[Instructions précises]

# Format de sortie attendu

TODO - Décrire le format exact des résultats.

Exemple :
```json
{{
  "status": "success",
  "data": {{
    "resultat": "...",
    "metadata": {{}}
  }}
}}
```

# Gestion des erreurs

TODO - Décrire comment l'agent doit gérer les erreurs.

Si [CONDITION], alors :
1. [ACTION]
2. [FALLBACK]

En cas d'échec complet :
- Documenter l'erreur dans le rapport final
- Proposer des solutions alternatives
- Retourner un statut d'erreur clair

# Exemples

TODO - Ajouter des exemples concrets d'utilisation.

## Exemple 1 : [CAS_USAGE]

**Entrée** :
```
[Données d'entrée]
```

**Sortie attendue** :
```
[Résultat attendu]
```

# Notes et limitations

TODO - Documenter les limites connues de l'agent.

- Limitation 1
- Limitation 2
"""


def validate_agent_name(name: str) -> bool:
    """Valide le nom de l'agent (kebab-case recommandé)."""
    if not name:
        return False
    # Accepte kebab-case, snake_case, ou camelCase
    return all(c.isalnum() or c in '-_' for c in name)


def create_agent(agent_name: str, output_dir: str) -> None:
    """Crée la structure d'un nouvel agent."""

    # Validation
    if not validate_agent_name(agent_name):
        print(f"Erreur : Le nom '{agent_name}' n'est pas valide.")
        print("Utiliser kebab-case (ex: mathalea-scraper) recommandé.")
        sys.exit(1)

    # Créer le dossier de sortie si nécessaire
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Chemin du fichier agent
    agent_file = output_path / f"{agent_name}.md"

    # Vérifier si le fichier existe déjà
    if agent_file.exists():
        print(f"Erreur : L'agent '{agent_name}' existe déjà à {agent_file}")
        response = input("Voulez-vous l'écraser ? (y/N) : ")
        if response.lower() != 'y':
            print("Opération annulée.")
            sys.exit(0)

    # Générer le contenu à partir du template
    content = AGENT_TEMPLATE.format(agent_name=agent_name)

    # Écrire le fichier
    with open(agent_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Agent créé avec succès : {agent_file}")
    print(f"\nProchaines étapes :")
    print(f"1. Éditer {agent_file}")
    print(f"2. Remplacer tous les TODO par le contenu approprié")
    print(f"3. Adapter la liste des outils dans le frontmatter")
    print(f"4. Valider avec : python scripts/validate_agent.py {agent_file}")
    print(f"5. Tester l'agent via Task tool")


def main():
    parser = argparse.ArgumentParser(
        description="Initialiser un nouvel agent avec sa structure de base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python init_agent.py mathalea-scraper
  python init_agent.py log-analyzer --output-dir .claude/agents
        """
    )

    parser.add_argument(
        'agent_name',
        help='Nom de l\'agent (kebab-case recommandé, ex: mathalea-scraper)'
    )

    parser.add_argument(
        '--output-dir',
        default='.claude/agents',
        help='Dossier de destination (défaut: .claude/agents)'
    )

    args = parser.parse_args()

    create_agent(args.agent_name, args.output_dir)


if __name__ == '__main__':
    main()
