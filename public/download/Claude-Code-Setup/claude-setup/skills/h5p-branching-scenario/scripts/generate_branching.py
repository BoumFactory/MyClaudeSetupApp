#!/usr/bin/env python3
"""
Générateur de H5P Branching Scenario depuis un preplan JSON.

Supporte :
- Noeuds riches : text, branching_question, course_presentation (avec quiz embarqués),
  interactive_video (avec questions à des timestamps), image, video
- Scoring : static-end-score, dynamic-score, no-score
- Post-processing du scoring pour Moodle (endScreenScore sur noeuds terminaux)
- Détection automatique des dépendances H5P

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
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import deque

# Import validation
try:
    from validators import validate_preplan
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from validators import validate_preplan


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

SCORING_OPTIONS = ['no-score', 'static-end-score', 'dynamic-score']


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
                'notFilledOut': 'Complete tous les champs.',
                'answerIsCorrect': "':ans' est correct !",
                'answerIsWrong': "':ans' est incorrect.",
                'answeredCorrectly': 'Bonne reponse !',
                'answeredIncorrectly': 'Mauvaise reponse.',
                'solutionLabel': 'Réponse :', 'inputLabel': 'Champ @num sur @total',
                'inputHasTipLabel': 'Indice disponible', 'tipLabel': 'Indice',
                'behaviour': {
                    'enableRetry': True, 'enableSolutionsButton': True,
                    'enableCheckButton': True, 'autoCheck': False,
                    'caseSensitive': False, 'showSolutionsRequiresInput': True,
                    'separateLines': False, 'acceptSpellingErrors': True
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


CP_INTERACTION_GENERATORS = {
    'multichoice': _make_cp_interaction_multichoice,
    'truefalse': _make_cp_interaction_truefalse,
    'dragtext': _make_cp_interaction_dragtext,
    'blanks': _make_cp_interaction_blanks,
    'singlechoiceset': _make_cp_interaction_singlechoiceset,
    'markthewords': _make_cp_interaction_markthewords,
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

        # Element texte de base (toujours present)
        elements = [{
            'x': 0, 'y': 0, 'width': 100, 'height': 100,
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
        'library': 'H5P.CoursePresentation 1.25',
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
                answers.append({
                    'correct': ans.get('correct', False),
                    'tipsAndFeedback': {'tip': '', 'chosenFeedback': '', 'notChosenFeedback': ''},
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
        'library': 'H5P.InteractiveVideo 1.27',
        'metadata': {
            'contentType': 'Interactive Video', 'license': 'U',
            'title': node.get('title', 'Video interactive')
        },
        'subContentId': str(uuid.uuid4())
    }


def make_image(node: Dict) -> Dict:
    """Genere un noeud H5P.Image."""
    return {
        'params': {
            'file': node.get('image', {}),
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
    'video': make_video,
}


def build_branching_scenario(data: Dict) -> Tuple[Dict, Dict]:
    """Construit le content.json et h5p.json du Branching Scenario."""

    nodes = data.get('nodes', [])
    scoring = data.get('scoring', 'no-score')

    # Construire les noeuds de contenu
    content_list = []
    for i, node in enumerate(nodes):
        ntype = node.get('type', 'text')
        generator = GENERATORS.get(ntype, make_advanced_text)
        h5p_content = generator(node)

        # Pour branching_question, nextContentId doit etre -1
        # (la navigation est geree par les alternatives)
        if ntype == 'branching_question':
            next_id = -1
        else:
            next_id = node.get('nextContentId', i + 1 if i < len(nodes) - 1 else -1)

        # CRITIQUE: forceContentFinished
        # - "disabled" : le bouton Continuer est TOUJOURS actif (pas de blocage)
        # - "enabled" : BLOQUE le bouton tant que le contenu n'a pas signale "finished"
        # - "useBehavioural" : suit le setting global (behaviour.forceContentFinished)
        # Les types text/image/video ne peuvent PAS signaler "finished" → toujours "disabled"
        # CoursePresentation/InteractiveVideo PEUVENT signaler mais on laisse le choix
        force_finished = node.get('forceContentFinished', 'disabled')

        # Auto-fix forceContentFinished pour types bloquants
        if ntype in ('text', 'image', 'video'):
            if force_finished == 'enabled':
                print(f"  ! Noeud {i} ({node.get('title', '?')}): "
                      f"force_finished=enabled override → disabled ({ntype} ne peut pas signaler finished)")
                force_finished = 'disabled'

        content_item = {
            'type': h5p_content,
            'showContentTitle': node.get('showTitle', True),
            'proceedButtonText': node.get('proceedText', 'Continuer'),
            'forceContentFinished': force_finished,
            'nextContentId': next_id,
            'contentBehaviour': 'useBehavioural'
        }

        # Feedback de fin optionnel
        feedback = node.get('feedback', {})
        if feedback:
            content_item['feedback'] = {
                'title': feedback.get('title', ''),
                'subtitle': feedback.get('subtitle', ''),
                'endScreenScore': feedback.get('score', 0)
            }

        content_list.append(content_item)

    # Post-processing scoring
    _postprocess_scoring(content_list, nodes, data)

    # Auto-fix missing endScreens
    _ensure_endscreens_coverage(data, content_list, nodes)

    # Ecrans de fin
    end_screens = data.get('endScreens', [])
    if not end_screens:
        end_screens = [{
            'endScreenTitle': '<p><strong>Bravo !</strong></p>',
            'endScreenSubtitle': '<p>Tu as termine le parcours.</p>',
            'endScreenScore': 100,
            'contentId': -1
        }]
    else:
        formatted_ends = []
        for es in end_screens:
            title = es.get('title', 'Fin')
            if not title.strip().startswith('<'):
                title = f"<p><strong>{title}</strong></p>"
            subtitle = es.get('subtitle', '')
            if subtitle and not subtitle.strip().startswith('<'):
                subtitle = f"<p>{subtitle}</p>"
            formatted_ends.append({
                'endScreenTitle': title,
                'endScreenSubtitle': subtitle,
                'endScreenImage': es.get('image', {}),
                'endScreenScore': es.get('score', 0),
                'contentId': es.get('contentId', -1)
            })
        end_screens = formatted_ends

    # Ecran de demarrage
    start_screen = data.get('startScreen', {})
    start_title = start_screen.get('title', data.get('title', 'Parcours'))
    start_subtitle = start_screen.get('subtitle', '')
    if start_title and not start_title.strip().startswith('<'):
        start_title = f"<p><strong>{start_title}</strong></p>"
    if start_subtitle and not start_subtitle.strip().startswith('<'):
        start_subtitle = f"<p>{start_subtitle}</p>"

    # content.json
    content_json = {
        'branchingScenario': {
            'title': data.get('title', 'Parcours adaptatif'),
            'startScreen': {
                'startScreenTitle': start_title,
                'startScreenSubtitle': start_subtitle,
                'startScreenImage': start_screen.get('image', {}),
                'startScreenAltText': start_screen.get('altText', '')
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
                'randomizeBranchingQuestions': data.get('randomizeBranchingQuestions', False)
            },
            'l10n': {
                'startScreenButtonText': 'Commencer',
                'endScreenButtonText': 'Recommencer',
                'backButtonText': 'Retour',
                'disableProceedButtonText': 'Termine le contenu pour continuer',
                'replayButtonText': 'Rejouer',
                'scoreText': 'Ton score :',
                'fullscreenAria': 'Plein ecran'
            }
        }
    }

    # h5p.json
    h5p_json = {
        'title': data.get('title', 'Parcours adaptatif'),
        'language': 'fr',
        'mainLibrary': 'H5P.BranchingScenario',
        'embedTypes': ['iframe'],
        'license': 'CC BY-SA',
        'preloadedDependencies': _get_dependencies(nodes)
    }

    return content_json, h5p_json


def _postprocess_scoring(content_list: List[Dict], nodes: List[Dict], data: Dict):
    """Post-processing : verifie que chaque noeud terminal a feedback.endScreenScore."""
    scoring = data.get('scoring', 'no-score')
    if scoring == 'no-score':
        return

    for i, (content_item, node) in enumerate(zip(content_list, nodes)):
        ntype = node.get('type', 'text')

        # Noeud terminal direct
        if content_item.get('nextContentId', 0) == -1:
            if 'feedback' not in content_item:
                content_item['feedback'] = {
                    'title': '', 'subtitle': '',
                    'endScreenScore': node.get('feedback', {}).get('score', 0)
                }
            elif 'endScreenScore' not in content_item.get('feedback', {}):
                content_item['feedback']['endScreenScore'] = \
                    node.get('feedback', {}).get('score', 0)

        # Alternatives de branching_question avec nextContentId -1
        if ntype == 'branching_question':
            bq = content_item['type']['params'].get('branchingQuestion', {})
            for alt in bq.get('alternatives', []):
                if alt.get('nextContentId', 0) == -1:
                    if 'feedback' not in alt:
                        alt['feedback'] = {
                            'title': '', 'subtitle': '', 'endScreenScore': 0
                        }
                    elif 'endScreenScore' not in alt.get('feedback', {}):
                        alt['feedback']['endScreenScore'] = 0


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


def _get_dependencies(nodes: List[Dict]) -> List[Dict]:
    """Retourne les dependances H5P selon les types utilises."""
    base = [
        {'machineName': 'H5P.BranchingScenario', 'majorVersion': '1', 'minorVersion': '8'},
        {'machineName': 'H5P.BranchingQuestion', 'majorVersion': '1', 'minorVersion': '0'},
        {'machineName': 'H5P.AdvancedText', 'majorVersion': '1', 'minorVersion': '1'},
    ]

    type_deps = {
        'course_presentation': {'machineName': 'H5P.CoursePresentation', 'majorVersion': '1', 'minorVersion': '25'},
        'interactive_video': {'machineName': 'H5P.InteractiveVideo', 'majorVersion': '1', 'minorVersion': '27'},
        'image': {'machineName': 'H5P.Image', 'majorVersion': '1', 'minorVersion': '1'},
        'image_hotspots': {'machineName': 'H5P.ImageHotspots', 'majorVersion': '1', 'minorVersion': '10'},
        'video': {'machineName': 'H5P.Video', 'majorVersion': '1', 'minorVersion': '6'},
    }

    # Dependances des quiz embarques
    quiz_deps = {
        'multichoice': {'machineName': 'H5P.MultiChoice', 'majorVersion': '1', 'minorVersion': '16'},
        'truefalse': {'machineName': 'H5P.TrueFalse', 'majorVersion': '1', 'minorVersion': '8'},
        'dragtext': {'machineName': 'H5P.DragText', 'majorVersion': '1', 'minorVersion': '10'},
        'blanks': {'machineName': 'H5P.Blanks', 'majorVersion': '1', 'minorVersion': '14'},
        'singlechoiceset': {'machineName': 'H5P.SingleChoiceSet', 'majorVersion': '1', 'minorVersion': '11'},
        'markthewords': {'machineName': 'H5P.MarkTheWords', 'majorVersion': '1', 'minorVersion': '11'},
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

    for t in interaction_types_used:
        dep = quiz_deps.get(t)
        if dep and dep not in base:
            base.append(dep)

    # InteractiveVideo necessite H5P.Summary
    if 'interactive_video' in types_used:
        summary_dep = {'machineName': 'H5P.Summary', 'majorVersion': '1', 'minorVersion': '10'}
        if summary_dep not in base:
            base.append(summary_dep)

    return base


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


def generate_h5p(data: Dict, output_path: str) -> Tuple[str, Dict]:
    """Genere le fichier .h5p final et retourne le chemin + rapport."""
    content_json, h5p_json = build_branching_scenario(data)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
        zf.writestr('content/content.json', json.dumps(content_json, ensure_ascii=False, indent=2))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(buf.getvalue())

    report = generate_assembly_report(data, output_path)

    return output_path, report


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Genere un H5P Branching Scenario depuis un preplan JSON'
    )
    parser.add_argument('--input', '-i', required=True, help='Fichier JSON du preplan')
    parser.add_argument('--output', '-o', help='Fichier H5P de sortie')
    parser.add_argument('--validate', action='store_true', help='Valider uniquement')
    parser.add_argument('--report', action='store_true', help='Generer un rapport JSON')

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

    errors, warnings = validate_preplan(data)

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

    h5p_path, report = generate_h5p(data, args.output)

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

    if args.report:
        report_path = str(Path(args.output).with_suffix('.report.json'))
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Rapport genere : {report_path}")

    print("Import Moodle : Banque de contenus > Ajouter > H5P > Téléverser le .h5p")
    return 0


if __name__ == '__main__':
    sys.exit(main())
