# Catalogue des Styles

Système modulaire à 3 axes pour générer des styles de cours uniques.

## Axe 1 : Niveau

Adapte la typographie, la taille, l'espacement selon le public.

| ID | Nom | Description |
|----|-----|-------------|
| `6eme` | Sixième | Grande police, espacement aéré, blocs très visibles |
| `5eme` | Cinquième | Police lisible, couleurs vives |
| `4eme` | Quatrième | Équilibre lisibilité/densité |
| `3eme` | Troisième | Préparation lycée, plus compact |
| `2nde` | Seconde | Style lycée, police moyenne |
| `1ere` | Première | Plus dense, vocabulaire technique |
| `tle` | Terminale | Compact, style pré-universitaire |
| `sup` | Supérieur | Dense, académique, sobre |

## Axe 2 : Thème mathématique

Palette de couleurs et iconographie selon le domaine.

| ID | Nom | Couleur dominante | Associations |
|----|-----|-------------------|--------------|
| `geometrie` | Géométrie | Bleu/Cyan | Formes, compas, règle |
| `analyse` | Analyse | Vert/Émeraude | Courbes, dérivées, intégrales |
| `algebre` | Algèbre | Violet/Mauve | Équations, lettres, structures |
| `probabilites` | Probabilités | Orange/Ambre | Dés, cartes, arbres |
| `statistiques` | Statistiques | Rouge/Corail | Graphiques, données |
| `arithmetique` | Arithmétique | Jaune/Or | Nombres, divisibilité |
| `trigonometrie` | Trigonométrie | Turquoise | Cercle, angles, ondes |
| `complexes` | Nombres complexes | Indigo | Plan complexe, spirales |
| `suites` | Suites | Teal | Séquences, récurrence |
| `vecteurs` | Vecteurs | Bleu marine | Flèches, translations |

## Axe 3 : Univers graphique

Style visuel global qui donne une identité au document.

| ID | Nom | Description | Éléments caractéristiques |
|----|-----|-------------|---------------------------|
| `standard` | Académique | Classique, sobre, professionnel | Serif, bordures fines, fond blanc |
| `manga` | Manga | Dynamique, expressif | Bordures épaisses, ombres, badges colorés |
| `futuriste` | Futuriste | High-tech, néon | Sans-serif, gradients, effet glow |
| `nature` | Nature | Organique, apaisant | Tons terreux, coins arrondis, textures |
| `retro` | Rétro | Vintage, nostalgique | Sépia, typographie ancienne, cadres |
| `minimal` | Minimaliste | Épuré, essentiel | Beaucoup de blanc, traits fins |
| `gaming` | Gaming | Énergique, moderne | Couleurs vives, angles, contraste fort |
| `paper` | Papier | Effet cahier/carnet | Lignes, effet papier, marges |

## Combinaisons exemple

| Niveau | Thème | Univers | Résultat |
|--------|-------|---------|----------|
| 2nde | vecteurs | standard | Cours classique lycée |
| 6eme | geometrie | manga | Géométrie fun et accessible |
| tle | analyse | futuriste | Analyse moderne et dense |
| 3eme | probabilites | gaming | Probas engageantes pour ados |
| sup | complexes | minimal | Style universitaire épuré |

## Structure technique

```
styles/
├── base.css              # Reset et fondations communes
├── niveaux/
│   ├── 6eme.css
│   ├── 5eme.css
│   └── ...
├── themes/
│   ├── geometrie.css
│   ├── analyse.css
│   └── ...
└── univers/
    ├── standard.css
    ├── manga.css
    └── ...
```

Le CSS final est assemblé : `base.css` + `niveau.css` + `theme.css` + `univers.css`
