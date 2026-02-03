# TODO - Extraction des programmes officiels

**Date : 10 janvier 2026**
**Statut : EXTRACTION COMPLETE**

---

## ETAT ACTUEL

Toutes les extractions critiques sont terminées.

### Pages restantes (faible priorité)

Seules 3 pages de garde collège ne sont pas extraites (pages de titre sans contenu pédagogique) :

```
14-Maths-5e : page 1 (page de garde)
16-Maths-4e : page 1 (page de garde)
18-Maths-3e : page 1 (page de garde)
```

Ces pages ne contiennent que le titre du document, pas de compétences à extraire.

---

## NIVEAUX COMPLETS (16/16)

| Niveau | Pages extraites | Statut |
|--------|-----------------|--------|
| cycle3_v2 (6ème) | 28/28 | OK |
| 14-Maths-5e | 12/13 | OK (page 1 = titre) |
| 16-Maths-4e | 11/12 | OK (page 1 = titre) |
| 18-Maths-3e | 10/11 | OK (page 1 = titre) |
| 2GT (2nde GT) | 16/16 | OK |
| 2STHR | 13/13 | OK |
| 1GT (1ère Spé) | 16/16 | OK |
| 1ere_techno | 16/16 | OK |
| premiere_ens_sci | 15/15 | OK |
| Mathematiques_integrees_EnsSci_1reG | 7/7 | OK |
| TG_spe | 21/21 | OK |
| TG_comp | 17/17 | OK |
| TG_expertes | 11/11 | OK |
| Tle_techno | 16/16 | OK |
| terminale_spe | 21/21 | OK |
| spe265_annexe_1159134 | 17/17 | OK |

---

## PROCHAINES ETAPES

L'extraction est terminée. Pour maintenir la base :

1. **Agrégation** (si modifications) :
```bash
python ".claude/skills/programmes-officiels/scripts/aggregate_competences.py"
```

2. **Normalisation** (si modifications) :
```bash
python ".claude/skills/programmes-officiels/scripts/renormalize_codes.py"
```

3. **Vérification couverture** :
```bash
python ".claude/skills/programmes-officiels/scripts/check_coverage.py"
```

4. **Vérification pages manquantes** :
```bash
python ".claude/skills/programmes-officiels/scripts/check_missing_extractions.py"
```

---

## HISTORIQUE

- **9 janvier 2026** : Extraction massive des 53 pages manquantes critiques
- **10 janvier 2026** : Validation - toutes extractions critiques terminées
