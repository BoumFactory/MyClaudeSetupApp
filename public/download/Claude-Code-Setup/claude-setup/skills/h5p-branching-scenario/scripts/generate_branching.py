#!/usr/bin/env python3
"""
Générateur de H5P Branching Scenario depuis un preplan JSON.

Supporte :
- Noeuds riches : text, branching_question, course_presentation (avec quiz embarqués),
  interactive_video (avec questions à des timestamps), image, video
- Scoring : static-end-score, dynamic-score, no-score
- Post-processing du scoring pour Moodle (endScreenScore sur noeuds terminaux)
- Détection automatique des dépendances H5P
- DOUBLE SORTIE : la version Moodle (complète) et, si nécessaire, une version
  « <nom>-logiquiz.h5p » pour les lecteurs H5P légers hors-ligne, dont les types
  non supportés sont remplacés en place (routage et indices intacts).
  Voir LOGIQUIZ_SUPPORTED_LIBRARIES.

Usage:
  python generate_branching.py --input preplan.json --output scenario.h5p
  python generate_branching.py --input preplan.json --validate
"""
import json
import zipfile
import io
import uuid
import sys
import argparse
import re
import random
import copy
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import deque

# Import validation
try:
    from validators import validate_preplan, image_size as _image_size, slide_layout_boxes
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from validators import validate_preplan, image_size as _image_size, slide_layout_boxes


# ============================================================================
# TYPES DE CONTENUS SUPPORTES
# ============================================================================

CONTENT_TYPES = {
    'text': 'H5P.AdvancedText 1.1',
    'branching_question': 'H5P.BranchingQuestion 1.0',
    'course_presentation': 'H5P.CoursePresentation 1.25',
    'interactive_video': 'H5P.InteractiveVideo 1.27',
    'image': 'H5P.Image 1.1',
    'image_hotspots': 'H5P.ImageHotspots 1.10',
    'video': 'H5P.Video 1.6',
}

# ============================================================================
# COMPATIBILITE LOGIQUIZ (lecteur H5P hors-ligne de La Digitale)
# ============================================================================
# SEULE constante a modifier pour suivre l evolution de Logiquiz : les types de
# noeuds et d interactions supportes en sont DERIVES (tables juste dessous).
#
# Releve du 26/07/2026, DEUX sources divergentes — lire avant de toucher :
#   (1) Export HTML (11 Mo) produit par une installation Logiquiz reelle, celle
#       de l enseignant : seules H5P.AdvancedText, H5P.BranchingQuestion,
#       H5P.CoursePresentation et H5P.MultiChoice y figurent. Un parcours
#       contenant un noeud interactive_video n y affiche RIEN — le lecteur lit
#       undefined.library dans le constructeur de H5P.BranchingScenario et leve
#       « TypeError: Cannot read properties of undefined (reading 'library') ».
#       TOUT le parcours reste vide, pas seulement les noeuds fautifs, et
#       l echec est silencieux (« contenu vide », aucune erreur affichee).
#   (2) Depot amont https://codeberg.org/ladigitale/logiquiz, dossier libraries/
#       (verifie via l API Codeberg le 26/07/2026) : plus de 100 bibliotheques,
#       dont H5P.InteractiveVideo-1.26/1.27/1.28, H5P.Video-1.6, H5P.Image-1.1,
#       H5P.ImageHotspots-1.10/1.11, H5P.Blanks-1.14, H5P.DragText-1.10,
#       H5P.MarkTheWords-1.11, H5P.SingleChoiceSet-1.11.
#
# On retient (1), le comportement MESURE, et non (2), le catalogue amont : une
# installation en retard sur le depot est le cas courant. Le cout de l erreur
# est asymetrique — un socle trop etroit degrade quelques blocs, un socle trop
# large rend un parcours entierement vide.
# Si l installation cible est a jour, elargir cette liste (une ligne par
# bibliotheque) : rien d autre n est a modifier.
LOGIQUIZ_SUPPORTED_LIBRARIES = {
    'H5P.AdvancedText',
    'H5P.BranchingQuestion',
    'H5P.CoursePresentation',
    'H5P.MultiChoice',
}

#: Bibliotheque instanciee par chaque type de noeud (derivee de CONTENT_TYPES).
NODE_TYPE_LIBRARY = {t: lib.split(' ')[0] for t, lib in CONTENT_TYPES.items()}

#: Bibliotheque instanciee par chaque type d interaction embarquee.
INTERACTION_LIBRARY = {
    'multichoice':     'H5P.MultiChoice',
    'truefalse':       'H5P.TrueFalse',
    'dragtext':        'H5P.DragText',
    'blanks':          'H5P.Blanks',
    'singlechoiceset': 'H5P.SingleChoiceSet',
    'markthewords':    'H5P.MarkTheWords',
    # Ajouts du 30/09/2026 (activités variées). Les trois
    # figurent dans la liste des éléments de diapositive autorisés par
    # semantics.json de H5P.CoursePresentation 1.25 (l. 57-78).
    'summary':         'H5P.Summary',
    'dragquestion':    'H5P.DragQuestion',
    'dialogcards':     'H5P.Dialogcards',
    # 04/10/2026 : image de contexte (tableau, arbre) posée dans une diapositive.
    'image':           'H5P.Image',
}

#: H5P.ImageHotspots n'est PAS autorisée comme élément de diapositive par
#: CoursePresentation 1.25 (absente de la liste « options » de semantics.json) :
#: à l'import, Moodle écarterait l'élément (« Library used in content is not a
#: valid library according to semantics »). Elle est en revanche autorisée comme
#: NŒUD par H5P.BranchingScenario 1.8 : c'est le type de nœud 'image_hotspots'.
CP_FORBIDDEN_INTERACTIONS = {
    'imagehotspots': "H5P.ImageHotspots n'est pas autorisée dans une diapositive "
                     "par CoursePresentation 1.25 : utiliser un nœud de type "
                     "'image_hotspots' (autorisé par BranchingScenario 1.8).",
}

#: Libelles lisibles par un eleve de college (jamais le nom technique).
TYPE_LABELS_FR = {
    'text':                'texte',
    'branching_question':  "question d'embranchement",
    'course_presentation': 'présentation',
    'interactive_video':   'vidéo interactive',
    'video':               'vidéo',
    'image':               'image',
    'image_hotspots':      'image interactive',
    'multichoice':         'question à choix multiples',
    'truefalse':           'question vrai ou faux',
    'dragtext':            'texte à compléter en glissant des mots',
    'blanks':              'texte à trous',
    'singlechoiceset':     'série de questions',
    'markthewords':        'mots à repérer dans un texte',
    'summary':             'affirmations justes à choisir',
    'dragquestion':        'glisser-déposer sur une image',
    'dialogcards':         'cartes recto-verso',
}

#: Suffixe du second fichier produit (« parcours.h5p » -> « parcours-logiquiz.h5p »).
LOGIQUIZ_SUFFIX = '-logiquiz'

# ============================================================================
# VERSIONS H5P
# ============================================================================
# Aligne sur les versions installees dans les Moodle FR standards (Moodle 4.x).
# H5P.BranchingScenario 1.7 est la version stable presente dans la plupart des
# instances Moodle francaises (academies, lycees). Les versions 1.8+ ne sont
# pas garanties d etre installees, ce qui fait planter le rendu (bouton
# Continuer bloque, navigation cassee).
#
# Si tu cibles un Moodle qui a des versions plus recentes, modifie ces deux
# tables (CONTENT_TYPES et LIB_VERSIONS plus bas dans _get_dependencies).

#
# IMPORTANT : majorVersion et minorVersion DOIVENT etre des INTEGERS
# (pas des strings). Le H5P parser est strict sur les types et refuse
# les chaines "1"/"7". Reference : fichier .h5p produit par l app
# LABOMATHS qui marche en Moodle FR.

# Dossier des librairies H5P a bundler (template fat de reference).
# Un .h5p VALIDE doit embarquer un dossier par bibliotheque (library.json + JS + CSS).
# Un thin package (h5p.json + content.json seulement) ne fonctionne dans aucun player.
H5P_LIBS_DIR = Path(__file__).parent.parent / 'h5p_libs'

# Second jeu de librairies, aligne sur un lecteur H5P leger HORS LIGNE (Logiquiz,
# La Digitale). Ce n est PAS un socle reduit : Logiquiz possede tout, mais dans des
# versions PLUS RECENTES que les Moodle academiques vises par h5p_libs/.
#
# Mesure du 26/07/2026, faite sur un .h5p exporte depuis l installation reelle de
# l enseignant (et non sur le depot amont, qui n est qu un catalogue) :
#     H5P.BranchingScenario   1.8  -> 1.11      H5P.CoursePresentation 1.25 -> 1.27
#     H5P.InteractiveVideo    1.27 -> 1.28      H5P.ImageHotspots      1.10 -> 1.11
#     H5P.DragQuestion        1.14 -> 1.15      H5P.Components         absente -> 1.0
#
# Pourquoi c est bloquant : H5P resout une librairie par version EXACTE. Un contenu
# qui demande BranchingScenario 1.8 sur une installation qui n a que 1.10/1.11 ne
# resout pas la racine du parcours -> « TypeError: Cannot read properties of
# undefined (reading 'library') » -> TOUT le parcours reste vide, sans message.
# L echec est silencieux et TOTAL : meme les noeuds parfaitement supportes
# disparaissent.
#
# Rétro-compatibilite des schemas VERIFIEE le 26/07/2026 (diff des semantics.json) :
#   - InteractiveVideo 1.27 -> 1.28  : aucun changement structurel (2 libelles l10n,
#                                      option override/hasNoAutoPause).
#   - CoursePresentation 1.25 -> 1.27 : que des AJOUTS, aucune suppression.
# Le content.json produit pour Moodle est donc lisible tel quel par ces versions :
# la variante se contente de remapper les numeros et de bundler l autre jeu.
LOGIQUIZ_LIBS_DIR = Path(__file__).parent.parent / 'h5p_libs_logiquiz'

# Fallback si h5p_libs/ est absent : versions alignees sur les Moodle FR standards.
_LIB_VERSIONS_FALLBACK = {
    'H5P.BranchingScenario':  (1, 8),
    'H5P.CoursePresentation': (1, 25),
    'H5P.BranchingQuestion':  (1, 0),
    'H5P.AdvancedText':       (1, 1),
    'H5P.MultiChoice':        (1, 16),
    'H5P.TrueFalse':          (1, 8),
    'H5P.Blanks':             (1, 14),
    'H5P.DragText':           (1, 10),
    'H5P.SingleChoiceSet':    (1, 11),
    'H5P.MarkTheWords':       (1, 11),
    'H5P.InteractiveVideo':   (1, 27),
    'H5P.Image':              (1, 1),
    'H5P.ImageHotspots':      (1, 10),
    'H5P.Video':              (1, 6),
    'H5P.Summary':            (1, 10),
    'H5P.MathDisplay':        (1, 0),
    'H5P.JoubelUI':           (1, 3),
    'H5P.FontIcons':          (1, 0),
    'FontAwesome':            (4, 5),
    'H5P.Transition':         (1, 0),
    'H5P.Question':           (1, 5),
}


def _scan_lib_versions(libs_dir: Path = None) -> Dict:
    """Derive {machineName: (major, minor)} depuis les library.json reels d un
    dossier de librairies. SOURCE UNIQUE DE VERITE : les versions declarees dans
    h5p.json et content.json sont ainsi toujours alignees sur les libs
    effectivement bundlees. Tombe sur le fallback si le dossier est absent.

    libs_dir vaut h5p_libs/ (cible Moodle) par defaut ; passer LOGIQUIZ_LIBS_DIR
    pour deriver le jeu de versions du lecteur leger."""
    libs_dir = libs_dir or H5P_LIBS_DIR
    versions = dict(_LIB_VERSIONS_FALLBACK)
    if not libs_dir.is_dir():
        return versions
    for lib_dir in libs_dir.iterdir():
        lib_json = lib_dir / 'library.json'
        if not lib_json.is_file():
            continue
        try:
            meta = json.loads(lib_json.read_text(encoding='utf-8'))
            versions[meta['machineName']] = (
                int(meta['majorVersion']), int(meta['minorVersion'])
            )
        except (json.JSONDecodeError, KeyError, ValueError, OSError):
            continue
    return versions


LIB_VERSIONS = _scan_lib_versions()

#: Versions du lecteur leger, derivees des library.json de h5p_libs_logiquiz/.
#: Vide (= identique a LIB_VERSIONS) si le dossier n a pas ete constitue.
LOGIQUIZ_LIB_VERSIONS = _scan_lib_versions(LOGIQUIZ_LIBS_DIR)

SCORING_OPTIONS = ['no-score', 'static-end-score', 'dynamic-score']


def _lib(name: str) -> str:
    """« H5P.X maj.min » d'après LIB_VERSIONS (réservé aux types ajoutés le
    30/09/2026 : les fabriques plus anciennes gardent leurs chaînes en dur, pour
    que les archives existantes restent identiques octet pour octet)."""
    major, minor = LIB_VERSIONS.get(name, (1, 0))
    return f"{name} {major}.{minor}"


# ============================================================================
# IMAGES LOCALES (copiées dans l'archive)
# ============================================================================
# Un champ image du preplan peut être une CHAÎNE : chemin local, relatif au
# dossier du preplan (ou absolu). Le fichier est copié dans l'archive sous
# content/images/<nom>-<empreinte>.<ext>, et le champ devient l'objet image de
# H5P : {path, mime, width, height, copyright}. Un OBJET déjà au format H5P est
# repris tel quel (comportement historique du nœud 'image').

_IMAGE_MIMES = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                '.gif': 'image/gif'}


# _image_size (lecture des dimensions dans l'en-tête) vit dans validators.py,
# qui s'en sert aussi pour contrôler la hauteur d'un glisser-déposer.


class _AssetCollector:
    """Rassemble les images locales à copier dans content/images/."""

    def __init__(self, base_dir: Optional[Path] = None):
        # Sans base_dir, un chemin relatif se lit depuis le dossier de lancement.
        self.base_dir = Path(base_dir) if base_dir else None
        self.files: Dict[str, bytes] = {}      # nom dans l'archive -> octets
        self._by_source: Dict[str, Dict] = {}  # chemin absolu -> objet image

    def resolve(self, ref: str) -> Path:
        p = Path(ref)
        if p.is_absolute() or self.base_dir is None:
            return p
        return self.base_dir / p

    def image(self, ref: Any) -> Dict:
        """Objet image H5P pour `ref` (chaîne = chemin local, dict = repris)."""
        if isinstance(ref, dict) or not ref:
            return ref or {}
        src = self.resolve(str(ref)).resolve()
        key = str(src)
        if key in self._by_source:
            return dict(self._by_source[key])
        if not src.is_file():
            raise FileNotFoundError(f"Image introuvable : {src}")
        ext = src.suffix.lower()
        if ext not in _IMAGE_MIMES:
            raise ValueError(f"Format d'image non pris en charge ({ext}) : {src}. "
                             f"Formats admis : {', '.join(sorted(_IMAGE_MIMES))}")
        raw = src.read_bytes()
        width, height = _image_size(raw, ext)
        digest = hashlib.sha1(raw).hexdigest()[:8]
        stem = re.sub(r'[^A-Za-z0-9_-]+', '-', src.stem).strip('-') or 'image'
        name = f"images/{stem}-{digest}{ext}"
        self.files[name] = raw
        obj = {'path': name, 'mime': _IMAGE_MIMES[ext], 'width': width,
               'height': height, 'copyright': {'license': 'U'}}
        self._by_source[key] = obj
        return dict(obj)


#: Collecteur courant, réinitialisé par build_branching_scenario().
_ASSETS = _AssetCollector()


# ============================================================================
# HELPERS (L10N française)
# ============================================================================

def _get_ui_multichoice() -> Dict:
    return {
        'checkAnswerButton': 'Vérifier',
        'submitAnswerButton': 'Soumettre',
        'showSolutionButton': 'Voir la solution',
        'tryAgainButton': 'Réessayer',
        'tipsLabel': 'Indice',
        'scoreBarLabel': 'Score : :num sur :total',
        'tipAvailable': 'Indice disponible',
        'feedbackAvailable': 'Explication disponible',
        'readFeedback': "Lire l'explication",
        'wrongAnswer': 'Incorrect',
        'correctAnswer': 'Correct !',
        'shouldCheck': 'A cocher',
        'shouldNotCheck': 'A ne pas cocher',
        'noInput': 'Réponds avant de voir la solution',
        'a11yCheck': 'Vérifier les réponses.',
        'a11yShowSolution': 'Afficher la solution.',
        'a11yRetry': 'Recommencer.'
    }


def _get_confirm_dialog(header: str, body: str) -> Dict:
    return {
        'header': header,
        'body': body,
        'cancelLabel': 'Annuler',
        'confirmLabel': 'Valider'
    }


def _get_cp_l10n() -> Dict:
    """Localisation française complète pour CoursePresentation."""
    return {
        'slide': 'Slide', 'score': 'Score', 'yourScore': 'Ton score',
        'maxScore': 'Score max', 'total': 'Total',
        'totalScore': 'Score total', 'showSolutions': 'Solutions',
        'retry': 'Réessayer', 'exportAnswers': 'Exporter',
        'hideKeywords': 'Masquer mots-clés', 'showKeywords': 'Mots-clés',
        'fullscreen': 'Plein écran', 'exitFullscreen': 'Quitter plein écran',
        'prevSlide': 'Précédent', 'nextSlide': 'Suivant',
        'currentSlide': 'Slide actuelle', 'lastSlide': 'Dernière slide',
        'solutionModeTitle': 'Mode solutions', 'solutionModeText': 'Mode solutions',
        'summaryMultipleTaskText': 'Plusieurs exercices',
        'scoreMessage': ':achieved sur :max points',
        'shareFacebook': 'Partager sur Facebook',
        'shareTwitter': 'Partager sur Twitter',
        'shareGoogle': 'Partager sur Google+',
        'goToSlide': 'Aller à la slide :num',
        'solutionsButtonTitle': 'Voir la solution',
        'printTitle': 'Imprimer', 'printIng498': 'Préparation...',
        'printAllSlides': 'Tout imprimer', 'printCurrentSlide': 'Slide courante',
        'noTitle': 'Sans titre',
        'accessibilitySlideNavigationExplanation': 'Navigation slides',
        'accessibilityCanvasLabel': 'Contenu de la présentation',
        'containsNotCompleted': 'Contient @slideName incomplet',
        'containsCompleted': 'Contient @slideName complété',
        'slideCount': 'Slide @index sur @total',
        'containsOnlyCorrect': 'Tout correct',
        'containsIncorrectAnswers': 'Réponses incorrectes',
        'shareResult': 'Partager',
        'accessibilityTotalScore': 'Score total :score sur :maxScore',
        'accessibilityEnteredFullscreen': 'Plein écran',
        'accessibilityExitedFullscreen': 'Sorti du plein écran'
    }


# ============================================================================
# GENERATEURS D'INTERACTIONS (quiz embarques dans CoursePresentation)
# ============================================================================

def _make_cp_interaction_multichoice(interaction: Dict) -> Dict:
    """Genere un element multichoice pour CoursePresentation."""
    answers = []
    for ans in interaction.get('answers', []):
        answers.append({
            'correct': ans.get('correct', False),
            'tipsAndFeedback': {
                'tip': '',
                'chosenFeedback': f"<div>{ans.get('feedback', '')}</div>",
                'notChosenFeedback': ''
            },
            'text': f"<div>{ans.get('text', '')}</div>\n"
        })
    random.shuffle(answers)

    return {
        'x': interaction.get('x', 5),
        'y': interaction.get('y', 40),
        'width': interaction.get('width', 90),
        'height': interaction.get('height', 55),
        'action': {
            'params': {
                'media': {'disableImageZooming': False},
                'answers': answers,
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage ! Relis bien la question."},
                    {'from': 1, 'to': 99, 'feedback': "Presque ! Réfléchis encore."},
                    {'from': 100, 'to': 100, 'feedback': "Parfait !"}
                ],
                'behaviour': {
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'enableCheckButton': True,
                    'type': 'auto',
                    'singlePoint': False,
                    'randomAnswers': False,
                    'showSolutionsRequiresInput': True,
                    'passPercentage': 100,
                    'showScorePoints': True
                },
                'UI': _get_ui_multichoice(),
                'confirmCheck': _get_confirm_dialog('Valider ?', 'Es-tu sur de ta reponse ?'),
                'confirmRetry': _get_confirm_dialog('Reessayer ?', 'Tu vas recommencer cette question.'),
                'question': f"<p>{interaction.get('question', '')}</p>\n"
            },
            'library': 'H5P.MultiChoice 1.16',
            'metadata': {'contentType': 'Multiple Choice', 'license': 'U', 'title': 'Quiz'},
            'subContentId': str(uuid.uuid4())
        }
    }


def _make_cp_interaction_truefalse(interaction: Dict) -> Dict:
    """Genere un element truefalse pour CoursePresentation."""
    return {
        'x': interaction.get('x', 5),
        'y': interaction.get('y', 40),
        'width': interaction.get('width', 90),
        'height': interaction.get('height', 55),
        'action': {
            'params': {
                'media': {'disableImageZooming': False},
                'correct': 'true' if interaction.get('correct', True) else 'false',
                'behaviour': {
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'enableCheckButton': True,
                    'confirmCheckDialog': False,
                    'confirmRetryDialog': False,
                    'autoCheck': False
                },
                'l10n': {
                    'trueText': 'Vrai',
                    'falseText': 'Faux',
                    'score': 'Score : @score sur @total',
                    'checkAnswer': 'Vérifier',
                    'submitAnswer': 'Soumettre',
                    'showSolutionButton': 'Voir la solution',
                    'tryAgain': 'Réessayer',
                    'wrongAnswerMessage': interaction.get('feedback_incorrect', 'Incorrect.'),
                    'correctAnswerMessage': interaction.get('feedback_correct', 'Correct !'),
                    'scoreBarLabel': 'Score : :num sur :total',
                    'a11yCheck': 'Vérifier.', 'a11yShowSolution': 'Solution.', 'a11yRetry': 'Recommencer.'
                },
                'question': f"<p>{interaction.get('question', '')}</p>\n"
            },
            'library': 'H5P.TrueFalse 1.8',
            'metadata': {'contentType': 'True/False Question', 'license': 'U', 'title': 'Quiz'},
            'subContentId': str(uuid.uuid4())
        }
    }


def _make_cp_interaction_dragtext(interaction: Dict) -> Dict:
    """Genere un element dragtext pour CoursePresentation."""
    return {
        'x': interaction.get('x', 5),
        'y': interaction.get('y', 40),
        'width': interaction.get('width', 90),
        'height': interaction.get('height', 55),
        'action': {
            'params': {
                'media': {'disableImageZooming': False},
                'taskDescription': f"<p>{interaction.get('description', '')}</p>\n",
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage ! Réessaie !"},
                    {'from': 1, 'to': 99, 'feedback': "Presque ! Vérifie les derniers mots."},
                    {'from': 100, 'to': 100, 'feedback': "Parfait !"}
                ],
                'checkAnswer': 'Vérifier', 'submitAnswer': 'Soumettre',
                'tryAgain': 'Réessayer', 'showSolution': 'Voir la solution',
                'dropZoneIndex': 'Zone @index.', 'empty': 'Zone @index vide.',
                'contains': 'Zone @index contient @draggable.',
                'ariaDraggableIndex': '@index sur @count.',
                'tipLabel': 'Indice', 'correctText': 'Correct !', 'incorrectText': 'Incorrect',
                'resetDropTitle': 'Reinitialiser', 'resetDropDescription': 'Reinitialiser cette zone ?',
                'grabbed': 'Element selectionne.', 'cancelledDragging': 'Annule.',
                'correctAnswer': 'Réponse correcte :', 'feedbackHeader': 'Résultat',
                'behaviour': {
                    'enableRetry': True, 'enableSolutionsButton': True,
                    'enableCheckButton': True, 'instantFeedback': False
                },
                'scoreBarLabel': 'Score : :num sur :total',
                'textField': interaction.get('text', '')
            },
            'library': 'H5P.DragText 1.10',
            'metadata': {'contentType': 'Drag the Words', 'license': 'U', 'title': 'Quiz'},
            'subContentId': str(uuid.uuid4())
        }
    }


def _blanks_accept_spelling_errors(interaction: Dict) -> bool:
    """Tolérance aux fautes d'un texte à trous.

    Défaut historique : True (utile pour les mots). Désactivée par
    `numeric: true` (réponse chiffrée) ; `acceptSpellingErrors` explicite
    l'emporte sur tout.

    Mesure M4 (lecture de H5P.Blanks 1.14, js/cloze.js l. 43-60) : la tolérance
    ne distingue PAS les nombres. Elle ne dépend que de la longueur de la
    réponse attendue : plus de 3 caractères -> 1 erreur tolérée (distance de
    Damerau-Levenshtein), plus de 9 -> 2. Donc « 0,25 » accepte « 0,26 »,
    « 0,35 », « 0,2 » ou « 0,52 » ; « 1500 » accepte « 1600 ». Une réponse de
    3 caractères ou moins (« 0,4 ») n'a aucune tolérance.
    """
    if 'acceptSpellingErrors' in interaction:
        return bool(interaction['acceptSpellingErrors'])
    return not bool(interaction.get('numeric', False))


def _make_cp_interaction_blanks(interaction: Dict) -> Dict:
    """Genere un element blanks (texte a trous) pour CoursePresentation."""
    return {
        'x': interaction.get('x', 5),
        'y': interaction.get('y', 40),
        'width': interaction.get('width', 90),
        'height': interaction.get('height', 55),
        'action': {
            'params': {
                'media': {'disableImageZooming': False},
                'text': f"<p>{interaction.get('description', '')}</p>\n",
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage !"},
                    {'from': 1, 'to': 99, 'feedback': "Presque parfait !"},
                    {'from': 100, 'to': 100, 'feedback': "Excellent !"}
                ],
                'showSolutions': 'Voir la solution', 'tryAgain': 'Réessayer',
                'checkAnswer': 'Vérifier', 'submitAnswer': 'Soumettre',
                'notFilledOut': 'Complète tous les champs.',
                'answerIsCorrect': "« :ans » est correct.",
                'answerIsWrong': "« :ans » est incorrect.",
                'answeredCorrectly': 'Bonne réponse.',
                'answeredIncorrectly': 'Mauvaise réponse.',
                'solutionLabel': 'Réponse :', 'inputLabel': 'Champ @num sur @total',
                'inputHasTipLabel': 'Indice disponible', 'tipLabel': 'Indice',
                'behaviour': {
                    'enableRetry': True, 'enableSolutionsButton': True,
                    'enableCheckButton': True, 'autoCheck': False,
                    'caseSensitive': False, 'showSolutionsRequiresInput': True,
                    'separateLines': False,
                    'acceptSpellingErrors': _blanks_accept_spelling_errors(interaction)
                },
                'scoreBarLabel': 'Score : :num sur :total',
                'questions': [f"<p>{interaction.get('text', '')}</p>"]
            },
            'library': 'H5P.Blanks 1.14',
            'metadata': {'contentType': 'Fill in the Blanks', 'license': 'U', 'title': 'Quiz'},
            'subContentId': str(uuid.uuid4())
        }
    }


def _make_cp_interaction_singlechoiceset(interaction: Dict) -> Dict:
    """Genere un element singlechoiceset (serie de questions a choix unique) pour CoursePresentation."""
    questions = []
    for q in interaction.get('questions', []):
        answers_list = q.get('answers', [])
        # La premiere reponse est la correcte dans SingleChoiceSet
        questions.append({
            'question': f"<p>{q.get('question', '')}</p>",
            'answers': [f"<p>{a}</p>" for a in answers_list]
        })

    return {
        'x': interaction.get('x', 5),
        'y': interaction.get('y', 40),
        'width': interaction.get('width', 90),
        'height': interaction.get('height', 55),
        'action': {
            'params': {
                'choices': questions,
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage ! Relis bien les questions."},
                    {'from': 1, 'to': 99, 'feedback': "Presque ! Encore un effort."},
                    {'from': 100, 'to': 100, 'feedback': "Parfait ! Tout est correct !"}
                ],
                'behaviour': {
                    'autoContinue': True,
                    'timeoutCorrect': 2000,
                    'timeoutWrong': 3000,
                    'soundEffectsEnabled': True,
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'passPercentage': 100
                },
                'l10n': {
                    'nextButtonLabel': 'Suivant',
                    'showSolutionButtonLabel': 'Voir la solution',
                    'retryButtonLabel': 'Réessayer',
                    'solutionViewTitle': 'Mode solution',
                    'correctText': 'Correct !',
                    'incorrectText': 'Incorrect',
                    'muteButtonLabel': 'Couper le son',
                    'closeButtonLabel': 'Fermer',
                    'slideOfTotal': 'Question :num sur :total',
                    'scoreBarLabel': 'Score : :num sur :total',
                    'solutionListQuestionNumber': 'Question :num',
                    'a11yShowSolution': 'Afficher la solution.',
                    'a11yRetry': 'Recommencer.'
                }
            },
            'library': 'H5P.SingleChoiceSet 1.11',
            'metadata': {'contentType': 'Single Choice Set', 'license': 'U', 'title': 'Quiz rapide'},
            'subContentId': str(uuid.uuid4())
        }
    }


def _make_cp_interaction_markthewords(interaction: Dict) -> Dict:
    """Genere un element markthewords (marquer les mots corrects) pour CoursePresentation."""
    # Les mots a marquer sont entoures de *asterisques* dans le texte source
    text = interaction.get('text', '')

    return {
        'x': interaction.get('x', 5),
        'y': interaction.get('y', 40),
        'width': interaction.get('width', 90),
        'height': interaction.get('height', 55),
        'action': {
            'params': {
                'taskDescription': f"<p>{interaction.get('description', 'Marque les mots corrects.')}</p>\n",
                'textField': text,
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage ! Réessaie."},
                    {'from': 1, 'to': 99, 'feedback': "Presque ! Vérifie les derniers mots."},
                    {'from': 100, 'to': 100, 'feedback': "Parfait !"}
                ],
                'behaviour': {
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'enableCheckButton': True,
                    'showScorePoints': True
                },
                'checkAnswerButton': 'Vérifier',
                'submitAnswerButton': 'Soumettre',
                'tryAgainButton': 'Réessayer',
                'showSolutionButton': 'Voir la solution',
                'correctAnswer': 'Réponse correcte !',
                'incorrectAnswer': 'Réponse incorrecte.',
                'missedAnswer': 'Réponse manquee.',
                'displaySolutionDescription': 'La solution est affichee.',
                'scoreBarLabel': 'Score : :num sur :total'
            },
            'library': 'H5P.MarkTheWords 1.11',
            'metadata': {'contentType': 'Mark the Words', 'license': 'U', 'title': 'Marquer les mots'},
            'subContentId': str(uuid.uuid4())
        }
    }


# ----------------------------------------------------------------------------
# Types ajoutés le 30/09/2026 : summary, dragquestion, dialogcards
# Formats preplan documentés dans SKILL.md (« Activités variées ») et dans
# references/json-schema.md. Ne pas les modifier à la légère : des outils amont
# peuvent les reprendre tels quels.
# ----------------------------------------------------------------------------

def _html_block(text: str, tag: str = 'p', style: str = '') -> str:
    """Enveloppe un texte brut dans une balise ; laisse le HTML tel quel."""
    text = '' if text is None else str(text)
    if text.strip().startswith('<'):
        return text
    attr = f' style="{style}"' if style else ''
    return f"<{tag}{attr}>{text}</{tag}>"


def _element_box(interaction: Dict) -> Dict:
    """Position de l'élément dans la diapositive (en % de la diapositive)."""
    return {
        'x': interaction.get('x', 5),
        'y': interaction.get('y', 40),
        'width': interaction.get('width', 90),
        'height': interaction.get('height', 55),
    }


def _make_cp_interaction_summary(interaction: Dict) -> Dict:
    """Élément H5P.Summary : à chaque étape, choisir l'affirmation juste.

    Preplan : {"type": "summary", "intro": "...", "statements": [
                 {"correct": "...", "wrong": ["...", "..."], "tip": "..."}]}
    H5P attend l'affirmation juste EN PREMIER dans chaque groupe et mélange
    lui-même l'affichage (summary.js l. 201).
    """
    summaries = []
    for st in interaction.get('statements', []):
        group = {'summary': [_html_block(st.get('correct', ''))]
                 + [_html_block(w) for w in st.get('wrong', [])]}
        if st.get('tip'):
            group['tip'] = _html_block(st['tip'])
        summaries.append(group)

    return dict(_element_box(interaction), action={
        'params': {
            'intro': _html_block(interaction.get(
                'intro', "Choisis, à chaque étape, l'affirmation juste.")),
            'summaries': summaries,
            'overallFeedback': [
                {'from': 0, 'to': 49, 'feedback': "Relis le cours, puis recommence."},
                {'from': 50, 'to': 99, 'feedback': "Presque ! Quelques erreurs à revoir."},
                {'from': 100, 'to': 100, 'feedback': "Parfait !"}
            ],
            'solvedLabel': 'Progression :',
            'scoreLabel': 'Réponses fausses :',
            'resultLabel': 'Ton résultat',
            'labelCorrect': 'Juste.',
            'labelIncorrect': 'Faux ! Essaie encore.',
            'alternativeIncorrectLabel': 'Faux',
            'labelCorrectAnswers': 'Affirmations justes.',
            'tipButtonLabel': "Afficher l'indice",
            'scoreBarLabel': 'Tu as obtenu :num points sur :total',
            'progressText': 'Étape :num sur :total'
        },
        'library': _lib('H5P.Summary'),
        'metadata': {'contentType': 'Summary', 'license': 'U',
                     'title': interaction.get('title', 'Résumé')},
        'subContentId': str(uuid.uuid4())
    })


#: Taille par défaut d'une étiquette à glisser, en % du cadre de l'image.
DRAG_LABEL_W, DRAG_LABEL_H = 12, 9

#: Largeur de référence (size.width) d'un glisser-déposer : la police vaut
#: 16 px x largeur affichée / DRAG_REF_WIDTH. 640 donne environ 15 px pour un
#: élément de 56 % dans une diapositive de 1060 px de large.
DRAG_REF_WIDTH = 640


def _layout_draggables(draggables: List[Dict]) -> List[Tuple[float, float, float, float]]:
    """Position (x, y, l, h) en % de chaque étiquette. Celles qui n'ont pas de
    x/y sont rangées en rangées centrées dans la BANDE DU BAS de l'image
    (l'image doit y réserver une zone libre : 12 % de hauteur par rangée)."""
    boxes = [None] * len(draggables)
    free = [k for k, d in enumerate(draggables) if 'x' not in d or 'y' not in d]
    rows, row, row_w = [], [], 0.0
    for k in free:
        w = draggables[k].get('width', DRAG_LABEL_W)
        if row and row_w + w + 2 > 96:
            rows.append(row)
            row, row_w = [], 0.0
        row.append(k)
        row_w += w + 2
    if row:
        rows.append(row)
    y = 100.0
    for r in reversed(rows):
        h_row = max(draggables[k].get('height', DRAG_LABEL_H) for k in r)
        y -= h_row + 1.5
        total = sum(draggables[k].get('width', DRAG_LABEL_W) for k in r) + 2 * (len(r) - 1)
        x = (100 - total) / 2
        for k in r:
            w = draggables[k].get('width', DRAG_LABEL_W)
            boxes[k] = (round(x, 2), round(y, 2), w, draggables[k].get('height', DRAG_LABEL_H))
            x += w + 2
    for k, d in enumerate(draggables):
        if boxes[k] is None:
            boxes[k] = (d['x'], d['y'], d.get('width', DRAG_LABEL_W),
                        d.get('height', DRAG_LABEL_H))
    return boxes


def _make_cp_interaction_dragquestion(interaction: Dict) -> Dict:
    """Élément H5P.DragQuestion : glisser des étiquettes sur une image.

    Preplan : {"type": "dragquestion", "image": "chemin/local.png",
               "zones": [{"label": "...", "x": %, "y": %, "width": %,
                          "height": %, "correct": [indices d'étiquettes]}],
               "draggables": [{"text": "...", "x"?: %, "y"?: %,
                               "width"?: %, "height"?: %}]}
    Toutes les positions sont en POURCENTAGES du cadre de l'image (coin haut
    gauche + taille). Conversion vers H5P (h5p-drag-question.js) : x et y
    restent en %, largeur et hauteur passent en em, avec
    1 em = largeur affichée / size.width x 16 px, soit
    largeur_em = largeur_% x size.width / 1600 (idem en hauteur).
    size ne sert que de RÉFÉRENCE d'échelle (le cadre prend toute la largeur
    disponible) : on la fixe à DRAG_REF_WIDTH de large, aux proportions de
    l'image. Avec la largeur réelle de l'image (1000 px), les étiquettes
    s'écrivaient en 11 px environ dans une diapositive (mesuré le 30/09/2026).
    """
    image = _ASSETS.image(interaction.get('image'))
    src_w = int(image.get('width') or 800)
    src_h = int(image.get('height') or 450)
    img_w = int(interaction.get('scaleWidth', DRAG_REF_WIDTH))
    img_h = max(1, round(img_w * src_h / src_w))

    def em(pct: float, px: int) -> float:
        return round(float(pct) * px / 1600.0, 4)

    zones_in = interaction.get('zones', [])
    drags_in = interaction.get('draggables', [])
    all_zones = [str(z) for z in range(len(zones_in))]

    elements = []
    for (x, y, w, h), d in zip(_layout_draggables(drags_in), drags_in):
        allowed = d.get('allowedZones')
        elements.append({
            'type': {
                'params': {'text': f"<p style=\"text-align:center\">{d.get('text', '')}</p>"},
                'library': 'H5P.AdvancedText 1.1',
                'metadata': {'contentType': 'Text', 'license': 'U',
                             'title': re.sub(r'<[^>]+>', '', str(d.get('text', '')))[:60]},
                'subContentId': str(uuid.uuid4())
            },
            'x': x, 'y': y, 'width': em(w, img_w), 'height': em(h, img_h),
            'dropZones': [str(z) for z in allowed] if allowed is not None else list(all_zones),
            'backgroundOpacity': 100,
            'multiple': bool(d.get('multiple', False))
        })

    drop_zones = []
    for z_idx, z in enumerate(zones_in):
        drop_zones.append({
            'label': f"<div>{z.get('label', f'Zone {z_idx + 1}')}</div>",
            'showLabel': bool(z.get('showLabel', False)),
            'x': z.get('x', 0), 'y': z.get('y', 0),
            'width': em(z.get('width', 10), img_w),
            'height': em(z.get('height', 10), img_h),
            'correctElements': [str(k) for k in z.get('correct', [])],
            'backgroundOpacity': interaction.get('zoneOpacity', 40),
            'tipsAndFeedback': {
                'tip': z.get('tip', ''),
                'feedbackOnCorrect': z.get('feedbackCorrect', ''),
                'feedbackOnIncorrect': z.get('feedbackIncorrect', '')
            },
            'single': bool(z.get('single', False)),
            'autoAlign': bool(z.get('autoAlign', True))
        })

    return dict(_element_box(interaction), action={
        'params': {
            'scoreShow': 'Vérifier',
            'submit': 'Soumettre',
            'tryAgain': 'Réessayer',
            'scoreExplanation': ("Une étiquette bien placée rapporte 1 point, une "
                                 "étiquette mal placée en retire 1. Le score ne "
                                 "descend jamais sous 0."),
            'question': {
                'settings': {'background': image,
                             'size': {'width': img_w, 'height': img_h}},
                'task': {'elements': elements, 'dropZones': drop_zones}
            },
            'overallFeedback': [
                {'from': 0, 'to': 49, 'feedback': "Regarde bien la figure et recommence."},
                {'from': 50, 'to': 99, 'feedback': "Presque ! Vérifie les étiquettes en rouge."},
                {'from': 100, 'to': 100, 'feedback': "Parfait !"}
            ],
            'behaviour': {
                'enableRetry': True,
                'enableCheckButton': True,
                'singlePoint': False,
                'applyPenalties': bool(interaction.get('penalties', False)),
                'enableScoreExplanation': bool(interaction.get('penalties', False)),
                'dropZoneHighlighting': interaction.get('zoneHighlight', 'dragging'),
                'autoAlignSpacing': 2,
                'enableFullScreen': False,
                'showScorePoints': True,
                'showTitle': False
            },
            'localize': {'fullscreen': 'Plein écran',
                         'exitFullscreen': 'Quitter le plein écran'},
            'grabbablePrefix': 'Étiquette {num} sur {total}.',
            'grabbableSuffix': 'Placée dans la zone {num}.',
            'dropzonePrefix': 'Zone {num} sur {total}.',
            'noDropzone': 'Aucune zone.',
            'tipLabel': "Afficher l'indice.",
            'tipAvailable': 'Indice disponible',
            'correctAnswer': 'Bonne réponse',
            'wrongAnswer': 'Mauvaise réponse',
            'feedbackHeader': 'Retour',
            'scoreBarLabel': 'Tu as obtenu :num points sur :total',
            'scoreExplanationButtonLabel': "Afficher l'explication du score",
            'a11yCheck': ("Vérifier les réponses. Chaque réponse sera marquée "
                          "juste, fausse ou sans réponse."),
            'a11yRetry': "Recommencer l'exercice depuis le début."
        },
        'library': _lib('H5P.DragQuestion'),
        'metadata': {'contentType': 'Drag and Drop', 'license': 'U',
                     'title': interaction.get('title', 'Glisser-déposer')},
        'subContentId': str(uuid.uuid4())
    })


def _make_cp_interaction_dialogcards(interaction: Dict) -> Dict:
    """Élément H5P.Dialogcards : cartes recto-verso (mémorisation).

    Preplan : {"type": "dialogcards", "title"?: "...", "description"?: "...",
               "cards": [{"front": "...", "back": "...", "tipFront"?: "...",
                          "tipBack"?: "...", "image"?: "chemin/local.png"}],
               "mode"?: "normal" | "repetition", "random"?: false}
    """
    center = 'text-align: center;'
    dialogs = []
    for card in interaction.get('cards', []):
        dialog = {
            'text': _html_block(card.get('front', ''), 'p', center),
            'answer': _html_block(card.get('back', ''), 'p', center),
            'tips': {'front': card.get('tipFront', ''), 'back': card.get('tipBack', '')}
        }
        if card.get('image'):
            dialog['image'] = _ASSETS.image(card['image'])
            dialog['imageAltText'] = card.get('imageAlt', '')
        dialogs.append(dialog)

    mode = interaction.get('mode', 'normal')
    return dict(_element_box(interaction), action={
        'params': {
            'title': _html_block(interaction.get('title', '')) if interaction.get('title') else '',
            'mode': mode if mode in ('normal', 'repetition') else 'normal',
            'description': _html_block(interaction.get(
                'description', 'Lis le recto, réponds dans ta tête, puis retourne la carte.')),
            'dialogs': dialogs,
            'behaviour': {
                'enableRetry': True,
                'disableBackwardsNavigation': False,
                'scaleTextNotCard': False,
                'randomCards': bool(interaction.get('random', False)),
                'maxProficiency': 5,
                'quickProgression': False
            },
            'answer': 'Retourner',
            'next': 'Suivante',
            'prev': 'Précédente',
            'retry': 'Recommencer',
            'correctAnswer': 'Je savais !',
            'incorrectAnswer': 'Je ne savais pas',
            'round': 'Tour @round',
            'cardsLeft': 'Cartes restantes : @number',
            'nextRound': 'Passer au tour @round',
            'startOver': 'Tout recommencer',
            'showSummary': 'Suivant',
            'summary': 'Bilan',
            'summaryCardsRight': 'Cartes sues :',
            'summaryCardsWrong': 'Cartes à revoir :',
            'summaryCardsNotShown': 'Cartes pas encore montrées :',
            'summaryOverallScore': 'Score global',
            'summaryCardsCompleted': 'Cartes maîtrisées :',
            'summaryCompletedRounds': 'Tours terminés :',
            'summaryAllDone': ('Bravo ! Tu maîtrises les @cards cartes, '
                               'chacune réussie @max fois !'),
            'progressText': 'Carte @card sur @total',
            'cardFrontLabel': 'Recto',
            'cardBackLabel': 'Verso',
            'tipButtonLabel': "Afficher l'indice",
            'audioNotSupported': 'Ton navigateur ne peut pas lire ce son',
            'confirmStartingOver': {
                'header': 'Tout recommencer ?',
                'body': ('Toute ta progression sera perdue. Veux-tu vraiment '
                         'recommencer ?'),
                'cancelLabel': 'Annuler',
                'confirmLabel': 'Recommencer'
            }
        },
        'library': _lib('H5P.Dialogcards'),
        'metadata': {'contentType': 'Dialog Cards', 'license': 'U',
                     'title': re.sub(r'<[^>]+>', '', str(interaction.get('title', ''))) or 'Cartes'},
        'subContentId': str(uuid.uuid4())
    })


def _make_cp_interaction_image(interaction: Dict) -> Dict:
    """Élément H5P.Image posé dans une diapositive (ajout du 04/10/2026).

    Sert à garder le CONTEXTE d'une question (tableau, arbre) sous les yeux de
    l'élève : AdvancedText n'autorise ni <img> ni <table> (sémantique de
    CoursePresentation 1.25), Moodle les retirerait à l'import.

    Preplan : {"type": "image", "image": "chemin/local.png", "alt": "...",
               "x": .., "y": .., "width": .., "height": ..}
    L'image est étirée à la taille de l'élément : choisir
    height = width x 1,98 x (hauteur / largeur de l'image) pour garder ses
    proportions (le validateur le vérifie).
    """
    alt = interaction.get('alt', '') or 'Figure'
    return {
        'x': interaction.get('x', 2),
        'y': interaction.get('y', 30),
        'width': interaction.get('width', 45),
        'height': interaction.get('height', 60),
        'action': {
            'params': {
                'contentName': 'Image',
                'file': _ASSETS.image(interaction.get('image')),
                'alt': alt,
                'title': alt,
                'decorative': False,
                'expandImage': "Agrandir l'image",
                'minimizeImage': "Réduire l'image",
            },
            'library': _lib('H5P.Image'),
            'metadata': {'contentType': 'Image', 'license': 'U', 'title': alt[:60]},
            'subContentId': str(uuid.uuid4())
        }
    }


def _make_cp_interaction_notice(interaction: Dict) -> Dict:
    """Encart de texte remplacant une interaction non supportee par le lecteur.

    Type INTERNE ('__notice__') : jamais ecrit par un auteur, produit uniquement
    par degrade_for_logiquiz(). Reprend les coordonnees de l interaction
    remplacee, pour que la mise en page de la slide reste identique.
    """
    return {
        'x': interaction.get('x', 5),
        'y': interaction.get('y', 40),
        'width': interaction.get('width', 90),
        'height': interaction.get('height', 55),
        'action': {
            'params': {'text': interaction.get('html', '<p>Exercice non disponible.</p>')},
            'library': 'H5P.AdvancedText 1.1',
            'metadata': {'contentType': 'AdvancedText', 'license': 'U',
                         'title': 'Exercice non disponible'},
            'subContentId': str(uuid.uuid4())
        }
    }


CP_INTERACTION_GENERATORS = {
    'multichoice': _make_cp_interaction_multichoice,
    'truefalse': _make_cp_interaction_truefalse,
    'dragtext': _make_cp_interaction_dragtext,
    'blanks': _make_cp_interaction_blanks,
    'singlechoiceset': _make_cp_interaction_singlechoiceset,
    'markthewords': _make_cp_interaction_markthewords,
    'summary': _make_cp_interaction_summary,
    'dragquestion': _make_cp_interaction_dragquestion,
    'dialogcards': _make_cp_interaction_dialogcards,
    'image': _make_cp_interaction_image,
    '__notice__': _make_cp_interaction_notice,
}


# ============================================================================
# GENERATEURS DE NOEUDS
# ============================================================================

def make_advanced_text(node: Dict) -> Dict:
    """Genere un noeud H5P.AdvancedText."""
    content = node.get('content', '<p>Contenu vide</p>')
    if not content.strip().startswith('<'):
        content = f"<p>{content}</p>"

    return {
        'params': {'text': content},
        'library': 'H5P.AdvancedText 1.1',
        'metadata': {
            'contentType': 'AdvancedText', 'license': 'U',
            'title': node.get('title', 'Texte')
        },
        'subContentId': str(uuid.uuid4())
    }


def make_branching_question(node: Dict) -> Dict:
    """Genere un noeud H5P.BranchingQuestion."""
    question = node.get('question', node.get('content', ''))
    if not question.strip().startswith('<'):
        question = f"<p>{question}</p>"

    alternatives = []
    for alt in node.get('alternatives', []):
        alt_obj = {
            'text': alt.get('text', ''),
            'nextContentId': alt.get('nextContentId', -1),
        }
        feedback = alt.get('feedback', {})
        if feedback:
            alt_obj['feedback'] = {
                'title': feedback.get('title', ''),
                'subtitle': feedback.get('subtitle', ''),
                'endScreenScore': feedback.get('score', 0)
            }
        alternatives.append(alt_obj)

    return {
        'params': {
            'branchingQuestion': {
                'question': question,
                'alternatives': alternatives
            }
        },
        'library': 'H5P.BranchingQuestion 1.0',
        'metadata': {
            'contentType': 'Branching Question', 'license': 'U',
            'title': node.get('title', 'Question')
        },
        'subContentId': str(uuid.uuid4())
    }


def make_course_presentation(node: Dict) -> Dict:
    """Genere un noeud H5P.CoursePresentation avec quiz embarques."""
    slides_data = node.get('slides', [])
    if not slides_data:
        slides_data = [{'content': node.get('content', '<p>Slide</p>')}]

    slides = []
    for slide in slides_data:
        content = slide.get('content', '<p></p>')
        if not content.strip().startswith('<'):
            content = f"<p>{content}</p>"

        # Disposition : 'full' (defaut, comportement historique) ou
        # 'text-left' / 'text-top' (texte et activite cote a cote / superposes)
        layout = slide_layout_boxes(slide)
        tb = layout['text']

        # Element texte de base (toujours present)
        elements = [{
            'x': tb['x'], 'y': tb['y'], 'width': tb['width'], 'height': tb['height'],
            'action': {
                'params': {'text': content},
                'library': 'H5P.AdvancedText 1.1',
                'metadata': {'contentType': 'AdvancedText', 'license': 'U', 'title': ''},
                'subContentId': str(uuid.uuid4())
            }
        }]

        # Interactions (quiz embarques)
        interactions = slide.get('interactions', [])
        for interaction in interactions:
            int_type = interaction.get('type', 'multichoice')
            generator = CP_INTERACTION_GENERATORS.get(int_type)
            if generator:
                if layout['interaction']:
                    # Les coordonnees propres a l'interaction priment
                    interaction = {**layout['interaction'], **interaction}
                elements.append(generator(interaction))

        slides.append({
            'elements': elements,
            'slideBackgroundSelector': {}
        })

    return {
        'params': {
            'presentation': {
                'slides': slides,
                'keywordListEnabled': False,
                'globalBackgroundSelector': {},
                'keywordListAlwaysShow': False,
                'keywordListAutoHide': False,
                'keywordListOpacity': 90
            },
            'override': {
                'activeSurface': False,
                'hideSummarySlide': False,
                'summarySlideSolutionButton': True,
                'summarySlideRetryButton': False,
                'enablePrintButton': False,
                'social': {
                    'showFacebookShare': False,
                    'facebookShare': {'url': '', 'quote': ''},
                    'showTwitterShare': False,
                    'twitterShare': {'statement': '', 'url': '', 'hashtags': ''}
                }
            },
            'l10n': _get_cp_l10n()
        },
        'library': CONTENT_TYPES['course_presentation'],
        'metadata': {
            'contentType': 'Course Presentation', 'license': 'U',
            'title': node.get('title', 'Presentation')
        },
        'subContentId': str(uuid.uuid4())
    }


def make_interactive_video(node: Dict) -> Dict:
    """Genere un noeud H5P.InteractiveVideo avec questions a des timestamps."""
    url = node.get('videoUrl', node.get('url', ''))
    is_youtube = 'youtube' in url or 'youtu.be' in url

    sources = []
    if url:
        sources.append({
            'path': url,
            'mime': 'video/YouTube' if is_youtube else 'video/mp4',
            'copyright': {'license': 'U'}
        })

    # Interactions aux timestamps
    interactions_data = node.get('interactions', [])
    h5p_interactions = []
    for interaction in interactions_data:
        time = interaction.get('time', 0)
        int_type = interaction.get('type', 'multichoice')
        duration = interaction.get('duration', 10)

        # Generer le contenu de l'interaction
        if int_type == 'multichoice':
            answers = []
            for ans in interaction.get('answers', []):
                # CORRIGE 26/07/2026 : chosenFeedback etait force a '' ici, alors que
                # _make_cp_interaction_multichoice (meme fichier) l honore depuis toujours.
                # Consequence : les feedbacks rediges pour les questions incrustees dans une
                # video etaient presents dans le preplan et DETRUITS a la generation — un eleve
                # qui se trompait dans une video n avait aucun retour, en silence.
                fb = ans.get('feedback', '')
                answers.append({
                    'correct': ans.get('correct', False),
                    'tipsAndFeedback': {
                        'tip': '',
                        'chosenFeedback': f"<div>{fb}</div>" if fb else '',
                        'notChosenFeedback': ''
                    },
                    'text': f"<div>{ans.get('text', '')}</div>\n"
                })
            random.shuffle(answers)

            action = {
                'params': {
                    'media': {'disableImageZooming': False},
                    'answers': answers,
                    'overallFeedback': [{'from': 0, 'to': 100}],
                    'behaviour': {
                        'enableRetry': True, 'enableSolutionsButton': True,
                        'enableCheckButton': True, 'type': 'auto',
                        'singlePoint': False, 'randomAnswers': False,
                        'showSolutionsRequiresInput': True, 'passPercentage': 100,
                        'showScorePoints': True
                    },
                    'UI': _get_ui_multichoice(),
                    'question': f"<p>{interaction.get('question', '')}</p>\n"
                },
                'library': 'H5P.MultiChoice 1.16',
                'metadata': {'contentType': 'Multiple Choice', 'license': 'U', 'title': 'Question'},
                'subContentId': str(uuid.uuid4())
            }
        elif int_type == 'truefalse':
            action = {
                'params': {
                    'media': {'disableImageZooming': False},
                    'correct': 'true' if interaction.get('correct', True) else 'false',
                    'behaviour': {
                        'enableRetry': True, 'enableSolutionsButton': True,
                        'enableCheckButton': True
                    },
                    'l10n': {
                        'trueText': 'Vrai', 'falseText': 'Faux',
                        'score': 'Score : @score sur @total',
                        'checkAnswer': 'Vérifier',
                        'showSolutionButton': 'Voir la solution',
                        'tryAgain': 'Réessayer',
                        'wrongAnswerMessage': interaction.get('feedback_incorrect', 'Incorrect.'),
                        'correctAnswerMessage': interaction.get('feedback_correct', 'Correct !')
                    },
                    'question': f"<p>{interaction.get('question', '')}</p>\n"
                },
                'library': 'H5P.TrueFalse 1.8',
                'metadata': {'contentType': 'True/False Question', 'license': 'U', 'title': 'Question'},
                'subContentId': str(uuid.uuid4())
            }
        else:
            continue

        h5p_interactions.append({
            'x': interaction.get('x', 10),
            'y': interaction.get('y', 10),
            'width': interaction.get('width', 80),
            'height': interaction.get('height', 60),
            'duration': {'from': time, 'to': time + duration},
            'pause': interaction.get('pause', True),
            'adaptivity': {
                'correct': {'seekTo': 0, 'allowOptOut': True, 'message': ''},
                'wrong': {'seekTo': 0, 'allowOptOut': True, 'message': ''}
            },
            'label': interaction.get('label', f'Question a {time}s'),
            'action': action
        })

    return {
        'params': {
            'interactiveVideo': {
                'video': {
                    'startScreenOptions': {
                        'title': node.get('title', 'Video interactive'),
                        'hideStartTitle': False
                    },
                    'textTracks': {'videoTrack': []},
                    'files': sources
                },
                'assets': {
                    'interactions': h5p_interactions,
                    'bookmarks': [],
                    'endscreens': [{
                        'time': 0,
                        'label': 'Fin'
                    }]
                },
                'summary': {
                    'task': {
                        'params': {'text': ''},
                        'library': 'H5P.Summary 1.10',
                        'metadata': {'contentType': 'Summary', 'license': 'U', 'title': 'Résumé'},
                        'subContentId': str(uuid.uuid4())
                    },
                    'displayAt': 3
                }
            },
            'override': {
                'autoplay': False,
                'loop': False,
                'showBookmarksmenuOnLoad': False,
                'showRewind10': False,
                'preventSkipping': False,
                'deactivateSound': False
            },
            'l10n': {
                'interaction': 'Interaction',
                'play': 'Lire', 'pause': 'Pause',
                'mute': 'Couper le son', 'unmute': 'Activer le son',
                'quality': 'Qualité', 'captions': 'Sous-titres',
                'close': 'Fermer', 'fullscreen': 'Plein ecran',
                'exitFullscreen': 'Quitter plein écran',
                'summary': 'Résumé', 'bookmarks': 'Signets',
                'defaultAdaptivitySeekLabel': 'Retour a @timecode',
                'continueWithVideo': 'Continuer la video',
                'playbackRate': 'Vitesse',
                'rewind10': 'Reculer 10s',
                'navDisabled': 'Navigation désactivée',
                'sndDisabled': 'Son désactivé',
                'requiresCompletionWarning': 'Réponds a toutes les questions pour continuer',
                'back': 'Retour', 'hours': 'Heures',
                'minutes': 'Minutes', 'seconds': 'Secondes',
                'currentTime': 'Temps actuel',
                'totalTime': 'Durée totale',
                'singleInteractionAnnouncement': 'Interaction apparue',
                'multipleInteractionsAnnouncement': 'Interactions apparues',
                'videoPausedAnnouncement': 'Video en pause',
                'content': 'Contenu',
                'answered': '@answered sur @total repondues',
                'endcardTitle': 'Résumé',
                'endcardInformationText': 'Tu as repondu a @answered sur @total questions.',
                'endcardInformationNo498': 'Tu as termine la video.',
                'endcardInformationMustHaveCompletedText': 'Réponds a toutes les questions.',
                'endcardSubmitButton': 'Soumettre',
                'endcardSubmitMessage': 'Réponses soumises !',
                'endcardTableRowAnswered': 'Repondues',
                'endcardTableRowScore': 'Score',
                'endcardAnsweredScore': 'repondues',
                'endCardTableRowSummaryWithScore': '@score sur @total pour Q@question'
            }
        },
        'library': CONTENT_TYPES['interactive_video'],
        'metadata': {
            'contentType': 'Interactive Video', 'license': 'U',
            'title': node.get('title', 'Video interactive')
        },
        'subContentId': str(uuid.uuid4())
    }


def make_image(node: Dict) -> Dict:
    """Genere un noeud H5P.Image."""
    # Une chaîne = chemin local, copié dans l'archive (ajout du 30/09/2026) ;
    # un objet est repris tel quel (comportement historique, inchangé).
    image = node.get('image', {})
    return {
        'params': {
            'file': _ASSETS.image(image) if isinstance(image, str) else image,
            'alt': node.get('alt', node.get('title', 'Image')),
            'title': node.get('title', 'Image')
        },
        'library': 'H5P.Image 1.1',
        'metadata': {
            'contentType': 'Image', 'license': 'U',
            'title': node.get('title', 'Image')
        },
        'subContentId': str(uuid.uuid4())
    }


#: Icônes admises par H5P.ImageHotspots 1.10 (semantics.json, champ « icon »).
HOTSPOT_ICONS = ('plus', 'minus', 'times', 'check', 'question', 'info', 'exclamation')


def make_image_hotspots(node: Dict) -> Dict:
    """Nœud H5P.ImageHotspots : image à zones cliquables (découverte).

    NŒUD et non élément de diapositive : CoursePresentation 1.25 n'autorise
    pas cette librairie dans une diapositive, BranchingScenario 1.8 l'autorise
    comme nœud.

    Preplan : {"type": "image_hotspots", "title": "...", "image": "local.png",
               "alt"?: "...", "icon"?: "plus", "color"?: "#1f6feb",
               "hotspots": [{"x": %, "y": %, "width"?: %, "height"?: %,
                             "header": "...", "text": "<p>...</p>"}]}
    Une zone est un POINT : (x, y) en % du cadre de l'image désigne le CENTRE
    de l'icône (hotspot.js l. 76-77 + CSS translate(-50%, -50%), mode non
    hérité). Si width/height sont donnés, x/y décrivent un rectangle (coin haut
    gauche) et l'icône est placée en son centre.
    """
    hotspots = []
    for hs in node.get('hotspots', []):
        x = float(hs.get('x', 50))
        y = float(hs.get('y', 50))
        if 'width' in hs or 'height' in hs:
            x += float(hs.get('width', 0)) / 2
            y += float(hs.get('height', 0)) / 2
        # image-hotspots.js l. 119 rejette une position nulle (test de vérité).
        x = min(max(round(x, 2), 0.01), 100)
        y = min(max(round(y, 2), 0.01), 100)
        hotspots.append({
            'position': {'x': x, 'y': y, 'legacyPositioning': False},
            'alwaysFullscreen': bool(hs.get('fullscreen', False)),
            'header': hs.get('header', ''),
            'content': [{
                'params': {'text': _html_block(hs.get('text', ''))},
                'library': _lib('H5P.Text'),
                'metadata': {'contentType': 'Text', 'license': 'U',
                             'title': hs.get('header', 'Zone') or 'Zone'},
                'subContentId': str(uuid.uuid4())
            }]
        })

    icon = node.get('icon', 'plus')
    return {
        'params': {
            'image': _ASSETS.image(node.get('image')),
            'backgroundImageAltText': node.get('alt', node.get('title', 'Image')),
            'iconType': 'icon',
            'icon': icon if icon in HOTSPOT_ICONS else 'plus',
            'color': node.get('color', '#981d99'),
            'hotspots': hotspots,
            'hotspotNumberLabel': 'Zone n° #num',
            'closeButtonLabel': 'Fermer',
            'containsAudioVideoLabel': 'Contient du son ou de la vidéo'
        },
        'library': CONTENT_TYPES['image_hotspots'],
        'metadata': {
            'contentType': 'Image Hotspots', 'license': 'U',
            'title': node.get('title', 'Image interactive')
        },
        'subContentId': str(uuid.uuid4())
    }


def make_video(node: Dict) -> Dict:
    """Genere un noeud H5P.Video (YouTube ou fichier)."""
    sources = []
    url = node.get('videoUrl', node.get('url', ''))
    if url:
        sources.append({
            'path': url,
            'mime': 'video/YouTube' if 'youtube' in url or 'youtu.be' in url else 'video/mp4',
            'copyright': {'license': 'U'}
        })

    return {
        'params': {
            'sources': sources,
            'visuals': {'fit': True, 'controls': True},
            'playback': {'autoplay': False, 'loop': False}
        },
        'library': 'H5P.Video 1.6',
        'metadata': {
            'contentType': 'Video', 'license': 'U',
            'title': node.get('title', 'Video')
        },
        'subContentId': str(uuid.uuid4())
    }


# ============================================================================
# CONSTRUCTION DU BRANCHING SCENARIO
# ============================================================================

GENERATORS = {
    'text': make_advanced_text,
    'branching_question': make_branching_question,
    'course_presentation': make_course_presentation,
    'interactive_video': make_interactive_video,
    'image': make_image,
    'image_hotspots': make_image_hotspots,
    'video': make_video,
}


# ----------------------------------------------------------------------------
# forceContentFinished PAR NOEUD
# ----------------------------------------------------------------------------
# semantics.json de H5P.BranchingScenario 1.8 declare DEUX champs homonymes de
# types DIFFERENTS :
#   branchingScenario.content[].forceContentFinished -> "select" (CHAINE),
#       optionnel, defaut 'useBehavioural', options useBehavioural|enabled|disabled
#   branchingScenario.behaviour.forceContentFinished -> "boolean", defaut false
# Le lecteur compare le champ PAR NOEUD en === STRICT sur des chaines
# (src/scripts/libraryScreen.js l. 524-527, identique dans le dist/ minifie) :
#   forceContentFinished === 'enabled'
#   || (forceContentFinished === 'useBehavioural' && behaviour.forceContentFinished === true)
# => un BOOLEEN ne satisfait aucune branche : il neutralise en silence le
# reglage global, noeud par noeud. C'est ce que ce fichier ecrivait jusqu'au
# 25/07/2026. Mesure dans h5p-standalone, paquets identiques a un champ pres :
#   booleen false + global true      -> bouton « Continuer » ACTIF (aucun verrou)
#   'useBehavioural' + global true   -> bouton verrouille, « Terminez le contenu »
#   booleen true  + global false     -> aucun verrou
#   'enabled'     + global false     -> verrouille
# Le champ voisin contentBehaviour, lui aussi de type select, a toujours ete
# ecrit correctement (chaine) : c'etait une erreur, pas une convention.
FORCE_FINISHED_VALUES = ('useBehavioural', 'enabled', 'disabled')

# Seuls ces deux types savent signaler leur achevement via xAPI. Sur les autres,
# un verrou n'est jamais leve : l'eleve reste bloque pour toujours. On y ecrit
# donc 'disabled' (valeur VALIDE du schema, qui signifie « ne verrouille jamais »)
# et non 'useBehavioural', qui suivrait un reglage global a true et bloquerait.
FORCE_FINISHED_CAPABLE = ('course_presentation', 'interactive_video')


def _resolve_force_content_finished(raw: Any, ntype: str, index: int,
                                    title: str) -> Tuple[str, Optional[str]]:
    """Resout le forceContentFinished d un noeud vers une des 3 chaines du schema.

    Retourne (valeur, message a afficher ou None). Ne leve jamais : un preplan
    fautif doit produire un fichier sain et un avertissement lisible.
    """
    tag = f"  ! Noeud {index} ({title})"
    msg = None

    if raw is None:
        value = 'useBehavioural'          # defaut du schema : suit le global
    elif raw is True:                     # ancien format booleen
        value = 'enabled'
    elif raw is False:                    # ancien format booleen
        value = 'useBehavioural'
    elif isinstance(raw, str) and raw in FORCE_FINISHED_VALUES:
        value = raw
    else:
        value = 'useBehavioural'
        msg = (f"{tag}: forceContentFinished={raw!r} hors schema "
               f"(valeurs admises : {', '.join(FORCE_FINISHED_VALUES)}) "
               f"-> 'useBehavioural' applique")

    if ntype not in FORCE_FINISHED_CAPABLE and value != 'disabled':
        if value == 'enabled' or raw is True:
            extra = (f"{tag}: le verrou « terminer avant de continuer » est "
                     f"impossible sur un noeud {ntype} (jamais de signal "
                     f"« finished ») -> 'disabled' applique")
            msg = f"{msg}\n{extra}" if msg else extra
        # Implicite : un texte/une image ne doit pas heriter d un global a true,
        # sans quoi le bouton « Continuer » resterait verrouille indefiniment.
        value = 'disabled'

    return value, msg


def build_branching_scenario(data: Dict, base_dir: Optional[Path] = None) -> Tuple[Dict, Dict]:
    """Construit le content.json et h5p.json du Branching Scenario.

    base_dir : dossier de référence des chemins d'images locales (celui du
    preplan). Les images rencontrées sont rassemblées dans _ASSETS.files, que
    generate_h5p() copie dans content/images/."""
    global _ASSETS
    _ASSETS = _AssetCollector(base_dir)

    nodes = data.get('nodes', [])
    scoring = data.get('scoring', 'no-score')

    # Construire les noeuds de contenu
    content_list = []
    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        generator = GENERATORS.get(ntype, make_advanced_text)
        h5p_content = generator(node)

        # nextContentId :
        # - branching_question : TOUJOURS -1 au top-level. Le routage se fait
        #   via alternatives[].nextContentId. Reference : H5P qui marche en
        #   Moodle FR via l app LABOMATHS.
        # - autres : index du noeud suivant ou -1 si terminal.
        if ntype == 'branching_question':
            next_id = -1
        else:
            next_id = node.get('nextContentId',
                               i + 1 if i < len(nodes) - 1 else -1)

        # CRITIQUE : forceContentFinished au niveau NOEUD est une CHAINE
        # ('useBehavioural' | 'enabled' | 'disabled'), jamais un booleen.
        # Voir le bloc de commentaire de _resolve_force_content_finished :
        # le lecteur H5P compare en === strict, un booleen desactive le verrou
        # en silence, y compris quand le reglage global le demande.
        force_finished, ff_msg = _resolve_force_content_finished(
            node.get('forceContentFinished'), ntype, i, node.get('title', '?'))
        if ff_msg:
            print(ff_msg)

        # Le contentTitle est un champ separe du metadata.title.
        # Affiche dans la barre du parcours selon showContentTitle.
        title = node.get('title', '')

        # showContentTitle par defaut : false (comportement LABOMATHS).
        # L auteur peut explicitement passer showTitle: true.
        show_title = node.get('showTitle', False)

        content_item = {
            'type': h5p_content,
            'showContentTitle': show_title,
            'contentTitle': title,
            'forceContentFinished': force_finished,
            'nextContentId': next_id,
            'contentBehaviour': 'useBehavioural',
        }

        # proceedButtonText : present sur les noeuds de CONTENU (text, image,
        # video, course_presentation, interactive_video) mais ABSENT sur les
        # branching_question (qui n ont pas de bouton Continuer, l utilisateur
        # clique directement sur une alternative).
        # Sans ce champ, le player affiche "proceed" (texte anglais par defaut).
        if ntype != 'branching_question':
            content_item['proceedButtonText'] = node.get('proceedText', 'Continuer')

        # feedback top-level : TOUJOURS present sur tous les noeuds, meme vide.
        # Reference LABOMATHS : { title: "", subtitle: "", endScreenScore: 0 }
        # est present systematiquement. L absence de ce champ casse le rendu
        # de certains players. Pas de champ "image" ici (LABOMATHS ne l a pas).
        feedback = node.get('feedback', {})
        content_item['feedback'] = {
            'title': feedback.get('title', ''),
            'subtitle': feedback.get('subtitle', ''),
            'endScreenScore': feedback.get('score', 0),
        }

        content_list.append(content_item)

    # Post-processing scoring
    _postprocess_scoring(content_list, nodes, data)

    # NOTE : on ne fait PLUS de _ensure_endscreens_coverage. Le format
    # LABOMATHS qui marche n a qu un seul endScreen generique. Si l auteur
    # veut des paliers de score multiples, il les fournit explicitement
    # dans data['endScreens'].

    # endScreens : format LABOMATHS = un seul endScreen generique en texte pur
    # (PAS de wrapping <p><strong>...</strong></p>). Le H5P player ajoute le
    # styling lui-meme. Plusieurs endScreens supportes mais l auteur doit les
    # fournir explicitement.
    end_screens_in = data.get('endScreens', [])
    if not end_screens_in:
        end_screens = [{
            'endScreenTitle': 'Fin du parcours',
            'endScreenSubtitle': 'Vous avez termine ce parcours pedagogique.',
            'contentId': -1,
            'endScreenScore': 0,
            'endScreenImage': {}
        }]
    else:
        end_screens = []
        for es in end_screens_in:
            end_screens.append({
                'endScreenTitle': es.get('title', 'Fin'),
                'endScreenSubtitle': es.get('subtitle', ''),
                'contentId': es.get('contentId', -1),
                'endScreenScore': es.get('score', 0),
                'endScreenImage': es.get('image', {}),
            })

    # startScreen : titre/sous-titre en TEXTE PUR (pas de wrapping HTML).
    # Le H5P player gere le rendu lui-meme.
    start_screen = data.get('startScreen', {})
    start_title = start_screen.get('title', data.get('title', 'Parcours'))
    start_subtitle = start_screen.get('subtitle', '')

    # content.json - Ordre des cles aligne sur LABOMATHS qui marche.
    content_json = {
        'branchingScenario': {
            'startScreen': {
                'startScreenTitle': start_title,
                'startScreenSubtitle': start_subtitle,
                'startScreenImage': start_screen.get('image', {}),
            },
            'endScreens': end_screens,
            'content': content_list,
            'scoringOptionGroup': {
                'scoringOption': scoring,
                'includeInteractionsScores': data.get('includeInteractionsScores', True)
            },
            'behaviour': {
                'enableBackwardsNavigation': data.get('enableBackwardsNavigation', True),
                'forceContentFinished': data.get('forceContentFinished', False),
                'randomizeBranchingQuestions': data.get('randomizeBranchingQuestions', True)
            },
            'l10n': {
                'startScreenButtonText': 'Commencer le parcours',
                'endScreenButtonText': 'Recommencer le parcours',
                'proceedButtonText': 'Continuer',
                'scoreText': 'Votre score :',
                'fullScoreText': 'Score maximum',
                'currentOfTotal': '@current sur @total questions',
                'backButtonText': 'Retour',
                'replayButtonText': 'Rejouer',
                'disableProceedButtonText': 'Terminez le contenu pour continuer'
            }
        }
    }

    # h5p.json - license "U" comme LABOMATHS, PAS "CC BY-SA"
    h5p_json = {
        'title': data.get('title', 'Parcours adaptatif'),
        'language': 'fr',
        'mainLibrary': 'H5P.BranchingScenario',
        'preloadedDependencies': _get_dependencies(nodes),
        'embedTypes': ['iframe'],
        'license': 'U',
    }

    return content_json, h5p_json


def _postprocess_scoring(content_list: List[Dict], nodes: List[Dict], data: Dict):
    """Post-processing : aligne le feedback top-level sur le score eventuel
    defini par l auteur dans node.feedback.score.

    Le feedback top-level est deja present sur tous les noeuds (cf.
    build_branching_scenario qui le cree systematiquement). On se contente
    ici de propager le score si l auteur en a defini un.
    """
    scoring = data.get('scoring', 'no-score')
    if scoring == 'no-score':
        return

    for content_item, node in zip(content_list, nodes):
        node_feedback = node.get('feedback', {})
        score = node_feedback.get('score')
        if score is not None and 'feedback' in content_item:
            content_item['feedback']['endScreenScore'] = score


def _ensure_endscreens_coverage(data: Dict, content_list: List[Dict], nodes: List[Dict]):
    """Auto-génère les endScreens manquants pour couvrir tous les scores."""
    end_screens = data.get('endScreens', [])
    if not end_screens:
        return  # endScreens vides, pas de coverage check

    # Collecter tous les scores utilisés
    scores_used = set()
    for content_item in content_list:
        feedback = content_item.get('feedback', {})
        if 'endScreenScore' in feedback:
            scores_used.add(feedback['endScreenScore'])

    # Scores couverts
    scores_covered = set(es.get('score', 0) for es in end_screens)

    # Auto-générer les manquants
    missing = scores_used - scores_covered
    if missing:
        for score in sorted(missing):
            generic_title = f"Score {score}"
            new_es = {
                'endScreenTitle': f"<p><strong>{generic_title}</strong></p>",
                'endScreenSubtitle': '<p>Fin du parcours</p>',
                'endScreenScore': score,
                'contentId': -1
            }
            end_screens.append(new_es)
            print(f"  i endScreen auto-généré : score={score}")


def _dep(name: str) -> Dict:
    """Construit une entree preloadedDependency a partir de LIB_VERSIONS."""
    major, minor = LIB_VERSIONS.get(name, ('1', '0'))
    return {'machineName': name, 'majorVersion': major, 'minorVersion': minor}


def _get_dependencies(nodes: List[Dict]) -> List[Dict]:
    """Retourne les dependances H5P selon les types utilises.

    Toutes les versions sont centralisees dans LIB_VERSIONS pour faciliter
    l adaptation a un Moodle cible.
    """
    # Coeur prouve (issu du .h5p de reference qui s'importe en Moodle FR) :
    # inclut les libs support (JoubelUI, FontIcons, FontAwesome, Transition,
    # Question) et H5P.MathDisplay pour le rendu MathJax des maths.
    base = [
        _dep('H5P.BranchingScenario'),
        _dep('H5P.BranchingQuestion'),
        _dep('H5P.AdvancedText'),
        _dep('H5P.MultiChoice'),
        _dep('H5P.CoursePresentation'),
        _dep('H5P.JoubelUI'),
        _dep('H5P.FontIcons'),
        _dep('FontAwesome'),
        _dep('H5P.Transition'),
        _dep('H5P.Question'),
        _dep('H5P.MathDisplay'),
    ]

    type_deps = {
        'course_presentation': _dep('H5P.CoursePresentation'),
        'interactive_video':   _dep('H5P.InteractiveVideo'),
        'image':               _dep('H5P.Image'),
        'image_hotspots':      _dep('H5P.ImageHotspots'),
        'video':               _dep('H5P.Video'),
    }

    # Dependances des quiz embarques
    quiz_deps = {
        'multichoice':     _dep('H5P.MultiChoice'),
        'truefalse':       _dep('H5P.TrueFalse'),
        'dragtext':        _dep('H5P.DragText'),
        'blanks':          _dep('H5P.Blanks'),
        'singlechoiceset': _dep('H5P.SingleChoiceSet'),
        'markthewords':    _dep('H5P.MarkTheWords'),
        'summary':         _dep('H5P.Summary'),
        'dragquestion':    _dep('H5P.DragQuestion'),
        'dialogcards':     _dep('H5P.Dialogcards'),
        'image':           _dep('H5P.Image'),
    }

    types_used = set(n.get('type', 'text') for n in nodes)

    for t in types_used:
        dep = type_deps.get(t)
        if dep and dep not in base:
            base.append(dep)

    # Detecter les quiz embarques dans les CoursePresentation et InteractiveVideo
    interaction_types_used = set()
    for node in nodes:
        ntype = node.get('type', 'text')
        if ntype == 'course_presentation':
            for slide in node.get('slides', []):
                for interaction in slide.get('interactions', []):
                    interaction_types_used.add(interaction.get('type', ''))
        elif ntype == 'interactive_video':
            for interaction in node.get('interactions', []):
                interaction_types_used.add(interaction.get('type', ''))

    # Tri : ordre stable d'une exécution à l'autre (l'ordre d'un set varie).
    # Pour les anciens types, l'ordre est sans effet : chacun n'est ajouté
    # qu'une fois et H5P ne dépend pas de l'ordre des preloadedDependencies.
    for t in sorted(interaction_types_used):
        dep = quiz_deps.get(t)
        if dep and dep not in base:
            if t == 'summary' and any(d['machineName'] == 'H5P.Summary' for d in base):
                continue
            base.append(dep)

    # InteractiveVideo necessite H5P.Summary
    if 'interactive_video' in types_used:
        summary_dep = {'machineName': 'H5P.Summary', 'majorVersion': '1', 'minorVersion': '10'}
        if summary_dep not in base and not any(
                d['machineName'] == 'H5P.Summary' for d in base):
            base.append(summary_dep)

    # Dépendances de contenu des types ajoutés le 30/09/2026 (les dépendances
    # des librairies elles-mêmes — jQuery.ui, JoubelUI, Question... — sont
    # résolues par H5P depuis leur library.json ; tout h5p_libs/ est embarqué).
    if 'image_hotspots' in types_used:
        base.append(_dep('H5P.Text'))                 # contenu des bulles

    return base


# ============================================================================
# VARIANTE LOGIQUIZ : DEGRADATION EN PLACE
# ============================================================================
# Voir le bloc LOGIQUIZ_SUPPORTED_LIBRARIES en tete de fichier pour la source
# du releve et la facon de l elargir.

def _supports_node(ntype: str) -> bool:
    """Le lecteur leger sait-il instancier ce type de noeud ?"""
    return NODE_TYPE_LIBRARY.get(ntype) in LOGIQUIZ_SUPPORTED_LIBRARIES


def _supports_interaction(int_type: str) -> bool:
    """Le lecteur leger sait-il instancier ce type d interaction embarquee ?"""
    return INTERACTION_LIBRARY.get(int_type) in LOGIQUIZ_SUPPORTED_LIBRARIES


def _esc(text: str) -> str:
    """Echappe le strict necessaire pour une insertion dans du HTML."""
    return (str(text).replace('&', '&amp;')
                     .replace('<', '&lt;')
                     .replace('>', '&gt;')
                     .replace('"', '&quot;'))


def _notice_node_html(title: str, ntype: str, video_url: str = '') -> str:
    """Message affiche a la place d un noeud non supporte (francais simple).

    Tournure sans determinant genre (« type : ... ») : les libelles de
    TYPE_LABELS_FR n ont pas tous le meme genre, et la liste est appelee a
    s allonger.
    """
    label = TYPE_LABELS_FR.get(ntype, ntype)
    parts = [
        f"<p><strong>{_esc(title)}</strong></p>",
        f"<p>Ce bloc (type : {label}) ne peut pas s'afficher dans le logiciel "
        f"utilisé pour lire ce parcours. Il a été remplacé par ce message pour "
        f"que la suite du parcours continue de fonctionner.</p>",
    ]
    if video_url:
        url = _esc(video_url)
        parts.append(
            f'<p>Tu peux la regarder dans ton navigateur : '
            f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>, '
            f'puis revenir ici et cliquer sur « Continuer ».</p>')
    return '\n'.join(parts)


def _notice_interaction_html(int_type: str) -> str:
    """Message affiche a la place d une interaction non supportee."""
    label = TYPE_LABELS_FR.get(int_type, int_type)
    return (f"<p><strong>Exercice non disponible</strong></p>\n"
            f"<p>Cet exercice (type : {label}) ne peut pas s'afficher dans le "
            f"logiciel utilisé pour lire ce parcours.</p>")


def degrade_for_logiquiz(data: Dict) -> Tuple[Dict, Dict]:
    """Retourne (copie degradee du preplan, rapport des substitutions).

    REGLE DE SURETE, a ne jamais assouplir : on ne supprime JAMAIS un noeud ni
    une slide. Un noeud non supporte est remplace EN PLACE par un noeud 'text'
    qui conserve son INDICE, son nextContentId, son titre et son feedback (donc
    son score). Le routage du parcours est bit pour bit celui de la version
    Moodle : aucun indice ne bouge, aucune cible d alternative n est recalculee.

    Meme principe au niveau des slides : une interaction non supportee devient
    un encart de texte aux memes coordonnees, la slide n est jamais supprimee,
    meme si elle ne contenait que cette interaction.
    """
    degraded = copy.deepcopy(data)
    nodes_replaced = []
    interactions_replaced = []

    for i, node in enumerate(degraded.get('nodes', [])):
        ntype = node.get('type', 'text')
        title = node.get('title', 'Bloc sans titre')

        # 1. Noeud entier non supporte -> noeud text, indice et routage conserves
        if not _supports_node(ntype):
            video_url = node.get('videoUrl', node.get('url', '')) \
                if ntype in ('interactive_video', 'video') else ''

            replacement = {
                'type': 'text',
                'title': title,
                'content': _notice_node_html(title, ntype, video_url),
            }
            # Champs de routage et de score : repris a l identique.
            for key in ('nextContentId', 'feedback', 'showTitle'):
                if key in node:
                    replacement[key] = node[key]
            # forceContentFinished volontairement abandonne : un noeud text ne
            # signale jamais son achevement, le verrou y serait definitif
            # (_resolve_force_content_finished ecrira 'disabled').

            node.clear()
            node.update(replacement)

            nodes_replaced.append({
                'index': i,
                'title': title,
                'type': ntype,
                'library': NODE_TYPE_LIBRARY.get(ntype, '?'),
                'videoUrl': video_url,
            })
            continue

        # 2. Interactions embarquees non supportees -> encart de texte
        if ntype == 'course_presentation':
            for s_idx, slide in enumerate(node.get('slides', [])):
                for k, interaction in enumerate(slide.get('interactions', [])):
                    int_type = interaction.get('type', 'multichoice')
                    if _supports_interaction(int_type):
                        continue

                    notice = {
                        'type': '__notice__',
                        'html': _notice_interaction_html(int_type),
                    }
                    for dim in ('x', 'y', 'width', 'height'):
                        if dim in interaction:
                            notice[dim] = interaction[dim]
                    slide['interactions'][k] = notice

                    interactions_replaced.append({
                        'node': i,
                        'node_title': title,
                        'slide': s_idx + 1,
                        'index': k + 1,
                        'type': int_type,
                        'library': INTERACTION_LIBRARY.get(int_type, '?'),
                    })

    substitutions = {
        'supported_libraries': sorted(LOGIQUIZ_SUPPORTED_LIBRARIES),
        'nodes_replaced': nodes_replaced,
        'interactions_replaced': interactions_replaced,
    }
    return degraded, substitutions


def generate_logiquiz_variant(data: Dict, moodle_output_path: str,
                              degrade: bool = False,
                              base_dir: Optional[Path] = None) -> Tuple[Optional[str], Dict]:
    """Genere la seconde archive, destinee a un lecteur H5P leger hors ligne.

    Mode NOMINAL (degrade=False) : le contenu est integralement conserve — videos
    interactives comprises — et seules les VERSIONS de librairies sont realignees
    sur celles du lecteur, avec le jeu h5p_libs_logiquiz/ embarque. C est la cause
    reelle de l ecran vide observe le 26/07/2026 : un decalage de versions, pas une
    librairie manquante (voir le commentaire de LOGIQUIZ_LIBS_DIR).

    Mode DEGRADE (degrade=True, jamais par defaut) : recours pour un lecteur qui
    ne possede REELLEMENT pas une librairie. Les elements hors socle sont
    substitues en place par un texte de remplacement. A n employer qu apres avoir
    verifie que le realignement de versions ne suffit pas — il ampute le parcours.

    Retourne (chemin, infos), ou (None, infos) si aucune seconde archive n est
    necessaire (pas de jeu de librairies leger disponible, ou rien a degrader).
    """
    src = Path(moodle_output_path)
    logiquiz_path = str(src.with_name(f"{src.stem}{LOGIQUIZ_SUFFIX}{src.suffix}"))

    if degrade:
        degraded, substitutions = degrade_for_logiquiz(data)
        if not substitutions['nodes_replaced'] and not substitutions['interactions_replaced']:
            return None, substitutions
        generate_h5p(degraded, logiquiz_path, base_dir=base_dir)
        substitutions['mode'] = 'degrade'
        return logiquiz_path, substitutions

    if not LOGIQUIZ_LIBS_DIR.is_dir():
        return None, {
            'mode': 'versions', 'nodes_replaced': [], 'interactions_replaced': [],
            'skipped': f"{LOGIQUIZ_LIBS_DIR.name}/ absent : variante non produite",
        }

    generate_h5p(data, logiquiz_path,
                 libs_dir=LOGIQUIZ_LIBS_DIR, lib_versions=LOGIQUIZ_LIB_VERSIONS,
                 base_dir=base_dir)

    remapped = sorted(
        f"{name} {LIB_VERSIONS[name][0]}.{LIB_VERSIONS[name][1]}"
        f" -> {LOGIQUIZ_LIB_VERSIONS[name][0]}.{LOGIQUIZ_LIB_VERSIONS[name][1]}"
        for name in LOGIQUIZ_LIB_VERSIONS
        if name in LIB_VERSIONS and LIB_VERSIONS[name] != LOGIQUIZ_LIB_VERSIONS[name]
    )
    return logiquiz_path, {
        'mode': 'versions', 'nodes_replaced': [], 'interactions_replaced': [],
        'remapped': remapped,
    }


# ============================================================================
# GENERATION DU FICHIER H5P
# ============================================================================

def generate_assembly_report(data: Dict, output_path: str) -> Dict:
    """Genère un rapport d'assemblage détaillé du scénario H5P."""
    nodes = data.get('nodes', [])
    end_screens = data.get('endScreens', [])

    # Compter les types de noeuds
    types_used = {}
    for node in nodes:
        ntype = node.get('type', 'text')
        types_used[ntype] = types_used.get(ntype, 0) + 1

    # Noeuds terminaux
    terminal_nodes = []
    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        if ntype == 'branching_question':
            for alt in node.get('alternatives', []):
                if alt.get('nextContentId', 0) == -1:
                    terminal_nodes.append(i)
                    break
        elif node.get('nextContentId', 0) == -1:
            terminal_nodes.append(i)

    # Scores uniques
    score_tiers = set()
    for node in nodes:
        feedback = node.get('feedback', {})
        if 'score' in feedback:
            score_tiers.add(feedback['score'])
        if node.get('type', 'text') == 'branching_question':
            for alt in node.get('alternatives', []):
                alt_feedback = alt.get('feedback', {})
                if 'score' in alt_feedback:
                    score_tiers.add(alt_feedback['score'])

    # Compter les quiz
    quiz_count = 0
    for node in nodes:
        ntype = node.get('type', 'text')
        if ntype == 'course_presentation':
            for slide in node.get('slides', []):
                quiz_count += len(slide.get('interactions', []))
        elif ntype == 'interactive_video':
            quiz_count += len(node.get('interactions', []))

    # Graph stats via BFS
    adj = {i: set() for i in range(len(nodes))}
    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        if ntype == 'branching_question':
            for alt in node.get('alternatives', []):
                next_id = alt.get('nextContentId', -1)
                if 0 <= next_id < len(nodes):
                    adj[i].add(next_id)
        else:
            next_id = node.get('nextContentId', -1)
            if 0 <= next_id < len(nodes):
                adj[i].add(next_id)

    # BFS pour max_depth
    visited = {0: 0}
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for neighbor in adj[current]:
            if neighbor not in visited:
                visited[neighbor] = visited[current] + 1
                queue.append(neighbor)

    max_depth = max(visited.values()) if visited else 0

    # Branching questions
    nb_branches = sum(1 for n in nodes if n.get('type', 'text') == 'branching_question')

    # Convergence points (noeuds avec plusieurs arêtes entrantes)
    incoming_edges = {i: 0 for i in range(len(nodes))}
    for i in range(len(nodes)):
        for neighbor in adj[i]:
            incoming_edges[neighbor] += 1
    nb_convergence = sum(1 for count in incoming_edges.values() if count > 1)

    report = {
        'title': data.get('title', 'Sans titre'),
        'output': output_path,
        'nb_nodes': len(nodes),
        'types_used': types_used,
        'scoring': data.get('scoring', 'no-score'),
        'nb_endscreens': len(end_screens),
        'terminal_nodes': terminal_nodes,
        'score_tiers': sorted(list(score_tiers)),
        'nb_quiz_total': quiz_count,
        'graph_stats': {
            'max_depth': max_depth,
            'nb_branches': nb_branches,
            'nb_convergence_points': nb_convergence
        }
    }

    return report


def _normalize_latex(obj):
    """Normalise les commandes LaTeX non supportees par MathJax dans H5P.

    Walker recursif qui modifie en place toutes les strings du dict/list.
    Substitutions :
      - \\dfrac{a}{b} -> \\displaystyle\\frac{a}{b}  (MathJax H5P ne connait pas \\dfrac)
      - \\tfrac{a}{b} -> \\textstyle\\frac{a}{b}     (idem)
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = _normalize_latex(v)
        return obj
    if isinstance(obj, list):
        return [_normalize_latex(x) for x in obj]
    if isinstance(obj, str):
        s = obj
        s = s.replace('\\dfrac', '\\displaystyle\\frac')
        s = s.replace('\\tfrac', '\\textstyle\\frac')
        return s
    return obj


def _collect_library_refs(obj, refs: set):
    """Collecte toute valeur 'library': 'H5P.X maj.min', a tous les niveaux
    d imbrication (noeuds, interactions de slides, interactions video)."""
    if isinstance(obj, dict):
        lib = obj.get('library')
        if isinstance(lib, str) and ' ' in lib:
            refs.add(lib)
        for v in obj.values():
            _collect_library_refs(v, refs)
    elif isinstance(obj, list):
        for v in obj:
            _collect_library_refs(v, refs)


def _remap_library_versions(obj, versions: Dict) -> int:
    """Reecrit EN PLACE toute cle 'library' vers la version de `versions`.

    Le nom de la librairie est conserve, seul le couple maj.min change. Utilise
    pour produire une variante alignee sur un lecteur dont les librairies sont
    plus recentes, SANS toucher a la structure du contenu (les schemas concernes
    sont retro-compatibles, cf. le commentaire de LOGIQUIZ_LIBS_DIR).
    Retourne le nombre de references reecrites."""
    n = 0
    if isinstance(obj, dict):
        lib = obj.get('library')
        if isinstance(lib, str) and ' ' in lib:
            name, _ = lib.rsplit(' ', 1)
            if name in versions:
                new = f"{name} {versions[name][0]}.{versions[name][1]}"
                if new != lib:
                    obj['library'] = new
                    n += 1
        for v in obj.values():
            n += _remap_library_versions(v, versions)
    elif isinstance(obj, list):
        for v in obj:
            n += _remap_library_versions(v, versions)
    return n


def _expand_dependencies(deps: List[Dict], libs_dir: Path) -> List[Dict]:
    """Ferme transitivement les dependances en lisant les library.json du jeu
    de librairies vise, et realigne chaque version sur celle du dossier.

    Necessaire car un jeu plus recent introduit des dependances que la table
    statique ignore : H5P.Components 1.0, par exemple, est exigee par
    InteractiveVideo 1.28, CoursePresentation 1.27 et Question 1.5, mais
    n existe dans aucune version du jeu Moodle."""
    if not libs_dir.is_dir():
        return deps

    index = {}
    for lib_dir in libs_dir.iterdir():
        lj = lib_dir / 'library.json'
        if not lj.is_file():
            continue
        try:
            meta = json.loads(lj.read_text(encoding='utf-8'))
            index[meta['machineName']] = (
                int(meta['majorVersion']), int(meta['minorVersion']),
                meta.get('preloadedDependencies', []) or [],
            )
        except (json.JSONDecodeError, KeyError, ValueError, OSError):
            continue

    seen, out, queue = set(), [], [d.get('machineName') for d in deps]
    while queue:
        name = queue.pop(0)
        if not name or name in seen or name not in index:
            continue
        seen.add(name)
        major, minor, sub = index[name]
        out.append({'machineName': name, 'majorVersion': major, 'minorVersion': minor})
        queue.extend(d.get('machineName') for d in sub)
    return out


def _verify_content_libs_bundled(content_json: Dict, libs_dir: Path = None) -> List[str]:
    """Verifie que CHAQUE 'library': 'H5P.X maj.min' reference dans content.json
    correspond a un dossier present dans le jeu de librairies vise. Retourne la
    liste des references manquantes (vide = OK). Empeche les bugs 'version
    mismatch' ou 'lib introuvable' silencieux a l'import."""
    libs_dir = libs_dir or H5P_LIBS_DIR
    refs = set()
    _collect_library_refs(content_json, refs)
    missing = []
    for ref in sorted(refs):
        name, ver = ref.rsplit(' ', 1)
        folder = libs_dir / f"{name}-{ver}"
        if not folder.is_dir():
            missing.append(ref)
    return missing


def _bundle_libraries(zf: zipfile.ZipFile, h5p_json: Dict, libs_dir: Path = None) -> int:
    """Copie TOUTES les librairies du jeu vise dans le .h5p.

    Un package H5P valide doit embarquer un dossier par bibliotheque
    (library.json + scripts + styles). On bundle l'ensemble du template fat
    de reference (set prouve qui s'importe en Moodle FR) plutot qu'un
    sous-ensemble minimal, pour garantir la resolution des dependances
    transitives. Retourne le nombre de fichiers copies."""
    libs_dir = libs_dir or H5P_LIBS_DIR
    if not libs_dir.is_dir():
        raise FileNotFoundError(
            f"Dossier des librairies introuvable : {libs_dir}\n"
            "Sans bundling, le .h5p est 'thin' et ne s'importe dans AUCUN player.\n"
            "Restaurer le dossier depuis un .h5p fat de reference."
        )
    n = 0
    for path in sorted(libs_dir.rglob('*')):
        if path.is_file():
            arcname = path.relative_to(libs_dir).as_posix()
            zf.write(path, arcname)
            n += 1
    return n


def generate_h5p(data: Dict, output_path: str, libs_dir: Path = None,
                 lib_versions: Dict = None, base_dir: Optional[Path] = None) -> Tuple[str, Dict]:
    """Genere le fichier .h5p final (FAT, importable) et retourne chemin + rapport.

    libs_dir / lib_versions permettent de produire la meme structure de contenu
    contre un autre jeu de librairies (cf. generate_logiquiz_variant). Par
    defaut : h5p_libs/ et LIB_VERSIONS, c est-a-dire la cible Moodle.
    base_dir : dossier des chemins d'images locales (celui du preplan)."""
    libs_dir = libs_dir or H5P_LIBS_DIR
    content_json, h5p_json = build_branching_scenario(data, base_dir=base_dir)
    assets = dict(_ASSETS.files)

    # Normalisation LaTeX : \dfrac -> \displaystyle\frac (non supporte par MathJax H5P)
    content_json = _normalize_latex(content_json)

    # Variante : realignement des versions declarees sur le jeu de librairies vise.
    # La STRUCTURE du contenu n est jamais touchee, seuls les numeros de version.
    if lib_versions:
        _remap_library_versions(content_json, lib_versions)
        _remap_library_versions(h5p_json, lib_versions)
        h5p_json['preloadedDependencies'] = _expand_dependencies(
            h5p_json.get('preloadedDependencies', []), libs_dir
        )

    # Garde-fou : toute lib referencee dans content.json doit etre bundlable.
    missing = _verify_content_libs_bundled(content_json, libs_dir)
    if missing:
        raise ValueError(
            f"Librairies referencees dans content.json mais absentes de {libs_dir.name}/ :\n  "
            + "\n  ".join(missing)
            + f"\nAjouter ces libs (bonnes versions) dans {libs_dir.name}/ avant de generer."
        )

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
        zf.writestr('content/content.json', json.dumps(content_json, ensure_ascii=False, indent=2))
        for arc_name, raw in sorted(assets.items()):      # images locales
            zf.writestr(f'content/{arc_name}', raw)
        n_lib_files = _bundle_libraries(zf, h5p_json, libs_dir)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(buf.getvalue())

    print(f"  i Librairies bundlees : {n_lib_files} fichiers (package fat)")
    if assets:
        print(f"  i Images embarquées : {len(assets)} (content/images/)")

    report = generate_assembly_report(data, output_path)

    return output_path, report


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Genere un H5P Branching Scenario depuis un preplan JSON '
                    '(version Moodle + version « -logiquiz » si necessaire)'
    )
    parser.add_argument('--input', '-i', required=True, help='Fichier JSON du preplan')
    parser.add_argument('--output', '-o',
                        help='Fichier H5P de sortie (version Moodle ; la version '
                             'lecteur leger prend le suffixe -logiquiz)')
    parser.add_argument('--validate', action='store_true', help='Valider uniquement')
    parser.add_argument('--report', action='store_true', help='Generer un rapport JSON')
    parser.add_argument('--degrade', action='store_true',
                        help="Variante lecteur leger en mode DEGRADE : remplace les blocs "
                             "hors socle par un texte, au lieu de realigner les versions de "
                             "librairies. Recours pour un lecteur qui ne possede REELLEMENT "
                             "pas la librairie ; ampute le parcours, a n employer qu en "
                             "dernier ressort.")

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

    errors, warnings = validate_preplan(data, base_dir=input_path.parent)

    if warnings:
        print("Avertissements:")
        for w in warnings:
            print(f"  ! {w}")
        print()

    if errors:
        print("Erreurs bloquantes:")
        for e in errors:
            print(f"  X {e}")
        return 1

    nb_nodes = len(data.get('nodes', []))
    types_used = set(n.get('type', '?') for n in data.get('nodes', []))
    print(f"OK JSON valide - {nb_nodes} noeuds, types: {', '.join(sorted(types_used))}")

    if args.validate:
        return 0

    if not args.output:
        slug = re.sub(r'[^a-z0-9]+', '_', data.get('title', 'scenario').lower()).strip('_')
        args.output = str(input_path.parent / f"branching_{slug}.h5p")

    h5p_path, report = generate_h5p(data, args.output, base_dir=input_path.parent)

    print(f"\nOK H5P genere : {h5p_path}")
    print(f"  Titre  : {data.get('title', '?')}")
    print(f"  Noeuds : {nb_nodes}")
    print(f"  Scoring: {data.get('scoring', 'no-score')}")
    print()
    for i, n in enumerate(data.get('nodes', [])):
        ntype = n.get('type', 'text')
        marker = 'Q' if ntype == 'branching_question' else 'V' if ntype == 'interactive_video' else 'P' if ntype == 'course_presentation' else ' '
        next_id = n.get('nextContentId', '-')
        extras = ''
        if ntype == 'course_presentation':
            nb_quiz = sum(len(s.get('interactions', [])) for s in n.get('slides', []))
            if nb_quiz > 0:
                extras = f' ({nb_quiz} quiz)'
        elif ntype == 'interactive_video':
            nb_int = len(n.get('interactions', []))
            if nb_int > 0:
                extras = f' ({nb_int} interactions)'
        print(f"  [{marker}] {i}. {n.get('title', '?')} [{ntype}]{extras} -> {next_id}")
    print()

    # ------------------------------------------------------------------
    # Seconde archive : version degradee pour lecteur leger (Logiquiz).
    # AJOUT pur — la version Moodle ci-dessus n est jamais modifiee.
    # ------------------------------------------------------------------
    logiquiz_path, subs = generate_logiquiz_variant(data, args.output,
                                                    degrade=args.degrade,
                                                    base_dir=input_path.parent)
    report['logiquiz'] = dict(subs, output=logiquiz_path or '')

    if logiquiz_path and subs.get('mode') == 'versions':
        print(f"OK Version lecteur léger : {logiquiz_path}")
        print("  Contenu INTÉGRALEMENT conservé (vidéos interactives comprises).")
        for r in subs.get('remapped', []):
            print(f"  ~ {r}")
        print("  Routage, indices, titres et scores identiques à la version Moodle.")
    elif logiquiz_path:
        print(f"OK Version Logiquiz (mode dégradé) : {logiquiz_path}")
        for n in subs['nodes_replaced']:
            lien = ' + lien vers la vidéo' if n['videoUrl'] else ''
            print(f"  ~ Noeud {n['index']} « {n['title']} » [{n['type']}] "
                  f"-> texte de remplacement{lien}")
        for it in subs['interactions_replaced']:
            print(f"  ~ Noeud {it['node']} slide {it['slide']} interaction "
                  f"{it['index']} [{it['type']}] -> encart de texte")
        print(f"  Socle du lecteur : {', '.join(subs['supported_libraries'])}")
        print("  Routage, indices et scores identiques à la version Moodle.")
    elif subs.get('skipped'):
        print(f"  i Pas de seconde archive : {subs['skipped']}")
    else:
        print("OK Parcours déjà entièrement compatible avec un lecteur léger "
              "(Logiquiz) : pas de seconde archive.")
    print()

    if args.report:
        report_path = str(Path(args.output).with_suffix('.report.json'))
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Rapport genere : {report_path}")

    print("Import Moodle : Banque de contenus > Ajouter > H5P > Téléverser le .h5p")
    return 0


if __name__ == '__main__':
    sys.exit(main())
