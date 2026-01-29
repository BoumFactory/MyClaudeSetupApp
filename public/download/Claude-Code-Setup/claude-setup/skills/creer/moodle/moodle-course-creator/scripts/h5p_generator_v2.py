#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur H5P v2 avec métadonnées complètes pour Moodle.
Supporte: Question Set, Single Choice Set, Fill in the Blanks, Drag the Words, True/False

IMPORTANT: Tout est en français, avec support MathJax pour les formules LaTeX.
Syntaxe LaTeX: \\(formule\\) pour inline, \\[formule\\] pour display.
"""

import json
import zipfile
import io
import re
from typing import List, Dict, Optional, Union
from datetime import datetime
import html


def escape_html_preserve_math(text: str) -> str:
    """Échappe HTML tout en préservant les formules LaTeX MathJax"""
    if not text:
        return ""

    result = str(text)

    # Protéger les formules LaTeX
    math_blocks = []

    def protect_block(m):
        math_blocks.append(m.group(0))
        return f"__MATH_BLOCK_{len(math_blocks)-1}__"

    # Protéger \[ \] et \( \)
    result = re.sub(r'\\\[.*?\\\]', protect_block, result, flags=re.DOTALL)
    result = re.sub(r'\\\(.*?\\\)', protect_block, result, flags=re.DOTALL)

    # Échapper HTML (mais pas les balises qu'on veut garder)
    # Pour H5P, on garde le HTML tel quel si c'est déjà du HTML
    if '<p>' in result or '<strong>' in result or '<div>' in result:
        # C'est déjà du HTML, ne pas échapper
        pass
    else:
        result = html.escape(result)

    # Restaurer les maths
    for i, block in enumerate(math_blocks):
        result = result.replace(f"__MATH_BLOCK_{i}__", block)

    return result


class H5PGeneratorV2:
    """Générateur H5P avec métadonnées complètes et types variés - Tout en français"""

    DEFAULT_METADATA = {
        "license": "CC BY-SA",
        "licenseVersion": "4.0",
        "yearFrom": str(datetime.now().year),
        "yearTo": str(datetime.now().year),
        "source": "",
        "authors": [{"name": "ROMAIN DESCHAMPS", "role": "Author"}],
        "licenseExtras": "",
        "changes": [],
        "authorComments": ""
    }

    @classmethod
    def _create_h5p_package(cls, h5p_json: Dict, content: Dict,
                            title: str, metadata: Dict = None) -> bytes:
        """Crée un package .h5p avec métadonnées complètes

        IMPORTANT: Ne PAS ajouter metadata au top-level de content.json
        car cela perturbe l'import via .mbz dans Moodle.
        Les métadonnées sont dans h5p.json uniquement.
        """
        # Note: metadata n'est PAS ajouté à content pour compatibilité .mbz
        # (Le Game Map fonctionne sans metadata au top-level)

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
            zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False, indent=2))

        return buffer.getvalue()

    # =========================================================================
    # FILL IN THE BLANKS (Textes à trous) - CORRIGÉ
    # =========================================================================
    @classmethod
    def create_fill_in_blanks(cls, title: str,
                               questions: List[str],
                               task_description: str = "Complétez les trous avec les mots appropriés.",
                               author: str = "ROMAIN DESCHAMPS") -> bytes:
        """
        Crée un Fill in the Blanks H5P.

        Syntaxe des trous: *mot* ou *mot1/mot2* pour alternatives
        Exemple: ["Une suite est définie sur *N* à valeurs dans *R*."]

        Args:
            title: Titre de l'exercice
            questions: Liste de textes avec *trous* marqués (chaque élément = un bloc)
            task_description: Description de la tâche
            author: Auteur
        """

        content = {
            "media": {"disableImageZooming": False},
            "taskDescription": f"<p>{escape_html_preserve_math(task_description)}</p>",
            "questions": [f"<p>{escape_html_preserve_math(q)}</p>" for q in questions],
            "overallFeedback": [
                {"from": 0, "to": 50, "feedback": "Révisez davantage !"},
                {"from": 51, "to": 75, "feedback": "Pas mal, continuez !"},
                {"from": 76, "to": 100, "feedback": "Excellent travail !"}
            ],
            "showSolutions": "Voir la solution",
            "tryAgain": "Réessayer",
            "checkAnswer": "Vérifier",
            "submitAnswer": "Soumettre",
            "notFilledOut": "Veuillez remplir tous les trous avant de vérifier.",
            "answerIsCorrect": "« :ans » est correct",
            "answerIsWrong": "« :ans » est incorrect",
            "answeredCorrectly": "Correct !",
            "answeredIncorrectly": "Incorrect",
            "solutionLabel": "Réponse correcte :",
            "inputLabel": "Trou @num sur @total",
            "inputHasTipLabel": "Indice disponible",
            "tipLabel": "Afficher l'indice",
            "behaviour": {
                "enableRetry": True,
                "enableSolutionsButton": True,
                "enableCheckButton": True,
                "caseSensitive": False,
                "showSolutionsRequiresInput": True,
                "autoCheck": False,
                "separateLines": False,
                "acceptSpellingErrors": True
            },
            "scoreBarLabel": "Vous avez obtenu :num sur :total points",
            "a11yCheck": "Vérifier les réponses. Les réponses seront marquées correctes ou incorrectes.",
            "a11yShowSolution": "Afficher la solution. Les bonnes réponses seront affichées.",
            "a11yRetry": "Recommencer. Toutes les réponses seront effacées.",
            "a11yCheckingModeHeader": "Mode vérification"
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.Blanks",
            "embedTypes": ["iframe"],
            "license": "CC BY-SA",
            "licenseVersion": "4.0",
            "defaultLanguage": "fr",
            "authors": [{"name": author, "role": "Author"}],
            "preloadedDependencies": [
                {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
                {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5},
                {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.TextUtilities", "majorVersion": 1, "minorVersion": 3}
            ]
        }

        return cls._create_h5p_package(h5p_json, content, title, {
            "authors": [{"name": author, "role": "Author"}]
        })

    # =========================================================================
    # DRAG THE WORDS (Mots à glisser) - CORRIGÉ
    # =========================================================================
    @classmethod
    def create_drag_words(cls, title: str,
                          text_field: str,
                          task_description: str = "Glissez les mots dans les emplacements corrects.",
                          author: str = "ROMAIN DESCHAMPS") -> bytes:
        """
        Crée un Drag the Words H5P.

        Syntaxe: *mot* pour les mots à glisser
        Exemple: "Le nombre \\(u_n\\) est le *terme* *général* de la suite."

        Args:
            title: Titre
            text_field: Texte avec *mots* à glisser
            task_description: Description de la tâche
            author: Auteur
        """

        content = {
            "media": {"disableImageZooming": False},
            "taskDescription": f"<p>{escape_html_preserve_math(task_description)}</p>",
            "textField": escape_html_preserve_math(text_field),
            "overallFeedback": [
                {"from": 0, "to": 50, "feedback": "Révisez davantage !"},
                {"from": 51, "to": 75, "feedback": "Pas mal !"},
                {"from": 76, "to": 100, "feedback": "Excellent !"}
            ],
            "checkAnswer": "Vérifier",
            "submitAnswer": "Soumettre",
            "tryAgain": "Réessayer",
            "showSolution": "Voir la solution",
            "dropZoneIndex": "Zone de dépôt @index.",
            "empty": "La zone @index est vide.",
            "contains": "La zone @index contient le mot @draggable.",
            "ariaDraggableIndex": "@index sur @count éléments déplaçables.",
            "tipLabel": "Afficher l'indice",
            "correctText": "Correct !",
            "incorrectText": "Incorrect",
            "resetDropTitle": "Réinitialiser",
            "resetDropDescription": "Êtes-vous sûr de vouloir réinitialiser ?",
            "grabbed": "Élément saisi.",
            "cancelledDragging": "Déplacement annulé.",
            "correctAnswer": "Bonne réponse",
            "wrongAnswer": "Mauvaise réponse",
            "feedbackHeader": "Résultat",
            "scoreBarLabel": "Vous avez obtenu :num sur :total points",
            "a11yCheck": "Vérifier les réponses",
            "a11yShowSolution": "Afficher la solution",
            "a11yRetry": "Recommencer",
            "behaviour": {
                "enableRetry": True,
                "enableSolutionsButton": True,
                "enableCheckButton": True,
                "instantFeedback": False
            }
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.DragText",
            "embedTypes": ["iframe"],
            "license": "CC BY-SA",
            "licenseVersion": "4.0",
            "defaultLanguage": "fr",
            "authors": [{"name": author, "role": "Author"}],
            "preloadedDependencies": [
                {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10},
                {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5},
                {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.TextUtilities", "majorVersion": 1, "minorVersion": 3}
            ]
        }

        return cls._create_h5p_package(h5p_json, content, title, {
            "authors": [{"name": author, "role": "Author"}]
        })

    # =========================================================================
    # TRUE/FALSE (Vrai/Faux) - CORRIGÉ
    # =========================================================================
    @classmethod
    def create_true_false(cls, title: str, question: str, correct_answer: bool,
                          author: str = "ROMAIN DESCHAMPS",
                          feedback_correct: str = "Correct !",
                          feedback_incorrect: str = "Incorrect.") -> bytes:
        """
        Crée un True/False H5P.

        Args:
            title: Titre
            question: L'affirmation à juger
            correct_answer: True si l'affirmation est vraie
            author: Auteur
            feedback_correct: Feedback si bonne réponse
            feedback_incorrect: Feedback si mauvaise réponse
        """

        content = {
            "media": {"disableImageZooming": False},
            "question": f"<p>{escape_html_preserve_math(question)}</p>",
            "correct": "true" if correct_answer else "false",
            "behaviour": {
                "enableRetry": True,
                "enableSolutionsButton": True,
                "enableCheckButton": True,
                "confirmCheckDialog": False,
                "confirmRetryDialog": False,
                "autoCheck": False
            },
            "l10n": {
                "trueText": "Vrai",
                "falseText": "Faux",
                "score": "Vous avez obtenu @score sur @total points",
                "checkAnswer": "Vérifier",
                "submitAnswer": "Soumettre",
                "showSolutionButton": "Voir la solution",
                "tryAgain": "Réessayer",
                "wrongAnswerMessage": escape_html_preserve_math(feedback_incorrect),
                "correctAnswerMessage": escape_html_preserve_math(feedback_correct),
                "scoreBarLabel": "Vous avez obtenu :num sur :total points",
                "a11yCheck": "Vérifier la réponse",
                "a11yShowSolution": "Afficher la solution",
                "a11yRetry": "Recommencer"
            },
            "confirmCheck": {
                "header": "Terminer ?",
                "body": "Êtes-vous sûr de vouloir terminer ?",
                "cancelLabel": "Annuler",
                "confirmLabel": "Confirmer"
            },
            "confirmRetry": {
                "header": "Recommencer ?",
                "body": "Êtes-vous sûr de vouloir recommencer ?",
                "cancelLabel": "Annuler",
                "confirmLabel": "Confirmer"
            }
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.TrueFalse",
            "embedTypes": ["iframe"],
            "license": "CC BY-SA",
            "licenseVersion": "4.0",
            "defaultLanguage": "fr",
            "authors": [{"name": author, "role": "Author"}],
            "preloadedDependencies": [
                {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
                {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5},
                {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0}
            ]
        }

        return cls._create_h5p_package(h5p_json, content, title, {
            "authors": [{"name": author, "role": "Author"}]
        })

    # =========================================================================
    # QUESTION SET (Quiz multi-questions) - CORRIGÉ
    # =========================================================================
    @classmethod
    def create_question_set(cls, title: str, questions: List[Dict],
                           author: str = "ROMAIN DESCHAMPS",
                           intro_text: str = "",
                           pass_percentage: int = 50,
                           randomize: bool = False) -> bytes:
        """
        Crée un Question Set H5P avec types mixtes - Tout en français.

        Args:
            title: Titre du quiz
            questions: Liste de questions:
                - MultiChoice: {"type": "multichoice", "text": "...", "options": [...], "correct_index": 0}
                - TrueFalse: {"type": "truefalse", "text": "...", "correct": True/False}
                - Fill Blanks: {"type": "blanks", "text": "Texte avec *trous*"}
                - Drag Words: {"type": "dragwords", "text": "Texte avec *mots*"}
            author: Auteur
            intro_text: Texte d'introduction
            pass_percentage: % pour réussir
            randomize: Mélanger les questions
        """

        h5p_questions = []

        for i, q in enumerate(questions):
            q_type = q.get('type', 'multichoice')

            # Support des deux formats de question : "text" ou "question"
            question_text = q.get('text', q.get('question', ''))

            if q_type == 'multichoice':
                answers = []
                options = q.get('options', [])

                # Détecter le format des options
                if options and isinstance(options[0], dict):
                    # Format avancé : [{"text": "...", "correct": True, "feedback": "..."}, ...]
                    for j, opt in enumerate(options):
                        opt_text = opt.get('text', str(opt))
                        opt_correct = opt.get('correct', False)
                        opt_feedback = opt.get('feedback', '')
                        # ORDRE CRITIQUE pour compatibilité Moodle .mbz : correct, tipsAndFeedback, text
                        answers.append({
                            "correct": opt_correct,
                            "tipsAndFeedback": {
                                "tip": q.get('tip', ''),
                                "chosenFeedback": f"<div>{escape_html_preserve_math(opt_feedback)}</div>" if opt_feedback else "",
                                "notChosenFeedback": ""
                            },
                            "text": f"<div>{escape_html_preserve_math(opt_text)}</div>\n"  # \n obligatoire
                        })
                else:
                    # Format simple : ["option1", "option2", ...]
                    correct_idx = q.get('correct_index', 0)
                    if isinstance(correct_idx, int):
                        correct_idx = [correct_idx]
                    for j, opt in enumerate(options):
                        # ORDRE CRITIQUE pour compatibilité Moodle .mbz : correct, tipsAndFeedback, text
                        answers.append({
                            "correct": j in correct_idx,
                            "tipsAndFeedback": {
                                "tip": q.get('tip', ''),
                                "chosenFeedback": "",
                                "notChosenFeedback": ""
                            },
                            "text": f"<div>{escape_html_preserve_math(opt)}</div>\n"  # \n obligatoire
                        })

                feedback = q.get('feedback', '')

                h5p_questions.append({
                    "params": {
                        "media": {"disableImageZooming": False},
                        "question": f"<p>{escape_html_preserve_math(question_text)}</p>\n",
                        "answers": answers,
                        "overallFeedback": [
                            {"from": 0, "to": 0, "feedback": "Dommage ! Relis bien la question."},
                            {"from": 1, "to": 99, "feedback": "Presque ! Réfléchis encore."},
                            {"from": 100, "to": 100, "feedback": "Parfait !"}
                        ],
                        "behaviour": {
                            "enableRetry": True,
                            "enableSolutionsButton": True,
                            "enableCheckButton": True,
                            "type": "auto",
                            "singlePoint": False,  # False pour compatibilité Moodle .mbz
                            "randomAnswers": q.get('randomize_answers', False),
                            "showSolutionsRequiresInput": True,
                            "confirmCheckDialog": False,
                            "confirmRetryDialog": False,
                            "autoCheck": False,
                            "passPercentage": 100,
                            "showScorePoints": True
                        },
                        "UI": {
                            "checkAnswerButton": "Vérifier",
                            "submitAnswerButton": "Soumettre",
                            "showSolutionButton": "Voir la solution",
                            "tryAgainButton": "Réessayer",
                            "tipsLabel": "Indice",
                            "scoreBarLabel": "Score : :num sur :total",
                            "tipAvailable": "Indice disponible",
                            "feedbackAvailable": "Explication disponible",
                            "readFeedback": "Lire l'explication",
                            "wrongAnswer": "Incorrect",
                            "correctAnswer": "Correct !",
                            "shouldCheck": "À cocher",
                            "shouldNotCheck": "À ne pas cocher",
                            "noInput": "Réponds avant de voir la solution",
                            "a11yCheck": "Vérifier les réponses.",
                            "a11yShowSolution": "Afficher la solution.",
                            "a11yRetry": "Recommencer."
                        },
                        "confirmCheck": {
                            "header": "Valider ?",
                            "body": "Es-tu sûr de ta réponse ?",
                            "cancelLabel": "Annuler",
                            "confirmLabel": "Valider"
                        },
                        "confirmRetry": {
                            "header": "Réessayer ?",
                            "body": "Tu vas recommencer cette question.",
                            "cancelLabel": "Annuler",
                            "confirmLabel": "Valider"
                        }
                    },
                    "library": "H5P.MultiChoice 1.16",
                    "metadata": {
                        "contentType": "Multiple Choice",
                        "license": "U",
                        "title": q.get('name', f'Question {i+1}')
                    },
                    "subContentId": f"mc-{i+1}-{abs(hash(q.get('text', ''))) % 10000:04d}"
                })

            elif q_type == 'truefalse':
                h5p_questions.append({
                    "params": {
                        "media": {"disableImageZooming": False},
                        "question": f"<p>{escape_html_preserve_math(question_text)}</p>",
                        "correct": "true" if q.get('correct', True) else "false",
                        "behaviour": {
                            "enableRetry": True,
                            "enableSolutionsButton": True,
                            "enableCheckButton": True,
                            "confirmCheckDialog": False,
                            "confirmRetryDialog": False,
                            "autoCheck": False
                        },
                        "l10n": {
                            "trueText": "Vrai",
                            "falseText": "Faux",
                            "score": "Vous avez obtenu @score sur @total points",
                            "checkAnswer": "Vérifier",
                            "showSolutionButton": "Voir la solution",
                            "tryAgain": "Réessayer",
                            "wrongAnswerMessage": escape_html_preserve_math(q.get('feedback_incorrect', 'Incorrect.')),
                            "correctAnswerMessage": escape_html_preserve_math(q.get('feedback_correct', 'Correct !'))
                        }
                    },
                    "library": "H5P.TrueFalse 1.8",
                    "metadata": {
                        "contentType": "True/False Question",
                        "license": "U",
                        "title": q.get('name', f'Question {i+1}')
                    },
                    "subContentId": f"tf-{i+1}-{abs(hash(q.get('text', ''))) % 10000:04d}"
                })

            elif q_type == 'blanks':
                # Questions est une liste de textes pour Fill in the Blanks
                blanks_text = question_text
                h5p_questions.append({
                    "params": {
                        "media": {"disableImageZooming": False},
                        "taskDescription": "<p>Complétez les trous.</p>",
                        "questions": [f"<p>{escape_html_preserve_math(blanks_text)}</p>"],
                        "overallFeedback": [
                            {"from": 0, "to": 100, "feedback": ""}
                        ],
                        "showSolutions": "Voir la solution",
                        "tryAgain": "Réessayer",
                        "checkAnswer": "Vérifier",
                        "submitAnswer": "Soumettre",
                        "notFilledOut": "Remplissez tous les trous.",
                        "answerIsCorrect": "« :ans » est correct",
                        "answerIsWrong": "« :ans » est incorrect",
                        "answeredCorrectly": "Correct !",
                        "answeredIncorrectly": "Incorrect",
                        "solutionLabel": "Solution :",
                        "inputLabel": "Trou @num sur @total",
                        "inputHasTipLabel": "Indice disponible",
                        "tipLabel": "Afficher l'indice",
                        "behaviour": {
                            "enableRetry": True,
                            "enableSolutionsButton": True,
                            "enableCheckButton": True,
                            "caseSensitive": False,
                            "showSolutionsRequiresInput": True,
                            "autoCheck": False,
                            "separateLines": False,
                            "acceptSpellingErrors": True
                        },
                        "scoreBarLabel": "Vous avez obtenu :num sur :total points",
                        "a11yCheck": "Vérifier les réponses",
                        "a11yShowSolution": "Afficher la solution",
                        "a11yRetry": "Recommencer"
                    },
                    "library": "H5P.Blanks 1.14",
                    "metadata": {
                        "contentType": "Fill in the Blanks",
                        "license": "U",
                        "title": q.get('name', f'Question {i+1}')
                    },
                    "subContentId": f"bl-{i+1}-{abs(hash(q.get('text', ''))) % 10000:04d}"
                })

            elif q_type == 'dragwords':
                h5p_questions.append({
                    "params": {
                        "media": {"disableImageZooming": False},
                        "taskDescription": "<p>Glissez les mots dans les emplacements.</p>",
                        "textField": escape_html_preserve_math(question_text),
                        "overallFeedback": [
                            {"from": 0, "to": 100, "feedback": ""}
                        ],
                        "checkAnswer": "Vérifier",
                        "submitAnswer": "Soumettre",
                        "tryAgain": "Réessayer",
                        "showSolution": "Voir la solution",
                        "dropZoneIndex": "Zone @index.",
                        "empty": "Zone @index vide.",
                        "contains": "Zone @index contient @draggable.",
                        "ariaDraggableIndex": "@index sur @count.",
                        "tipLabel": "Indice",
                        "correctText": "Correct !",
                        "incorrectText": "Incorrect",
                        "resetDropTitle": "Réinitialiser",
                        "grabbed": "Saisi.",
                        "cancelledDragging": "Annulé.",
                        "correctAnswer": "Bonne réponse",
                        "wrongAnswer": "Mauvaise réponse",
                        "feedbackHeader": "Résultat",
                        "scoreBarLabel": "Score : :num sur :total",
                        "a11yCheck": "Vérifier",
                        "a11yShowSolution": "Solution",
                        "a11yRetry": "Recommencer",
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
                        "title": q.get('name', f'Question {i+1}')
                    },
                    "subContentId": f"dw-{i+1}-{abs(hash(q.get('text', ''))) % 10000:04d}"
                })

        content = {
            "introPage": {
                "showIntroPage": bool(intro_text),
                "startButtonText": "Commencer le quiz",
                "title": title,
                "introduction": f"<p>{escape_html_preserve_math(intro_text)}</p>" if intro_text else ""
            },
            "progressType": "dots",
            "passPercentage": pass_percentage,
            "disableBackwardsNavigation": False,
            "randomQuestions": randomize,
            "endGame": {
                "showResultPage": True,
                "showSolutionButton": True,
                "showRetryButton": True,
                "noResultMessage": "Quiz terminé",
                "message": "Votre résultat :",
                "scoreBarLabel": "Vous avez obtenu @score sur @total points",
                "overallFeedback": [
                    {"from": 0, "to": 50, "feedback": "Révisez davantage."},
                    {"from": 51, "to": 75, "feedback": "Pas mal !"},
                    {"from": 76, "to": 100, "feedback": "Excellent !"}
                ],
                "solutionButtonText": "Voir les solutions",
                "retryButtonText": "Recommencer",
                "finishButtonText": "Terminer",
                "submitButtonText": "Soumettre",
                "showAnimations": False,
                "skippable": False
            },
            "override": {
                "checkButton": True,
                "showSolutionButton": "on",
                "retryButton": "on"
            },
            "texts": {
                "prevButton": "Précédent",
                "nextButton": "Suivant",
                "finishButton": "Terminer",
                "submitButton": "Soumettre",
                "textualProgress": "Question @current sur @total",
                "questionLabel": "Question",
                "readSpeakerProgress": "Question @current sur @total",
                "unansweredText": "Non répondu",
                "answeredText": "Répondu",
                "currentQuestionText": "Question actuelle",
                "navigationLabel": "Questions"
            },
            "questions": h5p_questions
        }

        # Dépendances selon les types utilisés
        dependencies = [
            {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
            {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
            {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
            {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
            {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
            {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5}
        ]

        types_used = set(q.get('type', 'multichoice') for q in questions)

        if 'multichoice' in types_used:
            dependencies.append({"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16})
        if 'truefalse' in types_used:
            dependencies.append({"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8})
        if 'blanks' in types_used:
            dependencies.extend([
                {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
                {"machineName": "H5P.TextUtilities", "majorVersion": 1, "minorVersion": 3}
            ])
        if 'dragwords' in types_used:
            dependencies.extend([
                {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10},
                {"machineName": "H5P.TextUtilities", "majorVersion": 1, "minorVersion": 3}
            ])

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.QuestionSet",
            "embedTypes": ["iframe"],
            "license": "CC BY-SA",
            "licenseVersion": "4.0",
            "defaultLanguage": "fr",
            "authors": [{"name": author, "role": "Author"}],
            "preloadedDependencies": dependencies
        }

        return cls._create_h5p_package(h5p_json, content, title, {
            "authors": [{"name": author, "role": "Author"}]
        })

    # =========================================================================
    # SINGLE CHOICE SET (Quiz rapide) - CORRIGÉ
    # =========================================================================
    @classmethod
    def create_single_choice_set(cls, title: str, questions: List[Dict],
                                  author: str = "ROMAIN DESCHAMPS") -> bytes:
        """
        Crée un Single Choice Set H5P (quiz rapide avec feedback immédiat).
        La première option est TOUJOURS la bonne réponse.
        """

        choices = []
        for q in questions:
            answers = []
            for opt in q.get('options', []):
                answers.append(f"<div>{escape_html_preserve_math(opt)}</div>")

            choices.append({
                "question": f"<p>{escape_html_preserve_math(q.get('text', ''))}</p>",
                "answers": answers
            })

        content = {
            "choices": choices,
            "overallFeedback": [
                {"from": 0, "to": 50, "feedback": "Révisez davantage !"},
                {"from": 51, "to": 75, "feedback": "Pas mal !"},
                {"from": 76, "to": 100, "feedback": "Excellent !"}
            ],
            "behaviour": {
                "autoContinue": True,
                "timeoutCorrect": 2000,
                "timeoutWrong": 3000,
                "soundEffectsEnabled": False,
                "enableRetry": True,
                "enableSolutionsButton": True,
                "passPercentage": 50
            },
            "l10n": {
                "nextButtonLabel": "Question suivante",
                "showSolutionButtonLabel": "Voir la solution",
                "retryButtonLabel": "Recommencer",
                "solutionViewTitle": "Solution",
                "correctText": "Correct !",
                "incorrectText": "Incorrect",
                "muteButtonLabel": "Son",
                "closeButtonLabel": "Fermer",
                "slideOfTotal": "Question :num sur :total",
                "scoreBarLabel": "Vous avez obtenu :num sur :total points",
                "solutionListQuestionNumber": "Question :num",
                "a11yShowSolution": "Afficher la solution",
                "a11yRetry": "Recommencer"
            }
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.SingleChoiceSet",
            "embedTypes": ["iframe"],
            "license": "CC BY-SA",
            "licenseVersion": "4.0",
            "defaultLanguage": "fr",
            "authors": [{"name": author, "role": "Author"}],
            "preloadedDependencies": [
                {"machineName": "H5P.SingleChoiceSet", "majorVersion": 1, "minorVersion": 11},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.SoundJS", "majorVersion": 1, "minorVersion": 0}
            ]
        }

        return cls._create_h5p_package(h5p_json, content, title, {
            "authors": [{"name": author, "role": "Author"}]
        })


if __name__ == "__main__":
    print("Test du générateur H5P v2...")

    # Test Fill in the Blanks
    blanks = H5PGeneratorV2.create_fill_in_blanks(
        title="Test - Texte à trous",
        questions=[
            "Une suite numérique est une fonction définie sur *N* à valeurs dans *R*.",
            "Le nombre \\(u_n\\) est appelé le *terme général* de la suite."
        ],
        task_description="Complétez avec les mots appropriés."
    )
    with open("test_blanks.h5p", "wb") as f:
        f.write(blanks)
    print(f"test_blanks.h5p créé ({len(blanks)} bytes)")

    # Test Drag Words
    drag = H5PGeneratorV2.create_drag_words(
        title="Test - Mots à glisser",
        text_field="Le nombre \\(u_n\\) est le *terme* *général* de la suite. Une suite est *croissante* si chaque terme est supérieur au précédent.",
        task_description="Placez les mots dans les bons emplacements."
    )
    with open("test_drag.h5p", "wb") as f:
        f.write(drag)
    print(f"test_drag.h5p créé ({len(drag)} bytes)")

    # Test Question Set mixte
    mixed = H5PGeneratorV2.create_question_set(
        title="Test - Quiz mixte",
        questions=[
            {
                "type": "multichoice",
                "name": "QCM LaTeX",
                "text": "Que vaut \\(u_0\\) si \\(u_n = 2n + 1\\) ?",
                "options": ["1", "2", "3", "0"],
                "correct_index": 0,
                "feedback": "\\(u_0 = 2 \\times 0 + 1 = 1\\)"
            },
            {
                "type": "truefalse",
                "name": "Vrai/Faux",
                "text": "La représentation graphique d'une suite est un nuage de points.",
                "correct": True,
                "feedback_correct": "Oui, car \\(\\mathbb{N}\\) est discret.",
                "feedback_incorrect": "Si, c'est bien un nuage de points !"
            },
            {
                "type": "blanks",
                "name": "Texte à trous",
                "text": "Une suite définie par *récurrence* nécessite un *premier terme*."
            }
        ],
        intro_text="Quiz de test avec différents types de questions."
    )
    with open("test_mixed.h5p", "wb") as f:
        f.write(mixed)
    print(f"test_mixed.h5p créé ({len(mixed)} bytes)")

    print("Tests terminés !")
