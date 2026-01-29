---
description: Recherche approfondie de ressources mathematiques pedagogiques
tags: [mathematiques, ressources, pedagogie, recherche, enseignement]
---

# Recherche de Ressources Mathematiques

Cette commande effectue une recherche structuree de ressources mathematiques pedagogiques sur les sites de reference francais.

## Argument requis

$ARGUMENTS = Le sujet de recherche (ex: "exercices Pythagore 4eme", "activite introduction fonctions", "probleme ouvert geometrie")

## Donnees de reference

- **Sites de reference** : `claude_datas/searchMathSources/sites-reference.json`
- **Historique des recherches** : `claude_datas/searchMathSources/historique.jsonl`

## Protocole de recherche

### Phase 1 : Analyse de la demande

1. **Identifier le niveau scolaire** (si mentionne) :
   - College : 6eme, 5eme, 4eme, 3eme
   - Lycee : 2nde, 1ere, Terminale

2. **Identifier le type de ressource recherche** :
   - Exercices (entrainement, evaluation)
   - Cours (lecons, fiches)
   - Activites (introduction, decouverte, probleme ouvert)
   - Videos (cours, corrections)
   - Sujets d'examen (brevet, bac)
   - Outils (GeoGebra, Desmos, Python)

3. **Extraire les mots-cles mathematiques** :
   - Theme principal (geometrie, calcul, fonctions, probabilites...)
   - Notions specifiques (Pythagore, Thales, derivation, suites...)

### Phase 2 : Recherche sur les sites prioritaires

Consulter dans cet ordre les sites du fichier `sites-reference.json` :

#### Etape 2.1 : Sites prioritaires (toujours consulter)

1. **MathAlea (coopmaths.fr)** - Pour exercices generes
   - Recherche : `site:coopmaths.fr {mots-cles}`
   - Ou navigation directe si le theme est connu

2. **Maths et Tiques** - Pour cours et exercices corriges
   - Recherche : `site:maths-et-tiques.fr {niveau} {theme}`

3. **Sesamath** - Pour manuels et ressources completes
   - Recherche : `site:sesamath.net {mots-cles}`

4. **Eduscol** - Pour documents officiels et ressources d'accompagnement
   - Recherche : `site:eduscol.education.fr mathematiques {theme}`

#### Etape 2.2 : Sites specialises (selon le besoin)

- **Pour exercices interactifs** : WIMS/Euler, Labomep
- **Pour sujets d'examen** : APMEP Annales, Annales2maths
- **Pour activites innovantes** : Mathix, Planete-maths
- **Pour outils dynamiques** : GeoGebra, Desmos
- **Pour culture maths** : Images des Mathematiques, Micmaths

### Phase 3 : Execution des recherches

Pour chaque site pertinent :

1. **Utiliser WebSearch** avec les requetes ciblees :
```
WebSearch: site:{domaine} {niveau} {theme} {type_ressource}
```

2. **Utiliser WebFetch** pour extraire le contenu des pages prometteuses :
   - Verifier que la ressource correspond au niveau
   - Extraire les liens directs vers les ressources (PDF, LaTeX, etc.)
   - Noter la qualite et la pertinence

### Phase 4 : Synthese et presentation

Presenter les resultats sous forme structuree :

```markdown
## Resultats de recherche : "{sujet}"

### Ressources trouvees

#### [Nom du site 1]
- **Lien** : [URL directe]
- **Type** : [exercice/cours/activite/etc.]
- **Niveau** : [si applicable]
- **Description** : [breve description du contenu]
- **Qualite estimee** : [Excellente/Bonne/Moyenne]

#### [Nom du site 2]
...

### Suggestions complementaires
- [Autres pistes de recherche]
- [Sites non explores qui pourraient etre pertinents]

### Resume
- X ressources trouvees sur Y sites consultes
- Types : [repartition par type]
```

### Phase 5 : Mise a jour de l'historique

Ajouter une entree dans `historique.jsonl` :

```jsonl
{"ts":"[timestamp]","query":"[recherche]","niveau":"[niveau]","theme":"[theme]","sites_visites":["site1","site2"],"resultats_utiles":[nombre],"ressources_cles":["url1","url2"]}
```

### Phase 6 : Auto-amelioration OBLIGATOIRE

**Cette phase est un DEVOIR. Elle doit etre executee a chaque recherche.**

#### 6.1 Mise a jour des scores des sites existants

Pour chaque site consulte pendant la recherche, mettre a jour `sites-reference.json` :

1. **Incrementer `utilisations`** : +1 pour chaque site visite
2. **Mettre a jour le score selon les resultats** :
   - Ressource **excellente** trouvee : `score += 5`
   - Ressource **utile** trouvee : `score += 2`
   - Aucun resultat pertinent : `score -= 1` (minimum 1)
3. **Incrementer `ressources_trouvees`** : +N pour chaque ressource utile

#### 6.2 Ajout de nouveaux sites decouverts

Si une ressource pertinente est trouvee sur un site **non repertorie** :

1. **Extraire le domaine** du nouveau site
2. **Verifier** qu'il n'existe pas deja dans `sites-reference.json`
3. **Ajouter** le site avec la structure suivante :

```json
{
  "id": "[domaine-slug]",
  "nom": "[Nom du site]",
  "domaine": "[domaine.fr]",
  "url": "[URL complete]",
  "description": "[Description de la ressource trouvee]",
  "niveaux": ["[niveaux identifies]"],
  "types_ressources": ["[types identifies]"],
  "categorie": "[categorie appropriee]",
  "score": 5,
  "utilisations": 1,
  "ressources_trouvees": 1,
  "date_ajout": "[date du jour]",
  "source": "decouverte_auto",
  "recherche_origine": "[requete qui a mene a la decouverte]"
}
```

#### 6.3 Prioritisation dynamique

Les sites sont consultes par ordre de score decroissant :
- **Score >= 20** : Site prioritaire (toujours consulter)
- **Score 10-19** : Site secondaire (consulter si pertinent)
- **Score < 10** : Site occasionnel (consulter en dernier recours)

#### 6.4 Rapport d'auto-amelioration

A la fin de chaque recherche, afficher un resume :

```markdown
### Auto-amelioration effectuee
- Sites consultes : X
- Scores mis a jour : [liste des modifications]
- Nouveaux sites ajoutes : [liste ou "aucun"]
- Top 3 sites actuels : [sites avec meilleurs scores]
```

**IMPORTANT** : Ne jamais sauter cette phase. L'amelioration continue de la base est essentielle pour optimiser les futures recherches.

## Conseils de recherche

### Requetes efficaces

| Objectif | Requete type |
|----------|--------------|
| Exercices niveau | `site:coopmaths.fr {niveau} {theme}` |
| Cours structure | `site:maths-et-tiques.fr cours {theme}` |
| Activite decouverte | `activite introduction {theme} {niveau}` |
| Probleme ouvert | `probleme ouvert {theme} college/lycee` |
| Sujet brevet/bac | `site:apmep.fr annales {examen} {theme}` |
| Ressource GeoGebra | `site:geogebra.org {theme} francais` |

### Filtres par niveau

- **College** : Ajouter "college" ou le niveau precis
- **Lycee** : Ajouter "lycee" ou "seconde/premiere/terminale"
- **Brevet** : Ajouter "DNB" ou "brevet"
- **Bac** : Ajouter "baccalaureat" ou "terminale"

## Actions post-recherche

Proposer a l'utilisateur :
1. Telecharger les ressources trouvees (si applicable)
2. Creer une fiche de synthese des ressources
3. Integrer une ressource dans un document LaTeX existant
4. Affiner la recherche avec des criteres supplementaires

## Exemple d'execution

```
/searchMathSource "exercices theoreme de Thales 3eme avec correction"
```

Resultat attendu :
- Recherche sur MathAlea pour exercices generes
- Recherche sur Maths et Tiques pour exercices corriges
- Recherche sur APMEP pour sujets de brevet avec Thales
- Synthese avec liens directs et recommandations
