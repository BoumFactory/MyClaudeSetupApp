# programmes-officiels

Skill Claude Code de référence pour les **nouveaux programmes officiels de mathématiques** applicables à la **rentrée 2026** (Éducation Nationale française).

## Sources couvertes

- **Lycée** (7 PDF) : BO Hebdo 14 du 2 avril 2026
- **Cycle 4** (1 PDF) : BO n°10 du 5 mars 2026 (annexe 2)
- **Cycle 3** (1 PDF) : BO du cycle 3 (rentrée 2026) — CM1, CM2, 6e

Les PDF du BO sont des documents publics ; chaque compétence cite son PDF et sa page.

## Public

Professeurs de mathématiques de l'école élémentaire (CM1/CM2), du collège et du lycée. Le contenu est dense, technique, et cite verbatim le BO.

## Principe d'architecture

- **JSON-first** : un fichier `data/json/{NIVEAU}.json` par niveau, validable par un JSON Schema.
- **Markdown dérivé** : auto-généré depuis les JSON via un script idempotent (`06_export_markdown.py`), pour usage humain et RAG.
- **Preuve visuelle** : chaque compétence référence un PNG de la page BO source.
- **Pipeline reproductible** : PDF → split → images → **bullets extraits par script Python** → JSON → indexes → markdown.

### Directive anti-régurgitation

Le champ `formulation_bo` et toute citation BO verbatim proviennent strictement de `scripts/build/04_extract_bullets.py` (extraction PyMuPDF). **Aucune génération LLM** ne reproduit le texte du BO. Le LLM n'intervient que pour l'**analyse** (classification de domaine, atomicité, prérequis, liens, parsers spécialisés).

## Démarrage rapide

```bash
# Chercher « théorème de Pythagore »
python scripts/search.py --keyword "Pythagore"

# Lister toutes les démonstrations exigibles en TSPE
python scripts/search.py --niveau TSPE --type demonstration

# Détail complet d'une compétence
python scripts/get.py 2GT-NB-008
```

Seul Python 3 est nécessaire pour consulter ; PyMuPDF (`pip install pymupdf`) n'est utile que pour reconstruire la base avec un nouveau BO.

## Mettre à jour avec un nouveau BO

1. Déposer le nouveau PDF dans `data/pdf/` (et adapter `data/pdf/_mapping.json` si besoin).
2. Relancer les scripts de `scripts/build/` dans l'ordre `01` → `07`.
3. Valider : `python scripts/validate.py`.

## Performance

| Opération | Mesuré |
|-----------|--------|
| Recherche FTS5 plein texte | ~0,8 ms |
| Recherche par code | < 1 ms |
| Validation complète | < 1 s |
| Build des indexes (1076 compétences) | < 5 s |

## Limites connues

- Graphe `progressions.json` : prérequis et liens à 0 arête (à enrichir par analyse ciblée, sans toucher à `formulation_bo`).
- Transcriptions des tableaux complexes : partielles (`python scripts/validate.py` signale les pages manquantes).

## Licence et contribution

Knowledge base ouverte aux enseignants. Pas de modification directe des markdowns dérivés : éditer les JSON et regénérer.
