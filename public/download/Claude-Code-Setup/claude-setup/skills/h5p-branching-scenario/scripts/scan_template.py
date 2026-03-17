#!/usr/bin/env python3
"""
Scanner de template Branching Scenario.

Scanne un template JSON pour trouver tous les marqueurs __TODO__,
detecter les champs vides/manquants, et generer un rapport structure
avec des questions challenge pour guider le remplissage.

Usage:
  python scan_template.py --input template.json [--output report.json] [--human]
"""
import json
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple


# ============================================================================
# SCANNING
# ============================================================================

def scan_todos(data: Any, path: str = "") -> List[Dict]:
    """Parcours recursif du JSON pour trouver tous les __TODO__*."""
    findings = []

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, str) and '__TODO' in value:
                findings.append({
                    'path': current_path,
                    'marker': value,
                    'type': 'todo'
                })
            elif isinstance(value, str) and value.strip() == '':
                findings.append({
                    'path': current_path,
                    'marker': '(empty)',
                    'type': 'empty'
                })
            else:
                findings.extend(scan_todos(value, current_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]"
            findings.extend(scan_todos(item, current_path))

    return findings


def detect_missing_fields(data: Dict) -> List[Dict]:
    """Detecte les champs manquants ou incomplets."""
    issues = []
    nodes = data.get('nodes', [])

    for i, node in enumerate(nodes):
        tag = f"nodes[{i}]"
        ntype = node.get('type', 'text')

        # Feedback manquant sur noeuds terminaux
        next_id = node.get('nextContentId', 0)
        if next_id == -1:
            if not node.get('feedback'):
                issues.append({
                    'path': f"{tag}.feedback",
                    'marker': '(missing)',
                    'type': 'missing_field',
                    'detail': f"Noeud terminal sans feedback/score"
                })
            elif 'score' not in node.get('feedback', {}):
                issues.append({
                    'path': f"{tag}.feedback.score",
                    'marker': '(missing)',
                    'type': 'missing_field',
                    'detail': f"Feedback sans score"
                })

        # Alternatives de branching_question
        if ntype == 'branching_question':
            for j, alt in enumerate(node.get('alternatives', [])):
                if not alt.get('feedback'):
                    issues.append({
                        'path': f"{tag}.alternatives[{j}].feedback",
                        'marker': '(missing)',
                        'type': 'missing_field',
                        'detail': f"Alternative sans feedback"
                    })

        # Slides vides dans course_presentation
        if ntype == 'course_presentation':
            slides = node.get('slides', [])
            if not slides:
                issues.append({
                    'path': f"{tag}.slides",
                    'marker': '(empty)',
                    'type': 'missing_field',
                    'detail': f"CoursePresentation sans slides"
                })

    # EndScreens
    scoring = data.get('scoring', 'no-score')
    if scoring == 'static-end-score':
        end_screens = data.get('endScreens', [])
        if not end_screens:
            issues.append({
                'path': 'endScreens',
                'marker': '(missing)',
                'type': 'missing_field',
                'detail': 'static-end-score sans endScreens'
            })

    return issues


# ============================================================================
# GROUPEMENT PAR NOEUD
# ============================================================================

def group_by_node(findings: List[Dict], data: Dict) -> Dict[str, Dict]:
    """Groupe les findings par noeud avec contexte."""
    nodes = data.get('nodes', [])
    groups = {}

    # Groupe "racine" pour les champs hors nodes
    root_items = [f for f in findings if not f['path'].startswith('nodes[')]
    if root_items:
        groups['root'] = {
            'title': 'Champs racine',
            'type': 'root',
            'meta': {},
            'items': root_items
        }

    # Grouper par noeud
    for i, node in enumerate(nodes):
        prefix = f"nodes[{i}]"
        node_items = [f for f in findings if f['path'].startswith(prefix)]
        if node_items:
            groups[f"node_{i}"] = {
                'title': node.get('title', f'Noeud {i}'),
                'type': node.get('type', 'text'),
                'meta': node.get('meta', {}),
                'items': node_items
            }

    # EndScreens
    es_items = [f for f in findings if f['path'].startswith('endScreens[')]
    if es_items:
        groups['endScreens'] = {
            'title': 'Ecrans de fin',
            'type': 'endScreens',
            'meta': {},
            'items': es_items
        }

    return groups


# ============================================================================
# QUESTIONS CHALLENGE
# ============================================================================

def generate_challenges(groups: Dict[str, Dict], data: Dict) -> List[str]:
    """Genere des questions challenge pour guider le remplissage."""
    challenges = []
    nodes = data.get('nodes', [])

    for key, group in groups.items():
        ntype = group['type']
        meta = group['meta']
        title = group['title']
        nb_todos = len([it for it in group['items'] if it['type'] == 'todo'])

        if ntype == 'course_presentation':
            nb_slides = 0
            nb_quiz = 0
            # Compter slides et quiz
            if key.startswith('node_'):
                idx = int(key.split('_')[1])
                node = nodes[idx]
                slides = node.get('slides', [])
                nb_slides = len(slides)
                for s in slides:
                    nb_quiz += len(s.get('interactions', []))

            purpose = meta.get('purpose', 'content')
            challenges.append(
                f"Le noeud '{title}' est une CoursePresentation de {purpose} "
                f"avec {nb_slides} slides et {nb_quiz} quiz embarques. "
                f"{nb_todos} champs a remplir. "
                f"Combien de questions souhaitez-vous par quiz ?"
            )

        elif ntype == 'branching_question':
            if key.startswith('node_'):
                idx = int(key.split('_')[1])
                node = nodes[idx]
                nb_alts = len(node.get('alternatives', []))
                purpose = meta.get('purpose', 'question')
                challenges.append(
                    f"Le noeud '{title}' est une question de {purpose} "
                    f"avec {nb_alts} alternatives. "
                    f"Est-ce suffisant pour discriminer les niveaux souhaites ?"
                )

        elif ntype == 'text' and meta.get('purpose') == 'conclusion':
            branch = meta.get('branch', 'unknown')
            challenges.append(
                f"Le noeud '{title}' est la conclusion de la branche '{branch}'. "
                f"Quel message encourageant voulez-vous transmettre ?"
            )

    # Questions globales
    scoring = data.get('scoring', 'no-score')
    if scoring == 'static-end-score':
        end_scores = [es.get('score', 0) for es in data.get('endScreens', [])]
        if end_scores:
            challenges.append(
                f"Les scores de fin sont {end_scores}. "
                f"Ces ecarts sont-ils adaptes pour motiver les eleves ?"
            )

    # Duree estimee
    total_time = sum(
        n.get('meta', {}).get('estimated_time_seconds', 60) for n in nodes
    )
    challenges.append(
        f"Duree estimee du parcours complet : {total_time // 60} minutes. "
        f"Est-ce adapte a la seance prevue ?"
    )

    return challenges


# ============================================================================
# FORMATAGE
# ============================================================================

def format_human_report(groups: Dict, challenges: List[str], data: Dict) -> str:
    """Genere un rapport lisible."""
    lines = []
    lines.append(f"=== RAPPORT DE SCAN : {data.get('title', '?')} ===")
    lines.append(f"Pattern : {data.get('_meta', {}).get('pattern', 'custom')}")
    lines.append(f"Noeuds  : {len(data.get('nodes', []))}")
    lines.append("")

    total_todos = 0
    total_empty = 0
    total_missing = 0

    for key, group in groups.items():
        todos = [it for it in group['items'] if it['type'] == 'todo']
        empties = [it for it in group['items'] if it['type'] == 'empty']
        missings = [it for it in group['items'] if it['type'] == 'missing_field']

        total_todos += len(todos)
        total_empty += len(empties)
        total_missing += len(missings)

        meta = group['meta']
        meta_str = ""
        if meta:
            meta_str = f" | {meta.get('purpose', '')}/{meta.get('branch', '')}"

        lines.append(f"--- {group['title']} [{group['type']}]{meta_str} ---")

        for item in group['items']:
            marker_type = item['type']
            if marker_type == 'todo':
                lines.append(f"  [TODO]    {item['path']} = {item['marker']}")
            elif marker_type == 'empty':
                lines.append(f"  [VIDE]    {item['path']}")
            elif marker_type == 'missing_field':
                lines.append(f"  [ABSENT]  {item['path']} : {item.get('detail', '')}")

        lines.append("")

    lines.append(f"=== RESUME ===")
    lines.append(f"  __TODO__ : {total_todos}")
    lines.append(f"  Vides   : {total_empty}")
    lines.append(f"  Absents : {total_missing}")
    lines.append(f"  TOTAL   : {total_todos + total_empty + total_missing}")
    lines.append("")

    if challenges:
        lines.append("=== QUESTIONS CHALLENGE ===")
        for i, q in enumerate(challenges, 1):
            lines.append(f"  {i}. {q}")
        lines.append("")

    return "\n".join(lines)


def format_json_report(groups: Dict, challenges: List[str], data: Dict) -> Dict:
    """Genere un rapport JSON machine-readable."""
    total_todos = sum(
        len([it for it in g['items'] if it['type'] == 'todo'])
        for g in groups.values()
    )
    total_issues = sum(len(g['items']) for g in groups.values())

    return {
        'title': data.get('title', '?'),
        'pattern': data.get('_meta', {}).get('pattern', 'custom'),
        'nb_nodes': len(data.get('nodes', [])),
        'summary': {
            'total_items': total_issues,
            'todos': total_todos,
            'empty': sum(len([it for it in g['items'] if it['type'] == 'empty']) for g in groups.values()),
            'missing': sum(len([it for it in g['items'] if it['type'] == 'missing_field']) for g in groups.values())
        },
        'groups': {
            key: {
                'title': g['title'],
                'type': g['type'],
                'meta': g['meta'],
                'items': g['items']
            }
            for key, g in groups.items()
        },
        'challenges': challenges
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Scanne un template Branching Scenario et genere un rapport'
    )
    parser.add_argument('--input', '-i', required=True, help='Fichier JSON du template')
    parser.add_argument('--output', '-o', help='Fichier JSON du rapport (optionnel)')
    parser.add_argument('--human', action='store_true', help='Afficher le rapport human-readable')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERREUR: fichier introuvable : {args.input}")
        return 1

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERREUR: JSON invalide ligne {e.lineno}: {e.msg}")
        return 1

    # Scanner
    todo_findings = scan_todos(data)
    missing_findings = detect_missing_fields(data)
    all_findings = todo_findings + missing_findings

    # Grouper
    groups = group_by_node(all_findings, data)

    # Challenges
    challenges = generate_challenges(groups, data)

    # Sortie human-readable
    if args.human or not args.output:
        human_report = format_human_report(groups, challenges, data)
        print(human_report)

    # Sortie JSON
    if args.output:
        json_report = format_json_report(groups, challenges, data)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, ensure_ascii=False, indent=2)
        print(f"OK Rapport JSON : {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
