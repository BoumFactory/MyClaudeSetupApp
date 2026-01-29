# /createGameMap - Création de parcours gamifiés H5P

## Description

Crée un parcours pédagogique gamifié au format H5P Game Map pour Moodle. Les élèves progressent sur une carte en répondant à des défis mathématiques.

**Peut fonctionner en deux modes** :
1. **Mode dossier** : Analyse un dossier de séquence pour créer un Game Map
2. **Mode ressource** : Analyse une ressource spécifique (PDF, LaTeX, etc.) pour en extraire du contenu

---

## ⚠️ RÈGLES CRITIQUES - À RESPECTER OBLIGATOIREMENT

### 1. PLUSIEURS QUESTIONS PAR ÉTAPE (OBLIGATOIRE)

**Chaque étape DOIT contenir 2-4 questions minimum** via QuestionSet.

```
INTERDIT : Une étape = une question simple (truefalse, multichoice seul)
OBLIGATOIRE : Une étape = QuestionSet avec 2-4 questions de types variés
EXCEPTION : SingleChoiceSet (qui enchaîne déjà plusieurs questions)
```

| Type d'étape | Structure OBLIGATOIRE |
|--------------|----------------------|
| Vocabulaire | QuestionSet [dragtext + truefalse + multichoice] |
| Propriétés | QuestionSet [truefalse + truefalse + multichoice] |
| Calculs | QuestionSet [multichoice + multichoice + truefalse] |
| Synthèse | QuestionSet [4-6 questions de types mixtes] |
| Quiz rapide | SingleChoiceSet [3-5 questions enchaînées] |

### 2. IMAGE DE FOND + PRÉVISUALISATION (OBLIGATOIRE)

**AVANT de générer le H5P final, TOUJOURS :**

1. Vérifier/créer l'image de fond (via `image-user` si nécessaire)
2. Lancer le script de prévisualisation des hotspots
3. Attendre la validation de l'utilisateur

```python
# ÉTAPE OBLIGATOIRE - NE JAMAIS SAUTER
python ".claude/skills/creer/moodle/h5p-gamemap/scripts/hotspot_preview.py" \
  --image "[dossier]/background.png" \
  --positions "[dossier]/preplan_gamemap.md" \
  --update-preplan
```

### 3. CONTENU ÉQUILIBRÉ (OBLIGATOIRE)

Pour un parcours de 8 étapes minimum :
- **Équations** : au moins 3 étapes dédiées
- **Inéquations** : au moins 2 étapes dédiées
- **Synthèse** : 1 étape avec questions sur TOUS les sujets

---

## Usage

```
/createGameMap [chemin] [--style STYLE] [--etapes N] [--output DOSSIER_SORTIE]
```

## Exemples

```bash
# Mode dossier : créer un Game Map dans le dossier Capsule_H5P
/createGameMap "1. Cours/1ere/Sequence-Suites_numeriques/Capsule_H5P/"

# Mode ressource : analyser un fichier LaTeX pour créer un Game Map
/createGameMap "1. Cours/1ere/Sequence-Suites_numeriques/Cours/enonce.tex"

# Mode ressource avec PDF
/createGameMap "1. Cours/2nde/Sequence-Vecteurs/Cours/cours_vecteurs.pdf" --output "./H5P/"

# Mode dossier complet : analyser toutes les ressources d'une séquence
/createGameMap "1. Cours/4eme/Sequence-Calcul_litteral/"

# Avec style spécifique
/createGameMap "1. Cours/2nde/Sequence-Vecteurs/H5P/" --style evaluation
```

---

## ARBRE DE DÉCISION : ANALYSE DES RESSOURCES

### Phase 1 : Identifier le type d'entrée

```
[Chemin fourni]
      │
      ├─► EST UN FICHIER ?
      │         │
      │         ├─► .tex  → Mode RESSOURCE_LATEX
      │         ├─► .pdf  → Mode RESSOURCE_PDF
      │         ├─► .html → Mode RESSOURCE_HTML
      │         ├─► .md   → Mode RESSOURCE_MARKDOWN
      │         └─► autre → ERREUR "Type non supporté"
      │
      └─► EST UN DOSSIER ?
                │
                ├─► Contient preplan_gamemap.md → Mode PREPLAN_EXISTANT
                ├─► Nom contient "H5P" ou "Capsule" → Mode DOSSIER_SORTIE
                ├─► Nom contient "Sequence-" ou "Chapitre-" → Mode DOSSIER_SEQUENCE
                └─► Autre → Scanner le contenu pour décider
```

### Phase 2 : Analyse selon le mode détecté

#### Mode RESSOURCE_LATEX (.tex)

```
[Fichier .tex]
      │
      ├─► Lire le contenu avec Read
      │
      ├─► Identifier les environnements bfcours :
      │     • \begin{definition} → DÉFINITIONS
      │     • \begin{propriete} → PROPRIÉTÉS
      │     • \begin{theoreme} → THÉORÈMES
      │     • \begin{exemple} → EXEMPLES
      │     • \begin{exercice} → EXERCICES
      │     • \begin{activite} → ACTIVITÉS
      │
      ├─► Extraire les formules LaTeX importantes :
      │     • $...$ ou \(...\) → inline
      │     • $$...$$ ou \[...\] → display
      │
      ├─► Construire le contenu pédagogique :
      │     • Résumer chaque notion clé
      │     • Identifier les concepts à évaluer
      │     • Repérer les erreurs typiques (pour distracteurs)
      │
      └─► Générer 6-10 questions variées basées sur ce contenu
```

**Mapping environnements → types de questions** :

| Environnement | Type de question suggéré |
|--------------|--------------------------|
| `definition` | `blanks` (texte à trous) |
| `propriete` | `truefalse` (vrai/faux) |
| `theoreme` | `multichoice` (QCM) |
| `exemple` | `multichoice` avec calcul |
| `exercice` | `multichoice` ou `blanks` |
| `vocabulaire` | `dragtext` (glisser-déposer) |

#### Mode RESSOURCE_PDF (.pdf)

```
[Fichier .pdf]
      │
      ├─► Lire avec Read (extraction texte + visuel)
      │
      ├─► Identifier la structure :
      │     • Titres et sous-titres
      │     • Encadrés/définitions
      │     • Exemples numérotés
      │     • Exercices
      │
      ├─► Si PDF de COURS :
      │     └─► Extraire notions pour créer des questions
      │
      ├─► Si PDF d'EXERCICES :
      │     └─► Adapter les exercices en format quiz
      │
      ├─► Si PDF d'ÉVALUATION :
      │     └─► Utiliser les questions existantes (avec reformulation)
      │
      └─► Générer les questions en évitant le copier-coller strict
```

#### Mode RESSOURCE_HTML (.html)

```
[Fichier .html]
      │
      ├─► Détecter le type :
      │     • Présentation reveal.js → Extraire les slides
      │     • Animation interactive → Analyser les concepts démontrés
      │     • Page de cours → Extraire le contenu textuel
      │
      └─► Adapter en questions selon le contenu visuel/interactif
```

#### Mode RESSOURCE_MARKDOWN (.md)

```
[Fichier .md]
      │
      ├─► Parser la structure Markdown
      │     • # Titres → Sections du parcours
      │     • > Citations → Définitions importantes
      │     • - Listes → Éléments à mémoriser
      │
      └─► Générer des questions par section
```

#### Mode DOSSIER_SEQUENCE

```
[Dossier Sequence-*]
      │
      ├─► Scanner les sous-dossiers :
      │     • Cours/ → Source principale
      │     • Exos/ ou Exercices/ → Questions d'entraînement
      │     • Eval*/ → Questions d'évaluation type
      │     • Activit*/ → Activités de découverte
      │
      ├─► Prioriser les sources :
      │     1. enonce.tex (cours principal)
      │     2. Autres .tex du dossier Cours/
      │     3. exercices.tex
      │     4. PDFs si pas de LaTeX
      │
      ├─► Créer le dossier Capsule_H5P/ s'il n'existe pas
      │
      └─► Synthétiser le contenu pour un parcours cohérent
```

### Phase 3 : Conception du parcours (AMBITIEUX, PAS UNE BATTERIE)

**OBJECTIF** : Créer une aventure pédagogique immersive, pas une série d'exercices.

```
[Contenu analysé]
      │
      ├─► RÈGLE ANTI-BATTERIE :
      │     • JAMAIS 2 mêmes types consécutifs
      │     • Alterner quiz et moments de "respiration"
      │     • Varier les formats de réponse (clic, glisser, compléter)
      │
      ├─► STRUCTURE NARRATIVE (10-15 étapes) :
      │
      │     ZONE DÉCOUVERTE (3-4 étapes)
      │     ├─► dragtext : vocabulaire
      │     ├─► blanks : définitions
      │     └─► truefalse : premières notions
      │
      │     [Étape respiration : rappel visuel, pas de quiz]
      │
      │     ZONE EXPLORATION (4-5 étapes)
      │     ├─► multichoice : premier calcul
      │     ├─► ★ défi bonus optionnel (+1 vie)
      │     ├─► singlechoiceset : mini-série (3 questions)
      │     └─► truefalse : propriété clé
      │
      │     [Checkpoint : encouragement + récap]
      │
      │     ZONE MAÎTRISE (3-4 étapes)
      │     ├─► multichoice : application
      │     ├─► questionset : mix de types
      │     └─► boss final : synthèse
      │
      ├─► EMBRANCHEMENTS (optionnel mais recommandé) :
      │     • Proposer 2 chemins vers le même objectif
      │     • "Forêt des Définitions" vs "Grotte des Calculs"
      │     • Permet de tester différemment selon préférence élève
      │
      ├─► NOMS D'ÉTAPES ÉVOCATEURS :
      │     ✗ "Question 1", "Question 2", "Question 3"
      │     ✓ "L'Entrée du Royaume", "Le Pont des Calculs", "La Tour du Théorème"
      │
      ├─► DÉFIS BONUS :
      │     • 1-2 étapes optionnelles sur le côté de la carte
      │     • Récompense : +1 vie ou message spécial
      │     • Plus difficiles mais gratifiants
      │
      └─► FEEDBACKS NARRATIFS :
            • Correct : "Bravo, aventurier ! [explication]"
            • Incorrect : "Attention au piège ! [explication de l'erreur]"
            • Indice : contextualisé dans l'univers ("Le sage te souffle...")
```

### Variété des interactions (OBLIGATOIRE)

| Interaction | Description | Quand l'utiliser |
|-------------|-------------|------------------|
| **Cliquer** | QCM, Vrai/Faux | Max 40% du parcours |
| **Glisser** | DragText | Vocabulaire, associations |
| **Compléter** | Blanks | Définitions, formules verbalisées |
| **Sélectionner** | MarkTheWords | Identifier des éléments dans un texte |
| **Ordonner** | SortParagraphs | Étapes d'une démonstration |
| **Série rapide** | SingleChoiceSet | Mini-quiz de 3-4 questions |
| **Mix** | QuestionSet | Boss final, récapitulatif |

### Étapes "respiration" (RECOMMANDÉ)

Insérer des étapes informatives (type `advancedtext`) :
- Après la zone Découverte : rappel visuel illustré
- Avant le boss final : checkpoint d'encouragement

```yaml
type: advancedtext
label: "La Halte du Voyageur"
content: |
  <h3>🗺️ Checkpoint !</h3>
  <p>Tu as parcouru la moitié du chemin. Rappelle-toi :</p>
  <ul>
    <li>Une suite est une <strong>fonction</strong> de ℕ vers ℝ</li>
    <li>La notation \((u_n)\) désigne la suite entière</li>
  </ul>
  <p><em>Continue, le sommet est proche !</em></p>
```

---

## Protocole d'exécution

### ÉTAPE 0 : CHARGER LE SKILL ET ANALYSER L'ENTRÉE

```
Lire : .claude/skills/creer/moodle/h5p-gamemap/SKILL.md
```

**IMPORTANT** : Mémoriser les RÈGLES CRITIQUES du skill :
1. Pas de LaTeX dans les réponses élèves (dragtext, blanks)
2. DragText : toujours une ligne finale sans trou
3. Validation visuelle des positions obligatoire

**Déterminer le MODE** selon l'arbre de décision (voir ci-dessus) :
- `RESSOURCE_LATEX` | `RESSOURCE_PDF` | `RESSOURCE_HTML` | `RESSOURCE_MARKDOWN`
- `DOSSIER_SEQUENCE` | `DOSSIER_SORTIE` | `PREPLAN_EXISTANT`

### ÉTAPE 1 : EXTRAIRE LE CONTENU PÉDAGOGIQUE

#### Si mode RESSOURCE_* (fichier unique)

1. **Lire le fichier source** avec Read
2. **Analyser selon le type** (voir arbre de décision Phase 2)
3. **Construire un résumé structuré** :

```markdown
## Analyse de la ressource : [nom_fichier]

### Notions identifiées
1. [Notion 1] - définition/propriété/théorème
2. [Notion 2] - ...

### Formules clés
- \(formule_1\) : description
- \(formule_2\) : description

### Points à évaluer
- [ ] Compréhension du vocabulaire
- [ ] Application des formules
- [ ] Distinction cas particuliers
- [ ] Erreurs typiques à éviter

### Questions suggérées
| Type | Notion ciblée | Difficulté |
|------|--------------|------------|
| blanks | Définition de [X] | Facile |
| truefalse | Propriété de [Y] | Moyen |
| multichoice | Calcul avec [Z] | Moyen |
```

4. **Déterminer le dossier de sortie** :
   - Si `--output` spécifié → utiliser ce dossier
   - Sinon → créer `Capsule_H5P/` à côté du fichier source

#### Si mode DOSSIER_SEQUENCE

1. **Scanner les sous-dossiers** (Cours/, Exos/, etc.)
2. **Lire les fichiers prioritaires** :
   - `Cours/enonce.tex` en premier
   - Autres `.tex` ensuite
   - PDFs si pas de LaTeX
3. **Synthétiser** les contenus de toutes les sources
4. **Dossier de sortie** : `[sequence]/Capsule_H5P/`

#### Si mode PREPLAN_EXISTANT

Proposer via AskUserQuestion :

```
Je détecte un préplan existant : preplan_gamemap.md

1. Générer le H5P depuis ce préplan (Recommandé)
2. Modifier le préplan existant
3. Créer un nouveau préplan (écrase l'ancien)
```

### ÉTAPE 2 : INFÉRER NIVEAU ET THÈME DEPUIS LE CHEMIN

**Pattern de chemin attendu** :
```
1. Cours/[NIVEAU]/Sequence-[THEME]/...
```

**Extraction automatique** :

| Segment chemin | Niveau détecté |
|----------------|----------------|
| `/6eme/` | 6eme |
| `/5eme/` | 5eme |
| `/4eme/` | 4eme |
| `/3eme/` | 3eme |
| `/2nde/` | 2nde |
| `/1ere/` | 1ere |
| `/Terminale/` ou `/Tle/` | Terminale |

**Thème** : Extraire depuis `Sequence-[THEME]` ou `Chapitre-[THEME]`
- `Sequence-Suites_numeriques` → "Suites numériques"
- `Sequence-Vecteurs` → "Vecteurs"
- `Chapitre-Probabilites` → "Probabilités"

**Si le chemin ne permet pas d'inférer** → Demander à l'utilisateur (rare)

### ÉTAPE 3 : DEMANDER UNIQUEMENT LE STYLE (si non spécifié)

**Une seule question** via AskUserQuestion :

```
Question: Quel style de parcours ?

Options:
1. Aventure (Recommandé) - 4 vies, doit réussir pour avancer
2. Révision - Vies illimitées, navigation libre
3. Évaluation - 1 vie, mode strict
4. Découverte - Navigation libre, brouillard total
```

### ÉTAPE 4 : CRÉER LE PRÉPLAN

1. Utiliser le template `.claude/skills/creer/moodle/h5p-gamemap/templates/PREPLAN_TEMPLATE.md`
2. Pré-remplir avec :
   - Titre généré depuis le thème
   - Niveau et thème inférés
   - Style choisi
   - **5-7 étapes** avec questions adaptées au thème
3. **APPLIQUER LES RÈGLES CRITIQUES** :
   - **dragtext/blanks** : mots à compléter en texte simple, SANS LaTeX
   - **dragtext** : ajouter une ligne finale sans trou
4. Écrire `preplan_gamemap.md` dans le dossier cible

**Informer l'utilisateur** :

```
Préplan créé : [chemin]/preplan_gamemap.md

Vous pouvez :
- Le modifier pour ajuster les questions
- Ou relancer /createGameMap pour générer directement le H5P
```

### ÉTAPE 5 : GÉRER L'IMAGE DE FOND (OBLIGATOIRE)

**Chercher dans le dossier** : `*.png`, `background.*`, `carte.*`, `map.*`

#### Si une image est trouvée

→ Demander à l'utilisateur via AskUserQuestion :

```
Question: Une image de fond existe déjà. Que souhaitez-vous faire ?

Options:
1. Utiliser l'image existante (Recommandé) - [nom_fichier.png]
2. Générer une nouvelle image - L'agent image-user créera une carte thématique
```

#### Si aucune image n'est trouvée

→ Demander à l'utilisateur via AskUserQuestion :

```
Question: Aucune image de fond trouvée. Que souhaitez-vous faire ?

Options:
1. Générer une image thématique (Recommandé) - L'agent image-user créera une carte d'aventure
2. Continuer sans image - Le Game Map utilisera un fond neutre
3. Je fournirai une image plus tard - Arrêter ici pour que je puisse en ajouter une
```

#### Génération d'image via agent image-user

**Si l'utilisateur choisit de générer une image**, lancer l'agent `image-user` :

```python
Task(
    subagent_type="image-user",
    prompt=f"""
    Génère une image de fond pour un Game Map H5P.

    **Chemin du skill** : `.claude/skills/creer/media/image-generator/scripts/generate_image.py`
    **Dossier de sortie** : `{dossier_sortie}`
    **Nom du fichier** : `background_{theme_slug}.png`
    **Dimensions** : 1920x1080

    **Contexte pédagogique** :
    - Niveau : {niveau}
    - Thème : {theme}

    **Style demandé** :
    - Carte d'aventure/fantastique style jeu de rôle
    - Un chemin sinueux traversant un paysage thématique
    - Points d'étape circulaires visibles le long du chemin (pour placer les hotspots)
    - Couleurs accueillantes et lumineuses
    - PAS de texte ni de formules mathématiques sur l'image
    - Ambiance adaptée à des élèves de {age_eleves} ans

    Retourne le chemin complet du fichier créé.
    """
)
```

**Attendre la fin de l'agent** avant de continuer à l'étape suivante.

### ÉTAPE 6 : VALIDATION VISUELLE DES POSITIONS (CRITIQUE - NE JAMAIS SAUTER)

**⚠️ ABSOLUMENT OBLIGATOIRE avant génération du H5P final - MÊME EN SOUS-AGENT !**

Cette étape permet à l'utilisateur de repositionner visuellement les hotspots sur la carte.
Sans cette étape, les points risquent de ne pas être alignés avec l'image de fond.

**1. Vérifier que l'image existe**

```python
import os
background = "[chemin]/background.png"
if not os.path.exists(background):
    # ERREUR : Impossible de continuer sans image
    raise FileNotFoundError("Image de fond manquante - utilisez /createImage d'abord")
```

**2. Lancer l'outil de prévisualisation**

```bash
python ".claude/skills/creer/moodle/h5p-gamemap/scripts/hotspot_preview.py" \
  --image "[chemin]/background.png" \
  --positions "[chemin]/preplan_gamemap.md" \
  --update-preplan
```

**3. Informer l'utilisateur via message direct**

```
🗺️ L'outil de positionnement des hotspots est maintenant ouvert.

📍 Glissez-déposez les marqueurs pour les aligner avec votre carte.
✅ Cliquez sur "Valider" quand c'est terminé.
❌ Cliquez sur "Annuler" pour arrêter la génération.
```

**4. Attendre la validation**

```python
import time
done_file = "[chemin]/positions_corrected.json.done"
cancel_file = "[chemin]/positions_corrected.json.cancelled"

while True:
    if os.path.exists(done_file):
        print("✅ Positions validées par l'utilisateur")
        break
    if os.path.exists(cancel_file):
        print("❌ Génération annulée par l'utilisateur")
        return  # ARRÊTER ICI
    time.sleep(1)
```

**5. Si positions validées** : Le préplan est automatiquement mis à jour avec les nouvelles coordonnées

**⚠️ ATTENTION SOUS-AGENTS :**
- Cette étape est INTERACTIVE et nécessite l'utilisateur
- NE PAS sauter cette étape même si vous êtes un sous-agent
- Si le script de prévisualisation n'existe pas, INFORMER l'utilisateur et proposer de continuer sans validation

### ÉTAPE 7 : GÉNÉRER LE H5P

**Après validation des positions** :

```bash
python ".claude/skills/creer/moodle/h5p-gamemap/scripts/generate_gamemap.py" \
  --preplan [chemin]/preplan_gamemap.md \
  --output [chemin]/parcours_[theme].h5p \
  --background [chemin]/background.png
```

### ÉTAPE 8 : RAPPORT FINAL

```markdown
## Parcours H5P créé

**Fichier** : `[chemin]/parcours_[theme].h5p`
**Préplan** : `[chemin]/preplan_gamemap.md`

**Configuration** :
- Niveau : [niveau]
- Thème : [thème]
- Style : [style]
- Étapes : [N]

**Import dans Moodle** :
1. Cours → Mode édition → Ajouter activité H5P
2. Téléverser le fichier .h5p
```

---

## Règles de rédaction des questions

### Pour dragtext (glisser-déposer)

```markdown
**CORRECT** :
Une suite est *croissante* si elle augmente.
Elle est *décroissante* si elle diminue.
Une suite *constante* a tous ses termes égaux.

Connais-tu bien ton vocabulaire ?   ← LIGNE FINALE SANS TROU
```

```markdown
**INCORRECT** :
La suite est définie sur *\(\mathbb{N}\)*.   ← LaTeX dans le trou !
```

### Pour blanks (texte à trous)

```markdown
**CORRECT** :
La notation \((u_n)_{n \in \mathbb{N}}\) désigne *la suite entière*.
Le terme \(u_5\) est de *rang* 5, c'est le *6ème* terme.
```

```markdown
**INCORRECT** :
Le terme général s'écrit *\(u_n = 2n+1\)*.   ← LaTeX dans le trou !
```

---

## Logique de détection automatique

### Détection du préplan

```python
# Pseudo-code
preplan_path = dossier / "preplan_gamemap.md"
if preplan_path.exists():
    # Proposer: générer depuis préplan OU régénérer
else:
    # Créer nouveau préplan
```

### Extraction niveau/thème

```python
# Patterns regex sur le chemin
niveau_patterns = {
    r'/6eme/': '6eme',
    r'/5eme/': '5eme',
    r'/4eme/': '4eme',
    r'/3eme/': '3eme',
    r'/2nde/': '2nde',
    r'/1ere/': '1ere',
    r'/[Tt]erminale/': 'Terminale',
    r'/[Tt]le/': 'Terminale'
}

theme_pattern = r'Sequence-([^/]+)'  # ou Chapitre-
# Nettoyer: underscores → espaces, capitalisation
```

---

## Types de questions supportés

| Type | Code | Usage | Règles spéciales |
|------|------|-------|------------------|
| QCM | `multichoice` | Questions à choix | LaTeX OK partout |
| Vrai/Faux | `truefalse` | Propriétés | LaTeX OK partout |
| Glisser-déposer | `dragtext` | Vocabulaire | **Pas de LaTeX dans `*mots*`** + ligne finale |
| Texte à trous | `blanks` | Définitions | **Pas de LaTeX dans `*mots*`** |
| Quiz rapide | `singlechoiceset` | 2-5 QCM enchaînés | LaTeX OK partout |
| Set de questions | `questionset` | Mix de types | Selon le type |

---

## Styles prédéfinis

| Style | Vies | Roaming | Fog |
|-------|------|---------|-----|
| `aventure` | 4 | complete | visited |
| `revision` | illimité | free | none |
| `evaluation` | 1 | strict | visited |
| `decouverte` | illimité | free | all |

---

## Workflow complet

```
/createGameMap [chemin]
     │
     ├─► PHASE ANALYSE
     │     ├─► Détecter le mode (fichier/dossier/préplan)
     │     ├─► Extraire le contenu pédagogique
     │     └─► Construire le résumé structuré
     │
     ├─► PHASE CONFIGURATION
     │     ├─► Inférer niveau/thème du chemin
     │     ├─► Demander style (si non spécifié)
     │     └─► Déterminer dossier de sortie
     │
     ├─► PHASE GÉNÉRATION PRÉPLAN
     │     ├─► Mapper contenu → types de questions
     │     ├─► Créer préplan (avec règles critiques)
     │     └─► Respecter la règle des 40% QCM
     │
     ├─► PHASE VISUELLE
     │     ├─► Vérifier/générer image de fond
     │     │       └─► /createImage si manquante
     │     ├─► Lancer hotspot_preview.py
     │     └─► Attendre validation utilisateur
     │
     ├─► PHASE COMPILATION
     │     ├─► Générer le H5P final
     │     └─► Vérifier l'intégrité du fichier
     │
     └─► PHASE RAPPORT
           └─► Afficher résumé et instructions import
```

---

## Exemples de transformation ressource → questions

### Exemple 1 : Définition LaTeX → Question blanks

**Source (enonce.tex)** :
```latex
\begin{definition}[Suite numérique]
Une \motcle{suite numérique} est une fonction de $\mathbb{N}$ (ou d'une partie de $\mathbb{N}$) vers $\mathbb{R}$.
On note $(u_n)_{n \in \mathbb{N}}$ ou simplement $(u_n)$.
\end{definition}
```

**Question générée** :
```yaml
type: blanks
question: |
  Une suite numérique est une *fonction* de \(\mathbb{N}\) vers \(\mathbb{R}\).
  On la note \((u_n)_{n \in \mathbb{N}}\) ou simplement *la suite* \((u_n)\).
feedback: "La suite est bien une fonction qui à chaque entier associe un réel."
```

### Exemple 2 : Propriété LaTeX → Question truefalse

**Source (enonce.tex)** :
```latex
\begin{propriete}
Une suite arithmétique $(u_n)$ de raison $r > 0$ est strictement croissante.
\end{propriete}
```

**Question générée** :
```yaml
type: truefalse
question: "Une suite arithmétique de raison positive est toujours croissante."
correct: true
feedback_correct: "Exact ! Si r > 0, alors u_{n+1} = u_n + r > u_n."
feedback_incorrect: "C'est pourtant vrai : ajouter un nombre positif augmente la valeur."
```

### Exemple 3 : Exemple calculatoire → Question multichoice

**Source (enonce.tex)** :
```latex
\begin{exemple}
Soit $(u_n)$ définie par $u_n = 2n + 3$.
Calculons $u_5$ : $u_5 = 2 \times 5 + 3 = 13$.
\end{exemple}
```

**Question générée** :
```yaml
type: multichoice
question: |
  Soit \((u_n)\) définie par \(u_n = 2n + 3\).
  Que vaut \(u_4\) ?
options:
  - text: "\\(11\\)"
    correct: true
    feedback: "Bravo ! u_4 = 2×4 + 3 = 8 + 3 = 11"
  - text: "\\(10\\)"
    correct: false
    feedback: "Non, tu as oublié d'ajouter 3."
  - text: "\\(9\\)"
    correct: false
    feedback: "Non, tu as peut-être confondu avec 2×4 + 1."
  - text: "\\(14\\)"
    correct: false
    feedback: "Non, tu as calculé u_5, pas u_4."
```

### Exemple 4 : Vocabulaire → Question dragtext

**Source (analyse du cours)** :
```
Termes clés identifiés : croissante, décroissante, monotone, bornée, convergente
```

**Question générée** :
```yaml
type: dragtext
text: |
  Une suite est *croissante* si chaque terme est supérieur au précédent.
  Elle est *décroissante* si chaque terme est inférieur au précédent.
  Une suite croissante ou décroissante est dite *monotone*.

  As-tu bien retenu ces définitions ?
feedback: "Parfait ! Tu maîtrises le vocabulaire des suites."
```

### Exemple 5 : Exercice PDF → Question adaptée

**Source (PDF exercices, exercice 3)** :
```
Calculer les 5 premiers termes de la suite (u_n) définie par u_0 = 2 et u_{n+1} = 3u_n - 1.
```

**Adaptation pour Game Map** :
```yaml
type: singlechoiceset
questions:
  - question: "Avec u_0 = 2 et u_{n+1} = 3u_n - 1, que vaut u_1 ?"
    options: ["5", "6", "4", "7"]
    correct: 0
  - question: "Et u_2 ?"
    options: ["14", "13", "15", "12"]
    correct: 0
  - question: "La suite est-elle croissante ?"
    options: ["Oui, car chaque terme est plus grand", "Non, elle est décroissante"]
    correct: 0
```

---

## Exemple de parcours complet (12 étapes)

### "L'Archipel des Suites" - Niveau 1ère

```
┌────────────────────────────────────────────────────────────────────┐
│                         🏝️ CARTE DU PARCOURS                       │
│                                                                    │
│    [1]━━━[2]━━━[3]                                                 │
│              ↘                                                     │
│               [4 Respiration]                                      │
│              ↙         ↘                                          │
│         [5]━━━━━━━━━━━[6 ★ Bonus]                                  │
│          ↓                                                         │
│         [7]━━━[8]━━━[9 Checkpoint]                                 │
│                        ↓                                           │
│                      [10]━━━[11]━━━[12 🏆]                         │
└────────────────────────────────────────────────────────────────────┘
```

| # | Étape | Zone | Type | Contenu |
|---|-------|------|------|---------|
| 1 | 🚢 Le Départ | Découverte | `dragtext` | "Une *suite* est une *fonction* de ℕ vers ℝ." |
| 2 | 📜 Le Parchemin | Découverte | `blanks` | Compléter la notation (u_n)_{n∈ℕ} |
| 3 | ⚖️ La Balance | Découverte | `truefalse` | "u_5 est le 5ème terme" (faux : c'est le 6ème si u_0 existe) |
| 4 | 🏕️ *Le Bivouac* | Respiration | `advancedtext` | Récap illustré + encouragement |
| 5 | 🌉 Le Pont | Exploration | `multichoice` | Calculer u_4 pour u_n = 2n+1 |
| 6 | 🗝️ *La Grotte Secrète* ★ | Bonus | `multichoice` | Défi difficile → +1 vie si réussi |
| 7 | 🔢 La Cascade | Exploration | `singlechoiceset` | 3 calculs de termes enchaînés |
| 8 | 📐 Le Théorème | Exploration | `truefalse` | Propriété de monotonie |
| 9 | ⛺ *Checkpoint* | Respiration | `advancedtext` | "Tu approches du sommet !" |
| 10 | 🏔️ L'Ascension | Maîtrise | `multichoice` | Application : sens de variation |
| 11 | ⚔️ L'Épreuve | Maîtrise | `questionset` | Mix 4 questions (tous types) |
| 12 | 🏆 Le Trésor | Boss | `multichoice` | Question de synthèse |

### Caractéristiques de ce parcours

- **12 étapes** dont 2 respirations et 1 bonus
- **6 types différents** : dragtext, blanks, truefalse, multichoice, singlechoiceset, questionset, advancedtext
- **Jamais 2 consécutifs identiques**
- **Noms évocateurs** avec emojis
- **Embranchement** : étape 6 optionnelle sur le côté
- **Progression narrative** : métaphore du voyage/exploration

---

## Gestion des cas particuliers

### Ressource sans structure claire

Si le fichier analysé n'a pas de structure identifiable :
1. **Demander à l'utilisateur** le thème principal
2. **Proposer un préplan générique** avec types variés
3. **Suggérer de compléter manuellement** les questions

### Ressource courte (< 5 notions)

- Générer un parcours de **8-10 étapes** quand même
- **Approfondir** chaque notion avec plusieurs angles :
  - Définition → blanks
  - Propriété → truefalse
  - Application simple → multichoice
  - Application avancée → singlechoiceset
- Ajouter des étapes respiration pour la fluidité

### Ressource longue (> 15 notions)

- **Sélectionner les 12-15 notions clés**
- Proposer de créer **plusieurs Game Maps** (un par sous-thème)
- Ou créer un **parcours synthèse** ambitieux avec les points essentiels

---

## Voir aussi

- `.claude/skills/creer/moodle/h5p-gamemap/SKILL.md`
- `.claude/skills/creer/moodle/h5p-gamemap/ETAT_DES_LIEUX.md`
