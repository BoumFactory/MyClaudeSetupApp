# Prompts pour générer des questions de révision

Ces prompts sont à utiliser avec une IA (ChatGPT, Mistral, Claude...) pour générer des questions au bon format JSON.

---

## Prompt générique (toutes matières)

```
Génère-moi des questions de révision au format JSON pour mon application.

Matière : [MATIERE]
Thème : [THEME]
Niveau : Lycée

Format requis (un seul objet JSON ou un tableau) :

Pour un QCM :
{
  "subject": "[matiere-id]",
  "theme": "[Thème affiché]",
  "type": "qcm",
  "difficulty": 1,
  "question": "Ta question avec $LaTeX$ si besoin",
  "choices": [
    { "id": "a", "text": "Choix A" },
    { "id": "b", "text": "Choix B" },
    { "id": "c", "text": "Choix C" }
  ],
  "correctAnswers": ["b"],
  "explanation": "Explication de la réponse"
}

Pour une réponse libre :
{
  "subject": "[matiere-id]",
  "theme": "[Thème affiché]",
  "type": "input",
  "difficulty": 2,
  "question": "Ta question",
  "fields": [
    {
      "id": "reponse",
      "label": "Réponse :",
      "type": "text",
      "answer": "réponse attendue",
      "alternatives": ["autre forme acceptée"]
    }
  ],
  "explanation": "Explication"
}

IDs de matières disponibles : maths, physique, svt, nsi, francais, philosophie, histoire-geo, ses, anglais, allemand, espagnol

Génère 5 questions variées (QCM et réponses libres mélangés).
```

---

## Prompt spécifique Maths

```
Génère 5 questions de maths niveau lycée au format JSON.

Thème : [Second degré / Dérivation / Suites / Probabilités / ...]

Utilise le LaTeX pour les formules :
- Inline : $x^2 + 2x + 1$
- Fractions : $\frac{a}{b}$
- Racines : $\sqrt{\Delta}$

Format :
[
  {
    "subject": "maths",
    "theme": "[Thème]",
    "type": "qcm" ou "input",
    "difficulty": 1 à 3,
    "question": "...",
    "choices": [...] ou "fields": [...],
    "correctAnswers": [...],
    "explanation": "..."
  }
]

Pour les champs numériques, utilise "type": "number" avec une "tolerance" si besoin.
```

---

## Prompt spécifique NSI/Python

```
Génère 5 questions de NSI/Python niveau lycée au format JSON.

Thème : [Python / Algorithmes / Structures de données / ...]

Pour le code, utilise les backticks :
- Inline : `print("Hello")`
- Bloc :
```python
def fonction(x):
    return x * 2
```

Format :
[
  {
    "subject": "nsi",
    "theme": "[Thème]",
    "type": "qcm",
    "question": "Que retourne ce code ?\n```python\nprint(len('test'))\n```",
    "choices": [
      { "id": "a", "text": "`3`" },
      { "id": "b", "text": "`4`" }
    ],
    "correctAnswers": ["b"],
    "explanation": "..."
  }
]
```

---

## Prompt spécifique Physique-Chimie

```
Génère 5 questions de physique-chimie niveau lycée au format JSON.

Thème : [Mécanique / Chimie organique / Ondes / ...]

Pour les formules chimiques, utilise : $\ce{H2O}$, $\ce{CH3COOH}$
Pour les unités : $\text{m/s}$, $\text{J}$

Format avec tolerance pour les calculs :
{
  "subject": "physique",
  "theme": "[Thème]",
  "type": "input",
  "question": "Calculez la vitesse...",
  "fields": [{
    "id": "vitesse",
    "label": "v (en m/s) :",
    "type": "number",
    "answer": 15.5,
    "tolerance": 0.1
  }],
  "explanation": "..."
}
```

---

## Prompt spécifique Langues

```
Génère 5 questions d'anglais niveau lycée au format JSON.

Thème : [Grammaire / Vocabulaire / Conjugaison / ...]

Exemples de questions :
- Compléter une phrase
- Choisir la bonne forme verbale
- Traduire un mot/expression

Format :
{
  "subject": "anglais",
  "theme": "Grammaire",
  "type": "qcm",
  "question": "Complete: She ___ to school every day.",
  "choices": [
    { "id": "a", "text": "go" },
    { "id": "b", "text": "goes" },
    { "id": "c", "text": "going" }
  ],
  "correctAnswers": ["b"],
  "explanation": "Third person singular takes 's' in present simple."
}
```

---

## Prompt pour import en lot

```
Je veux importer plusieurs questions dans mon application de révision.
Génère un tableau JSON avec 10 questions de [MATIERE] sur [THEME].

Mélange :
- 6 QCM (type: "qcm")
- 4 réponses libres (type: "input")

Difficulté variée : 3 faciles (1), 5 moyennes (2), 2 difficiles (3)

Format attendu :
[
  { ... question 1 ... },
  { ... question 2 ... },
  ...
]

Important :
- subject doit être l'ID exact de la matière
- Pour les QCM, correctAnswers est un tableau (ex: ["a"])
- Pour les inputs, fields contient au moins un champ avec id, type, answer
```

---

## IDs des matières

| ID | Matière |
|----|---------|
| maths | Mathématiques |
| physique | Physique-Chimie |
| svt | SVT |
| nsi | NSI |
| francais | Français |
| philosophie | Philosophie |
| histoire-geo | Histoire-Géographie |
| ses | SES |
| anglais | Anglais |
| allemand | Allemand |
| espagnol | Espagnol |

---

## Conseils

1. **Vérifiez le JSON** : L'IA peut faire des erreurs de syntaxe. Utilisez un validateur JSON si besoin.

2. **Testez dans l'app** : Importez une question test avant d'en générer beaucoup.

3. **Adaptez les alternatives** : Pour les réponses libres, pensez aux différentes façons d'écrire la même réponse (avec/sans espaces, fractions vs décimales...).

4. **Difficulté** : 1 = Facile (application directe), 2 = Moyen (un peu de réflexion), 3 = Difficile (plusieurs étapes).
