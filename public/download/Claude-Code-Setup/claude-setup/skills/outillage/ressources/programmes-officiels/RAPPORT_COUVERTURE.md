# Rapport de Couverture - Programmes Officiels

**Date de generation : Janvier 2026**
**Total competences : 4050**

---

## ETAT GLOBAL

| Niveau | Score | Status | Competences | Probleme majeur |
|--------|-------|--------|-------------|-----------------|
| 6eme (C3) | 70% | WARN | 906 | Mots-cles manquants |
| 5eme | 79% | WARN | 309 | Domaines faibles (Analyse, Probas) |
| 4eme | 91% | OK | 205 | - |
| 3eme | 62% | WARN | 197 | Mots-cles manquants |
| **2nde GT** | **20%** | **CRITICAL** | 232 | **ANALYSE ABSENT, GEOMETRIE=1** |
| **1ere Spe** | **53%** | **WARN** | 246 | **GEOMETRIE ABSENT** |
| Term. Spe | 75% | WARN | 722 | Mots-cles manquants |
| Term. Expert | 70% | WARN | 207 | Domaines faibles |

---

## PROBLEMES CRITIQUES

### 1. 2nde GT - Score 20% (CRITICAL)

**Domaines problematiques :**
- `ANALYSE` : **ABSENT** (devrait contenir : fonctions, variations, extremum, courbes)
- `GEOMETRIE` : **1 seule competence** (devrait contenir : vecteurs, coordonnees, repere, milieu, distance)

**Mots-cles absents :**
- polynome, second degre (ALGEBRE)
- extremum, courbe, fonction, variation (ANALYSE)
- vecteur, coordonnees, repere, milieu, distance, colineaire (GEOMETRIE)

**Cause probable :**
Le PDF 2GT a ete extrait mais les pages de geometrie/analyse n'ont pas ete correctement traitees.

**Action requise :**
```bash
# Verifier les pages du PDF 2GT
python scripts/verify_extraction_quality.py 2GT

# Re-extraire les competences manquantes
# L'agent bo-competence-extractor doit retraiter les pages 8-16 du PDF 2GT
```

---

### 2. 1ere Spe - Score 53% (WARN -> CRITICAL pour GEOMETRIE)

**Domaines problematiques :**
- `GEOMETRIE` : **ABSENT** (devrait contenir : vecteur, produit scalaire, droite, plan, equation cartesienne)
- `NOMBRES` : 3 competences seulement (faible)

**Mots-cles absents :**
- logarithme (devrait etre en ANALYSE)
- vecteur, produit scalaire, droite, plan, equation cartesienne (GEOMETRIE)

**Cause probable :**
Les competences de geometrie de 1ere Spe ont ete classees ailleurs ou non extraites.

**Action requise :**
```bash
# Verifier les extractions du PDF 1GT
python scripts/verify_extraction_quality.py 1GT

# Re-extraire les pages de geometrie (produit scalaire, vecteurs)
```

---

## MOTS-CLES FREQUEMMENT MANQUANTS

| Mot-cle | Niveaux concernes | Domaine attendu |
|---------|-------------------|-----------------|
| `vecteur` | 2G, 1S | GEOMETRIE |
| `equation` | 5, 3 | ALGEBRE |
| `pythagore` | 4, 3 | GEOMETRIE |
| `logarithme` | 1S | ANALYSE |
| `produit scalaire` | 1S | GEOMETRIE |
| `loi normale` | 0S | PROBABILITES |

---

## RECOMMANDATIONS PAR PRIORITE

### Priorite 1 : Corrections critiques

1. **Re-extraire ANALYSE et GEOMETRIE pour 2nde GT**
   - Pages concernees : 8-16 du PDF 2GT.pdf
   - Domaines attendus : fonctions, variations, vecteurs, coordonnees

2. **Re-extraire GEOMETRIE pour 1ere Spe**
   - Pages concernees : PDF 1GT.pdf (section geometrie)
   - Domaines attendus : produit scalaire, vecteurs, equations de droites

### Priorite 2 : Enrichissements

1. **Completer les mots-cles manquants** en 6eme, 3eme
2. **Ajouter les competences de probabilites** en Terminale Spe (loi normale, densite)
3. **Verifier l'exhaustivite** des demonstrations exigibles

### Priorite 3 : Maintenance

1. **Executer `check_coverage.py`** apres chaque nouvelle extraction
2. **Mettre a jour les seuils** de MIN_COMPETENCES_PER_DOMAIN si necessaire
3. **Ajouter de nouveaux mots-cles** attendus au fur et a mesure

---

## SCRIPTS DE VERIFICATION

### Verification quotidienne
```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026"
python ".claude/skills/programmes-officiels/scripts/check_coverage.py"
```

### Verification qualite extraction
```bash
python ".claude/skills/programmes-officiels/scripts/verify_extraction_quality.py" --report
```

### Recherche specifique
```bash
python ".claude/skills/programmes-officiels/scripts/search_competences.py" --keyword "vecteur" --all-levels
```

---

## METRIQUES CIBLES

Pour considerer le skill comme **complet et fiable** :

| Metrique | Cible | Actuel |
|----------|-------|--------|
| Score moyen tous niveaux | > 80% | ~65% |
| Aucun domaine ABSENT | 0 | **2** |
| Aucun domaine < 5 competences | 0 | 8 |
| Total competences | > 4000 | 4050 |
| Couverture mots-cles | > 90% | ~75% |

---

## HISTORIQUE

- **Janvier 2026** : Creation du script `check_coverage.py`, detection des lacunes critiques
- **Octobre 2025** : Extraction initiale, creation de `valider_extractions.py`

---

*Ce rapport est genere automatiquement par `check_coverage.py`*
