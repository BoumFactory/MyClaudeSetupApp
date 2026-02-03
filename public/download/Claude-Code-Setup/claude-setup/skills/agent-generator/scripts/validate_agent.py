#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation pour vérifier qu'un agent respecte les bonnes pratiques.

Usage:
    python validate_agent.py <path/to/agent.md>

Exemple:
    python validate_agent.py .claude/agents/mathalea-scraper.md
"""

import argparse
import sys
from pathlib import Path
import re

class AgentValidator:
    def __init__(self, agent_path: str):
        self.agent_path = Path(agent_path)
        self.errors = []
        self.warnings = []
        self.content = ""
        self.frontmatter = {}

    def validate(self) -> bool:
        """Valide l'agent et retourne True si valide."""
        if not self.agent_path.exists():
            self.errors.append(f"Fichier introuvable : {self.agent_path}")
            return False

        # Lire le contenu
        with open(self.agent_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

        # Vérifications
        self._validate_frontmatter()
        self._validate_structure()
        self._validate_description()
        self._validate_tools()
        self._validate_todos()

        return len(self.errors) == 0

    def _validate_frontmatter(self):
        """Vérifie le frontmatter YAML."""
        if not self.content.startswith('---'):
            self.errors.append("Le fichier doit commencer par '---' (frontmatter YAML)")
            return

        # Extraire le frontmatter
        parts = self.content.split('---', 2)
        if len(parts) < 3:
            self.errors.append("Frontmatter YAML mal formé (doit être entouré de '---')")
            return

        frontmatter_text = parts[1]

        # Parser le frontmatter (simple parsing)
        for line in frontmatter_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                self.frontmatter[key.strip()] = value.strip()

        # Vérifier les champs requis
        required_fields = ['name', 'description', 'model', 'tools']
        for field in required_fields:
            if field not in self.frontmatter:
                self.errors.append(f"Champ requis manquant dans le frontmatter : {field}")

        # Vérifier le modèle
        if 'model' in self.frontmatter:
            model = self.frontmatter['model']
            if model not in ['sonnet', 'haiku', 'opus']:
                self.errors.append(f"Modèle invalide : {model}. Utiliser 'sonnet', 'haiku', ou 'opus'")

    def _validate_structure(self):
        """Vérifie la présence des sections essentielles."""
        required_sections = [
            '# Rôle',
            '# Processus de travail',
            '# Format de sortie',
            '# Gestion des erreurs'
        ]

        for section in required_sections:
            if section not in self.content:
                self.errors.append(f"Section manquante : {section}")

        recommended_sections = ['# Exemples', '# Capacités']
        for section in recommended_sections:
            if section not in self.content:
                self.warnings.append(f"Section recommandée manquante : {section}")

    def _validate_description(self):
        """Vérifie la qualité de la description."""
        if 'description' not in self.frontmatter:
            return

        description = self.frontmatter['description']

        # Vérifier la longueur
        word_count = len(description.split())
        if word_count < 10:
            self.errors.append(f"Description trop courte ({word_count} mots). Minimum 10 mots recommandé.")
        elif word_count > 150:
            self.warnings.append(f"Description longue ({word_count} mots). 50-150 mots recommandé.")

        # Vérifier si c'est un placeholder
        if description.startswith('TODO'):
            self.errors.append("La description contient encore un TODO")

    def _validate_tools(self):
        """Vérifie la cohérence des outils listés."""
        if 'tools' not in self.frontmatter:
            return

        # Outils valides connus
        valid_tools = [
            'Read', 'Write', 'Edit', 'MultiEdit',
            'Bash', 'WebFetch', 'WebSearch',
            'Glob', 'Grep', 'LS',
            'Task', 'TodoWrite', 'Skill'
        ]

        # Note : les outils sont listés sur plusieurs lignes dans le YAML
        # On les extrait du contenu brut
        tools_section = re.search(r'tools:\s*\n((?:\s+-\s+\w+\s*\n?)+)', self.content)
        if tools_section:
            tools = re.findall(r'-\s+(\w+)', tools_section.group(1))

            for tool in tools:
                if tool not in valid_tools:
                    self.warnings.append(f"Outil non standard : {tool}. Vérifier s'il existe.")

            # Vérifier que les outils sont utilisés dans le texte
            for tool in tools:
                if tool not in self.content.split('---', 2)[2]:
                    self.warnings.append(f"L'outil '{tool}' est listé mais pas mentionné dans le corps")

    def _validate_todos(self):
        """Vérifie la présence de TODOs non résolus."""
        todo_count = self.content.count('TODO')
        if todo_count > 0:
            self.errors.append(f"{todo_count} TODO(s) non résolu(s) trouvé(s)")

    def print_report(self):
        """Affiche le rapport de validation."""
        print(f"\n{'='*60}")
        print(f"Rapport de validation : {self.agent_path.name}")
        print(f"{'='*60}\n")

        if self.errors:
            print("ERREURS :\n")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
            print()

        if self.warnings:
            print("AVERTISSEMENTS :\n")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
            print()

        if not self.errors and not self.warnings:
            print("Agent valide ! Aucune erreur ou avertissement.")
        elif not self.errors:
            print("Agent valide avec quelques avertissements.")
        else:
            print(f"Agent invalide : {len(self.errors)} erreur(s) à corriger.")

        print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Valider un fichier agent",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'agent_path',
        help='Chemin vers le fichier agent à valider (ex: .claude/agents/mathalea-scraper.md)'
    )

    args = parser.parse_args()

    validator = AgentValidator(args.agent_path)
    is_valid = validator.validate()
    validator.print_report()

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
