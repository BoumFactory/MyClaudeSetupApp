#!/usr/bin/env python3
"""
Générateur de H5P Game Map depuis un préplan Markdown ou une structure JSON.

Supporte :
- Questions simples : multichoice, truefalse, dragtext, blanks
- Questions multiples : singlechoiceset, questionset

Usage:
  python generate_gamemap.py --preplan preplan.md --output parcours.h5p --background carte.png
  python generate_gamemap.py --json config.json --output parcours.h5p
"""
import json
import zipfile
import io
import uuid
import random
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import du parser
try:
    from parse_preplan import parse_preplan, validate_preplan
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from parse_preplan import parse_preplan, validate_preplan


# ============================================================================
# STYLES PRÉDÉFINIS
# ============================================================================

STYLES = {
    'aventure': {
        'lives': 4,
        'roaming': 'complete',
        'fog': 'visited',
        'colors': {
            'stageUnvisited': 'rgba(52, 152, 219, 0.85)',
            'stageLocked': 'rgba(127, 140, 141, 0.7)',
            'stageCleared': 'rgba(46, 204, 113, 0.85)',
            'pathNormal': 'rgba(44, 62, 80, 0.6)',
            'pathCleared': 'rgba(46, 204, 113, 0.7)',
        }
    },
    'revision': {
        'lives': None,
        'roaming': 'free',
        'fog': 'none',
        'colors': {
            'stageUnvisited': 'rgba(41, 128, 185, 0.8)',
            'stageLocked': 'rgba(149, 165, 166, 0.6)',
            'stageCleared': 'rgba(39, 174, 96, 0.8)',
            'pathNormal': 'rgba(52, 73, 94, 0.5)',
            'pathCleared': 'rgba(39, 174, 96, 0.6)',
        }
    },
    'evaluation': {
        'lives': 1,
        'roaming': 'strict',
        'fog': 'visited',
        'colors': {
            'stageUnvisited': 'rgba(155, 89, 182, 0.8)',
            'stageLocked': 'rgba(127, 140, 141, 0.7)',
            'stageCleared': 'rgba(46, 204, 113, 0.85)',
            'pathNormal': 'rgba(44, 62, 80, 0.6)',
            'pathCleared': 'rgba(46, 204, 113, 0.7)',
        }
    },
    'decouverte': {
        'lives': None,
        'roaming': 'free',
        'fog': 'all',
        'colors': {
            'stageUnvisited': 'rgba(230, 126, 34, 0.85)',
            'stageLocked': 'rgba(127, 140, 141, 0.7)',
            'stageCleared': 'rgba(46, 204, 113, 0.85)',
            'pathNormal': 'rgba(44, 62, 80, 0.6)',
            'pathCleared': 'rgba(46, 204, 113, 0.7)',
        }
    }
}


# ============================================================================
# GÉNÉRATEURS DE CONTENUS H5P
# ============================================================================

def make_multichoice(etape: Dict) -> Dict:
    """Génère un contenu H5P MultiChoice."""

    content = etape.get('content', {})
    answers = []

    for ans in content.get('answers', []):
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
        'contentType': {
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
                'confirmCheck': _get_confirm_dialog('Valider ?', 'Es-tu sûr de ta réponse ?'),
                'confirmRetry': _get_confirm_dialog('Réessayer ?', 'Tu vas recommencer cette question.'),
                'question': f"<p><strong>{etape.get('title', '')}</strong></p>\n<p>{content.get('question', '')}</p>\n" +
                           (f"<p><em>Indice : {content.get('tip', '')}</em></p>" if content.get('tip') else "")
            },
            'library': 'H5P.MultiChoice 1.16',
            'metadata': {'contentType': 'Multiple Choice', 'license': 'U', 'title': etape.get('title', '')},
            'subContentId': str(uuid.uuid4())
        }
    }


def make_truefalse(etape: Dict) -> Dict:
    """Génère un contenu H5P TrueFalse."""

    content = etape.get('content', {})

    return {
        'contentType': {
            'params': {
                'media': {'disableImageZooming': False},
                'correct': 'true' if content.get('correct', True) else 'false',
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
                    'wrongAnswerMessage': content.get('feedback_incorrect', 'Incorrect.'),
                    'correctAnswerMessage': content.get('feedback_correct', 'Correct !'),
                    'scoreBarLabel': 'Score : :num sur :total',
                    'a11yCheck': 'Vérifier.',
                    'a11yShowSolution': 'Solution.',
                    'a11yRetry': 'Recommencer.'
                },
                'confirmCheck': _get_confirm_dialog('Valider ?', 'Sûr ?'),
                'confirmRetry': _get_confirm_dialog('Réessayer ?', 'Recommencer.'),
                'question': f"<p><strong>{etape.get('title', '')}</strong></p>\n<p>{content.get('question', '')}</p>\n"
            },
            'library': 'H5P.TrueFalse 1.8',
            'metadata': {'contentType': 'True/False Question', 'license': 'U', 'title': etape.get('title', '')},
            'subContentId': str(uuid.uuid4())
        }
    }


def make_dragtext(etape: Dict) -> Dict:
    """Génère un contenu H5P DragText."""

    content = etape.get('content', {})

    return {
        'contentType': {
            'params': {
                'media': {'disableImageZooming': False},
                'taskDescription': f"<p><strong>{etape.get('title', '')}</strong></p>\n<p>{content.get('description', '')}</p>\n",
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage ! Réessaie !"},
                    {'from': 1, 'to': 99, 'feedback': "Presque ! Vérifie les derniers mots."},
                    {'from': 100, 'to': 100, 'feedback': "Parfait !"}
                ],
                'checkAnswer': 'Vérifier',
                'submitAnswer': 'Soumettre',
                'tryAgain': 'Réessayer',
                'showSolution': 'Voir la solution',
                'dropZoneIndex': 'Zone @index.',
                'empty': 'Zone @index vide.',
                'contains': 'Zone @index contient @draggable.',
                'ariaDraggableIndex': '@index sur @count.',
                'tipLabel': 'Indice',
                'correctText': 'Correct !',
                'incorrectText': 'Incorrect',
                'resetDropTitle': 'Réinitialiser',
                'resetDropDescription': 'Réinitialiser cette zone ?',
                'grabbed': 'Élément sélectionné.',
                'cancelledDragging': 'Annulé.',
                'correctAnswer': 'Réponse correcte :',
                'feedbackHeader': 'Résultat',
                'behaviour': {
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'enableCheckButton': True,
                    'instantFeedback': False
                },
                'scoreBarLabel': 'Score : :num sur :total',
                'a11yCheck': 'Vérifier.',
                'a11yShowSolution': 'Solution.',
                'a11yRetry': 'Recommencer.',
                'textField': content.get('text', '')
            },
            'library': 'H5P.DragText 1.10',
            'metadata': {'contentType': 'Drag the Words', 'license': 'U', 'title': etape.get('title', '')},
            'subContentId': str(uuid.uuid4())
        }
    }


def make_blanks(etape: Dict) -> Dict:
    """Génère un contenu H5P Blanks (texte à trous)."""

    content = etape.get('content', {})

    return {
        'contentType': {
            'params': {
                'media': {'disableImageZooming': False},
                'text': f"<p><strong>{etape.get('title', '')}</strong></p>\n<p>{content.get('description', '')}</p>\n",
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage !"},
                    {'from': 1, 'to': 99, 'feedback': "Presque parfait !"},
                    {'from': 100, 'to': 100, 'feedback': "Excellent !"}
                ],
                'showSolutions': 'Voir la solution',
                'tryAgain': 'Réessayer',
                'checkAnswer': 'Vérifier',
                'submitAnswer': 'Soumettre',
                'notFilledOut': 'Complète tous les champs.',
                'answerIsCorrect': "':ans' est correct !",
                'answerIsWrong': "':ans' est incorrect.",
                'answeredCorrectly': 'Bonne réponse !',
                'answeredIncorrectly': 'Mauvaise réponse.',
                'solutionLabel': 'Réponse :',
                'inputLabel': 'Champ @num sur @total',
                'inputHasTipLabel': 'Indice disponible',
                'tipLabel': 'Indice',
                'behaviour': {
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'enableCheckButton': True,
                    'autoCheck': False,
                    'caseSensitive': False,
                    'showSolutionsRequiresInput': True,
                    'separateLines': False,
                    'acceptSpellingErrors': True
                },
                'scoreBarLabel': 'Score : :num sur :total',
                'a11yCheck': 'Vérifier.',
                'a11yShowSolution': 'Solution.',
                'a11yRetry': 'Recommencer.',
                'a11yCheckingModeHeader': 'Vérification',
                'confirmCheck': _get_confirm_dialog('Valider ?', 'Sûr ?'),
                'confirmRetry': _get_confirm_dialog('Réessayer ?', 'Recommencer.'),
                'questions': [f"<p>{content.get('text', '')}</p>"]
            },
            'library': 'H5P.Blanks 1.14',
            'metadata': {'contentType': 'Fill in the Blanks', 'license': 'U', 'title': etape.get('title', '')},
            'subContentId': str(uuid.uuid4())
        }
    }


def make_singlechoiceset(etape: Dict) -> Dict:
    """Génère un contenu H5P SingleChoiceSet (plusieurs questions QCM enchaînées)."""

    content = etape.get('content', {})
    questions = content.get('questions', [])

    choices = []
    for q in questions:
        # Trouver la bonne réponse (doit être en premier pour SingleChoiceSet)
        answers = q.get('answers', [])
        correct_answers = [a['text'] for a in answers if a.get('correct', False)]
        wrong_answers = [a['text'] for a in answers if not a.get('correct', False)]

        # SingleChoiceSet: la première réponse est toujours la bonne
        ordered_answers = correct_answers + wrong_answers

        choices.append({
            'subContentId': str(uuid.uuid4()),
            'question': q.get('question', ''),
            'answers': ordered_answers
        })

    return {
        'contentType': {
            'params': {
                'behaviour': {
                    'autoContinue': True,
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'passPercentage': 100,
                    'soundEffectsEnabled': True,
                    'timeoutCorrect': 2000,
                    'timeoutWrong': 3000
                },
                'choices': choices,
                'l10n': {
                    'nextButtonLabel': 'Question suivante',
                    'showSolutionButtonLabel': 'Voir la solution',
                    'retryButtonLabel': 'Réessayer',
                    'solutionViewTitle': 'Solutions',
                    'correctText': 'Correct !',
                    'incorrectText': 'Incorrect !',
                    'shouldSelect': 'Aurait dû être sélectionné',
                    'shouldNotSelect': 'Ne devait pas être sélectionné',
                    'muteButtonLabel': 'Couper le son',
                    'closeButtonLabel': 'Fermer',
                    'slideOfTotal': 'Question :num sur :total',
                    'scoreBarLabel': 'Tu as :num sur :total points',
                    'solutionListQuestionNumber': 'Question :num',
                    'a11yShowSolution': 'Afficher la solution.',
                    'a11yRetry': 'Recommencer.'
                },
                'overallFeedback': [
                    {'from': 0, 'to': 50, 'feedback': "Continue tes efforts !"},
                    {'from': 51, 'to': 99, 'feedback': "Bien, mais tu peux mieux faire !"},
                    {'from': 100, 'to': 100, 'feedback': "Parfait !"}
                ]
            },
            'library': 'H5P.SingleChoiceSet 1.11',
            'metadata': {'contentType': 'Single Choice Set', 'license': 'U', 'title': etape.get('title', '')},
            'subContentId': str(uuid.uuid4())
        }
    }


def make_questionset(etape: Dict) -> Dict:
    """Génère un contenu H5P QuestionSet (mix de types dans une étape)."""

    content = etape.get('content', {})
    questions = content.get('questions', [])

    question_list = []
    for q in questions:
        q_type = q.get('type', 'multichoice')

        if q_type == 'multichoice':
            answers = []
            for ans in q.get('answers', []):
                answers.append({
                    'correct': ans.get('correct', False),
                    'tipsAndFeedback': {'tip': '', 'chosenFeedback': '', 'notChosenFeedback': ''},
                    'text': f"<div>{ans.get('text', '')}</div>\n"
                })
            random.shuffle(answers)

            question_list.append({
                'params': {
                    'media': {'disableImageZooming': False},
                    'answers': answers,
                    'overallFeedback': [{'from': 0, 'to': 100}],
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
                    'question': f"<p>{q.get('question', '')}</p>\n"
                },
                'library': 'H5P.MultiChoice 1.16',
                'metadata': {'contentType': 'Multiple Choice', 'license': 'U', 'title': 'Question'},
                'subContentId': str(uuid.uuid4())
            })

        elif q_type == 'truefalse':
            question_list.append({
                'params': {
                    'media': {'disableImageZooming': False},
                    'correct': 'true' if q.get('correct', True) else 'false',
                    'behaviour': {
                        'enableRetry': True,
                        'enableSolutionsButton': True,
                        'enableCheckButton': True
                    },
                    'l10n': {
                        'trueText': 'Vrai',
                        'falseText': 'Faux',
                        'score': 'Score : @score sur @total',
                        'checkAnswer': 'Vérifier',
                        'showSolutionButton': 'Voir la solution',
                        'tryAgain': 'Réessayer',
                        'wrongAnswerMessage': q.get('feedback_incorrect', 'Incorrect.'),
                        'correctAnswerMessage': q.get('feedback_correct', 'Correct !')
                    },
                    'question': f"<p>{q.get('question', '')}</p>\n"
                },
                'library': 'H5P.TrueFalse 1.8',
                'metadata': {'contentType': 'True/False Question', 'license': 'U', 'title': 'Question'},
                'subContentId': str(uuid.uuid4())
            })

    return {
        'contentType': {
            'params': {
                'introPage': {
                    'showIntroPage': False,
                    'startButtonText': 'Commencer',
                    'introduction': ''
                },
                'progressType': 'dots',
                'passPercentage': 50,
                'questions': question_list,
                'disableBackwardsNavigation': False,
                'randomQuestions': False,
                'endGame': {
                    'showResultPage': True,
                    'showSolutionButton': True,
                    'showRetryButton': True,
                    'noResultMessage': 'Quiz terminé',
                    'message': 'Tu as obtenu @score sur @total points.',
                    'overallFeedback': [
                        {'from': 0, 'to': 50, 'feedback': 'Continue !'},
                        {'from': 51, 'to': 100, 'feedback': 'Bien joué !'}
                    ],
                    'solutionButtonText': 'Voir les solutions',
                    'retryButtonText': 'Réessayer',
                    'finishButtonText': 'Terminer',
                    'submitButtonText': 'Soumettre',
                    'showAnimations': True,
                    'skippable': False,
                    'skipButtonText': 'Passer'
                },
                'override': {
                    'showSolutionButton': 'on',
                    'retryButton': 'on'
                },
                'texts': {
                    'prevButton': 'Précédent',
                    'nextButton': 'Suivant',
                    'finishButton': 'Terminer',
                    'submitButton': 'Soumettre',
                    'textualProgress': 'Question :current sur :total',
                    'jumpToQuestion': 'Question %d sur %total',
                    'questionLabel': 'Question',
                    'readSpeakerProgress': 'Question :current sur :total',
                    'unansweredText': 'Non répondu',
                    'answeredText': 'Répondu',
                    'currentQuestionText': 'Question actuelle',
                    'navigationLabel': 'Questions'
                }
            },
            'library': 'H5P.QuestionSet 1.20',
            'metadata': {'contentType': 'Question Set', 'license': 'U', 'title': etape.get('title', '')},
            'subContentId': str(uuid.uuid4())
        }
    }


# ============================================================================
# HELPERS
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
        'shouldCheck': 'À cocher',
        'shouldNotCheck': 'À ne pas cocher',
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


# ============================================================================
# CONSTRUCTION DU GAME MAP
# ============================================================================

def build_gamemap(data: Dict, background_path: Optional[str] = None) -> tuple:
    """Construit le contenu H5P Game Map complet."""

    style = STYLES.get(data.get('style', 'aventure'), STYLES['aventure'])
    config = data.get('config', {})
    colors = {**style['colors'], **data.get('colors', {})}

    # Construire les stages
    elements = []
    etapes = data.get('etapes', [])

    for i, e in enumerate(etapes):
        # Déterminer le générateur selon le type
        e_type = e.get('type', 'multichoice')

        generators = {
            'multichoice': make_multichoice,
            'truefalse': make_truefalse,
            'dragtext': make_dragtext,
            'blanks': make_blanks,
            'singlechoiceset': make_singlechoiceset,
            'questionset': make_questionset
        }

        generator = generators.get(e_type, make_multichoice)
        content = generator(e)

        # Voisins (linéaire par défaut)
        neighbors = []
        if i > 0:
            neighbors.append(str(i - 1))
        if i < len(etapes) - 1:
            neighbors.append(str(i + 1))

        stage = {
            'id': str(uuid.uuid4()),
            'label': e.get('title', f'Étape {i+1}'),
            'telemetry': {
                'x': str(e.get('x', 50)),
                'y': str(e.get('y', 50)),
                'width': '6',
                'height': '10'
            },
            'neighbors': neighbors,
            'type': 'stage',
            'canBeStartStage': e.get('isStart', i == 0),
            'time': {},
            'accessRestrictions': {
                'allOrAnyRestrictionSet': 'all',
                'restrictionSetList': [{
                    'allOrAnyRestriction': 'any',
                    'restrictionList': [{'restrictionType': 'totalScore'}]
                }]
            },
            'specialStageExtraLives': 0,
            'specialStageExtraTime': 0,
            'contentsList': [content]
        }
        elements.append(stage)

    # Feedbacks de fin
    end_feedbacks = data.get('endScreen', {}).get('feedbacks', [])
    if not end_feedbacks:
        end_feedbacks = [
            {'from': 0, 'to': 40, 'feedback': "Continue tes efforts !"},
            {'from': 41, 'to': 70, 'feedback': "Bon travail !"},
            {'from': 71, 'to': 99, 'feedback': "Excellent !"},
            {'from': 100, 'to': 100, 'feedback': "Parfait !"}
        ]

    # Content.json
    content_json = {
        'showTitleScreen': True,
        'titleScreen': {
            'titleScreenIntroduction': data.get('lore', '<p>Bienvenue dans ce parcours !</p>')
        },
        'gamemapSteps': {
            'backgroundImageSettings': {
                'backgroundImage': {
                    'path': 'images/background.png',
                    'mime': 'image/png',
                    'copyright': {'license': 'U'},
                    'width': 1920,
                    'height': 1080
                }
            },
            'gamemap': {
                'elements': elements
            }
        },
        'endScreen': {
            'noSuccess': {
                'endScreenTextNoSuccess': data.get('endScreen', {}).get('failure', '<p><strong>Dommage !</strong></p>')
            },
            'success': {
                'endScreenTextSuccess': data.get('endScreen', {}).get('success', '<p><strong>Bravo !</strong></p>')
            },
            'overallFeedback': end_feedbacks
        },
        'visual': {
            'stages': {
                'colorStage': colors.get('stageUnvisited'),
                'colorStageLocked': colors.get('stageLocked'),
                'colorStageCleared': colors.get('stageCleared'),
                'showScoreStars': config.get('showScoreStars', 'always')
            },
            'paths': {
                'displayPaths': True,
                'style': {
                    'colorPath': colors.get('pathNormal'),
                    'colorPathCleared': colors.get('pathCleared'),
                    'pathWidth': '0.25',
                    'pathStyle': colors.get('pathStyle', 'dotted')
                }
            },
            'misc': {
                'useAnimation': config.get('useAnimation', True)
            }
        },
        'audio': {
            'backgroundMusic': {'muteDuringExercise': True},
            'ambient': {}
        },
        'behaviour': {
            'enableRetry': True,
            'enableSolutionsButton': True,
            'lives': config.get('lives') or style.get('lives'),
            'map': {
                'showLabels': config.get('showLabels', True),
                'roaming': config.get('roaming') or style.get('roaming', 'complete'),
                'fog': config.get('fog') or style.get('fog', 'visited')
            }
        },
        'l10n': _get_l10n(),
        'a11y': _get_a11y(),
        'headline': data.get('title', 'Parcours')
    }

    # Déterminer les bibliothèques nécessaires
    types_used = set(e.get('type', 'multichoice') for e in etapes)
    dependencies = _get_dependencies(types_used)

    # h5p.json
    h5p_json = {
        'title': data.get('title', 'Parcours'),
        'language': 'fr',
        'mainLibrary': 'H5P.GameMap',
        'embedTypes': ['iframe'],
        'license': 'CC BY-SA',
        'preloadedDependencies': dependencies
    }

    return content_json, h5p_json


def _get_l10n() -> Dict:
    return {
        'start': 'Commencer',
        'continue': 'Continuer',
        'restart': 'Recommencer',
        'showSolutions': 'Solutions',
        'completedMap': 'Parcours terminé !',
        'fullScoreButnoLivesLeft': 'Score parfait mais plus de vies !',
        'confirmFinishHeader': 'Terminer ?',
        'confirmFinishDialog': 'Tu ne pourras plus explorer.',
        'confirmFinishDialogSubmission': 'Ton score sera enregistré.',
        'confirmFinishDialogQuestion': 'Veux-tu vraiment terminer ?',
        'confirmAccessDeniedHeader': 'Étape verrouillée',
        'confirmAccessDeniedDialog': 'Réussis les étapes précédentes.',
        'yes': 'Oui',
        'no': 'Non',
        'confirmGameOverHeader': 'Game Over !',
        'confirmGameOverDialog': 'Tu as perdu toutes tes vies ! Recommence.',
        'confirmTimeoutHeader': 'Temps écoulé !',
        'confirmTimeoutDialog': 'Le temps est écoulé.',
        'confirmTimeoutDialogLostLife': 'Temps écoulé, tu perds une vie.',
        'confirmScoreIncompleteHeader': 'Score incomplet',
        'confirmIncompleteScoreDialogLostLife': 'Score insuffisant, tu perds une vie.',
        'confirmFullScoreHeader': 'Score parfait !',
        'confirmFullScoreDialog': 'Bravo ! Tu peux continuer.',
        'confirmFullScoreDialogLoseLivesAmendmend': 'Attention, tu peux encore perdre des vies !',
        'ok': 'OK',
        'noStages': 'Aucune étape valide.',
        'fullScoreButTimeout': 'Score parfait mais temps écoulé !'
    }


def _get_a11y() -> Dict:
    return {
        'buttonFinish': 'Terminer',
        'buttonAudioActive': 'Couper le son',
        'buttonAudioInactive': 'Activer le son',
        'close': 'Fermer',
        'yourResult': 'Tu as obtenu @score sur @total points',
        'mapWasOpened': 'La carte est ouverte.',
        'mapSolutionsWasOpened': 'Mode solutions.',
        'startScreenWasOpened': 'Écran de démarrage.',
        'endScreenWasOpened': 'Écran de fin.',
        'exerciseLabel': '. Exercice pour @stagelabel',
        'stageButtonLabel': 'Étape : @stagelabel',
        'adjacentStageLabel': 'Étape voisine : @stagelabelNeighbor',
        'locked': 'Verrouillée',
        'cleared': 'Réussie',
        'applicationInstructions': 'Utilise Espace ou Entrée pour activer une étape. Flèches pour naviguer.',
        'applicationDescription': 'Carte du parcours',
        'movedToStage': 'Déplacement vers @stagelabel',
        'stageUnlocked': 'Étape @stagelabel débloquée !',
        'toolbarFallbackLabel': 'Parcours',
        'enterFullscreen': 'Plein écran',
        'exitFullscreen': 'Quitter plein écran'
    }


def _get_dependencies(types_used: set) -> List[Dict]:
    """Retourne les dépendances H5P nécessaires selon les types utilisés."""

    base = [
        {'machineName': 'H5P.GameMap', 'majorVersion': '1', 'minorVersion': '5'},
        {'machineName': 'H5P.Question', 'majorVersion': '1', 'minorVersion': '5'},
        {'machineName': 'H5P.JoubelUI', 'majorVersion': '1', 'minorVersion': '3'},
        {'machineName': 'FontAwesome', 'majorVersion': '4', 'minorVersion': '5'}
    ]

    type_deps = {
        'multichoice': {'machineName': 'H5P.MultiChoice', 'majorVersion': '1', 'minorVersion': '16'},
        'truefalse': {'machineName': 'H5P.TrueFalse', 'majorVersion': '1', 'minorVersion': '8'},
        'dragtext': {'machineName': 'H5P.DragText', 'majorVersion': '1', 'minorVersion': '10'},
        'blanks': {'machineName': 'H5P.Blanks', 'majorVersion': '1', 'minorVersion': '14'},
        'singlechoiceset': {'machineName': 'H5P.SingleChoiceSet', 'majorVersion': '1', 'minorVersion': '11'},
        'questionset': {'machineName': 'H5P.QuestionSet', 'majorVersion': '1', 'minorVersion': '20'}
    }

    for t in types_used:
        if t in type_deps:
            base.append(type_deps[t])

    # QuestionSet peut contenir MultiChoice et TrueFalse
    if 'questionset' in types_used:
        if type_deps['multichoice'] not in base:
            base.append(type_deps['multichoice'])
        if type_deps['truefalse'] not in base:
            base.append(type_deps['truefalse'])

    return base


# ============================================================================
# GÉNÉRATION DU FICHIER H5P
# ============================================================================

def generate_h5p(data: Dict, output_path: str, background_path: Optional[str] = None):
    """Génère le fichier H5P final."""

    content_json, h5p_json = build_gamemap(data, background_path)

    # Lire l'image de fond
    image_data = None
    if background_path and Path(background_path).exists():
        with open(background_path, 'rb') as f:
            image_data = f.read()
    else:
        # Image par défaut (1x1 pixel transparent)
        import base64
        image_data = base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
        )

    # Créer le ZIP
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
        zf.writestr('content/content.json', json.dumps(content_json, ensure_ascii=False, indent=2))
        zf.writestr('content/images/background.png', image_data)

    # Écrire le fichier
    with open(output_path, 'wb') as f:
        f.write(buf.getvalue())

    return output_path


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Génère un H5P Game Map depuis un préplan Markdown')
    parser.add_argument('--preplan', help='Chemin vers le fichier préplan.md')
    parser.add_argument('--json', help='Chemin vers un fichier JSON de configuration')
    parser.add_argument('--output', '-o', required=True, help='Chemin de sortie du fichier .h5p')
    parser.add_argument('--background', '-b', help='Chemin vers l\'image de fond')

    args = parser.parse_args()

    # Charger les données
    if args.preplan:
        data = parse_preplan(args.preplan)
        errors = validate_preplan(data)
        if errors:
            print("Avertissements:")
            for e in errors:
                print(f"  - {e}")
    elif args.json:
        with open(args.json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print("Erreur: spécifiez --preplan ou --json")
        return 1

    # Générer le H5P
    output = generate_h5p(data, args.output, args.background)

    print("=" * 60)
    print(f"  {data.get('title', 'Parcours')} - GÉNÉRÉ")
    print("=" * 60)
    print(f"[OK] Fichier : {output}")
    print()
    print("Configuration :")
    config = data.get('config', {})
    print(f"   - Vies : {config.get('lives', 'illimité')}")
    print(f"   - Roaming : {config.get('roaming', 'complete')}")
    print(f"   - Style : {data.get('style', 'aventure')}")
    print()
    print(f"{len(data.get('etapes', []))} étapes :")
    for i, e in enumerate(data.get('etapes', [])):
        print(f"   {i+1}. {e.get('title', 'Étape')} [{e.get('type', 'multichoice').upper()}]")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    exit(main())
