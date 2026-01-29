# Guide d'extraction des programmes officiels du college

## Etat actuel (2026-01-03)

### PDFs prepares

| PDF | Niveau | Pages | Statut Split | Pages extraites |
|-----|--------|-------|--------------|-----------------|
| cycle3_v2.pdf | Cycle 3 (CM1-CM2-6e) | 28 | OK | 21/28 |
| 14-Maths-5e-attendus-eduscol_1114744.pdf | 5eme | 13 | OK | En cours |
| 16-Maths-4e-attendus-eduscol_1114746.pdf | 4eme | 12 | OK | 0/12 |
| 18-Maths-3e-attendus-eduscol_1114748.pdf | 3eme | 11 | OK | 0/11 |

**Total : 64 pages a extraire**

## Comment continuer l'extraction

### 1. Lire le fichier de suivi

```
Lire: .claude/skills/programmes-officiels/data/extraction_tracking.json
```

Ce fichier contient l'etat actuel de toutes les extractions.

### 2. Identifier les pages restantes

Regarder le champ `pages_restantes` de chaque PDF dans le fichier de suivi.

### 3. Lancer un batch d'agents

**IMPORTANT : Ne pas lancer plus de 3-5 agents en parallele pour economiser le credit.**

Exemple de lancement pour la page 5 du PDF 5eme :

```
Task(
  subagent_type='bo-competence-extractor',
  prompt='''Extraire les competences mathematiques atomiques de la page 5 du programme de 5eme.

Le fichier texte source est: C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/.claude/skills/programmes-officiels/data/pages/14-Maths-5e-attendus-eduscol_1114744/page_005.txt

Le PDF source est: 14-Maths-5e-attendus-eduscol_1114744.pdf
Le niveau est: 5E

Sauvegarder le resultat JSON dans: C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/.claude/skills/programmes-officiels/data/extractions/14-Maths-5e-attendus-eduscol_1114744/page_005_competences.json

Lis d'abord le fichier texte source, puis extrait TOUTES les competences atomiques selon le format defini dans ta mission.''',
  run_in_background=True
)
```

### 4. Mettre a jour le fichier de suivi

Apres chaque batch termine, mettre a jour :
- `pages_extraites` : incrementer le nombre
- `pages_restantes` : retirer les pages traitees
- `sessions` : ajouter une nouvelle entree avec les actions effectuees

### 5. Verifier les extractions

Lire un fichier JSON de competences pour verifier la qualite :
```
Lire: .claude/skills/programmes-officiels/data/extractions/[DOSSIER]/page_XXX_competences.json
```

## Chemins importants

```
Base: C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/.claude/skills/programmes-officiels

Pages sources:
- data/pages/cycle3_v2/page_XXX.txt
- data/pages/14-Maths-5e-attendus-eduscol_1114744/page_XXX.txt
- data/pages/16-Maths-4e-attendus-eduscol_1114746/page_XXX.txt
- data/pages/18-Maths-3e-attendus-eduscol_1114748/page_XXX.txt

Extractions JSON:
- data/extractions/cycle3_v2/page_XXX_competences.json
- data/extractions/14-Maths-5e-attendus-eduscol_1114744/page_XXX_competences.json
- data/extractions/16-Maths-4e-attendus-eduscol_1114746/page_XXX_competences.json
- data/extractions/18-Maths-3e-attendus-eduscol_1114748/page_XXX_competences.json
```

## Codes de niveau pour les competences

| Niveau | Code |
|--------|------|
| Cycle 3 | C3 |
| 6eme | 6E |
| 5eme | 5E |
| 4eme | 4E |
| 3eme | 3E |

## Notes

- La page 1 de chaque PDF est generalement une page de titre sans contenu a extraire
- Le texte extrait des PDFs peut avoir des problemes de formatage (fractions cassees, symboles manquants) - l'agent sait les interpreter
- Verifier que les fichiers JSON generes sont valides et contiennent des competences
