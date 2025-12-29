#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook de logging des erreurs d'agents

Ce script est exécuté après chaque appel au Task tool (agents)
Il analyse le résultat et logue les erreurs dans un fichier dédié
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path


def get_project_dir():
    """Récupère le répertoire du projet"""
    return os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())


def get_tool_output():
    """Récupère la sortie du tool depuis l'environnement"""
    return os.environ.get('CLAUDE_TOOL_OUTPUT', '')


def detect_errors(tool_output):
    """Parse le résultat du tool pour détecter les erreurs"""
    errors = []

    # Détection d'erreurs LaTeX
    latex_errors = re.findall(r'LaTeX Error:.*?(?=\n|$)', tool_output)
    for err in latex_errors:
        errors.append({
            'type': 'latex',
            'message': err,
            'severity': 'error'
        })

    # Détection d'erreurs de compilation génériques
    compile_errors = re.findall(r'(?:Error|ERROR):.*?(?=\n|$)', tool_output, re.IGNORECASE)
    for err in compile_errors:
        if err not in [e['message'] for e in errors]:  # Éviter les doublons
            errors.append({
                'type': 'compilation',
                'message': err,
                'severity': 'error'
            })

    # Détection de warnings
    warnings = re.findall(r'(?:Warning|WARNING):.*?(?=\n|$)', tool_output, re.IGNORECASE)
    for warn in warnings:
        errors.append({
            'type': 'warning',
            'message': warn,
            'severity': 'warning'
        })

    # Détection d'erreurs Bash
    bash_patterns = [
        r'command not found',
        r'No such file or directory',
        r'Permission denied',
        r'syntax error'
    ]

    for pattern in bash_patterns:
        if re.search(pattern, tool_output, re.IGNORECASE):
            match = re.search(f'({pattern}).*?(?=\n|$)', tool_output, re.IGNORECASE)
            if match:
                errors.append({
                    'type': 'bash',
                    'message': match.group(0),
                    'severity': 'error'
                })

    # Détection d'erreurs d'outils (Edit, Write, Read, etc.)
    if '<error>' in tool_output:
        error_match = re.search(r'<error>(.*?)</error>', tool_output, re.DOTALL)
        if error_match:
            errors.append({
                'type': 'tool-error',
                'message': error_match.group(1)[:200],
                'severity': 'error',
                'details': tool_output[:500]
            })

    # Détection d'échecs d'agents
    if any(keyword in tool_output for keyword in ['Failed', 'ERREUR', 'Échec', 'Erreur']):
        errors.append({
            'type': 'agent-failure',
            'message': 'Agent returned failure status',
            'severity': 'error',
            'details': tool_output[:500]
        })

    # Détection d'erreurs Python (Traceback)
    python_errors = re.findall(r'Traceback.*?(?:\n(?!  )|\Z)', tool_output, re.DOTALL)
    for err in python_errors:
        errors.append({
            'type': 'python',
            'message': err[:200],
            'severity': 'error'
        })

    # Détection d'erreurs Python (Exception sans Traceback)
    exception_errors = re.findall(r'(\w+Error|Exception):.*?(?=\n|$)', tool_output)
    for err in exception_errors:
        if err not in [e['message'] for e in errors]:
            errors.append({
                'type': 'python',
                'message': err,
                'severity': 'error'
            })

    # Détection de packages manquants
    pkg_patterns = [
        r'package.*not found',
        r'module.*not found',
        r'cannot find module',
        r'No module named'
    ]

    for pattern in pkg_patterns:
        match = re.search(pattern, tool_output, re.IGNORECASE)
        if match:
            pkg_error = re.search(f'({pattern}).*?(?=\n|$)', tool_output, re.IGNORECASE)
            if pkg_error:
                errors.append({
                    'type': 'missing-dependency',
                    'message': pkg_error.group(0),
                    'severity': 'error'
                })

    return errors


def log_errors(errors, hook_data=None):
    """Logue les erreurs dans le fichier de log"""
    if not errors:
        return

    hook_data = hook_data or {}
    project_dir = get_project_dir()
    log_file = Path(project_dir) / '.claude' / 'hooks' / 'agent-errors.log'

    # Créer le dossier .claude/hooks si nécessaire
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Préparer l'entrée de log
    timestamp = datetime.now().isoformat()
    tool_output = get_tool_output()

    log_entry = {
        'timestamp': timestamp,
        'errors': errors,
        'tool': hook_data.get('tool', 'unknown'),
        'context': {
            'toolOutput': tool_output[:1000],  # Limiter la taille
            'projectDir': project_dir,
            'filePaths': os.environ.get('CLAUDE_FILE_PATHS', '')
        }
    }

    # Ajouter au fichier de log (format JSONL)
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

        print(f"[Hook] {len(errors)} erreur(s) de {log_entry['tool']} loguée(s) dans {log_file}",
              file=sys.stderr)
    except Exception as e:
        print(f"[Hook Error] Impossible d'écrire dans le log: {e}", file=sys.stderr)


def main():
    """Point d'entrée principal"""
    try:
        # Lire stdin (données JSON du hook) si disponibles
        hook_data = {}

        if not sys.stdin.isatty():
            try:
                stdin_content = sys.stdin.read()
                if stdin_content.strip():
                    hook_data = json.loads(stdin_content)
            except (json.JSONDecodeError, Exception):
                # Ignorer les erreurs de parsing, continuer sans les données du hook
                pass

        # Détecter les erreurs dans la sortie du tool
        tool_output = get_tool_output()
        errors = detect_errors(tool_output)

        # Logger les erreurs si trouvées
        if errors:
            log_errors(errors, hook_data)

        # Toujours retourner succès pour ne pas bloquer
        sys.exit(0)

    except Exception as e:
        print(f"[Hook Error] {e}", file=sys.stderr)
        sys.exit(0)  # Ne pas bloquer l'exécution


if __name__ == '__main__':
    main()
