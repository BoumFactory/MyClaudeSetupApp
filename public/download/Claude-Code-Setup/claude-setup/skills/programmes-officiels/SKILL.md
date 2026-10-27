---
name: programmes-officiels
description: Rechercher et citer précisément les éléments des nouveaux programmes officiels de mathématiques applicables à la rentrée 2026 (Éducation Nationale française), du cycle 3 (CM1/CM2/6e) à la Terminale. Utiliser pour sourcer compétences, capacités, démonstrations exigibles et algorithmes Python. Base JSON par niveau + miroir markdown avec preuve visuelle des pages BO.
---

# Skill `programmes-officiels`

Base de connaissances **JSON-first** des programmes officiels de mathématiques (rentrée 2026) :

- **Lycée** : 2GT, 1SPE, 1ENS, 1TEC, TSPE, TCOMP, TTEC — BO Hebdo 14 du 2 avril 2026
- **Cycle 4** : 5E, 4E, 3E — BO n°10 du 5 mars 2026
- **Cycle 3** : CM1, CM2, 6E — BO du cycle 3 (rentrée 2026)

## Quand utiliser ce skill

- Sourcer une compétence officielle pour une fiche pédagogique, un devoir, une progression annuelle.
- Vérifier qu'une notion est au programme (et à quel niveau).
- Citer la **formulation BO exacte** d'un attendu (capacité, contenu, démonstration exigible, algorithme).
- Retrouver l'**image-preuve** de la page BO d'où provient la compétence.
- Tracer la **progression verticale** d'une notion (cycle 3 → cycle 4 → lycée).

## Commandes principales

### 🔎 Recherche libre

```bash
# Recherche FTS5 plein texte (accents normalisés, wildcards supportés)
python scripts/search.py --keyword "dérivée"
python scripts/search.py --keyword "pythagore" --niveau 4E
python scripts/search.py --keyword "fraction*" --niveau CM1   # wildcard pour singulier+pluriel

# Recherche structurée
python scripts/search.py --niveau 2GT --domaine GEO
python scripts/search.py --niveau TSPE --type demonstration
```

### 🎯 CLI ergonomiques (un script = une question)

```bash
# Détail complet d'une compétence (intitulé + formulation BO verbatim + source PDF/page)
python scripts/get.py CM1-NB-014
python scripts/get.py TSPE-AN-031 --format json
# → suggère des codes proches si le code est inconnu

# Toutes les démonstrations exigibles d'un niveau
python scripts/demos.py --niveau TSPE                # 18 démos en TSPE
python scripts/demos.py --niveau TSPE --domaine AN   # filtré sur Analyse

# Tous les algorithmes Python attendus
python scripts/algos.py --niveau 1SPE                # liste des algos
python scripts/algos.py --niveau TSPE --code         # avec code Python

# Progression verticale d'une notion (CM1 → … → TSPE)
python scripts/progression.py "fraction*"            # de la fraction unitaire CM1 au quotient TSPE
python scripts/progression.py "pythagore"
python scripts/progression.py "derivation"

# Vue d'ensemble du skill (compteurs par niveau / domaine / type)
python scripts/stats.py
python scripts/stats.py --niveau TSPE                # drill-down

# Comparer deux niveaux (par sous-domaines) — révèle nouveautés / abandons
python scripts/compare.py CM2 6E --domaine NB
python scripts/compare.py 5E 4E --domaine GEO
python scripts/compare.py 1SPE 1TEC --domaine STA    # spécialité vs voie techno
```

Tous les scripts ci-dessus acceptent `--format json` pour usage programmatique (RAG, API, scripts).

### 🛠 Maintenance

```bash
# Validation globale du skill (schéma, codes uniques, sources, transcriptions)
python scripts/validate.py

# Suite pytest complète (anti-régurgitation, golden queries, md_sync, etc.)
python -m pytest tests/
```

## Prouver une citation

Toute affirmation sur le programme doit pouvoir être prouvée : donner le **chemin du BO** (`data/pdf/<niveau>.pdf`) et la **page** (champ `source.page` de la compétence), et au besoin l'image de la page (`data/pages/<niveau>/page_NNN.png`) ou son texte brut (`data/pages_txt/…`). `python scripts/get.py <CODE>` affiche ces références.

**Images de pages non fournies.** Les dossiers `data/pages/` (PNG) et `data/pages_pdf/` (pages PDF isolées) ne sont pas livrés : ils se régénèrent depuis les BO complets de `data/pdf/`. `get.py` recrée seul l'image de la page citée si PyMuPDF est installé ; sinon il indique la commande à lancer. Régénération manuelle :

```bash
pip install pymupdf                                        # requis pour cela uniquement
python scripts/regenerer_pages.py --niveau 5E              # un niveau (PNG + PDF de page)
python scripts/regenerer_pages.py --niveau cycle4 --page 7 --png
python scripts/regenerer_pages.py                          # tous les niveaux
```

Sans PyMuPDF, la preuve reste possible : ouvrir `data/pdf/<niveau>.pdf` à la page `source.page` (ou texte brut dans `data/pages_txt/`).

Les scripts de construction (`scripts/build/`) servent à **mettre à jour les programmes avec un nouveau BO** : remplacer le PDF dans `data/pdf/`, puis relancer le pipeline (voir plus bas).

## Niveaux et codes

| Code | Niveau | Cycle | PDF source |
|------|--------|-------|------------|
| `CM1` `CM2` `6E` | Cycle 3 (école + 6e) | C3 | `cycle3.pdf` |
| `5E` `4E` `3E` | Cycle 4 (collège) | C4 | `cycle4.pdf` |
| `2GT` | Seconde générale et technologique | Lycée | `2gt.pdf` |
| `1SPE` | 1ère spécialité maths | Lycée | `1spe.pdf` |
| `1ENS` | 1ère maths dans l'enseignement scientifique | Lycée | `1ens.pdf` |
| `1TEC` | 1ère voie technologique | Lycée | `1tec.pdf` |
| `TSPE` | Terminale spécialité maths | Lycée | `tspe.pdf` |
| `TCOMP` | Terminale maths complémentaires | Lycée | `tcomp.pdf` |
| `TTEC` | Terminale voie technologique | Lycée | `ttec.pdf` |

## Domaines

| Code | Domaine |
|------|---------|
| `NB` | Nombres et calculs |
| `AL` | Algèbre |
| `AN` | Analyse |
| `GEO` | Géométrie |
| `GM` | Grandeurs et mesures |
| `STA` | Statistiques |
| `PR` | Probabilités |
| `OGD` | Organisation et gestion de données |
| `ALGO` | Algorithmique et programmation |
| `TRG` | Trigonométrie |
| `LOG` | Vocabulaire ensembliste et logique |

## Types

| Type | Sens |
|------|------|
| `contenu` | Définition, propriété, théorème |
| `capacite` | Savoir-faire, application |
| `demonstration` | Démonstration exigible au programme |
| `algorithme` | Programme Python/Scratch attendu |
| `approfondissement` | Extension possible non exigible |

## Architecture & directive anti-régurgitation

```
data/
├── pdf/{niveau}.pdf                            # 9 PDFs sources (7 lycée + cycle4 + cycle3)
├── pages_txt/{folder}/page_NNN.txt             # Texte brut PyMuPDF
├── pages_pdf/{folder}/page_NNN.pdf             # (non fourni) PDFs page isolée, régénérable
├── pages/{folder}/page_NNN.png                 # (non fourni) PNG ~1200 px, régénérable
├── bullets/{folder}/page_NNN.json              # Bullets BO verbatim — extrait Python
├── transcriptions/{niveau}/page_NNN.md         # Optionnel — cas tableaux complexes uniquement
├── json/
│   ├── schema.json                             # JSON Schema validateur
│   ├── {NIVEAU}.json                           # SOURCE DE VÉRITÉ par niveau (généré mécaniquement)
│   ├── all_flat.json                           # Dérivé : liste plate globale
│   └── _backup/                                # Anciennes versions (avant pivot mécanique)
├── markdown/{cycle}/{niveau}/{dom}/{code}.md   # Miroir auto-généré (RAG-ready)
├── index.json                                  # Index principal
├── search_index.sqlite                         # FTS5 SQLite
└── progressions.json                           # Graphe prérequis/liens
```

> 🔒 **Directive anti-régurgitation**
> Le champ `formulation_bo` et toute citation BO verbatim proviennent **strictement** du script `04_extract_bullets.py` (extraction PyMuPDF du texte du PDF). **Aucune génération LLM** ne reproduit le texte du BO. Le LLM est utilisé pour l'**analyse** : classification de domaine, atomicité, prérequis, liens, parsers spécialisés.

**Source de vérité** : les `data/json/{NIVEAU}.json`. Le markdown est dérivé via `06_export_markdown.py` (idempotent). **On n'édite jamais un MD à la main.**

**Pipeline de construction (Python pur jusqu'aux JSON niveau)** :

```
PDF → 01_split_pdfs.py → pages_txt/
    → 02_generate_page_images.py → pages/*.png
    → 04_extract_bullets.py → bullets/*.json     (0 LLM, formulation_bo verbatim)
    → 05_competences_from_bullets.py → json/*.json  (0 LLM, mapping sous_domaine→domaine)
    → 05_build_indexes.py + 06_export_markdown.py + 07_build_progressions.py
```

## État

Pipeline mécanique opérationnel sur les 13 niveaux :

- **1076 compétences** extraites mécaniquement, **0 régurgitation LLM** (`formulation_bo` strictement issu du PDF via PyMuPDF).
- **Cycle 3** : CM1 (128), CM2 (112), 6E (103). Mode "bulletless" du parser : sous "Objectifs d'apprentissage", chaque ligne MAJ = bullet implicite, ligne min = continuation (le BO cycle 3 n'utilise pas de caractères de puce).
- **Cycle 4** : 5E (15), 4E (11), 3E (14). Bullets explicites + détection des titres "Cinquième/Quatrième/Troisième" pour le split.
- **Lycée** : 2GT (134), 1SPE (114), 1ENS (19), 1TEC (63), TSPE (180), TCOMP (136), TTEC (47).
- **Automatismes** : 917 entrées indexées (FTS5 dédié).
- **Validation** : `validate.py` 4/4 OK ; `pytest` 66/66 OK ; FTS5 query ~0.8 ms.

Limites résiduelles : prérequis/liens à 0 edges ; 1ENS reste à 19 compétences (BO bi-colonne, cohérent avec un programme allégé).

Pour mettre à jour avec un nouveau BO : remplacer le PDF dans `data/pdf/`, puis relancer le pipeline `scripts/build/` (voir « Cycle de mise à jour »).

## Format d'une compétence (extrait JSON)

```json
{
  "code": "2GT-NB-008",
  "intitule": "Démonstration : √2 est irrationnel",
  "niveau": "2GT",
  "domaine": "NB",
  "type": "demonstration",
  "formulation_bo": "Le nombre réel √2 est irrationnel.",
  "demonstrations_exigibles": ["Par l'absurde : ..."],
  "prerequis": ["2GT-NB-003", "2GT-LOG-003"],
  "source": {"pdf": "2gt.pdf", "page": 7, "page_image": "../pages/2GT/page_007.png"},
  "tags": ["démonstration", "absurde", "irrationnel", "exigible"]
}
```

## Performance

- Recherche FTS5 : < 1 ms p95
- Validation complète : < 1 s
- Build complet des indexes : < 5 s

## Cycle de mise à jour

Lors de l'ajout/modification d'une compétence :

```bash
# 1. Éditer data/json/{NIVEAU}.json (source de vérité)
# 2. Re-générer indexes et markdown :
python scripts/build/05_build_indexes.py
python scripts/build/06_export_markdown.py
python scripts/build/07_build_progressions.py
# 3. Valider :
python scripts/validate.py
```
