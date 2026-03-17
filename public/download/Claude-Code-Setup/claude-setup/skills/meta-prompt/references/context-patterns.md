# Patterns de Prompts par Contexte

Patterns optimisés pour les différents contextes d'utilisation du prof de maths et développeur QF-Studio.

---

## Contexte 1 : Éducation Mathématique

### Template de base

```markdown
# [Titre : type de contenu + theme + niveau]

## Role

Professeur de mathematiques experimente en college/lycee ({{NIVEAU}}).
Specialiste du programme officiel de l'Education Nationale.
Approche progressive, bienveillante, centree sur la comprehension.

## Contexte

<programme>
Domaine : {{DOMAINE}}
Competence : {{COMPETENCE}}
Capacite : {{CAPACITE}}
</programme>

<situation>
{{CONTEXTE_PEDAGOGIQUE}}
Prerequis eleves : {{PREREQUIS}}
</situation>

## Instructions

### Etape 1 : Analyse des prerequis
Identifier les notions que les eleves doivent maitriser avant {{THEME}}.

### Etape 2 : Structuration progressive
Organiser en {{NB_PARTIES}} parties, du simple au complexe.
Introduire une seule difficulte nouvelle par partie.

### Etape 3 : Generation du contenu
<rules>
- Tous les chiffres/coefficients DISTINCTS dans un meme exercice
- Varier les representations (numerique, graphique, textuel)
- Inclure au moins un exercice avec contexte reel
- Niveaux de difficulte : facile → moyen → difficile
</rules>

### Etape 4 : Verification
Relire en verifiant :
- [ ] Conformite programme officiel {{NIVEAU}}
- [ ] Progression logique
- [ ] Zero erreur mathematique
- [ ] Vocabulaire adapte au public

## Format de sortie

{{FORMAT}} (LaTeX bfcours / Markdown / JSON)

## Variables

| Variable | Description | Defaut |
|----------|-------------|--------|
| `{{NIVEAU}}` | Niveau scolaire | obligatoire |
| `{{THEME}}` | Theme mathematique | obligatoire |
| `{{DOMAINE}}` | Domaine du programme | obligatoire |
| `{{NB_PARTIES}}` | Nombre de parties | 3 |
| `{{FORMAT}}` | Format de sortie | "LaTeX bfcours" |
```

### Sous-patterns éducatifs

#### Questions Flash (QF)
```
Generer {{NB_QUESTIONS}} questions flash pour le niveau {{NIVEAU}}.
Theme : {{THEME}}.

Chaque question :
- Enonce court (1-2 lignes max)
- Reponse directe attendue
- Temps de reflexion : 30 secondes max
- Difficulte progressive (1 facile, 1 moyen, 1 difficile)

Format JSON :
{
  "enonce": "texte",
  "reponse": "texte",
  "details": "explication courte",
  "theme": "{{THEME}}",
  "prompt": "prompt utilise"
}
```

#### Évaluation / Devoir
```
Creer une evaluation sur {{THEME}} pour le niveau {{NIVEAU}}.
Duree : {{DUREE}} minutes.
Bareme total : {{POINTS}} points.

Structure :
- {{NB_EXERCICES}} exercices de difficulte croissante
- Premier exercice = acquis de base (accessibilite)
- Dernier exercice = approfondissement / defi
- Points repartis proportionnellement a la difficulte
- Chaque exercice avec competence evaluee explicite
```

#### Fiche de cours
```
Rediger une fiche de cours synthetique sur {{THEME}} ({{NIVEAU}}).

Structure :
1. Titre et objectifs
2. Proprietes/Theoremes (max {{NB_PROPRIETES}})
3. Exemples detailles pour chaque propriete
4. Methodes (comment faire)
5. Pieges a eviter
6. Exercices d'application directe

Chaque propriete : enonce formel + explication en langage courant + exemple
```

---

## Contexte 2 : Développement Logiciel (Rust/Tauri)

### Template de base

```markdown
# [Titre : action + composant + objectif]

## Role

Ingenieur logiciel expert en Rust et architectures Tauri v2.
Specialiste des patterns async, serde, et des applications desktop hybrides.

## Contexte

<architecture>
Application : QF-Studio (Tauri v2)
Crates : qf-generator (lib) + qf-studio (Tauri)
Frontend : Vanilla JS/CSS/HTML, Vite 5
</architecture>

<constraints>
- anyhow::Context pour toute erreur, jamais unwrap()
- Derives : Debug, Clone, PartialEq, Serialize, Deserialize
- JSON compatible Python (champs sans accents)
- BTreeMap pour cles triees
</constraints>

## Instructions

### Etape 1 : Analyse du code existant
Lire les fichiers impactes avant toute modification.
Identifier les interfaces publiques et les dependances.

### Etape 2 : Implementation
<rules>
- Respecter les conventions existantes du fichier
- Ajouter .context("description") a chaque ? operator
- Utiliser les types existants, ne pas en creer de nouveaux inutilement
- Tester chaque chemin d'erreur
</rules>

### Etape 3 : Verification
- cargo clippy sans warnings
- cargo test passe
- Build complet reussi

## Variables

| Variable | Description | Defaut |
|----------|-------------|--------|
| `{{COMPOSANT}}` | Module/fichier cible | obligatoire |
| `{{ACTION}}` | Ce qu'il faut faire | obligatoire |
| `{{IMPACT}}` | Fichiers impactes | obligatoire |
```

---

## Contexte 3 : Agent Autonome

### Template de base

```markdown
# [Nom de l'agent]

## Role

Agent specialise dans {{DOMAINE}}.
Mission : {{OBJECTIF_PRINCIPAL}}.

## Capacites

Outils disponibles :
- **Read** : Lire fichiers source
- **Write** : Ecrire resultats
- **Bash** : Executer commandes
- **Grep/Glob** : Rechercher dans le code

## Processus de travail

### Etape 1 : Reconnaissance
Lire les fichiers pertinents. Ne JAMAIS speculer sur du code non lu.

### Etape 2 : Planification
Reflechir dans <thinking> avant chaque action.
Lister les modifications necessaires.

### Etape 3 : Execution
Implementer les changements. Un fichier a la fois.
Verifier apres chaque modification.

### Etape 4 : Validation
Executer les tests. Verifier que rien n'est casse.

## Regles critiques

- Persistence : continuer jusqu'a resolution complete
- Anti-hallucination : utiliser les outils, ne pas deviner
- Planification : reflechir avant chaque action

## Format de sortie

Rapport final :
```
## Résumé
[Ce qui a ete fait]

## Fichiers modifies
- [fichier1] : [description changement]

## Tests
[Resultats des tests]
```
```

---

## Contexte 4 : Analyse de Données

### Template de base

```markdown
# [Titre de l'analyse]

## Role

Analyste de donnees expert en statistiques et visualisation.

## Donnees source

<data>
{{DONNEES}}
</data>

## Instructions

### Etape 1 : Exploration
Decrire la structure des donnees : colonnes, types, valeurs manquantes.

### Etape 2 : Analyse
Calculer : {{METRIQUES}}.
Raisonner etape par etape pour chaque calcul.

### Etape 3 : Interpretation
Expliquer les resultats en langage clair.
Identifier les tendances et anomalies.

## Format de sortie

JSON structure :
{
  "summary": "resume en 2-3 phrases",
  "metrics": { ... },
  "insights": ["insight1", "insight2"],
  "recommendations": ["rec1", "rec2"]
}
```

---

## Contexte 5 : Génération Créative

### Template de base

```markdown
# [Titre du contenu]

## Role

Createur de contenu specialise en {{DOMAINE}}.
Style : {{STYLE}} (informatif / humoristique / formel / ludique).

## Public cible

{{PUBLIC}} — Age, interets, niveau de connaissance.

## Instructions

Generer {{TYPE_CONTENU}} sur {{SUJET}}.

<creative_direction>
- Ton : {{TON}}
- Registre de langue : {{REGISTRE}}
- References culturelles : {{REFERENCES}}
</creative_direction>

## Contraintes

- Longueur : {{LONGUEUR}}
- Eviter : {{EVITER}}
- Inclure obligatoirement : {{INCLURE}}

## Exemples de style

<example>
{{EXEMPLE_STYLE}}
</example>
```

---

## Matrice de sélection des techniques par contexte

| Technique | Education | Software | Agent | Analyse | Creatif |
|-----------|:---------:|:--------:|:-----:|:-------:|:-------:|
| XML Tags | ++ | ++ | ++ | + | + |
| Role specifique | +++ | ++ | +++ | ++ | +++ |
| Few-Shot | +++ | + | + | ++ | +++ |
| CoT | ++ | ++ | ++ | +++ | - |
| Structured Output | ++ | +++ | ++ | +++ | + |
| Constitutional | +++ | + | + | + | ++ |
| ReAct | - | ++ | +++ | + | - |
| RAG | ++ | + | + | +++ | + |
| Prompt Chaining | + | ++ | ++ | ++ | + |
| Adaptive Thinking | + | +++ | +++ | ++ | + |
| Self-Consistency | ++ | - | - | +++ | - |
| Reflexion | ++ | +++ | ++ | + | ++ |

Légende : +++ = essentiel, ++ = recommandé, + = utile, - = inutile
