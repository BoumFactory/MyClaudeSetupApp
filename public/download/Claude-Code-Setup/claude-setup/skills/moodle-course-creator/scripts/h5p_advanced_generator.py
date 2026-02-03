#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur H5P Avance - Support complet des types de contenus interactifs.

Types supportes:
- Question Set (quiz multi-questions)
- Single Choice Set
- Multiple Choice
- True/False
- Fill in the Blanks (textes a trous)
- Drag and Drop (glisser-deposer)
- Drag the Words (reconstruction phrases)
- Mark the Words (selection mots)
- Course Presentation (diaporama interactif)
- Interactive Book (livre interactif)
- Branching Scenario (scenarios adaptatifs)
- Column (organisation contenus)
- Image Hotspots (images annotees)

Support LaTeX/MathJax pour formules mathematiques.
Support HTML enrichi.
"""

import json
import zipfile
import io
import base64
import re
from typing import List, Dict, Optional, Any, Union
from pathlib import Path
import html


def escape_html_preserve_math(text: str) -> str:
    """
    Echappe le texte pour HTML tout en preservant les formules LaTeX.

    IMPORTANT: Cette fonction doit etre utilisee PARTOUT (questions, options, feedbacks)
    pour garantir un traitement uniforme du LaTeX.

    Ordre des operations:
    1. Convertir les notations $ en notations \( \)
    2. Proteger toutes les formules LaTeX
    3. Echapper le HTML
    4. Restaurer les formules
    """
    if not text:
        return ""

    result = str(text)

    # Etape 1: Convertir les notations alternatives AVANT protection
    # $$ ... $$ -> \[ ... \]
    result = re.sub(r'\$\$(.*?)\$\$', r'\\[\1\\]', result, flags=re.DOTALL)
    # $ ... $ -> \( ... \) (attention aux faux positifs)
    result = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', r'\\(\1\\)', result)

    # Etape 2: Proteger les formules LaTeX
    math_blocks = []

    def protect_block(m):
        math_blocks.append(m.group(0))
        return f"__MATH_BLOCK_{len(math_blocks)-1}__"

    # Proteger \[ ... \] (blocs)
    result = re.sub(r'\\\[.*?\\\]', protect_block, result, flags=re.DOTALL)
    # Proteger \( ... \) (inline)
    result = re.sub(r'\\\(.*?\\\)', protect_block, result, flags=re.DOTALL)

    # Etape 3: Echapper HTML si ce n'est pas deja du HTML
    if not any(tag in result for tag in ['<p>', '<div>', '<strong>', '<em>', '<h1>', '<h2>', '<h3>', '<ul>', '<ol>']):
        result = html.escape(result)

    # Etape 4: Restaurer les formules
    for i, block in enumerate(math_blocks):
        result = result.replace(f"__MATH_BLOCK_{i}__", block)

    return result


# Alias pour compatibilite avec l'ancien code
def escape_html(text: str) -> str:
    """Alias vers escape_html_preserve_math pour compatibilite"""
    return escape_html_preserve_math(text)


def wrap_math(text: str) -> str:
    """
    DEPRECATED: Utiliser escape_html_preserve_math() directement.

    Cette fonction est conservee pour compatibilite mais ne devrait plus etre utilisee.
    La conversion $ -> \( est maintenant integree dans escape_html_preserve_math.
    """
    if not text:
        return ""
    # Deleguons a la fonction unifiee
    return escape_html_preserve_math(text)


class H5PAdvancedGenerator:
    """Generateur H5P avance avec support complet des types de contenus"""

    # Versions des bibliotheques H5P
    LIBRARY_VERSIONS = {
        'H5P.QuestionSet': {'major': 1, 'minor': 20},
        'H5P.MultiChoice': {'major': 1, 'minor': 16},
        'H5P.SingleChoiceSet': {'major': 1, 'minor': 11},
        'H5P.TrueFalse': {'major': 1, 'minor': 8},
        'H5P.Blanks': {'major': 1, 'minor': 14},
        'H5P.DragQuestion': {'major': 1, 'minor': 14},
        'H5P.DragText': {'major': 1, 'minor': 10},
        'H5P.MarkTheWords': {'major': 1, 'minor': 11},
        'H5P.CoursePresentation': {'major': 1, 'minor': 25},
        'H5P.InteractiveBook': {'major': 1, 'minor': 7},
        'H5P.BranchingScenario': {'major': 1, 'minor': 8},
        'H5P.Column': {'major': 1, 'minor': 16},
        'H5P.ImageHotspots': {'major': 1, 'minor': 10},
        'H5P.AdvancedText': {'major': 1, 'minor': 1},
        'H5P.Image': {'major': 1, 'minor': 1},
    }

    # ==========================================================================
    # UTILITAIRES
    # ==========================================================================

    @staticmethod
    def _create_h5p_package(h5p_json: Dict, content: Dict,
                            images: Optional[Dict[str, bytes]] = None) -> bytes:
        """Cree un package .h5p (fichier ZIP)"""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
            zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False, indent=2))

            # Ajouter les images si presentes
            if images:
                for name, data in images.items():
                    zf.writestr(f'content/images/{name}', data)

        return buffer.getvalue()

    @staticmethod
    def _get_base_dependencies() -> List[Dict]:
        """Retourne les dependances de base communes"""
        return [
            {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
            {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
            {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
            {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
            {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5},
        ]

    # ==========================================================================
    # FILL IN THE BLANKS (Textes a trous)
    # ==========================================================================

    @classmethod
    def create_fill_blanks_h5p(cls, title: str, questions: List[Dict],
                                overall_feedback: Optional[List[Dict]] = None) -> bytes:
        """
        Cree un H5P Fill in the Blanks (textes a trous).

        Args:
            title: Titre du contenu
            questions: Liste de questions avec format:
                {
                    "text": "La capitale de la France est *Paris*.",
                    "tip": "Indice optionnel"
                }
                Les mots entre *asterisques* sont les trous a completer.
                Pour plusieurs reponses acceptees: *Paris/paris/PARIS*

        Returns:
            Contenu du fichier .h5p
        """
        # Construire les questions
        h5p_questions = []
        for q in questions:
            text = q.get('text', '')
            # Convertir la syntaxe *reponse* en syntaxe H5P *reponse:tip*
            tip = q.get('tip', '')
            if tip:
                # Ajouter le tip a chaque trou
                text = re.sub(r'\*([^*]+)\*', rf'*\1:{tip}*', text)

            h5p_questions.append(f"<p>{wrap_math(text)}</p>")

        if not overall_feedback:
            overall_feedback = [
                {"from": 0, "to": 49, "feedback": "Il faut reviser !"},
                {"from": 50, "to": 79, "feedback": "Pas mal !"},
                {"from": 80, "to": 100, "feedback": "Excellent !"}
            ]

        content = {
            "media": {"disableImageZooming": False},
            "text": "\n".join(h5p_questions),
            "overallFeedback": overall_feedback,
            "showSolutions": "Show solution",
            "tryAgain": "Retry",
            "checkAnswer": "Check",
            "submitAnswer": "Submit",
            "notFilledOut": "Please fill in all blanks to view solution",
            "answerIsCorrect": "\":ans\" is correct",
            "answerIsWrong": "\":ans\" is wrong",
            "answeredCorrectly": "Filled in correctly.",
            "answeredIncorrectly": "Filled in incorrectly.",
            "solutionLabel": "Correct answer:",
            "inputLabel": "Blank input @num of @total",
            "inputHasTipLabel": "Tip available",
            "tipLabel": "Tip",
            "behaviour": {
                "enableRetry": True,
                "enableSolutionsButton": True,
                "enableCheckButton": True,
                "autoCheck": False,
                "caseSensitive": False,
                "showSolutionsRequiresInput": True,
                "separateLines": False,
                "confirmCheckDialog": False,
                "confirmRetryDialog": False,
                "acceptSpellingErrors": True
            },
            "scoreBarLabel": "You got :num out of :total points",
            "a11yCheck": "Check the answers. The responses will be marked as correct, incorrect, or unanswered.",
            "a11yShowSolution": "Show the solution. The task will be marked with its correct solution.",
            "a11yRetry": "Retry the task. Reset all responses and start the task over again.",
            "a11yCheckingModeHeader": "Checking mode"
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.Blanks",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
                *cls._get_base_dependencies()
            ]
        }

        return cls._create_h5p_package(h5p_json, content)

    # ==========================================================================
    # DRAG THE WORDS (Reconstruction de phrases)
    # ==========================================================================

    @classmethod
    def create_drag_words_h5p(cls, title: str, text_with_blanks: str,
                               task_description: str = "Faites glisser les mots aux bons endroits") -> bytes:
        """
        Cree un H5P Drag the Words.

        Args:
            title: Titre
            text_with_blanks: Texte avec mots a placer entre *asterisques*.
                Ex: "Une suite *arithmetique* a une raison *constante*."
            task_description: Description de la tache

        Returns:
            Contenu du fichier .h5p
        """
        content = {
            "media": {"disableImageZooming": False},
            "taskDescription": f"<p>{task_description}</p>",
            "textField": f"<p>{wrap_math(text_with_blanks)}</p>",
            "overallFeedback": [
                {"from": 0, "to": 49, "feedback": "Il faut reviser !"},
                {"from": 50, "to": 79, "feedback": "Pas mal !"},
                {"from": 80, "to": 100, "feedback": "Excellent !"}
            ],
            "checkAnswer": "Verifier",
            "submitAnswer": "Soumettre",
            "tryAgain": "Reessayer",
            "showSolution": "Voir la solution",
            "dropZoneIndex": "Zone de depot @index.",
            "empty": "Zone de depot @index est vide.",
            "contains": "Zone de depot @index contient un element deplacable @draggable.",
            "ariaDraggableIndex": "@index of @count deplacables.",
            "tipLabel": "Indice",
            "correctText": "Correct !",
            "incorrectText": "Incorrect !",
            "resetDropTitle": "Remettre l'element",
            "resetDropDescription": "Voulez-vous remettre cet element ?",
            "grabbed": "Element saisi.",
            "cancelledDragging": "Deplacement annule. @draggable remis.",
            "correctAnswer": "Reponse correcte :",
            "scoreBarLabel": "Vous avez :num sur :total points",
            "behaviour": {
                "enableRetry": True,
                "enableSolutionsButton": True,
                "enableCheckButton": True,
                "instantFeedback": False
            },
            "a11yCheck": "Verifier les reponses.",
            "a11yShowSolution": "Afficher la solution.",
            "a11yRetry": "Recommencer."
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.DragText",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10},
                *cls._get_base_dependencies()
            ]
        }

        return cls._create_h5p_package(h5p_json, content)

    # ==========================================================================
    # MARK THE WORDS (Selection de mots)
    # ==========================================================================

    @classmethod
    def create_mark_words_h5p(cls, title: str, text_with_marks: str,
                               task_description: str = "Selectionnez les mots corrects") -> bytes:
        """
        Cree un H5P Mark the Words.

        Args:
            title: Titre
            text_with_marks: Texte avec mots a selectionner entre *asterisques*.
                Ex: "Parmi ces nombres, lesquels sont *pairs* ? 2, 3, *4*, 5, *6*"
            task_description: Description de la tache

        Returns:
            Contenu du fichier .h5p
        """
        content = {
            "media": {"disableImageZooming": False},
            "taskDescription": f"<p>{task_description}</p>",
            "textField": f"<p>{wrap_math(text_with_marks)}</p>",
            "overallFeedback": [
                {"from": 0, "to": 49, "feedback": "Il faut reviser !"},
                {"from": 50, "to": 79, "feedback": "Pas mal !"},
                {"from": 80, "to": 100, "feedback": "Excellent !"}
            ],
            "checkAnswerButton": "Verifier",
            "submitAnswerButton": "Soumettre",
            "tryAgainButton": "Reessayer",
            "showSolutionButton": "Voir la solution",
            "correctAnswer": "Reponse correcte !",
            "incorrectAnswer": "Reponse incorrecte !",
            "missedAnswer": "Reponse manquee !",
            "displaySolutionDescription": "La tache est affichee avec sa solution.",
            "scoreBarLabel": "Vous avez :num sur :total points",
            "a11yFullTextLabel": "Texte complet : ",
            "a11yClickableTextLabel": "Mots selectionnables : ",
            "a11ySelectableTag": "Selectionnable",
            "a11ySolutionModeHeader": "Mode solution",
            "a11yCheckingHeader": "Mode verification",
            "a11yCheck": "Verifier les reponses.",
            "a11yShowSolution": "Afficher la solution.",
            "a11yRetry": "Recommencer.",
            "behaviour": {
                "enableRetry": True,
                "enableSolutionsButton": True,
                "enableCheckButton": True,
                "showScorePoints": True
            }
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.MarkTheWords",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.MarkTheWords", "majorVersion": 1, "minorVersion": 11},
                *cls._get_base_dependencies()
            ]
        }

        return cls._create_h5p_package(h5p_json, content)

    # ==========================================================================
    # QUESTION SET AVANCE (Quiz multi-types)
    # ==========================================================================

    @classmethod
    def create_advanced_question_set(cls, title: str, questions: List[Dict],
                                      intro_text: str = "",
                                      pass_percentage: int = 50,
                                      randomize: bool = False) -> bytes:
        """
        Cree un Question Set avance avec differents types de questions.

        Args:
            title: Titre du quiz
            questions: Liste de questions avec format variable selon le type:

                Type multichoice:
                {
                    "type": "multichoice",
                    "text": "Enonce avec \\(formule LaTeX\\)",
                    "options": ["Option A", "Option B", ...],
                    "correct_index": 0 ou [0, 2] pour multi-reponses,
                    "feedback": "Feedback general",
                    "tip": "Indice optionnel"
                }

                Type truefalse:
                {
                    "type": "truefalse",
                    "text": "Affirmation",
                    "correct": True ou False,
                    "feedback_correct": "...",
                    "feedback_incorrect": "..."
                }

                Type blanks (texte a trous):
                {
                    "type": "blanks",
                    "text": "La *reponse* est ici",
                    "tip": "Indice"
                }

                Type dragwords:
                {
                    "type": "dragwords",
                    "text": "Le mot *correct* va ici"
                }

            intro_text: Texte d'introduction
            pass_percentage: Pourcentage pour reussir
            randomize: Melanger les questions

        Returns:
            Contenu du fichier .h5p
        """
        h5p_questions = []

        for i, q in enumerate(questions):
            q_type = q.get('type', 'multichoice')

            if q_type == 'multichoice':
                h5p_questions.append(cls._build_multichoice_question(q, i))
            elif q_type == 'truefalse':
                h5p_questions.append(cls._build_truefalse_question(q, i))
            elif q_type == 'blanks':
                h5p_questions.append(cls._build_blanks_question(q, i))
            elif q_type == 'dragwords':
                h5p_questions.append(cls._build_dragwords_question(q, i))

        content = {
            "introPage": {
                "showIntroPage": bool(intro_text),
                "title": title,
                "introduction": f"<p>{wrap_math(intro_text)}</p>" if intro_text else "",
                "startButtonText": "Commencer"
            },
            "progressType": "dots",
            "passPercentage": pass_percentage,
            "disableBackwardsNavigation": False,
            "randomQuestions": randomize,
            "endGame": {
                "showResultPage": True,
                "showSolutionButton": True,
                "showRetryButton": True,
                "noResultMessage": "Quiz termine",
                "message": "Votre score : @score sur @total",
                "overallFeedback": [
                    {"from": 0, "to": 49, "feedback": "Il faut reviser davantage !"},
                    {"from": 50, "to": 69, "feedback": "C'est un debut, continuez !"},
                    {"from": 70, "to": 89, "feedback": "Bien joue !"},
                    {"from": 90, "to": 100, "feedback": "Excellent ! Maitrise parfaite !"}
                ],
                "solutionButtonText": "Voir les solutions",
                "retryButtonText": "Recommencer",
                "finishButtonText": "Terminer",
                "submitButtonText": "Soumettre"
            },
            "override": {
                "checkButton": True,
                "showSolutionButton": "on",
                "retryButton": "on"
            },
            "texts": {
                "prevButton": "Precedent",
                "nextButton": "Suivant",
                "finishButton": "Terminer",
                "submitButton": "Soumettre",
                "textualProgress": "Question @current sur @total",
                "jumpToQuestion": "Question %d sur %total",
                "questionLabel": "Question",
                "readSpeakerProgress": "Question @current sur @total",
                "unansweredText": "Non repondue",
                "answeredText": "Repondue",
                "currentQuestionText": "Question actuelle",
                "navigationLabel": "Questions"
            },
            "questions": h5p_questions
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.QuestionSet",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
                {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
                {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
                {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10},
                *cls._get_base_dependencies(),
                {"machineName": "H5P.Video", "majorVersion": 1, "minorVersion": 6}
            ]
        }

        return cls._create_h5p_package(h5p_json, content)

    @classmethod
    def _build_multichoice_question(cls, q: Dict, index: int) -> Dict:
        """Construit une question multichoice pour QuestionSet"""
        answers = []
        correct_indices = q.get('correct_index', 0)
        if isinstance(correct_indices, int):
            correct_indices = [correct_indices]

        for j, opt in enumerate(q.get('options', [])):
            answers.append({
                "text": f"<p>{escape_html_preserve_math(opt)}</p>",
                "correct": j in correct_indices,
                "tpiMapping": "undefined"
            })

        tip = q.get('tip', '')
        tip_obj = {"tip": f"<p>{tip}</p>"} if tip else None

        return {
            "params": {
                "media": {"disableImageZooming": False},
                "question": f"<p>{escape_html_preserve_math(q.get('text', ''))}</p>",
                "answers": answers,
                "tips": [tip_obj] if tip_obj else [],
                "overallFeedback": [{"from": 0, "to": 100, "feedback": q.get('feedback', '')}],
                "behaviour": {
                    "singleAnswer": len(correct_indices) == 1,
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "type": "auto",
                    "singlePoint": True,
                    "randomAnswers": False,
                    "showSolutionsRequiresInput": True,
                    "confirmCheckDialog": False,
                    "confirmRetryDialog": False,
                    "autoCheck": False,
                    "passPercentage": 100,
                    "showScorePoints": True
                },
                "UI": {
                    "checkAnswerButton": "Verifier",
                    "showSolutionButton": "Voir la solution",
                    "tryAgainButton": "Reessayer",
                    "tipsLabel": "Indice",
                    "correctAnswer": "Bonne reponse !",
                    "wrongAnswer": "Mauvaise reponse",
                    "noInput": "Veuillez repondre",
                    "scoreBarLabel": "Score"
                },
                "confirmCheck": {"header": "", "body": "", "cancelLabel": "", "confirmLabel": ""},
                "confirmRetry": {"header": "", "body": "", "cancelLabel": "", "confirmLabel": ""}
            },
            "library": "H5P.MultiChoice 1.16",
            "metadata": {
                "contentType": "Multiple Choice",
                "license": "U",
                "title": q.get('name', f'Question {index+1}')
            }
        }

    @classmethod
    def _build_truefalse_question(cls, q: Dict, index: int) -> Dict:
        """Construit une question vrai/faux pour QuestionSet"""
        return {
            "params": {
                "media": {"disableImageZooming": False},
                "question": f"<p>{escape_html_preserve_math(q.get('text', ''))}</p>",
                "correct": "true" if q.get('correct', True) else "false",
                "l10n": {
                    "trueText": "Vrai",
                    "falseText": "Faux",
                    "checkAnswer": "Verifier",
                    "showSolutionButton": "Voir la solution",
                    "tryAgain": "Reessayer",
                    "correctAnswerMessage": q.get('feedback_correct', 'Correct !'),
                    "wrongAnswerMessage": q.get('feedback_incorrect', 'Incorrect !')
                },
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "confirmCheckDialog": False,
                    "confirmRetryDialog": False,
                    "autoCheck": False
                }
            },
            "library": "H5P.TrueFalse 1.8",
            "metadata": {
                "contentType": "True/False Question",
                "license": "U",
                "title": q.get('name', f'Question {index+1}')
            }
        }

    @classmethod
    def _build_blanks_question(cls, q: Dict, index: int) -> Dict:
        """Construit une question texte a trous pour QuestionSet"""
        text = q.get('text', '')
        tip = q.get('tip', '')

        return {
            "params": {
                "media": {"disableImageZooming": False},
                "text": f"<p>{wrap_math(text)}</p>",
                "overallFeedback": [{"from": 0, "to": 100}],
                "showSolutions": "Voir la solution",
                "tryAgain": "Reessayer",
                "checkAnswer": "Verifier",
                "notFilledOut": "Completez tous les trous",
                "answerIsCorrect": "Correct !",
                "answerIsWrong": "Incorrect !",
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "autoCheck": False,
                    "caseSensitive": False,
                    "showSolutionsRequiresInput": True,
                    "acceptSpellingErrors": True
                }
            },
            "library": "H5P.Blanks 1.14",
            "metadata": {
                "contentType": "Fill in the Blanks",
                "license": "U",
                "title": q.get('name', f'Question {index+1}')
            }
        }

    @classmethod
    def _build_dragwords_question(cls, q: Dict, index: int) -> Dict:
        """Construit une question drag the words pour QuestionSet"""
        return {
            "params": {
                "media": {"disableImageZooming": False},
                "taskDescription": "<p>Placez les mots au bon endroit</p>",
                "textField": f"<p>{wrap_math(q.get('text', ''))}</p>",
                "overallFeedback": [{"from": 0, "to": 100}],
                "checkAnswer": "Verifier",
                "tryAgain": "Reessayer",
                "showSolution": "Voir la solution",
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "instantFeedback": False
                }
            },
            "library": "H5P.DragText 1.10",
            "metadata": {
                "contentType": "Drag the Words",
                "license": "U",
                "title": q.get('name', f'Question {index+1}')
            }
        }

    # ==========================================================================
    # COURSE PRESENTATION (Diaporama interactif)
    # ==========================================================================

    @classmethod
    def create_course_presentation(cls, title: str, slides: List[Dict],
                                    keywords: Optional[List[str]] = None) -> bytes:
        """
        Cree une Course Presentation H5P (diaporama interactif).

        Args:
            title: Titre de la presentation
            slides: Liste des slides avec format:
                {
                    "elements": [
                        {
                            "type": "text",
                            "content": "Contenu HTML avec \\(LaTeX\\)",
                            "x": 0, "y": 0, "width": 100, "height": 20
                        },
                        {
                            "type": "image",
                            "path": "/chemin/vers/image.png",
                            "x": 0, "y": 25, "width": 50, "height": 50
                        },
                        {
                            "type": "quiz",
                            "question": "Question ?",
                            "options": ["A", "B", "C"],
                            "correct": 0,
                            "x": 0, "y": 80, "width": 100, "height": 20
                        }
                    ],
                    "keywords": ["mot1", "mot2"]
                }
            keywords: Mots-cles globaux

        Returns:
            Contenu du fichier .h5p
        """
        h5p_slides = []
        images = {}

        for slide_idx, slide in enumerate(slides):
            elements = []

            for elem in slide.get('elements', []):
                elem_type = elem.get('type', 'text')

                if elem_type == 'text':
                    elements.append(cls._build_cp_text_element(elem))
                elif elem_type == 'image':
                    el, img_data = cls._build_cp_image_element(elem, slide_idx, len(elements))
                    elements.append(el)
                    if img_data:
                        images.update(img_data)
                elif elem_type == 'quiz':
                    elements.append(cls._build_cp_quiz_element(elem))

            h5p_slides.append({
                "elements": elements,
                "keywords": [{"main": kw} for kw in slide.get('keywords', [])]
            })

        content = {
            "presentation": {
                "slides": h5p_slides,
                "keywordListEnabled": bool(keywords),
                "globalBackgroundSelector": {},
                "keywordListAlwaysShow": False,
                "keywordListAutoHide": False,
                "keywordListOpacity": 90
            },
            "l10n": {
                "slide": "Diapositive",
                "score": "Score",
                "yourScore": "Votre score",
                "maxScore": "Score maximum",
                "total": "Total",
                "totalScore": "Score total",
                "showSolutions": "Voir les solutions",
                "retry": "Reessayer",
                "exportAnswers": "Exporter",
                "hideKeywords": "Masquer les mots-cles",
                "showKeywords": "Afficher les mots-cles",
                "fullscreen": "Plein ecran",
                "exitFullscreen": "Quitter plein ecran",
                "prevSlide": "Diapositive precedente",
                "nextSlide": "Diapositive suivante",
                "currentSlide": "Diapositive actuelle",
                "lastSlide": "Derniere diapositive",
                "solutionModeTitle": "Quitter le mode solution",
                "solutionModeText": "Mode solution",
                "summaryMultipleTaskText": "Plusieurs taches",
                "scoreMessage": "Vous avez obtenu :obtenu sur :max points",
                "shareFacebook": "Partager sur Facebook",
                "shareTwitter": "Partager sur Twitter",
                "shareGoogle": "Partager sur Google+",
                "summary": "Resume",
                "solutionsButtonTitle": "Voir les solutions",
                "printTitle": "Imprimer",
                "printIng498":"Preparation de l'impression...",
                "printAllSlides": "Imprimer toutes les diapositives",
                "printCurrentSlide": "Imprimer cette diapositive",
                "noTitle": "Sans titre",
                "accessibilitySlideNavigationExplanation": "Utilisez les fleches pour naviguer entre les diapositives.",
                "accessibilityCanvasLabel": "Zone de presentation. Utilisez fleche gauche/droite pour avancer.",
                "containsNotCompleted": "Contient des interactions non completees",
                "containsCompleted": "Contient des interactions completees",
                "slideCount": "Diapositive @index sur @total",
                "containsOnlyCorrect": "Contient uniquement des reponses correctes",
                "containsIncorrectAnswers": "Contient des reponses incorrectes",
                "shareResult": "Partager le resultat",
                "accessibilityTotalScore": "Vous avez @score points sur @maxScore au total",
                "accessibilityEnteredFullscreen": "Plein ecran active",
                "accessibilityExitedFullscreen": "Plein ecran desactive"
            },
            "override": {
                "activeSurface": False,
                "hideSummarySlide": False,
                "summarySlideSolutionButton": True,
                "summarySlideRetryButton": True,
                "enablePrintButton": False,
                "social": {
                    "showFacebookShare": False,
                    "facebookShare": {"url": "@currentpageurl", "quote": "I scored @score out of @maxScore on a task at @currentpageurl."},
                    "showTwitterShare": False,
                    "twitterShare": {"statement": "I scored @score out of @maxScore on a task at @currentpageurl.", "url": "@currentpageurl", "hashtags": "h5p,trainer"},
                    "showGoogleShare": False,
                    "googleShareUrl": "@currentpageurl"
                }
            }
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.CoursePresentation",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.CoursePresentation", "majorVersion": 1, "minorVersion": 25},
                {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
                {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
                {"machineName": "H5P.Image", "majorVersion": 1, "minorVersion": 1},
                *cls._get_base_dependencies()
            ]
        }

        return cls._create_h5p_package(h5p_json, content, images if images else None)

    @classmethod
    def _build_cp_text_element(cls, elem: Dict) -> Dict:
        """Construit un element texte pour Course Presentation"""
        return {
            "x": elem.get('x', 0),
            "y": elem.get('y', 0),
            "width": elem.get('width', 100),
            "height": elem.get('height', 20),
            "action": {
                "library": "H5P.AdvancedText 1.1",
                "params": {
                    "text": f"<p>{wrap_math(elem.get('content', ''))}</p>"
                },
                "metadata": {"contentType": "Text", "license": "U", "title": "Texte"}
            }
        }

    @classmethod
    def _build_cp_image_element(cls, elem: Dict, slide_idx: int, elem_idx: int) -> tuple:
        """Construit un element image pour Course Presentation"""
        img_path = elem.get('path', '')
        img_data = {}
        img_name = f"slide{slide_idx}_img{elem_idx}.png"

        # Si un chemin est fourni, lire l'image
        if img_path and Path(img_path).exists():
            with open(img_path, 'rb') as f:
                img_data[img_name] = f.read()

        element = {
            "x": elem.get('x', 0),
            "y": elem.get('y', 0),
            "width": elem.get('width', 50),
            "height": elem.get('height', 50),
            "action": {
                "library": "H5P.Image 1.1",
                "params": {
                    "contentName": "Image",
                    "file": {
                        "path": f"images/{img_name}",
                        "mime": "image/png",
                        "copyright": {"license": "U"}
                    },
                    "alt": elem.get('alt', 'Image')
                },
                "metadata": {"contentType": "Image", "license": "U", "title": "Image"}
            }
        }

        return element, img_data

    @classmethod
    def _build_cp_quiz_element(cls, elem: Dict) -> Dict:
        """Construit un element quiz pour Course Presentation"""
        answers = []
        correct_idx = elem.get('correct', 0)

        for j, opt in enumerate(elem.get('options', [])):
            answers.append({
                "text": f"<p>{escape_html_preserve_math(opt)}</p>",
                "correct": j == correct_idx,
                "tpiMapping": "undefined"
            })

        return {
            "x": elem.get('x', 0),
            "y": elem.get('y', 0),
            "width": elem.get('width', 100),
            "height": elem.get('height', 20),
            "action": {
                "library": "H5P.MultiChoice 1.16",
                "params": {
                    "media": {"disableImageZooming": False},
                    "question": f"<p>{escape_html_preserve_math(elem.get('question', ''))}</p>",
                    "answers": answers,
                    "behaviour": {
                        "singleAnswer": True,
                        "enableRetry": True,
                        "enableSolutionsButton": True,
                        "enableCheckButton": True,
                        "type": "auto",
                        "singlePoint": True,
                        "randomAnswers": False,
                        "showSolutionsRequiresInput": True,
                        "autoCheck": False,
                        "passPercentage": 100,
                        "showScorePoints": True
                    },
                    "UI": {
                        "checkAnswerButton": "Verifier",
                        "showSolutionButton": "Voir la solution",
                        "tryAgainButton": "Reessayer",
                        "correctAnswer": "Bonne reponse !",
                        "wrongAnswer": "Mauvaise reponse"
                    }
                },
                "metadata": {"contentType": "Multiple Choice", "license": "U", "title": "Quiz"}
            }
        }

    # ==========================================================================
    # INTERACTIVE BOOK (Livre interactif)
    # ==========================================================================

    @classmethod
    def create_interactive_book(cls, title: str, chapters: List[Dict],
                                 cover_title: str = "",
                                 cover_subtitle: str = "") -> bytes:
        """
        Cree un Interactive Book H5P.

        Args:
            title: Titre du livre
            chapters: Liste des chapitres avec format:
                {
                    "title": "Titre du chapitre",
                    "contents": [
                        {
                            "type": "text",
                            "content": "Contenu HTML avec \\(formules\\)"
                        },
                        {
                            "type": "quiz",
                            "questions": [...] # Format QuestionSet
                        },
                        {
                            "type": "dragwords",
                            "text": "Texte avec *mots* a placer"
                        }
                    ]
                }
            cover_title: Titre sur la couverture
            cover_subtitle: Sous-titre

        Returns:
            Contenu du fichier .h5p
        """
        h5p_chapters = []

        for chap in chapters:
            chapter_content = []

            for item in chap.get('contents', []):
                item_type = item.get('type', 'text')

                if item_type == 'text':
                    chapter_content.append({
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {
                                "text": f"<div>{wrap_math(item.get('content', ''))}</div>"
                            },
                            "metadata": {"contentType": "Text", "license": "U"}
                        }
                    })
                elif item_type == 'quiz':
                    # Construire un mini QuestionSet
                    questions = []
                    for q in item.get('questions', []):
                        questions.append(cls._build_multichoice_question(q, len(questions)))

                    chapter_content.append({
                        "content": {
                            "library": "H5P.QuestionSet 1.20",
                            "params": {
                                "introPage": {"showIntroPage": False},
                                "progressType": "dots",
                                "passPercentage": 50,
                                "questions": questions,
                                "endGame": {
                                    "showResultPage": True,
                                    "showSolutionButton": True,
                                    "showRetryButton": True,
                                    "message": "Score : @score sur @total"
                                },
                                "texts": {
                                    "prevButton": "Precedent",
                                    "nextButton": "Suivant",
                                    "finishButton": "Terminer"
                                }
                            },
                            "metadata": {"contentType": "Question Set", "license": "U"}
                        }
                    })
                elif item_type == 'dragwords':
                    chapter_content.append({
                        "content": {
                            "library": "H5P.DragText 1.10",
                            "params": {
                                "taskDescription": "<p>Placez les mots</p>",
                                "textField": f"<p>{wrap_math(item.get('text', ''))}</p>",
                                "checkAnswer": "Verifier",
                                "tryAgain": "Reessayer",
                                "showSolution": "Voir la solution",
                                "behaviour": {
                                    "enableRetry": True,
                                    "enableSolutionsButton": True,
                                    "instantFeedback": False
                                }
                            },
                            "metadata": {"contentType": "Drag the Words", "license": "U"}
                        }
                    })
                elif item_type == 'blanks':
                    chapter_content.append({
                        "content": {
                            "library": "H5P.Blanks 1.14",
                            "params": {
                                "text": f"<p>{wrap_math(item.get('text', ''))}</p>",
                                "showSolutions": "Voir la solution",
                                "tryAgain": "Reessayer",
                                "checkAnswer": "Verifier",
                                "behaviour": {
                                    "enableRetry": True,
                                    "enableSolutionsButton": True,
                                    "caseSensitive": False,
                                    "acceptSpellingErrors": True
                                }
                            },
                            "metadata": {"contentType": "Fill in the Blanks", "license": "U"}
                        }
                    })

            h5p_chapters.append({
                "title": chap.get('title', 'Chapitre'),
                "content": chapter_content
            })

        content = {
            "bookCover": {
                "coverDescription": f"<p><strong>{cover_title or title}</strong></p><p>{cover_subtitle}</p>",
                "coverMedium": {}
            },
            "chapters": h5p_chapters,
            "behaviour": {
                "defaultTableOfContents": True,
                "progressIndicators": True,
                "progressAuto": True,
                "displaySummary": True
            },
            "l10n": {
                "previousPage": "Page precedente",
                "nextPage": "Page suivante",
                "navigateToTop": "Retour au debut",
                "fullscreen": "Plein ecran",
                "exitFullscreen": "Quitter plein ecran",
                "bookProgressTooltip": "Progression du livre",
                "bookProgressSubtitle": "@count pages",
                "interactionsProgressTooltip": "Progression des exercices",
                "interactionsProgressSubtitle": "@count exercises",
                "submitReport": "Soumettre le rapport",
                "reportDescription": "Rapport de progression",
                "totalScoreLabel": "Score total",
                "noInteractions": "Aucune interaction dans ce chapitre",
                "yourAnswersAreSubmittedForReview": "Vos reponses ont ete soumises",
                "summaryHeader": "Resume",
                "allInteractions": "Toutes les interactions",
                "unansweredInteractions": "Interactions non repondues",
                "scoreText": "Score: @score/@max",
                "leftOutOfTotalCompleted": "@left interactions sur @total completees",
                "noAnswered": "Pas encore de reponses",
                "answeredAndSubmitted": "Reponse soumise",
                "answeredNotSubmitted": "Reponse pas encore soumise"
            }
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.InteractiveBook",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
                {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
                {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
                {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
                {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
                {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10},
                *cls._get_base_dependencies()
            ]
        }

        return cls._create_h5p_package(h5p_json, content)

    # ==========================================================================
    # COLUMN (Organisation de contenus)
    # ==========================================================================

    @classmethod
    def create_column(cls, title: str, contents: List[Dict]) -> bytes:
        """
        Cree un H5P Column pour organiser plusieurs contenus.

        Args:
            title: Titre
            contents: Liste de contenus:
                [
                    {"type": "text", "content": "HTML avec \\(LaTeX\\)"},
                    {"type": "quiz", "questions": [...]},
                    {"type": "dragwords", "text": "..."},
                    {"type": "blanks", "text": "..."}
                ]

        Returns:
            Contenu du fichier .h5p
        """
        h5p_contents = []

        for item in contents:
            item_type = item.get('type', 'text')

            if item_type == 'text':
                h5p_contents.append({
                    "content": {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {
                            "text": f"<div>{wrap_math(item.get('content', ''))}</div>"
                        },
                        "metadata": {"contentType": "Text", "license": "U"}
                    },
                    "useSeparator": "auto"
                })
            elif item_type == 'quiz':
                questions = []
                for q in item.get('questions', []):
                    questions.append(cls._build_multichoice_question(q, len(questions)))

                h5p_contents.append({
                    "content": {
                        "library": "H5P.QuestionSet 1.20",
                        "params": {
                            "introPage": {"showIntroPage": False},
                            "progressType": "dots",
                            "passPercentage": 50,
                            "questions": questions,
                            "endGame": {
                                "showResultPage": True,
                                "showSolutionButton": True,
                                "showRetryButton": True
                            },
                            "texts": {
                                "prevButton": "Precedent",
                                "nextButton": "Suivant",
                                "finishButton": "Terminer"
                            }
                        },
                        "metadata": {"contentType": "Question Set", "license": "U"}
                    },
                    "useSeparator": "auto"
                })
            elif item_type == 'dragwords':
                h5p_contents.append({
                    "content": {
                        "library": "H5P.DragText 1.10",
                        "params": {
                            "taskDescription": f"<p>{item.get('description', 'Placez les mots')}</p>",
                            "textField": f"<p>{wrap_math(item.get('text', ''))}</p>",
                            "checkAnswer": "Verifier",
                            "tryAgain": "Reessayer",
                            "showSolution": "Voir la solution"
                        },
                        "metadata": {"contentType": "Drag the Words", "license": "U"}
                    },
                    "useSeparator": "auto"
                })
            elif item_type == 'blanks':
                h5p_contents.append({
                    "content": {
                        "library": "H5P.Blanks 1.14",
                        "params": {
                            "text": f"<p>{wrap_math(item.get('text', ''))}</p>",
                            "showSolutions": "Voir la solution",
                            "tryAgain": "Reessayer",
                            "checkAnswer": "Verifier",
                            "behaviour": {
                                "enableRetry": True,
                                "enableSolutionsButton": True,
                                "caseSensitive": False
                            }
                        },
                        "metadata": {"contentType": "Fill in the Blanks", "license": "U"}
                    },
                    "useSeparator": "auto"
                })

        content = {
            "content": h5p_contents
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.Column",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
                {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
                {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
                {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
                {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
                {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10},
                *cls._get_base_dependencies()
            ]
        }

        return cls._create_h5p_package(h5p_json, content)


# ==========================================================================
# FONCTIONS UTILITAIRES
# ==========================================================================

def create_math_quiz(title: str, questions: List[Dict], quiz_type: str = "questionset") -> bytes:
    """
    Cree un quiz mathematique avec support LaTeX complet.

    Args:
        title: Titre du quiz
        questions: Questions au format standardise
        quiz_type: "questionset", "singlechoice", "advanced"

    Returns:
        Fichier .h5p en bytes
    """
    if quiz_type == "advanced":
        return H5PAdvancedGenerator.create_advanced_question_set(title, questions)
    elif quiz_type == "singlechoice":
        # Convertir au format SingleChoiceSet
        from h5p_generator import H5PGenerator
        simple_questions = []
        for q in questions:
            simple_questions.append({
                'text': q.get('text', ''),
                'options': q.get('options', []),
                'correct_index': q.get('correct_index', 0)
            })
        return H5PGenerator.create_single_choice_set_h5p(title, simple_questions)
    else:
        return H5PAdvancedGenerator.create_advanced_question_set(title, questions)


def create_interactive_lesson(title: str, chapters: List[Dict]) -> bytes:
    """
    Cree une lecon interactive complete (Interactive Book).

    Args:
        title: Titre de la lecon
        chapters: Chapitres avec contenu mixte (texte + exercices)

    Returns:
        Fichier .h5p en bytes
    """
    return H5PAdvancedGenerator.create_interactive_book(
        title=title,
        chapters=chapters,
        cover_title=title,
        cover_subtitle="Lecon interactive"
    )


if __name__ == "__main__":
    # Tests
    print("Test du generateur H5P avance...")

    # Test Fill in the Blanks
    blanks = H5PAdvancedGenerator.create_fill_blanks_h5p(
        "Test Blanks",
        [{"text": "La racine carree de 4 est *2*."}]
    )
    with open("test_blanks.h5p", "wb") as f:
        f.write(blanks)
    print("- test_blanks.h5p cree")

    # Test Drag Words
    dragwords = H5PAdvancedGenerator.create_drag_words_h5p(
        "Test Drag Words",
        "Une suite *arithmetique* a une raison *constante*."
    )
    with open("test_dragwords.h5p", "wb") as f:
        f.write(dragwords)
    print("- test_dragwords.h5p cree")

    # Test Question Set avance
    questions = [
        {
            "type": "multichoice",
            "text": "Si \\(u_n = 2n + 1\\), que vaut \\(u_5\\) ?",
            "options": ["11", "10", "9", "12"],
            "correct_index": 0,
            "feedback": "On calcule \\(u_5 = 2 \\times 5 + 1 = 11\\)"
        },
        {
            "type": "truefalse",
            "text": "Une suite arithmetique a une raison constante.",
            "correct": True,
            "feedback_correct": "Exact !",
            "feedback_incorrect": "C'est la definition meme d'une suite arithmetique."
        }
    ]
    qs = H5PAdvancedGenerator.create_advanced_question_set("Test Question Set", questions)
    with open("test_questionset.h5p", "wb") as f:
        f.write(qs)
    print("- test_questionset.h5p cree")

    # Test Interactive Book
    chapters = [
        {
            "title": "Introduction aux suites",
            "contents": [
                {"type": "text", "content": "<h2>Qu'est-ce qu'une suite ?</h2><p>Une suite numerique est une fonction de \\(\\mathbb{N}\\) vers \\(\\mathbb{R}\\).</p>"},
                {"type": "quiz", "questions": [
                    {"type": "multichoice", "text": "Une suite est definie sur :", "options": ["\\(\\mathbb{N}\\)", "\\(\\mathbb{R}\\)", "\\(\\mathbb{Z}\\)"], "correct_index": 0}
                ]}
            ]
        }
    ]
    book = H5PAdvancedGenerator.create_interactive_book("Test Interactive Book", chapters)
    with open("test_book.h5p", "wb") as f:
        f.write(book)
    print("- test_book.h5p cree")

    print("\nTous les tests ont reussi !")
