# Guide de prompting pour images \u00e9ducatives

Bonnes pratiques pour cr\u00e9er des prompts efficaces g\u00e9n\u00e9rant des images adapt\u00e9es aux besoins p\u00e9dagogiques.

## Principes fondamentaux

### 1. \u00catre sp\u00e9cifique mais concis

**Bon exemple :**
```
A medieval castle gate with iron lock, simple line art,
minimal colors, high contrast
```

**Mauvais exemple :**
```
castle
```
→ Trop vague

**Mauvais exemple :**
```
A very detailed and intricate medieval castle with numerous
towers, battlements, a complex moat system, various flags,
guards, horses, and a marketplace nearby
```
→ Trop complexe pour un style minimaliste

### 2. Adapter le niveau de d\u00e9tail au style

**Pour minimal_color_print :**
- Description simple et directe
- Focalisez sur 1-2 \u00e9l\u00e9ments principaux
- \u00c9vitez les adjectifs de texture

**Pour moderate_color_classroom :**
- D\u00e9tails moyens accept\u00e9s
- Mentions de couleurs possibles
- Contexte enrichi

**Pour educational_illustration :**
- Pr\u00e9ciser les \u00e9l\u00e9ments techniques
- Mentionner les labels/annotations si n\u00e9cessaires

---

## Structure d'un bon prompt

### Format recommand\u00e9

```
[SUJET PRINCIPAL] + [CONTEXTE] + [STYLE] + [CONTRAINTES TECHNIQUES]
```

### Exemple d\u00e9taill\u00e9

**SUJET** : A treasure map
**CONTEXTE** : with marked path and X location
**STYLE** : simple line art, minimal colors
**CONTRAINTES** : white background, suitable for printing

**Prompt final :**
```
A treasure map with marked path and X location, simple line art,
minimal colors, white background, suitable for printing
```

---

## Techniques avanc\u00e9es

### 1. Utilisation des negative prompts

Les negative prompts indiquent ce qu'il faut \u00c9VITER.

**Pour impression \u00e9conomique :**
```
negative_prompt: "gradient, photorealistic, detailed textures,
many colors, dark background, shadows"
```

**Pour clart\u00e9 p\u00e9dagogique :**
```
negative_prompt: "abstract, artistic, decorative, complex,
confusing elements"
```

### 2. Mots-cl\u00e9s de style graphique

Ces mots influencent fortement le rendu :

**Style \u00e9pur\u00e9 :**
- "line art"
- "flat design"
- "vector style"
- "clean lines"
- "simple illustration"

**Style didactique :**
- "diagram"
- "schematic"
- "instructional"
- "educational"
- "clear and readable"

**Style accessible :**
- "friendly"
- "approachable"
- "fun"
- "engaging"

### 3. Gestion des couleurs

**Pour limiter les couleurs :**
- Sp\u00e9cifier explicitement : "2-3 colors max"
- Nommer les couleurs : "blue and orange only"
- Demander un style : "monochromatic with accent color"

**Pour optimiser l'impression :**
- "white background"
- "high contrast"
- "bold colors" (pas de pastels)

---

## Prompts par contexte \u00e9ducatif

### Escape game m\u00e9di\u00e9val

**Porte myst\u00e9rieuse :**
```
A heavy wooden door with iron lock and mysterious symbols,
medieval theme, simple line art, minimal colors,
white background, suitable for printing
```

**Coffre au tr\u00e9sor :**
```
An ancient treasure chest slightly open with golden glow,
medieval theme, colorful illustration, 4-5 vibrant colors,
engaging and fun, educational style
```

**Carte ancienne :**
```
An old parchment map with marked locations and compass rose,
medieval theme, simple line art, sepia and brown tones,
white background, high contrast
```

### Math\u00e9matiques

**G\u00e9om\u00e9trie :**
```
Geometric shapes showing theorem demonstration,
clean educational diagram, didactic style, minimal colors,
clear labels possible, white background
```

**Fonctions :**
```
Coordinate system with function curve and key points,
educational diagram, simple line art, blue and black,
instructional design, maximum clarity
```

### Sciences

**Physique :**
```
Laboratory equipment setup for experiment,
flat design, geometric shapes, 3-4 colors,
simple composition, educational style
```

**Biologie :**
```
Plant cell diagram with labeled organelles,
educational illustration, didactic style,
clear and simple, suitable for students
```

---

## Erreurs fr\u00e9quentes \u00e0 \u00e9viter

### \u274c Demander un style r\u00e9aliste pour impression \u00e9conomique

**Mauvais :**
```
A photorealistic castle with detailed stones and textures
```
→ Co\u00fbteux en encre, complexe

**Bon :**
```
A castle silhouette, simple line art, minimal details
```

### \u274c Oublier le fond

**Mauvais :**
```
A mysterious door, simple style
```
→ Risque de fond color\u00e9 ou sombre

**Bon :**
```
A mysterious door, simple style, white background
```

### \u274c Trop de d\u00e9tails pour un style minimaliste

**Mauvais :**
```
A complex scene with multiple characters, objects, and backgrounds,
simple line art
```
→ Contradiction entre complexit\u00e9 et style simple

**Bon :**
```
A single character with one key object, simple line art
```

### \u274c Ne pas sp\u00e9cifier le contexte \u00e9ducatif

**Mauvais :**
```
A cool dragon
```
→ Peut g\u00e9n\u00e9rer quelque chose d'inappropri\u00e9

**Bon :**
```
A friendly dragon character for math story problem,
simple cartoon style, suitable for young students
```

---

## Checklist avant g\u00e9n\u00e9ration

Avant de lancer la g\u00e9n\u00e9ration, v\u00e9rifier que vos prompts :

- [ ] D\u00e9crivent clairement le sujet principal
- [ ] Sp\u00e9cifient le style graphique
- [ ] Incluent "white background" (sauf exception)
- [ ] Mentionnent "suitable for printing" si n\u00e9cessaire
- [ ] Limitent explicitement les couleurs si besoin
- [ ] Sont adapt\u00e9s au public cible (\u00e2ge des \u00e9l\u00e8ves)
- [ ] Sont coh\u00e9rents avec le th\u00e8me global
- [ ] Ont un negative prompt appropri\u00e9
- [ ] Sont suffisamment simples pour le style choisi
- [ ] Respectent les contraintes d'impression

---

## Templates r\u00e9utilisables

### Template minimal_color_print
```
[SUJET], [TH\u00c8ME] theme, simple line art, minimal colors (2-3 max),
high contrast, clean lines, white background, suitable for economical printing
```

### Template moderate_color_classroom
```
[SUJET], [TH\u00c8ME] theme, colorful illustration, 4-6 vibrant colors,
medium detail, engaging and fun, educational style, clear and readable
```

### Template educational_illustration
```
[SUJET], clean educational diagram, didactic style, clear labels possible,
maximum clarity, instructional design, simple and understandable
```

### Template flat_design
```
[SUJET], flat design, geometric shapes, simple composition,
bold colors, modern minimalist style
```

### Template cartoon_simple
```
[SUJET], simple cartoon style, friendly characters, basic shapes,
approachable and fun, suitable for young students
```

---

## Exemples complets par niveau

### Coll\u00e8ge (11-15 ans)

**Style recommand\u00e9 :** cartoon_simple ou moderate_color_classroom

```
A student solving a puzzle with mathematical symbols,
simple cartoon style, friendly character, 4-5 colors,
fun and engaging, suitable for middle school students
```

### Lyc\u00e9e (15-18 ans)

**Style recommand\u00e9 :** educational_illustration ou flat_design

```
Scientific experiment setup showing chemical reaction,
flat design, geometric shapes, 3-4 colors,
modern minimalist style, educational context
```

### Universit\u00e9/Adultes

**Style recommand\u00e9 :** educational_illustration

```
Complex mathematical concept visualization,
clean educational diagram, didactic style,
maximum clarity, academic illustration, minimal colors
```
