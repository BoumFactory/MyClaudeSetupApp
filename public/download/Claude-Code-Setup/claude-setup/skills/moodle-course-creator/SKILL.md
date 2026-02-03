# Skill: Moodle Course Creator

Skill pour creer des cours Moodle complets avec support H5P avance : parcours gamifies, quiz varies, capsules interactives.

## Commande associee

```
/moodleise <chemin_dossier_sequence>
```

## Quand utiliser ce skill

- Creer un cours Moodle a partir de ressources pedagogiques
- Generer des parcours interactifs gamifies
- Creer des quiz H5P avec LaTeX
- Packager des contenus pour import Moodle

## IMPORTANT : H5P vs Quiz Moodle

**Privilegier H5P** : les quiz Moodle natifs posent des problemes de banque de questions a l'import. Les H5P sont autonomes et portables.

---

## Types H5P pour Parcours Gamifies

### Course Presentation (RECOMMANDE pour parcours)
- Diaporama interactif avec quiz integres
- Image de fond + etapes avec quiz varies
- Tous types de quiz supportes
- **Script** : `h5p_course_presentation.py`

### Branching Scenario
- Parcours a embranchements
- Ideal pour escape games, simulations
- Choix multiples menant a differentes branches

### Interactive Book
- Livre numerique avec chapitres
- Cours complets avec exercices integres

### Image Hotspots (LIMITE)
- Points cliquables sur image
- **ATTENTION** : Contenu statique uniquement (texte, image, video)
- **NE PEUT PAS** contenir de quiz interactifs !

---

## Types de Quiz Disponibles

| Type | Code | Syntaxe speciale |
|------|------|------------------|
| QCM | `multichoice` | `options: []`, `correct: index` |
| Vrai/Faux | `truefalse` | `correct: True/False` |
| Texte a trous | `blanks` | `*reponse*` dans le texte |
| Mots a glisser | `dragwords` | `*mot*` dans le texte |
| Selection de mots | `markwords` | `*mot*` a selectionner |
| Quiz rapide | `singlechoiceset` | Premiere option = correcte |

---

## Support LaTeX/MathJax

### Syntaxe dans le code Python
```python
# Utiliser des raw strings ou doubler les backslashes
question = "Calculer \\\\(x^2\\\\) pour x=3"
# OU
question = r"Calculer \\(x^2\\) pour x=3"
```

### Rendu dans H5P
- `\\(formule\\)` : inline
- `\\[formule\\]` : block
- Les `$` sont convertis automatiquement

---

## Scripts Disponibles

| Script | Usage |
|--------|-------|
| `h5p_course_presentation.py` | **Parcours gamifies** |
| `h5p_generator_v2.py` | Quiz avec metadonnees |
| `h5p_advanced_generator.py` | Tous types avances |
| `h5p_image_hotspots.py` | Image avec hotspots (statique) |
| `generate_course_mbz.py` | Package Moodle complet |

---

## Creer un Parcours Gamifie

### Exemple complet

```python
from h5p_course_presentation import H5PCoursePresentation

stages = [
    {
        "title": "Etape 1",
        "intro": "Introduction de l'etape",
        "quiz_type": "multichoice",
        "question": "Question avec \\\\(LaTeX\\\\) ?",
        "options": ["Reponse A", "Reponse B", "Reponse C"],
        "correct": 0,  # Index de la bonne reponse
        "feedback": "Explication"
    },
    {
        "title": "Etape 2",
        "intro": "Vrai ou faux ?",
        "quiz_type": "truefalse",
        "question": "Affirmation a juger",
        "correct": True,
        "feedback": "Explication"
    },
    {
        "title": "Etape 3",
        "intro": "Completez les trous",
        "quiz_type": "blanks",
        "text": "Le resultat est *42* et la reponse est *oui*.",
        "feedback": "Bien joue !"
    },
    {
        "title": "Etape 4",
        "intro": "Glissez les mots",
        "quiz_type": "dragwords",
        "text": "Une *suite* est une *fonction* de N vers R.",
        "feedback": "Exact !"
    }
]

h5p = H5PCoursePresentation.create_gamified_course(
    title="Mon Parcours",
    background_image="chemin/vers/image.png",
    stages=stages
)

with open("parcours.h5p", "wb") as f:
    f.write(h5p)
```

---

## Integration avec image-generator

Pour creer une image de fond thematique :

```bash
python ".claude/skills/creer/media/image-generator/scripts/generate_image.py" \\
  --prompt "Illustration d'une echelle a gravir avec des etapes numerotees, style gamifie, fond colore" \\
  --type "illustration" \\
  --output "image_parcours.png"
```

Puis utiliser l'image dans le parcours :

```python
H5PCoursePresentation.create_gamified_course(
    title="L'Ascension",
    background_image="image_parcours.png",
    stages=[...]
)
```

---

## Workflow : Capsule Complete

```
1. Definir les objectifs pedagogiques
2. Lister les notions a evaluer
3. Creer les etapes avec quiz varies :
   - QCM pour les definitions
   - V/F pour les proprietes
   - Texte a trous pour le vocabulaire
   - Drag&Drop pour les associations
4. [Optionnel] Generer image de fond avec image-generator
5. Generer le H5P avec le script
6. Tester dans Moodle
```

---

## References

Voir le dossier `references/` :
- `h5p-all-types.md` : Liste complete des types H5P
- `h5p-course-presentation.md` : Details Course Presentation
- `h5p-image-hotspots.md` : Details Image Hotspots (et limites)
- `latex-h5p-guide.md` : Guide LaTeX
- `integration-image-generator.md` : Creer des images

---

## Strategie "Front" pour Moodle

**Principe** : Cacher les ressources standards Moodle et presenter un H5P style comme page d'accueil du cours.

### Avantages
- Presentation visuelle attrayante
- Navigation guidee pour les eleves
- Liens clairs vers les ressources
- Experience gamifiee

### Implementation
1. Creer un Course Presentation avec image de fond thematique
2. Ajouter des zones cliquables (hotspots simules) vers :
   - Les quiz (slides internes)
   - Les documents (liens externes)
   - Les activites Moodle
3. Cacher les sections standards dans Moodle
4. Mettre le H5P en evidence comme "portail" du cours

---

## Exemple : Capsule Suites Numeriques

Voir `1. Cours/1ere/Sequence-Suites_numeriques/Capsule_H5P/` :
- `parcours_suites.h5p` : Parcours complet (echelle + 7 quiz + navigation)
- `echelle_v2.png` : Image de fond (echelle a gravir)
- `generer_parcours_hotspot.py` : Script de generation

### Structure du parcours
- Slide 1 : Image echelle avec 7 boutons colores cliquables
- Slides 2-8 : Un quiz par etape (QCM, V/F, trous, drag&drop)
- Slide 9 : Victoire
- Navigation : clic etape -> quiz -> bouton retour

---

## Intégration Game Map H5P (OBLIGATOIRE en mode Enrichi/Complet)

**RÈGLE** : Tout cours Moodle en mode **Enrichi** ou **Parcours complet** doit inclure **au moins un Game Map H5P** bien fourni.

### Pourquoi un Game Map ?

Le Game Map offre une expérience ludique et engageante :
- Progression visuelle sur une carte
- Système de vies/déblocage motivant
- Variété des types de questions
- Feedback immédiat et personnalisé

### Comment l'intégrer ?

**L'agent principal ne génère PAS le Game Map lui-même.** Il délègue à un agent `meta-high` qui utilise le skill `h5p-gamemap`.

#### Workflow de délégation

```python
# L'agent moodle-course-creator fait :
Task(
    subagent_type="meta-high",
    prompt="""
    Utilise le skill h5p-gamemap pour créer un parcours gamifié complet.

    **Contexte du cours** :
    - Niveau : [NIVEAU]
    - Thème : [THEME]
    - Dossier de sortie : [DOSSIER]/Capsule_H5P/

    **Contenu pédagogique** (extrait des sources LaTeX) :
    [Résumé des notions clés, définitions, théorèmes, exemples]

    **Exigences** :
    - 6 à 10 étapes de progression
    - Types variés : max 40% QCM, min 1 DragText, min 1 Blanks
    - Feedbacks explicatifs pour chaque réponse
    - Style "aventure" avec 4 vies
    - Image de fond thématique (utiliser image-generator si besoin)
    - Préplan + validation + génération H5P

    Retourne le chemin du fichier .h5p généré.
    """
)
```

#### Intégration du résultat

Une fois le Game Map généré, l'agent principal :
1. Récupère le fichier `.h5p` du dossier `Capsule_H5P/`
2. L'ajoute dans la section "Quiz interactifs" ou "Révision"
3. Le référence dans la configuration JSON du cours

```json
{
  "sections": [
    {
      "name": "5. Parcours de révision",
      "visible": false,
      "activities": [
        {
          "type": "h5p",
          "name": "Parcours - [THEME]",
          "file": "Capsule_H5P/gamemap_[theme].h5p",
          "description": "Parcours gamifié de révision"
        }
      ]
    }
  ]
}
```

### Contenu du Game Map (AMBITIEUX)

**OBJECTIF** : Un vrai parcours d'aventure pédagogique, PAS des exercices en batterie.

| Élément | Spécification |
|---------|---------------|
| **Étapes** | 10-15 (parcours riche) |
| **Types de questions** | ≥5 types différents, jamais 2 identiques consécutifs |
| **Feedbacks** | Personnalisés et explicatifs (pas juste "correct/incorrect") |
| **Vies** | 4 (assez pour explorer, pas trop pour garder le challenge) |
| **Image de fond** | Carte thématique immersive (île, montagne, château, etc.) |
| **Écrans fin** | Succès/échec avec messages narratifs |

### Structure narrative du parcours

```
┌─────────────────────────────────────────────────────────────────┐
│  ZONE 1 : DÉCOUVERTE (3-4 étapes)                               │
│  - Vocabulaire et définitions                                   │
│  - Types doux : dragtext, blanks                                │
│  - Feedbacks encourageants, indices généreux                    │
├─────────────────────────────────────────────────────────────────┤
│  ZONE 2 : EXPLORATION (4-5 étapes)                              │
│  - Propriétés et premiers calculs                               │
│  - Types variés : truefalse, multichoice simples                │
│  - Introduction d'un "défi bonus" optionnel                     │
├─────────────────────────────────────────────────────────────────┤
│  ZONE 3 : MAÎTRISE (3-4 étapes)                                 │
│  - Applications et problèmes                                    │
│  - Types complexes : singlechoiceset, questionset               │
│  - Embranchements possibles (chemin facile/difficile)           │
├─────────────────────────────────────────────────────────────────┤
│  BOSS FINAL (1-2 étapes)                                        │
│  - Synthèse des notions                                         │
│  - Défi récapitulatif multi-questions                           │
│  - Récompense narrative ("Tu as maîtrisé les suites !")         │
└─────────────────────────────────────────────────────────────────┘
```

### Mécaniques anti-batterie

Pour éviter l'effet "exercices en série" :

1. **Jamais 2 mêmes types consécutifs** : QCM → DragText → TrueFalse → Blanks → QCM...

2. **Étapes "respiration"** :
   - Étape informative (AdvancedText) entre deux défis
   - Rappel de cours illustré avant un calcul

3. **Embranchements narratifs** :
   - "Choisis ton chemin : la Forêt des Définitions ou la Grotte des Calculs"
   - Les deux mènent au même point mais testent différemment

4. **Défis bonus optionnels** :
   - Étapes secondaires qui donnent des vies supplémentaires
   - Accessibles mais pas obligatoires

5. **Progression de difficulté visible** :
   - Étapes colorées différemment selon la zone
   - Noms évocateurs ("Le Pont des Propriétés", "La Tour du Théorème")

6. **Variété des formats de réponse** :
   - Pas que du clic : glisser, compléter, ordonner, sélectionner
   - Mélanger texte et formules dans les interactions

### Exemple de parcours type (12 étapes)

| # | Nom | Zone | Type | Contenu |
|---|-----|------|------|---------|
| 1 | L'Entrée du Royaume | Découverte | `dragtext` | Vocabulaire de base |
| 2 | La Fontaine aux Définitions | Découverte | `blanks` | Compléter une définition |
| 3 | Le Carrefour | Découverte | `truefalse` | Vrai/Faux sur les notations |
| 4 | *Rappel illustré* | - | `advancedtext` | Récap visuel (pas de quiz) |
| 5 | Le Pont des Calculs | Exploration | `multichoice` | Premier calcul simple |
| 6 | La Grotte Secrète ★ | Exploration | `multichoice` | Défi bonus (+1 vie) |
| 7 | Les Escaliers | Exploration | `singlechoiceset` | 3 questions enchaînées |
| 8 | Le Belvédère | Exploration | `truefalse` | Propriété importante |
| 9 | *Checkpoint* | - | `advancedtext` | Encouragement + rappel |
| 10 | La Salle du Trône | Maîtrise | `multichoice` | Application complexe |
| 11 | L'Épreuve Finale | Maîtrise | `questionset` | Mix de 4 questions |
| 12 | La Victoire ! | Boss | `multichoice` | Question de synthèse |

---

## Bonnes Pratiques

### Structure
- 5-10 etapes par parcours
- Alterner les types de quiz
- Feedback apres chaque question
- Ecran de victoire final

### LaTeX
- Tester le rendu avant production
- Eviter les formules trop complexes
- Utiliser des notations simples

### Images
- Resolution 1280x720 ou 1920x1080
- Format PNG recommande
- Fond adapte aux hotspots/texte superpose
