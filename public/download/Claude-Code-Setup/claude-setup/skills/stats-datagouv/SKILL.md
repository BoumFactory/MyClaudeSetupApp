---
name: stats-datagouv
description: >
  Ce skill s'utilise quand l'utilisateur demande de « créer un exercice de statistiques »,
  un « exercice avec données réelles », d'« utiliser data.gouv », un « exercice de probabilités
  avec données réelles », des « stats avec MCP datagouv », un « exercice moyenne médiane quartiles »,
  un « TP statistiques », un « exercice de pourcentages avec données INSEE », ou mentionne
  data.gouv.fr, le MCP datagouv, les statistiques descriptives ou des probabilités avec des données authentiques.
  Génère des exercices de maths (statistiques, probabilités, proportionnalité)
  à partir de données réelles extraites du portail open data data.gouv.fr via le serveur MCP DataGouv.
version: 0.4.0
---

# Exercices de statistiques avec données réelles (MCP DataGouv)

## Avant la première utilisation

Ce skill a besoin du **serveur MCP officiel de data.gouv.fr** : gratuit, données publiques de l'État, sans compte.

1. Lancer **une seule fois** dans un terminal (pas dans Claude Code) :
   ```
   claude mcp add --transport http --scope user datagouv https://mcp.data.gouv.fr/mcp
   ```
   L'option `--scope user` rend le serveur disponible dans tous les projets.
2. Redémarrer Claude Code.
3. Taper `/mcp` et vérifier que `datagouv` apparaît comme connecté.

**Consigne pour Claude** : si les outils `mcp__datagouv__*` sont absents, ne pas continuer sans données. Proposer d'abord cette commande à l'utilisateur, puis attendre le redémarrage.

Outils disponibles une fois le serveur connecté :
- `mcp__datagouv__search_datasets` : recherche par mots-clés
- `mcp__datagouv__get_dataset_info` : métadonnées d'un jeu de données
- `mcp__datagouv__list_dataset_resources` : fichiers disponibles
- `mcp__datagouv__get_resource_info` : détails d'une ressource (vérifier l'API Tabulaire)
- `mcp__datagouv__query_resource_data` : interroger les données CSV/XLSX

Générer des exercices de mathématiques contextuels et motivants en exploitant des données
réelles du portail national open data data.gouv.fr.

## Workflow principal

### Étape 1 — Collecter les paramètres

Déterminer auprès de l'utilisateur :
- **Thème** : population, climat, transports, éducation, économie…
- **Niveau scolaire** : 6e, 5e, 4e, 3e, 2nde, 1re, Terminale
- **Notions cibles** : moyenne, médiane, étendue, quartiles, écart-type, fréquences, probabilités…
- **Format** : exercice court (4-6 questions), TP long (10+ questions), DM
- **Sortie** : LaTeX (bfcours) ou HTML

Si l'utilisateur ne précise pas tout, proposer des valeurs par défaut adaptées.

### Étape 2 — Explorer via le MCP (recherche uniquement)

Le MCP sert **uniquement à explorer et identifier** le bon jeu de données :

1. Appeler `search_datasets` avec des mots-clés adaptés au thème
2. Examiner les 3-5 premiers résultats pertinents
3. Appeler `list_dataset_resources` pour lister les fichiers CSV/XLSX
4. Appeler `get_resource_info` pour obtenir **l'URL de téléchargement direct** du fichier

**Objectif de cette étape : obtenir l'URL brute du fichier CSV/XLSX.**

Consulter `references/datasets-catalogue.md` pour des jeux de données pré-identifiés par thème.

### Étape 3 — Télécharger et traiter les données brutes (scripts)

**Principe fondamental : la chaîne de vérité part du fichier brut téléchargé.**

Créer le dossier de l'exercice et son sous-dossier `_data/`, puis exécuter le pipeline
(chemins des scripts relatifs au dossier du skill) :

#### 3a. Télécharger le fichier brut

Exécuter `scripts/download.py` :
```bash
python scripts/download.py \
  --url "https://www.data.gouv.fr/fr/datasets/r/{resource_id}" \
  --output _data/raw_file.csv \
  --source-json _data/source.json \
  --dataset-id "xxx" \
  --dataset-title "Licences sportives" \
  --resource-id "yyy" \
  --producer "Ministere des Sports"
```

Produit :
- `_data/raw_file.csv` (ou `.xlsx`) : le fichier **tel quel** depuis data.gouv.fr
- `_data/source.json` : métadonnées de provenance (URL, date, identifiants)

#### 3b. Filtrer et extraire le sous-ensemble

Exécuter `scripts/extract.py` :
```bash
python scripts/extract.py \
  --input _data/raw_file.csv \
  --output _data/extract.csv \
  --columns "federation,nb_licences,pct_femmes" \
  --filter "annee==2024" \
  --limit 20 \
  --sort "nb_licences desc"
```

Produit :
- `_data/extract.csv` : sous-ensemble filtré (ce qui sera utilisé dans l'exercice)
- `_data/extract.json` : même contenu en JSON (pour `verify.py`)
- `_data/extract_params.json` : paramètres de filtrage appliqués (reproductibilité)

#### 3c. Construire la chaîne de vérification

Après rédaction du corrigé, écrire `_data/computed.json` en déclarant chaque calcul :

```json
{
  "exercice": "Exo_probas_licences_sportives",
  "source_file": "extract.csv",
  "calculs": [
    {
      "question": "Q1",
      "operation": "sum",
      "column": "nb_licences",
      "result": 4000000
    },
    {
      "question": "Q3",
      "operation": "ratio",
      "input_values": [2200000, 4000000],
      "result": 0.55
    }
  ]
}
```

#### 3d. Vérifier

```bash
python scripts/verify.py _data/
```

Relit `extract.csv` + `computed.json`, recalcule tout, affiche OK/FAIL par question.

**Arborescence `_data/` finale :**
```
_data/
├── source.json           # provenance (URL, IDs, date de téléchargement)
├── raw_file.csv          # fichier brut téléchargé tel quel
├── extract.csv           # sous-ensemble filtré pour l'exercice
├── extract.json          # idem en JSON
├── extract_params.json   # paramètres de filtrage (reproductibilité)
└── computed.json         # déclaration des calculs du corrigé
```

### Étape 4 — Générer l'exercice

Structure type d'un exercice :

1. **Chapeau contextuel** (2-3 lignes) : d'où viennent les données, pourquoi c'est intéressant
2. **Tableau de données** : présentation claire des valeurs extraites
3. **Questions progressives** (4-6 pour un exercice, 8-12 pour un TP) :
   - Q1-Q2 : lecture de données, calculs simples (effectifs, fréquences)
   - Q3-Q4 : indicateurs statistiques (moyenne, médiane, étendue)
   - Q5-Q6 : interprétation, comparaison, esprit critique
4. **Source** : « Source : data.gouv.fr — {nom du jeu de données} ({producteur}, {année}) »

Adapter le vocabulaire et la complexité au niveau. Voir `references/notions-par-niveau.md`.

### Étape 5 — Produire le corrigé

Pour chaque question :
- Calcul détaillé étape par étape
- Résultat encadré ou mis en valeur
- Phrase de conclusion interprétant le résultat dans le contexte

**Chaque calcul du corrigé DOIT avoir une entrée correspondante dans `computed.json`.**

### Étape 6 — Vérifier la chaîne

Exécuter `verify.py` pour confirmer que tous les calculs du corrigé sont cohérents
avec les données brutes. Si un test échoue, corriger le corrigé avant de livrer.

**Arborescence finale produite :**
```
Exo_probas_licences_sportives/
├── Exo_probas_licences_sportives.tex   # fichier principal (EXO avec \exocorrection)
├── enonce.tex                          # ou .html
└── _data/
    ├── source.json
    ├── raw_file.csv
    ├── extract.csv
    ├── extract.json
    ├── extract_params.json
    └── computed.json
```

Le corrigé n'est **jamais** un fichier séparé : il se place après `\exocorrection` dans l'environnement `EXO`.

## Contraintes de qualité

- **Vérifier les calculs** : recalculer moyenne, médiane, quartiles sur les données extraites
- **Cohérence des unités** : toujours préciser les unités (habitants, euros, km, degrés…)
- **Arrondis** : adapter au niveau (entiers en 6e-5e, 1 décimale en 4e-3e, 2 au lycée)
- **Citation obligatoire** : toute donnée data.gouv.fr doit être sourcée
- **Programme** : se limiter aux outils du programme officiel du niveau visé

## Limites techniques à connaître

- API Tabulaire : CSV ≤ 100 Mo, XLSX ≤ 12,5 Mo
- Pagination : 200 lignes maximum par requête (itérer si besoin)
- Pas de jointures entre jeux de données
- Qualité des données variable selon les producteurs

## Intégration LaTeX (bfcours)

Pour la sortie LaTeX, charger le skill `bfcours-latex` (et `choix-didactiques` pour le fond). Environnements réels du paquet :

- `EXO` pour l'exercice **et** son corrigé : `\def\rdifficulty{n}` (1 à 3) avant, `\begin{EXO}{Titre sans virgule ni math}{code_competence}`, énoncé, puis `\exocorrection`, puis la correction, `\end{EXO}`
- `\tcbitempoint{n}` pour les points de chaque question, `\acc{Calculer}` pour les verbes d'action et la forme de réponse attendue
- `tcbenumerate` pour les questions (jamais `enumerate`), `MultiColonnes` pour la mise en page
- `tcbtab` pour les tableaux de données (jamais `tabular`) : la première ligne est l'en-tête, pas de virgule dans le titre
- Au collège, espaces réponses (`\repsim`, `\tcfillcrep`, `crep`) ; au lycée, seulement sur demande

Gabarit :

```latex
\def\rdifficulty{1.5}
\begin{EXO}{Statistiques sur les licences sportives}{code_competence}
Chapeau : la Fédération… a publié le nombre de licenciés par sport.

\begin{tcbtab}[Licenciés par fédération en 2024]{l|c}
Fédération & Licenciés\\
\hline
Football & 2\,200\,000\\
Tennis & 1\,000\,000\\
\end{tcbtab}

\begin{tcbenumerate}
    \tcbitem \tcbitempoint{1}\acc{Calculer} le nombre total de licenciés.
    \tcbitem \tcbitempoint{2}\acc{Calculer} la proportion de licenciés au football, \acc{en pourcentage arrondi à l'unité}.
\end{tcbenumerate}

{\footnotesize Source : data.gouv.fr — Licences sportives (Ministère des Sports, 2024)}

\exocorrection

\begin{tcbenumerate}
    \tcbitem $2\,200\,000 + 1\,000\,000 = 3\,200\,000$.
    \tcbitem $\dfrac{2\,200\,000}{3\,200\,000} \approx 69\,\%$.
\end{tcbenumerate}
\end{EXO}
```

Diagrammes éventuels en TikZ/pgfplots.

## Ressources additionnelles

### Fichiers de référence

- **`references/datasets-catalogue.md`** : jeux de données pré-identifiés par thème avec mots-clés de recherche
- **`references/notions-par-niveau.md`** : notions statistiques par niveau scolaire (6e à Terminale) avec attendus du programme

### Scripts du pipeline

- **`scripts/download.py`** : télécharge le fichier brut et génère `source.json`
- **`scripts/extract.py`** : filtre, sélectionne les colonnes, trie, exporte `extract.csv` et `extract.json`
- **`scripts/verify.py`** : vérifie `computed.json` contre `extract.csv`, affiche OK/FAIL
