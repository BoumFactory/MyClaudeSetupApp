---
name: programmes-officiels
description: Rechercher et citer precisement les elements des programmes officiels de l'Education Nationale francaise (college et lycee). Utiliser pour sourcer les competences, capacites et contenus du programme dans les fiches pedagogiques et documents administratifs.
---

# Skill Programmes Officiels

Ce skill permet de rechercher, extraire et citer precisement les elements des programmes officiels de l'Education Nationale francaise pour les mathematiques du CM1 a la Terminale.

---

## DEMO RAPIDE (5 min)

Voici une sequence de commandes pour montrer les fonctionnalites principales :

```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026"

# 1. STATS GLOBALES - Vue d'ensemble
python ".claude/skills/programmes-officiels/scripts/search_competences.py" --stats

# 2. RECHERCHE PAR MOT-CLE - Ex: "Pythagore" tous niveaux
python ".claude/skills/programmes-officiels/scripts/search_competences.py" --keyword "pythagore" --all-levels

# 3. RECHERCHE PAR NIVEAU - Ex: Suites en 1ere Spe
python ".claude/skills/programmes-officiels/scripts/search_competences.py" --niveau 1S --keyword "suite"

# 4. RECHERCHE PAR DOMAINE - Ex: Geometrie en 3eme
python ".claude/skills/programmes-officiels/scripts/search_competences.py" --niveau 3 --domaine G

# 5. COMPETENCE PRECISE - Format detaille
python ".claude/skills/programmes-officiels/scripts/search_competences.py" --code 3G12 --format medium

# 6. OUVRIR LA SOURCE - Voir la page du BO
python ".claude/skills/programmes-officiels/scripts/open_source_page.py" --code 3G12

# 7. VALIDATION - Verifier coherence base
python ".claude/skills/programmes-officiels/scripts/validate_json_vs_source.py"
```

### Points forts a montrer

| Fonctionnalite | Commande demo |
|----------------|---------------|
| **5500+ competences** | `--stats` |
| **Recherche intelligente** | `--keyword "vecteur"` (trouve aussi "vectoriel") |
| **Multi-niveaux** | `--all-levels` |
| **Tracabilite BO** | `open_source_page.py --code XXX` |
| **Validation qualite** | `validate_json_vs_source.py` (90% OK) |

---

## REGLE ABSOLUE : UTILISER LES SCRIPTS

**JAMAIS acceder directement aux fichiers JSON** dans `data/extractions/`, `data/aggregated/` ou `data/normalized/`.

**TOUJOURS utiliser les scripts de recherche** pour interroger la base de competences.

---

## FORMAT DES CODES NORMALISES

```
[niveau][filiere][theme][index]-[palier]
```

### Exemples

| Code | Signification |
|------|---------------|
| `6N1` | 6eme, Nombres, competence 1 |
| `1SY16` | 1ere Spe, Analyse, competence 16 |
| `0EA5` | Term. Expert, Algebre, competence 5 |
| `3G12-2` | 3eme, Geometrie, competence 12, palier 2 |

---

## CODES DE NIVEAU

| Code | Niveau | Aliases |
|------|--------|---------|
| `6` | 6eme (C3) | C3, 6E |
| `5` | 5eme | 5E |
| `4` | 4eme | 4E |
| `3` | 3eme | 3E |
| `2G` | 2nde GT | 2GT, SECONDE |
| `2H` | 2nde STHR | 2STHR |
| `1S` | 1ere Spe | 1SPE, PREMIERE |
| `1T` | 1ere Techno | 1TECHNO |
| `1E` | 1ere Ens.Sci | 1ENS_SCI |
| `0S` | Term. Spe | TSPE, TERMINALE |
| `0C` | Term. Comp | TCOMP |
| `0E` | Term. Expert | TEXP |
| `0T` | Term. Techno | TTECHNO |

---

## CODES DE DOMAINE

| Lettre | Domaine |
|--------|---------|
| `N` | Nombres |
| `A` | Algebre |
| `Y` | Analyse (analYse) |
| `L` | Algorithmique (aLgorithmique) |
| `G` | Geometrie |
| `R` | Grandeurs (gRandeurs) |
| `S` | Statistiques |
| `P` | Probabilites |
| `T` | Trigonometrie |
| `O` | Logique (lOgique) |

---

## SCRIPTS DE RECHERCHE

### Script principal

```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026"
python ".claude/skills/programmes-officiels/scripts/search_competences.py" [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--niveau 1S` | Niveau (code ou alias) |
| `--keyword "suite"` | Recherche par mot-cle (avec synonymes par defaut) |
| `--domaine Y` | Filtrer par domaine (lettre ou nom) |
| `--code 1SY16` | Recherche par code exact |
| `--all-levels` | Rechercher tous niveaux |
| `--exact` | Recherche exacte (desactive les synonymes) |
| `--limit 20` | Limite de resultats (defaut: 20) |
| `--format json` | Format: short, medium, json |
| `--stats` | Statistiques globales |
| `--list-niveaux` | Lister les niveaux |
| `--list-domaines` | Lister les domaines |
| `--list-synonyms` | Lister les synonymes de recherche |

### Exemples

```bash
# Suites en 1ere Spe
python search_competences.py --niveau 1S --keyword "suite" --format json

# Nombres en 6eme
python search_competences.py --niveau 6 --domaine N

# Recherche par code exact
python search_competences.py --code 1SY16 --format medium

# Pythagore tous niveaux
python search_competences.py --keyword "pythagore" --all-levels

# Statistiques
python search_competences.py --stats
```

---

## STATISTIQUES

**Total : 4017 competences**

| Niveau | Code | Competences |
|--------|------|-------------|
| 6eme (C3) | 6 | 906 |
| 5eme | 5 | 309 |
| 4eme | 4 | 205 |
| 3eme | 3 | 197 |
| 2nde GT | 2G | 232 |
| 2nde STHR | 2H | 276 |
| 1ere Spe | 1S | 213 |
| 1ere Techno | 1T | 317 |
| 1ere Ens.Sci | 1E | 163 + 169 |
| Term. Spe | 0S | 476 + 246 |
| Term. Comp | 0C | 70 |
| Term. Expert | 0E | 207 |
| Term. Techno | 0T | 18 |

---

## FORMAT JSON DES COMPETENCES

```json
{
  "code": "1SY16",
  "old_code": "1SPE-AN-311",
  "intitule": "Definir une suite arithmetique",
  "niveau": "1S",
  "domaine": "Y",
  "domaine_nom": "ANALYSE",
  "sous_domaine": "Suites numeriques",
  "type": "contenu",
  "description": "Connaitre la definition d'une suite arithmetique",
  "formulation_bo": "Suites arithmetiques : exemples, definition",
  "source": {
    "pdf": "1GT.pdf",
    "page": 5
  }
}
```

Le champ `source` indique le PDF et la page d'origine de la competence dans le BO.

### Types de competences

- `contenu` : Definitions, proprietes, theoremes
- `capacite` : Savoir-faire, applications
- `demonstration` : Preuves exigibles au programme
- `algorithme` : Programmes Python/Scratch attendus
- `approfondissement` : Extensions non obligatoires

---

## OUVRIR LA PAGE SOURCE

Le script `open_source_page.py` permet d'ouvrir directement la page PDF d'origine d'une competence.

### Usage

```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026"
python ".claude/skills/programmes-officiels/scripts/open_source_page.py" --code 5G40
```

### Options

| Option | Description |
|--------|-------------|
| `--code 5G40` | Code de la competence a consulter |
| `--viewer edge` | Visualiseur (auto, vscode, edge, chrome, default_pdf) |
| `--folder` ou `-f` | Ouvrir le dossier (pour naviguer vers pages suivantes) |
| `--list-viewers` | Lister les visualiseurs disponibles |
| `--set-default vscode` | Definir le visualiseur par defaut |
| `--info` | Afficher les infos sans ouvrir le PDF |

### Configuration

Le fichier `config.json` a la racine du skill permet de configurer :

```json
{
  "viewer": {
    "default": "auto",
    "preferences": ["vscode", "edge", "chrome"]
  }
}
```

- `auto` : Detection automatique du meilleur visualiseur
- `vscode` : VS Code (necessite extension PDF)
- `edge` : Microsoft Edge
- `chrome` : Google Chrome
- `default_pdf` : Application PDF par defaut du systeme

---

## AUTRES SCRIPTS

| Script | Usage |
|--------|-------|
| `open_source_page.py` | Ouvrir la page source PDF d'une competence |
| `renormalize_codes.py` | Renormaliser les codes apres extraction |
| `aggregate_competences.py` | Agreger apres nouvelles extractions |
| `search_advanced.py` | Recherche avancee multi-criteres |
| `get_demonstrations.py` | Demonstrations exigibles |
| `check_in_program.py` | Verifier si une notion est au programme |

---

## AGENTS ASSOCIES

- `bo-competence-extractor` : Extraction depuis pages PDF
- `bo-search-agent` : Recherche de competences (preservant le contexte)

---

## SYSTEME DE SYNONYMES

La recherche utilise automatiquement des synonymes pour elargir les resultats. Exemples :

| Mot-cle | Synonymes automatiques |
|---------|------------------------|
| `milieu` | milieux, centre, median, mediane |
| `identite remarquable` | (a+b)^2, (a-b)^2, a^2-b^2, developpement, factorisation |
| `repere` | reperes, orthonorme, coordonnees, abscisse, ordonnee |
| `vecteur` | vecteurs, vectoriel, translation, composantes |
| `intervalle` | intervalles, borne, bornes, ouvert, ferme |

Utilisez `--list-synonyms` pour voir la liste complete.
Utilisez `--exact` pour desactiver les synonymes.

---

## LIMITATIONS CONNUES

### Donnees incompletes

Certaines competences du programme ne sont pas encore extraites :

| Niveau | Domaine | Probleme |
|--------|---------|----------|
| 2GT | GEOMETRIE | Seulement 1 competence (geometrie reperee manquante) |

Les competences de **geometrie reperee** (coordonnees, milieu, distance, vecteurs) sont dans le programme de 2nde mais classees dans NOMBRES ou ALGEBRE, pas GEOMETRIE.

**Workaround** : Chercher par mot-cle plutot que par domaine.

---

## NOTES

- **Toujours utiliser les scripts**, jamais les JSON directement
- Les programmes evoluent : verifier la date du BO cite
- Les approfondissements possibles ne sont pas exigibles
- Pour les documents officiels (inspecteurs), privilegier les citations exactes
- **Encodage** : Le script force UTF-8, compatible Windows
