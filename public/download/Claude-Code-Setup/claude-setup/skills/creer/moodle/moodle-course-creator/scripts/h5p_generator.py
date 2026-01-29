#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur de fichiers H5P basiques.
Permet de creer des fichiers .h5p pour les types de contenu courants.

Types supportes:
- Question Set (quiz avec plusieurs questions)
- Single Choice Set
- Multiple Choice
"""

import json
import zipfile
import io
from typing import List, Dict, Optional
import html


def escape_html(text: str) -> str:
    """Echappe le texte pour HTML"""
    return html.escape(str(text)) if text else ""


class H5PGenerator:
    """Generateur de fichiers H5P"""

    # Versions des bibliotheques H5P (doivent correspondre aux versions Moodle)
    LIBRARY_VERSIONS = {
        'H5P.QuestionSet': {'majorVersion': 1, 'minorVersion': 20},
        'H5P.MultiChoice': {'majorVersion': 1, 'minorVersion': 16},
        'H5P.SingleChoiceSet': {'majorVersion': 1, 'minorVersion': 11},
        'H5P.TrueFalse': {'majorVersion': 1, 'minorVersion': 8},
    }

    @classmethod
    def create_multichoice_h5p(cls, title: str, questions: List[Dict]) -> bytes:
        """
        Cree un fichier H5P de type Question Set avec questions a choix multiples.

        Args:
            title: Titre du quiz
            questions: Liste de questions avec format:
                {
                    "text": "Question text",
                    "options": ["Option A", "Option B", ...],
                    "correct_index": 0,  # ou liste pour choix multiples
                    "feedback_correct": "Bravo!",
                    "feedback_incorrect": "Essayez encore"
                }

        Returns:
            Contenu du fichier .h5p (bytes)
        """
        # Construire les questions H5P
        h5p_questions = []
        for i, q in enumerate(questions):
            answers = []
            correct_indices = q.get('correct_index', 0)
            if isinstance(correct_indices, int):
                correct_indices = [correct_indices]

            for j, opt in enumerate(q.get('options', [])):
                answers.append({
                    "text": f"<p>{escape_html(opt)}</p>",
                    "correct": j in correct_indices,
                    "tpiMapping": "undefined"
                })

            h5p_questions.append({
                "params": {
                    "media": {"disableImageZooming": False},
                    "question": f"<p>{escape_html(q.get('text', ''))}</p>",
                    "answers": answers,
                    "overallFeedback": [
                        {"from": 0, "to": 100, "feedback": ""}
                    ],
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
                        "textHolder": "...",
                        "correctAnswer": "Bonne reponse !",
                        "wrongAnswer": "Mauvaise reponse",
                        "noInput": "Veuillez repondre",
                        "scoreBarLabel": "Score"
                    },
                    "confirmCheck": {"header": "", "body": "", "cancelLabel": "", "confirmLabel": ""},
                    "confirmRetry": {"header": "", "body": "", "cancelLabel": "", "confirmLabel": ""}
                },
                "library": "H5P.MultiChoice 1.16",
                "metadata": {"contentType": "Multiple Choice", "license": "U", "title": q.get('name', f'Question {i+1}')}
            })

        # Contenu principal
        content = {
            "introPage": {
                "showIntroPage": True,
                "title": title,
                "introduction": f"<p>Quiz : {escape_html(title)}</p>",
                "startButtonText": "Commencer"
            },
            "progressType": "dots",
            "passPercentage": 50,
            "disableBackwardsNavigation": False,
            "randomQuestions": False,
            "endGame": {
                "showResultPage": True,
                "showSolutionButton": True,
                "showRetryButton": True,
                "noResultMessage": "Quiz termine",
                "message": "Votre score : @score sur @total",
                "overallFeedback": [
                    {"from": 0, "to": 49, "feedback": "Il faut reviser !"},
                    {"from": 50, "to": 79, "feedback": "Pas mal !"},
                    {"from": 80, "to": 100, "feedback": "Excellent !"}
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

        # Metadata H5P
        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.QuestionSet",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5},
                {"machineName": "H5P.Video", "majorVersion": 1, "minorVersion": 6}
            ]
        }

        # Creer le fichier ZIP (.h5p)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
            zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False, indent=2))

        return buffer.getvalue()

    @classmethod
    def create_single_choice_set_h5p(cls, title: str, questions: List[Dict]) -> bytes:
        """
        Cree un fichier H5P de type Single Choice Set (plus simple, feedback immediat).

        Args:
            title: Titre du quiz
            questions: Liste de questions avec format:
                {
                    "text": "Question text",
                    "options": ["Option A (correcte)", "Option B", ...],
                    "correct_index": 0
                }

        Returns:
            Contenu du fichier .h5p (bytes)
        """
        choices = []
        for q in questions:
            answers = []
            for j, opt in enumerate(q.get('options', [])):
                answers.append(f"<p>{escape_html(opt)}</p>")

            # Reorganiser pour que la bonne reponse soit en premier (format SingleChoiceSet)
            correct_idx = q.get('correct_index', 0)
            if correct_idx > 0 and correct_idx < len(answers):
                # Deplacer la bonne reponse en premiere position
                correct_answer = answers[correct_idx]
                answers.pop(correct_idx)
                answers.insert(0, correct_answer)

            choices.append({
                "question": f"<p>{escape_html(q.get('text', ''))}</p>",
                "answers": answers
            })

        content = {
            "choices": choices,
            "overallFeedback": [
                {"from": 0, "to": 49, "feedback": "Il faut reviser !"},
                {"from": 50, "to": 79, "feedback": "Pas mal !"},
                {"from": 80, "to": 100, "feedback": "Excellent !"}
            ],
            "behaviour": {
                "autoContinue": True,
                "timeoutCorrect": 2000,
                "timeoutWrong": 3000,
                "soundEffectsEnabled": True,
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
                "incorrectText": "Incorrect !",
                "muteButtonLabel": "Couper le son",
                "closeButtonLabel": "Fermer",
                "slideOfTotal": "Question :num sur :total",
                "scoreBarLabel": "Score",
                "solutionListQuestionNumber": "Question :num",
                "a11yShowSolution": "Afficher la solution",
                "a11yRetry": "Recommencer le quiz"
            }
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.SingleChoiceSet",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.SingleChoiceSet", "majorVersion": 1, "minorVersion": 11},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.SoundJS", "majorVersion": 1, "minorVersion": 0}
            ]
        }

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
            zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False, indent=2))

        return buffer.getvalue()

    @classmethod
    def create_true_false_h5p(cls, title: str, statement: str, correct_answer: bool,
                              feedback_correct: str = "Correct !",
                              feedback_incorrect: str = "Incorrect !") -> bytes:
        """
        Cree un fichier H5P de type True/False.

        Args:
            title: Titre
            statement: L'affirmation a evaluer
            correct_answer: True si l'affirmation est vraie
            feedback_correct: Feedback si bonne reponse
            feedback_incorrect: Feedback si mauvaise reponse

        Returns:
            Contenu du fichier .h5p (bytes)
        """
        content = {
            "media": {"disableImageZooming": False},
            "question": f"<p>{escape_html(statement)}</p>",
            "correct": "true" if correct_answer else "false",
            "l10n": {
                "trueText": "Vrai",
                "falseText": "Faux",
                "checkAnswer": "Verifier",
                "showSolutionButton": "Voir la solution",
                "tryAgain": "Reessayer",
                "correctAnswerMessage": feedback_correct,
                "wrongAnswerMessage": feedback_incorrect,
                "scoreBarLabel": "Score"
            },
            "behaviour": {
                "enableRetry": True,
                "enableSolutionsButton": True,
                "enableCheckButton": True,
                "confirmCheckDialog": False,
                "confirmRetryDialog": False,
                "autoCheck": False
            },
            "confirmCheck": {"header": "", "body": "", "cancelLabel": "", "confirmLabel": ""},
            "confirmRetry": {"header": "", "body": "", "cancelLabel": "", "confirmLabel": ""}
        }

        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.TrueFalse",
            "embedTypes": ["div"],
            "license": "U",
            "preloadedDependencies": [
                {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
                {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5},
                {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0}
            ]
        }

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
            zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False, indent=2))

        return buffer.getvalue()


def convert_quiz_to_h5p(quiz_questions: List[Dict], title: str, h5p_type: str = "questionset") -> bytes:
    """
    Convertit des questions au format du generateur Moodle vers H5P.

    Args:
        quiz_questions: Questions au format:
            {
                "type": "multichoice",
                "name": "Q1",
                "text": "Question text {#1}",
                "options": ["A", "B", "C"],
                "correct_index": 1,
                "feedbacks": ["...", "...", "..."],
                "general_feedback": "..."
            }
        title: Titre du quiz H5P
        h5p_type: "questionset" ou "singlechoiceset"

    Returns:
        Contenu du fichier .h5p
    """
    h5p_questions = []

    for q in quiz_questions:
        if q.get('type') in ['multichoice', 'shortanswer']:
            # Nettoyer le texte (retirer {#1})
            text = q.get('text', '').replace('{#1}', '______')

            h5p_questions.append({
                'text': text,
                'options': q.get('options', []),
                'correct_index': q.get('correct_index', 0),
                'name': q.get('name', '')
            })

    if h5p_type == "singlechoiceset":
        return H5PGenerator.create_single_choice_set_h5p(title, h5p_questions)
    else:
        return H5PGenerator.create_multichoice_h5p(title, h5p_questions)


if __name__ == "__main__":
    # Test
    questions = [
        {
            "text": "Quelle est la capitale de la France ?",
            "options": ["Paris", "Lyon", "Marseille", "Bordeaux"],
            "correct_index": 0,
            "name": "Q1 - Capitale"
        },
        {
            "text": "2 + 2 = ?",
            "options": ["3", "4", "5", "6"],
            "correct_index": 1,
            "name": "Q2 - Calcul"
        }
    ]

    h5p_content = H5PGenerator.create_multichoice_h5p("Quiz Test", questions)
    with open("test_quiz.h5p", "wb") as f:
        f.write(h5p_content)
    print("Fichier test_quiz.h5p genere avec succes!")
