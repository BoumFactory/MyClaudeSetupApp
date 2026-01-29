# Skill: html-katex-compiler

Skill complet pour créer, éditer et compiler des cours HTML interactifs avec rendu mathématique KaTeX. Produit des fichiers autonomes fonctionnant 100% hors-ligne avec sélecteur d'univers visuel, mode dark/light et infobulles de vocabulaire.

## Quand utiliser ce skill

- Création de supports de cours HTML pour projection en classe
- Documents mathématiques interactifs avec formules LaTeX (KaTeX)
- Cours consultables sur tablette/web hors-ligne
- Alternative au format PDF pour les cours projetés

## Fonctionnalités du Fichier Final

Le fichier HTML généré inclut :
- **Sélecteur d'univers** : 8 styles visuels au choix (⚙️ en haut à droite)
- **Mode dark/light** : Clair, Sombre ou Auto (selon système)
- **Infobulles de vocabulaire** : Définitions au survol des termes
- **100% hors-ligne** : KaTeX et styles embarqués
- **Responsive** : S'adapte à tous les écrans

---

## Système de Styles

### Les 3 Paramètres de Style

| Paramètre | Description | Rôle |
|-----------|-------------|------|
| `niveau` | Niveau scolaire | Taille police, espacement, densité |
| `theme` | Thème mathématique | Palette de couleurs |
| `univers` | Style visuel global | Look and feel |

### Niveaux Disponibles

| ID | Nom | Caractéristiques |
|----|-----|------------------|
| `6eme` | Sixième | Grande police, très aéré |
| `5eme` | Cinquième | Police lisible |
| `4eme` | Quatrième | Équilibré |
| `3eme` | Troisième | Prépa lycée |
| `2nde` | Seconde | Style lycée standard |
| `1ere` | Première | Plus dense |
| `tle` | Terminale | Compact |
| `sup` | Supérieur | Dense, académique |

### Thèmes Mathématiques (Couleurs)

| ID | Domaine | Couleur dominante |
|----|---------|-------------------|
| `geometrie` | Géométrie | Bleu/Cyan |
| `analyse` | Fonctions, dérivées | Vert/Émeraude |
| `algebre` | Équations | Violet/Mauve |
| `probabilites` | Probabilités | Orange/Ambre |
| `statistiques` | Statistiques | Rouge/Corail |
| `arithmetique` | Nombres | Jaune/Or |
| `trigonometrie` | Trigonométrie | Turquoise |
| `complexes` | Nombres complexes | Indigo |
| `suites` | Suites numériques | Teal |
| `vecteurs` | Vecteurs | Bleu marine |

### Univers Graphiques (Style Global)

| ID | Style | Recommandé pour |
|----|-------|-----------------|
| `standard` | Classique, sobre, professionnel | Tout public |
| `minimal` | Épuré, beaucoup de blanc | Focus contenu |
| `paper` | Effet cahier avec lignes | Collège |
| `nature` | Tons terreux, organique | Calme |
| `retro` | Vintage, sépia | Nostalgie |
| `manga` | Dynamique, badges colorés | Collège ludique |
| `futuriste` | Dark mode, néon, high-tech | Lycée/Sup |
| `gaming` | Énergique, contrasté, RGB | Ados |

---

## Architecture d'un Projet

```
mon-cours/
├── parts/                    # Contenu modulaire
│   ├── 01-introduction.html
│   ├── 02-definitions.html
│   ├── XX-section.html
│   └── figures.tikz          # [OPTIONNEL] Figures TikZ
├── config.json               # Configuration
└── output/                   # Fichiers compilés
    └── titre-ONEFILE.html
```

---

## Figures TikZ (Optionnel)

Le système permet d'écrire les figures géométriques en **TikZ pur** et de les compiler automatiquement en SVG base64 lors de la génération du HTML.

### Avantages

- **Syntaxe LaTeX native** : Utilisez vos styles et commandes TikZ habituels
- **Qualité vectorielle** : Figures parfaitement nettes à toute échelle
- **Cohérence visuelle** : Styles unifiés pour toutes les figures
- **Un seul fichier** : Toutes les figures dans `figures.tikz`

### Format du fichier `figures.tikz`

```latex
%% FIGURE: triangle-rectangle
\begin{tikzpicture}
    \coordinate (A) at (0,0);
    \coordinate (B) at (3,0);
    \coordinate (C) at (0,2);
    \draw[thick] (A) -- (B) -- (C) -- cycle;
    % ... reste du code TikZ
\end{tikzpicture}

%% FIGURE: mediatrice
\begin{tikzpicture}
    % ... code de la figure
\end{tikzpicture}
```

### Usage dans les parties HTML

```html
<div class="figure-container" style="text-align: center;">
    {{tikz:triangle-rectangle}}
</div>
```

### Styles TikZ prédéfinis

Le préambule inclut automatiquement :
- `point/.style` : Points avec cercles pleins
- `ligne/.style`, `droite/.style` : Lignes et droites
- `vecteur/.style` : Flèches de vecteurs
- `angle droit/.style` : Marquage d'angle droit
- `mark segment/.style` : Codage d'égalité de segments
- `couleur1`, `couleur2`, `couleur3`, `couleur4` : Couleurs thématiques
- `axe/.style`, `grille/.style` : Pour les repères

### Prérequis système

- **pdflatex** (MiKTeX ou TeX Live)
- **dvisvgm** ou **pdf2svg** pour la conversion PDF→SVG

---

## Scripts

### Initialisation

```bash
python ".claude/skills/html-katex-compiler/scripts/init_project.py" <chemin> [options]

Options:
  --titre "Titre du cours"
  --niveau 6eme|5eme|4eme|3eme|2nde|1ere|tle|sup
  --theme geometrie|analyse|algebre|probabilites|...
  --univers standard|manga|futuriste|nature|retro|minimal|gaming|paper
```

Exemples :
```bash
# Cours classique
python ".claude/skills/html-katex-compiler/scripts/init_project.py" "mon-cours" --titre "Les Vecteurs" --niveau 2nde --theme vecteurs

# Cours fun pour collège
python ".claude/skills/html-katex-compiler/scripts/init_project.py" "mon-cours" --titre "Géométrie" --niveau 6eme --theme geometrie --univers manga

# Cours avancé style tech
python ".claude/skills/html-katex-compiler/scripts/init_project.py" "mon-cours" --titre "Analyse" --niveau tle --theme analyse --univers futuriste
```

### Compilation

```bash
python ".claude/skills/html-katex-compiler/scripts/compile_project.py" <chemin> [options]

Options:
  --output nom.html        # Nom du fichier de sortie
  --no-vocabulary         # Désactiver les infobulles
  --no-theme-switcher     # Désactiver le sélecteur d'univers
```

---

## Format config.json

```json
{
  "titre": "Les Vecteurs du Plan",
  "niveau": "2nde",
  "niveau_label": "Seconde",
  "theme": "vecteurs",
  "univers": "standard",
  "auteur": "M. Dupont",
  "parts_order": ["01-introduction", "02-definition", "03-operations"],
  "vocabulary": true,
  "theme_switcher": true
}
```

---

## Édition du Contenu (parts/*.html)

### Structure de Base

```html
<!-- XX-titre-section.html -->
<h2>X. Titre de la Section</h2>

<div class="definition">
    <strong>Titre optionnel</strong><br>
    Contenu avec formule : $x^2 + y^2 = r^2$
</div>
```

### Blocs Pédagogiques Disponibles

| Classe | Usage | Couleur |
|--------|-------|---------|
| `.definition` | Définitions formelles | Bleu |
| `.theoreme` | Théorèmes à retenir | Violet |
| `.propriete` | Propriétés importantes | Vert |
| `.exemple` | Exemples d'application | Orange |
| `.methode` | Méthodes et procédures | Cyan |
| `.remarque` | Remarques et notes | Gris |
| `.exercice` | Exercices à faire | Jaune |
| `.demonstration` | Preuves | Rose |
| `.attention` | Points d'attention | Rouge |
| `.rappel` | Rappels de notions | Bleu clair |
| `.astuce` | Astuces et conseils | Vert clair |

**Note** : Le label (Définition, Théorème, etc.) est ajouté automatiquement par le CSS.

### Exemples de Blocs

```html
<div class="definition">
    <strong>Fonction polynôme du second degré</strong><br>
    Une fonction polynôme du second degré est définie sur $\mathbb{R}$ par :
    $$f(x) = ax^2 + bx + c$$
    où $a$, $b$, $c$ sont des réels avec $a \neq 0$.
</div>

<div class="theoreme">
    <strong>Théorème de Pythagore</strong><br>
    Dans un triangle rectangle :
    $$a^2 + b^2 = c^2$$
</div>

<div class="methode">
    <strong>Résoudre une équation du second degré</strong><br>
    <ol>
        <li>Mettre sous forme $ax^2 + bx + c = 0$</li>
        <li>Calculer $\Delta = b^2 - 4ac$</li>
        <li>Conclure selon le signe de $\Delta$</li>
    </ol>
</div>

<div class="attention">
    <strong>Erreur fréquente</strong><br>
    $(a + b)^2 \neq a^2 + b^2$ en général !
</div>

<div class="exercice">
    <strong>Exercice 1</strong><br>
    Soit $\vec{u}(3; 4)$. Calculer $\|\vec{u}\|$.
</div>
```

---

## Formules Mathématiques (KaTeX)

### Syntaxe

| Type | Syntaxe | Usage |
|------|---------|-------|
| Inline | `$formule$` | Dans le texte |
| Display | `$$formule$$` | Formule centrée |
| Alternatif | `\(...\)` et `\[...\]` | Compatible LaTeX |

### Commandes Courantes

```latex
% Fractions
$\frac{a}{b}$, $\dfrac{a}{b}$

% Racines
$\sqrt{x}$, $\sqrt[n]{x}$

% Vecteurs
$\vec{u}$, $\vec{AB}$, $\overrightarrow{AB}$

% Normes
$\|u\|$, $\|\vec{AB}\|$

% Ensembles
$\mathbb{R}$, $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$

% Alignement multiligne
$$\begin{aligned}
f(x) &= x^2 + 2x + 1 \\
     &= (x + 1)^2
\end{aligned}$$

% Système
$$\begin{cases}
2x + y = 5 \\
x - y = 1
\end{cases}$$
```

---

## Vocabulaire Interactif

### Infobulle Simple

```html
<span class="vocab" data-definition="Explication au survol">terme</span>
```

### Catégories Avancées

| Classe | Catégorie | Style |
|--------|-----------|-------|
| `.tip-def` | Définition | Rouge rubis |
| `.tip-formule` | Formule | Orange |
| `.tip-prop` | Propriété | Vert émeraude |
| `.tip-attention` | Attention | Rouge vif |
| `.tip-astuce` | Astuce | Cyan |
| `.tip-lien` | Lien vers autre notion | Bleu |

```html
<span class="tip-def" data-definition="Objet avec direction, sens et norme">vecteur</span>
<span class="tip-formule" data-definition="Toujours vraie pour triangles rectangles">a² + b² = c²</span>
```

---

## Autres Éléments HTML

### Listes

```html
<ul>
    <li>Premier élément</li>
    <li>Avec $formule$</li>
</ul>

<ol>
    <li>Étape 1</li>
    <li>Étape 2</li>
</ol>
```

### Tableaux

```html
<table>
    <tr>
        <th>$x$</th>
        <th>$f(x)$</th>
    </tr>
    <tr>
        <td>0</td>
        <td>1</td>
    </tr>
</table>
```

### Figures

```html
<figure>
    <img src="images/figure.png" alt="Description">
    <figcaption>Légende</figcaption>
</figure>
```

### Utilitaires CSS

| Classe | Effet |
|--------|-------|
| `.text-center` | Centre le texte |
| `.highlight` | Surligne en jaune |
| `.important` | Texte coloré important |
| `.formule` | Encadre une formule |

---

## Workflow Complet

1. **Initialiser** le projet :
   ```bash
   python ".claude/skills/html-katex-compiler/scripts/init_project.py" "chemin" --titre "..." --niveau X --theme Y --univers Z
   ```

2. **Éditer** les fichiers `parts/*.html` avec les blocs pédagogiques

3. **Mettre à jour** `config.json` si nouvelles parties :
   ```json
   "parts_order": ["01-intro", "02-defs", "03-props"]
   ```

4. **Compiler** :
   ```bash
   python ".claude/skills/html-katex-compiler/scripts/compile_project.py" "chemin"
   ```

5. **Ouvrir** le fichier dans `output/` pour vérifier

---

## Bonnes Pratiques

### RÈGLE OBLIGATOIRE : Vocabulaire Interactif Exhaustif

**TOUS les termes techniques mathématiques DOIVENT avoir une infobulle de définition.**

Le système de vocabulaire est **automatique** : les termes présents dans la banque (`vocabulary.json`) sont détectés et annotés automatiquement par le JavaScript.

#### Comment ça fonctionne

1. **Détection automatique** : Le JS scanne le texte et détecte les termes de la banque
2. **Infobulles riches** : Au survol, affichage de la définition + formule KaTeX
3. **Adaptation visuelle** : Les infobulles s'adaptent à l'univers choisi

#### Termes déjà dans la banque (détection automatique)

| Catégorie | Termes détectés automatiquement |
|-----------|--------------------------------|
| **Géométrie** | perpendiculaire, parallèle, sécante, médiatrice, hypoténuse, cercle, diamètre, angle droit, angle aigu |
| **Triangles** | triangle rectangle, triangle isocèle, triangle équilatéral |
| **Trigonométrie** | cosinus, sinus, tangente, côté adjacent, côté opposé |
| **Théorèmes** | théorème de Pythagore, théorème de Thalès |
| **Vecteurs** | vecteur, norme, coordonnées, colinéaire, produit scalaire |
| **Analyse** | fonction, dérivée, primitive, intégrale, limite, suite |
| **Probabilités** | probabilité, espérance, variance, écart-type |

#### Syntaxe pour définitions personnalisées

Pour un terme **pas dans la banque** ou pour **override** une définition :

```html
<!-- Définition manuelle (override ou terme custom) -->
<span class="vocab" data-definition="Ma définition personnalisée">mon terme</span>
```

#### Enrichir la banque

Pour ajouter des termes permanents, modifier `assets/vocabulary.json` :

```json
{
  "mon_terme": {
    "definition": "Définition claire et concise.",
    "formula": "\\LaTeX",
    "category": "geometrie",
    "niveau": ["3eme", "2nde"],
    "synonyms": ["variante1", "variante2"]
  }
}
```

### Organisation Progressive

1. **Rappels** → `.rappel`
2. **Définitions** → `.definition`
3. **Propriétés/Théorèmes** → `.propriete`, `.theoreme`
4. **Exemples** → `.exemple`
5. **Méthodes** → `.methode`
6. **Exercices** → `.exercice`

### Découpage en Parties

Pour un cours complet, créer plusieurs fichiers :

```
parts/
├── 01-introduction.html
├── 02-definitions.html
├── 03-proprietes.html
├── 04-methodes.html
├── 05-exercices.html
└── 06-synthese.html
```

### Marquer le Vocabulaire

```html
<!-- Toujours expliquer les termes clés -->
Un <span class="vocab" data-definition="Objet défini par direction, sens et norme">vecteur</span> est...
```

### Contextualiser les Formules

```html
<!-- Toujours introduire les formules -->
<p>Les solutions sont données par :</p>
$$x = \frac{-b \pm \sqrt{\Delta}}{2a}$$
```

---

## Comparaison avec LaTeX (bfcours)

| Concept | HTML/KaTeX | LaTeX/bfcours |
|---------|------------|---------------|
| Définition | `<div class="definition">` | `\begin{Definition}` |
| Emphase | `<strong>` | `\acc{}` |
| Vocabulaire | `<span class="vocab">` | `\voc{}` |
| Liste | `<ol>` | `\begin{tcbenumerate}` |
| Tableau | `<table>` | `\begin{tcbtab}` |
| Formule | `$...$` / `$$...$$` | `$...$` / `\[...\]` |

---

## Quand Choisir HTML vs LaTeX ?

| Critère | HTML (ce skill) | LaTeX (/createTex) |
|---------|-----------------|-------------------|
| **Usage** | Projection, web | Impression, documents officiels |
| **Interactivité** | Oui (univers, dark mode) | Non (PDF statique) |
| **Modifications** | Édition directe | Recompilation |
| **Recommandé** | Cours projetés, révisions | Évaluations, fiches élèves |
