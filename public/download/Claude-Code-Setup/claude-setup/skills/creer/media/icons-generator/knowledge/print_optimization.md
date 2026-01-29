# Optimisation pour l'impression

Guide pratique pour g\u00e9n\u00e9rer et pr\u00e9parer des images optimis\u00e9es pour l'impression \u00e9conomique.

## Principes d'\u00e9conomie d'encre

### 1. Limiter le nombre de couleurs

**Co\u00fbt relatif par type :**
- Noir uniquement : 1x (r\u00e9f\u00e9rence)
- Noir + 1 couleur : 1.5x
- Noir + 2 couleurs : 2x
- Noir + 3 couleurs : 2.5x
- 4+ couleurs : 3x+

**Recommandations :**
- Fiches quotidiennes : noir + 1 couleur maximum
- Activit\u00e9s sp\u00e9ciales : 3-4 couleurs maximum
- \u00c9valuations : noir uniquement ou noir + 1 couleur

### 2. Privil\u00e9gier les fonds blancs

**\u00c9conomie :**
- Fond blanc : 0% de couverture
- Fond gris clair (10%) : +10% d'encre noire
- Fond color\u00e9 clair : +15-20% d'encre couleur
- Fond satur\u00e9 : +50-100% de consommation

**Toujours sp\u00e9cifier dans les prompts :**
```
white background
```

### 3. Utiliser des traits plutôt que des aplats

**\u00c9conomie :**
- Contours (line art) : Consommation minimale
- Aplats de couleur : Consommation moyenne-\u00e9lev\u00e9e
- D\u00e9grad\u00e9s : Consommation maximale

**Privil\u00e9gier :**
```
simple line art, clean lines, outline style
```

**\u00c9viter :**
```
filled shapes, solid colors, gradients
```

---

## Optimisation technique

### R\u00e9solution recommand\u00e9e

**Pour impression :**
- Minimum : 300 DPI
- Recommand\u00e9 : 600 DPI pour line art
- Format : PNG ou PDF vectoriel

**Dimensions selon usage :**
- Pleine page A4 : 2480 x 3508 px (300 DPI)
- Demi-page : 1240 x 1754 px
- Petite illustration : 800 x 800 px minimum

### Format de fichier

**PNG (Raster) :**
- Avantages : Compatibilit\u00e9 universelle, bonne pour line art
- Inconv\u00e9nients : Pas scalable, taille de fichier

**SVG (Vectoriel) - si possible :**
- Avantages : Scalable, fichiers l\u00e9gers, parfait pour line art
- Inconv\u00e9nients : Support limit\u00e9 par certaines API

**PDF :**
- Avantages : Excellent pour impression, garde la qualit\u00e9
- Inconv\u00e9nients : Plus lourd

---

## Palettes de couleurs recommand\u00e9es

### Palette 2 couleurs (\u00e9conomique)

**Option 1 : Math\u00e9matiques**
- Noir (#000000)
- Bleu (#0066CC)

**Option 2 : Sciences**
- Noir (#000000)
- Vert (#009933)

**Option 3 : Fran\u00e7ais/Histoire**
- Noir (#000000)
- Rouge brique (#CC3300)

### Palette 3 couleurs (standard)

**Option 1 : Polyvalente**
- Noir (#000000)
- Bleu (#0066CC)
- Orange (#FF9900)

**Option 2 : Scientifique**
- Noir (#000000)
- Bleu (#0066CC)
- Vert (#009933)

**Option 3 : Storytelling**
- Noir (#000000)
- Rouge (#CC3300)
- Jaune or (#FFCC00)

### Palette 4-5 couleurs (sp\u00e9cial)

**Pour escape games et activit\u00e9s th\u00e9matis\u00e9es :**
- Noir (#000000)
- Brun s\u00e9pia (#8B4513)
- Bleu nuit (#1A4A6A)
- Or (#D4AF37)
- Rouge terre (#A0522D)

---

## Tests avant impression massive

### 1. Impression test

**Avant d'imprimer 30 copies :**
1. Imprimer 1 exemplaire en couleur
2. Imprimer 1 exemplaire en noir et blanc (v\u00e9rifier lisibilit\u00e9)
3. Faire une photocopie (v\u00e9rifier qualit\u00e9 de reproduction)

### 2. V\u00e9rifications visuelles

**Checklist :**
- [ ] Les \u00e9l\u00e9ments sont clairement distincts
- [ ] Le texte (si pr\u00e9sent) est lisible
- [ ] Les contrastes sont suffisants
- [ ] Pas de zones trop sombres/satur\u00e9es
- [ ] Le fond reste blanc (pas de gris)
- [ ] La photocopie N&B reste lisible

### 3. Test de consommation

**Estimation visuelle :**
- Compter le nombre de zones color\u00e9es
- \u00c9valuer la surface couverte (< 20% id\u00e9al)
- V\u00e9rifier l'absence de grands aplats

---

## Param\u00e8tres d'impression recommand\u00e9s

### Pour imprimantes laser

```
Mode : Texte et graphiques
Qualit\u00e9 : Standard (pas besoin de Haute qualit\u00e9)
Couleur : Couleur ou N&B selon document
\u00c9conomie d'encre : Activ\u00e9
Recto-verso : Selon besoin
```

### Pour imprimantes jet d'encre

```
Mode : Brouillon ou Normal
Qualit\u00e9 : Standard
Papier : Ordinaire
\u00c9conomie d'encre : Activ\u00e9
Couleur : Selon document
```

### Astuce universelle

Utiliser le mode "\u00e9conomie d'encre" ou "brouillon" est suffisant pour des line art bien contrast\u00e9s.

---

## Optimisation post-g\u00e9n\u00e9ration

### Si l'image est trop color\u00e9e

**Options :**
1. Reg\u00e9n\u00e9rer avec prompts plus stricts
2. Convertir en niveaux de gris + 1 couleur
3. Augmenter le contraste et r\u00e9duire les couleurs

### Si le fond n'est pas blanc

**Solutions :**
1. Utiliser un outil pour remplacer le fond
2. Reg\u00e9n\u00e9rer en insistant sur "white background"
3. Ajuster les niveaux pour \u00e9claircir

### Si trop de d\u00e9tails

**Solutions :**
1. Simplifier via post-traitement
2. Reg\u00e9n\u00e9rer avec style plus minimaliste
3. Vectoriser et simplifier les traces

---

## Co\u00fbts comparatifs

### Exemple concret (fiche A4)

**Fiche tout en couleur (non optimis\u00e9e) :**
- Cyan : 15% → 0.15 page
- Magenta : 15% → 0.15 page
- Yellow : 15% → 0.15 page
- Black : 30% → 0.30 page
- **Total : ~0.75 page d'\u00e9quivalent encre**

**Fiche optimis\u00e9e (2 couleurs, line art) :**
- Cyan : 3% → 0.03 page
- Magenta : 0%
- Yellow : 0%
- Black : 5% → 0.05 page
- **Total : ~0.08 page d'\u00e9quivalent encre**

**\u00c9conomie : ~90% d'encre**

### Sur une ann\u00e9e scolaire

**Hypoth\u00e8se :** 30 \u00e9l\u00e8ves, 100 fiches/an

**Non optimis\u00e9 :**
- 3000 impressions × 0.75 = 2250 pages \u00e9quivalent encre

**Optimis\u00e9 :**
- 3000 impressions × 0.08 = 240 pages \u00e9quivalent encre

**\u00c9conomie : ~2000 pages d'\u00e9quivalent encre**
(soit environ 10-15 cartouches selon mod\u00e8le)

---

## Exemples avant/apr\u00e8s

### Exemple 1 : Porte myst\u00e9rieuse

**❌ Non optimis\u00e9 :**
```
A highly detailed wooden door with intricate carvings,
realistic textures, dark atmospheric background,
photorealistic style
```
→ Co\u00fbt : \u00c9lev\u00e9 (nombreuses couleurs, fond sombre)

**✅ Optimis\u00e9 :**
```
A simple wooden door with lock, simple line art,
minimal colors, white background, high contrast
```
→ Co\u00fbt : Tr\u00e8s bas (2 couleurs, fond blanc, line art)

### Exemple 2 : Carte au tr\u00e9sor

**❌ Non optimis\u00e9 :**
```
An aged treasure map with detailed coastlines,
vintage paper texture, sepia tones with gradient,
weathered edges
```
→ Co\u00fbt : Moyen-\u00e9lev\u00e9 (d\u00e9grad\u00e9s, texture de fond)

**✅ Optimis\u00e9 :**
```
A treasure map with marked path and X location,
simple line art, brown and black only,
white background, clean lines
```
→ Co\u00fbt : Bas (2 couleurs, pas de texture, fond blanc)

---

## R\u00e8gle d'or

> **Pour chaque image, se demander :**
> "Si je devais imprimer 100 copies, quel serait le co\u00fbt ?"
>
> Si la r\u00e9ponse est "trop cher", simplifier le style.

---

## Checklist finale avant impression

- [ ] Fond blanc ou tr\u00e8s clair
- [ ] 3 couleurs maximum (id\u00e9alement 2)
- [ ] Style line art ou flat design
- [ ] Pas de d\u00e9grad\u00e9s
- [ ] Pas de grandes zones color\u00e9es
- [ ] Contraste \u00e9lev\u00e9
- [ ] Test d'impression effectu\u00e9
- [ ] Photocopie N&B lisible
- [ ] R\u00e9solution ad\u00e9quate (300+ DPI)
- [ ] Format de fichier appropri\u00e9

Si tous les crit\u00e8res sont remplis : **pr\u00eat pour impression en masse !**
