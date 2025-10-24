# Arbres de Probabilités - ProfLycee

## Commande principale : `\ArbreProbasTikz`

### Syntaxe
```latex
\ArbreProbasTikz[options]{données}
```

### Options disponibles (clés KV)
- `InclineProbas=true/false` : incline les étiquettes de probabilité
- `Fleche=true/false` : affiche des flèches sur les arcs
- `type` : type d'arbre (2x2, etc.)
- `racine` : étiquette pour le nœud racine
- `unite` : unité de mesure TikZ
- `espniv` : espacement entre niveaux
- `espfeuille` : espacement entre feuilles
- `font` : police des nœuds
- `fontproba` : police des probabilités
- `colnoeuds` : couleur des nœuds
- `colprobas` : couleur des probabilités
- `typetrait` : type de trait
- `eptrait` : épaisseur des traits
- `colarc` : couleur des arcs
- `colback` : couleur de fond des étiquettes

### Structure des données
Les données sont structurées sous forme de liste avec séparateurs :
- Niveau 1 : virgule (,) sépare les branches
- Niveau 2 : point (.) sépare nœud/probabilité/position
- Niveau 3 : slash (/) sépare les éléments individuels

### Exemple d'utilisation
```latex
\ArbreProbasTikz[type=2x2,racine=S]{
    A/0.6/above,
    A∩B/0.7/above,
    A∩B̄/0.3/below,
    Ā/0.4/below,
    Ā∩B/0.5/above,
    Ā∩B̄/0.5/below
}
```

## Environnement : `EnvArbreProbasTikz`

Alternative sous forme d'environnement :
```latex
\begin{EnvArbreProbasTikz}[options]{données}
% Contenu additionnel si nécessaire
\end{EnvArbreProbasTikz}
```

## Styles TikZ intégrés
- `noeud` : style pour les nœuds de l'arbre
- `probas` : style pour les étiquettes de probabilité
- `PLetiquette` : style pour le positionnement des étiquettes
- `PLfleche` : style pour les flèches/arcs

## Types d'arbres supportés
- `2x2` : arbre binaire à deux niveaux (4 issues finales)
- Extensions possibles selon les développements futurs

## Placement des probabilités
- `above` : au-dessus de l'arc
- `below` : en-dessous de l'arc  
- `sur` : sur l'arc avec fond coloré
- Position automatique selon l'orientation