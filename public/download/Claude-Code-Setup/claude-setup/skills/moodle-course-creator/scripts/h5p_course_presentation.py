#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur H5P Course Presentation - Parcours gamifies

Permet de creer des diaporamas interactifs avec quiz integres.
Ideal pour les parcours gamifies avec progression.

Usage pedagogique:
- Parcours type "escalade" avec defis
- Capsules interactives autonomes
- Cours avec quiz integres
"""

import json
import zipfile
import io
import re
from typing import List, Dict, Optional
from pathlib import Path
import html


def format_latex_for_h5p(text: str) -> str:
    """
    Formate le texte avec LaTeX pour H5P/MathJax.

    Accepte:
    - \\(formule\\) : inline
    - \\[formule\\] : block
    - $formule$ : converti en inline
    - $$formule$$ : converti en block

    Le JSON H5P necessite des doubles backslashes.
    """
    if not text:
        return ""

    result = str(text)

    # Convertir notations $ en notations \
    result = re.sub(r'\$\$(.*?)\$\$', r'\\[\1\\]', result, flags=re.DOTALL)
    result = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', r'\\(\1\\)', result)

    return result


class H5PCoursePresentation:
    """Generateur de Course Presentation H5P"""

    @classmethod
    def create_gamified_course(cls,
                                title: str,
                                background_image: str,
                                stages: List[Dict],
                                author: str = "ROMAIN DESCHAMPS") -> bytes:
        """
        Cree un parcours gamifie avec Course Presentation.

        Args:
            title: Titre du parcours
            background_image: Chemin vers l'image de fond (ex: echelle)
            stages: Liste des etapes avec quiz:
                [
                    {
                        "title": "Etape 1",
                        "intro": "Texte d'introduction",
                        "quiz_type": "multichoice",  # ou "blanks", "dragwords", "truefalse"
                        "question": "Question avec \\\\(LaTeX\\\\)",
                        "options": ["Option 1", "Option 2"],  # pour multichoice
                        "correct": 0,  # index pour multichoice, True/False pour truefalse
                        "feedback": "Explication"
                    }
                ]
            author: Auteur

        Returns:
            Contenu du fichier .h5p
        """

        slides = []
        images = {}

        # Charger l'image de fond
        bg_image_name = "background.png"
        bg_image_data = None
        if Path(background_image).exists():
            with open(background_image, 'rb') as f:
                bg_image_data = f.read()
            ext = Path(background_image).suffix.lower()
            bg_image_name = f"background{ext}"

        # Slide de titre
        slides.append({
            "elements": [
                {
                    "x": 0, "y": 0, "width": 100, "height": 100,
                    "action": {
                        "library": "H5P.Image 1.1",
                        "params": {
                            "contentName": "Image",
                            "file": {"path": f"images/{bg_image_name}", "mime": "image/png"},
                            "alt": "Background"
                        }
                    },
                    "backgroundOpacity": 100
                },
                {
                    "x": 10, "y": 30, "width": 80, "height": 20,
                    "action": {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {
                            "text": f"<h1 style='text-align:center; background:rgba(255,255,255,0.9); padding:20px; border-radius:10px;'>{title}</h1>"
                        }
                    }
                },
                {
                    "x": 30, "y": 60, "width": 40, "height": 15,
                    "action": {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {
                            "text": "<p style='text-align:center; background:#4CAF50; color:white; padding:15px; border-radius:8px; font-size:1.2em;'>Commencer le parcours !</p>"
                        }
                    },
                    "goToSlide": 2
                }
            ],
            "keywords": [{"main": "Accueil"}]
        })

        # Slides pour chaque etape
        for i, stage in enumerate(stages):
            quiz_type = stage.get("quiz_type", "multichoice")
            question = format_latex_for_h5p(stage.get("question", ""))
            feedback = format_latex_for_h5p(stage.get("feedback", ""))

            # Slide d'introduction de l'etape
            intro_slide = {
                "elements": [
                    {
                        "x": 0, "y": 0, "width": 100, "height": 100,
                        "action": {
                            "library": "H5P.Image 1.1",
                            "params": {
                                "file": {"path": f"images/{bg_image_name}", "mime": "image/png"},
                                "alt": "Background"
                            }
                        },
                        "backgroundOpacity": 50
                    },
                    {
                        "x": 5, "y": 5, "width": 90, "height": 15,
                        "action": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {
                                "text": f"<h2 style='background:rgba(255,255,255,0.95); padding:15px; border-radius:8px; text-align:center;'>Etape {i+1} : {stage.get('title', '')}</h2>"
                            }
                        }
                    },
                    {
                        "x": 5, "y": 25, "width": 90, "height": 20,
                        "action": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {
                                "text": f"<p style='background:rgba(255,255,255,0.95); padding:15px; border-radius:8px;'>{format_latex_for_h5p(stage.get('intro', ''))}</p>"
                            }
                        }
                    }
                ],
                "keywords": [{"main": f"Etape {i+1}"}]
            }

            # Ajouter le quiz selon le type
            quiz_element = cls._create_quiz_element(quiz_type, stage, question, feedback)
            quiz_element["x"] = 5
            quiz_element["y"] = 50
            quiz_element["width"] = 90
            quiz_element["height"] = 45
            intro_slide["elements"].append(quiz_element)

            slides.append(intro_slide)

        # Slide finale (victoire)
        slides.append({
            "elements": [
                {
                    "x": 0, "y": 0, "width": 100, "height": 100,
                    "action": {
                        "library": "H5P.Image 1.1",
                        "params": {
                            "file": {"path": f"images/{bg_image_name}", "mime": "image/png"},
                            "alt": "Background"
                        }
                    },
                    "backgroundOpacity": 30
                },
                {
                    "x": 10, "y": 20, "width": 80, "height": 30,
                    "action": {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {
                            "text": "<h1 style='text-align:center; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; padding:30px; border-radius:15px;'>Felicitations !</h1>"
                        }
                    }
                },
                {
                    "x": 15, "y": 55, "width": 70, "height": 20,
                    "action": {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {
                            "text": "<p style='text-align:center; background:rgba(255,255,255,0.95); padding:20px; border-radius:10px; font-size:1.1em;'>Tu as termine le parcours avec succes !</p>"
                        }
                    }
                }
            ],
            "keywords": [{"main": "Victoire"}]
        })

        # Construire le contenu
        content = {
            "presentation": {
                "slides": slides,
                "keywordListEnabled": True,
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
                "hideKeywords": "Masquer le menu",
                "showKeywords": "Afficher le menu",
                "fullscreen": "Plein ecran",
                "exitFullscreen": "Quitter plein ecran",
                "prevSlide": "Precedent",
                "nextSlide": "Suivant",
                "currentSlide": "Diapositive actuelle",
                "lastSlide": "Derniere diapositive",
                "solutionModeStated": "Mode solution active",
                "solutionModeText": "Mode solution",
                "accessibilitySlideNavigationExplanation": "Utilisez les fleches pour naviguer",
                "accessibilityCanvasLabel": "Zone de presentation",
                "containsNotCompleted": "Contient des activites non terminees",
                "containsCompleted": "Contient des activites terminees",
                "slideCount": "Diapositive @index sur @total",
                "containsOnlyCorrect": "Contient uniquement des reponses correctes",
                "containsIncorrectAnswers": "Contient des reponses incorrectes",
                "shareResult": "Partager le resultat",
                "confirmFinalization": "Confirmer la fin",
                "close": "Fermer"
            },
            "override": {
                "activeSurface": False,
                "hideSummarySlide": False,
                "summarySlideSolutionButton": True,
                "summarySlideRetryButton": True,
                "enablePrintButton": False,
                "social": {}
            }
        }

        # Dependances - versions compatibles avec Moodle 3.x et 4.x
        h5p_json = {
            "title": title,
            "language": "fr",
            "mainLibrary": "H5P.CoursePresentation",
            "embedTypes": ["iframe"],
            "license": "CC BY-SA",
            "licenseVersion": "4.0",
            "defaultLanguage": "fr",
            "authors": [{"name": author, "role": "Author"}],
            "preloadedDependencies": [
                {"machineName": "H5P.CoursePresentation", "majorVersion": 1, "minorVersion": 22},
                {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
                {"machineName": "H5P.Image", "majorVersion": 1, "minorVersion": 1},
                {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 14},
                {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 6},
                {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 12},
                {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 8},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 4}
            ]
        }

        # Creer le package
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('h5p.json', json.dumps(h5p_json, ensure_ascii=False, indent=2))
            zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False, indent=2))

            if bg_image_data:
                zf.writestr(f'content/images/{bg_image_name}', bg_image_data)

        return buffer.getvalue()

    @classmethod
    def _create_quiz_element(cls, quiz_type: str, stage: Dict, question: str, feedback: str) -> Dict:
        """Cree un element quiz selon le type"""

        if quiz_type == "multichoice":
            options = stage.get("options", [])
            correct = stage.get("correct", 0)

            answers = []
            for j, opt in enumerate(options):
                answers.append({
                    "text": f"<div>{format_latex_for_h5p(opt)}</div>",
                    "correct": j == correct,
                    "tpiMapping": None
                })

            return {
                "action": {
                    "library": "H5P.MultiChoice 1.14",
                    "params": {
                        "media": {"disableImageZooming": False},
                        "question": f"<p style='background:rgba(255,255,255,0.95); padding:10px; border-radius:5px;'>{question}</p>",
                        "answers": answers,
                        "overallFeedback": [
                            {"from": 0, "to": 100, "feedback": f"<p>{feedback}</p>" if feedback else ""}
                        ],
                        "behaviour": {
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
                            "submitAnswerButton": "Soumettre",
                            "showSolutionButton": "Solution",
                            "tryAgainButton": "Reessayer",
                            "tipsLabel": "Indice",
                            "scoreBarLabel": "Score: :num/:total",
                            "tipAvailable": "Indice disponible",
                            "feedbackAvailable": "Feedback disponible",
                            "readFeedback": "Lire le feedback",
                            "wrongAnswer": "Incorrect",
                            "correctAnswer": "Correct",
                            "shouldCheck": "Aurait du etre coche",
                            "shouldNotCheck": "N'aurait pas du etre coche",
                            "noInput": "Repondez d'abord",
                            "a11yCheck": "Verifier",
                            "a11yShowSolution": "Solution",
                            "a11yRetry": "Reessayer"
                        }
                    },
                    "metadata": {"contentType": "Multiple Choice", "license": "U"}
                }
            }

        elif quiz_type == "truefalse":
            correct = stage.get("correct", True)

            return {
                "action": {
                    "library": "H5P.TrueFalse 1.6",
                    "params": {
                        "media": {"disableImageZooming": False},
                        "question": f"<p style='background:rgba(255,255,255,0.95); padding:10px; border-radius:5px;'>{question}</p>",
                        "correct": "true" if correct else "false",
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
                            "score": "Score: @score/@total",
                            "checkAnswer": "Verifier",
                            "showSolutionButton": "Solution",
                            "tryAgain": "Reessayer",
                            "wrongAnswerMessage": feedback if not correct else "Incorrect",
                            "correctAnswerMessage": feedback if correct else "Correct !",
                            "scoreBarLabel": "Score: :num/:total"
                        }
                    },
                    "metadata": {"contentType": "True/False Question", "license": "U"}
                }
            }

        elif quiz_type == "blanks":
            text = stage.get("text", question)

            return {
                "action": {
                    "library": "H5P.Blanks 1.12",
                    "params": {
                        "media": {"disableImageZooming": False},
                        "taskDescription": f"<p style='background:rgba(255,255,255,0.95); padding:10px; border-radius:5px;'>Completez les trous :</p>",
                        "questions": [f"<p style='background:rgba(255,255,255,0.95); padding:10px; border-radius:5px;'>{format_latex_for_h5p(text)}</p>"],
                        "overallFeedback": [
                            {"from": 0, "to": 100, "feedback": feedback if feedback else ""}
                        ],
                        "showSolutions": "Solution",
                        "tryAgain": "Reessayer",
                        "checkAnswer": "Verifier",
                        "submitAnswer": "Soumettre",
                        "notFilledOut": "Remplissez tous les trous",
                        "answerIsCorrect": "Correct !",
                        "answerIsWrong": "Incorrect",
                        "answeredCorrectly": "Bien !",
                        "answeredIncorrectly": "Erreur",
                        "solutionLabel": "Solution:",
                        "inputLabel": "Trou @num/@total",
                        "behaviour": {
                            "enableRetry": True,
                            "enableSolutionsButton": True,
                            "enableCheckButton": True,
                            "caseSensitive": False,
                            "showSolutionsRequiresInput": True,
                            "autoCheck": False,
                            "separateLines": False,
                            "acceptSpellingErrors": True
                        }
                    },
                    "metadata": {"contentType": "Fill in the Blanks", "license": "U"}
                }
            }

        elif quiz_type == "dragwords":
            text = stage.get("text", question)

            return {
                "action": {
                    "library": "H5P.DragText 1.8",
                    "params": {
                        "media": {"disableImageZooming": False},
                        "taskDescription": f"<p style='background:rgba(255,255,255,0.95); padding:10px; border-radius:5px;'>Glissez les mots :</p>",
                        "textField": format_latex_for_h5p(text),
                        "overallFeedback": [
                            {"from": 0, "to": 100, "feedback": feedback if feedback else ""}
                        ],
                        "checkAnswer": "Verifier",
                        "submitAnswer": "Soumettre",
                        "tryAgain": "Reessayer",
                        "showSolution": "Solution",
                        "dropZoneIndex": "Zone @index",
                        "empty": "Zone @index vide",
                        "contains": "Zone @index: @draggable",
                        "ariaDraggableIndex": "@index/@count",
                        "tipLabel": "Indice",
                        "correctText": "Correct !",
                        "incorrectText": "Incorrect",
                        "behaviour": {
                            "enableRetry": True,
                            "enableSolutionsButton": True,
                            "enableCheckButton": True,
                            "instantFeedback": False
                        }
                    },
                    "metadata": {"contentType": "Drag the Words", "license": "U"}
                }
            }

        # Default: multichoice vide
        return {
            "action": {
                "library": "H5P.AdvancedText 1.1",
                "params": {"text": f"<p>{question}</p>"}
            }
        }


if __name__ == "__main__":
    print("Module H5P Course Presentation charge.")
    print("Utilisez H5PCoursePresentation.create_gamified_course() pour creer un parcours.")
