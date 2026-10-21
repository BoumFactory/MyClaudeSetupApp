# Skill H5P Game Map - Parcours Gamifiés

## Description

Génère des parcours pédagogiques gamifiés au format H5P Game Map pour Moodle. Les élèves progressent sur une carte en répondant à des défis mathématiques.

## Modes d'utilisation

### 1. Appel direct via commande
```
/createGameMap [chemin] [--style STYLE] [--etapes N] [--output DOSSIER]
```

### 2. Délégation par agent (intégration /moodleise)

Ce skill est utilisé par `/moodleise` (skill `moodle-course-creator`) en modes **Enrichi** ou **Parcours complet**.

L'agent principal lance un agent (`meta-high`) avec le prompt :
```
Utilise le skill h5p-gamemap (/createGameMap) pour créer un parcours gamifié complet.
Contexte : [niveau], [thème], [contenu pédagogique extrait]
```

### 3. Analyse de ressources

Le skill peut analyser différents types de fichiers :
- `.tex` → Extraction des environnements bfcours
- `.pdf` → Analyse de la structure et du contenu
- `.html` → Parsing des présentations reveal.js
- `.md` → Parsing Markdown structuré

Voir la commande `/createGameMap` pour l'arbre de décision complet.

## Workflow recommandé

### 1. Génération du préplan

```bash
/createGameMap "<dossier de la séquence>/Capsule_H5P/" --preplan --theme "Suites numériques" --niveau 1ere
```

Cela génère un fichier `preplan_gamemap.md` à modifier.

### 2. Modification du préplan

L'utilisateur modifie le fichier Markdown :
- Ajuste les questions et réponses
- Modifie les positions des étapes
- Personnalise les feedbacks
- Choisit les types de questions

### 3. Validation des positions (NOUVELLE ÉTAPE)

Avant de générer le H5P final, lancer l'outil de prévisualisation :

```bash
python ".claude/skills/h5p-gamemap/scripts/hotspot_preview.py" \
  --image "chemin/background.png" \
  --positions "chemin/preplan_gamemap.md" \
  --update-preplan
```

L'utilisateur peut alors repositionner visuellement les hotspots sur la carte.

### 4. Génération du H5P

Après validation du préplan :

```bash
/createGameMap "<dossier de la séquence>/Capsule_H5P/" --from-preplan
```

---

## RÈGLES CRITIQUES

### 0. PLUSIEURS QUESTIONS PAR ÉTAPE (NOUVEAU - OBLIGATOIRE)

**Chaque étape du parcours DOIT contenir PLUSIEURS questions (2-4 minimum).**

```
❌ INTERDIT : truefalse seul, multichoice seul, blanks seul
✅ OBLIGATOIRE : questionset avec 2-4 questions de types variés
✅ EXCEPTION : singlechoiceset (enchaîne déjà plusieurs questions)
```

| Type d'étape | Structure REQUISE |
|--------------|-------------------|
| Vocabulaire | `questionset` [dragtext + 2 autres types] |
| Définitions | `questionset` [blanks + truefalse + multichoice] |
| Propriétés | `questionset` [truefalse + truefalse + multichoice] |
| Calculs | `questionset` [multichoice × 2-3 + truefalse] |
| Synthèse | `questionset` [4-6 questions de TOUS types] |

**Exemple de structure d'étape correcte :**

```python
{
    "title": "Le Pont des Définitions",
    "type": "questionset",  # TOUJOURS questionset (sauf singlechoiceset)
    "content": {
        "questions": [
            {"type": "dragtext", "text": "Une *suite* est une *fonction* de N vers R..."},
            {"type": "truefalse", "question": "...", "correct": True, ...},
            {"type": "multichoice", "question": "...", "answers": [...]}
        ]
    }
}
```

### 1. PAS DE LATEX DANS LES RÉPONSES ÉLÈVES

**Les réponses que l'élève doit saisir ou glisser NE DOIVENT JAMAIS contenir de LaTeX.**

Sinon, l'élève devra taper exactement `\mathbb{N}` ce qui génère des erreurs gratuites.

| Type | Zone LaTeX autorisé | Zone LaTeX INTERDIT |
|------|---------------------|---------------------|
| `multichoice` | Question, propositions, feedbacks | - |
| `truefalse` | Question, feedbacks | - |
| `dragtext` | Texte d'habillage | **Mots à glisser** (`*mot*`) |
| `blanks` | Texte d'habillage | **Réponses attendues** (`*mot*`) |
| `singlechoiceset` | Questions, propositions | - |

**Exemple CORRECT pour blanks** :
```
La notation \((u_n)_{n \in \mathbb{N}}\) avec parenthèses désigne *la suite entière*.
Sans parenthèses, \(u_n\) désigne *un terme particulier* de *rang* n.
```

**Exemple INCORRECT** :
```
La suite est définie sur *\(\mathbb{N}\)*.
```
→ L'élève devrait taper `\(\mathbb{N}\)` !

### 2. DRAGTEXT : TOUJOURS UNE LIGNE FINALE SANS TROU

**Bug H5P** : Si la dernière ligne contient un mot à glisser, l'interface peut buguer et empêcher de placer le dernier mot.

**Solution** : Toujours terminer par une ligne de texte simple (question engageante, remarque...).

**Exemple CORRECT** :
```
Une suite est *croissante* si chaque terme est plus grand que le précédent.
Elle est *décroissante* si chaque terme est plus petit.

Connais-tu bien ton vocabulaire ?
```

**Exemple INCORRECT** :
```
Une suite est *croissante* si elle augmente.
Elle est *décroissante* si elle diminue.
```
→ Le dernier mot `*décroissante*` peut buguer !

### 3. POSITIONS DES HOTSPOTS : VALIDATION VISUELLE OBLIGATOIRE

Les positions x/y en % ne correspondent pas toujours visuellement à l'image de fond.

**⚠️ TOUJOURS lancer le script de prévisualisation AVANT de générer le H5P final :**

```bash
python ".claude/skills/h5p-gamemap/scripts/hotspot_preview.py" \
  --image "[dossier]/background.png" \
  --positions "[dossier]/preplan_gamemap.md" \
  --update-preplan
```

**Cette étape est INTERACTIVE et nécessite la validation de l'utilisateur.**
**NE JAMAIS SAUTER cette étape, même en mode sous-agent !**

Le script :
1. Ouvre une fenêtre avec l'image de fond
2. Affiche les hotspots aux positions définies
3. Permet à l'utilisateur de les repositionner par glisser-déposer
4. Met à jour automatiquement le préplan avec les nouvelles positions
5. Crée un fichier `.done` ou `.cancelled` pour signaler la fin

### 4. DISTINCTION RANG / POSITION (Pédagogie)

Pour les suites, attention à la distinction :
- `u_5` est le terme de **rang 5**
- Mais c'est le **6ème terme** de la suite (si on commence à `u_0`)

Inclure cette nuance dans les exercices de notation.

---

## Types de contenus disponibles

### Questions interactives

| Type | Code | Syntaxe spéciale | Usage |
|------|------|------------------|-------|
| QCM | `multichoice` | LaTeX : `\(formule\)` | Calculs, choix conceptuels |
| Vrai/Faux | `truefalse` | - | Propriétés, définitions |
| Glisser-déposer | `dragtext` | `*mot*` (SANS LaTeX) | Vocabulaire, associations |
| Texte à trous | `blanks` | `*mot*` (SANS LaTeX) | Définitions, compléter phrases |
| Sélectionner mots | `markthewords` | `*mot*` à sélectionner | Identifier éléments |
| Ordonner | `sortparagraphs` | Liste ordonnée | Étapes démonstration |

### Questions groupées

| Type | Code | Description |
|------|------|-------------|
| Quiz rapide | `singlechoiceset` | 2-5 QCM enchaînés |
| Set de questions | `questionset` | Mix de types (boss final) |

### Contenus non-interactifs (RESPIRATIONS)

| Type | Code | Usage |
|------|------|-------|
| Texte avancé | `advancedtext` | Rappel de cours, checkpoint, encouragement |
| Image | `image` | Illustration, schéma récapitulatif |

**IMPORTANT** : Les étapes `advancedtext` n'ont pas de score et servent de "respiration" entre les défis.

---

## Conception du parcours (AMBITIEUX)

**OBJECTIF** : Créer une aventure pédagogique, PAS des exercices en batterie.

### Règles anti-batterie

1. **JAMAIS 2 mêmes types consécutifs**
2. **Alterner quiz et respirations** (1 respiration toutes les 3-4 étapes)
3. **Noms d'étapes évocateurs** (pas "Question 1, 2, 3...")
4. **Embranchements optionnels** (défis bonus sur le côté)

### Structure narrative (10-15 étapes)

```
ZONE DÉCOUVERTE (3-4 étapes)
│ dragtext → blanks → truefalse
│ Vocabulaire, définitions, premières notions
▼
[RESPIRATION : rappel visuel]
▼
ZONE EXPLORATION (4-5 étapes)
│ multichoice → [★ bonus optionnel] → singlechoiceset → truefalse
│ Premiers calculs, propriétés
▼
[CHECKPOINT : encouragement]
▼
ZONE MAÎTRISE (3-4 étapes)
│ multichoice → questionset → BOSS FINAL
│ Applications, synthèse
```

### Nommage des étapes

| ✗ Éviter | ✓ Préférer |
|----------|------------|
| Question 1 | 🚢 Le Départ |
| Exercice 2 | 📜 Le Parchemin |
| QCM 3 | 🌉 Le Pont des Calculs |
| Vrai/Faux 4 | ⚖️ La Balance |
| Synthèse | 🏆 Le Trésor |

### Défis bonus (★)

- 1-2 étapes optionnelles **sur le côté** de la carte
- Plus difficiles mais récompensent (+1 vie)
- Accessibles mais pas obligatoires pour finir

---

## Paramètres de style

### Styles prédéfinis

| Style | Vies | Roaming | Fog | Usage |
|-------|------|---------|-----|-------|
| `aventure` | 4 | complete | visited | Révision ludique |
| `revision` | illimité | free | none | Entraînement |
| `evaluation` | 1 | strict | visited | Test noté |
| `decouverte` | illimité | free | all | Introduction |

---

## LaTeX dans les questions

### Support par type

| Type | Question | Réponses | Feedback |
|------|----------|----------|----------|
| multichoice | Oui | Oui | Oui |
| truefalse | Oui | - | Oui |
| dragtext | Oui (texte) | **NON** (mots drag) | Oui |
| blanks | Oui (texte) | **NON** (trous) | Oui |
| singlechoiceset | Oui | Oui | Oui |

### Syntaxe MathJax

```latex
\(u_n = 2n + 1\)           % Inline
\(\mathbb{N}\)             % Ensemble N
\(\sum_{k=0}^{n} u_k\)     % Somme
```

---

## Règles de conception

### Variation des types

Pour un parcours de N étapes :
- **Max 40% QCM** (éviter la monotonie)
- **Min 1 DragText** ou Blanks (interactivité)
- **Min 2 types différents** pour 4+ étapes

### Feedbacks obligatoires

Chaque réponse doit avoir :
- Un feedback explicatif (pas juste "correct/incorrect")
- Une explication de l'erreur pour les mauvaises réponses
- Un indice optionnel

### Progression pédagogique

1. Commencer par des définitions/vocabulaire
2. Progresser vers des calculs simples
3. Terminer par des applications complexes

---

## Fichiers générés

```
[dossier_sortie]/
├── preplan_gamemap.md       # Préplan modifiable
├── gamemap_[theme].h5p      # Fichier H5P final
├── background.png           # Image de fond (si générée)
└── positions_corrected.json # Positions après validation visuelle
```

---

## Scripts disponibles

| Script | Usage |
|--------|-------|
| `generate_gamemap.py` | Génération complète depuis préplan |
| `parse_preplan.py` | Parse le Markdown en structure JSON |
| `validate_preplan.py` | Vérifie la cohérence du préplan |
| `hotspot_preview.py` | **Prévisualisation et repositionnement des hotspots** |

### Utilisation de hotspot_preview.py

```bash
# Depuis un préplan Markdown
python hotspot_preview.py --image carte.png --positions preplan.md --update-preplan

# Depuis un JSON
python hotspot_preview.py --image carte.png --positions positions.json -o positions_new.json
```

**Fonctionnement** :
1. Ouvre une fenêtre avec l'image et les hotspots positionnés
2. Permet de glisser-déposer les hotspots
3. Affiche les coordonnées en temps réel
4. Crée un fichier `.done` quand validé (pour notification)

---

## Exemple de préplan minimal

```markdown
# Préplan Game Map : Les Vecteurs

## Informations générales
- **Titre** : L'Île aux Vecteurs
- **Niveau** : 2nde
- **Style** : aventure

## Configuration du jeu
| Paramètre | Valeur |
|-----------|--------|
| **Vies** | 4 |
| **Roaming** | complete |

## Étapes du parcours

### Étape 1 : Définition
- **Position** : x=15, y=70
- **Type** : multichoice

**Question** : Un vecteur est caractérisé par :

| | Réponse | Feedback |
|-|---------|----------|
| [x] | Direction, sens et norme | Bravo ! |
| [ ] | Longueur uniquement | Non, il manque des éléments. |
```

---

## Workflow avec validation des positions

```
1. Créer le préplan (/createGameMap --preplan)
        ↓
2. Modifier le préplan manuellement
        ↓
3. Générer/obtenir l'image de fond
        ↓
4. Lancer hotspot_preview.py  ← VALIDATION VISUELLE
        ↓
   [Utilisateur repositionne les hotspots]
        ↓
5. Génération du H5P final
```

L'outil `hotspot_preview.py` crée un fichier signal `.done` ou `.cancelled` pour permettre à Claude de continuer automatiquement après validation.

---

## Dépendances

- Python 3.8+
- Modules obligatoires : `json`, `zipfile`, `uuid`, `pathlib`, `re`
- Modules pour prévisualisation : `tkinter`, `pillow`
- Optionnel : un outil de génération d'images pour les fonds

Installation des dépendances GUI :
```bash
pip install pillow
```

---

## Voir aussi

- `references/ETAT_DES_LIEUX.md` - Documentation technique complète
- `examples/preplan_gamemap.md` - Exemple de préplan
