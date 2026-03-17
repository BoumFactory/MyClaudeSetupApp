---
name: h5p-branching-scenario
description: Génère des parcours pédagogiques adaptatifs au format H5P Branching Scenario pour Moodle. Ce skill devrait être utilisé pour créer des parcours non-linéaires où les élèves font des choix qui déterminent leur chemin d'apprentissage (différenciation, remédiation, scénarios à dilemmes). Analyse un cours existant (LaTeX, HTML, texte) et produit un fichier .h5p importable dans Moodle.
---

# Skill H5P Branching Scenario - Parcours Adaptatifs

## Description

Génère des parcours d'apprentissage adaptatifs au format H5P Branching Scenario avec :
- **Nœuds riches** : CoursePresentation avec quiz embarqués, InteractiveVideo avec questions aux timestamps
- **4 patterns prédéfinis** : diagnostic, remédiation, dilemmes, choix élève
- **Scoring Moodle** : configuration correcte pour que les notes remontent au carnet
- **Pipeline template > scan > challenge > fill > compile**
- **Production modulaire parallèle** : allocation d'index entre agents, assemblage sans conflits
- **Post-production pipeline** : correction d'accents, validation, compilation, visualiseur standalone
- **Workflow collaboratif** : relecture collegue via HTML interactif, intégration des remarques

## Deux modes d'utilisation

### Mode Transcription (cours existant → H5P)

1. Lire le fichier source (LaTeX, HTML, texte)
2. Identifier les blocs : definitions, proprietes, exemples, exercices
3. Convertir le LaTeX en HTML+MathJax :
   - `\frac{a}{b}` → `\(\frac{a}{b}\)` (entourer de delimiteurs MathJax)
   - Utiliser `\(` `\)` pour inline, `\[` `\]` pour display (PAS `$`)
   - Pour `\cancel` : préfixer `\require{cancel}` une fois dans le premier champ math du document
   - Éviter le LaTeX dans les zones drag/blanks/markthewords
4. Choisir le pattern adaptatif selon la structure du cours :
   - Cours linéaire avec exercices → `remediation_loop`
   - Cours avec niveaux différenciés → `diagnostic_differentiation`
   - Activité exploratoire → `scenario_dilemmes`
   - Cours à la carte → `student_choice`
5. Générer le JSON avec contenu rempli (pas de `__TODO__`)
6. Valider et compiler directement en .h5p

### Mode Creation (depuis zero)

1. Theme + niveau donnes par l'utilisateur
2. Pipeline standard : template > scan > challenge > fill > compile (voir phases ci-dessous)

---

## Workflow en 4 phases (Mode Creation)

### Phase 1 : ANALYSER > GENERER TEMPLATE

1. Lire le cours source (LaTeX, HTML, texte) si disponible
2. Identifier les blocs de contenu, points de décision, chemins de remédiation
3. Choisir le pattern adapté :
   - `diagnostic_differentiation` : Q diagnostic > branches par niveau > fins différenciées
   - `remediation_loop` : contenu > test > réussi/échoué > remédiation > retest
   - `scenario_dilemmes` : situation > choix > conséquences > nouveaux choix
   - `student_choice` : menu > parcours parallèles > fins individuelles
4. Générer le squelette :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/create_template.py" \
  --pattern diagnostic_differentiation --title "Les fractions" --output template.json
```

Ou depuis une analyse JSON :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/create_template.py" \
  --input analysis.json --output template.json
```

### Phase 2 : SCANNER > CHALLENGER L'UTILISATEUR

1. Scanner le template pour identifier les zones à remplir :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/scan_template.py" \
  --input template.json --human
```

2. Le scan produit :
   - Liste de tous les `__TODO__` groupés par nœud
   - Détection des champs vides et scores manquants
   - **Questions challenge** pour guider le remplissage :
     - "Le nœud 4 est une CoursePresentation de remédiation avec 1 quiz. Combien de questions souhaitez-vous ?"
     - "Le test diagnostique a 2 alternatives. Est-ce suffisant pour discriminer 3 niveaux ?"
     - "Durée estimée : 8 minutes. Est-ce adapté à la séance ?"

3. Poser les questions challenge à l'utilisateur et noter ses réponses

### Phase 3 : REMPLIR LE TEMPLATE

1. Remplacer chaque `__TODO__` par du contenu pédagogique adapté
2. Respecter le champ `meta` de chaque nœud (purpose, difficulty, branch)
3. Pour les quiz embarqués dans CoursePresentation, écrire :
   - La question
   - Les réponses (avec `correct: true` sur la bonne)
   - Les feedbacks explicatifs
4. Valider le preplan rempli :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan.json --validate
```

### Phase 4 : COMPILER > LIVRER

1. Generer le fichier H5P :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan.json --output scenario.h5p
```

2. Upload sur Moodle :
   - Cours > Mode édition > Banque de contenus > Ajouter > H5P
   - Téléverser le `.h5p`
   - Publier comme **activité H5P** (bouton bleu, PAS comme label)
   - Tester chaque branche

---

## Production modulaire parallèle

Pour les parcours complexes (20+ nœuds), organiser le travail en modules parallèles avec allocation d'index prédéfinie.

### Stratégie d'allocation d'index

**Avant que les agents commencent**, créer une table d'allocation globale :

| Module          | Index range | Agent assigné | Node count | Description |
|-----------------|-------------|---------------|-----------|-------------|
| Introduction    | 0-2         | agent-intro   | 3         | Écran titre + consigne + diagnostic |
| Diagnostic      | 3-5         | agent-diag    | 3         | Question d'orientation |
| Parcours expert | 6-10        | agent-expert  | 5         | Contenu avancé (CP) + quiz + fin |
| Parcours moyen  | 11-15       | agent-mid     | 5         | Contenu intermédiaire + quiz + fin |
| Parcours base   | 16-20       | agent-begin   | 5         | Contenu introductif + quiz + fin |
| Bilans/Feedback | 21-23       | agent-final   | 3         | Écrans de synthèse |

**Point critique** : chaque agent **connaît la plage globale** de ses voisins. Quand le nœud 10 (fin expert) renvoie vers le bilan, utiliser `nextContentId: 21` (index global), PAS `nextContentId: 1` (local).

### Exemple de preplan avec allocation

```json
{
  "contentType": "H5P.BranchingScenario",
  "content": {
    "branching": [
      { "id": 0, "type": "text", "title": "Bienvenue", "nextContentId": 1 },
      { "id": 1, "type": "text", "title": "Instructions", "nextContentId": 3 },
      { "id": 2, "type": "text", "title": "placeholder", "reserved": true },

      { "id": 3, "type": "branching_question", "title": "Diagnostic", "answers": [
        { "text": "Expert", "nextContentId": 6 },
        { "text": "Moyen", "nextContentId": 11 },
        { "text": "Débutant", "nextContentId": 16 }
      ]},
      { "id": 4, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 5, "type": "text", "title": "placeholder", "reserved": true },

      { "id": 6, "type": "course_presentation", "title": "Module Expert", "nextContentId": 21 },
      { "id": 7, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 8, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 9, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 10, "type": "text", "title": "placeholder", "reserved": true },

      { "id": 11, "type": "course_presentation", "title": "Module Moyen", "nextContentId": 21 },
      { "id": 12, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 13, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 14, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 15, "type": "text", "title": "placeholder", "reserved": true },

      { "id": 16, "type": "course_presentation", "title": "Module Débutant", "nextContentId": 21 },
      { "id": 17, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 18, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 19, "type": "text", "title": "placeholder", "reserved": true },
      { "id": 20, "type": "text", "title": "placeholder", "reserved": true },

      { "id": 21, "type": "text", "title": "Bilan et conclusion", "nextContentId": -1 }
    ]
  }
}
```

### Gestion du décalage d'index

Si un module produit 4 nœuds au lieu de 5, les indexes suivants **se décalent**.

#### Solution 1 : Pré-allocation avec padding

Utiliser des nœuds "placeholder" (texte vide avec `reserved: true`) comme amortisseurs :

```json
{ "id": 10, "type": "text", "title": "", "content": "", "reserved": true, "nextContentId": -1 }
```

Ces nœuds ne sont jamais référencés et n'impactent pas le flux.

#### Solution 2 : Références symboliques

Utiliser des clés symboliques et résoudre au moment de l'assemblage :

```json
{ "id": 3, "answers": [
  { "text": "Expert", "nextContentId": "$MODULE_EXPERT_START" },
  { "text": "Moyen", "nextContentId": "$MODULE_MOYEN_START" },
  { "text": "Débutant", "nextContentId": "$MODULE_DEBUT_START" }
]}
```

Puis **avant compilation**, exécuter :

```python
import json
import re

preplan = json.load(open("preplan_with_symbols.json"))
allocation = {
  "$MODULE_EXPERT_START": 6,
  "$MODULE_MOYEN_START": 11,
  "$MODULE_DEBUT_START": 16,
  "$MODULE_BILAN": 21
}

def resolve_refs(obj):
  if isinstance(obj, dict):
    for k, v in obj.items():
      if isinstance(v, str) and v.startswith("$"):
        obj[k] = allocation.get(v, v)
      else:
        resolve_refs(v)
  elif isinstance(obj, list):
    for item in obj:
      resolve_refs(item)

resolve_refs(preplan)
json.dump(preplan, open("preplan.json", "w"), indent=2)
```

#### Solution 3 : Pré-allocation exacte (recommandée)

- Chaque agent **valide** le nombre exact de nœuds générés avant assemblage
- Remplir les emplacements inutilisés avec des nœuds "redirect" qui sautent au contenu réel

### Script d'assemblage

```bash
python ".claude/skills/h5p-branching-scenario/scripts/assemble_modules.py" \
  --config allocation.json \
  --input module_expert.json module_moyen.json module_debut.json \
  --output preplan_assembled.json
```

Le script :
1. Valide que chaque module a le nombre de nœuds prévu
2. Concatène les nœuds dans l'ordre
3. Règle les index globaux dans les références `nextContentId`
4. Signale les divergences

### Post-assemblage obligatoire

```bash
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan_assembled.json --validate --strict
```

Le flag `--strict` force la validation complète : tous les chemins BFS doivent aboutir à un terminal, pas de références cassées.

---

## Post-production pipeline

Après la génération du preplan, un pipeline garantit la qualité avant compilation et livraison.

### Étapes du pipeline

```
preplan.json
  ↓
[1] fix_accents.py          → preplan_fixed.json
  ↓
[2] generate_branching.py --validate --report
  ↓
[3] generate_branching.py --output scenario.h5p
  ↓
[4] build_standalone.py     → scenario_visualiseur.html
  ↓
[relecture collègue via HTML interactif]
  ↓
[intégration des remarques] → preplan_revised.json
  ↓
[compilation finale] → scenario_final.h5p
```

### 1. Correction des accents français

**Problème** : l'IA génère souvent `Resultats` au lieu de `Résultats`, `echec` au lieu de `échec`.

**Solution** :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/fix_accents.py" \
  --input preplan.json
```

Le script applique 100+ regex patterns pour normaliser le français :
- `resultat` → `résultat`
- `echec` → `échec`
- `branche` → `branche` (ok)
- `feedback` → `retour` (si souhaité)
- `endScreen` → vérifie les textes et ajoute accents manquants

Le preplan est mis à jour sur place : `preplan.json.fixed`.

### 2. Validation

```bash
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan_fixed.json --validate --strict
```

Vérifie :
- Aucun `__TODO__` restant
- Tous les chemins aboutissent à un terminal (`nextContentId: -1`)
- Pas de références cassées
- Scoring cohérent
- HTML valide dans les champs texte

Produit un rapport de validation : `preplan_validation_report.json`.

### 3. Compilation avec rapport

```bash
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan_fixed.json --output scenario.h5p --report
```

Génère :
- `scenario.h5p` : fichier prêt pour Moodle
- `scenario_report.json` : statistiques du parcours

Le rapport inclut :
- Nombre total de nœuds par type
- Nombre de branches (points de divergence)
- Profondeur maximale (nombre de sauts avant terminal)
- Points de convergence (nœuds ayant 2+ parents)
- Tier de score (40, 70, 100%)
- Durée estimée

Exemple :

```json
{
  "metadata": {
    "title": "Les fractions",
    "total_nodes": 24,
    "node_types": {
      "text": 12,
      "course_presentation": 8,
      "branching_question": 3,
      "interactive_video": 1
    },
    "branching_points": 3,
    "max_depth": 4,
    "convergence_points": 5,
    "score_tiers": [40, 70, 100],
    "estimated_duration_minutes": 15
  },
  "warnings": []
}
```

### 4. Visualiseur standalone pour relecture

```bash
python ".claude/skills/h5p-branching-scenario/scripts/build_standalone.py" \
  --input scenario.h5p \
  --output scenario_visualiseur.html
```

Génère une page HTML **interactive et autonome** pour permettre au collègue de :
1. Naviguer dans le parcours (clics sur branches, remplissage simulé)
2. Voir tous les chemins possibles (diagramme du flux)
3. Ajouter des remarques directes sur les nœuds (interface annotée)
4. Télécharger un fichier JSON avec ses annotations

**Avantages** :
- Pas d'accès Moodle nécessaire
- Relecture hors-ligne
- Export des remarques = facilite l'intégration

La page inclut un formulaire au bas :

```html
<form>
  <textarea name="feedback">Remarques générales</textarea>
  <button type="submit">Télécharger feedback.json</button>
</form>
```

### Intégration des remarques collègue

Quand le collègue télécharge `feedback.json` :

```json
{
  "node_5": {
    "content": "Le texte est trop long, réduire de 50%",
    "priority": "medium"
  },
  "node_12": {
    "content": "La question Q3 est ambiguë",
    "priority": "high"
  }
}
```

Utiliser un agent pour :
1. Lire le preplan original
2. Appliquer les corrections (édition du contenu)
3. Re-lancer le pipeline complet

```bash
# Script wrapper pour intégration commentaires
python ".claude/skills/h5p-branching-scenario/scripts/integrate_feedback.py" \
  --preplan preplan_fixed.json \
  --feedback feedback.json \
  --output preplan_revised.json
```

Puis relancer :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/fix_accents.py" \
  --input preplan_revised.json

python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan_revised.json \
  --output scenario_final.h5p --validate --report
```

---

## Extraction de corpus

Pour les parcours lourds en contenu (cours PDF à transformer), extraire le matériel source d'abord.

### Extraction des ressources

```bash
python ".claude/skills/h5p-branching-scenario/scripts/extract_corpus.py" \
  --input corpus/ \
  --output generated/reference/
```

**Entrée** : dossier avec PDFs, images, fichiers texte

**Sortie** :
- `reference/pages_text/` : PDFs découpés en pages texte
- `reference/index.json` : index des ressources avec métadonnées
- `reference/manifest.md` : catalogue lisible

Exemple manifest :

```markdown
# Corpus - Les fractions

## Pages 1-5 : Définitions
- Page 1 : Fraction comme quotient
- Page 2 : Fraction équivalente
- Page 3 : Simplification
- Page 4 : Comparaison
- Page 5 : Exercice diagnostic

## Pages 6-12 : Opérations
- Page 6 : Addition même dénominateur
- Page 7 : Addition dénominateurs différents
...
```

**Avantage** : Les agents ne reçoivent PAS 1 GB de PDF (longues entrées). Ils reçoivent un index structuré et peuvent chercher des passages spécifiques par numéro de page.

---

## REGLES CRITIQUES

### 1. SCORING POUR MOODLE

**Utiliser `static-end-score` (le plus fiable).**

Les scores des quiz embarques dans CoursePresentation ne remontent PAS au carnet de notes Moodle. Seul `endScreenScore` (configure via `feedback.score` sur les noeuds terminaux) est envoye via xAPI.

Chaque noeud terminal (`nextContentId: -1`) DOIT avoir :
```json
"feedback": { "title": "...", "subtitle": "...", "score": 70 }
```

### 2. LIMITER LA PROFONDEUR

**Maximum 3-4 niveaux de branchement.** Au-delà, la complexité explose.

```
OK :  Intro > Question > Branche A/B > Fin
OK :  Intro > Q1 > A: [contenu > Q2 > A1/A2 > fin] / B: [contenu > fin]
NON : 5+ niveaux d'embranchement imbriqués
```

### 3. PREVOIR DES POINTS DE CONVERGENCE

Ne pas laisser les branches diverger indéfiniment. Faire converger vers des nœuds communs quand c'est pertinent.

### 4. CHAQUE BRANCHE MÈNE À UNE FIN

Le validateur BFS vérifie que tous les chemins depuis le nœud 0 aboutissent à un `nextContentId: -1`. Un chemin sans issue = apprenant bloqué.

### 5. forceContentFinished TOUJOURS "disabled" PAR DÉFAUT

Le générateur force automatiquement `forceContentFinished: "disabled"` sur les nœuds `text`, `image` et `video` car ces types H5P ne peuvent **PAS** signaler "finished".

Mettre `forceContentFinished: "enabled"` sur ces types = **le bouton Continuer reste bloqué à jamais**.

**Seuls** `course_presentation` et `interactive_video` peuvent utiliser `forceContentFinished: "enabled"` car ces types implémentent la sérialisation xAPI de l'état "finished".

Exemple correct :

```json
{
  "id": 5,
  "type": "text",
  "title": "Écran de feedback",
  "content": "Bravo ! Tu as réussi.",
  "forceContentFinished": "disabled",
  "nextContentId": 21
}
```

### 6. CONTENU ADAPTE AUX NOEUDS

| Pour afficher... | Utiliser... |
|-----------------|------------|
| Texte simple (feedback, intro) | `text` (AdvancedText) |
| Contenu riche + quiz embarqués | `course_presentation` (slides + interactions) |
| Vidéo avec questions | `interactive_video` |
| Vidéo simple | `video` |
| Point de décision | `branching_question` |

### 7. MATHJAX POUR LES MATHS

```html
<p>Calculer \(\frac{1}{2} + \frac{1}{3}\)</p>
```

MathJax est supporté nativement dans H5P si le plugin est activé sur Moodle.

**Delimiteurs** :
- Inline : `\(` ... `\)` (PAS `$` ... `$`)
- Display : `\[` ... `\]` (PAS `$$` ... `$$`)

**Extensions MathJax** : certaines commandes nécessitent `\require{extension}` :
- `\cancel`, `\bcancel`, `\xcancel` → `\require{cancel}` (une seule fois dans le document)
- `\color`, `\colorbox` → `\require{color}`

**Exemple avec extension** :
```html
<p>\(\require{cancel}\frac{\cancel{3}}{7} \times \frac{2}{\cancel{3}} = \frac{2}{7}\)</p>
```

**Commandes NON supportees** : `\newcommand`, `\renewcommand`, `\usepackage`, `\begin{align*}` hors mode math.

**ATTENTION** : pas de LaTeX dans les zones interactives (drag/blanks/markthewords). Le validateur le détecte.

---

## Types de noeuds

| Type | Code | Quiz embarques | Description |
|------|------|----------------|-------------|
| Texte riche | `text` | Non | HTML simple |
| Question d'embranchement | `branching_question` | Non | Choix determinant la branche |
| Presentation | `course_presentation` | Oui (multichoice, truefalse, dragtext, blanks, singlechoiceset, markthewords) | Diaporama multi-slides avec quiz |
| Video interactive | `interactive_video` | Oui (multichoice, truefalse) | Video avec questions aux timestamps |
| Video | `video` | Non | Video YouTube ou fichier |
| Image | `image` | Non | Image simple |

---

## Scripts disponibles

| Script | Usage |
|--------|-------|
| `create_template.py` | Génère un squelette JSON avec marqueurs `__TODO__` |
| `scan_template.py` | Scanne les `__TODO__`, génère rapport + questions challenge |
| `validators.py` | Validation (import par generate_branching.py) |
| `generate_branching.py` | Validation + génération du fichier .h5p |
| `extract_corpus.py` | Découpe des PDFs en pages + extraction texte pour référence |
| `fix_accents.py` | Correction automatique des accents français manquants |
| `build_standalone.py` | Génère un visualiseur HTML standalone pour relecture collègue |
| `assemble_modules.py` | Assemblage de modules parallèles avec gestion des indexes |
| `integrate_feedback.py` | Intègre les remarques d'un collègue dans le preplan |

### Usage détaillé

```bash
# Générer un template
python ".claude/skills/h5p-branching-scenario/scripts/create_template.py" \
  --pattern remediation_loop --title "Les équations" --output template.json

# Scanner le template
python ".claude/skills/h5p-branching-scenario/scripts/scan_template.py" \
  --input template.json --human

# Scanner avec sortie JSON
python ".claude/skills/h5p-branching-scenario/scripts/scan_template.py" \
  --input template.json --output report.json

# Valider un preplan rempli
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan.json --validate

# Generer le H5P
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan.json --output scenario.h5p

# Extraire corpus depuis PDFs
python ".claude/skills/h5p-branching-scenario/scripts/extract_corpus.py" \
  --input corpus/ --output generated/reference/

# Corriger les accents français
python ".claude/skills/h5p-branching-scenario/scripts/fix_accents.py" \
  --input preplan.json

# Generer le visualiseur standalone
python ".claude/skills/h5p-branching-scenario/scripts/build_standalone.py" \
  --input scenario.h5p --output scenario_visualiseur.html

# Assembler des modules parallèles
python ".claude/skills/h5p-branching-scenario/scripts/assemble_modules.py" \
  --config allocation.json \
  --input module_expert.json module_moyen.json module_debut.json \
  --output preplan_assembled.json

# Intégrer les remarques du collègue
python ".claude/skills/h5p-branching-scenario/scripts/integrate_feedback.py" \
  --preplan preplan_fixed.json \
  --feedback feedback.json \
  --output preplan_revised.json
```

---

## Patterns disponibles

### Diagnostic > Différenciation

```
[Intro] > [Q diagnostic]
  Expert       > [CoursePresentation avancé + quiz] > [Bilan 100%]
  Intermédiaire > [CoursePresentation moyen + quiz] > [Bilan 70%]
  Débutant     > [CoursePresentation base + quiz]   > [Bilan 40%]
```

### Remédiation en boucle

```
[Cours CP] > [Test]
  Réussi  > [Fin 100%]
  Échoué  > [Remédiation CP + quiz] > [Retest]
    Réussi  > [Fin 70%]
    Échoué  > [Fin 30%]
```

### Scénario à dilemmes

```
[Situation] > [Choix 1/2/3]
  Choix A > [Conséquence] > [2nd choix] > Fin A/B
  Choix B > [Conséquence] > [2nd choix] > Fin A/B
  Choix C > [Conséquence] > Fin directe
```

### Choix du parcours par l'élève

```
[Accueil] > [Menu]
  Découverte    > [3 étapes mixtes] > [Fin 60%]
  Entraînement  > [4 étapes mixtes] > [Fin 80%]
  Expert        > [2 étapes intenses] > [Fin 100%]
```

---

## Reference

Le schema JSON complet est documente dans `references/json-schema.md`.

Consulter cette reference pour :
- La structure detaillee de chaque type de noeud
- Les conventions `__TODO__` et le champ `meta`
- Le schema complet des interactions dans CoursePresentation
- Les interactions dans InteractiveVideo (timestamps)
- Les options de scoring et la limitation xAPI
- Les 4 patterns predefinis

---

## Dépendances

- Python 3.8+
- Modules standard uniquement : `json`, `zipfile`, `uuid`, `pathlib`, `re`, `io`, `random`, `collections`
- Dépendance optionnelle : `PyPDF2` (uniquement pour `extract_corpus.py`)
  - Installation : `pip install PyPDF2`
  - Non requise si extraction de corpus non utilisée

---

## Voir aussi

- Skill `h5p-gamemap` : pour les parcours gamifies (Game Map)
- Commande `/moodleise` : pour la creation complete de cours Moodle
- Commande `/createGameMap` : pour les parcours a hotspots sur carte
