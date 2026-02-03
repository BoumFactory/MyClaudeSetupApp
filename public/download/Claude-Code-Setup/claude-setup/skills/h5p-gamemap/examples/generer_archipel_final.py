#!/usr/bin/env python3
"""
L'Archipel des Suites - Game Map H5P - VERSION FINALE AUX PETITS OIGNONS
Parcours gamifie sur les suites numeriques (Premiere)

- 4 vies (chaque erreur retire une vie)
- Doit reussir pour avancer (roaming: complete)
- Types varies : MultiChoice, DragText, Blanks, TrueFalse
- Interface 100% francais avec feedbacks pro
- Couleurs personnalisees style aventure
"""
import json, zipfile, io, uuid, random
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

with open(OUTPUT_DIR / 'archipel_suites.png', 'rb') as f:
    image_data = f.read()

# ============================================================================
# CONFIGURATION DU JEU
# ============================================================================
CONFIG = {
    'lives': 4,                    # Nombre de vies
    'roaming': 'complete',         # Doit reussir pour avancer (complete/free/strict)
    'fog': 'visited',              # Brouillard sur les iles non visitees
    'showLabels': True,            # Afficher les noms des iles
    'showScoreStars': 'always',    # Afficher les etoiles (always/visited/never)
    'displayPaths': True,          # Afficher les chemins entre iles
    'useAnimation': True,          # Animations
}

# Couleurs style aventure/tresor
COLORS = {
    'stageUnvisited': 'rgba(52, 152, 219, 0.85)',    # Bleu ocean
    'stageLocked': 'rgba(127, 140, 141, 0.7)',       # Gris brume
    'stageCleared': 'rgba(46, 204, 113, 0.85)',      # Vert victoire
    'pathNormal': 'rgba(44, 62, 80, 0.6)',           # Sombre
    'pathCleared': 'rgba(46, 204, 113, 0.7)',        # Vert
}

# ============================================================================
# POSITIONS DES ILES (calibrees sur l'image archipel_suites.png)
# ============================================================================
# Ile 1: bas-gauche (palmiers)    | Ile 2: centre-gauche (rocher)
# Ile 3: bas-centre (croissant)   | Ile 4: centre (volcan)
# Ile 5: haut-centre (foret)      | Ile 6: haut-droite (montagnes)
# Ile 7: droite (tresor X)

etapes = [
    {
        'title': "Ile de la Definition",
        'x': 12, 'y': 72,
        'type': 'multichoice',
        'question': r"Une suite numerique est une fonction definie sur :",
        'answers': [
            {'text': r"\(\mathbb{N} \to \mathbb{R}\) (entiers naturels vers reels)", 'correct': True,
             'feedback': r"Bravo ! Une suite associe a chaque entier naturel \(n \in \mathbb{N}\) un nombre reel \(u_n \in \mathbb{R}\)."},
            {'text': r"\(\mathbb{R} \to \mathbb{N}\)", 'correct': False,
             'feedback': r"Non, c'est l'inverse ! Une suite part de \(\mathbb{N}\), pas de \(\mathbb{R}\)."},
            {'text': r"\(\mathbb{Z} \to \mathbb{R}\)", 'correct': False,
             'feedback': r"Attention, \(\mathbb{Z}\) inclut les entiers negatifs. Une suite classique part de \(\mathbb{N}\)."},
            {'text': r"\(\mathbb{R} \to \mathbb{R}\)", 'correct': False,
             'feedback': "Non, ce serait une fonction quelconque, pas une suite."}
        ],
        'tip': r"Rappel : \(\mathbb{N} = \{0, 1, 2, ...\}\) et \(\mathbb{R}\) = nombres reels"
    },
    {
        'title': "Ile des Notations",
        'x': 23, 'y': 45,
        'type': 'dragtext',
        'description': r"Place les termes au bon endroit. Notation : \((u_n)\) = suite entiere, \(u_n\) = un terme.",
        'text': r"La notation avec parentheses designe la *suite* entiere, tandis que sans parentheses on designe un *terme* particulier de rang \(n\).",
    },
    {
        'title': "Ile du Vocabulaire",
        'x': 42, 'y': 55,
        'type': 'blanks',
        'description': r"Complete les definitions. Dans \(u_n\), que representent \(n\) et \(u_n\) ?",
        'text': r"Dans \(u_n\), le nombre \(n\) s'appelle le *rang* ou l'*indice*. La valeur \(u_n\) est appelee le *terme* de rang \(n\).",
    },
    {
        'title': "Ile Explicite",
        'x': 52, 'y': 28,
        'type': 'multichoice',
        'question': r"Soit \(u_n = 2n - 7\). Que vaut \(u_5\) ?",
        'answers': [
            {'text': r"\(3\)", 'correct': True,
             'feedback': r"Bravo ! \(u_5 = 2 \times 5 - 7 = 10 - 7 = 3\)"},
            {'text': r"\(10\)", 'correct': False,
             'feedback': r"Tu as calcule \(2 \times 5 = 10\) mais oublie de soustraire 7."},
            {'text': r"\(-3\)", 'correct': False,
             'feedback': "Attention au signe ! Le resultat est positif."},
            {'text': r"\(5\)", 'correct': False,
             'feedback': r"Tu as peut-etre confondu \(n\) et le resultat."}
        ],
        'tip': r"Remplace \(n\) par 5 dans la formule \(u_n = 2n - 7\)"
    },
    {
        'title': "Ile de la Recurrence",
        'x': 64, 'y': 20,
        'type': 'truefalse',
        'question': r"Une suite definie par recurrence necessite de connaitre le terme precedent pour calculer le suivant.",
        'correct': True,
        'feedback_correct': r"Exact ! C'est le principe de la recurrence : \(u_{n+1}\) depend de \(u_n\).",
        'feedback_incorrect': "Si, c'est justement la definition d'une suite recurrente !"
    },
    {
        'title': "Ile du Calcul",
        'x': 75, 'y': 22,
        'type': 'multichoice',
        'question': r"Soit \(u_0 = 1\) et \(u_{n+1} = 3u_n + 1\). Que vaut \(u_2\) ?",
        'answers': [
            {'text': r"\(13\)", 'correct': True,
             'feedback': r"Bravo ! \(u_1 = 3 \times 1 + 1 = 4\), puis \(u_2 = 3 \times 4 + 1 = 13\)."},
            {'text': r"\(4\)", 'correct': False,
             'feedback': r"C'est \(u_1\) ! Il faut continuer pour trouver \(u_2\)."},
            {'text': r"\(7\)", 'correct': False,
             'feedback': "Verifie ton calcul etape par etape."},
            {'text': r"\(10\)", 'correct': False,
             'feedback': r"Attention, \(u_{n+1} = 3u_n + 1\), n'oublie pas le +1."}
        ],
        'tip': r"Calcule d'abord \(u_1 = 3u_0 + 1\), puis \(u_2 = 3u_1 + 1\)."
    },
    {
        'title': "Ile du Tresor",
        'x': 80, 'y': 42,
        'type': 'dragtext',
        'description': r"Derniere epreuve ! La representation graphique d'une suite \((u_n)\) est-elle une courbe ?",
        'text': r"La representation graphique d'une suite est un *nuage* de *points* discrets et non une courbe continue, car une suite n'est definie que sur \(\mathbb{N}\).",
    }
]

# ============================================================================
# GENERATEURS DE CONTENUS H5P - 100% FRANCAIS
# ============================================================================

def make_multichoice(etape):
    answers = []
    for ans in etape['answers']:
        answers.append({
            'correct': ans['correct'],
            'tipsAndFeedback': {
                'tip': '',
                'chosenFeedback': f"<div>{ans['feedback']}</div>",
                'notChosenFeedback': ''
            },
            'text': f"<div>{ans['text']}</div>\n"
        })
    random.shuffle(answers)

    return {
        'contentType': {
            'params': {
                'media': {'disableImageZooming': False},
                'answers': answers,
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage ! Tu perds une vie. Relis bien la question."},
                    {'from': 1, 'to': 99, 'feedback': "Presque ! Reflechis encore."},
                    {'from': 100, 'to': 100, 'feedback': "Parfait ! Tu peux avancer vers l'ile suivante."}
                ],
                'behaviour': {
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'enableCheckButton': True,
                    'type': 'auto',
                    'singlePoint': False,
                    'randomAnswers': False,
                    'showSolutionsRequiresInput': True,
                    'confirmCheckDialog': False,
                    'confirmRetryDialog': False,
                    'autoCheck': False,
                    'passPercentage': 100,
                    'showScorePoints': True
                },
                'UI': {
                    'checkAnswerButton': 'Verifier',
                    'submitAnswerButton': 'Soumettre',
                    'showSolutionButton': 'Voir la solution',
                    'tryAgainButton': 'Reessayer',
                    'tipsLabel': 'Indice',
                    'scoreBarLabel': 'Score : :num sur :total',
                    'tipAvailable': 'Indice disponible',
                    'feedbackAvailable': 'Explication disponible',
                    'readFeedback': "Lire l'explication",
                    'wrongAnswer': 'Incorrect',
                    'correctAnswer': 'Correct !',
                    'shouldCheck': 'A cocher',
                    'shouldNotCheck': 'A ne pas cocher',
                    'noInput': 'Reponds avant de voir la solution',
                    'a11yCheck': 'Verifier les reponses.',
                    'a11yShowSolution': 'Afficher la solution.',
                    'a11yRetry': 'Recommencer.'
                },
                'confirmCheck': {
                    'header': 'Valider ?',
                    'body': 'Es-tu sur de ta reponse ?',
                    'cancelLabel': 'Annuler',
                    'confirmLabel': 'Valider'
                },
                'confirmRetry': {
                    'header': 'Reessayer ?',
                    'body': 'Tu vas recommencer cette question.',
                    'cancelLabel': 'Annuler',
                    'confirmLabel': 'Reessayer'
                },
                'question': f"<p><strong>{etape['title']}</strong></p>\n<p>{etape['question']}</p>\n" +
                           (f"<p><em>Indice : {etape.get('tip', '')}</em></p>" if etape.get('tip') else "")
            },
            'library': 'H5P.MultiChoice 1.16',
            'metadata': {'contentType': 'Multiple Choice', 'license': 'U', 'title': etape['title']},
            'subContentId': str(uuid.uuid4())
        }
    }

def make_dragtext(etape):
    return {
        'contentType': {
            'params': {
                'media': {'disableImageZooming': False},
                'taskDescription': f"<p><strong>{etape['title']}</strong></p>\n<p>{etape['description']}</p>\n",
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage ! Tu perds une vie. Reessaie !"},
                    {'from': 1, 'to': 99, 'feedback': "Presque ! Verifie les derniers mots."},
                    {'from': 100, 'to': 100, 'feedback': "Parfait ! Direction l'ile suivante !"}
                ],
                'checkAnswer': 'Verifier',
                'submitAnswer': 'Soumettre',
                'tryAgain': 'Reessayer',
                'showSolution': 'Voir la solution',
                'dropZoneIndex': 'Zone @index.',
                'empty': 'Zone @index vide.',
                'contains': 'Zone @index contient @draggable.',
                'ariaDraggableIndex': '@index sur @count.',
                'tipLabel': 'Indice',
                'correctText': 'Correct !',
                'incorrectText': 'Incorrect',
                'resetDropTitle': 'Reinitialiser',
                'resetDropDescription': 'Reinitialiser cette zone ?',
                'grabbed': 'Element selectionne.',
                'cancelledDragging': 'Annule.',
                'correctAnswer': 'Reponse correcte :',
                'feedbackHeader': 'Resultat',
                'behaviour': {
                    'enableRetry': True,
                    'enableSolutionsButton': True,
                    'enableCheckButton': True,
                    'instantFeedback': False
                },
                'scoreBarLabel': 'Score : :num sur :total',
                'a11yCheck': 'Verifier.',
                'a11yShowSolution': 'Solution.',
                'a11yRetry': 'Recommencer.',
                'textField': etape['text']
            },
            'library': 'H5P.DragText 1.10',
            'metadata': {'contentType': 'Drag the Words', 'license': 'U', 'title': etape['title']},
            'subContentId': str(uuid.uuid4())
        }
    }

def make_blanks(etape):
    return {
        'contentType': {
            'params': {
                'media': {'disableImageZooming': False},
                'text': f"<p><strong>{etape['title']}</strong></p>\n<p>{etape['description']}</p>\n",
                'overallFeedback': [
                    {'from': 0, 'to': 0, 'feedback': "Dommage ! Tu perds une vie."},
                    {'from': 1, 'to': 99, 'feedback': "Presque parfait !"},
                    {'from': 100, 'to': 100, 'feedback': "Excellent ! Tu maitrises le vocabulaire."}
                ],
                'showSolutions': 'Voir la solution',
                'tryAgain': 'Reessayer',
                'checkAnswer': 'Verifier',
                'submitAnswer': 'Soumettre',
                'notFilledOut': 'Complete tous les champs.',
                'answerIsCorrect': "':ans' est correct !",
                'answerIsWrong': "':ans' est incorrect.",
                'answeredCorrectly': 'Bonne reponse !',
                'answeredIncorrectly': 'Mauvaise reponse.',
                'solutionLabel': 'Reponse :',
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
                    'confirmCheckDialog': False,
                    'confirmRetryDialog': False,
                    'acceptSpellingErrors': True
                },
                'scoreBarLabel': 'Score : :num sur :total',
                'a11yCheck': 'Verifier.',
                'a11yShowSolution': 'Solution.',
                'a11yRetry': 'Recommencer.',
                'a11yCheckingModeHeader': 'Verification',
                'confirmCheck': {'header': 'Valider ?', 'body': 'Sur ?', 'cancelLabel': 'Annuler', 'confirmLabel': 'Valider'},
                'confirmRetry': {'header': 'Reessayer ?', 'body': 'Recommencer.', 'cancelLabel': 'Annuler', 'confirmLabel': 'OK'},
                'questions': [f"<p>{etape['text']}</p>"]
            },
            'library': 'H5P.Blanks 1.14',
            'metadata': {'contentType': 'Fill in the Blanks', 'license': 'U', 'title': etape['title']},
            'subContentId': str(uuid.uuid4())
        }
    }

def make_truefalse(etape):
    return {
        'contentType': {
            'params': {
                'media': {'disableImageZooming': False},
                'correct': 'true' if etape['correct'] else 'false',
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
                    'checkAnswer': 'Verifier',
                    'submitAnswer': 'Soumettre',
                    'showSolutionButton': 'Voir la solution',
                    'tryAgain': 'Reessayer',
                    'wrongAnswerMessage': etape.get('feedback_incorrect', 'Incorrect. Tu perds une vie !'),
                    'correctAnswerMessage': etape.get('feedback_correct', 'Correct !'),
                    'scoreBarLabel': 'Score : :num sur :total',
                    'a11yCheck': 'Verifier.',
                    'a11yShowSolution': 'Solution.',
                    'a11yRetry': 'Recommencer.'
                },
                'confirmCheck': {'header': 'Valider ?', 'body': 'Sur ?', 'cancelLabel': 'Annuler', 'confirmLabel': 'Valider'},
                'confirmRetry': {'header': 'Reessayer ?', 'body': 'Recommencer.', 'cancelLabel': 'Annuler', 'confirmLabel': 'OK'},
                'question': f"<p><strong>{etape['title']}</strong></p>\n<p>{etape['question']}</p>\n"
            },
            'library': 'H5P.TrueFalse 1.8',
            'metadata': {'contentType': 'True/False Question', 'license': 'U', 'title': etape['title']},
            'subContentId': str(uuid.uuid4())
        }
    }

# ============================================================================
# CONSTRUCTION DES STAGES
# ============================================================================

elements = []
for i, e in enumerate(etapes):
    if e['type'] == 'multichoice':
        content = make_multichoice(e)
    elif e['type'] == 'dragtext':
        content = make_dragtext(e)
    elif e['type'] == 'blanks':
        content = make_blanks(e)
    elif e['type'] == 'truefalse':
        content = make_truefalse(e)

    neighbors = []
    if i > 0:
        neighbors.append(str(i - 1))
    if i < len(etapes) - 1:
        neighbors.append(str(i + 1))

    stage = {
        'id': str(uuid.uuid4()),
        'label': e['title'],
        'telemetry': {
            'x': str(e['x']),
            'y': str(e['y']),
            'width': '6',
            'height': '10'
        },
        'neighbors': neighbors,
        'type': 'stage',
        'canBeStartStage': (i == 0),
        'time': {},
        'accessRestrictions': {
            'allOrAnyRestrictionSet': 'all',
            'restrictionSetList': [{
                'allOrAnyRestriction': 'any',
                'restrictionList': [{'restrictionType': 'totalScore'}]
            }]
        },
        'specialStageExtraLives': 0,  # Pas de vie bonus
        'specialStageExtraTime': 0,
        'contentsList': [content]
    }
    elements.append(stage)

# ============================================================================
# CONTENT.JSON COMPLET
# ============================================================================

content = {
    'showTitleScreen': True,
    'titleScreen': {
        'titleScreenIntroduction': '''<p style="text-align: center;"><strong>Bienvenue, navigateur !</strong></p>
<p style="text-align: center;">Explore l'Archipel des Suites et conquiers chaque ile en repondant aux defis mathematiques.</p>
<p style="text-align: center;"><strong>Attention : tu n'as que 4 vies !</strong> Chaque erreur t'en coute une.</p>
<p style="text-align: center;">Bonne chance pour atteindre l'Ile du Tresor !</p>'''
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
            'endScreenTextNoSuccess': '''<p style="text-align: center;"><strong>Naufrage !</strong></p>
<p style="text-align: center;">Tu as perdu toutes tes vies avant d'atteindre le tresor.</p>
<p style="text-align: center;">Reprends la mer et reessaie !</p>'''
        },
        'success': {
            'endScreenTextSuccess': '''<p style="text-align: center;"><strong>Felicitations, navigateur !</strong></p>
<p style="text-align: center;">Tu as conquis l'Archipel des Suites et decouvert le tresor !</p>
<p style="text-align: center;">Les suites numeriques n'ont plus de secret pour toi.</p>'''
        },
        'overallFeedback': [
            {'from': 0, 'to': 40, 'feedback': "Continue tes explorations, tu peux progresser !"},
            {'from': 41, 'to': 70, 'feedback': "Bon voyage ! Tu maitrises les bases."},
            {'from': 71, 'to': 99, 'feedback': "Excellent parcours ! Tu es presque au sommet."},
            {'from': 100, 'to': 100, 'feedback': "Parfait ! Tu es un vrai maitre des suites !"}
        ]
    },
    'visual': {
        'stages': {
            'colorStage': COLORS['stageUnvisited'],
            'colorStageLocked': COLORS['stageLocked'],
            'colorStageCleared': COLORS['stageCleared'],
            'showScoreStars': CONFIG['showScoreStars']
        },
        'paths': {
            'displayPaths': CONFIG['displayPaths'],
            'style': {
                'colorPath': COLORS['pathNormal'],
                'colorPathCleared': COLORS['pathCleared'],
                'pathWidth': '0.25',
                'pathStyle': 'dotted'
            }
        },
        'misc': {
            'useAnimation': CONFIG['useAnimation']
        }
    },
    'audio': {
        'backgroundMusic': {'muteDuringExercise': True},
        'ambient': {}
    },
    'behaviour': {
        'enableRetry': True,
        'enableSolutionsButton': True,
        'lives': CONFIG['lives'],  # 4 VIES !
        'map': {
            'showLabels': CONFIG['showLabels'],
            'roaming': CONFIG['roaming'],  # Doit reussir pour avancer
            'fog': CONFIG['fog']
        }
    },
    'l10n': {
        'start': 'Embarquer !',
        'continue': 'Continuer',
        'restart': 'Recommencer',
        'showSolutions': 'Solutions',
        'completedMap': "Bravo ! Tu as explore tout l'archipel !",
        'fullScoreButnoLivesLeft': 'Score parfait mais plus de vies !',
        'confirmFinishHeader': 'Terminer le voyage ?',
        'confirmFinishDialog': "Si tu termines maintenant, tu ne pourras plus explorer.",
        'confirmFinishDialogSubmission': 'Ton score sera enregistre.',
        'confirmFinishDialogQuestion': 'Veux-tu vraiment terminer ?',
        'confirmAccessDeniedHeader': 'Ile verrouillee !',
        'confirmAccessDeniedDialog': 'Tu dois reussir les iles precedentes pour acceder a celle-ci.',
        'yes': 'Oui',
        'no': 'Non',
        'confirmGameOverHeader': 'Naufrage !',
        'confirmGameOverDialog': 'Tu as perdu toutes tes vies ! Recommence depuis le debut.',
        'confirmTimeoutHeader': 'Temps ecoule !',
        'confirmTimeoutDialog': "Le temps imparti est ecoule.",
        'confirmTimeoutDialogLostLife': "Temps ecoule ! Tu perds une vie.",
        'confirmScoreIncompleteHeader': 'Score incomplet !',
        'confirmIncompleteScoreDialogLostLife': "Tu n'as pas obtenu le score maximum. Tu perds une vie.",
        'confirmFullScoreHeader': 'Score parfait !',
        'confirmFullScoreDialog': "Bravo ! Tu peux continuer vers les autres iles.",
        'confirmFullScoreDialogLoseLivesAmendmend': "Attention, tu peux encore perdre des vies !",
        'ok': 'OK',
        'noStages': 'Aucune ile sur la carte.',
        'fullScoreButTimeout': 'Score parfait mais temps ecoule !'
    },
    'a11y': {
        'buttonFinish': 'Terminer',
        'buttonAudioActive': 'Couper le son',
        'buttonAudioInactive': 'Activer le son',
        'close': 'Fermer',
        'yourResult': 'Tu as obtenu @score sur @total points',
        'mapWasOpened': 'La carte est ouverte.',
        'mapSolutionsWasOpened': 'Mode solutions.',
        'startScreenWasOpened': 'Ecran de demarrage.',
        'endScreenWasOpened': 'Ecran de fin.',
        'exerciseLabel': '. Exercice pour @stagelabel',
        'stageButtonLabel': 'Ile : @stagelabel',
        'adjacentStageLabel': 'Ile voisine : @stagelabelNeighbor',
        'locked': 'Verrouillee',
        'cleared': 'Conquise',
        'applicationInstructions': 'Utilise Espace ou Entree pour activer une ile. Fleches pour naviguer.',
        'applicationDescription': "Carte de l'Archipel des Suites",
        'movedToStage': 'Deplacement vers @stagelabel',
        'stageUnlocked': 'Ile @stagelabel debloquee !',
        'toolbarFallbackLabel': 'Archipel des Suites',
        'enterFullscreen': 'Plein ecran',
        'exitFullscreen': 'Quitter plein ecran'
    },
    'headline': "L'Archipel des Suites"
}

# ============================================================================
# H5P.JSON
# ============================================================================

h5p = {
    'title': "L'Archipel des Suites",
    'language': 'fr',
    'mainLibrary': 'H5P.GameMap',
    'embedTypes': ['iframe'],
    'license': 'CC BY-SA',
    'preloadedDependencies': [
        {'machineName': 'H5P.GameMap', 'majorVersion': '1', 'minorVersion': '5'},
        {'machineName': 'H5P.MultiChoice', 'majorVersion': '1', 'minorVersion': '16'},
        {'machineName': 'H5P.DragText', 'majorVersion': '1', 'minorVersion': '10'},
        {'machineName': 'H5P.Blanks', 'majorVersion': '1', 'minorVersion': '14'},
        {'machineName': 'H5P.TrueFalse', 'majorVersion': '1', 'minorVersion': '8'},
        {'machineName': 'H5P.Question', 'majorVersion': '1', 'minorVersion': '5'},
        {'machineName': 'H5P.JoubelUI', 'majorVersion': '1', 'minorVersion': '3'},
        {'machineName': 'FontAwesome', 'majorVersion': '4', 'minorVersion': '5'}
    ]
}

# ============================================================================
# GENERATION
# ============================================================================

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('h5p.json', json.dumps(h5p, ensure_ascii=False, indent=2))
    zf.writestr('content/content.json', json.dumps(content, ensure_ascii=False, indent=2))
    zf.writestr('content/images/background.png', image_data)

with open(OUTPUT_DIR / 'archipel_suites_final.h5p', 'wb') as f:
    f.write(buf.getvalue())

print("=" * 60)
print("  L'ARCHIPEL DES SUITES - VERSION FINALE")
print("=" * 60)
print("[OK] Fichier : archipel_suites_final.h5p")
print()
print("Configuration du jeu :")
print(f"   - {CONFIG['lives']} vies")
print(f"   - Roaming : {CONFIG['roaming']} (doit reussir pour avancer)")
print(f"   - Brouillard : {CONFIG['fog']}")
print(f"   - Etoiles : {CONFIG['showScoreStars']}")
print()
print("7 iles avec types varies :")
for i, e in enumerate(etapes):
    icon = {'multichoice': 'QCM', 'dragtext': 'DRAG', 'blanks': 'FILL', 'truefalse': 'V/F'}
    print(f"   {i+1}. {e['title']} [{icon.get(e['type'])}]")
print()
print("[+] Interface 100% francais")
print("[+] Feedbacks personnalises")
print("[+] Couleurs style aventure")
print("=" * 60)
