---
name: h5p-branching-scenario
description: Génère des parcours pédagogiques adaptatifs au format H5P Branching Scenario pour Moodle. Ce skill devrait être utilisé pour créer des parcours non-linéaires où les élèves font des choix qui déterminent leur chemin d'apprentissage (différenciation, remédiation, scénarios à dilemmes). Analyse un cours existant (LaTeX, HTML, texte) et produit un fichier .h5p importable dans Moodle.
---

# Skill H5P Branching Scenario - Parcours Adaptatifs

## RÈGLE ABSOLUE — Sources d'exercices obligatoires

**Un parcours H5P Branching Scenario ne doit JAMAIS être conçu avec des exercices inventés par l'IA.** L'expérience montre que le contenu généré ex nihilo est systématiquement superficiel, peu pertinent didactiquement, et ne reflète pas la progression voulue par l'enseignant.

### Avant TOUTE génération de parcours

1. **Demander à l'utilisateur les sources d'exercices** sur lesquelles s'appuyer si elles ne sont pas explicitement fournies. Formulation type :

   > « Avant de générer le parcours, j'ai besoin de m'appuyer sur des exercices existants (les contenus inventés sont systématiquement trop faibles). Peux-tu m'indiquer :
   > - le **dossier d'exercices** à exploiter (chemin vers `.tex`, `.pdf`, `.html`...) ?
   > - éventuellement les **numéros d'exercices** prioritaires pour cette notion ?
   >
   > Si tu n'as pas de source dédiée, dis-le moi et je te proposerai d'abord de créer une fiche d'exercices avant le parcours H5P. »

2. **Lire effectivement les sources** fournies (au moins un échantillon représentatif) avant de rédiger les questions du preplan.

3. **Tracer la provenance** de chaque question dans le preplan via un commentaire `_source` ou dans le rapport final, par exemple :
   - Q B1 ← Ex02 item 6
   - Éval Q3 ← Ex09 item 2

4. **Si aucune source n'existe**, ne pas inventer : proposer à l'utilisateur de créer d'abord une fiche d'exercices LaTeX (via le worker LaTeX), PUIS de générer le parcours H5P à partir de cette fiche.

### Exercices à privilégier pour chaque type de question

- **QCM de calcul** : items numériques d'exercices de simplification, équations, calculs directs
- **QCM de raisonnement** : extraits d'exercices avec « justifier », « démontrer », « expliquer pourquoi »
- **QCM piège / signe / domaine** : exercices où la difficulté est conceptuelle (cas impossibles, valeurs interdites)
- **Distracteurs réalistes** : reprendre les erreurs typiques visibles dans les corrections d'exercices

## RÈGLE ABSOLUE — Mélange des alternatives (anti pattern « toujours la première »)

**Toutes les BranchingQuestion DOIVENT avoir leurs alternatives mélangées** à chaque tentative de l'élève. Sans cela, l'élève (et même un professeur) résout systématiquement en cliquant sur la première proposition, ce qui détruit toute valeur pédagogique.

### Implémentation

Le top-level du preplan.json **doit** contenir :

```json
{
  "randomizeBranchingQuestions": true,
  ...
}
```

Cette option, native à `H5P.BranchingScenario`, randomise l'ordre d'affichage des alternatives dans chaque BranchingQuestion à chaque chargement par l'élève. Le `nextContentId` reste correctement attaché à chaque alternative, donc le routage ne casse pas.

Le script `generate_branching.py` met **`true` par défaut** depuis la mise à jour : il faut explicitement le passer à `false` (déconseillé) si on veut désactiver.

### Conséquences pour la rédaction

- **NE JAMAIS** écrire des feedbacks qui supposent un ordre fixe (ex : « la première proposition est juste »)
- **NE JAMAIS** ordonner les alternatives par difficulté croissante en s'attendant à ce que l'élève les voie dans cet ordre
- Les distracteurs doivent rester pertinents même si présentés en premier

## RÈGLE ABSOLUE — Scoring automatique (interdiction de l'auto-évaluation honnête)

H5P **sait compter les points tout seul**. Il est strictement interdit de produire un nœud du type :

> « Combien de bonnes réponses as-tu eues ? »
> - 6 ou 7 : excellent
> - 4 ou 5 : bien
> - 0 à 3 : à reprendre

C'est à la fois inutile (l'élève n'a aucune raison d'être honnête) et insultant pour l'outil.

### Bonne pratique : `dynamic-score`

Pour tout parcours qui contient une évaluation par QCM, utiliser le mode `dynamic-score` :

```json
{
  "scoring": "dynamic-score",
  "includeInteractionsScores": true,
  "randomizeBranchingQuestions": true
}
```

Et **sur chaque alternative** des questions d'évaluation, mettre un score :

```json
{
  "type": "branching_question",
  "question": "...",
  "alternatives": [
    {
      "text": "Bonne réponse",
      "nextContentId": 12,
      "feedback": {"title": "Bravo", "subtitle": "...", "score": 1}
    },
    {
      "text": "Mauvaise réponse",
      "nextContentId": 13,
      "feedback": {"title": "Faux", "subtitle": "...", "score": 0}
    }
  ]
}
```

H5P additionne automatiquement les `score` des alternatives choisies sur l'ensemble du parcours et affiche le total final. Plus besoin d'auto-évaluation.

### Conventions de scoring

- **Question d'évaluation** (compte vraiment) : `score: 1` sur la bonne réponse, `score: 0` sur les distracteurs
- **Question de remédiation / entraînement** (ne doit pas compter) : `score: 0` partout, ou ne pas mettre `score` du tout
- **Questions d'auto-positionnement initial** : `score: 0` (pas de bonne ou mauvaise réponse)
- Le score maximal n'est PAS fixé par le générateur : en `dynamic-score`, le lecteur le calcule à l'exécution en sommant les seuls nœuds **visités** (`calculateDynamicMaxScore`), donc il varie d'un élève à l'autre selon le chemin. Voir « REGLES CRITIQUES > 1. SCORING POUR MOODLE ».

### Et le routage par niveau (excellent/bien/à reprendre) ?

H5P BranchingScenario ne sait PAS faire de routage conditionnel sur le score accumulé. Donc :
- **Solution recommandée** : un seul nœud final avec un message générique (« Voici ton score »), H5P affichera automatiquement le total chiffré
- **Si l'auteur tient absolument à 3 fins différenciées** : utiliser `static-end-score` et router via les `nextContentId` des alternatives finales (chaque mauvaise réponse mène vers le palier inférieur). Mais c'est moins fiable que `dynamic-score`.

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
2. **STOP — Demander les sources d'exercices** (cf. RÈGLE ABSOLUE en haut du skill). Ne JAMAIS passer à l'étape suivante sans avoir au moins un dossier `.tex`/`.pdf` d'exercices à exploiter, ou l'accord explicite de l'utilisateur pour générer sans source (à éviter).
3. Pipeline standard : template > scan > challenge > fill > compile (voir phases ci-dessous)

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
  --input preplan_assembled.json --validate
```

`--validate` applique TOUTES les règles de `validators.py` : chemins BFS aboutissant à un terminal, références non cassées, valeurs hors schéma. Il n'existe pas de flag `--strict` (l'argparse le refuserait : `unrecognized arguments`).

---

## Post-production pipeline

Après la génération du preplan, un pipeline garantit la qualité avant compilation et livraison.

### Étapes du pipeline

```
preplan.json
  ↓
[1] fix_accents.py          → preplan_fixed.json   (non destructif)
  ↓
[2] generate_branching.py --validate
  ↓
[3] generate_branching.py --output scenario.h5p    (package FAT, libs bundlees)
  ↓
[4] render_h5p.py           → renders/screen_*.png  (AUTO-VISUALISATION : vrai player H5P + gate d'erreur)
  ↓
[5] build_standalone.py     → scenario_visualiseur.html  (relecture collegue, contenu + MathJax)
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
- `endScreen` → vérifie les textes et ajoute accents manquants

**Sortie (non destructive)** : par défaut, le résultat est écrit dans `<nom>_fixed.json` (ex. `preplan.json` → `preplan_fixed.json`) ; le fichier d'entrée n'est PAS modifié. Utiliser `--output` pour choisir le nom, ou `--in-place` pour écraser l'entrée.

### 2. Validation

```bash
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input preplan_fixed.json --validate
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
- `scenario-logiquiz.h5p` : **seulement** si le parcours contient des éléments hors socle (voir « REGLES CRITIQUES > 6b »)
- `scenario_report.json` : statistiques du parcours

Le rapport inclut :
- Nombre total de nœuds par type
- Nombre de branches (points de divergence)
- Profondeur maximale (nombre de sauts avant terminal)
- Points de convergence (nœuds ayant 2+ parents)
- Tier de score (40, 70, 100%)
- Durée estimée
- `logiquiz` : socle du lecteur léger, nœuds et interactions substitués dans la seconde archive

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

### 4. Auto-visualisation : rendu fidèle dans le VRAI player H5P

**`render_h5p.py` est le levier d'auto-visualisation.** Il ouvre le `.h5p` dans le vrai player H5P (h5p-standalone) en Chrome headless, capture l'écran réel en PNG, et détecte les erreurs bloquantes (libs manquantes, contenu cassé). C'est la preuve, AVANT Moodle, que le package s'importe et s'affiche « sans friction » — et le moyen pour l'agent de voir le rendu réel.

```bash
python ".claude/skills/h5p-branching-scenario/scripts/render_h5p.py" \
  --input scenario.h5p --output renders/
```

Sortie : `renders/screen_00.png` (écran réel) + `renders/render.log`. **Code de sortie ≠ 0 si une erreur H5P est détectée** → utiliser comme gate de qualité. L'agent LIT ensuite `screen_00.png` pour juger le rendu (mise en page, MathJax, boutons). Prérequis : Chrome installé + dossier `assets/h5p-standalone/` présent. La navigation multi-écrans (`--screens N`) est best-effort (l'iframe H5P n'est pas toujours pilotable en headless).

**Captures de TOUS les écrans : `--parcours`** (ajouté le 30/09/2026, Playwright, à lancer avec le python du venv du projet) :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/render_h5p.py" \
  --input scenario.h5p --output captures/ --parcours
```

Énumère tous les chemins racine → fin d'après `content.json`, les rejoue dans le vrai lecteur (choix des propositions par `data-id`, donc insensible au mélange) et capture chaque écran une fois : accueil, chaque diapositive (question vierge puis corrigée avec un distracteur), chaque question d'embranchement, chaque retour de proposition, chaque texte, chaque écran de fin. Fichiers `NN_<nœud>-<état>.png` dans l'ordre de l'organigramme + `captures.json`. **Regarder les PNG** : un QCM de Course Presentation dont l'énoncé est long (tableau, arbre) défile À L'INTÉRIEUR de son cadre et cache ses propositions ou son énoncé, sans erreur. Remède dans le schéma actuel : énoncé en lignes courtes (`<br>`) dans le texte de la diapositive, QCM placé à droite (`x: 50, y: 7, width: 48, height: 92`).

**Règle Chrome** (tous modes) : profil `--user-data-dir` temporaire dédié par lancement, `timeout`, arrêt par PID sans `/T`, orphelins filtrés sur le profil. Jamais `taskkill /IM chrome.exe`.

### 5. Visualiseur standalone pour relecture (contenu nœud par nœud)

Deux étapes (le script prend le **preplan JSON**, pas le `.h5p`) :

```bash
# 1) générer le template du visualiseur (une fois)
python ".claude/skills/h5p-branching-scenario/scripts/build_standalone.py" \
  --generate-template --output _template_viz.html

# 2) embarquer le preplan dans le visualiseur
python ".claude/skills/h5p-branching-scenario/scripts/build_standalone.py" \
  --input preplan_fixed.json --template _template_viz.html \
  --output scenario_visualiseur.html
```

Génère une page HTML **interactive** où chaque nœud rend son contenu réel (slides, quiz, MathJax). Pour que l'agent capture un nœud précis, ouvrir l'URL `scenario_visualiseur.html?node=N` (auto-sélection du nœud N) en Chrome headless puis lire le PNG.

Le collègue peut :
1. Cliquer chaque nœud pour voir son contenu rendu (texte, questions, alternatives + scores)
2. Ajouter des remarques par nœud (interface annotée)
3. Télécharger un `feedback.json` (à réinjecter via `integrate_feedback.py`)

**Avantages** : pas d'accès Moodle nécessaire ; export des remarques facilitant l'intégration.

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

**Correction du 26/07/2026** — l'ancienne consigne (« les scores des quiz embarqués ne remontent jamais ») était **fausse en `dynamic-score`**. Chaîne relue dans les librairies bundlées : `H5P.CoursePresentation.getScore()` somme ses interactions → `h5p-branching-scenario.js` l. 255-262 la lit à chaque changement d'écran → `scoring.js` `addLibraryScore()` l. 294-300 l'ajoute **si `includeInteractionsScores`** → `triggerXAPICompleted()` l. 294-297 l'envoie.

| Configuration | Ce qui part au carnet Moodle |
|---------------|------------------------------|
| `static-end-score` | **Uniquement** l'`endScreenScore` de l'écran de fin atteint (`scoring.js` l. 212-216). Les quiz ne servent qu'à l'entraînement. |
| `dynamic-score` + `includeInteractionsScores: true` (**défaut du générateur**) | endScreenScore **+ scores des quiz** des CoursePresentation. |
| `dynamic-score` + `includeInteractionsScores: false` | endScreenScore des nœuds et des alternatives seulement. |

⚠️ **Limite réelle du `dynamic-score`** : le maximum est calculé sur les seuls nœuds **visités** (`calculateDynamicMaxScore`, `scoring.js` l. 132-136). Il **dépend du chemin** — un élève passé par les remédiations est noté sur un total plus grand qu'un élève allé droit au but. Note de travail exploitable, **non comparable d'un élève à l'autre**. Pour noter la seule évaluation finale : `includeInteractionsScores: false`.

**Comment choisir** : palier de réussite unique et comparable → `static-end-score` ; comptage réel du travail fourni → `dynamic-score`.

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

### 5. forceContentFinished : une CHAINE par nœud, jamais un booléen

**Bug historique corrigé le 25/07/2026** (l'ancienne consigne de cette section était fausse). Le champ par nœud est de type `select` dans `semantics.json` : **trois valeurs, toutes valides**, défaut `"useBehavioural"`.

| Valeur | Effet |
|--------|-------|
| `"useBehavioural"` (défaut) | Suit le réglage global `behaviour.forceContentFinished` |
| `"enabled"` | Bloque le bouton Continuer tant que le contenu ne signale pas "finished" |
| `"disabled"` | Ne bloque jamais, même si le global vaut `true` |

⚠️ **Le piège n'est pas `"disabled"` — c'est le BOOLEEN.** Le lecteur compare en `===` strict sur des chaines (`libraryScreen.js` l. 524-527) : un `true`/`false` par nœud ne satisfait aucune branche et **neutralise le verrou en silence**, y compris quand le réglage global le demande. Le générateur écrivait ce booléen : le réglage global comme le réglage par nœud étaient sans aucun effet. Détail, mesures et tableau de vérité : `references/json-schema.md`, section « forceContentFinished (par noeud) ».

**Seuls** `course_presentation` et `interactive_video` peuvent utiliser `"enabled"` : eux seuls implémentent la sérialisation xAPI de l'état "finished". Sur `text` / `image` / `video` / `branching_question`, le générateur écrit `"disabled"` (un verrou y serait définitif). Toute valeur hors des trois est refusée par `validators.py`.

Exemple correct :

```json
{
  "type": "course_presentation",
  "title": "Cours + quiz obligatoire",
  "forceContentFinished": "enabled",
  "nextContentId": 21
}
```

### 5b. Versions H5P : alignées sur les Moodle FR

Les versions des librairies H5P sont centralisées dans `LIB_VERSIONS` (au début de `generate_branching.py`). Elles sont alignées sur les versions installées par défaut dans les Moodle français standards (académies, lycées) :

| Librairie | Version |
|-----------|---------|
| `H5P.BranchingScenario` | 1.8 |
| `H5P.CoursePresentation` | 1.25 |
| `H5P.InteractiveVideo` | 1.27 |
| `H5P.MultiChoice` | 1.16 |
| `H5P.TrueFalse` | 1.8 |
| `H5P.Blanks` | 1.14 |
| `H5P.MathDisplay` | 1.0 (rendu MathJax) |

**Source unique de vérité** : depuis le bundling, `LIB_VERSIONS` est **dérivé automatiquement** des `library.json` réels de `h5p_libs/` (fonction `_scan_lib_versions`). Les versions déclarées dans `h5p.json`/`content.json` correspondent donc TOUJOURS aux libs effectivement embarquées — plus de divergence déclaré/bundlé. Pour cibler un autre Moodle, remplacer les dossiers de `h5p_libs/` par les versions voulues (extraites d'un `.h5p` fat exporté depuis ce Moodle) : les versions suivront automatiquement.

### 5c. nextContentId sur branching_question : index réel, jamais -1

Pour les nœuds `branching_question`, le routage réel se fait via les `alternatives[].nextContentId`. Mais le champ top-level `nextContentId` du nœud doit quand même contenir un **index réel** (typiquement `i+1`), pas `-1`.

Si on met `-1` ici, certains H5P players interprètent le nœud comme terminal et bloquent la navigation. Le générateur attribue automatiquement un fallback `i+1`.

### 5d. feedback top-level vide : à éviter sur branching_question

Ne JAMAIS ajouter un objet `feedback: { title: "", subtitle: "", endScreenScore: 0 }` sur un nœud `branching_question` qui n'est pas terminal. Le player affiche un écran de feedback vide qui peut perturber le rendu. Le générateur n'ajoute le feedback que si l'auteur a défini un score ou un titre explicite.

### 6. CONTENU ADAPTE AUX NOEUDS

| Pour afficher... | Utiliser... |
|-----------------|------------|
| Texte simple (feedback, intro) | `text` (AdvancedText) |
| Contenu riche + quiz embarqués | `course_presentation` (slides + interactions) |
| Vidéo avec questions | `interactive_video` |
| Vidéo simple | `video` |
| Point de décision | `branching_question` |

### 6b. COMPATIBILITÉ DES LECTEURS — c'est une question de VERSIONS, pas de types

> ⚠️ Cette section a d'abord été rédigée à l'envers (26/07/2026, corrigée le jour même).
> Elle affirmait que Logiquiz ne possédait que quatre librairies. **C'est faux.**
> Le vrai piège est ci-dessous ; ne pas réintroduire l'ancienne explication.

**Aucun type de nœud n'est à proscrire.** Logiquiz (La Digitale) et les lecteurs H5P hors-ligne
équivalents possèdent l'ensemble des librairies, vidéo interactive comprise — mais dans des
versions **plus récentes** que celles que ce générateur déclare, lesquelles visent volontairement
bas pour les Moodle académiques (souvent en retard).

Mesure du 26/07/2026, faite sur un `.h5p` **exporté depuis l'installation réelle** :

| Librairie | `h5p_libs/` (Moodle) | Logiquiz |
|---|---|---|
| `H5P.BranchingScenario` | 1.8 | **1.11** (et 1.10) |
| `H5P.CoursePresentation` | 1.25 | **1.27** |
| `H5P.InteractiveVideo` | 1.27 | **1.28** |
| `H5P.ImageHotspots` | 1.10 | 1.11 |
| `H5P.DragQuestion` | 1.14 | 1.15 |
| `H5P.Components` | *absente* | **1.0** — exigée par IV 1.28, CP 1.27, Question 1.5 |

⚠️ **H5P résout une librairie par version EXACTE.** Un contenu qui demande
`H5P.BranchingScenario 1.8` sur une installation qui n'a que 1.10/1.11 ne résout pas la **racine**
du parcours : le constructeur lit `undefined.library`, lève
`TypeError: Cannot read properties of undefined (reading 'library')`, et **plus rien ne s'affiche** —
y compris les nœuds parfaitement supportés. L'échec est **silencieux** : « contenu vide », aucune
erreur visible. Le `.h5p` est pourtant valide et s'ouvre normalement ailleurs.

**Diagnostiquer par la version, jamais par la présence d'un type.** Et pour établir ce que possède
une installation, la seule mesure valable est un `.h5p` exporté **depuis elle** : ni l'export HTML
d'un contenu (il ne bundle que ce qu'il croit utile), ni le dépôt amont (simple catalogue) ne
prouvent quoi que ce soit.

#### Double sortie automatique

`generate_branching.py` produit **deux archives** :

```
parcours.h5p            -> Moodle, versions conservatrices, strictement inchangée
parcours-logiquiz.h5p   -> lecteur léger : MÊME CONTENU, seules les versions changent
```

La variante conserve le parcours **à l'identique** — vidéos interactives comprises. Elle se borne
à remapper les numéros de version (`_remap_library_versions`) et à embarquer `h5p_libs_logiquiz/`.
Routage, indices, titres, scores : rigoureusement identiques, vérifié programmatiquement.
`_expand_dependencies()` ferme transitivement les dépendances en lisant les `library.json` du jeu
visé — c'est lui qui ajoute `H5P.Components`, qu'aucune table statique ne connaît.

La rétro-compatibilité des schémas a été **vérifiée** (diff des `semantics.json`) : InteractiveVideo
1.27 → 1.28 n'ajoute que deux libellés `l10n` et une option ; CoursePresentation 1.25 → 1.27 n'a
que des ajouts, aucune suppression. Le `content.json` produit pour Moodle est donc lisible tel quel
par ces versions. **Refaire ce contrôle avant d'aligner sur un jeu de librairies encore plus récent.**

#### Constituer le jeu de librairies d'un autre lecteur

1. Créer n'importe quel contenu dans le lecteur cible, l'exporter en `.h5p`.
2. Extraire tous ses dossiers de librairies (tout sauf `content/`) dans `h5p_libs_logiquiz/`.
3. `_scan_lib_versions(LOGIQUIZ_LIBS_DIR)` en dérive les versions automatiquement : aucune table à
   tenir à jour. Ne **jamais** écraser `h5p_libs/`, dont dépend la sortie Moodle.

#### `--degrade` : le recours de dernier ressort

L'option `--degrade` bascule sur une substitution des blocs hors socle par un texte de remplacement
(avec lien cliquable vers la vidéo quand l'URL est connue), à indices et routage identiques. Elle ne
sert que pour un lecteur qui ne possède **réellement pas** une librairie — cas non observé à ce jour.
Elle **ampute le parcours** : ne l'employer qu'après avoir vérifié que le réalignement de versions ne
suffit pas. Jamais par défaut.
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

**ATTENTION** : pas de LaTeX dans les zones interactives (drag/blanks/markthewords, étiquettes et libellés de zones d'un `dragquestion`). Le validateur le détecte. MathJax est en revanche rendu (vérifié dans le lecteur) dans `summary`, `dialogcards` et les bulles d'`image_hotspots`.

---

## Types de noeuds

| Type | Code | Quiz embarques | Description |
|------|------|----------------|-------------|
| Texte riche | `text` | Non | HTML simple |
| Question d'embranchement | `branching_question` | Non | Choix determinant la branche |
| Presentation | `course_presentation` | Oui (multichoice, truefalse, dragtext, blanks, singlechoiceset, markthewords, **summary, dragquestion, dialogcards**) | Diaporama multi-slides avec quiz |
| Video interactive | `interactive_video` | Oui (multichoice, truefalse) | Video avec questions aux timestamps |
| Video | `video` | Non | Video YouTube ou fichier |
| Image | `image` | Non | Image simple (`image` : chemin local accepté) |
| Image à zones cliquables | `image_hotspots` | Non | Image + points qui ouvrent une bulle (découverte) |

---

## Disposition d'une diapositive : `layout` (30/09/2026)

Dans un nœud `course_presentation`, le texte d'une diapositive occupe par défaut tout le cadre : une
activité placée dessus le recouvre. Champ `layout` de la **diapositive** :

- `"full"` (défaut) : comportement historique, archive identique ;
- `"text-left"` : texte à gauche (45 % de la largeur, réglable par `text_width`), activité à droite ;
- `"text-top"` : texte en haut (25 % de la hauteur, réglable par `text_height`), activité dessous.

Une interaction qui porte ses propres `x`, `y`, `width`, `height` les garde. `validators.py` refuse
une valeur inconnue et avertit d'un recouvrement texte / activité (rectangles calculés).
**Un outil amont qui produit le preplan doit émettre `layout`** plutôt que d'écrire
« texte à gauche, activité à droite » dans le prompt. Détail : `references/json-schema.md`,
« Disposition de la diapositive » ; exemple jouable : `examples/dispositions_diapo/`.
Rendu à la taille d'un PC élève : `render_h5p.py … --parcours --width 1366 --height 768`.

---

## Exemples : régénérer les `.h5p`

`examples/` ne contient que les sources `.json` (les `.h5p` pèsent 7 à 9 Mo chacun, car ils embarquent les librairies H5P). Pour reconstruire un exemple :

```bash
python ".claude/skills/h5p-branching-scenario/scripts/generate_branching.py" \
  --input ".claude/skills/h5p-branching-scenario/examples/fractions_complet.json" \
  --output fractions_complet.h5p
```

Même commande pour `examples/activites_variees/activites_variees.json` et `examples/dispositions_diapo/dispositions.json` (la seconde archive `-logiquiz` est produite automatiquement si le parcours sort du socle léger).

---

## Activités variées et réponses saisies (30/09/2026)

Formats à ne pas changer à la légère (des outils amont peuvent les reprendre tels quels). Détail complet (tous les champs, conversions, mesures) :
`references/json-schema.md`, sections « Activités variées » et « Réponses saisies ». Exemple
complet, jouable, avec captures du lecteur réel : `examples/activites_variees/`.

**Autorisations vérifiées dans les `semantics.json`** : Summary 1.10, DragQuestion 1.14 et
Dialogcards 1.9 figurent parmi les éléments de diapositive de CoursePresentation 1.25 →
interactions de diapositive. **ImageHotspots 1.10 n'y figure pas** (Moodle l'écarterait à
l'import) mais BranchingScenario 1.8 l'accepte comme nœud → type de **nœud** `image_hotspots`
(une interaction `imagehotspots` est refusée par le validateur).

**Images** : champ `image` = chemin local (relatif au preplan), PNG / JPEG / GIF, copié dans
`content/images/`. **Positions en % du cadre de l'image** : `x`, `y` = coin haut gauche,
`width`, `height`, de 0 à 100, axe vertical vers le bas. Dessiner la figure dans un repère
`[0, 100]²` qui couvre l'image rend les coordonnées directement utilisables
(`examples/activites_variees/make_images.py`). Contrôle obligatoire : `jouer_activites.py`
surligne les zones en rouge sur la capture.

```json
{"type": "summary", "x": 4, "y": 14, "width": 92, "height": 84,
 "intro": "À chaque étape, choisis l'affirmation juste.",
 "statements": [{"correct": "Le produit des branches donne la probabilité du chemin.",
                 "wrong": ["La somme des branches donne la probabilité du chemin."], "tip": ""}]}
```

```json
{"type": "dragquestion", "x": 42, "y": 2, "width": 56, "height": 96,
 "image": "arbre_a_completer.png",
 "zones": [{"label": "Branche vers A", "x": 17.5, "y": 25, "width": 11, "height": 8, "correct": [0]},
           {"label": "Branche vers Ā", "x": 17.5, "y": 47, "width": 11, "height": 8, "correct": [1]}],
 "draggables": [{"text": "0,3"}, {"text": "0,7"}, {"text": "0,5"}]}
```

```json
{"type": "dialogcards", "x": 15, "y": 12, "width": 70, "height": 86,
 "cards": [{"front": "Probabilité de \\(\\overline{A}\\) ?", "back": "\\(1 - P(A)\\)"}]}
```

```json
{"type": "image_hotspots", "title": "Explorer l'arbre", "image": "arbre_complet.png",
 "hotspots": [{"x": 88, "y": 5, "header": "Chemin A puis B", "text": "<p>\\(0{,}3\\times 0{,}6\\)</p>"}],
 "nextContentId": 3}
```

Pièges mesurés dans le lecteur :

- `dragquestion` : les étiquettes sans `x`/`y` sont rangées dans la **bande du bas de l'image**,
  à laisser libre (10,5 % de hauteur par rangée). L'élément doit avoir
  `height ≥ width x 1,98 x (h/l de l'image) + 25` : sinon, après « Vérifier », il défile et coupe
  le haut de l'image. Le validateur donne la largeur maximale. Mise en page sûre : consigne à
  gauche en lignes courtes (`<br>`), image à droite.
- `image_hotspots` : (`x`, `y`) est le **centre** de l'icône (ou le centre du rectangle si
  `width`/`height` sont donnés). L'icône masque ce qu'elle recouvre : la poser à côté.
- Pas de MathJax dans les étiquettes ni les libellés de zones d'un `dragquestion`.

### Textes à trous : réponses multiples et tolérance

- Syntaxe `*rép1/rép2/rép3:indice*` : `/` sépare les réponses acceptées, `:` ouvre un indice.
- **Piège du `/`** : `*2/5*` accepte « 2 » OU « 5 », jamais la fraction. Demander la fraction en
  deux trous (numérateur, dénominateur) ou l'écriture décimale, et le dire dans la consigne.
  **Piège du `:`** : `*12:30*` attend « 12 ».
- Nombres : virgule ET point (`*0,4/0.4*`), jamais de MathJax.
- **Réponse chiffrée : `"numeric": true`** sur l'interaction `blanks` (écrit
  `acceptSpellingErrors: false`). Sans champ, la tolérance reste active (défaut des mots,
  inchangé) ; `"acceptSpellingErrors"` explicite l'emporte.
- **Mesure M4** (code `cloze.js` l. 43-60 + essai dans le lecteur) : la tolérance ne connaît pas
  les nombres, seulement la longueur de la réponse attendue — plus de 3 caractères, 1 erreur
  tolérée (inversion comprise), plus de 9, 2. Mesuré : `0,26` accepté pour `0,25`, `1600` pour
  `1500`, `12,57` pour `12,75`, `0,19` pour `0,18` ; `0,1` refusé pour `0,4` (3 caractères).
  Avec `numeric: true`, tout est refusé.
- Avertissements du validateur : `ANSWER_SINGLE_FORM`, `ANSWER_SLASH_FRACTION`,
  `ANSWER_TIP_COLON`, `ANSWER_NUMERIC_TOLERANCE`.

---

## Scripts disponibles

| Script | Usage |
|--------|-------|
| `create_template.py` | Génère un squelette JSON avec marqueurs `__TODO__` |
| `scan_template.py` | Scanne les `__TODO__`, génère rapport + questions challenge |
| `validators.py` | Validation (import par generate_branching.py) |
| `generate_branching.py` | Validation + génération du fichier .h5p **fat** (libs bundlées depuis `h5p_libs/`) + **seconde archive `-logiquiz`** si le parcours sort du socle des lecteurs légers |
| `render_h5p.py` | **Auto-visualisation** : rend le .h5p dans le vrai player H5P (headless), PNG + gate d'erreur |
| `extract_corpus.py` | Découpe des PDFs en pages + extraction texte pour référence |
| `fix_accents.py` | Correction des accents français (sortie `_fixed.json`, non destructive) |
| `build_standalone.py` | Visualiseur HTML de relecture (contenu nœud par nœud + MathJax ; `?node=N`) |
| `assemble_modules.py` | Assemblage de modules parallèles avec gestion des indexes |
| `integrate_feedback.py` | Intègre (annote) les remarques d'un collègue dans le preplan |

**Ressources bundlées** (ne pas supprimer) :
- `h5p_libs/` — les 70 bibliothèques H5P copiées dans chaque `.h5p` (sans elles, package « thin » non importable). Versions dérivées automatiquement des `library.json` réels.
- `assets/h5p-standalone/` — le player H5P utilisé par `render_h5p.py` pour l'auto-visualisation.

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
