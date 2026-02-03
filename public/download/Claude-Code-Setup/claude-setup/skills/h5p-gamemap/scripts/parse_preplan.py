#!/usr/bin/env python3
"""
Parse un fichier préplan Markdown en structure JSON pour la génération H5P Game Map.
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

def parse_preplan(preplan_path: str) -> Dict[str, Any]:
    """Parse un fichier préplan Markdown et retourne une structure JSON."""

    with open(preplan_path, 'r', encoding='utf-8') as f:
        content = f.read()

    result = {
        'title': '',
        'niveau': '',
        'theme': '',
        'style': 'aventure',
        'config': {
            'lives': 4,
            'roaming': 'complete',
            'fog': 'visited',
            'showLabels': True,
            'showScoreStars': 'always',
            'useAnimation': True
        },
        'background': None,
        'lore': '',
        'etapes': [],
        'endScreen': {
            'success': '',
            'failure': '',
            'feedbacks': []
        },
        'colors': {
            'stageUnvisited': 'rgba(52, 152, 219, 0.85)',
            'stageLocked': 'rgba(127, 140, 141, 0.7)',
            'stageCleared': 'rgba(46, 204, 113, 0.85)',
            'pathNormal': 'rgba(44, 62, 80, 0.6)',
            'pathCleared': 'rgba(46, 204, 113, 0.7)',
            'pathStyle': 'dotted'
        }
    }

    # Extraire le titre
    title_match = re.search(r'^# Préplan Game Map\s*:\s*(.+)$', content, re.MULTILINE)
    if title_match:
        result['title'] = title_match.group(1).strip()

    # Extraire les informations générales
    info_section = re.search(r'## Informations générales\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if info_section:
        info_text = info_section.group(1)

        niveau_match = re.search(r'\*\*Niveau\*\*\s*:\s*(.+)', info_text)
        if niveau_match:
            result['niveau'] = niveau_match.group(1).strip()

        theme_match = re.search(r'\*\*Thème\*\*\s*:\s*(.+)', info_text)
        if theme_match:
            result['theme'] = theme_match.group(1).strip()

        style_match = re.search(r'\*\*Style\*\*\s*:\s*(\w+)', info_text)
        if style_match:
            result['style'] = style_match.group(1).strip().lower()

    # Extraire la configuration
    config_section = re.search(r'## Configuration du jeu\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if config_section:
        config_text = config_section.group(1)

        lives_match = re.search(r'\*\*Vies\*\*\s*\|\s*(\d+|illimité)', config_text, re.IGNORECASE)
        if lives_match:
            val = lives_match.group(1).strip().lower()
            result['config']['lives'] = None if val == 'illimité' else int(val)

        roaming_match = re.search(r'\*\*Roaming\*\*\s*\|\s*(\w+)', config_text)
        if roaming_match:
            result['config']['roaming'] = roaming_match.group(1).strip()

        fog_match = re.search(r'\*\*Brouillard\*\*\s*\|\s*(\w+)', config_text)
        if fog_match:
            result['config']['fog'] = fog_match.group(1).strip()

    # Extraire l'image de fond
    bg_section = re.search(r'## Image de fond\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if bg_section:
        bg_text = bg_section.group(1)

        source_match = re.search(r'\*\*Source\*\*\s*:\s*(.+)', bg_text)
        if source_match:
            source = source_match.group(1).strip()
            if source.lower().startswith('générer:'):
                result['background'] = {'generate': source[8:].strip()}
            else:
                result['background'] = {'path': source}

    # Extraire le lore
    lore_section = re.search(r'## Lore / Introduction\s*\n.*?```html\s*\n(.*?)\n```', content, re.DOTALL)
    if lore_section:
        result['lore'] = lore_section.group(1).strip()

    # Extraire les étapes
    etapes_section = re.search(r'## Étapes du parcours\s*\n(.*?)(?=\n## Écrans|\n## Couleurs|\Z)', content, re.DOTALL)
    if etapes_section:
        etapes_text = etapes_section.group(1)

        # Trouver toutes les étapes
        etape_pattern = r'### Étape (\d+)\s*:\s*(.+?)\n(.*?)(?=\n### Étape|\Z)'
        for match in re.finditer(etape_pattern, etapes_text, re.DOTALL):
            etape_num = int(match.group(1))
            etape_name = match.group(2).strip()
            etape_content = match.group(3)

            etape = parse_etape(etape_num, etape_name, etape_content)
            result['etapes'].append(etape)

    # Extraire les écrans de fin
    end_section = re.search(r'## Écrans de fin\s*\n(.*?)(?=\n## Couleurs|\n## Notes|\Z)', content, re.DOTALL)
    if end_section:
        end_text = end_section.group(1)

        success_match = re.search(r'### Succès\s*\n.*?```html\s*\n(.*?)\n```', end_text, re.DOTALL)
        if success_match:
            result['endScreen']['success'] = success_match.group(1).strip()

        failure_match = re.search(r'### Échec\s*\n.*?```html\s*\n(.*?)\n```', end_text, re.DOTALL)
        if failure_match:
            result['endScreen']['failure'] = failure_match.group(1).strip()

        # Feedbacks par score
        feedback_pattern = r'\|\s*(\d+)-(\d+)%\s*\|\s*(.+?)\s*\|'
        for fb_match in re.finditer(feedback_pattern, end_text):
            result['endScreen']['feedbacks'].append({
                'from': int(fb_match.group(1)),
                'to': int(fb_match.group(2)),
                'feedback': fb_match.group(3).strip()
            })

    # Extraire les couleurs optionnelles
    colors_section = re.search(r'## Couleurs \(optionnel\)\s*\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
    if colors_section:
        colors_text = colors_section.group(1)

        color_mappings = {
            'Stage non visité': 'stageUnvisited',
            'Stage verrouillé': 'stageLocked',
            'Stage réussi': 'stageCleared',
            'Chemin normal': 'pathNormal',
            'Chemin réussi': 'pathCleared',
            'Style chemin': 'pathStyle'
        }

        for label, key in color_mappings.items():
            color_match = re.search(rf'\|\s*{re.escape(label)}\s*\|\s*`?([^|`]+)`?\s*\|', colors_text)
            if color_match:
                result['colors'][key] = color_match.group(1).strip()

    return result


def parse_etape(num: int, name: str, content: str) -> Dict[str, Any]:
    """Parse une section d'étape."""

    etape = {
        'num': num,
        'title': name,
        'x': 50,
        'y': 50,
        'type': 'multichoice',
        'isStart': num == 1,
        'content': {}
    }

    # Position
    pos_match = re.search(r'\*\*Position\*\*\s*:\s*x\s*=\s*(\d+)\s*,\s*y\s*=\s*(\d+)', content)
    if pos_match:
        etape['x'] = int(pos_match.group(1))
        etape['y'] = int(pos_match.group(2))

    # Type
    type_match = re.search(r'\*\*Type\*\*\s*:\s*(\w+)', content)
    if type_match:
        etape['type'] = type_match.group(1).strip().lower()

    # Départ
    start_match = re.search(r'\*\*Départ\*\*\s*:\s*(oui|non)', content, re.IGNORECASE)
    if start_match:
        etape['isStart'] = start_match.group(1).lower() == 'oui'

    # Parser selon le type
    if etape['type'] == 'multichoice':
        etape['content'] = parse_multichoice(content)
    elif etape['type'] == 'truefalse':
        etape['content'] = parse_truefalse(content)
    elif etape['type'] == 'dragtext':
        etape['content'] = parse_dragtext(content)
    elif etape['type'] == 'blanks':
        etape['content'] = parse_blanks(content)
    elif etape['type'] == 'singlechoiceset':
        etape['content'] = parse_singlechoiceset(content)
    elif etape['type'] == 'questionset':
        etape['content'] = parse_questionset(content)

    return etape


def parse_multichoice(content: str) -> Dict[str, Any]:
    """Parse une question MultiChoice."""

    result = {
        'question': '',
        'answers': [],
        'tip': ''
    }

    # Question
    question_match = re.search(r'\*\*Question\*\*\s*:\s*\n```\s*\n(.*?)\n```', content, re.DOTALL)
    if question_match:
        result['question'] = question_match.group(1).strip()

    # Réponses (format tableau)
    answers_pattern = r'\|\s*\[([ x])\]\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|'
    for match in re.finditer(answers_pattern, content):
        is_correct = match.group(1).strip() == 'x'
        text = match.group(2).strip().strip('`')
        feedback = match.group(3).strip()

        result['answers'].append({
            'text': text,
            'correct': is_correct,
            'feedback': feedback
        })

    # Indice
    tip_match = re.search(r'\*\*Indice\*\*\s*:\s*`?([^`\n]+)`?', content)
    if tip_match:
        result['tip'] = tip_match.group(1).strip()

    return result


def parse_truefalse(content: str) -> Dict[str, Any]:
    """Parse une question TrueFalse."""

    result = {
        'question': '',
        'correct': True,
        'feedback_correct': '',
        'feedback_incorrect': ''
    }

    # Affirmation
    question_match = re.search(r'\*\*Affirmation\*\*\s*:\s*\n```\s*\n(.*?)\n```', content, re.DOTALL)
    if question_match:
        result['question'] = question_match.group(1).strip()

    # Correct
    correct_match = re.search(r'\*\*Correct\*\*\s*:\s*(vrai|faux)', content, re.IGNORECASE)
    if correct_match:
        result['correct'] = correct_match.group(1).lower() == 'vrai'

    # Feedbacks
    fb_correct_match = re.search(r'Si correct\s*:\s*(.+)', content)
    if fb_correct_match:
        result['feedback_correct'] = fb_correct_match.group(1).strip()

    fb_incorrect_match = re.search(r'Si incorrect\s*:\s*(.+)', content)
    if fb_incorrect_match:
        result['feedback_incorrect'] = fb_incorrect_match.group(1).strip()

    return result


def parse_dragtext(content: str) -> Dict[str, Any]:
    """Parse une question DragText."""

    result = {
        'description': '',
        'text': ''
    }

    # Consigne
    desc_match = re.search(r'\*\*Consigne\*\*\s*:\s*\n```\s*\n(.*?)\n```', content, re.DOTALL)
    if desc_match:
        result['description'] = desc_match.group(1).strip()

    # Texte à compléter
    text_match = re.search(r'\*\*Texte à compléter\*\*\s*:\s*\n```\s*\n(.*?)\n```', content, re.DOTALL)
    if text_match:
        result['text'] = text_match.group(1).strip()

    return result


def parse_blanks(content: str) -> Dict[str, Any]:
    """Parse une question Blanks."""

    result = {
        'description': '',
        'text': ''
    }

    # Consigne
    desc_match = re.search(r'\*\*Consigne\*\*\s*:\s*\n```\s*\n(.*?)\n```', content, re.DOTALL)
    if desc_match:
        result['description'] = desc_match.group(1).strip()

    # Texte à trous
    text_match = re.search(r'\*\*Texte à trous\*\*\s*:\s*\n```\s*\n(.*?)\n```', content, re.DOTALL)
    if text_match:
        result['text'] = text_match.group(1).strip()

    return result


def parse_singlechoiceset(content: str) -> Dict[str, Any]:
    """Parse un SingleChoiceSet (plusieurs questions rapides)."""

    result = {
        'questions': []
    }

    # Trouver chaque question numérotée
    question_pattern = r'(\d+)\.\s*\*\*Question\*\*\s*:\s*(.+?)\n(.*?)(?=\d+\.\s*\*\*Question\*\*|\Z)'
    for match in re.finditer(question_pattern, content, re.DOTALL):
        question_text = match.group(2).strip()
        answers_section = match.group(3)

        answers = []
        answer_pattern = r'-\s*\[([ x])\]\s*(.+)'
        for ans_match in re.finditer(answer_pattern, answers_section):
            is_correct = ans_match.group(1).strip() == 'x'
            text = ans_match.group(2).strip()
            answers.append({
                'text': text,
                'correct': is_correct
            })

        if answers:
            result['questions'].append({
                'question': question_text,
                'answers': answers
            })

    return result


def parse_questionset(content: str) -> Dict[str, Any]:
    """Parse un QuestionSet (mix de types dans une étape)."""

    result = {
        'questions': []
    }

    # Trouver chaque question avec son type
    question_pattern = r'\*\*Question (\d+)\*\*\s*\((\w+)\)\s*:\s*\n```\s*\n(.*?)\n```(.*?)(?=\*\*Question \d+\*\*|\Z)'
    for match in re.finditer(question_pattern, content, re.DOTALL):
        q_type = match.group(2).strip().lower()
        q_text = match.group(3).strip()
        q_content = match.group(4)

        question = {
            'type': q_type,
            'question': q_text
        }

        if q_type == 'multichoice':
            answers = []
            answer_pattern = r'-\s*\[([ x])\]\s*(.+)'
            for ans_match in re.finditer(answer_pattern, q_content):
                is_correct = ans_match.group(1).strip() == 'x'
                text = ans_match.group(2).strip()
                answers.append({'text': text, 'correct': is_correct})
            question['answers'] = answers

        elif q_type == 'truefalse':
            correct_match = re.search(r'Correct\s*:\s*(vrai|faux)', q_content, re.IGNORECASE)
            if correct_match:
                question['correct'] = correct_match.group(1).lower() == 'vrai'

            fb_correct = re.search(r'Feedback correct\s*:\s*(.+)', q_content)
            if fb_correct:
                question['feedback_correct'] = fb_correct.group(1).strip()

            fb_incorrect = re.search(r'Feedback incorrect\s*:\s*(.+)', q_content)
            if fb_incorrect:
                question['feedback_incorrect'] = fb_incorrect.group(1).strip()

        result['questions'].append(question)

    return result


def validate_preplan(data: Dict[str, Any]) -> List[str]:
    """Valide la cohérence du préplan parsé."""

    errors = []

    if not data['title']:
        errors.append("Titre manquant")

    if not data['etapes']:
        errors.append("Aucune étape définie")

    # Vérifier qu'il y a un départ
    has_start = any(e.get('isStart', False) for e in data['etapes'])
    if not has_start and data['etapes']:
        data['etapes'][0]['isStart'] = True  # Auto-fix

    # Vérifier la variation des types
    if len(data['etapes']) >= 4:
        types = [e['type'] for e in data['etapes']]
        unique_types = set(types)
        if len(unique_types) < 2:
            errors.append("Recommandation: varier les types de questions (actuellement que des {})".format(types[0]))

        multichoice_count = types.count('multichoice')
        if multichoice_count / len(types) > 0.4:
            errors.append(f"Recommandation: trop de QCM ({multichoice_count}/{len(types)}), max 40% recommandé")

    # Vérifier les positions
    for etape in data['etapes']:
        if not (0 <= etape['x'] <= 100) or not (0 <= etape['y'] <= 100):
            errors.append(f"Position invalide pour '{etape['title']}': x={etape['x']}, y={etape['y']}")

    return errors


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python parse_preplan.py <chemin_preplan.md>")
        sys.exit(1)

    preplan_path = sys.argv[1]

    try:
        data = parse_preplan(preplan_path)
        errors = validate_preplan(data)

        if errors:
            print("Avertissements:")
            for e in errors:
                print(f"  - {e}")
            print()

        print("Préplan parsé avec succès:")
        print(f"  - Titre: {data['title']}")
        print(f"  - Niveau: {data['niveau']}")
        print(f"  - Style: {data['style']}")
        print(f"  - Étapes: {len(data['etapes'])}")

        # Optionnel: sortie JSON
        if len(sys.argv) > 2 and sys.argv[2] == '--json':
            output_path = preplan_path.replace('.md', '.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\nJSON exporté: {output_path}")

    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)
