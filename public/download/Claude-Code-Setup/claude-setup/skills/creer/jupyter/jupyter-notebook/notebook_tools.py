#!/usr/bin/env python3
"""
Outils pour naviguer et valider les notebooks Jupyter.
Usage: python notebook_tools.py <commande> <notebook_path> [options]

Commandes:
  list      Liste toutes les cellules avec aperçu
  find      Recherche une cellule par contenu (option: --pattern "texte")
  validate  Valide la structure du notebook
"""

import json
import sys
import re
import argparse
from pathlib import Path

# Forcer UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def load_notebook(path: str) -> dict:
    """Charge un notebook JSON."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_cell_preview(cell: dict, max_length: int = 60) -> str:
    """Extrait un aperçu du contenu d'une cellule."""
    source = cell.get('source', [])
    if isinstance(source, list):
        text = ''.join(source)
    else:
        text = source

    # Nettoyer et tronquer
    text = text.strip().replace('\n', ' ')
    if len(text) > max_length:
        text = text[:max_length] + '...'
    return text


def get_cell_title(cell: dict) -> str:
    """Extrait le titre markdown si présent."""
    source = cell.get('source', [])
    if isinstance(source, list):
        text = ''.join(source)
    else:
        text = source

    # Chercher un titre markdown (# ou ##)
    match = re.search(r'^#{1,3}\s+(.+)$', text, re.MULTILINE)
    if match:
        return match.group(1).strip()[:50]
    return None


def list_cells(notebook_path: str) -> list:
    """Liste toutes les cellules avec leur index, type et aperçu."""
    nb = load_notebook(notebook_path)
    cells = nb.get('cells', [])

    result = []
    for i, cell in enumerate(cells):
        cell_type = cell.get('cell_type', 'unknown')
        cell_id = cell.get('id', f'cell-{i}')
        preview = get_cell_preview(cell)
        title = get_cell_title(cell)

        entry = {
            'index': i,
            'id': cell_id,
            'type': cell_type,
            'title': title,
            'preview': preview
        }
        result.append(entry)

    return result


def find_cells(notebook_path: str, pattern: str, case_sensitive: bool = False) -> list:
    """Trouve les cellules contenant un pattern."""
    nb = load_notebook(notebook_path)
    cells = nb.get('cells', [])

    flags = 0 if case_sensitive else re.IGNORECASE

    result = []
    for i, cell in enumerate(cells):
        source = cell.get('source', [])
        if isinstance(source, list):
            text = ''.join(source)
        else:
            text = source

        if re.search(pattern, text, flags):
            cell_type = cell.get('cell_type', 'unknown')
            cell_id = cell.get('id', f'cell-{i}')
            preview = get_cell_preview(cell, max_length=80)
            title = get_cell_title(cell)

            entry = {
                'index': i,
                'id': cell_id,
                'type': cell_type,
                'title': title,
                'preview': preview,
                'match': True
            }
            result.append(entry)

    return result


def validate_notebook(notebook_path: str) -> dict:
    """Valide la structure d'un notebook."""
    issues = []
    warnings = []

    # 1. Vérifier JSON valide
    try:
        nb = load_notebook(notebook_path)
    except json.JSONDecodeError as e:
        return {'valid': False, 'issues': [f'JSON invalide: {e}'], 'warnings': []}

    # 2. Vérifier structure de base
    if 'cells' not in nb:
        issues.append("Clé 'cells' manquante")
    if 'metadata' not in nb:
        warnings.append("Clé 'metadata' manquante")
    if 'nbformat' not in nb:
        warnings.append("Clé 'nbformat' manquante")

    cells = nb.get('cells', [])

    for i, cell in enumerate(cells):
        cell_id = cell.get('id', f'cell-{i}')
        cell_type = cell.get('cell_type', 'unknown')
        source = cell.get('source', [])

        if isinstance(source, list):
            text = ''.join(source)
        else:
            text = source

        # 3. Vérifier les balises HTML dans les cellules markdown
        if cell_type == 'markdown':
            # Vérifier <details> fermés
            open_details = text.count('<details')
            close_details = text.count('</details>')
            if open_details != close_details:
                issues.append(f"[{cell_id}] Balises <details> non équilibrées ({open_details} ouvertes, {close_details} fermées)")

            # Vérifier <summary> fermés
            open_summary = text.count('<summary')
            close_summary = text.count('</summary>')
            if open_summary != close_summary:
                issues.append(f"[{cell_id}] Balises <summary> non équilibrées")

            # Vérifier <div> fermés
            open_div = text.count('<div')
            close_div = text.count('</div>')
            if open_div != close_div:
                warnings.append(f"[{cell_id}] Balises <div> non équilibrées ({open_div} ouvertes, {close_div} fermées)")

        # 4. Vérifier si du HTML est dans une cellule code (erreur fréquente)
        if cell_type == 'code':
            if '<details>' in text or '<summary>' in text:
                issues.append(f"[{cell_id}] HTML détecté dans une cellule CODE (devrait être markdown)")

        # 5. Vérifier les cellules vides
        if not text.strip():
            warnings.append(f"[{cell_id}] Cellule vide")

    return {
        'valid': len(issues) == 0,
        'nb_cells': len(cells),
        'issues': issues,
        'warnings': warnings
    }


def format_list_output(cells: list) -> str:
    """Formate la sortie de list_cells pour l'affichage."""
    lines = []
    lines.append(f"{'IDX':<4} {'ID':<12} {'TYPE':<10} {'TITRE/APERCU'}")
    lines.append("-" * 80)

    for cell in cells:
        idx = cell['index']
        cell_id = cell['id'][:11]
        cell_type = cell['type'][:9]
        display = cell['title'] if cell['title'] else cell['preview']

        # Indicateur visuel du type (ASCII pour compatibilite Windows)
        icon = "[M]" if cell['type'] == 'markdown' else "[C]"

        lines.append(f"{idx:<4} {cell_id:<12} {icon} {cell_type:<8} {display}")

    return '\n'.join(lines)


def format_find_output(cells: list, pattern: str) -> str:
    """Formate la sortie de find_cells pour l'affichage."""
    if not cells:
        return f"Aucune cellule trouvee pour '{pattern}'"

    lines = []
    lines.append(f"Trouve {len(cells)} cellule(s) pour '{pattern}':")
    lines.append("-" * 80)

    for cell in cells:
        idx = cell['index']
        cell_id = cell['id']
        cell_type = cell['type']
        display = cell['title'] if cell['title'] else cell['preview']

        icon = "[M]" if cell['type'] == 'markdown' else "[C]"
        lines.append(f"[{idx}] {cell_id} {icon} {display}")

    return '\n'.join(lines)


def format_validate_output(result: dict) -> str:
    """Formate la sortie de validate_notebook pour l'affichage."""
    lines = []

    status = "[OK] VALIDE" if result['valid'] else "[!!] INVALIDE"
    lines.append(f"Statut: {status}")
    lines.append(f"Nombre de cellules: {result.get('nb_cells', '?')}")

    if result['issues']:
        lines.append(f"\n[ERREURS] ({len(result['issues'])}):")
        for issue in result['issues']:
            lines.append(f"  - {issue}")

    if result['warnings']:
        lines.append(f"\n[AVERTISSEMENTS] ({len(result['warnings'])}):")
        for warning in result['warnings']:
            lines.append(f"  - {warning}")

    if not result['issues'] and not result['warnings']:
        lines.append("\nAucun probleme detecte.")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Outils pour notebooks Jupyter')
    parser.add_argument('command', choices=['list', 'find', 'validate'],
                        help='Commande à exécuter')
    parser.add_argument('notebook', help='Chemin vers le notebook .ipynb')
    parser.add_argument('--pattern', '-p', help='Pattern à rechercher (pour find)')
    parser.add_argument('--json', '-j', action='store_true',
                        help='Sortie en JSON')

    args = parser.parse_args()

    # Vérifier que le fichier existe
    if not Path(args.notebook).exists():
        print(f"Erreur: Fichier non trouvé: {args.notebook}", file=sys.stderr)
        sys.exit(1)

    if args.command == 'list':
        result = list_cells(args.notebook)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_list_output(result))

    elif args.command == 'find':
        if not args.pattern:
            print("Erreur: --pattern requis pour la commande find", file=sys.stderr)
            sys.exit(1)
        result = find_cells(args.notebook, args.pattern)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_find_output(result, args.pattern))

    elif args.command == 'validate':
        result = validate_notebook(args.notebook)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_validate_output(result))


if __name__ == '__main__':
    main()
