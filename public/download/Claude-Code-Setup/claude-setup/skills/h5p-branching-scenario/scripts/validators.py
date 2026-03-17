#!/usr/bin/env python3
"""
Validation pour H5P Branching Scenario.

Validation extraite et enrichie :
- validate_preplan() : validation complete (erreurs bloquantes + warnings)
- Validators par type de noeud
- Coherence du scoring
- Accessibilite du graphe (BFS)
- Detection LaTeX dans zones interactives

Usage:
  from validators import validate_preplan
  errors, warnings = validate_preplan(data)
"""
import re
from typing import Dict, List, Tuple, Any, Set
from collections import deque


# ============================================================================
# CONSTANTES
# ============================================================================

CONTENT_TYPES = {
    'text', 'branching_question', 'course_presentation',
    'interactive_video', 'image', 'video'
}

INTERACTION_TYPES = {'multichoice', 'truefalse', 'dragtext', 'blanks', 'singlechoiceset', 'markthewords'}

SCORING_OPTIONS = ['no-score', 'static-end-score', 'dynamic-score']


# ============================================================================
# VALIDATION PRINCIPALE
# ============================================================================

def validate_preplan(data: Dict) -> Tuple[List[str], List[str]]:
    """Valide un preplan JSON complet. Retourne (erreurs, avertissements)."""
    errors = []
    warnings = []

    if not isinstance(data, dict):
        errors.append("Le JSON doit être un objet")
        return errors, warnings

    if not data.get('title'):
        errors.append("Champ 'title' requis")

    nodes = data.get('nodes', [])
    if not nodes:
        errors.append("Au moins un noeud requis dans 'nodes'")
        return errors, warnings

    end_screens = data.get('endScreens', [])
    if not end_screens:
        warnings.append("Aucun endScreen défini, des fins par défaut seront générées")

    # Validation par noeud
    max_index = len(nodes) - 1
    for i, node in enumerate(nodes):
        tag = f"Noeud {i} ({node.get('title', 'sans titre')})"
        ntype = node.get('type', 'text')

        if ntype not in CONTENT_TYPES:
            errors.append(f"{tag}: type '{ntype}' invalide. Valides: {', '.join(sorted(CONTENT_TYPES))}")
            continue

        # Dispatch vers validateur spécifique
        if ntype == 'text':
            _validate_text(tag, node, errors, warnings)
        elif ntype == 'branching_question':
            _validate_branching_question(tag, node, max_index, errors, warnings)
        elif ntype == 'course_presentation':
            _validate_course_presentation(tag, node, errors, warnings)
        elif ntype == 'interactive_video':
            _validate_interactive_video(tag, node, errors, warnings)

        # nextContentId commun (sauf branching_question qui gere via alternatives)
        if ntype != 'branching_question':
            next_id = node.get('nextContentId')
            if next_id is not None and next_id >= 0:
                if next_id > max_index:
                    errors.append(f"{tag}: nextContentId={next_id} dépasse l'index max ({max_index})")

    # Scoring
    scoring = data.get('scoring', 'no-score')
    if scoring not in SCORING_OPTIONS:
        warnings.append(f"scoring '{scoring}' inconnu, défaut 'no-score' appliqué")

    # Cohérence du scoring
    _validate_scoring_coherence(data, errors, warnings)

    # Accessibilité du graphe
    _validate_graph_reachability(nodes, errors, warnings)

    # Compatibilité LaTeX/MathJax
    _validate_mathjax_compat(data, errors, warnings)

    # Couverture endScreen
    _validate_endscreen_coverage(data, errors, warnings)

    # forceContentFinished
    _validate_force_content_finished(nodes, errors, warnings)

    # Résidus __TODO__
    _validate_todos(data, errors)

    # Accents français
    _validate_french_accents(data, warnings)

    return errors, warnings


# ============================================================================
# VALIDATION LATEX / MATHJAX
# ============================================================================

# Commandes MathJax nécessitant une extension via \require{}
_MATHJAX_EXTENSION_CMDS = {
    r'\cancel': 'cancel', r'\bcancel': 'cancel', r'\xcancel': 'cancel',
    r'\cancelto': 'cancel', r'\enclose': 'enclose', r'\bbox': 'bbox',
    r'\color': 'color', r'\colorbox': 'color', r'\fcolorbox': 'color',
}

# Commandes LaTeX pures non supportées par MathJax
_LATEX_ONLY_CMDS = [r'\newcommand', r'\renewcommand', r'\usepackage',
                    r'\documentclass', r'\begin{document}', r'\end{document}']


def _validate_mathjax_compat(data: dict, errors: list, warnings: list):
    """Vérifie la compatibilité LaTeX/MathJax dans tous les champs texte."""
    all_texts = _extract_all_strings(data)
    require_found = set()  # extensions déjà déclarées via \require

    for path, text in all_texts:
        # Detecter les \require{ext} deja presents
        for m in re.finditer(r'\\require\{(\w+)\}', text):
            require_found.add(m.group(1))

    for path, text in all_texts:
        # 1. Délimiteurs non fermés
        _check_delimiters(path, text, errors)

        # 2. Commandes nécessitant extensions
        for cmd, ext in _MATHJAX_EXTENSION_CMDS.items():
            if cmd in text and ext not in require_found:
                warnings.append(
                    f"{path}: '{cmd}' nécessite \\require{{{ext}}} "
                    f"en début de formule MathJax")

        # 3. Commandes LaTeX pures non MathJax
        for cmd in _LATEX_ONLY_CMDS:
            if cmd in text:
                errors.append(
                    f"{path}: commande LaTeX pure '{cmd}' non supportée "
                    f"par MathJax — à supprimer ou adapter")

        # 4. Dollar simple pour le mode math
        if re.search(r'(?<!\$)\$(?!\$)', text):
            if r'\(' not in text and r'\[' not in text:
                warnings.append(
                    f"{path}: utiliser \\( \\) au lieu de $ $ "
                    f"pour le mode math inline MathJax")


def _check_delimiters(path: str, text: str, errors: list):
    """Vérifie que les délimiteurs MathJax sont bien appariés."""
    # Inline \( ... \)
    open_inline = len(re.findall(r'(?<!\\)\\\(', text))
    close_inline = len(re.findall(r'(?<!\\)\\\)', text))
    if open_inline != close_inline:
        errors.append(
            f"{path}: délimiteurs inline non appariés — "
            f"{open_inline} \\( vs {close_inline} \\)")

    # Display \[ ... \]
    open_display = len(re.findall(r'(?<!\\)\\\[', text))
    close_display = len(re.findall(r'(?<!\\)\\\]', text))
    if open_display != close_display:
        errors.append(
            f"{path}: délimiteurs display non appariés — "
            f"{open_display} \\[ vs {close_display} \\]")


def _extract_all_strings(obj, path: str = "racine") -> list:
    """Parcours récursif : extrait toutes les chaînes du JSON avec leur chemin."""
    results = []
    if isinstance(obj, str):
        if len(obj) > 3:  # ignorer les tres courtes chaines
            results.append((path, obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            results.extend(_extract_all_strings(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            results.extend(_extract_all_strings(item, f"{path}[{i}]"))
    return results


# ============================================================================
# VALIDATEURS PAR TYPE
# ============================================================================

def _validate_text(tag: str, node: Dict, errors: List, warnings: List):
    """Valide un noeud de type text."""
    content = node.get('content', '')
    if not content:
        warnings.append(f"{tag}: contenu texte vide")


def _validate_branching_question(tag: str, node: Dict, max_index: int,
                                  errors: List, warnings: List):
    """Valide un noeud de type branching_question."""
    question = node.get('question', node.get('content', ''))
    if not question:
        errors.append(f"{tag}: 'question' requis pour branching_question")

    alts = node.get('alternatives', [])
    if len(alts) < 2:
        errors.append(f"{tag}: branching_question necessite au moins 2 alternatives")

    for j, alt in enumerate(alts):
        alt_tag = f"{tag} alt {j+1}"
        alt_next = alt.get('nextContentId')
        if alt_next is None:
            errors.append(f"{alt_tag}: nextContentId requis")
        elif alt_next >= 0 and alt_next > max_index:
            errors.append(f"{alt_tag}: nextContentId={alt_next} depasse l'index max ({max_index})")
        if not alt.get('text'):
            errors.append(f"{alt_tag}: 'text' requis")


def _validate_course_presentation(tag: str, node: Dict, errors: List, warnings: List):
    """Valide un noeud course_presentation avec quiz embarques optionnels."""
    slides = node.get('slides', [])
    if not slides and not node.get('content'):
        warnings.append(f"{tag}: aucune slide ni contenu defini")

    for s_idx, slide in enumerate(slides):
        slide_tag = f"{tag} slide {s_idx+1}"
        interactions = slide.get('interactions', [])

        for int_idx, interaction in enumerate(interactions):
            int_tag = f"{slide_tag} interaction {int_idx+1}"
            int_type = interaction.get('type', '')

            if int_type not in INTERACTION_TYPES:
                errors.append(f"{int_tag}: type '{int_type}' invalide. "
                              f"Valides: {', '.join(sorted(INTERACTION_TYPES))}")
                continue

            # Validation specifique par type d'interaction
            if int_type == 'multichoice':
                _validate_interaction_multichoice(int_tag, interaction, errors)
            elif int_type == 'truefalse':
                _validate_interaction_truefalse(int_tag, interaction, errors)
            elif int_type in ('dragtext', 'blanks'):
                _validate_interaction_text(int_tag, int_type, interaction, errors, warnings)
            elif int_type == 'singlechoiceset':
                _validate_interaction_singlechoiceset(int_tag, interaction, errors)
            elif int_type == 'markthewords':
                _validate_interaction_markthewords(int_tag, interaction, errors, warnings)

            # Verifier les dimensions
            for dim in ('x', 'y', 'width', 'height'):
                val = interaction.get(dim)
                if val is not None and not (0 <= val <= 100):
                    warnings.append(f"{int_tag}: {dim}={val} hors limites 0-100")


def _validate_interactive_video(tag: str, node: Dict, errors: List, warnings: List):
    """Valide un noeud interactive_video."""
    url = node.get('videoUrl', node.get('url', ''))
    if not url:
        errors.append(f"{tag}: 'videoUrl' requis pour interactive_video")

    interactions = node.get('interactions', [])
    for int_idx, interaction in enumerate(interactions):
        int_tag = f"{tag} interaction {int_idx+1}"
        if 'time' not in interaction:
            errors.append(f"{int_tag}: 'time' (timestamp en secondes) requis")
        int_type = interaction.get('type', '')
        if int_type and int_type not in INTERACTION_TYPES:
            errors.append(f"{int_tag}: type '{int_type}' invalide")


# ============================================================================
# VALIDATEURS D'INTERACTIONS (quiz embarques)
# ============================================================================

def _validate_interaction_multichoice(tag: str, interaction: Dict, errors: List):
    """Valide une interaction multichoice dans une CoursePresentation."""
    if not interaction.get('question'):
        errors.append(f"{tag}: 'question' manquante")
    answers = interaction.get('answers', [])
    if len(answers) < 2:
        errors.append(f"{tag}: minimum 2 reponses pour multichoice")
    if answers and not any(a.get('correct') for a in answers):
        errors.append(f"{tag}: aucune reponse marquee correct=true")


def _validate_interaction_truefalse(tag: str, interaction: Dict, errors: List):
    """Valide une interaction truefalse."""
    if not interaction.get('question'):
        errors.append(f"{tag}: 'question' manquante")
    if 'correct' not in interaction:
        errors.append(f"{tag}: champ 'correct' (true/false) requis")


def _validate_interaction_text(tag: str, int_type: str, interaction: Dict,
                                errors: List, warnings: List):
    """Valide une interaction dragtext ou blanks."""
    text = interaction.get('text', '')
    if not text:
        errors.append(f"{tag}: 'text' manquant")
        return

    trous = re.findall(r'\*([^*]+)\*', text)
    if not trous:
        warnings.append(f"{tag}: aucun trou (*mot*) détecté dans le texte")

    # LaTeX interdit dans les zones interactives
    _check_latex_in_interactive_zones(tag, trous, errors)


def _check_latex_in_interactive_zones(tag: str, trous: List[str], errors: List):
    """Vérifie qu'il n'y a pas de LaTeX dans les zones drag/blanks."""
    latex_patterns = ['\\(', '\\)', '$', '\\frac', '\\mathbb', '\\sqrt', '\\text']
    for trou in trous:
        for pat in latex_patterns:
            if pat in trou:
                errors.append(f"{tag}: LaTeX interdit dans les trous — trouve '*{trou}*'")
                break


def _validate_interaction_singlechoiceset(tag: str, interaction: Dict, errors: List):
    """Valide une interaction singlechoiceset (serie de questions a choix unique)."""
    questions = interaction.get('questions', [])
    if not questions:
        errors.append(f"{tag}: 'questions' requis pour singlechoiceset (liste de questions)")
        return
    for q_idx, q in enumerate(questions):
        q_tag = f"{tag} question {q_idx+1}"
        if not q.get('question'):
            errors.append(f"{q_tag}: 'question' manquante")
        answers = q.get('answers', [])
        if len(answers) < 2:
            errors.append(f"{q_tag}: minimum 2 reponses (la 1ere est la correcte)")


def _validate_interaction_markthewords(tag: str, interaction: Dict,
                                        errors: List, warnings: List):
    """Valide une interaction markthewords (marquer les mots corrects)."""
    text = interaction.get('text', '')
    if not text:
        errors.append(f"{tag}: 'text' manquant pour markthewords")
        return
    marked = re.findall(r'\*([^*]+)\*', text)
    if not marked:
        warnings.append(f"{tag}: aucun mot marqué (*mot*) détecté dans le texte markthewords")


# ============================================================================
# COHERENCE DU SCORING
# ============================================================================

def _validate_scoring_coherence(data: Dict, errors: List, warnings: List):
    """Vérifie la cohérence du scoring pour Moodle."""
    scoring = data.get('scoring', 'no-score')
    nodes = data.get('nodes', [])
    end_screens = data.get('endScreens', [])

    if scoring == 'static-end-score':
        # Chaque noeud terminal doit avoir feedback.endScreenScore
        terminal_nodes = _find_terminal_nodes(nodes)
        for idx in terminal_nodes:
            node = nodes[idx]
            tag = f"Noeud {idx} ({node.get('title', 'sans titre')})"
            feedback = node.get('feedback', {})
            if not feedback or 'score' not in feedback:
                warnings.append(
                    f"{tag}: noeud terminal sans feedback.score "
                    f"(requis pour static-end-score)")

        # EndScreens doivent avoir des scores
        for i, es in enumerate(end_screens):
            if 'score' not in es:
                warnings.append(f"endScreens[{i}]: score manquant")

    elif scoring == 'dynamic-score':
        # Vérifier que includeInteractionsScores est défini
        if not data.get('includeInteractionsScores'):
            warnings.append(
                "dynamic-score sans includeInteractionsScores=true : "
                "les scores des quiz embarqués ne seront pas comptés")

        # Attention : les scores CoursePresentation ne remontent PAS via xAPI
        has_cp = any(n.get('type') == 'course_presentation' for n in nodes)
        if has_cp:
            warnings.append(
                "ATTENTION : les scores des quiz embarqués dans CoursePresentation "
                "ne remontent PAS au carnet Moodle. Seul endScreenScore est envoyé via xAPI. "
                "Considérez static-end-score pour un scoring fiable.")


def _find_terminal_nodes(nodes: List[Dict]) -> List[int]:
    """Trouve les noeuds terminaux (nextContentId == -1)."""
    terminals = []
    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        if ntype == 'branching_question':
            for alt in node.get('alternatives', []):
                if alt.get('nextContentId', 0) == -1:
                    # Le noeud branching_question lui-meme est terminal via cette alternative
                    if i not in terminals:
                        terminals.append(i)
        else:
            if node.get('nextContentId', 0) == -1:
                terminals.append(i)
    return terminals


# ============================================================================
# ACCESSIBILITE DU GRAPHE
# ============================================================================

def _validate_endscreen_coverage(data: Dict, errors: List, warnings: List):
    """Vérifie que chaque score de fin a un endScreen correspondant."""
    nodes = data.get('nodes', [])
    end_screens = data.get('endScreens', [])

    # Collecter tous les scores uniques
    scores_needed = set()
    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        feedback = node.get('feedback', {})
        if 'score' in feedback:
            scores_needed.add(feedback['score'])

        # Alternatives de branching_question avec nextContentId=-1
        if ntype == 'branching_question':
            for alt in node.get('alternatives', []):
                if alt.get('nextContentId', 0) == -1:
                    alt_feedback = alt.get('feedback', {})
                    if 'score' in alt_feedback:
                        scores_needed.add(alt_feedback['score'])

    # Vérifier les endScreens
    scores_covered = set(es.get('score', 0) for es in end_screens)

    missing = scores_needed - scores_covered
    if missing:
        for score in sorted(missing):
            warnings.append(f"Score {score} utilisé mais pas d'endScreen correspondant")


def _validate_force_content_finished(nodes: List[Dict], errors: List, warnings: List):
    """Vérifie forceContentFinished pour text/image/video (types bloquants)."""
    problematic_types = {'text', 'image', 'video'}
    implicit_nodes = []

    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        if ntype not in problematic_types:
            continue

        tag = f"Noeud {i} ({node.get('title', 'sans titre')})"
        force_finished = node.get('forceContentFinished')

        if force_finished == 'enabled':
            warnings.append(
                f"{tag}: forceContentFinished='enabled' BLOQUE le bouton Continuer "
                f"(type {ntype} ne peut pas signaler 'finished')")
        elif force_finished is None or force_finished == 'useBehavioural':
            implicit_nodes.append(f"  - {tag}: sera 'useBehavioural' (risqué pour {ntype})")

    if implicit_nodes and len(implicit_nodes) <= 10:
        info_msg = "forceContentFinished implicite (à vérifier):\n" + "\n".join(implicit_nodes)
        warnings.append(info_msg)


def _validate_todos(data: Dict, errors: List):
    """Détecte tout __TODO__ résiduel dans le JSON."""
    all_strings = _extract_all_strings(data)
    for path, text in all_strings:
        matches = re.findall(r'__TODO__', text)
        for _ in matches:
            errors.append(f"{path}: __TODO__ résiduel trouvé")


def _validate_french_accents(data: Dict, warnings: List):
    """Vérifie les mots français courants sans accents."""
    unaccented_words = {
        r'\bEtape\b': 'Étape',
        r'\bReponse\b': 'Réponse',
        r'\bMethode\b': 'Méthode',
        r'\bResultat\b': 'Résultat',
        r'\bDefinition\b': 'Définition',
        r'\bEvaluation\b': 'Évaluation',
        r'\bEquation\b': 'Équation',
        r'\bFrancais\b': 'Français',
        r'\bSysteme\b': 'Système',
        r'\bComplementaire\b': 'Complémentaire',
        r'\bDependance\b': 'Dépendance',
        r'\bFonction\b': 'Fonction',
        r'\bOperation\b': 'Opération',
        r'\bProbabilite\b': 'Probabilité',
        r'\bFrequence\b': 'Fréquence',
        r'\bTerme\b': 'Terme',
        r'\bDenominateur\b': 'Dénominateur',
        r'\bNumerateur\b': 'Numérateur',
    }

    all_strings = _extract_all_strings(data)
    for path, text in all_strings:
        for pattern, correct in unaccented_words.items():
            if re.search(pattern, text):
                warnings.append(
                    f"{path}: mot sans accent trouvé — "
                    f"remplacer par '{correct}'")


def _validate_graph_reachability(nodes: List[Dict], errors: List, warnings: List):
    """BFS depuis noeud 0 : vérifie que tous les noeuds sont atteignables
    et que tous les chemins mènent à une fin."""
    if not nodes:
        return

    n = len(nodes)

    # Construire le graphe d'adjacence
    adj: Dict[int, Set[int]] = {i: set() for i in range(n)}
    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        if ntype == 'branching_question':
            for alt in node.get('alternatives', []):
                next_id = alt.get('nextContentId', -1)
                if 0 <= next_id < n:
                    adj[i].add(next_id)
        else:
            next_id = node.get('nextContentId', -1)
            if 0 <= next_id < n:
                adj[i].add(next_id)

    # BFS depuis noeud 0
    visited = set()
    queue = deque([0])
    visited.add(0)
    while queue:
        current = queue.popleft()
        for neighbor in adj[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Noeuds non atteignables
    unreachable = set(range(n)) - visited
    if unreachable:
        for idx in sorted(unreachable):
            node = nodes[idx]
            warnings.append(
                f"Noeud {idx} ({node.get('title', 'sans titre')}) "
                f"n'est pas atteignable depuis le noeud 0")

    # Vérifier que tous les chemins mènent à une fin (-1)
    # DFS pour trouver les noeuds sans issue
    def has_path_to_end(node_idx: int, path: Set[int]) -> bool:
        if node_idx in path:
            return False  # cycle
        node = nodes[node_idx]
        ntype = node.get('type', 'text')

        if ntype == 'branching_question':
            nexts = [alt.get('nextContentId', -1) for alt in node.get('alternatives', [])]
        else:
            nexts = [node.get('nextContentId', -1)]

        for next_id in nexts:
            if next_id == -1:
                return True
            if 0 <= next_id < n:
                if has_path_to_end(next_id, path | {node_idx}):
                    return True
        return False

    for idx in visited:
        if not has_path_to_end(idx, set()):
            node = nodes[idx]
            warnings.append(
                f"Noeud {idx} ({node.get('title', 'sans titre')}) "
                f"ne mène vers aucune fin de scénario")
