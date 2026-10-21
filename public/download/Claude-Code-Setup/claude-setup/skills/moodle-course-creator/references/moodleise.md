# Procédure « moodleise » : création automatique d'un cours Moodle

## Description
Transforme un dossier de séquence pédagogique en cours Moodle importable (.mbz) avec parcours interactifs H5P.

## Usage
Cette procédure s'applique quand l'utilisateur demande de « moodleiser » un dossier de séquence : `<chemin_dossier_sequence>` est le dossier de la séquence.

## Exemples d'utilisation
```bash
# Moodleiser un chapitre complet
moodleiser "<dossier>/1ere/Sequence-Suites_numeriques"
→ Génère: Sequence-Suites_numeriques/cours_moodle.mbz

# Moodleiser le dossier courant
moodleiser le dossier courant
→ Génère: ./cours_moodle.mbz
```

## Protocole d'exécution

### ÉTAPE 0 : DEMANDER LE MODE DE MOODLEISATION

**OBLIGATOIRE** - Poser la question à l'utilisateur (AskUserQuestion si disponible) pour demander le mode souhaité :

```
Question: Quel type de moodleisation souhaitez-vous ?

Options:
1. Simple (Recommandé) - Package Moodle basique avec PDFs, pas de quiz générés
2. Enrichi - Package avec quiz H5P de révision par section
3. Parcours complet - Interactive Book H5P avec cours et exercices intégrés
```

**Selon le choix** :
- **Simple** → Sauter les étapes 3-4 (pas de génération H5P)
- **Enrichi** → Exécuter toutes les étapes avec H5P classiques
- **Parcours complet** → Créer un Interactive Book H5P (mode avancé)

### ÉTAPE 1 : ANALYSER LE DOSSIER SOURCE

Scanner le dossier fourni pour identifier :

1. **Dossier Cours/** → Documents de cours (PDFs) + Sources LaTeX
2. **Dossier Exos*/** ou **Exercices*/** → Fiches d'exercices
3. **Dossier Evaluation*/** → Sujets et corrigés
4. **Dossier Revision*/** ou **Fiche*/** → Fiches de révision (PDFs)
5. **Dossier Diaporama*/** ou **Presentation*/** → Présentations reveal.js (HTML)
6. **Dossier Animation*/** → Animations interactives (HTML/JS)
7. **Dossier Activit*/** → Activités pédagogiques (PDFs, HTML)

**Fichiers à la racine à inclure** :
- `*.html` (présentations reveal.js, animations)
- `fiche*.pdf`, `revision*.pdf` (fiches de révision)
- `activite*.pdf` (activités)

**EXCLURE ABSOLUMENT** :
- `Sources/`, `source/`, `src/` - fichiers LaTeX sources
- `Ressources/`, `ressources/` - documents externes d'autres collègues
- `preview_*.html` - fichiers de prévisualisation générés
- Fichiers `.tex`, `.aux`, `.log`, `.synctex.gz`, etc.

### ÉTAPE 2 : IDENTIFIER LE CHAPITRE

Extraire du nom du dossier ou des PDFs :
- **Niveau** : 6eme, 5eme, 4eme, 3eme, 2nde, 1ere, Terminale
- **Thème** : Suites, Vecteurs, Probabilités, etc.
- **Titre complet** pour le cours Moodle

### ÉTAPE 3 : LIRE LES SOURCES LATEX (modes Enrichi/Complet)

Pour générer des questions H5P pertinentes :
1. **Lire les fichiers `enonce.tex`** dans les dossiers Cours/ et Exos/
2. Identifier les notions clés, définitions, théorèmes
3. Repérer les exemples et applications types
4. Extraire les formules mathématiques importantes

### ÉTAPE 4 : GÉNÉRER LES QUESTIONS H5P (modes Enrichi/Complet)

#### Mode Enrichi - Quiz par section

Pour chaque section du cours, générer un quiz avec des types variés :

**Types de questions à utiliser** :
- `multichoice` - QCM classique avec formules LaTeX
- `truefalse` - Vrai/Faux pour les propriétés
- `blanks` - Textes à trous pour les définitions
- `dragwords` - Vocabulaire à placer

**Structure des quiz par section** :
```
Section 1 (Définitions) → Quiz vocabulaire (3-4 questions)
Section 2 (Propriétés) → Quiz Vrai/Faux (3-4 questions)
Section 3 (Applications) → Quiz calculs (4-6 questions)
Quiz final → Synthèse (8-12 questions multi-types)
```

**Formats des questions avancées** :

```json
// Multichoice avec LaTeX
{
  "type": "multichoice",
  "name": "Calcul de terme",
  "text": "Si \\(u_n = 2n + 1\\), que vaut \\(u_5\\) ?",
  "options": ["\\(11\\)", "\\(10\\)", "\\(9\\)", "\\(12\\)"],
  "correct_index": 0,
  "feedback": "On calcule \\(u_5 = 2 \\times 5 + 1 = 11\\)",
  "tip": "Remplacez n par 5"
}

// Vrai/Faux
{
  "type": "truefalse",
  "name": "Propriété suite",
  "text": "Une suite arithmétique a une raison constante.",
  "correct": true,
  "feedback_correct": "C'est la définition !",
  "feedback_incorrect": "C'est justement la définition."
}

// Texte à trous
{
  "type": "blanks",
  "name": "Compléter",
  "text": "Une suite définie par *récurrence* calcule chaque terme à partir du *précédent*."
}

// Drag the words
{
  "type": "dragwords",
  "name": "Vocabulaire",
  "text": "Le nombre \\(u_n\\) est le *terme* *général* de la suite."
}
```

#### Mode Parcours Complet - Interactive Book

Créer un livre interactif H5P structuré par chapitres :

```json
{
  "title": "Suites numériques",
  "chapters": [
    {
      "title": "1. Notion de suite",
      "contents": [
        {"type": "text", "content": "<h2>Définition</h2><p>Cours HTML avec \\(LaTeX\\)</p>"},
        {"type": "blanks", "text": "Une suite est une *fonction* de \\(\\mathbb{N}\\) vers \\(\\mathbb{R}\\)."},
        {"type": "quiz", "questions": [...]}
      ]
    },
    {
      "title": "2. Suite explicite",
      "contents": [...]
    }
  ]
}
```

### ÉTAPE 4bis : GÉNÉRER UN GAME MAP H5P (modes Enrichi/Complet - OBLIGATOIRE)

**OBLIGATOIRE** pour les modes Enrichi et Parcours complet : déléguer la création d'un Game Map H5P complet.

#### Étape 4bis-A : Gérer l'image de fond

**AVANT de générer le Game Map**, demander à l'utilisateur :

```
Question: Pour le parcours gamifié (Game Map), avez-vous une image de fond ?

Options:
1. Fournir une image de fond (Recommandé) - Je donnerai le chemin vers ma carte d'aventure
2. Image plus tard - Arrêter ici pour que j'ajoute mon image
3. Pas d'image - Utiliser un fond neutre (moins immersif)
```

**Si l'utilisateur fournit une image**, lui demander le chemin et vérifier qu'elle existe.

Rappeler à l'utilisateur ce qu'une bonne image de fond doit contenir :

- format paysage (1920 x 1080 conseillé) ;
- un chemin sinueux avec des points d'étape bien visibles (un par spot voulu) ;
- aucun texte ni formule sur l'image.

L'image n'est pas générée par le paquet : l'utilisateur la crée avec l'outil de son choix ou la prend dans une banque d'images libres de droits.

**Donner le nombre de spots voulus au moment de lancer le Game Map.**

#### Étape 4bis-B : Lancement de l'agent meta-high pour le Game Map

```python
Task(
    subagent_type="meta-high",
    prompt=f"""
    Utilise le skill h5p-gamemap pour créer un parcours gamifié complet.

    **Contexte du cours** :
    - Niveau : {niveau}
    - Thème : {theme}
    - Dossier de sortie : {dossier}/Capsule_H5P/
    - **Image de fond** : {chemin_image_fond}  ← UTILISER CETTE IMAGE

    **Contenu pédagogique extrait des sources LaTeX** :
    {resume_notions_cles}

    **Exigences** :
    - 6 à 10 étapes de progression logique
    - Types variés : max 40% QCM, min 1 DragText, min 1 Blanks, min 1 TrueFalse
    - Feedbacks explicatifs pour CHAQUE réponse (correcte ET incorrecte)
    - Style "aventure" avec 4 vies et roaming "complete"
    - Workflow complet : préplan → validation → génération H5P
    - Respecter les règles LaTeX : PAS de LaTeX dans les zones de réponse élève
    - Intégrer l'image de fond fournie dans le fichier H5P final

    Retourne le chemin absolu du fichier .h5p généré.
    """
)
```

#### Récupération du résultat

Après exécution de l'agent :
1. Vérifier que le fichier `.h5p` existe dans `{dossier}/Capsule_H5P/`
2. Noter le chemin pour l'intégrer à la configuration JSON
3. Le Game Map sera ajouté dans la section "Parcours de révision"

#### En cas d'échec

Si l'agent échoue :
- Logger l'erreur
- Proposer de continuer SANS Game Map (mode dégradé)
- Ou réessayer avec des paramètres simplifiés (6 étapes, 3 types)

### ÉTAPE 5 : CRÉER LA FAÇADE DU COURS (PAGE D'ACCUEIL)

**OBLIGATOIRE pour tous les modes** - Créer une page HTML qui sert de **hub de navigation** vers tous les contenus du cours.

#### Objectif

Cette façade :
- Donne une **vue d'ensemble claire** du cours aux élèves
- Facilite la **navigation** vers chaque ressource
- Présente le contenu de manière **attractive et structurée**
- Sert de **point d'entrée principal** au cours Moodle

#### Structure de la façade

```html
<!-- Template de base -->
<div class="course-facade" style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px;">

  <!-- En-tête -->
  <div class="header" style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-bottom: 30px;">
    <h1 style="margin: 0; font-size: 2.2em;">[TITRE DU CHAPITRE]</h1>
    <p style="margin: 10px 0 0 0; opacity: 0.9;">[NIVEAU] - Mathématiques</p>
  </div>

  <!-- Sections de navigation -->
  <div class="nav-sections" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">

    <!-- Section Cours -->
    <div class="nav-card" style="background: #f8f9fa; border-radius: 12px; padding: 20px; border-left: 4px solid #3498db;">
      <h2 style="color: #2c3e50; margin-top: 0; display: flex; align-items: center; gap: 10px;">
        📘 Cours
      </h2>
      <ul style="list-style: none; padding: 0; margin: 0;">
        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">
          <a href="@@PLUGINFILE@@/cours_chapitre.pdf" style="color: #3498db; text-decoration: none;">
            📄 Cours complet (PDF)
          </a>
        </li>
        <!-- Répéter pour chaque ressource cours -->
      </ul>
    </div>

    <!-- Section Exercices -->
    <div class="nav-card" style="background: #f8f9fa; border-radius: 12px; padding: 20px; border-left: 4px solid #2ecc71;">
      <h2 style="color: #2c3e50; margin-top: 0;">
        ✏️ Exercices
      </h2>
      <ul style="list-style: none; padding: 0; margin: 0;">
        <!-- Liens vers les fiches d'exercices -->
      </ul>
    </div>

    <!-- Section Activités interactives -->
    <div class="nav-card" style="background: #f8f9fa; border-radius: 12px; padding: 20px; border-left: 4px solid #9b59b6;">
      <h2 style="color: #2c3e50; margin-top: 0;">
        🎮 Activités interactives
      </h2>
      <ul style="list-style: none; padding: 0; margin: 0;">
        <!-- Liens vers H5P, animations, etc. -->
      </ul>
    </div>

    <!-- Section Révisions -->
    <div class="nav-card" style="background: #f8f9fa; border-radius: 12px; padding: 20px; border-left: 4px solid #e74c3c;">
      <h2 style="color: #2c3e50; margin-top: 0;">
        🔄 Révisions
      </h2>
      <ul style="list-style: none; padding: 0; margin: 0;">
        <!-- Liens vers fiches de révision, quiz -->
      </ul>
    </div>

  </div>

  <!-- Pied de page optionnel -->
  <div class="footer" style="text-align: center; margin-top: 30px; padding: 15px; color: #7f8c8d; font-size: 0.9em;">
    <p>Bon courage ! N'hésite pas à poser des questions. 💪</p>
  </div>

</div>
```

#### Génération dynamique

L'agent doit **construire dynamiquement** le HTML de la façade en fonction du contenu détecté à l'étape 1 :

```python
# Pseudo-code de génération
facade_sections = []

# Pour chaque type de contenu trouvé
if cours_pdfs:
    facade_sections.append({
        "titre": "📘 Cours",
        "couleur": "#3498db",
        "items": [{"nom": pdf.stem, "lien": f"@@PLUGINFILE@@/{pdf.name}", "icone": "📄"} for pdf in cours_pdfs]
    })

if exercices_pdfs:
    facade_sections.append({
        "titre": "✏️ Exercices",
        "couleur": "#2ecc71",
        "items": [...]
    })

if animations_html:
    facade_sections.append({
        "titre": "🎬 Animations",
        "couleur": "#f39c12",
        "items": [{"nom": anim.stem, "lien": f"[LIEN_ACTIVITE_{i}]", "icone": "🎯"} for anim in animations_html]
    })

if h5p_activities:
    facade_sections.append({
        "titre": "🎮 Quiz interactifs",
        "couleur": "#9b59b6",
        "items": [{"nom": h5p.title, "lien": f"[LIEN_H5P_{i}]", "icone": "🧠"} for h5p in h5p_activities]
    })

if presentations_html:
    facade_sections.append({
        "titre": "📽️ Présentations",
        "couleur": "#1abc9c",
        "items": [...]
    })

if evaluation_pdfs:
    facade_sections.append({
        "titre": "📝 Évaluation",
        "couleur": "#e74c3c",
        "items": [...]
    })
```

#### Liens internes Moodle

Pour les liens **internes au cours Moodle** :
- **Fichiers PDFs intégrés** : `@@PLUGINFILE@@/nom_fichier.pdf`
- **Activités H5P** : Utiliser la syntaxe de lien relatif Moodle ou indiquer "[Voir dans la section X]"
- **Présentations HTML** : Si uploadées comme ressource URL ou fichier

#### Placement dans le cours

La façade est placée **en première position** :

```json
{
  "sections": [
    {
      "name": "🏠 Accueil du cours",
      "visible": true,  // VISIBLE par défaut !
      "activities": [
        {
          "type": "page",
          "name": "Plan du cours - Navigation",
          "content": "[HTML DE LA FAÇADE]",
          "intro": "Bienvenue ! Utilise cette page pour naviguer dans le cours."
        }
      ]
    },
    // Autres sections...
  ]
}
```

**Important** : Cette section d'accueil est la SEULE visible par défaut !

#### Variantes de style

**Style Collège (6e-3e)** :
- Couleurs vives, icônes ludiques
- Textes courts et explicites
- Boutons larges et cliquables

**Style Lycée (2nde-Terminale)** :
- Design plus épuré et professionnel
- Palette sobre (bleus, gris)
- Organisation par compétences si pertinent

#### Fichier de sortie

Sauvegarder aussi le HTML de la façade dans le dossier :
```
{dossier}/Moodle_Course/facade_cours.html
```

Cela permet :
- Prévisualisation avant import
- Réutilisation/modification ultérieure
- Backup du contenu

---

### ÉTAPE 6 : CRÉER LA CONFIGURATION JSON

#### Mode Simple
```json
{
  "course_fullname": "Mathematiques [Niveau] - [Chapitre]",
  "course_shortname": "MATH-[CODE]",
  "output": "cours_moodle.mbz",
  "sections": [
    {"name": "🏠 Accueil", "visible": true, "activities": [page façade navigation]},
    {"name": "1. Cours", "visible": false, "activities": [PDFs cours]},
    {"name": "2. Exercices", "visible": false, "activities": [PDFs exos]},
    {"name": "3. Évaluation", "visible": false, "activities": [PDFs éval]}
  ]
}
```

#### Mode Enrichi
```json
{
  "course_fullname": "Mathematiques [Niveau] - [Chapitre]",
  "course_shortname": "MATH-[CODE]",
  "output": "cours_moodle.mbz",
  "sections": [
    {"name": "🏠 Accueil", "visible": true, "activities": [page façade navigation]},
    {"name": "1. Cours", "visible": false, "activities": [PDFs + H5P quiz section]},
    {"name": "2. Exercices", "visible": false, "activities": [PDFs + H5P entraînement]},
    {"name": "3. Quiz interactifs", "visible": false, "activities": [H5P par section]},
    {"name": "4. Révision", "visible": false, "activities": [H5P synthèse]},
    {"name": "5. Évaluation", "visible": false, "activities": [PDFs éval]}
  ]
}
```

### ÉTAPE 7 : PRÉVISUALISATION

**OBLIGATOIRE** avant de générer le .mbz :

```bash
python ".claude/skills/moodle-course-creator/scripts/preview_course.py" --config cours_config.json --open
```

Cette commande :
- Génère `preview_cours.html` dans le dossier
- Ouvre automatiquement dans le navigateur
- Affiche le rendu LaTeX avec KaTeX
- Permet de vérifier les questions H5P
- **Affiche la façade de navigation** en premier

**Demander à l'utilisateur de valider** la prévisualisation avant de continuer.

### ÉTAPE 8 : GÉNÉRER LE FICHIER .MBZ

Après validation de la prévisualisation :

```bash
python ".claude/skills/moodle-course-creator/scripts/generate_course_mbz.py" --config cours_config.json
```

### ÉTAPE 9 : RAPPORT FINAL

Afficher un résumé :
- Fichier généré et son emplacement
- **Page d'accueil (façade) générée** : `facade_cours.html`
- Nombre de sections
- Nombre de fichiers PDF inclus
- Nombre d'activités H5P (par type)
- Liste des liens dans la façade
- Instructions d'import dans Moodle

**Rappel important** : La section "🏠 Accueil" est la seule visible par défaut. Le professeur doit dévoiler progressivement les autres sections.

## Structure du cours généré

### Mode Simple
```
🏠 Accueil (VISIBLE) ★ FAÇADE
   └── Page: Navigation du cours
       ├── Liens vers tous les PDFs
       ├── Design responsive et attractif
       └── Vue d'ensemble pour les élèves

1. Cours (caché)
   └── PDFs du dossier Cours/

2. Exercices (caché)
   └── PDFs d'exercices

3. Évaluation (caché)
   └── Sujets d'évaluation
```

### Mode Enrichi
```
🏠 Accueil (VISIBLE) ★ FAÇADE
   └── Page: Navigation du cours
       ├── Section "📘 Cours" → liens PDFs
       ├── Section "✏️ Exercices" → liens fiches
       ├── Section "🎮 Quiz" → liens H5P
       ├── Section "🎬 Animations" → liens HTML
       ├── Section "📝 Évaluation" → liens éval
       └── Design cartes colorées par catégorie

1. Cours (caché)
   ├── PDFs du dossier Cours/
   └── H5P Quiz vocabulaire (section 1)

2. Exercices (caché)
   ├── PDFs d'exercices
   └── H5P Entraînement (multi-types)

3. Quiz interactifs (caché)
   ├── H5P Quiz Section 1 (définitions)
   ├── H5P Quiz Section 2 (propriétés)
   └── H5P Quiz Section 3 (applications)

4. Parcours de révision (caché) ★ GAME MAP
   └── H5P Game Map gamifié (6-10 étapes)
       ├── Types variés (QCM, DragText, Blanks, TrueFalse)
       ├── Progression pédagogique
       ├── 4 vies, feedbacks personnalisés
       └── Image de fond thématique

5. Évaluation (caché)
   └── Sujets d'évaluation
```

### Avantages de la façade

| Aspect | Bénéfice |
|--------|----------|
| **Navigation** | L'élève voit tout le contenu d'un coup, sans fouiller |
| **Motivation** | Design attractif qui donne envie d'explorer |
| **Autonomie** | L'élève choisit ce qu'il veut travailler |
| **Clarté** | Organisation visuelle par catégorie de contenu |
| **Accessibilité** | Point d'entrée unique, visible par défaut |

## Notes importantes

- **Pas de quiz Moodle natifs** → Problèmes de banque de questions
- **Tout en H5P** → Contenu embarqué, pas de dépendances
- **Tout caché** → Dévoilage progressif par le professeur
- **Import** → Dans Moodle : Administration > Restaurer > Importer le .mbz

## Types H5P avancés disponibles

| Type | Code | Usage |
|------|------|-------|
| Question Set | `questionset` | Quiz multi-questions |
| Single Choice | `singlechoiceset` | Quiz rapide |
| Fill Blanks | `blanks` | Textes à trous |
| Drag Words | `dragwords` | Mots à placer |
| Mark Words | `markwords` | Mots à sélectionner |
| True/False | `truefalse` | Vrai/Faux |
| Interactive Book | `interactivebook` | Livre complet |
| Column | `column` | Organisation contenus |

## Scripts disponibles

- `generate_course_mbz.py` - Générateur de backup Moodle
- `h5p_generator.py` - Générateur H5P basique
- `h5p_advanced_generator.py` - **Générateur H5P avancé** (tous types)
- `preview_course.py` - Prévisualisation HTML

---

## H5P Game Map - Parcours Gamifiés

### Présentation

Le **Game Map** H5P permet de créer des parcours pédagogiques gamifiés où les élèves progressent sur une carte en répondant à des défis. Idéal pour :
- Révision de chapitre
- Parcours de découverte
- Évaluation formative ludique

### Structure d'un Game Map

```
H5P Game Map
├── h5p.json (manifest avec dépendances)
└── content/
    ├── content.json (configuration complète)
    └── images/
        └── background.png (carte de fond)
```

### Types de contenus supportés dans les stages

**OBLIGATION : Varier les types !** Ne pas faire que des QCM.

| Type | Library H5P | Usage | Syntaxe spéciale |
|------|-------------|-------|------------------|
| QCM | `H5P.MultiChoice 1.16` | Questions à choix | - |
| Vrai/Faux | `H5P.TrueFalse 1.8` | Propriétés, définitions | - |
| Glisser-déposer | `H5P.DragText 1.10` | Vocabulaire, phrases | `*mot*` pour drag |
| Texte à trous | `H5P.Blanks 1.14` | Définitions, formules | `*mot*` pour trou |
| Choix unique série | `H5P.SingleChoiceSet 1.11` | Quiz rapide | - |

### Règle de variation des types

Pour un parcours de N étapes :
- **Max 40% QCM** (arrondi sup)
- **Min 1 DragText** (glisser-déposer)
- **Min 1 Blanks** (texte à trous)
- **Au moins 2 types différents** par parcours de 4+ étapes

### LaTeX dans H5P

Utiliser le format **MathJax** :
- Inline : `\(formule\)` → Ex: `\(u_n = 2n + 1\)`
- Display : `\[formule\]` → Ex: `\[\sum_{n=0}^{N} u_n\]`

**Ensembles** : `\(\mathbb{N}\)`, `\(\mathbb{R}\)`, `\(\mathbb{Z}\)`

### Feedbacks professionnels

**OBLIGATOIRE** : Chaque réponse doit avoir un feedback explicatif.

```json
{
  "answers": [
    {
      "text": "<div>Réponse A</div>",
      "correct": true,
      "tipsAndFeedback": {
        "chosenFeedback": "<div>Bravo ! Explication de pourquoi c'est correct.</div>"
      }
    },
    {
      "text": "<div>Réponse B</div>",
      "correct": false,
      "tipsAndFeedback": {
        "chosenFeedback": "<div>Non, car... Explication de l'erreur.</div>"
      }
    }
  ]
}
```

### Feedbacks globaux par plage de score

```json
"overallFeedback": [
  {"from": 0, "to": 50, "feedback": "Continue tes efforts !"},
  {"from": 51, "to": 99, "feedback": "Bien, mais revois ce point."},
  {"from": 100, "to": 100, "feedback": "Parfait !"}
]
```

### Structure d'un stage

```json
{
  "id": "uuid",
  "label": "Nom de l'étape",
  "telemetry": {
    "x": "50",      // Position X en %
    "y": "30",      // Position Y en %
    "width": "6",   // Largeur du hotspot
    "height": "10"  // Hauteur du hotspot
  },
  "neighbors": ["0", "2"],  // INDICES (pas UUIDs!) des stages adjacents
  "type": "stage",
  "canBeStartStage": false,
  "contentsList": [{ "contentType": {...} }]
}
```

**IMPORTANT** : Les `neighbors` sont des **indices string** ("0", "1", "2"...), pas des UUIDs !

### Dépendances h5p.json

```json
{
  "mainLibrary": "H5P.GameMap",
  "preloadedDependencies": [
    {"machineName": "H5P.GameMap", "majorVersion": "1", "minorVersion": "5"},
    {"machineName": "H5P.MultiChoice", "majorVersion": "1", "minorVersion": "16"},
    {"machineName": "H5P.DragText", "majorVersion": "1", "minorVersion": "10"},
    {"machineName": "H5P.Blanks", "majorVersion": "1", "minorVersion": "14"},
    {"machineName": "H5P.TrueFalse", "majorVersion": "1", "minorVersion": "8"}
  ]
}
```

### Localisation française complète

```json
"l10n": {
  "start": "Commencer",
  "continue": "Continuer",
  "restart": "Recommencer",
  "showSolutions": "Solutions",
  "completedMap": "Parcours terminé !",
  "confirmFinishHeader": "Terminer ?",
  "confirmAccessDeniedHeader": "Étape verrouillée",
  "yes": "Oui",
  "no": "Non"
}
```

### Parametres comportementaux (behaviour)

```json
"behaviour": {
  "enableRetry": true,
  "enableSolutionsButton": true,
  "lives": 4,                    // Nombre de vies (vide = illimite)
  "globalTimeLimit": null,       // Limite temps en secondes (optionnel)
  "finishScore": null,           // Score pour terminer (optionnel)
  "map": {
    "showLabels": true,          // Afficher noms des etapes
    "roaming": "complete",       // free|complete|strict
    "fog": "visited"             // none|visited|all
  }
}
```

**Modes de roaming :**
- `free` : Navigation libre sur toutes les etapes
- `complete` : Doit reussir une etape pour debloquer les voisines
- `strict` : Doit reussir avec score max pour avancer

**Modes de brouillard (fog) :**
- `none` : Tout visible
- `visited` : Seules les etapes visitees sont visibles
- `all` : Brouillard total au debut

### Parametres visuels (visual)

```json
"visual": {
  "stages": {
    "colorStage": "rgba(52, 152, 219, 0.85)",      // Bleu - non visite
    "colorStageLocked": "rgba(127, 140, 141, 0.7)", // Gris - verrouille
    "colorStageCleared": "rgba(46, 204, 113, 0.85)", // Vert - reussi
    "showScoreStars": "always"   // never|visited|always
  },
  "paths": {
    "displayPaths": true,
    "style": {
      "colorPath": "rgba(44, 62, 80, 0.6)",
      "colorPathCleared": "rgba(46, 204, 113, 0.7)",
      "pathWidth": "0.25",
      "pathStyle": "dotted"      // solid|dotted|dashed
    }
  },
  "misc": {
    "useAnimation": true
  }
}
```

### Ecrans de fin (endScreen)

```json
"endScreen": {
  "noSuccess": {
    "endScreenTextNoSuccess": "<p><strong>Echec</strong></p><p>Message d'encouragement...</p>",
    "endScreenMedia": {
      "path": "images/echec.png",
      "mime": "image/png"
    }
  },
  "success": {
    "endScreenTextSuccess": "<p><strong>Bravo !</strong></p><p>Message de victoire...</p>",
    "endScreenMedia": {
      "path": "images/succes.png",
      "mime": "image/png"
    }
  },
  "overallFeedback": [
    {"from": 0, "to": 40, "feedback": "Message score faible"},
    {"from": 41, "to": 70, "feedback": "Message score moyen"},
    {"from": 71, "to": 99, "feedback": "Message bon score"},
    {"from": 100, "to": 100, "feedback": "Message score parfait"}
  ]
}
```

### Structure d'un stage avec options avancees

```json
{
  "id": "uuid",
  "label": "Nom de l'etape",
  "telemetry": {
    "x": "50",      // Position X en %
    "y": "30",      // Position Y en %
    "width": "6",   // Largeur hotspot
    "height": "10"  // Hauteur hotspot
  },
  "neighbors": ["0", "2"],  // INDICES string des voisins
  "type": "stage",
  "canBeStartStage": false,
  "time": {},               // Limite temps par stage (optionnel)
  "accessRestrictions": {
    "allOrAnyRestrictionSet": "all",
    "restrictionSetList": [{
      "allOrAnyRestriction": "any",
      "restrictionList": [{"restrictionType": "totalScore"}]
    }]
  },
  "specialStageExtraLives": 0,  // Vies bonus gagnees
  "specialStageExtraTime": 0,   // Temps bonus gagne
  "contentsList": [...]
}
```

### Localisation francaise complete (l10n)

```json
"l10n": {
  "start": "Commencer",
  "continue": "Continuer",
  "restart": "Recommencer",
  "showSolutions": "Solutions",
  "completedMap": "Parcours termine !",
  "fullScoreButnoLivesLeft": "Score parfait mais plus de vies !",
  "confirmFinishHeader": "Terminer ?",
  "confirmFinishDialog": "Tu ne pourras plus explorer.",
  "confirmAccessDeniedHeader": "Etape verrouillee",
  "confirmAccessDeniedDialog": "Reussis les etapes precedentes.",
  "yes": "Oui",
  "no": "Non",
  "confirmGameOverHeader": "Game Over !",
  "confirmGameOverDialog": "Tu as perdu toutes tes vies !",
  "confirmTimeoutHeader": "Temps ecoule !",
  "confirmTimeoutDialog": "Le temps est ecoule.",
  "confirmScoreIncompleteHeader": "Score incomplet",
  "confirmIncompleteScoreDialogLostLife": "Score insuffisant, tu perds une vie.",
  "confirmFullScoreHeader": "Score parfait !",
  "confirmFullScoreDialog": "Bravo ! Tu peux continuer.",
  "ok": "OK",
  "noStages": "Aucune etape valide."
}
```

### Exemple de script generateur complet

Voir le skill `h5p-gamemap` (SKILL.md et `scripts/`) pour le générateur. Un bon parcours montre :
- **4 vies** avec perte a chaque erreur
- **Roaming "complete"** : doit reussir pour avancer
- Positions calibrees sur image de fond
- Types varies (QCM, DragText, Blanks, TrueFalse)
- Feedbacks personnalises par reponse
- Couleurs style aventure/tresor
- Interface 100% francais
- Melange aleatoire des options QCM
