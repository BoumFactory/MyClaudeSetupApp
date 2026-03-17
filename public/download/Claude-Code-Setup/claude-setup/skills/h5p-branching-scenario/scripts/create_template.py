#!/usr/bin/env python3
"""
Generateur de squelette JSON pour Branching Scenario.

Genere un template JSON avec marqueurs __TODO__ depuis une analyse de cours.
4 patterns predefinis : diagnostic_differentiation, remediation_loop,
scenario_dilemmes, student_choice.

Usage:
  python create_template.py --input analysis.json --output template.json
  python create_template.py --pattern diagnostic_differentiation --title "Les fractions" --output template.json
"""
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any


# ============================================================================
# PATTERNS PREDEFINIS
# ============================================================================

def _pattern_diagnostic_differentiation(title: str, branches: int = 3) -> Dict:
    """Q diagnostic > branches par niveau > fins differenciees."""
    nodes = [
        {
            "title": "Introduction",
            "type": "text",
            "content": "__TODO_INTRO__",
            "nextContentId": 1,
            "meta": {"purpose": "introduction", "difficulty": "none", "branch": "common", "estimated_time_seconds": 30}
        },
        {
            "title": "Test diagnostique",
            "type": "branching_question",
            "question": "__TODO_DIAGNOSTIC_QUESTION__",
            "alternatives": [],
            "meta": {"purpose": "diagnostic", "difficulty": "medium", "branch": "common", "estimated_time_seconds": 60}
        }
    ]

    end_screens = []
    branch_labels = ["expert", "intermediaire", "debutant"]
    branch_scores = [100, 70, 40]
    branch_difficulties = ["hard", "medium", "easy"]
    next_node_id = 2

    for b in range(min(branches, 3)):
        label = branch_labels[b] if b < len(branch_labels) else f"branche_{b}"
        score = branch_scores[b] if b < len(branch_scores) else 50
        difficulty = branch_difficulties[b] if b < len(branch_difficulties) else "medium"

        content_id = next_node_id
        # Noeud de contenu
        nodes.append({
            "title": f"Parcours {label}",
            "type": "course_presentation",
            "slides": [
                {"content": f"__TODO_SLIDE_{label.upper()}_1__", "interactions": []},
                {"content": f"__TODO_SLIDE_{label.upper()}_2__", "interactions": [
                    {
                        "type": "multichoice",
                        "x": 5, "y": 40, "width": 90, "height": 55,
                        "question": f"__TODO_QUIZ_{label.upper()}__",
                        "answers": [
                            {"text": "__TODO_ANSWER_1__", "correct": True, "feedback": "__TODO_FEEDBACK_CORRECT__"},
                            {"text": "__TODO_ANSWER_2__", "correct": False, "feedback": "__TODO_FEEDBACK_INCORRECT__"},
                            {"text": "__TODO_ANSWER_3__", "correct": False, "feedback": "__TODO_FEEDBACK_INCORRECT__"}
                        ]
                    }
                ]}
            ],
            "nextContentId": content_id + 1,
            "meta": {"purpose": "content", "difficulty": difficulty, "branch": label, "estimated_time_seconds": 120}
        })
        next_node_id += 1

        # Noeud de fin de branche
        nodes.append({
            "title": f"Bilan {label}",
            "type": "text",
            "content": f"__TODO_BILAN_{label.upper()}__",
            "nextContentId": -1,
            "feedback": {"title": f"__TODO_FEEDBACK_TITLE_{label.upper()}__", "subtitle": f"__TODO_FEEDBACK_SUB_{label.upper()}__", "score": score},
            "meta": {"purpose": "conclusion", "difficulty": difficulty, "branch": label, "estimated_time_seconds": 30}
        })
        next_node_id += 1

        # Alternative pour la question diagnostique
        nodes[1]["alternatives"].append({
            "text": f"__TODO_ALT_{label.upper()}__",
            "nextContentId": content_id,
            "feedback": {"title": f"__TODO_ALT_FB_TITLE_{label.upper()}__", "subtitle": f"__TODO_ALT_FB_SUB_{label.upper()}__", "score": score}
        })

        end_screens.append({
            "title": f"__TODO_END_TITLE_{label.upper()}__",
            "subtitle": f"__TODO_END_SUB_{label.upper()}__",
            "score": score
        })

    return {
        "title": title,
        "scoring": "static-end-score",
        "enableBackwardsNavigation": True,
        "startScreen": {
            "title": title,
            "subtitle": "__TODO_SUBTITLE__"
        },
        "nodes": nodes,
        "endScreens": end_screens
    }


def _pattern_remediation_loop(title: str, max_retries: int = 2) -> Dict:
    """Contenu > test > reussi/echoue > remediation > retest."""
    nodes = [
        {
            "title": "Cours",
            "type": "course_presentation",
            "slides": [
                {"content": "__TODO_COURS_SLIDE_1__", "interactions": []},
                {"content": "__TODO_COURS_SLIDE_2__", "interactions": []},
                {"content": "__TODO_COURS_SLIDE_3__", "interactions": []}
            ],
            "nextContentId": 1,
            "meta": {"purpose": "content", "difficulty": "medium", "branch": "common", "estimated_time_seconds": 180}
        },
        {
            "title": "Test initial",
            "type": "branching_question",
            "question": "__TODO_TEST_QUESTION__",
            "alternatives": [
                {
                    "text": "__TODO_CORRECT_ANSWER__",
                    "nextContentId": 2,
                    "feedback": {"title": "Bravo !", "subtitle": "__TODO_FB_CORRECT__", "score": 100}
                },
                {
                    "text": "__TODO_WRONG_ANSWER_1__",
                    "nextContentId": 3,
                    "feedback": {"title": "Pas tout a fait", "subtitle": "__TODO_FB_WRONG__", "score": 0}
                }
            ],
            "meta": {"purpose": "assessment", "difficulty": "medium", "branch": "common", "estimated_time_seconds": 60}
        },
        {
            "title": "Reussite directe",
            "type": "text",
            "content": "__TODO_SUCCESS_CONTENT__",
            "nextContentId": -1,
            "feedback": {"title": "Excellent !", "subtitle": "__TODO_SUCCESS_FB__", "score": 100},
            "meta": {"purpose": "conclusion", "difficulty": "medium", "branch": "success", "estimated_time_seconds": 30}
        },
        {
            "title": "Remediation",
            "type": "course_presentation",
            "slides": [
                {"content": "__TODO_REMEDIATION_SLIDE_1__", "interactions": []},
                {"content": "__TODO_REMEDIATION_SLIDE_2__", "interactions": [
                    {
                        "type": "multichoice",
                        "x": 5, "y": 40, "width": 90, "height": 55,
                        "question": "__TODO_REMEDIATION_QUIZ__",
                        "answers": [
                            {"text": "__TODO_REM_ANSWER_1__", "correct": True, "feedback": "Correct !"},
                            {"text": "__TODO_REM_ANSWER_2__", "correct": False, "feedback": "__TODO_REM_FB__"}
                        ]
                    }
                ]}
            ],
            "nextContentId": 4,
            "meta": {"purpose": "remediation", "difficulty": "easy", "branch": "remediation", "estimated_time_seconds": 120}
        },
        {
            "title": "Retest",
            "type": "branching_question",
            "question": "__TODO_RETEST_QUESTION__",
            "alternatives": [
                {
                    "text": "__TODO_RETEST_CORRECT__",
                    "nextContentId": 5,
                    "feedback": {"title": "Bravo !", "subtitle": "__TODO_RETEST_FB_OK__", "score": 70}
                },
                {
                    "text": "__TODO_RETEST_WRONG__",
                    "nextContentId": 6,
                    "feedback": {"title": "Dommage", "subtitle": "__TODO_RETEST_FB_KO__", "score": 30}
                }
            ],
            "meta": {"purpose": "assessment", "difficulty": "medium", "branch": "remediation", "estimated_time_seconds": 60}
        },
        {
            "title": "Reussite apres remediation",
            "type": "text",
            "content": "__TODO_REMEDIATION_SUCCESS__",
            "nextContentId": -1,
            "feedback": {"title": "Bien !", "subtitle": "__TODO_REM_SUCCESS_FB__", "score": 70},
            "meta": {"purpose": "conclusion", "difficulty": "medium", "branch": "remediation_success", "estimated_time_seconds": 30}
        },
        {
            "title": "Fin remediation",
            "type": "text",
            "content": "__TODO_REMEDIATION_FAIL__",
            "nextContentId": -1,
            "feedback": {"title": "A retravailler", "subtitle": "__TODO_REM_FAIL_FB__", "score": 30},
            "meta": {"purpose": "conclusion", "difficulty": "easy", "branch": "remediation_fail", "estimated_time_seconds": 30}
        }
    ],
    end_screens = [
        {"title": "Excellent !", "subtitle": "__TODO_END_EXCELLENT__", "score": 100},
        {"title": "Bien !", "subtitle": "__TODO_END_BIEN__", "score": 70},
        {"title": "A retravailler", "subtitle": "__TODO_END_RETRAVAILLER__", "score": 30}
    ]

    return {
        "title": title,
        "scoring": "static-end-score",
        "enableBackwardsNavigation": True,
        "startScreen": {"title": title, "subtitle": "__TODO_SUBTITLE__"},
        "nodes": nodes,
        "endScreens": end_screens
    }


def _pattern_scenario_dilemmes(title: str, dilemmes: int = 2) -> Dict:
    """Situation > choix > consequences > nouveaux choix."""
    nodes = [
        {
            "title": "Situation initiale",
            "type": "text",
            "content": "__TODO_SITUATION__",
            "nextContentId": 1,
            "meta": {"purpose": "introduction", "difficulty": "none", "branch": "common", "estimated_time_seconds": 60}
        },
        {
            "title": "Premier choix",
            "type": "branching_question",
            "question": "__TODO_DILEMME_1__",
            "alternatives": [
                {
                    "text": "__TODO_CHOIX_1A__",
                    "nextContentId": 2,
                    "feedback": {"title": "__TODO_FB_1A_TITLE__", "subtitle": "__TODO_FB_1A_SUB__", "score": 0}
                },
                {
                    "text": "__TODO_CHOIX_1B__",
                    "nextContentId": 3,
                    "feedback": {"title": "__TODO_FB_1B_TITLE__", "subtitle": "__TODO_FB_1B_SUB__", "score": 0}
                },
                {
                    "text": "__TODO_CHOIX_1C__",
                    "nextContentId": 4,
                    "feedback": {"title": "__TODO_FB_1C_TITLE__", "subtitle": "__TODO_FB_1C_SUB__", "score": 0}
                }
            ],
            "meta": {"purpose": "dilemma", "difficulty": "medium", "branch": "common", "estimated_time_seconds": 90}
        },
        {
            "title": "Consequence choix A",
            "type": "text",
            "content": "__TODO_CONSEQUENCE_1A__",
            "nextContentId": 5,
            "meta": {"purpose": "consequence", "difficulty": "medium", "branch": "choix_a", "estimated_time_seconds": 60}
        },
        {
            "title": "Consequence choix B",
            "type": "text",
            "content": "__TODO_CONSEQUENCE_1B__",
            "nextContentId": 5,
            "meta": {"purpose": "consequence", "difficulty": "medium", "branch": "choix_b", "estimated_time_seconds": 60}
        },
        {
            "title": "Consequence choix C",
            "type": "text",
            "content": "__TODO_CONSEQUENCE_1C__",
            "nextContentId": -1,
            "feedback": {"title": "__TODO_END_C__", "subtitle": "__TODO_END_C_SUB__", "score": 30},
            "meta": {"purpose": "conclusion", "difficulty": "medium", "branch": "choix_c", "estimated_time_seconds": 30}
        },
        {
            "title": "Second choix",
            "type": "branching_question",
            "question": "__TODO_DILEMME_2__",
            "alternatives": [
                {
                    "text": "__TODO_CHOIX_2A__",
                    "nextContentId": 6,
                    "feedback": {"title": "__TODO_FB_2A__", "subtitle": "", "score": 0}
                },
                {
                    "text": "__TODO_CHOIX_2B__",
                    "nextContentId": 7,
                    "feedback": {"title": "__TODO_FB_2B__", "subtitle": "", "score": 0}
                }
            ],
            "meta": {"purpose": "dilemma", "difficulty": "hard", "branch": "convergence", "estimated_time_seconds": 90}
        },
        {
            "title": "Fin branche A",
            "type": "text",
            "content": "__TODO_FIN_A__",
            "nextContentId": -1,
            "feedback": {"title": "__TODO_FIN_A_TITLE__", "subtitle": "__TODO_FIN_A_SUB__", "score": 100},
            "meta": {"purpose": "conclusion", "difficulty": "hard", "branch": "fin_a", "estimated_time_seconds": 30}
        },
        {
            "title": "Fin branche B",
            "type": "text",
            "content": "__TODO_FIN_B__",
            "nextContentId": -1,
            "feedback": {"title": "__TODO_FIN_B_TITLE__", "subtitle": "__TODO_FIN_B_SUB__", "score": 70},
            "meta": {"purpose": "conclusion", "difficulty": "hard", "branch": "fin_b", "estimated_time_seconds": 30}
        }
    ]

    end_screens = [
        {"title": "__TODO_END_OPTIMAL__", "subtitle": "__TODO_END_OPTIMAL_SUB__", "score": 100},
        {"title": "__TODO_END_BON__", "subtitle": "__TODO_END_BON_SUB__", "score": 70},
        {"title": "__TODO_END_MOYEN__", "subtitle": "__TODO_END_MOYEN_SUB__", "score": 30}
    ]

    return {
        "title": title,
        "scoring": "static-end-score",
        "enableBackwardsNavigation": True,
        "startScreen": {"title": title, "subtitle": "__TODO_SUBTITLE__"},
        "nodes": nodes,
        "endScreens": end_screens
    }


def _pattern_student_choice(title: str, parcours: int = 3) -> Dict:
    """Menu > parcours paralleles > fins individuelles."""
    nodes = [
        {
            "title": "Accueil",
            "type": "text",
            "content": "__TODO_ACCUEIL__",
            "nextContentId": 1,
            "meta": {"purpose": "introduction", "difficulty": "none", "branch": "common", "estimated_time_seconds": 30}
        },
        {
            "title": "Choix du parcours",
            "type": "branching_question",
            "question": "__TODO_CHOIX_PARCOURS__",
            "alternatives": [],
            "meta": {"purpose": "menu", "difficulty": "none", "branch": "common", "estimated_time_seconds": 30}
        }
    ]

    end_screens = []
    parcours_labels = ["decouverte", "entrainement", "expert"]
    parcours_steps = [3, 4, 2]
    parcours_scores = [60, 80, 100]
    next_node_id = 2

    for p in range(min(parcours, 3)):
        label = parcours_labels[p] if p < len(parcours_labels) else f"parcours_{p}"
        nb_steps = parcours_steps[p] if p < len(parcours_steps) else 3
        score = parcours_scores[p] if p < len(parcours_scores) else 70
        start_id = next_node_id

        # Noeuds du parcours
        for s in range(nb_steps):
            is_last = (s == nb_steps - 1)
            node_type = "course_presentation" if s % 2 == 0 else "text"
            nodes.append({
                "title": f"{label.capitalize()} - etape {s+1}",
                "type": node_type,
                "content": f"__TODO_{label.upper()}_STEP_{s+1}__" if node_type == "text" else None,
                "slides": [
                    {"content": f"__TODO_{label.upper()}_SLIDE_{s+1}_1__", "interactions": []},
                    {"content": f"__TODO_{label.upper()}_SLIDE_{s+1}_2__", "interactions": []}
                ] if node_type == "course_presentation" else None,
                "nextContentId": -1 if is_last else next_node_id + 1,
                "feedback": {"title": f"__TODO_FB_{label.upper()}__", "subtitle": "", "score": score} if is_last else None,
                "meta": {"purpose": "content", "difficulty": "easy" if p == 0 else "medium" if p == 1 else "hard", "branch": label, "estimated_time_seconds": 90}
            })
            next_node_id += 1

        # Alternative du menu
        nodes[1]["alternatives"].append({
            "text": f"__TODO_MENU_{label.upper()}__",
            "nextContentId": start_id,
            "feedback": {"title": f"Parcours {label}", "subtitle": f"__TODO_MENU_FB_{label.upper()}__", "score": 0}
        })

        end_screens.append({
            "title": f"__TODO_END_{label.upper()}__",
            "subtitle": f"__TODO_END_SUB_{label.upper()}__",
            "score": score
        })

    # Nettoyer les champs None
    for node in nodes:
        keys_to_remove = [k for k, v in node.items() if v is None]
        for k in keys_to_remove:
            del node[k]

    return {
        "title": title,
        "scoring": "static-end-score",
        "enableBackwardsNavigation": True,
        "startScreen": {"title": title, "subtitle": "__TODO_SUBTITLE__"},
        "nodes": nodes,
        "endScreens": end_screens
    }


PATTERNS = {
    'diagnostic_differentiation': _pattern_diagnostic_differentiation,
    'remediation_loop': _pattern_remediation_loop,
    'scenario_dilemmes': _pattern_scenario_dilemmes,
    'student_choice': _pattern_student_choice,
}


# ============================================================================
# GENERATION DEPUIS INPUT
# ============================================================================

def create_template_from_analysis(analysis: Dict) -> Dict:
    """Genere un template depuis un JSON d'analyse.

    L'analyse contient:
    - title: titre du parcours
    - pattern: nom du pattern (ou auto)
    - level: niveau scolaire
    - branches: nombre de branches souhaitees
    - theme: theme pedagogique
    """
    title = analysis.get('title', 'Parcours adaptatif')
    pattern_name = analysis.get('pattern', 'diagnostic_differentiation')
    branches = analysis.get('branches', 3)

    pattern_fn = PATTERNS.get(pattern_name)
    if not pattern_fn:
        print(f"ERREUR: pattern '{pattern_name}' inconnu. "
              f"Disponibles: {', '.join(PATTERNS.keys())}")
        sys.exit(1)

    template = pattern_fn(title, branches)

    # Ajouter les metadonnees
    template['_meta'] = {
        'pattern': pattern_name,
        'level': analysis.get('level', ''),
        'theme': analysis.get('theme', ''),
        'generated_by': 'create_template.py',
        'version': '1.0'
    }

    return template


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Genere un squelette JSON Branching Scenario avec marqueurs __TODO__'
    )
    parser.add_argument('--input', '-i', help='Fichier JSON d\'analyse')
    parser.add_argument('--pattern', '-p', choices=list(PATTERNS.keys()),
                        default='diagnostic_differentiation',
                        help='Pattern predefini')
    parser.add_argument('--title', '-t', default='Parcours adaptatif',
                        help='Titre du parcours')
    parser.add_argument('--branches', '-b', type=int, default=3,
                        help='Nombre de branches (defaut: 3)')
    parser.add_argument('--output', '-o', required=True, help='Fichier JSON de sortie')

    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"ERREUR: fichier introuvable : {args.input}")
            return 1
        with open(input_path, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        template = create_template_from_analysis(analysis)
    else:
        pattern_fn = PATTERNS[args.pattern]
        template = pattern_fn(args.title, args.branches)
        template['_meta'] = {
            'pattern': args.pattern,
            'generated_by': 'create_template.py',
            'version': '1.0'
        }

    # Ecrire le template
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    # Compter les __TODO__
    content = json.dumps(template)
    todos = content.count('__TODO')
    nb_nodes = len(template.get('nodes', []))

    print(f"OK Template genere : {args.output}")
    print(f"  Pattern  : {template.get('_meta', {}).get('pattern', '?')}")
    print(f"  Titre    : {template.get('title', '?')}")
    print(f"  Noeuds   : {nb_nodes}")
    print(f"  __TODO__ : {todos} marqueurs a remplir")
    print()
    for i, n in enumerate(template.get('nodes', [])):
        meta = n.get('meta', {})
        purpose = meta.get('purpose', '?')
        branch = meta.get('branch', '?')
        print(f"  {i}. {n.get('title', '?')} [{n.get('type', '?')}] ({purpose}/{branch})")

    return 0


if __name__ == '__main__':
    sys.exit(main())
