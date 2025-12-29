# Animation - Le Produit Scalaire

Animation pédagogique interactive sur le produit scalaire pour le niveau Première Spécialité Mathématiques.

## Contenu

L'animation présente les trois définitions équivalentes du produit scalaire :
1. **Formule géométrique** : u · v = ||u|| × ||v|| × cos(θ)
2. **Formule analytique** : u · v = xu × xv + yu × yv
3. **Projection orthogonale** : u · v = ||u|| × OH

## Utilisation

### Version modulaire (développement)
Ouvrir `index.html` dans un navigateur après avoir lancé un serveur local :
```bash
python -m http.server 8000
```
Puis ouvrir http://localhost:8000

### Version monolithique (partage)
Ouvrir directement `produit_scalaire.html` dans un navigateur.
Ce fichier unique contient tout le code et peut être partagé facilement.

## Modes disponibles

### Mode Animation
Présentation séquentielle en 10 scènes :
1. Introduction
2. Norme d'un vecteur
3. Deux vecteurs
4. Angle θ
5. Calcul géométrique
6. Projection orthogonale
7. Formule analytique
8. Orthogonalité
9. Signe du produit scalaire
10. Récapitulatif

**Durée totale** : 78 secondes

**Contrôles** :
- Lecture/Pause
- Navigation entre scènes
- Vitesse de lecture (0.5x, 1x, 2x)

### Mode Interactif
Exploration libre avec manipulation des paramètres :

**Paramètres contrôlables** :
- x_u, y_u : Composantes du vecteur u (rouge)
- x_v, y_v : Composantes du vecteur v (bleu)
- Afficher la projection orthogonale
- Mode de formule (géométrique, analytique, projection)

**Informations affichées** :
- Coordonnées des vecteurs
- Normes ||u|| et ||v||
- Angle θ en degrés
- Produit scalaire u·v avec couleur selon le signe :
  - Vert : positif (angle aigu)
  - Bleu : nul (angle droit)
  - Orange : négatif (angle obtus)

## Structure des fichiers

```
Animation_Produit_scalaire/
├── index.html              # Version modulaire
├── produit_scalaire.html   # Version monolithique
├── build_monolith.py       # Script de génération
├── css/                    # Feuilles de style
│   ├── main.css
│   ├── timeline.css
│   └── interactive.css
├── js/                     # Scripts JavaScript
│   ├── math-utils.js       # Utilitaires mathématiques
│   ├── canvas-renderer.js  # Moteur de rendu
│   ├── animation-core.js   # Noyau d'animation
│   ├── timeline.js         # Gestion de la timeline
│   ├── controls.js         # Contrôles UI
│   ├── scenes.js           # Définition des 10 scènes
│   ├── animation-logic.js  # Logique du mode interactif
│   └── main.js            # Point d'entrée
└── scenarios/             # Scénarios pédagogiques
```

## Régénérer le fichier monolithique

```bash
python build_monolith.py -o produit_scalaire.html
```

Options disponibles :
- `-m` ou `--minify` : Minifier le code CSS/JS
- `-w` ou `--watch` : Mode surveillance (rebuild automatique)

## Propriétés mathématiques présentées

1. **Norme d'un vecteur** : ||u|| = √(xu² + yu²)

2. **Trois formules équivalentes** :
   - Géométrique : u · v = ||u|| × ||v|| × cos(θ)
   - Analytique : u · v = xu × xv + yu × yv
   - Projection : u · v = ||u|| × OH où H est la projection de v sur u

3. **Orthogonalité** : u ⊥ v ⟺ u · v = 0

4. **Signe du produit scalaire** :
   - u · v > 0 ⟺ angle aigu (θ < 90°)
   - u · v = 0 ⟺ angle droit (θ = 90°)
   - u · v < 0 ⟺ angle obtus (θ > 90°)

## Compatibilité

- Navigateurs modernes (Chrome, Firefox, Safari, Edge)
- Pas de dépendance externe
- Fonctionne hors ligne (version monolithique)

## Auteur

Animation créée avec le template interactive-animation.
