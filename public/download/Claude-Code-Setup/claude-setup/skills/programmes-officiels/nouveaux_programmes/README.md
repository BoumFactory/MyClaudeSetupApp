# Mise a jour des programmes officiels

Ce dossier sert a deposer les nouveaux PDFs de programmes officiels
pour declencher une mise a jour automatisee.

## Workflow complet

### Etape 1: Deposer le nouveau PDF

Placez le nouveau PDF dans ce dossier avec un nom clair:

```
nouveaux_programmes/
  └── 4eme_2026.pdf          # Nouveau programme de 4e
```

### Etape 2: Decouper le PDF en pages

```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026"

# Decouper le PDF (cree un dossier dans data/pages/)
python ".claude/skills/programmes-officiels/scripts/split_pdf_pages.py" ".claude/skills/programmes-officiels/nouveaux_programmes/4eme_2026.pdf"
```

Cela cree:
- `data/pages/4eme_2026/page_001.pdf`
- `data/pages/4eme_2026/page_001.txt`
- `data/pages/4eme_2026/index.json`
- etc.

### Etape 3: Comparer avec l'ancien programme

```bash
# Comparer ancien vs nouveau (genere rapport HTML)
python ".claude/skills/programmes-officiels/scripts/compare_programs.py" \
    16-Maths-4e-attendus-eduscol_1114746 \
    4eme_2026 \
    --html
```

Le rapport HTML s'ouvre et montre:
- Pages identiques (rien a faire)
- Pages modifiees (re-extraction necessaire)
- Pages ajoutees (nouvelle extraction)
- Pages supprimees (supprimer competences)

### Etape 4: Lancer l'agent de mise a jour

Demander a Claude:

```
Lance l'agent program-updater pour mettre a jour le programme de 4e
en utilisant le rapport de comparaison genere.
```

L'agent va:
1. Lire le rapport de comparaison
2. Pour chaque page modifiee/ajoutee:
   - Analyser le contenu
   - Extraire les competences
   - Utiliser les scripts pour mettre a jour les JSON
3. Pour les pages supprimees:
   - Supprimer les competences obsoletes
4. Generer un rapport de migration

### Etape 5: Valider les modifications

```bash
# Verifier coherence JSON vs texte source
python ".claude/skills/programmes-officiels/scripts/validate_json_vs_source.py" 4eme_2026

# Re-agreger toutes les competences
python ".claude/skills/programmes-officiels/scripts/aggregate_competences.py"

# Verifier la couverture
python ".claude/skills/programmes-officiels/scripts/check_coverage.py"
```

### Etape 6: Nettoyer

Une fois valide:
1. Archiver l'ancien dossier de pages (optionnel)
2. Renommer le nouveau dossier si necessaire
3. Supprimer le PDF de `nouveaux_programmes/`

---

## Scripts disponibles

| Script | Role |
|--------|------|
| `split_pdf_pages.py` | Decoupe PDF en pages |
| `compare_programs.py` | Compare 2 versions, genere diff HTML |
| `validate_json_vs_source.py` | Verifie coherence JSON/BO |
| `json_competence_tools.py` | Insert/delete/update competences |
| `aggregate_competences.py` | Agregation globale |
| `check_coverage.py` | Verification couverture |

## Agent

L'agent `program-updater` orchestre la mise a jour en utilisant les scripts
comme outils. Il ne charge jamais les gros JSON en memoire.

---

## Exemple concret

```
Scenario: Le programme de 4eme change en janvier 2027

1. Telecharger le nouveau BO depuis education.gouv.fr
2. Renommer en "4eme_2027.pdf"
3. Deposer dans ce dossier
4. Executer les commandes ci-dessus
5. L'agent met a jour les JSON
6. Valider et nettoyer
```

Temps estime: 15-30 minutes selon le nombre de pages modifiees.
