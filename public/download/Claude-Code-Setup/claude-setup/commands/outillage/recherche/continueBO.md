# /continueBO - Poursuite de l'extraction des compétences BO

Commande pour continuer l'extraction automatique des compétences depuis les pages des Bulletins Officiels.

## Protocole d'exécution

### 1. Lecture du fichier de statut

Lis le fichier `.claude/skills/programmes-officiels/data/extraction_status.json` pour connaître :
- Les pages déjà traitées (`completed`)
- Les pages en cours (`in_progress`)
- Les pages en attente (`pending`)
- Les échecs (`failed`)

### 2. Sélection des pages à traiter

Pour chaque BO dans `bo_status`, sélectionne jusqu'à **$BATCH_SIZE** pages pending au total (par défaut 8 pages).

Priorise les BO dans cet ordre :
1. BO avec le moins de pages restantes (finir les petits d'abord)
2. À nombre égal, ordre alphabétique

### 3. Lancement des agents

Pour chaque page sélectionnée, lance un agent `bo-competence-extractor` avec :

```
Fichier source : .claude/skills/programmes-officiels/data/pages/{BO}/{page}.txt
Fichier sortie : .claude/skills/programmes-officiels/data/extractions/{BO}/{page}_competences.json
Niveau : {niveau du BO}
PDF source : {pdf du BO}

Instructions :
1. Lis le fichier texte de la page
2. Identifie toutes les compétences atomiques
3. Atomise chaque élément en compétences unitaires testables
4. Structure le JSON avec métadonnées (niveau, thème, type, source)
5. Écris le fichier JSON

IMPORTANT - Rapport de fin :
À la fin, fournis un résumé structuré :
- BO traité : {nom}
- Page : {numéro}
- Nb compétences extraites : X
- Types : {contenus: N, capacités: N, ...}
- Domaines couverts : [liste]
- Fichier créé : {chemin}
```

Lance les agents en **parallèle** (un seul appel Task avec plusieurs agents).

### 4. Mise à jour du statut

Après réception des résultats de TOUS les agents :

1. Mets à jour `extraction_status.json` :
   - Déplace les pages traitées de `pending` vers `completed`
   - Note les échecs dans `failed` avec le message d'erreur
   - Met à jour `last_updated` et le compteur `completed`

2. Affiche un résumé :
```
## Batch terminé

| BO | Pages traitées | Compétences | Statut |
|----|----------------|-------------|--------|
| 1GT | page_001, page_002 | 87 | OK |
| ... | ... | ... | ... |

Progression globale : X/214 pages (Y%)
Prochaines pages : [liste des 8 prochaines]
```

### 5. Proposition de continuation

Si des pages sont encore en pending :
> "Il reste N pages à traiter. Lancer le prochain batch avec `/continueBO` ?"

## Arguments optionnels

- `$BATCH_SIZE` : Nombre de pages par batch (défaut: 8)
- `$BO` : Limiter à un BO spécifique (ex: "1GT")
- `$FORCE` : Retraiter les pages même si déjà complétées

## Exemple d'utilisation

```
/continueBO                    # Batch standard de 8 pages
/continueBO BATCH_SIZE=16      # Batch de 16 pages
/continueBO BO=cycle3_v2       # Uniquement le cycle 3
```

## Gestion des erreurs

- Si un agent échoue, note la page dans `failed` avec le contexte
- Ne bloque pas les autres agents
- Propose de relancer les pages en échec à la fin
