---
name: stats-datagouv
description: >
  This skill should be used when the user asks to "creer un exercice de statistiques",
  "exercice avec donnees reelles", "utiliser data.gouv", "exercice probabilites donnees reelles",
  "stats avec MCP datagouv", "exercice moyenne mediane quartiles", "TP statistiques",
  "exercice pourcentages donnees INSEE", or mentions data.gouv.fr, MCP datagouv,
  statistiques descriptives, ou probabilites avec des donnees authentiques.
  Genere des exercices de maths (statistiques, probabilites, proportionnalite)
  a partir de donnees reelles extraites du portail open data data.gouv.fr via le serveur MCP DataGouv.
version: 0.3.0
---

# Exercices de Statistiques avec Donnees Reelles (MCP DataGouv)

Generer des exercices de mathematiques contextuels et motivants en exploitant des donnees
reelles du portail national open data data.gouv.fr, via le serveur MCP DataGouv.

## Prerequis

Le serveur MCP DataGouv doit etre configure dans Claude Code :
```
claude mcp add --transport http datagouv https://mcp.data.gouv.fr/mcp
```

Outils MCP disponibles apres configuration :
- `mcp__datagouv__search_datasets` — Recherche par mots-cles
- `mcp__datagouv__get_dataset_info` — Metadonnees d'un dataset
- `mcp__datagouv__list_dataset_resources` — Fichiers disponibles
- `mcp__datagouv__get_resource_info` — Details d'une ressource (verifier API Tabulaire)
- `mcp__datagouv__query_resource_data` — Interroger les donnees CSV/XLSX

## Workflow principal

### Etape 1 — Collecter les parametres

Determiner aupres de l'utilisateur :
- **Theme** : population, climat, transports, education, economie...
- **Niveau scolaire** : 6e, 5e, 4e, 3e, 2nde, 1ere, Terminale
- **Notions cibles** : moyenne, mediane, etendue, quartiles, ecart-type, frequences, probabilites...
- **Format** : exercice court (4-6 questions), TP long (10+ questions), DM
- **Sortie** : LaTeX (bfcours) ou HTML

Si l'utilisateur ne precise pas tout, proposer des valeurs par defaut adaptees.

### Etape 2 — Explorer via MCP (recherche uniquement)

Le MCP sert **uniquement a explorer et identifier** le bon dataset :

1. Appeler `search_datasets` avec des mots-cles adaptes au theme
2. Examiner les 3-5 premiers resultats pertinents
3. Appeler `list_dataset_resources` pour lister les fichiers CSV/XLSX
4. Appeler `get_resource_info` pour obtenir **l'URL de telechargement direct** du fichier

**Objectif de cette etape : obtenir l'URL brute du fichier CSV/XLSX.**

Consulter `references/datasets-catalogue.md` pour des datasets pre-identifies par theme.

### Etape 3 — Telecharger et traiter les donnees brutes (scripts)

**Principe fondamental : la chaine de verite part du fichier brut telecharge.**

Creer le dossier de l'exercice et son sous-dossier `_data/`, puis executer le pipeline :

#### 3a. Telecharger le fichier brut

Executer `scripts/download.py` :
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
- `_data/raw_file.csv` (ou `.xlsx`) — le fichier **tel quel** depuis data.gouv.fr
- `_data/source.json` — metadonnees de provenance (URL, date, IDs)

#### 3b. Filtrer et extraire le sous-ensemble

Executer `scripts/extract.py` :
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
- `_data/extract.csv` — sous-ensemble filtre (ce qui sera utilise dans l'exercice)
- `_data/extract.json` — meme contenu en JSON (pour verify.py)
- `_data/extract_params.json` — parametres de filtrage appliques (reproductibilite)

#### 3c. Construire la chaine de verification

Apres redaction du corrige, executer `scripts/build_computed.py` ou ecrire
manuellement `_data/computed.json` en declarant chaque calcul :

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

#### 3d. Verifier

```bash
python scripts/verify.py _data/
```

Relit `extract.csv` + `computed.json`, recalcule tout, affiche OK/FAIL par question.

**Arborescence `_data/` finale :**
```
_data/
├── source.json           # provenance (URL, IDs, date telechargement)
├── raw_file.csv          # fichier brut telecharge tel quel
├── extract.csv           # sous-ensemble filtre pour l'exercice
├── extract.json          # idem en JSON
├── extract_params.json   # parametres de filtrage (reproductibilite)
├── computed.json         # declaration des calculs du corrige
└── verify.py             # copie locale du script de verification
```

### Etape 4 — Generer l'exercice

Structure type d'un exercice :

1. **Chapeau contextuel** (2-3 lignes) : d'ou viennent les donnees, pourquoi c'est interessant
2. **Tableau de donnees** : presentation claire des valeurs extraites
3. **Questions progressives** (4-6 pour un exercice, 8-12 pour un TP) :
   - Q1-Q2 : lecture de donnees, calculs simples (effectifs, frequences)
   - Q3-Q4 : indicateurs statistiques (moyenne, mediane, etendue)
   - Q5-Q6 : interpretation, comparaison, esprit critique
4. **Source** : "Source : data.gouv.fr — {nom du dataset} ({producteur}, {annee})"

Adapter le vocabulaire et la complexite au niveau. Voir `references/notions-par-niveau.md`.

### Etape 5 — Produire le corrige

Pour chaque question :
- Calcul detaille etape par etape
- Resultat encadre ou mis en valeur
- Phrase de conclusion interpretant le resultat dans le contexte

**Chaque calcul du corrige DOIT avoir une entree correspondante dans `computed.json`.**

### Etape 6 — Verifier la chaine

Executer `verify.py` pour confirmer que tous les calculs du corrige sont coherents
avec les donnees brutes. Si un test echoue, corriger le corrige avant de livrer.

**Arborescence finale produite :**
```
Exo_probas_licences_sportives/
├── enonce.tex              # ou .html
├── corrige.tex
└── _data/
    ├── source.json         # provenance (URL, IDs, date)
    ├── raw_file.csv        # fichier brut data.gouv.fr
    ├── extract.csv         # sous-ensemble filtre
    ├── extract.json        # idem JSON
    ├── extract_params.json # filtres appliques
    ├── computed.json       # calculs du corrige
    └── verify.py           # script de test
```

## Contraintes de qualite

- **Verifier les calculs** : recalculer moyenne, mediane, quartiles sur les donnees extraites
- **Coherence des unites** : toujours preciser les unites (habitants, euros, km, degres...)
- **Arrondis** : adapter au niveau (entiers en 6e-5e, 1 decimale en 4e-3e, 2 en lycee)
- **Citation obligatoire** : toute donnee data.gouv.fr doit etre sourcee

## Limites techniques a connaitre

- API Tabulaire : CSV <= 100 Mo, XLSX <= 12,5 Mo
- Pagination : max 200 lignes par requete (iterer si besoin)
- Pas de jointures entre datasets
- Qualite des donnees variable selon les producteurs

## Integration LaTeX (bfcours)

Pour la sortie LaTeX, utiliser les environnements bfcours :
- `\begin{exercice}` pour l'enonce
- `\begin{corrige}` pour le corrige
- `\begin{tabular}` pour les tableaux de donnees
- Commandes TikZ/pgfplots pour les diagrammes si demandes

## Ressources additionnelles

### Fichiers de reference

- **`references/datasets-catalogue.md`** — Datasets pre-identifies par theme avec IDs et mots-cles de recherche
- **`references/notions-par-niveau.md`** — Notions statistiques par niveau scolaire (6e a Terminale) avec attendus du programme

### Scripts du pipeline

- **`scripts/download.py`** — Telecharge le fichier brut et genere source.json
- **`scripts/extract.py`** — Filtre, selectionne colonnes, trie, exporte extract.csv + extract.json
- **`scripts/verify.py`** — Verifie computed.json contre extract.csv, affiche OK/FAIL
