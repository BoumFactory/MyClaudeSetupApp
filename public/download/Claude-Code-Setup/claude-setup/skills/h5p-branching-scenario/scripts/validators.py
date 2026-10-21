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
from pathlib import Path
from typing import Dict, List, Tuple, Any, Set, Optional
from collections import deque


# ============================================================================
# CONSTANTES
# ============================================================================

CONTENT_TYPES = {
    'text', 'branching_question', 'course_presentation',
    'interactive_video', 'image', 'video',
    'image_hotspots',   # 30/09/2026 : H5P.ImageHotspots, NŒUD (pas une diapositive)
}

INTERACTION_TYPES = {'multichoice', 'truefalse', 'dragtext', 'blanks', 'singlechoiceset', 'markthewords',
                     # 30/09/2026 : autorisés dans une diapositive par CoursePresentation 1.25
                     'summary', 'dragquestion', 'dialogcards',
                     # 04/10/2026 : image de contexte (tableau, arbre) dans une diapositive
                     'image'}

#: Types d'interaction refusés dans une diapositive, avec la raison et le remède.
CP_FORBIDDEN_INTERACTIONS = {
    'imagehotspots': "H5P.ImageHotspots n'est pas autorisée dans une diapositive par "
                     "CoursePresentation 1.25 (absente de semantics.json) : Moodle "
                     "écarterait l'élément à l'import. Utiliser un nœud de type "
                     "'image_hotspots', autorisé par BranchingScenario 1.8.",
}

#: Formats d'image acceptés pour un chemin local (copié dans l'archive).
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')

#: Dossier du preplan pendant la validation en cours (None : pas de contrôle
#: d'existence des images). Fixé par validate_preplan().
_BASE_DIR: Optional[Path] = None

#: Marqueurs de MathJax/LaTeX, interdits dans les zones interactives.
_LATEX_MARKERS = ['\\(', '\\)', '\\[', '\\]', '$', '\\frac', '\\mathbb', '\\sqrt', '\\text']

SCORING_OPTIONS = ['no-score', 'static-end-score', 'dynamic-score']

#: Types dont la librairie est la plus susceptible de diverger en version entre
#: un Moodle académique et un lecteur hors-ligne à jour. Sert uniquement à
#: enrichir l'avertissement : AUCUN type n'est interdit (cf. SKILL.md § 6b).
LIGHTWEIGHT_PLAYER_TYPES = {'text', 'branching_question', 'course_presentation'}

#: Librairie H5P requise par chaque type hors socle (pour nommer ce qui manque).
_TYPE_LIBRARIES = {
    'interactive_video': 'H5P.InteractiveVideo',
    'video': 'H5P.Video',
    'image': 'H5P.Image',
    'image_hotspots': 'H5P.ImageHotspots',
}


# ============================================================================
# VALIDATION PRINCIPALE
# ============================================================================

def validate_preplan(data: Dict, base_dir: Optional[Path] = None) -> Tuple[List[str], List[str]]:
    """Valide un preplan JSON complet. Retourne (erreurs, avertissements).

    base_dir : dossier du preplan. S'il est fourni, l'existence des images
    locales (champs image donnés sous forme de chemin) est vérifiée."""
    global _BASE_DIR
    _BASE_DIR = Path(base_dir) if base_dir else None
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
        elif ntype == 'image_hotspots':
            _validate_image_hotspots(tag, node, errors, warnings)
        elif ntype == 'image' and isinstance(node.get('image'), str):
            _check_image_ref(tag, node.get('image'), errors)

        # nextContentId commun (sauf branching_question qui gere via alternatives)
        if ntype != 'branching_question':
            next_id = node.get('nextContentId')
            if next_id is not None and next_id >= 0:
                if next_id > max_index:
                    errors.append(f"{tag}: nextContentId={next_id} dépasse l'index max ({max_index})")

    # Compatibilité des lecteurs (Moodle vs lecteur léger hors-ligne)
    _validate_player_compatibility(data, errors, warnings)

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

    # forceContentFinished (champ par nœud : CHAINE, pas booléen)
    _validate_force_content_finished(data, errors, warnings)

    # Résidus __TODO__
    _validate_todos(data, errors)

    # Accents français
    _validate_french_accents(data, warnings)

    return errors, warnings


# ============================================================================
# COMPATIBILITE DES LECTEURS H5P
# ============================================================================

def _validate_player_compatibility(data: Dict, errors: List, warnings: List):
    """Avertit du DECALAGE DE VERSIONS entre la cible Moodle et un lecteur a jour.

    Corrige le 26/07/2026 : la premiere version de cette fonction accusait a tort
    des librairies MANQUANTES. Le constat exact, mesure sur un .h5p exporte depuis
    une installation Logiquiz reelle, est que le lecteur possede TOUT — video
    interactive comprise — mais dans des versions PLUS RECENTES que celles que ce
    generateur declare (BranchingScenario 1.8 vs 1.11, CoursePresentation 1.25 vs
    1.27, InteractiveVideo 1.27 vs 1.28, + H5P.Components absente du jeu Moodle).

    H5P resout par version EXACTE : la RACINE du parcours n'est pas resolue, le
    constructeur leve « TypeError: Cannot read properties of undefined (reading
    'library') », et TOUT reste vide — y compris les noeuds parfaitement supportes.
    L'avertissement ne depend donc PAS des types employes : il vaut pour tout
    parcours, et rappelle que la seconde archive existe.

    Avertissement seulement, jamais bloquant.
    """
    nodes = data.get('nodes', [])
    if not nodes:
        return

    types_used = sorted({n.get('type', 'text') for n in nodes})
    hors_socle = [t for t in types_used if t not in LIGHTWEIGHT_PLAYER_TYPES]
    precision = ''
    if hors_socle:
        precision = (f" Ce parcours emploie de surcroit {', '.join(hors_socle)}, "
                     f"dont les librairies divergent elles aussi en version.")

    warnings.append(
        "COMPATIBILITÉ LECTEUR : les versions de librairies declarees ici visent les "
        "Moodle academiques (H5P.BranchingScenario 1.8, CoursePresentation 1.25, "
        "InteractiveVideo 1.27). Un lecteur hors-ligne A JOUR — Logiquiz (La Digitale) "
        "est en 1.11 / 1.27 / 1.28 — ne resout PAS ces versions : H5P resout par version "
        "exacte, la racine du parcours echoue (« TypeError: Cannot read properties of "
        "undefined (reading 'library') ») et TOUT le contenu reste vide, y compris les "
        "noeuds supportes. L'echec est silencieux (« contenu vide », aucune erreur "
        "visible)." + precision + " A la generation, une SECONDE archive "
        "« <nom>-logiquiz.h5p » est produite automatiquement : contenu IDENTIQUE "
        "(videos interactives comprises), seules les versions sont realignees. Livrer "
        "la version Moodle a Moodle, l'autre au lecteur hors-ligne. Ne jamais "
        "diagnostiquer ce symptome par un type de brique (cf. SKILL.md § 6b)."
    )


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


#: Dispositions de diapositive reconnues (champ `layout` d'une slide).
SLIDE_LAYOUTS = ('full', 'text-left', 'text-top')
#: Part de la largeur (text-left) ou de la hauteur (text-top) donnée au texte.
TEXT_LEFT_WIDTH = 45
TEXT_TOP_HEIGHT = 25
#: Position par défaut d'une interaction sans coordonnées, en disposition `full`.
_FULL_DEFAULT_BOX = {'x': 5, 'y': 40, 'width': 90, 'height': 55}
#: Au-delà de ce nombre de caractères, un texte plein cadre est jugé susceptible
#: de descendre sous le haut de l'activité (y = 40 %).
_LONG_TEXT_CHARS = 250


def slide_layout_boxes(slide: Dict) -> Dict:
    """Rectangles (en % du cadre) du texte et de l'activité pour une diapositive.

    Retourne {'text': {x, y, width, height}, 'interaction': {x, y, width, height} | None}.
    `full` (défaut) : texte plein cadre, aucune coordonnée imposée aux interactions
    (leurs défauts historiques s'appliquent : comportement strictement inchangé).
    Champs facultatifs de la slide : `text_width` (text-left), `text_height` (text-top).
    """
    layout = slide.get('layout', 'full')
    if layout == 'text-left':
        tw = slide.get('text_width', TEXT_LEFT_WIDTH)
        return {'text': {'x': 0, 'y': 0, 'width': tw, 'height': 100},
                'interaction': {'x': tw + 2, 'y': 3, 'width': 100 - tw - 4, 'height': 94}}
    if layout == 'text-top':
        th = slide.get('text_height', TEXT_TOP_HEIGHT)
        return {'text': {'x': 0, 'y': 0, 'width': 100, 'height': th},
                'interaction': {'x': 3, 'y': th + 2, 'width': 94, 'height': 100 - th - 4}}
    return {'text': {'x': 0, 'y': 0, 'width': 100, 'height': 100}, 'interaction': None}


def _boxes_overlap(a: Dict, b: Dict) -> bool:
    """Vrai si deux rectangles {x, y, width, height} se recouvrent (surface > 0)."""
    return (a['x'] < b['x'] + b['width'] and b['x'] < a['x'] + a['width']
            and a['y'] < b['y'] + b['height'] and b['y'] < a['y'] + a['height'])


def _validate_slide_layout(slide_tag: str, slide: Dict, errors: List, warnings: List):
    """Valide `layout` et signale un recouvrement texte / interaction (rectangles calculés)."""
    layout = slide.get('layout', 'full')
    if layout not in SLIDE_LAYOUTS:
        errors.append(f"{slide_tag}: layout '{layout}' inconnu. Valeurs : {', '.join(SLIDE_LAYOUTS)}")
        return
    for champ, valide_pour in (('text_width', 'text-left'), ('text_height', 'text-top')):
        if champ in slide:
            val = slide[champ]
            if layout != valide_pour:
                warnings.append(f"{slide_tag}: `{champ}` n'a d'effet qu'avec layout '{valide_pour}'")
            elif not isinstance(val, (int, float)) or not (10 <= val <= 90):
                errors.append(f"{slide_tag}: `{champ}` doit être un nombre entre 10 et 90 (reçu {val!r})")
                return

    boxes = slide_layout_boxes(slide)
    text_box = boxes['text']
    plain = re.sub(r'<[^>]+>', '', slide.get('content', '') or '')
    for i, interaction in enumerate(slide.get('interactions', [])):
        base = boxes['interaction'] or _FULL_DEFAULT_BOX
        if not all(isinstance(interaction.get(k, base[k]), (int, float)) for k in base):
            continue
        box = {k: interaction.get(k, base[k]) for k in base}
        tag = f"{slide_tag} interaction {i+1}"
        if interaction.get('type') == 'image' and layout != 'full':
            # Image de contexte posée volontairement sous un texte court de la
            # colonne de texte : seul le débordement du cadre est contrôlé.
            if box['x'] + box['width'] > 100 or box['y'] + box['height'] > 100:
                warnings.append(f"{tag}: l'image dépasse du cadre (x+largeur ou y+hauteur > 100)")
            continue
        if layout == 'full':
            # Le texte plein cadre ne recouvre l'activité que s'il est assez long
            if len(plain.strip()) > _LONG_TEXT_CHARS and _boxes_overlap(text_box, box):
                warnings.append(
                    f"{tag}: le texte de la diapositive ({len(plain.strip())} caractères) occupe "
                    f"tout le cadre et peut passer sous l'activité (x={box['x']}, y={box['y']}) ; "
                    f"utiliser layout 'text-left' ou 'text-top'")
        elif _boxes_overlap(text_box, box):
            warnings.append(
                f"{tag}: recouvre le texte de la diapositive (layout '{layout}' : texte "
                f"x={text_box['x']}..{text_box['x'] + text_box['width']}, "
                f"y={text_box['y']}..{text_box['y'] + text_box['height']} ; activité "
                f"x={box['x']}..{box['x'] + box['width']}, y={box['y']}..{box['y'] + box['height']})")
        if box['x'] + box['width'] > 100 or box['y'] + box['height'] > 100:
            warnings.append(f"{tag}: l'activité dépasse du cadre (x+largeur ou y+hauteur > 100)")


def _validate_course_presentation(tag: str, node: Dict, errors: List, warnings: List):
    """Valide un noeud course_presentation avec quiz embarques optionnels."""
    slides = node.get('slides', [])
    if not slides and not node.get('content'):
        warnings.append(f"{tag}: aucune slide ni contenu defini")

    for s_idx, slide in enumerate(slides):
        slide_tag = f"{tag} slide {s_idx+1}"
        interactions = slide.get('interactions', [])
        _validate_slide_layout(slide_tag, slide, errors, warnings)

        for int_idx, interaction in enumerate(interactions):
            int_tag = f"{slide_tag} interaction {int_idx+1}"
            int_type = interaction.get('type', '')

            if int_type in CP_FORBIDDEN_INTERACTIONS:
                errors.append(f"{int_tag}: {CP_FORBIDDEN_INTERACTIONS[int_type]}")
                continue

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
            elif int_type == 'summary':
                _validate_interaction_summary(int_tag, interaction, errors, warnings)
            elif int_type == 'dragquestion':
                _validate_interaction_dragquestion(int_tag, interaction, errors, warnings)
            elif int_type == 'dialogcards':
                _validate_interaction_dialogcards(int_tag, interaction, errors, warnings)
            elif int_type == 'image':
                _validate_interaction_image(int_tag, interaction, errors, warnings)

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

    if int_type == 'blanks':
        _check_blanks_answers(tag, interaction, trous, warnings)


# ----------------------------------------------------------------------------
# Réponses saisies (textes à trous) (voir references/json-schema.md, « Réponses saisies »)
# ----------------------------------------------------------------------------
# Syntaxe H5P.Blanks 1.14 (js/blanks.js l. 735-760) : *rép1/rép2/rép3:indice*
#   - « / » sépare les réponses acceptées ;
#   - « : » introduit un indice (tout ce qui suit n'est plus une réponse).
# Tolérance aux fautes (js/cloze.js l. 43-60) : purement fondée sur la LONGUEUR
# de la réponse attendue — plus de 3 caractères : 1 erreur tolérée, plus de 9 :
# 2 — sans distinguer les nombres des mots.

_DECIMAL_RE = re.compile(r'^[+-]?\d+[.,]\d+$')
_INTEGER_RE = re.compile(r'^[+-]?\d+$')
_NUMBER_RE = re.compile(r'^[+-]?\d+(?:[.,]\d+)?$')


def _blank_alternatives(trou: str) -> List[str]:
    """Réponses acceptées d'un trou, telles que H5P.Blanks les découpe."""
    solution = trou.split(':', 1)[0]
    return [a.strip() for a in solution.split('/') if a.strip()]


def _spelling_tolerance_on(interaction: Dict) -> bool:
    """Reflet de generate_branching._blanks_accept_spelling_errors()."""
    if 'acceptSpellingErrors' in interaction:
        return bool(interaction['acceptSpellingErrors'])
    return not bool(interaction.get('numeric', False))


def _check_blanks_answers(tag: str, interaction: Dict, trous: List[str], warnings: List):
    """Avertissements sur les réponses d'un texte à trous (jamais bloquants).

    ANSWER_SINGLE_FORM : un nombre décimal n'a qu'une écriture (0,4 sans 0.4).
    ANSWER_SLASH_FRACTION : « 2/5 » est lu « 2 OU 5 », pas comme une fraction.
    ANSWER_TIP_COLON : « 12:30 » est lu « 12 » + indice « 30 ».
    ANSWER_NUMERIC_TOLERANCE : tolérance aux fautes active sur un nombre.
    """
    tolerance = _spelling_tolerance_on(interaction)
    for trou in trous:
        alts = _blank_alternatives(trou)
        if not alts:
            continue
        shown = f"*{trou}*"

        # « : » entre deux chiffres : heure ou rapport lu comme un indice
        if re.search(r'\d\s*:\s*\d', trou):
            warnings.append(
                f"{tag}: ANSWER_TIP_COLON — {shown} : dans un texte à trous, « : » "
                f"introduit un INDICE ; la réponse attendue n'est que "
                f"« {trou.split(':', 1)[0].strip()} ». Écrire l'heure avec « h » "
                f"(12h30) ou reformuler.")

        # Fraction écrite avec « / » : découpée en réponses entières distinctes
        if len(alts) >= 2 and all(_INTEGER_RE.match(a) for a in alts) \
                and len({int(a) for a in alts}) > 1:
            warnings.append(
                f"{tag}: ANSWER_SLASH_FRACTION — {shown} : « / » sépare des réponses "
                f"acceptées, donc ce trou accepte {' OU '.join(alts)}, pas une "
                f"fraction. Demander la fraction en deux trous (numérateur, "
                f"dénominateur) ou l'écriture décimale.")

        # Nombre décimal avec une seule écriture (virgule OU point)
        decimals = [a for a in alts if _DECIMAL_RE.match(a)]
        for d in decimals:
            other = d.replace(',', '.') if ',' in d else d.replace('.', ',')
            if other not in alts:
                warnings.append(
                    f"{tag}: ANSWER_SINGLE_FORM — {shown} : le nombre « {d} » n'a "
                    f"qu'une écriture ; ajouter « {other} » (*{'/'.join(alts + [other])}*).")
                break

        # Tolérance aux fautes sur une réponse chiffrée
        if tolerance and all(_NUMBER_RE.match(a) for a in alts) \
                and any(len(a) > 3 for a in alts):
            longest = max(alts, key=len)
            warnings.append(
                f"{tag}: ANSWER_NUMERIC_TOLERANCE — {shown} : tolérance aux fautes "
                f"active sur un nombre de plus de 3 caractères ; « {longest} » "
                f"accepterait une réponse à un chiffre près. Ajouter "
                f"\"numeric\": true à l'interaction.")


def image_size(raw: bytes, ext: str) -> Tuple[int, int]:
    """Largeur et hauteur en pixels, lues dans l'en-tête (PNG, JPEG, GIF).
    Partagée avec generate_branching.py (objet image H5P)."""
    if ext == '.png' and raw[:8] == b'\x89PNG\r\n\x1a\n':
        return int.from_bytes(raw[16:20], 'big'), int.from_bytes(raw[20:24], 'big')
    if ext == '.gif' and raw[:3] == b'GIF':
        return int.from_bytes(raw[6:8], 'little'), int.from_bytes(raw[8:10], 'little')
    if ext in ('.jpg', '.jpeg') and raw[:2] == b'\xff\xd8':
        i = 2
        while i + 9 < len(raw):
            if raw[i] != 0xFF:
                i += 1
                continue
            marker = raw[i + 1]
            seg_len = int.from_bytes(raw[i + 2:i + 4], 'big')
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h = int.from_bytes(raw[i + 5:i + 7], 'big')
                w = int.from_bytes(raw[i + 7:i + 9], 'big')
                return w, h
            i += 2 + seg_len
    raise ValueError(f"dimensions illisibles (format {ext} non reconnu)")


def _local_image_ratio(ref: Any) -> Optional[float]:
    """Hauteur / largeur d'une image locale, ou None si illisible."""
    try:
        if isinstance(ref, dict) and ref.get('width') and ref.get('height'):
            return float(ref['height']) / float(ref['width'])
        if isinstance(ref, str) and _BASE_DIR is not None:
            p = Path(ref)
            p = p if p.is_absolute() else _BASE_DIR / p
            w, h = image_size(p.read_bytes(), p.suffix.lower())
            return h / w
    except (OSError, ValueError, ZeroDivisionError):
        return None
    return None


#: Largeur / hauteur d'une diapositive de CoursePresentation 1.25 (mesurée dans
#: le lecteur : 1060 x 536 px environ, soit à peu près 2 pour 1).
CP_SLIDE_RATIO = 1.98

#: Hauteur ajoutée sous l'image, en % de la hauteur de la diapositive : bouton
#: « Vérifier » avant correction, puis message de retour + barre de score +
#: « Réessayer » APRÈS correction (état le plus haut). Mesuré le 30/09/2026
#: dans le lecteur : 131 px pour une diapositive de 536 px, soit 24,4 % ; avec
#: moins, l'élément défile après « Vérifier » et coupe le haut de l'image.
CP_BUTTONS_PCT = 25


def _validate_interaction_image(tag: str, interaction: Dict, errors: List, warnings: List):
    """Image de contexte posée dans une diapositive (H5P.Image 1.1).

    Le lecteur étire l'image à la taille de l'élément : on vérifie que
    height ≈ width x 1,98 x (h/l de l'image), à 8 % près."""
    _check_image_ref(tag, interaction.get('image'), errors)
    if not interaction.get('alt'):
        warnings.append(f"{tag}: image sans texte alternatif ('alt')")
    ratio = _local_image_ratio(interaction.get('image'))
    width, height = interaction.get('width'), interaction.get('height')
    if ratio and isinstance(width, (int, float)) and isinstance(height, (int, float)):
        attendu = width * CP_SLIDE_RATIO * ratio
        if attendu and abs(height - attendu) / attendu > 0.08:
            warnings.append(
                f"{tag}: image déformée — avec width={width}, la hauteur qui garde ses "
                f"proportions est {attendu:.1f} (reçu height={height})")


def _has_latex(text: Any) -> bool:
    """Vrai si le texte contient un marqueur MathJax/LaTeX."""
    s = '' if text is None else str(text)
    return any(pat in s for pat in _LATEX_MARKERS)


def _check_image_ref(tag: str, ref: Any, errors: List):
    """Vérifie une référence d'image : chemin local (chaîne) ou objet H5P."""
    if not ref:
        errors.append(f"{tag}: 'image' requis (chemin local vers un PNG, JPEG ou GIF)")
        return
    if isinstance(ref, dict):
        if not ref.get('path'):
            errors.append(f"{tag}: objet 'image' sans 'path'")
        return
    if not isinstance(ref, str):
        errors.append(f"{tag}: 'image' doit être un chemin (chaîne) ou un objet H5P")
        return
    if Path(ref).suffix.lower() not in IMAGE_EXTENSIONS:
        errors.append(f"{tag}: image « {ref} » : format non pris en charge "
                      f"(admis : {', '.join(IMAGE_EXTENSIONS)})")
        return
    if _BASE_DIR is not None:
        p = Path(ref)
        p = p if p.is_absolute() else _BASE_DIR / p
        if not p.is_file():
            errors.append(f"{tag}: image introuvable : {p}")


def _check_box(tag: str, what: str, box: Dict, errors: List, warnings: List,
               need_size: bool = True):
    """Zone en % du cadre de l'image : x, y (coin haut gauche), width, height."""
    keys = ('x', 'y', 'width', 'height') if need_size else ('x', 'y')
    for k in keys:
        v = box.get(k)
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            errors.append(f"{tag}: {what} : '{k}' requis (nombre, en % du cadre de l'image)")
            return
        if not (0 <= v <= 100):
            errors.append(f"{tag}: {what} : {k}={v} hors de 0-100 (pourcentages)")
            return
    if need_size:
        if box['x'] + box['width'] > 100.5 or box['y'] + box['height'] > 100.5:
            warnings.append(f"{tag}: {what} déborde du cadre de l'image "
                            f"(x+width ou y+height > 100)")


def _validate_interaction_summary(tag: str, interaction: Dict, errors: List, warnings: List):
    """Summary : une suite d'étapes, chacune = 1 affirmation juste + des fausses."""
    statements = interaction.get('statements', [])
    if not statements:
        errors.append(f"{tag}: 'statements' requis pour summary (liste d'étapes)")
        return
    for k, st in enumerate(statements):
        st_tag = f"{tag} étape {k + 1}"
        if not st.get('correct'):
            errors.append(f"{st_tag}: 'correct' (affirmation juste) requis")
        wrong = st.get('wrong', [])
        if not isinstance(wrong, list) or not wrong:
            errors.append(f"{st_tag}: 'wrong' requis (liste d'au moins une affirmation fausse)")


def _validate_interaction_dragquestion(tag: str, interaction: Dict, errors: List, warnings: List):
    """DragQuestion : image + zones de dépôt + étiquettes, positions en %."""
    _check_image_ref(tag, interaction.get('image'), errors)

    zones = interaction.get('zones', [])
    drags = interaction.get('draggables', [])
    if not zones:
        errors.append(f"{tag}: 'zones' requis pour dragquestion (au moins une zone de dépôt)")
    if not drags:
        errors.append(f"{tag}: 'draggables' requis pour dragquestion (au moins une étiquette)")
    if not zones or not drags:
        return

    used = set()
    for z_idx, z in enumerate(zones):
        z_tag = f"zone {z_idx + 1}"
        _check_box(tag, z_tag, z, errors, warnings)
        correct = z.get('correct', [])
        if not isinstance(correct, list):
            errors.append(f"{tag}: {z_tag} : 'correct' doit être une liste d'indices d'étiquettes")
            continue
        for k in correct:
            if not isinstance(k, int) or not (0 <= k < len(drags)):
                errors.append(f"{tag}: {z_tag} : indice d'étiquette {k!r} invalide "
                              f"(0 à {len(drags) - 1})")
            else:
                used.add(k)
        if _has_latex(z.get('label')):
            errors.append(f"{tag}: {z_tag} : LaTeX/MathJax interdit dans le libellé d'une zone")

    for d_idx, d in enumerate(drags):
        d_tag = f"étiquette {d_idx + 1}"
        if not str(d.get('text', '')).strip():
            errors.append(f"{tag}: {d_tag} : 'text' requis")
        if _has_latex(d.get('text')):
            errors.append(f"{tag}: {d_tag} : LaTeX/MathJax interdit dans une étiquette "
                          f"à glisser (« {d.get('text')} ») — écrire 0,3 ou 1/2 en texte brut")
        if ('x' in d) != ('y' in d):
            errors.append(f"{tag}: {d_tag} : donner x ET y, ou aucun des deux (placement automatique)")
        elif 'x' in d:
            _check_box(tag, d_tag, {'x': d['x'], 'y': d['y'],
                                    'width': d.get('width', 12), 'height': d.get('height', 9)},
                       errors, warnings)
    if not used:
        errors.append(f"{tag}: aucune zone n'a de bonne réponse ('correct' vide partout)")

    # Place dans la diapositive : l'image garde ses proportions et prend toute
    # la LARGEUR de l'élément ; les boutons s'ajoutent dessous. Si la hauteur
    # ne suffit pas, le bouton « Vérifier » sort de la diapositive (mesuré).
    ratio = _local_image_ratio(interaction.get('image'))
    width = interaction.get('width', 90)
    height = interaction.get('height', 55)
    if ratio and isinstance(width, (int, float)) and isinstance(height, (int, float)):
        needed = width * CP_SLIDE_RATIO * ratio + CP_BUTTONS_PCT
        if needed > height + 0.5:
            w_max = (height - CP_BUTTONS_PCT) / (CP_SLIDE_RATIO * ratio)
            warnings.append(
                f"{tag}: élément trop bas pour son image — avec width={width}, l'image "
                f"et ses boutons occupent environ {needed:.0f} % de la hauteur de la "
                f"diapositive, pour height={height} : le bouton « Vérifier » sera "
                f"coupé. Réduire width à {int(w_max)} au plus, ou augmenter height.")

    # Placement automatique : bande du bas de l'image, 10,5 % par rangée
    auto = [d for d in drags if 'x' not in d]
    if auto:
        rows, row_w = 1, 0.0
        for d in auto:
            w = d.get('width', 12) + 2
            if row_w and row_w + w > 96:
                rows, row_w = rows + 1, 0.0
            row_w += w
        band_top = 100 - rows * 10.5
        for z_idx, z in enumerate(zones):
            if isinstance(z.get('y'), (int, float)) and isinstance(z.get('height'), (int, float)) \
                    and z['y'] + z['height'] > band_top:
                warnings.append(
                    f"{tag}: zone {z_idx + 1} empiète sur la bande du bas "
                    f"(y > {band_top:.0f} %) où sont rangées les étiquettes sans x/y : "
                    f"réserver cette bande dans l'image ou placer les étiquettes.")


def _validate_interaction_dialogcards(tag: str, interaction: Dict, errors: List, warnings: List):
    """Dialogcards : cartes recto-verso."""
    cards = interaction.get('cards', [])
    if not cards:
        errors.append(f"{tag}: 'cards' requis pour dialogcards (au moins une carte)")
        return
    for k, card in enumerate(cards):
        c_tag = f"{tag} carte {k + 1}"
        if not str(card.get('front', '')).strip():
            errors.append(f"{c_tag}: 'front' (recto) requis")
        if not str(card.get('back', '')).strip():
            errors.append(f"{c_tag}: 'back' (verso) requis")
        if card.get('image'):
            _check_image_ref(c_tag, card['image'], errors)
    mode = interaction.get('mode', 'normal')
    if mode not in ('normal', 'repetition'):
        warnings.append(f"{tag}: mode '{mode}' inconnu, 'normal' appliqué")


def _validate_image_hotspots(tag: str, node: Dict, errors: List, warnings: List):
    """Nœud image_hotspots : image + points cliquables en % du cadre."""
    _check_image_ref(tag, node.get('image'), errors)
    hotspots = node.get('hotspots', [])
    if not hotspots:
        errors.append(f"{tag}: 'hotspots' requis pour image_hotspots (au moins une zone)")
        return
    for k, hs in enumerate(hotspots):
        h_tag = f"zone {k + 1}"
        _check_box(tag, h_tag, hs, errors, warnings,
                   need_size=('width' in hs or 'height' in hs))
        if not str(hs.get('text', '')).strip() and not str(hs.get('header', '')).strip():
            errors.append(f"{tag}: {h_tag} : 'header' ou 'text' requis (contenu de la bulle)")
    icon = node.get('icon')
    if icon and icon not in ('plus', 'minus', 'times', 'check', 'question', 'info', 'exclamation'):
        warnings.append(f"{tag}: icône '{icon}' inconnue, 'plus' appliquée")


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

        # Ici — et seulement ici — les quiz embarqués sont bien ignorés.
        if any(n.get('type') == 'course_presentation' for n in nodes):
            warnings.append(
                "static-end-score : les scores des quiz embarqués dans "
                "CoursePresentation ne remontent PAS au carnet Moodle. En scoring "
                "statique, scoring.getScore() renvoie le score de l'écran de fin "
                "atteint (scoring.js l. 212-216) : seul endScreenScore part en xAPI, "
                "les quiz ne servent qu'à l'entraînement. Pour compter les quiz, "
                "utiliser dynamic-score avec includeInteractionsScores=true.")

    elif scoring == 'dynamic-score':
        # Le générateur écrit includeInteractionsScores=True PAR DÉFAUT
        # (generate_branching.py, 'scoringOptionGroup') : seule une valeur
        # explicitement fausse désactive le comptage des quiz.
        include_interactions = data.get('includeInteractionsScores', True)
        has_cp = any(n.get('type') == 'course_presentation' for n in nodes)

        if not include_interactions:
            warnings.append(
                "dynamic-score avec includeInteractionsScores=false : les scores des "
                "quiz embarqués ne sont PAS comptés (scoring.js l. 294-300) — seuls "
                "les endScreenScore des nœuds et des alternatives alimentent la note "
                "xAPI. Utile pour ne noter qu'une évaluation finale ; remettre à true "
                "(le défaut) pour compter les quiz.")
        elif has_cp:
            warnings.append(
                "dynamic-score + includeInteractionsScores=true : les scores des quiz "
                "des CoursePresentation SONT comptés dans la note xAPI "
                "(CoursePresentation.getScore() → addLibraryScore(), scoring.js "
                "l. 294-300 → triggerXAPICompleted). MAIS le maximum est calculé sur "
                "les seuls nœuds VISITÉS (calculateDynamicMaxScore, scoring.js "
                "l. 132-136) : il DÉPEND DU CHEMIN. Un élève passé par les remédiations "
                "est noté sur un total plus grand qu'un élève allé droit au but — note "
                "de travail exploitable, mais NON COMPARABLE d'un élève à l'autre. "
                "Pour noter la seule évaluation finale, mettre includeInteractionsScores "
                "à false.")


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


#: Les TROIS valeurs du champ par nœud (semantics.json de
#: H5P.BranchingScenario 1.8, type "select", défaut 'useBehavioural').
FORCE_FINISHED_VALUES = ('useBehavioural', 'enabled', 'disabled')

#: Seuls ces deux types signalent leur achèvement via xAPI : ailleurs, un verrou
#: ne serait jamais levé. Le générateur y écrit 'disabled' (« ne verrouille
#: jamais »), y compris quand le réglage global demande le verrou.
FORCE_FINISHED_CAPABLE = ('course_presentation', 'interactive_video')


def _validate_force_content_finished(data: Dict, errors: List, warnings: List):
    """Vérifie forceContentFinished (champ par nœud, de type chaîne).

    Décrit ce que le générateur écrira RÉELLEMENT dans content.json :
    'useBehavioural' (suit le réglage global), 'enabled' (verrouille) ou
    'disabled' (ne verrouille jamais). Un booléen y est un format ancien,
    illisible pour le lecteur H5P, qui le réécrit en chaîne.
    """
    nodes = data.get('nodes', []) if isinstance(data, dict) else data
    global_force = bool(data.get('forceContentFinished')) if isinstance(data, dict) else False
    asked_somewhere = global_force

    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        tag = f"Noeud {i} ({node.get('title', 'sans titre')})"
        raw = node.get('forceContentFinished')

        if raw is None:
            continue

        if isinstance(raw, bool):
            warnings.append(
                f"{tag}: forceContentFinished={str(raw).lower()} est un booléen — "
                f"le champ par nœud est une chaîne dans le schéma H5P ; il sera "
                f"réécrit en '{'enabled' if raw else 'useBehavioural'}'")
        elif raw not in FORCE_FINISHED_VALUES:
            errors.append(
                f"{tag}: forceContentFinished={raw!r} hors schéma "
                f"(valeurs admises : {', '.join(FORCE_FINISHED_VALUES)})")
            continue

        wants_lock = (raw is True) or (raw == 'enabled')
        if wants_lock:
            asked_somewhere = True
            if ntype not in FORCE_FINISHED_CAPABLE:
                warnings.append(
                    f"{tag}: un nœud {ntype} ne signale jamais son achèvement — "
                    f"le verrou demandé serait définitif. Le générateur écrira "
                    f"'disabled' (aucun verrou) sur ce nœud.")

    if global_force:
        capable = [n for n in nodes if n.get('type') in FORCE_FINISHED_CAPABLE]
        if not capable:
            warnings.append(
                "forceContentFinished global = true, mais aucun nœud "
                "course_presentation / interactive_video : le réglage ne "
                "produira aucun verrou (les autres types reçoivent 'disabled').")

    return asked_somewhere


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
