---
name: bfcours-latex
description: Utiliser ce skill pour éditer des documents LaTeX éducatifs avec le package bfcours. Expertise spécialisée pour l'écriture de contenu pédagogique français (6ème à Terminale) incluant cours, exercices, évaluations, fiches et activités. Utiliser de manière proactive pour l'édition de contenu LaTeX bfcours.
---

# Expert Édition LaTeX BFCours

Système expert LaTeX pour éditer et enrichir des documents éducatifs de mathématiques avec le package bfcours. Ce skill se concentre sur l'écriture de contenu pédagogique de haute qualité en respectant les conventions bfcours.

## Objectif

Éditer du contenu LaTeX en respectant les conventions strictes du package bfcours pour l'enseignement des mathématiques. Produire du matériel pédagogique professionnel pour l'enseignement français de la 6ème à la Terminale.

## ⚠️ Séparation des Responsabilités

Ce skill se concentre **uniquement sur l'édition de contenu**. Pour les autres tâches :

- **Créer un nouveau projet** → Utiliser le skill `tex-document-creator`
- **Compiler un document** → Utiliser le skill `tex-compiling-skill`
- **Éditer le contenu** → Ce skill (bfcours-latex)

## Workflows Principaux

### Workflow 1 : Éditer un Document Complet avec Validation

Lors de l'édition de documents existants nécessitant une validation par compilation.

**Étapes :**

1. **Lire le document** et la structure du projet (fichier principal, enonce.tex, sections/, etc.)

2. **Charger les connaissances bfcours** depuis `references/bfcours-conventions.md` dans ce skill

3. **Lire les ressources fournies** par l'utilisateur si présentes pour référence

4. **Écrire/éditer le contenu** en utilisant les environnements didactiques bfcours (voir conventions ci-dessous)

5. **Compiler pour valider** : Déléguer au skill `tex-compiling-skill` :

   ```
   Utiliser tex-compiling-skill pour quick_compile()

   ```

6. **Corriger les erreurs de compilation de manière itérative** si nécessaire :
   - Analyser les messages d'erreur (via tex-compiling-skill)
   - Corriger les problèmes dans le contenu
   - Re-compiler

7. **Valider la sortie PDF** : Utiliser `pdf-analyzer-server: analyze_pdf()` pour vérifier le contenu rendu

8. **Vérifier les erreurs mathématiques** dans le PDF qui peuvent ne pas être visibles dans le code LaTeX

9. **Effectuer les corrections finales** si nécessaire

10. **Finaliser le fichier principal** (pour les documents de type Cours uniquement) :
   - Lire le fichier principal du projet (généralement `Nom_projet.tex`)
   - **Compléter le tableau des compétences travaillées** juste après `\tableofcontents` avec les vraies compétences identifiées dans le contenu
   - **Supprimer les placeholders** : retirer `\voc{nobug}` et `\competence{nobug}` qui ne sont que des marqueurs temporaires
   - Sauvegarder le fichier principal modifié

### Workflow 2 : Éditer un Fichier Unique (Sans Compilation)

Lors de l'édition d'un fichier de contenu LaTeX autonome sans besoin de compilation immédiate.

**Étapes :**

1. **Se documenter** sur les exigences de la tâche ou du matériel source

2. **Charger les connaissances bfcours** depuis `references/bfcours-conventions.md`

3. **Vérifier si le fichier existe** et le lire s'il est présent

4. **Écrire le contenu** en suivant les standards bfcours

5. **NE PAS compiler** (focus uniquement sur la création de contenu)

## Architecture de Projet

Les documents suivent cette structure standard :

```
Nom_projet/
├── Nom_projet.tex          # Fichier principal à compiler (nommé d'après le répertoire)
│                           # Contient les en-têtes et les inputs globaux
├── VERSION_Nom_projet.tex  # Variantes de version (ex : ELEVE_Nom_projet.tex) [optionnel]
├── enonce.tex              # Contenu principal (importé dans le fichier principal)
├── enonce_TOOLS.tex        # Si présent, remplace enonce.tex [optionnel]
├── enonce_figures.tex      # Figures TikZ indexées par \tikzfig{CODE}
├── images/                 # Répertoire d'images [optionnel]
│   └── *.png
├── sections/               # Pour les gros documents [optionnel]
│   └── fichiers.tex        # Contenu réparti en plusieurs fichiers
└── annexes/                # Scripts et fichiers secondaires [optionnels]
    └── scripts.py
```

**Note** : Cette structure est créée par le skill `tex-document-creator`. Ce skill se concentre sur l'édition des fichiers de contenu (enonce.tex, sections/, etc.)

## Résumé des Conventions BFCours

**Conventions critiques** à toujours suivre (voir `references/bfcours-conventions.md` pour tous les détails) :

### Environnements Structurels

1. **MultiColonnes** : Système de mise en page en grille

   ```latex
   \begin{MultiColonnes}{nbCol}[options]
       \tcbitem[raster multicolumn=2] Contenu large
       \tcbitem Contenu colonne 1
       \tcbitem Contenu colonne 2
   \end{MultiColonnes}

   ```

2. **tcbenumerate** : Énumération OBLIGATOIRE (remplace enumerate)

   ```latex
   \begin{tcbenumerate}[nbCol][nbStart][style]
       \tcbitem Premier item
       \tcbitem Deuxième item
   \end{tcbenumerate}

   ```

3. **tcbtab** : Tableaux OBLIGATOIRES (remplace tabular)

   ```latex
   \begin{tcbtab}[Titre]{l|c|r}
   Entête1 & Entête2 & Entête3\\
   \hline
   contenu & contenu & contenu\\
   \end{tcbtab}

   ```

### Commandes de Formatage de Texte

- **\acc{mot}** : Accentuation (REMPLACE \textbf) - couleur adaptative
- **\voc{mot}** : OBLIGATOIRE pour la première occurrence de vocabulaire dans les cours
- **\frquote{expr}** : Citations
- **a$^{\circ}$** : Notation des degrés (format OBLIGATOIRE)
- **\encadrer[couleur]{contenu}** : Encadrer les formules/résultats importants
- **Logique** : \Si, \Alors, \Donc, \Mais, \SSI, \Et
- **Ligatures** : TOUJOURS utiliser `\oe` au lieu du caractère Unicode œ (exemples : n\oe ud, c\oe ur, \oe il, s\oe ur, b\oe uf)

### Environnements Didactiques

Tout le contenu doit utiliser les environnements didactiques appropriés :

- **Definition** : Pour les définitions (met à jour les couleurs et la table des matières)
- **Propriete** : Pour les propriétés
- **Theoreme** : Pour les théorèmes
- **Demonstration** : Pour les démonstrations
- **Exemple** : Pour les exemples
- **Remarque** : Pour les remarques
- **Notation** : Pour les conventions de notation
- **Activite** : Pour les activités de découverte

**Syntaxe** :
```latex
\begin{Definition}[Titre Court]
contenu avec \acc{emphase} et \voc{vocabulaire}
\end{Definition}
```

### Environnement Exercice (EXO)

**⚠️ RÈGLE ABSOLUE : Environnement EXO OBLIGATOIRE**

L'environnement `EXO` est OBLIGATOIRE pour **TOUS les exercices**, y compris :
- Les exercices dans les feuilles d'exercices
- Les exercices dans les activités (environnement Activite)
- Les exercices dans les évaluations
- Les devoirs maison

**Principe fondamental** : Les corrections sont **toujours** intégrées après `\exocorrection` dans le même environnement EXO, **jamais dans un fichier séparé**.

**Critique pour tous les exercices** :

```latex
\def\rdifficulty{1.5}  % Échelle de 1 à 3
\begin{EXO}{Titre de Compétence - sans virgule}{code_competence}

Énoncé avec instructions claires.
\tcbitempoint{2}\acc{Calculer} la valeur...

\exocorrection

Contenu de la solution suivant la structure de l'énoncé.
\end{EXO}
```

**Attribution des points** avec \tcbitempoint :
- 1 point : Action basique (calcul, rappel, tâche simple)
- 2 points : Figure, tableau, production complexe
- Cumulatif : Plusieurs actions dans une question
- 5 points : Tâches de recherche (pas de cumul)

### Espaces Réponses pour les Élèves

1. **Ligne courte** : `\repsim[1.5cm]{contenu}`
2. **Ligne adaptative** : `\tcfillcrep{texte}`
3. **Multiligne** :

   ```latex
   \begin{crep}[extra lines=4]
   Contenu de réponse
   \end{crep}

   ```

## Intégration des Serveurs MCP

### Serveurs utilisés par ce skill

- **latex-search-server** : Trouver des commandes LaTeX et documentation de packages
  - `search_fuzzy_command(query)` : Recherche floue de commandes LaTeX
  - `search_exact_command(command)` : Documentation exacte de commande
  - `search_in_specific_package(package, query)` : Recherche spécifique au package

- **competences-server** : Cadre de compétences de l'éducation française
  - `advanced_search(query, niveau)` : Trouver les compétences pour sujet et niveau
  - `get_competence_by_code(code)` : Obtenir les détails d'une compétence spécifique
  - `filter_by_niveau(niveau)` : Lister les compétences pour un niveau

### Serveurs délégués à d'autres skills

- **document-creator-server** → Skill `tex-document-creator`
- **latex-compiler-server** → Skill `tex-compiling-skill`

## Niveaux Scolaires

Niveaux du système éducatif français :

**Collège** :
- 6eme (Sixième) - `$\mathbf{6^{\text{ème}}}$`
- 5eme (Cinquième) - `$\mathbf{5^{\text{ème}}}$`
- 4eme (Quatrième) - `$\mathbf{4^{\text{ème}}}$`
- 3eme (Troisième) - `$\mathbf{3^{\text{ème}}}$`

**Lycée** :
- 2nde (Seconde) - `$\mathbf{2^{\text{nde}}}$`
- 1ere_spe (Première spécialité) - `$\mathbf{1^{\text{ère}}}$`
- Terminale - `$\mathbf{T^{\text{Le}}}$`

## Meilleures Pratiques

1. **Toujours utiliser les environnements bfcours** : Ne jamais utiliser les environnements LaTeX standard enumerate, itemize ou tabular. Utiliser tcbenumerate, MultiColonnes et tcbtab.

2. **Chargement progressif** :
   - Lire `references/bfcours-conventions.md` pour les conventions essentielles
   - Lire `references/exemples-usecases.md` pour des exemples professionnels si nécessaire
   - Utiliser Grep pour chercher des patterns spécifiques dans les exemples

3. **Validation par compilation** : Pour les documents complets, utiliser le skill `tex-compiling-skill` pour compiler et valider la sortie PDF.

4. **Intégration des compétences** : Toujours chercher et intégrer les compétences pertinentes depuis `competences-server` pour les exercices et évaluations.

5. **Emphase du vocabulaire** : Dans les cours (documents Cours), TOUJOURS utiliser `\voc{mot}` pour la première occurrence des termes de vocabulaire.

6. **Accentuation du texte** : Remplacer tous les `\textbf{}` par `\acc{}` pour une emphase colorée adaptative.

7. **Accentuation dans les énoncés d'exercices** : L'accentuation `\acc{}` est OBLIGATOIRE pour **DEUX éléments** :
   - **Les verbes d'action** : `\acc{Calculer}`, `\acc{Déterminer}`, `\acc{Résoudre}`, etc.
   - **La forme de réponse attendue** : `\acc{résultat simplifié}`, `\acc{sous forme d'intervalle(s)}`, `\acc{justifier le signe}`, etc.

   **Exemples corrects** :
   ```latex
   \tcbitempoint{2}\acc{Calculer} les valeurs suivantes en donnant un \acc{résultat simplifié} :
   \tcbitempoint{3}\acc{Résoudre} et donner l'ensemble des solutions \acc{sous forme d'intervalle(s)} :
   \tcbitempoint{2}\acc{Simplifier} les expressions suivantes (\acc{justifier le signe}) :
   ```

8. **Première ligne des tableaux** : Dans `tcbtab`, la première ligne EST l'en-tête (pas de `\hline` initial nécessaire, contrairement à tabular).

9. **Attribution des points** : Être réfléchi avec `\tcbitempoint{}` pour refléter avec précision la complexité de la tâche.

## Références de la Base de Connaissances

Ce skill inclut des références groupées dans le répertoire `references/` :

- **bfcours-conventions.md** : Conventions complètes du package bfcours (charger pour tous les workflows)
- **exemples-usecases.md** : Exemples professionnels réels de la séquence polynômes (utiliser Grep pour chercher des patterns spécifiques)

Charger ces références selon les besoins pendant les workflows en utilisant l'outil Read. Pour les documents volumineux, utiliser Grep avec des patterns de recherche spécifiques plutôt que de lire les fichiers entiers.

## Exemples d'Utilisation

### Exemple 1 : Éditer un cours existant

```
Utilisateur : "Ajoute une section sur les équations du second degré"

Workflow : Éditer un Document Complet avec Validation
1. Lire la structure actuelle du cours
2. Charger bfcours-conventions.md
3. Écrire une nouvelle section avec environnements Definition, Propriete, Exemple
4. Utiliser \voc{} pour le vocabulaire, \acc{} pour l'emphase
5. Déléguer compilation au skill tex-compiling-skill
6. Vérifier les erreurs mathématiques dans le PDF via pdf-analyzer
7. Effectuer corrections finales si nécessaire
```

### Exemple 2 : Édition rapide de fichier

```
Utilisateur : "Écris 3 exercices dans enonce.tex"

Workflow : Éditer un Fichier Unique (Sans Compilation)
1. Charger bfcours-conventions.md
2. Lire enonce.tex s'il existe
3. Chercher compétences pertinentes avec competences-server
4. Écrire les exercices en utilisant l'environnement EXO avec \tcbitempoint
5. Terminé (pas de compilation)
```

### Exemple 3 : Enrichir un document avec compétences

```
Utilisateur : "Ajoute les codes de compétences aux exercices sur les vecteurs en 1ère"

1. Lire le document
2. Utiliser competences-server: advanced_search("vecteurs", "1ere_spe")
3. Identifier les compétences pertinentes
4. Éditer chaque environnement EXO pour ajouter le code compétence
5. Valider avec compilation (déléguer à tex-compiling-skill)
```

## Intégration du Barème (Évaluations)

Après la rédaction d'une évaluation, utiliser le skill `bareme-actions-eleves` pour :

1. **Atomiser la correction** en actions élèves distinctes
2. **Appliquer les coefficients** selon le type d'exercice (1 pour calcul, 0.5 pour géométrie)
3. **Générer le fichier `bareme.json`** pour la correction interactive
4. **Analyser la densité** de l'évaluation (actions / note cible)

### Correspondance avec \tcbitempoint

| Ce que vous écrivez | Ce que ça signifie |
|---------------------|-------------------|
| `\tcbitempoint{3}` | 3 actions élèves attendues pour cette question |

**Recommandation** : Toujours rédiger la correction (`\exocorrection`) **avant** d'attribuer les points. L'atomisation de la correction donne le nombre exact d'actions.

### Workflow Évaluation Complet

1. Rédiger l'évaluation avec `bfcours-latex`
2. Rédiger les corrections dans chaque `EXO` après `\exocorrection`
3. Utiliser `/bareme` ou le skill `bareme-actions-eleves` pour générer le barème
4. Corriger avec l'interface `bareme.html`

## Rappels Critiques

- JAMAIS utiliser les environnements LaTeX standard `enumerate`, `itemize` ou `tabular`
- TOUJOURS utiliser `\acc{}` au lieu de `\textbf{}`
- TOUJOURS accentuer les **verbes d'action** ET la **forme de réponse attendue** dans les énoncés
- TOUJOURS utiliser `\voc{}` pour la première occurrence de vocabulaire dans les cours
- TOUJOURS déléguer la compilation au skill `tex-compiling-skill`
- TOUJOURS vérifier les exemples usecases en cas de doute sur l'utilisation bfcours
- TOUJOURS intégrer les compétences pertinentes pour les exercices/évaluations
- TOUJOURS utiliser `bareme-actions-eleves` après rédaction d'une évaluation
- NE JAMAIS créer de nouveau projet (utiliser `tex-document-creator`)
