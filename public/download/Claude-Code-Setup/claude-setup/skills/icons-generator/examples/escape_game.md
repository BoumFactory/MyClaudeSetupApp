# Exemple : Escape Game M\u00e9di\u00e9val pour Fiche d'Exercices

## Contexte

- **Type de document** : Fiche d'exercices de math\u00e9matiques (fractions)
- **Niveau** : 4\u00e8me
- **Nombre d'\u00e9l\u00e8ves** : 30
- **Usage** : Impression quotidienne (30 copies)
- **Contrainte** : Budget encre limit\u00e9

## Objectif

Cr\u00e9er un enrobage ludique sous forme d'escape game m\u00e9di\u00e9val pour 5 exercices sur les fractions.

---

## \u00c9tape 1 : Cahier des charges

### Images n\u00e9cessaires

1. **Porte du donjon** - Introduction de l'escape game
2. **Coffre avec cadenas** - Exercice 1 (addition de fractions)
3. **Carte au tr\u00e9sor** - Exercice 2 (soustraction de fractions)
4. **\u00c9nigme avec symboles** - Exercice 3 (multiplication de fractions)
5. **Couronne royale** - R\u00e9compense finale (division de fractions)

### Contraintes

- **Style** : minimal_color_print (impression \u00e9conomique)
- **Th\u00e8me** : escape_game_medieval
- **Couleurs** : 2-3 maximum (noir + brun + \u00e9ventuellement bleu)
- **Fond** : Blanc obligatoire
- **Coh\u00e9rence** : Tous les \u00e9l\u00e9ments doivent \u00e9voquer le m\u00eame univers m\u00e9di\u00e9val

---

## \u00c9tape 2 : G\u00e9n\u00e9ration des prompts

### Commande

```bash
python .claude/skills/image-generator/scripts/generate_prompt.py \
  --config .claude/skills/image-generator/config/escape_game_medieval.json \
  --output "prompts/escape_fractions_4eme.json" \
  --num_images 5 \
  --contexts "A heavy wooden door with iron lock and mysterious symbols,An ancient treasure chest with ornate lock,An old parchment map with marked locations and compass rose,A puzzle with geometric symbols and mysterious runes,A golden crown with jewels"
```

### R\u00e9sultat

Fichier `prompts/escape_fractions_4eme.json` cr\u00e9\u00e9 avec 5 prompts optimis\u00e9s :

```json
{
  "metadata": {
    "style": "minimal_color_print",
    "theme": "escape_game_medieval",
    "num_images": 5
  },
  "prompts": [
    {
      "id": 1,
      "context": "A heavy wooden door with iron lock and mysterious symbols",
      "prompt": "A heavy wooden door with iron lock and mysterious symbols, medieval theme, mysterious atmosphere, medieval elements, simple line art, minimal colors (2-3 colors max), high contrast, clean lines, white background, suitable for economical printing",
      "negative_prompt": "gradient, photorealistic, detailed textures, many colors, dark background, shadows",
      "max_colors": 3
    },
    ...
  ]
}
```

---

## \u00c9tape 3 : G\u00e9n\u00e9ration des images

### Commande

```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  --prompt_file "prompts/escape_fractions_4eme.json" \
  --output_dir "images/escape_fractions_4eme" \
  --num_variations 3
```

### Sortie attendue

```
============================================================
G\u00c9N\u00c9RATION D'IMAGES
============================================================
Fichier de prompts : prompts/escape_fractions_4eme.json
R\u00e9pertoire de sortie : images/escape_fractions_4eme
Nombre d'images : 5
Variations par image : 3
Style : minimal_color_print
Th\u00e8me : escape_game_medieval
============================================================

Image 1: A heavy wooden door with iron lock and mysterious symbols

  Variation 1/3
  G\u00e9n\u00e9ration en cours...
  \u2713 Image g\u00e9n\u00e9r\u00e9e avec succ\u00e8s
  \u2713 Sauvegard\u00e9e : image_001_var_1.png

  Variation 2/3
  G\u00e9n\u00e9ration en cours...
  \u2713 Image g\u00e9n\u00e9r\u00e9e avec succ\u00e8s
  \u2713 Sauvegard\u00e9e : image_001_var_2.png

  ...

============================================================
R\u00c9SUM\u00c9
============================================================
Images g\u00e9n\u00e9r\u00e9es avec succ\u00e8s : 5/5
Fichiers cr\u00e9\u00e9s : 15
R\u00e9pertoire : images/escape_fractions_4eme
============================================================
```

### Fichiers g\u00e9n\u00e9r\u00e9s

```
images/escape_fractions_4eme/
\u251c\u2500\u2500 image_001_var_1.png
\u251c\u2500\u2500 image_001_var_2.png
\u251c\u2500\u2500 image_001_var_3.png
\u251c\u2500\u2500 image_002_var_1.png
\u251c\u2500\u2500 image_002_var_2.png
\u251c\u2500\u2500 image_002_var_3.png
\u251c\u2500\u2500 ...
\u2514\u2500\u2500 generation_metadata.json
```

---

## \u00c9tape 4 : Comparaison et s\u00e9lection

### Commande

```bash
python .claude/skills/image-generator/scripts/compare_select.py \
  --input_dir "images/escape_fractions_4eme" \
  --selection_criteria "printability,clarity,simplicity"
```

### Sortie interactive

```
============================================================
COMPARAISON ET S\u00c9LECTION D'IMAGES
============================================================
R\u00e9pertoire : images/escape_fractions_4eme
Crit\u00e8res : printability, clarity, simplicity
Mode : Interactif
============================================================

Trouv\u00e9 5 groupe(s) d'images

============================================================
Image 1 - 3 variation(s)
============================================================

  Variation 1: image_001_var_1.png
    Score: 0.872
    Couleurs uniques: 1245
    Fond blanc: 92.3%
    Contraste: 78.5

  Variation 2: image_001_var_2.png
    Score: 0.845
    Couleurs uniques: 1389
    Fond blanc: 91.1%
    Contraste: 75.2

  Variation 3: image_001_var_3.png
    Score: 0.891
    Couleurs uniques: 1102
    Fond blanc: 93.7%
    Contraste: 81.3

  Recommandation: Variation 3 (meilleur score)

  Options:
    1-3: Choisir une variation sp\u00e9cifique
    A: Accepter la recommandation
    K: Garder toutes les variations

  Votre choix pour l'image 1: A

  ...
```

### R\u00e9sultat final

Apr\u00e8s s\u00e9lection et nettoyage :

```
images/escape_fractions_4eme/
\u251c\u2500\u2500 image_001.png  (anciennement image_001_var_3.png)
\u251c\u2500\u2500 image_002.png
\u251c\u2500\u2500 image_003.png
\u251c\u2500\u2500 image_004.png
\u251c\u2500\u2500 image_005.png
\u2514\u2500\u2500 generation_metadata.json
```

---

## \u00c9tape 5 : Int\u00e9gration dans le document LaTeX

### Structure du document

```latex
\documentclass{article}
\usepackage{graphicx}
\usepackage{bfcours}

\begin{document}

\section*{Mission : \u00c9chapper du Donjon Maudit}

\begin{center}
\includegraphics[width=0.3\textwidth]{images/escape_fractions_4eme/image_001.png}
\end{center}

Vous \u00eates enferm\u00e9s dans un donjon m\u00e9di\u00e9val. Pour vous \u00e9chapper,
vous devez r\u00e9soudre 4 \u00e9nigmes math\u00e9matiques...

\subsection*{\u00c9nigme 1 : Le Coffre Myst\u00e9rieux}

\begin{center}
\includegraphics[width=0.25\textwidth]{images/escape_fractions_4eme/image_002.png}
\end{center}

Pour ouvrir ce coffre, calculez...

[Exercice sur addition de fractions]

\subsection*{\u00c9nigme 2 : La Carte au Tr\u00e9sor}

\begin{center}
\includegraphics[width=0.25\textwidth]{images/escape_fractions_4eme/image_003.png}
\end{center}

D\u00e9chiffrez la carte en r\u00e9solvant...

[Exercice sur soustraction de fractions]

% etc...

\section*{F\u00e9licitations !}

\begin{center}
\includegraphics[width=0.2\textwidth]{images/escape_fractions_4eme/image_005.png}
\end{center}

Vous avez r\u00e9ussi \u00e0 vous \u00e9chapper ! Vous \u00eates couronn\u00e9s Champions des Fractions !

\end{document}
```

---

## Estimation des co\u00fbts

### Par copie

- **Nombre d'images** : 5
- **Style** : minimal_color_print
- **Couleurs moyennes par image** : 2-3
- **Co\u00fbt estim\u00e9 par image** : ~0.08 page d'\u00e9quivalent encre
- **Co\u00fbt total par copie** : ~0.40 page d'\u00e9quivalent encre

### Pour 30 copies

- **Total** : ~12 pages d'\u00e9quivalent encre
- **Compar\u00e9 \u00e0 version non optimis\u00e9e** : \u00c9conomie de ~85%

### Co\u00fbt si non optimis\u00e9

Si les m\u00eames images \u00e9taient g\u00e9n\u00e9r\u00e9es en style `moderate_color_classroom` :
- **Co\u00fbt par copie** : ~1.50 page d'\u00e9quivalent encre
- **Total pour 30 copies** : ~45 pages
- **Diff\u00e9rence** : 33 pages \u00e9conomis\u00e9es !

---

## R\u00e9sultats p\u00e9dagogiques

### Engagement des \u00e9l\u00e8ves

- Th\u00e9matisation attractive
- Histoire coh\u00e9rente
- Motivation accrue

### Co\u00fbt ma\u00eetris\u00e9

- Impression \u00e9conomique
- Qualit\u00e9 pr\u00e9serv\u00e9e
- Photocopie possible

### Temps de cr\u00e9ation

- G\u00e9n\u00e9ration des prompts : 2 minutes
- G\u00e9n\u00e9ration des images : 15 minutes
- S\u00e9lection : 5 minutes
- Int\u00e9gration LaTeX : 10 minutes
- **Total : ~30 minutes**

Compar\u00e9 \u00e0 la cr\u00e9ation manuelle ou recherche d'images libres de droits : **gain de temps consid\u00e9rable**.

---

## Conseils pour r\u00e9ussir

### 1. Pr\u00e9parer le cahier des charges

Avant de g\u00e9n\u00e9rer, d\u00e9finir clairement :
- Nombre exact d'images
- R\u00f4le de chaque image
- Coh\u00e9rence narrative

### 2. \u00catre pr\u00e9cis dans les contextes

Meilleur :
```
"A heavy wooden door with iron lock and mysterious symbols"
```

Moins bon :
```
"door"
```

### 3. Utiliser les configurations pr\u00e9-d\u00e9finies

Ne pas h\u00e9siter \u00e0 utiliser `--config` pour gagner du temps et assurer la coh\u00e9rence.

### 4. G\u00e9n\u00e9rer plusieurs variations

Toujours g\u00e9n\u00e9rer 2-3 variations pour avoir le choix. La diff\u00e9rence de qualit\u00e9 peut \u00eatre significative.

### 5. Valider avant impression massive

Toujours imprimer 1 exemplaire de test avant de lancer 30 copies.

---

## Conclusion

Cet exemple montre comment :
- Cr\u00e9er rapidement des images th\u00e9matis\u00e9es coh\u00e9rentes
- Optimiser pour l'impression \u00e9conomique
- Maintenir la qualit\u00e9 p\u00e9dagogique
- Gagner du temps

Le m\u00eame processus peut \u00eatre appliqu\u00e9 \u00e0 d'autres th\u00e8mes :
- Escape game science-fiction
- Enqu\u00eate polici\u00e8re
- Aventure historique
- Exploration g\u00e9ographique
- Etc.
