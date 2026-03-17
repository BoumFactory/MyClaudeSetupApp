# Catalogue des Techniques de Prompt Engineering 2025-2026

Référence complète des 23 techniques issues des guides officiels Anthropic, OpenAI, Google DeepMind et Meta.

Sources :
- Anthropic Claude 4 Best Practices (2025) — platform.claude.com
- OpenAI GPT-4.1 Prompting Guide — cookbook.openai.com
- Google Gemini 3 Prompting Guide — docs.cloud.google.com
- Meta Llama 4 Model Cards — llama.com
- PromptingGuide.ai — Reference academique

---

## 1. Be Clear and Direct

**Source** : Anthropic (fondamental)
**Contexte** : Toujours. Base de toutes les autres techniques.

Claude 4.x suit les instructions plus littéralement que les versions précédentes. Les hypothèses implicites ne sont plus inférées.

**Pattern** :
```
Moins efficace :
  Creer un dashboard analytique

Plus efficace :
  Creer un dashboard analytique avec graphiques interactifs,
  filtres par date et export CSV. Inclure au minimum 5 types
  de visualisations differentes.
```

**Règles Claude 4.x** :
- Ajouter contexte/motivation derrière chaque instruction
- Formuler positivement : "Écrire en paragraphes" et non "Ne pas utiliser de listes"
- Retirer les prompts anti-paresse ("be thorough", "don't be lazy")
- Remplacer "CRITICAL: You MUST" par des instructions directes simples

---

## 2. XML Tags pour la structure

**Source** : Anthropic (natif Claude), fonctionne sur tous les modèles
**Contexte** : Tout prompt avec composants multiples (instructions + contexte + données + exemples)

Claude a été spécifiquement entraîné à reconnaître la structure XML.

**Pattern** :
```xml
<role>Professeur de mathematiques en college</role>

<context>
Classe de 3eme, chapitre sur le theoreme de Thales.
Les eleves ont deja vu les triangles semblables.
</context>

<instructions>
1. Generer 5 exercices progressifs
2. Inclure un exercice de demonstration
3. Varier les configurations geometriques
</instructions>

<format>
Chaque exercice au format LaTeX avec environnement bfExercice.
</format>

<examples>
{{EXEMPLES_EXERCICES}}
</examples>
```

**Bonnes pratiques** :
- Noms de tags cohérents, référencés dans le texte ("Utiliser le contexte dans `<context>`...")
- Imbriquer pour hiérarchiser : `<outer><inner></inner></outer>`
- Combiner avec CoT : `<thinking>` pour raisonnement, `<answer>` pour sortie
- Utiliser XML en sortie aussi pour faciliter le parsing

---

## 3. Role / System Prompting

**Source** : Universel (tous providers)
**Contexte** : Toute application production

**Pattern pour agent logiciel** :
```xml
<role>Expert en ingenierie logicielle specialise en Rust et TypeScript</role>

<default_to_action>
Implementer les changements plutot que les suggerer.
En cas de doute, inferer l'action la plus utile et proceder.
</default_to_action>

<investigate_before_answering>
Ne jamais speculer sur du code non lu. Toujours lire les fichiers
pertinents AVANT de repondre.
</investigate_before_answering>
```

**Pattern pour educateur** :
```xml
<role>
Professeur de mathematiques experimente (college 6eme-3eme).
Connaissance parfaite des programmes officiels Education Nationale.
Approche progressive, bienveillante, centree sur la comprehension.
</role>
```

**Sections de system prompt recommandées** (Anthropic Claude 4) :

| Section | Contenu |
|---------|---------|
| `<default_to_action>` | Agir proactivement ou attendre instructions |
| `<investigate_before_answering>` | Toujours lire avant de répondre |
| `<use_parallel_tool_calls>` | Appels outils en parallèle si indépendants |
| `<avoid_excessive_markdown>` | Contrôle du format de sortie |
| `<frontend_aesthetics>` | Standards visuels pour UI |

---

## 4. Few-Shot Prompting

**Source** : Universel
**Contexte** : Format de sortie précis, tâche nouvelle/spécifique

**Règle** : 3-5 exemples optimal. Plus = risque d'overfitting (warning Google).

**Pattern** :
```markdown
## Exemples

### Exemple 1
**Entree** : Theme = "fractions", Niveau = "6eme"
**Sortie** :
\begin{bfExercice}{Fractions et partage}
Colorier \dfrac{3}{4} d'un rectangle decoupe en 8 parts egales.
\end{bfExercice}

### Exemple 2
**Entree** : Theme = "equations", Niveau = "4eme"
**Sortie** :
\begin{bfExercice}{Equation du premier degre}
Resoudre l'equation $2x + 3 = 7$.
\end{bfExercice}
```

**Règles qualité** :
- Exemples diversifiés couvrant les cas limites
- Montrer UNIQUEMENT les patterns positifs (jamais d'anti-pattern)
- Varier les formulations pour éviter le copie verbatim

---

## 5. Zero-Shot Chain-of-Thought

**Source** : Kojima et al. 2022, universel
**Contexte** : Raisonnement multi-étapes, mathématiques, logique

Ajouter simplement "Raisonner étape par étape" ou "Let's think step by step" déclenche un raisonnement en chaîne automatique.

**Pattern** :
```
Q : Un magasin a 23 pommes. Il en utilise 20 pour des tartes
    et en rachete 6. Combien en a-t-il ?

Raisonner etape par etape avant de donner la reponse.
```

**Pour Claude (CoT structure)** :
```xml
<instructions>
Raisonner etape par etape dans les balises <thinking>,
puis donner la reponse dans les balises <answer>.
</instructions>
```

---

## 6. Structured Output

**Source** : Universel
**Contexte** : Integrations API, pipelines de donnees, parsing automatique

**Pattern JSON** :
```
Analyser le texte et retourner un objet JSON avec exactement ces champs :
{
  "sentiment": "positive" | "negative" | "neutral",
  "confidence": float entre 0 et 1,
  "topics": array de strings (max 5),
  "summary": string (max 100 mots)
}

Retourner UNIQUEMENT le JSON. Pas d'explication, pas de code blocks.
```

**Pattern LaTeX** :
```
Generer le code LaTeX complet. Le code doit :
- Compiler sans erreur avec lualatex
- Utiliser le package bfcours
- Contenir uniquement le corps du document (pas de \documentclass)
```

---

## 7. Few-Shot Chain-of-Thought

**Source** : Wei et al. 2022, universel
**Contexte** : Raisonnement complexe quand le Zero-Shot CoT est insuffisant

**Pattern** :
```
Q : La cantine avait 23 pommes. Si elle en a utilise 20 pour le dejeuner
    et en a rachete 6, combien en a-t-elle maintenant ?
A : La cantine avait 23 pommes. Elle en utilise 20, il reste 23-20=3.
    Elle en rachete 6, total = 3+6=9. Reponse : 9.

Q : [Nouvelle question]
A :
```

---

## 8. Tree-of-Thought (ToT)

**Source** : Yao et al. 2023, PromptingGuide.ai
**Contexte** : Problemes durs de planification, puzzles mathematiques, decisions strategiques

**Pattern simplifie (sans framework)** :
```
Imaginer 3 experts qui travaillent sur ce probleme.
Chaque expert ecrit une etape de raisonnement et la partage.
Si un expert realise que son approche est erronee, il se retire.
Les experts restants continuent jusqu'a trouver la solution.

Probleme : {{PROBLEME}}
```

**Pattern complet (programmatique)** :
```
Etape 1 : Decomposer le probleme en sous-etapes
Etape 2 : Generer B=5 pensees candidates par etape
Etape 3 : Evaluer chaque pensee : "sur / possible / impossible"
Etape 4 : Explorer (BFS/DFS) les chemins viables, elaguer les impossibles
Etape 5 : Retourner le meilleur chemin complet
```

---

## 9. Self-Consistency

**Source** : Wang et al. 2022, PromptingGuide.ai
**Contexte** : Precision prioritaire, raisonnement arithmetique/logique

Generer N chaines de raisonnement independantes, vote majoritaire sur la reponse.

**Usage** : Executer le meme prompt N=5-20 fois avec temperature > 0, prendre la reponse la plus frequente.

---

## 10. ReAct (Reasoning + Acting)

**Source** : Yao et al. 2022, PromptingGuide.ai
**Contexte** : Agents avec outils, Q&A necessitant recherche, workflows multi-outils

**Pattern** :
```
Pour chaque etape :
1. Thought : exprimer le raisonnement en cours
2. Action : choisir l'outil a appeler et avec quels parametres
3. Observation : analyser le retour de l'outil
4. Repeter jusqu'a pouvoir donner une reponse finale.

Ne jamais deviner — toujours utiliser un outil en cas de doute.
```

---

## 11. Prompt Chaining

**Source** : Anthropic, universel
**Contexte** : Taches a etapes logiques distinctes (rechercher → analyser → ecrire → verifier)

**Pattern** :
```
Etape 1 : Extraire les faits pertinents de <document>
→ Output : liste de faits
Etape 2 : Analyser les faits extraits
→ Output : analyse structuree
Etape 3 : Generer le rapport final a partir de l'analyse
→ Output : rapport formate
```

Chaque etape peut utiliser un modele different (haiku pour extraction, opus pour analyse).

---

## 12. RAG (Retrieval-Augmented Generation)

**Source** : Universel
**Contexte** : Precision factuelle, donnees proprietaires, connaissances au-dela du training

**Pattern** :
```xml
Repondre a la question en utilisant UNIQUEMENT les documents fournis.
Si la reponse n'est pas dans les documents, le signaler.

<documents>
  <document id="1" title="{{TITRE_1}}">
    {{CONTENU_1}}
  </document>
  <document id="2" title="{{TITRE_2}}">
    {{CONTENU_2}}
  </document>
</documents>

<question>
  {{QUESTION}}
</question>

Citer l'ID du document pour chaque affirmation.
```

---

## 13. Constitutional AI (Auto-Critique)

**Source** : Anthropic Research
**Contexte** : Securite, precision, conformite a des valeurs/normes

**Pattern** :
```
Etape 1 — Generer la reponse initiale :
  [Prompt original]

Etape 2 — Auto-critique :
  Relire la reponse en verifiant :
  - Exactitude factuelle
  - Conformite au programme de {{NIVEAU}}
  - Absence d'erreurs mathematiques
  - Adaptation au public cible
  Lister les problemes trouves.

Etape 3 — Revision :
  Reecrire la reponse en corrigeant tous les problemes identifies.
  Retourner uniquement la version amelioree.
```

---

## 14. Reflexion

**Source** : PromptingGuide.ai
**Contexte** : Code complexe, raisonnement multi-etapes, taches verifiables

**Pattern** :
```
Tentative 1 :
  [Resoudre le probleme]

Reflexion :
  Analyser la tentative. Qu'est-ce qui a echoue ?
  Quels cas limites ont ete manques ?
  Que faire differemment ?

Tentative 2 :
  Resoudre a nouveau en integrant la reflexion.
```

---

## 15. Meta-Prompting (APE)

**Source** : OpenAI Cookbook, IBM Think, PromptingGuide.ai
**Contexte** : Optimisation de prompts a echelle, creation de templates

**Pattern APE (Automatic Prompt Engineer)** :
```
System: Expert en prompt engineering.

User:
  Description de la tache : [decrire ce que l'IA doit faire]
  Generer 3 prompts candidats diversifies pour cette tache.
  Pour chacun, expliquer pourquoi il fonctionnerait bien.
  Evaluer lequel performerait le mieux et pourquoi.
  Produire le prompt final optimise.
```

**Pattern structural (meta-template)** :
```
Tu es un expert en [DOMAINE].
Ta tache est de [VERBE] un(e) [TYPE_SORTIE].
Le/La [TYPE_SORTIE] doit :
  - [CONTRAINTE_1]
  - [CONTRAINTE_2]
Utiliser le format [FORMAT].
Voici l'input : [INPUT]
```

---

## 16. Adaptive Thinking (Claude 4.x)

**Source** : Anthropic (specifique Claude Opus 4.6 / Sonnet 4.6)
**Contexte** : Taches autonomes complexes

Mode `adaptive` : Claude decide dynamiquement quand et combien penser.

**Niveaux d'effort** :
- `low` — rapide, volume eleve, latence faible
- `medium` — la plupart des applications
- `high` — agents autonomes, coding complexe
- `max` — problemes les plus difficiles

**Prompt pour guider le thinking** :
```
Apres reception des resultats d'outil, reflechir attentivement a leur
qualite et determiner les prochaines etapes optimales avant de continuer.
```

**Prompt pour limiter l'overthinking** :
```
Prioriser l'execution sur la deliberation. Choisir une approche et
commencer immediatement. Ne pas comparer les alternatives avant d'ecrire.
```

---

## 17. Prefix Prompting (Gemini)

**Source** : Google Gemini
**Contexte** : Controle du format de sortie, traduction

**Pattern** :
```
English: The cat sat on the mat.
French: Le chat etait assis sur le tapis.
English: {{INPUT}}
French:
```

Le prefixe de sortie oriente le modele vers le format attendu.

---

## 18. Agentic 3-Reminders (OpenAI)

**Source** : OpenAI GPT-4.1 Guide (amelioration ~20% sur SWE-bench)
**Contexte** : Tout workflow agentic/autonome

Les 3 rappels critiques :
```
1. PERSISTENCE :
   "Continuer jusqu'a resolution complete avant de terminer le tour."

2. ANTI-HALLUCINATION :
   "Utiliser les outils pour lire les fichiers plutot que deviner."

3. PLANIFICATION :
   "Planifier avant chaque appel d'outil. Reflechir a ce qu'il faut
   faire et pourquoi avant d'agir."
```

---

## 19. State Management

**Source** : Anthropic, OpenAI
**Contexte** : Taches longues multi-contexte, agents autonomes

**Pattern** :
```json
// state.json — etat structure
{
  "progress": {"done": 15, "total": 50},
  "findings": ["bug A fixe", "test B echoue"],
  "next_steps": ["investiguer test B"]
}
```

```
// progress.txt — notes freeform
Session 3:
- Fixe validation token
- NEXT: investiguer echecs test #2
- IMPORTANT: Ne pas supprimer les tests
```

---

## 20. System Prompt Architecture (Mega-Prompts)

**Source** : Synthese tous providers
**Contexte** : Applications production, system prompts complexes

**Structure recommandee** :
```
1. IDENTITE ET ROLE (qui es-tu)
2. OBJECTIFS PRINCIPAUX (quoi accomplir)
3. REGLES COMPORTEMENTALES
   - Style de communication
   - Usage des outils
   - Politique d'action (agir vs demander)
   - Actions interdites
4. INSTRUCTIONS PAR TYPE DE TACHE
5. FORMAT DE SORTIE
6. EXEMPLES (2-5 scenarios)
7. CONTEXTE (documents, donnees)
8. RAPPEL FINAL (instruction la plus importante)
```

**Principe cle** : Plus specifique > plus complet. Un system prompt concentre de 500 tokens surpasse un prompt diffus de 3000 tokens.

---

## 21-23. Techniques Educatives (specifiques prof de maths)

### 21. Progression pedagogique
```
Organiser le contenu du simple au complexe.
Specifier les prerequis necessaires pour chaque notion.
Introduire une seule difficulte nouvelle par exercice.
```

### 22. Didactique mathematiques
```
TOUS les chiffres/valeurs/coefficients doivent etre DISTINCTS
quand on demande d'en identifier un specifique.
Les distracteurs QCM = erreurs reelles d'eleves, pas valeurs aleatoires.
Forcer des nombres a 4 chiffres avec variables separees pour
les questions chiffre/nombre.
```

### 23. Ancrage programme officiel
```
Chaque exercice doit reference une competence du programme :
- Domaine : {{DOMAINE}} (nombres, geometrie, grandeurs, etc.)
- Competence : {{COMPETENCE}}
- Capacite : {{CAPACITE}}
Utiliser le skill programmes-officiels pour sourcer.
```
