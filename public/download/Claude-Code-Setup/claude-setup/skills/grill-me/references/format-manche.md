# Format d'une manche (entrée de `manche_html.py`)

Une manche est un fichier Markdown : un front-matter facultatif, puis une section `##` par question.

## Commande

```
PYTHONIOENCODING=utf-8 python ".claude/skills/grill-me/scripts/manche_html.py" "<chemin>/manche-01.md" [--sortie fichier.html] [--pas-ouvrir]
```

Le script affiche le chemin du HTML produit (écrit à côté du `.md` par défaut) et l'ouvre dans le navigateur par défaut. En cas d'erreur de format, il indique la ligne fautive et rend le code de sortie 1.

## Structure

- **Front-matter** (facultatif), entre deux lignes `---` : `titre:` (défaut : nom du fichier) et `contexte:` (rappel de une ou deux lignes).
- **Question** : un titre `## Q1 — Titre court`. Le préfixe `Q<n> —` est retiré, les questions sont numérotées dans l'ordre.
- **`type:`** : `unique` (boutons radio), `multiple` (cases à cocher) ou `libre` (texte seulement). Défaut : `unique` s'il y a des options, `libre` sinon.
- **Corps** : Markdown minimal (paragraphes, `**gras**`, `*italique*`, `` `code` ``, listes à puces, liens).
- **`reco:`** (facultatif) : justification courte de la recommandation, affichée dans l'encart « Ma recommandation ». Elle peut courir sur plusieurs lignes jusqu'à la première ligne vide.
- **Options** : la **dernière liste à puces contiguë** du bloc, à condition que rien d'autre (hors `reco:`) ne la suive. Les listes à puces plus haut dans le bloc font partie du corps.
  - `- Label : description` (le séparateur est ` : `, la description est facultative).
  - `- [reco] Label : description` marque l'option recommandée : préselectionnée et badgée « Recommandé ». Une seule pour `unique`, plusieurs possibles pour `multiple`.

## Rendu et réponses

- Mode focus : une question à la fois ; raccourcis `1`..`9` (option), `Entrée` ou `→` (suivant), `←` (précédent), `t` (zone de texte).
- Chaque question a une zone de texte libre avec dictée vocale (Chrome ou Edge).
- « Copier les réponses » produit :

```
# Réponses — <titre>
Q1 — <titre> : <option(s) choisie(s) séparées par « + »> (recommandé)
  > commentaire libre éventuel
Q2 — <titre> : NON RÉPONDU
```

« (recommandé) » apparaît si le choix correspond exactement à la recommandation.

## Exemple complet

Voir `assets/exemple-manche.md` (trois questions : `unique`, `multiple`, `libre`).

```
---
titre: Manche 1 — Cadrage du projet
contexte: Rappel du sujet en une ou deux lignes.
---

## Q1 — Point d'entrée
type: unique
Corps de la question, avec **gras** et une liste :

- élément du corps

reco: Option A, parce que c'est le plus simple.

- [reco] Option A : description
- Option B : description

## Q2 — Question ouverte
type: libre
Quelles contraintes faut-il connaître ?
```

## Limites

- La dictée vocale dépend de l'API Web Speech : absente de Firefox, parfois bloquée sur une page ouverte en `file://` (le navigateur redemande alors l'autorisation du micro à chaque ouverture).
- Un bloc `type: unique` ou `multiple` sans liste d'options est refusé.
