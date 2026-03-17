---
name: pdf2tikz
description: "Convertisseur PDF vers TikZ via extraction vectorielle SVG + analyse de disposition. Utiliser ce skill quand l'utilisateur veut extraire des figures d'un PDF, convertir un PDF en TikZ, recuperer le code TikZ d'un document compile, transformer des graphiques PDF en code LaTeX editable, analyser la disposition/layout d'un PDF pour reproduire sa mise en page, ou mentions 'pdf2tikz', 'pdf to tikz', 'extraire tikz', 'figure pdf vers tikz', 'svg to tikz', 'analyser layout', 'disposition pdf'. Utiliser de maniere proactive quand l'utilisateur travaille avec des PDF contenant des figures geometriques et veut les editer en TikZ, ou quand il veut reproduire la mise en page d'un document existant."
---

# pdf2tikz — Extracteur PDF vers TikZ + Analyse de disposition

Deux outils complementaires pour reproduire fidelement un document PDF :

1. **Extraction TikZ** : convertit les figures vectorielles en code TikZ editable
2. **Analyse de disposition** : detecte l'agencement des elements (colonnes, tableaux, graphiques, boites d'annotation) pour reproduire la mise en page

## Workflow recommande : reproduire un document PDF

Quand l'utilisateur fournit un PDF source a reproduire en LaTeX :

### Etape 1 — Analyse de disposition (layout)

```bash
python .claude/skills/pdf2tikz/scripts/layout_analyze.py document.pdf --format markdown
```

Cela produit une analyse zone-par-zone de chaque page :
- **Zones horizontales** : bandes de contenu separees par des espaces verticaux
- **Colonnes detectees** : ratio, largeur, contenu de chaque colonne
- **Classification du contenu** : texte, tableau, graphique (barres/circulaire/cartesien), boite d'annotation
- **Semantique** : definition, exemple, titre de section, etc.
- **Couleurs** : codes hex des fonds colores et surlignages

Exemple de sortie :
```
### Zone 4 (y=9.59-15.09cm) — 2 colonnes (50:50)
  Col 1: [example] text — 8.35x5.5cm
    "Exemple(s) : Moyen de transport..."
    Couleurs: #c1e7f7
  Col 2: [example] table — 8.5x4.3cm
    Tableau 2x2: Longueur de quatre fleuves...
    Couleurs: #c1e7f7
```

→ Cela indique qu'il faut un `\begin{MultiColonnes}{2}` avec deux `\tcbitem` contenant respectivement un tableau et une boite d'annotation.

### Etape 2 — Extraction des figures TikZ

```bash
python .claude/skills/pdf2tikz/scripts/pdf2tikz.py document.pdf --page 1 --svg-bridge
```

Extrait les chemins vectoriels (lignes, courbes, rectangles) page par page.

### Etape 3 — Reconstruction LaTeX

Utiliser l'analyse de disposition pour structurer le document LaTeX :
- Les zones a **N colonnes** → `\begin{MultiColonnes}{N}` avec `\tcbitem`
- Les zones **pleine largeur** → contenu standard
- Les **tableaux** detectes → `\begin{tcbtab}[Titre]{format}`
- Les **graphiques** detectes → `\tikzinclude{NOM}` avec le code TikZ extrait
- Les **boites d'annotation** → `\begin{tcolorbox}[colback=...]`
- Les **fleches** entre tableau et annotation → `\annoflecheR[couleur]{src}{dst}{H}`

## Scripts disponibles

### layout_analyze.py — Analyse de disposition

```bash
python .claude/skills/pdf2tikz/scripts/layout_analyze.py document.pdf [options]
```

Options :
- `--pages 1,2,3` : pages specifiques (defaut: toutes)
- `--format markdown|json|both` : format de sortie (defaut: markdown)
- `--output FILE` : fichier de sortie (defaut: stdout)

Detecte :
- **Zones horizontales** via analyse des blocs texte (pas des decorations)
- **Colonnes** via analyse des ecarts horizontaux entre elements
- **Tableaux** via grilles de lignes h/v avec separateurs
- **Graphiques** via detection d'axes (barres/lignes) ou secteurs (circulaire)
- **Fleches d'annotation** via triangles remplis + lignes colorees/pointillees
- **Boites colorees** via rectangles remplis (fond de cellule, annotation)
- **Semantique textuelle** : detection de patterns (Definition, Exemple, section)

### pdf2tikz.py — Extraction vectorielle

```bash
python .claude/skills/pdf2tikz/scripts/pdf2tikz.py document.pdf [options]
```

Options :
- `--page N` / `--pages 1,3,5` : pages a extraire
- `--output FILE` : fichier de sortie
- `--svg-bridge` : extraction via SVG (recommande, capture les overlays tikzmark)
- `--scale FACTOR` / `--precision N` / `--colors named|rgb`
- `--standalone` : document LaTeX complet
- `--cluster` : regrouper les chemins proches
- `--no-text` : pas de labels texte

## Mapping PDF → TikZ

| Primitif PDF | TikZ |
|---|---|
| ligne | `\draw (x1,y1) -- (x2,y2);` |
| courbe Bezier | `.. controls (cx1,cy1) and (cx2,cy2) .. (x3,y3)` |
| rectangle | `(x,y) rectangle (x2,y2)` |
| cercle (detecte) | `(cx,cy) circle (r)` |
| couleur stroke/fill | `[draw=color]` / `[fill=color]` |
| epaisseur | `[line width=Xpt]` |
| pointilles | `[dashed]` |

## Dependances

- Python 3.8+
- PyMuPDF (`pip install pymupdf`) — deja installe
