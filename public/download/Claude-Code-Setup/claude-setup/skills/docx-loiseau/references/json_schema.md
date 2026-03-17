# Schéma JSON pour documents DOCX style Loiseau

## Structure racine

```json
{
  "metadata": {
    "doc_type": "Fiche Méthode",
    "number": "01",
    "title": "Dériver une fonction",
    "level": "1ère",
    "author": "Nom Auteur",
    "doc_mode": "exercice"
  },
  "versions": ["eleve", "corrige"],
  "pages": [
    {
      "components": [ ... ]
    }
  ]
}
```

## Champs metadata

| Champ | Type | Description |
|-------|------|-------------|
| `doc_type` | string | Type de document : "Fiche Méthode", "Fiche Exercices", "Évaluation", "Cours" |
| `number` | string | Numéro du document (ex: "01", "12") |
| `title` | string | Titre principal |
| `level` | string | Niveau : "6e", "5e", "4e", "3e", "2nde", "1ère", "Tle" |
| `author` | string | Auteur affiché dans le pied de page |
| `doc_mode` | string | Mode : "exercice", "cours" ou "eval" (affecte les étoiles/points) |

## Champs versions

Liste de strings parmi : `"eleve"`, `"corrige"`. Détermine quels fichiers sont générés.

## Structure d'une page

Chaque page est un objet avec un champ `components` : liste ordonnée de composants.
Le premier composant de chaque page est généralement un `header`.

## Composants

### header

```json
{
  "type": "header"
}
```

Utilise automatiquement les metadata du document. Pas de paramètres supplémentaires.

### section_title

```json
{
  "type": "section_title",
  "number": 1,
  "title": "Rappels : règles de dérivation"
}
```

### section_band

```json
{
  "type": "section_band",
  "title": "Exercices d'application directe"
}
```

### content_box

```json
{
  "type": "content_box",
  "label": "Règle",
  "subtitle": "Dérivée d'une somme",
  "content": "Si $f = u + v$ alors $f' = u' + v'$"
}
```

- `label` : Propriété, Règle, Méthode, Définition, Rappel, Remarque, Théorème, Exemple, Attention
- `subtitle` : (optionnel) sous-titre sur fond gris moyen
- `content` : texte avec formules $...$ et mots-clés **...**

### exercise

```json
{
  "type": "exercise",
  "number": 1,
  "statement": "Dériver chacune des fonctions suivantes :",
  "points": "5",
  "difficulty": 2,
  "items": [
    {
      "label": "a.",
      "content": "$f(x) = 3x^2 + 5x - 2$",
      "correction": "$f'(x) = 6x + 5$"
    },
    {
      "label": "b.",
      "content": "$g(x) = x^3 - 4x + 7$",
      "correction": "$g'(x) = 3x^2 - 4$"
    }
  ],
  "answer_grid_height": 4.0
}
```

- `number` : numéro de l'exercice
- `statement` : texte de l'énoncé global
- `points` : (optionnel) barème, affiché seulement en mode eval
- `difficulty` : (optionnel) 1-3, affiché en étoiles en mode exercice/cours
- `items` : (optionnel) liste de sous-questions avec correction
- `answer_grid_height` : (optionnel) hauteur en cm de la grille Séyès (version élève)

### items (standalone)

```json
{
  "type": "items",
  "items": [
    {"label": "a.", "content": "Question 1"},
    {"label": "b.", "content": "Question 2"}
  ],
  "layout": "list"
}
```

- `layout` : `"list"` (vertical) ou `"grid"` (grille 2 colonnes)

### answer_grid

```json
{
  "type": "answer_grid",
  "height_cm": 5.0,
  "width_cm": 19.0
}
```

### table

```json
{
  "type": "table",
  "headers": ["Fonction $f(x)$", "Dérivée $f'(x)$"],
  "rows": [
    ["$x^2$", "$2x$"],
    ["$x^3$", "$3x^2$"]
  ]
}
```

### text

```json
{
  "type": "text",
  "content": "On considère la fonction $f$ définie sur $\\mathbb{R}$...",
  "bold": false,
  "italic": false
}
```

### page_break

```json
{
  "type": "page_break"
}
```

## IMPORTANT : Espacement automatique

**NE PAS ajouter de composant `spacer` dans le JSON.** Le script gère automatiquement
l'espacement (2pt) entre tous les composants majeurs (header, section_title, section_band,
content_box, exercise, answer_grid, table, items).

## IMPORTANT : Mode mathématique obligatoire

**Toute expression mathématique** (formule, variable, nombre, symbole) doit être encadrée
par `$...$` pour être convertie en OMML natif Word. Exemples :

- `"Résoudre $2x + 3 = 7$"` — correct
- `"La fonction $f$ est définie sur $\\mathbb{R}$"` — correct
- `"Résoudre 2x + 3 = 7"` — **INCORRECT** (rendu en texte brut)

## Exemple complet minimal

```json
{
  "metadata": {
    "doc_type": "Fiche Exercices",
    "number": "03",
    "title": "Équations du second degré",
    "level": "1ère",
    "author": "M. Dupont",
    "doc_mode": "exercice"
  },
  "versions": ["eleve", "corrige"],
  "pages": [
    {
      "components": [
        {"type": "header"},
        {"type": "section_band", "title": "Exercices d'application"},
        {
          "type": "exercise",
          "number": 1,
          "statement": "Résoudre les équations suivantes :",
          "items": [
            {"label": "a.", "content": "$x^2 - 5x + 6 = 0$", "correction": "$x = 2$ ou $x = 3$"},
            {"label": "b.", "content": "$2x^2 + 3x - 2 = 0$", "correction": "$x = \\frac{1}{2}$ ou $x = -2$"}
          ],
          "answer_grid_height": 5.0
        }
      ]
    }
  ]
}
```
