# Skill : Programmes Officiels de Mathématiques

## 📋 Description

Ce skill permet de rechercher et citer précisément les éléments des programmes officiels de l'Éducation Nationale française (du cycle 3 au lycée).

## 📁 Structure des données

### Emplacement des fichiers

```
.claude/skills/programmes-officiels/
├── data/                           # Données structurées des programmes
│   ├── cycle3.json                 # Cycle 3 (CM1, CM2, 6ème)
│   ├── cycle4.json                 # Cycle 4 (5ème, 4ème, 3ème) [à finaliser]
│   ├── seconde.json                # 2nde générale et technologique
│   ├── premiere_spe.json           # 1ère spécialité mathématiques [à créer]
│   ├── terminale_spe.json          # Terminale spécialité mathématiques
│   ├── premiere_ens_sci.json       # 1ère enseignement scientifique
│   └── terminale_ens_sci.json      # Terminale enseignement scientifique [à créer]
│
├── pdf/                            # PDFs sources du BO
│   ├── cycle3_v2.pdf
│   ├── cycle4_v2.pdf
│   ├── seconde.pdf
│   ├── premiere_spe_v2.pdf
│   ├── terminale_spe.pdf
│   ├── premiere_ens_sci.pdf
│   └── terminale_ens_sci.pdf
│
├── references_bo.json              # Métadonnées de tous les programmes
├── README.md                       # Ce fichier
└── consulter_competences.py        # Programme de consultation
```

## 🎯 Utilisation

### 1. Consulter une compétence par code

```python
from consulter_competences import chercher_competence

# Rechercher par code unique
comp = chercher_competence("6-NC-001")
print(comp["intitule"])
```

### 2. Lister les compétences d'un niveau

```python
from consulter_competences import lister_competences_niveau

# Toutes les compétences de 6ème
competences_6e = lister_competences_niveau("6eme")
```

### 3. Rechercher par thème

```python
from consulter_competences import chercher_par_theme

# Compétences sur les fractions en 6ème
fractions = chercher_par_theme("6eme", "fractions")
```

### 4. Rechercher par mots-clés

```python
from consulter_competences import chercher_mots_cles

# Toutes les compétences contenant "dérivée"
derivees = chercher_mots_cles("dérivée")
```

## 📊 Structure des données JSON

### Format général

```json
{
  "niveau": "6ème|5ème|...|TERMINALE_SPE",
  "cycle": "Cycle 3|Cycle 4|...",
  "reference_bo": "BO n°X du JJ/MM/AAAA",
  "domaines": [
    {
      "nom": "Nombres et calculs",
      "code": "NC",
      "competences": [
        {
          "code": "6-NC-001",
          "intitule": "Composer, décomposer les grands nombres entiers...",
          "capacites": ["...", "..."],
          "connaissances": ["...", "..."],
          "attendus": "..."
        }
      ]
    }
  ]
}
```

### Codes des niveaux

| Code fichier | Niveau | Cycle |
|--------------|--------|-------|
| `cycle3.json` | CM1, CM2, 6ème | Cycle 3 |
| `cycle4.json` | 5ème, 4ème, 3ème | Cycle 4 |
| `seconde.json` | 2nde | Lycée |
| `premiere_spe.json` | 1ère Spé | Lycée |
| `terminale_spe.json` | Tale Spé | Lycée |
| `premiere_ens_sci.json` | 1ère Ens. Sci. | Lycée |
| `terminale_ens_sci.json` | Tale Ens. Sci. | Lycée |

### Codes des domaines

| Code | Domaine | Niveaux |
|------|---------|---------|
| `NC` | Nombres et calculs | Collège |
| `GM` | Grandeurs et mesures | Collège |
| `EG` | Espace et géométrie | Collège |
| `OGD` | Organisation et gestion de données | Collège |
| `ALG` | Algèbre | Lycée |
| `ANA` | Analyse | Lycée |
| `GEO` | Géométrie | Lycée |
| `PROB` | Probabilités et statistiques | Lycée |
| `ALGO` | Algorithmique et programmation | Lycée |

## 🔍 Format des codes de compétences

### Collège
```
{niveau}-{domaine}-{numéro}
```
Exemples :
- `6-NC-001` : 6ème, Nombres et calculs, compétence 1
- `5-EG-012` : 5ème, Espace et géométrie, compétence 12

### Lycée
```
{niveau}-{domaine}-{numéro}
```
Exemples :
- `2-ALG-005` : 2nde, Algèbre, compétence 5
- `1SPE-ANA-018` : 1ère Spé, Analyse, compétence 18
- `TSPE-GEO-007` : Tale Spé, Géométrie, compétence 7

## 📈 Statistiques

### Compétences extraites par niveau

| Niveau | Nb compétences | Statut |
|--------|----------------|--------|
| Cycle 3 (6ème) | 50 | ✅ Complet |
| Cycle 4 (5ème-4ème-3ème) | À finaliser | ⚠️ En cours |
| 2nde | 37 | ✅ Complet |
| 1ère Spé | 83 | ✅ Complet |
| Tale Spé | À extraire | ⏳ À faire |
| 1ère Ens. Sci. | 35 | ✅ Complet |
| Tale Ens. Sci. | 30 | ✅ Complet |
| **TOTAL** | **235+** | En construction |

## 🛠️ Maintenance

### Ajouter un nouveau programme

1. Télécharger le PDF officiel du BO dans `pdf/`
2. Mettre à jour `references_bo.json`
3. Lancer l'agent d'extraction :
```bash
claude-code task --agent programme-officiel-extractor \
  --pdf "pdf/nouveau_programme.pdf" \
  --output "data/nouveau_programme.json"
```

### Mettre à jour un programme existant

1. Sauvegarder l'ancienne version
2. Relancer l'extraction avec le nouveau PDF
3. Comparer les différences avec un diff JSON

## 📚 Références

- [Éduscol - Programmes](https://eduscol.education.fr/139/programmes-de-l-ecole-et-du-college)
- [BO Éducation Nationale](https://www.education.gouv.fr/pid285/le-bulletin-officiel.html)
- [Ressources Éduscol Mathématiques](https://eduscol.education.fr/154/mathematiques-cycle-3-et-4)

## 🤝 Contribution

Pour signaler une erreur ou proposer une amélioration :
1. Identifier la compétence concernée (code)
2. Vérifier dans le PDF source du BO
3. Proposer la correction avec référence précise (page du BO)

---

*Dernière mise à jour : Octobre 2025*
*Version : 1.0*
