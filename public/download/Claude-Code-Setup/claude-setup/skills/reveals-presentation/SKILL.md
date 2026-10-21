---
name: reveals-presentation
description: Skill spécialisé pour la création de présentations reveal.js interactives et stylées pour l'enseignement. Gère la mise en page, l'espacement, les animations, les exercices avec estimation de temps. Trois styles disponibles - collège, lycée, académique. Utiliser pour créer des présentations web professionnelles adaptées au contexte éducatif.
---

# Reveal.js Presentation Expert

Système expert pour la création de présentations reveal.js interactives et stylées de haute qualité avec gestion précise de l'espacement, animations progressives et styles contextuels.

## Objectif

Créer des présentations web professionnelles et interactives, parfaitement adaptées au contexte (classe collège, classe lycée, présentation académique) avec une attention particulière à la densité d'information par slide et à la progressivité pédagogique.

## ⚠️ RÈGLE ABSOLUE : Utilisation stricte des templates

**IMPORTANT** : L'agent NE DOIT JAMAIS modifier le CSS ou le design global.

### Workflow obligatoire
1. **Charger le template** depuis `assets/templates/template-lycee.html` (ou `template-college.html`, `template-academique.html`), dossier du skill. Copier le fichier dans le dossier de travail avant de le remplir.

2. **Conserver INTÉGRALEMENT** :
   - Le `<head>` complet (CDN, MathJax, CSS)
   - Tout le `<style>` (ne JAMAIS le modifier)
   - La structure `<script>` et configuration Reveal.js
3. **Remplir UNIQUEMENT** le contenu entre `<div class="slides">` et `</div>`
4. **Utiliser les classes CSS prédéfinies** sans en créer de nouvelles

### Classes CSS disponibles dans le template

Les classes sont **prédéfinies** et doivent être utilisées telles quelles, sans en créer de nouvelles. Liste complète (boîtes, exercices, questions/réponses, mise en forme, classes propres au style académique) : `references/classes-css.md`. Les trois gabarits (`template-college.html`, `template-lycee.html`, `template-academique.html`) partagent les mêmes classes ; le style académique ajoute `.theorem`, `.definition`, `.proof`, `.reference`, `.citation`, `.emphasis`, `.bibliography`.

Points à retenir :
- Boîtes : `.box-info`, `.box-warning`, `.box-success`, `.box-error`, `.result-box`, `.formula-box`.
- Exercices : `.exercise`, `.exercise-header`, `.difficulty`, `.estimated-time`, `.statement`, `.questions-overview`, `.question-header`, `.question-number`, `.question-time`, `.question-recall`, `.resolution`.
- `.nav-hint` (indication de navigation) est positionné en `absolute` en bas de la diapositive ; le CSS des templates réserve un `padding-bottom` : ne pas ajouter d'espaceur manuel avant.
- Le style académique n'a pas vocation à contenir des `.exercise`/`.question` : il s'appuie sur théorèmes, définitions et démonstrations.

### Exemples de présentations

**Consulter ces exemples** pour comprendre l'utilisation correcte du template :

- `assets/presentation_cours.html` : exemple de cours complet
- `assets/presentation_exos.html` : exemple d'exercices complets

Ces fichiers montrent comment utiliser les classes CSS prédéfinies sans jamais modifier le design.

### Ce que l'agent DOIT faire

✅ Lire le template approprié (collège/lycée/académique)
✅ Remplir uniquement le contenu des slides
✅ Utiliser les classes CSS prédéfinies
✅ Structurer le contenu avec les balises HTML standards
✅ Intégrer MathJax avec les délimiteurs `\(...\)` et `\[...\]`
✅ Ajouter des fragments (`class="fragment"`) pour progressivité
✅ Respecter la structure 2D pour navigation (si approprié)

### Ce que l'agent NE DOIT JAMAIS faire

❌ Modifier le CSS existant
❌ Ajouter de nouveaux styles
❌ Changer les couleurs ou polices
❌ Modifier la configuration Reveal.js
❌ Créer de nouvelles classes CSS
❌ Supprimer ou renommer des classes existantes

## Guides de référence

Tous les chemins sont relatifs au dossier du skill. **LIRE IMPÉRATIVEMENT** les guides prioritaires avant de créer une présentation.

### Guides prioritaires selon le contexte

**Pour COURS** :
- `references/interactive-pedagogy.md` : **PRIORITÉ ABSOLUE** - Structure en 4 niveaux (Question → Réponse → Remarques → FAQ)
- `references/navigation-2d.md` : **TRÈS IMPORTANT** - Navigation multidirectionnelle 2D

**Pour EXERCICES** :
- `references/exercices-structure.md` : **PRIORITÉ ABSOLUE** - Structure spécifique exercices (1 slide par question)
- `references/workflow-exercices.md` : pattern complet d'un exercice de géométrie avec figures (énoncé, une slide par question, figure finale), layout deux colonnes, `\boxed{}`
- `references/navigation-2d.md` : **TRÈS IMPORTANT** - Navigation multidirectionnelle 2D

### Guides techniques communs

- `references/fragments-reveals.md` : **IMPORTANT** - Fragments pour révélation progressive
- `references/mathjax-integration.md` : **ESSENTIEL** - Intégration des formules mathématiques (et ses limites : voir la section formules barrées)

### Références ponctuelles (à lire quand le besoin se présente)

- `references/classes-css.md` : classes CSS prédéfinies, styles par contexte, classes de fragments
- `references/gabarits-slides.md` : squelette HTML, slide de titre, slide de contenu avec fragments, slide d'exercice avec formules
- `references/configuration-reveal.md` : configuration reveal.js des templates, transitions, raccourcis clavier, speaker notes, marges et espacement
- `references/scripts.md` : scripts `extract_tikz_figures.py`, `convert_pdf_to_png.py`, `embed_images_base64.py` (figures TikZ, PDF vers PNG, HTML autonome)

## Principes Fondamentaux

### 1. Règle d'or : L'espace est votre allié

**JAMAIS plus de 70% de la slide remplie**

Une slide surchargée = une slide illisible. L'espace vide permet :
- La respiration visuelle
- La focalisation de l'attention
- La mémorisation efficace
- La lisibilité depuis le fond de la classe

### 2. Progressivité pédagogique avec fragments

**RÈGLE ABSOLUE** : Utiliser les fragments pour révélation progressive

Classes de fragments à utiliser :
- `class="fragment"` : Apparition au clic
- `class="fragment fade-in"` : Apparition en fondu
- `class="fragment fade-out"` : Disparition en fondu
- `class="fragment highlight-red"` : Mise en évidence rouge
- `data-fragment-index="1"` : Contrôle de l'ordre d'apparition

**Contrôle précis** : Savoir exactement ce qui s'affiche à chaque clic

### 2bis. Navigation 2D (multidirectionnelle)

**NOUVELLE POSSIBILITÉ** : Structurer la présentation en 2 dimensions !

- **Axe horizontal (← →)** : Progression principale du cours
- **Axe vertical (↑ ↓)** : Détails, approfondissements, explications complémentaires

**Quand utiliser la navigation 2D ?**
- Pour offrir des niveaux de détail optionnels
- Pour permettre différents parcours de lecture
- Pour ajouter des démonstrations étape par étape sans alourdir le flux principal
- Pour créer des exercices avec indices progressifs

**Lire impérativement** : `references/navigation-2d.md`

### 3. Adaptation au contexte

Chaque style (collège, lycée, académique) a ses propres contraintes :
- **Collège** : Police grande, couleurs vives, animations fréquentes
- **Lycée** : Équilibre entre rigueur et accessibilité
- **Académique** : Sobriété, densité maîtrisée, références

## Gabarits de slides

Squelette HTML de base, citations et mise en forme, slide de titre, slide de contenu avec fragments, slide d'exercice avec formules : `references/gabarits-slides.md`. Les templates fournis contiennent déjà ce squelette.

## Workflow de création d'une présentation

### Étape 1 : Analyse du contexte

Identifier :
1. **Public cible** : Collège (6e-3e), Lycée (2nde-Tale), Académique (conférence)
2. **Durée prévue** : Adapter le nombre de slides (1 slide ≈ 2-3 minutes)
3. **Niveau de détail** : Introduction, approfondissement, synthèse
4. **Interactivité** : Exercices, questions, activités

### Étape 2 : Choix du template

Utiliser le template approprié dans `assets/templates/` (dossier du skill) :
- `template-college.html` : Police 22px, couleurs vives, animations nombreuses
- `template-lycee.html` : Police 20px, style équilibré, rigueur mathématique
- `template-academique.html` : Police 18px, sobriété, références bibliographiques
- `template-navigation-2d-demo.html` : démonstration de la navigation 2D

### Étape 3 : Structure du contenu

**Règle des 5-7 slides par section** :
- 1 slide de titre de section
- 5-6 slides de contenu
- Éviter les sections de 1 seule slide

**Règle du 6-6-6** (pour lycée/académique) :
- Maximum 6 bullets par slide
- Maximum 6 mots par bullet
- Maximum 6 slides de suite sans pause interactive

### Étape 4 : Gestion de l'espace

**RÈGLE FONDAMENTALE : Maximum 2 éléments côte à côte par slide**

**Principe "2 par slide"** :
- **Maximum 2 images** côte à côte par slide (utiliser `.grid-2`)
- **Maximum 2 boxes/cartes** côte à côte par slide
- **Maximum 2 colonnes** de contenu
- Si plus de 2 éléments → créer des slides DOWN supplémentaires

**Application pratique** :
- 4 images à afficher → 2 slides DOWN (2 images par slide)
- 6 avantages à lister → 3 slides DOWN (2 avantages par slide)
- 5 étapes → 2 slides DOWN (2-3 par slide OU grille 2 colonnes)

**Exceptions acceptables** :
- Listes à puces textuelles : jusqu'à 5 points OK si courts
- Workflow steps : jusqu'à 5 OK si en grille 2 colonnes
- Tags/badges : nombreux OK car petits

**En cas de contenu abondant** :
1. **Priorité 1** : Navigation DOWN (slides verticales)
   - Slide principale : vue d'ensemble + hint `↓`
   - Slides DOWN : détails (2 éléments max par slide)
2. **Priorité 2** : Grille 2 colonnes (`.grid-2`)
3. **Priorité 3** : Nouvelle slide horizontale

Exemple complet (4 images en 2 slides DOWN) et réglages d'espacement CSS : `references/configuration-reveal.md`.

### Étape 5 : Animations et fragments

**Révélation progressive des items** :

```html
<ul>
  <li class="fragment">Premier</li>
  <li class="fragment">Deuxième</li>
  <li class="fragment">Troisième</li>
</ul>
```

**Mise en évidence** :

```html
<ul>
  <li>Point normal</li>
  <li class="fragment highlight-red">Point important révélé et surligné</li>
  <li>Point normal</li>
</ul>
```

**Ordre explicite** :

```html
<div class="fragment" data-fragment-index="2">Apparaît en deuxième</div>
<div class="fragment" data-fragment-index="1">Apparaît en premier</div>
```

### Étape 6 : Intégration de MathJax

Délimiteurs : inline `\(formule\)` ou `$formule$` ; bloc `\[formule\]` ou `$$formule$$` ; environnements LaTeX `\begin{align}...\end{align}`. La configuration MathJax est déjà dans les templates (voir `references/mathjax-integration.md` et `references/configuration-reveal.md`).

### Étape 7 : Test et vérification

**Lancer un serveur local** :

```bash
# Python
python -m http.server 8000

# Node.js (si http-server installé)
npx http-server -p 8000

# Puis ouvrir http://localhost:8000/presentation.html
```

**Vérifier** :
- Navigation (flèches, espace)
- Fragments (animations progressives)
- MathJax (formules affichées)
- Responsive (mobile, tablette)
- Mode présentation (touche S)

## Configuration reveal.js, styles et raccourcis

Options de configuration, transitions, styles par défaut collège/lycée/académique, raccourcis clavier et speaker notes sont dans `references/configuration-reveal.md` et `references/classes-css.md`. Ils sont déjà intégrés aux templates : ne pas les modifier.

## Vérifications finales

**Checklist avant finalisation** :

- [ ] Chaque slide < 70% remplie
- [ ] Fragments testés et fonctionnels
- [ ] MathJax affiche correctement toutes les formules
- [ ] Police lisible (≥ 18px)
- [ ] Cohérence des couleurs (thème respecté)
- [ ] Orthographe et mathématiques vérifiées
- [ ] Navigation fluide (pas de slides vides ou cassées)
- [ ] Exercices avec estimations de temps
- [ ] Responsive (testé sur mobile/tablette)
- [ ] Mode présentation fonctionne

## Bonnes pratiques

1. **Une idée = une slide** : Ne pas surcharger
2. **Couleurs cohérentes** : Respecter le thème choisi
3. **Taille de police** : Minimum 18px pour le texte principal
4. **Formules mathématiques** : Utiliser MathJax systématiquement
5. **Images** : Haute résolution, avec alt text
6. **Transitions** : Simples et discrètes
7. **Navigation** : Inclure sommaire pour présentations > 20 slides
8. **Accessibilité** : Contraste suffisant, texte alternatif

## Erreurs fréquentes à éviter

❌ **Slide surchargée** : > 10 lignes de texte
✅ **Slide aérée** : 5-7 points clés maximum

❌ **Police trop petite** : < 18px
✅ **Police adaptée** : 18-22px selon le contexte

❌ **Fragments désordonnés** : Animations illogiques
✅ **Ordre explicite** : `data-fragment-index` pour contrôle précis

❌ **MathJax oublié** : Formules mal affichées
✅ **MathJax intégré** : Toutes les formules avec délimiteurs corrects

❌ **Pas d'estimation** : Exercice sans indication de temps
✅ **Temps estimé** : Permet au professeur de gérer la séance

## Rappels critiques

- **PRIORITÉ ABSOLUE** : Utiliser les fragments pour révélation progressive
- **RÈGLE FONDAMENTALE** : Maximum 2 éléments côte à côte par slide (images, boxes, colonnes)
- **OBLIGATOIRE** : Intégrer MathJax pour toutes les formules mathématiques
- **TOUJOURS** tester dans un navigateur avant finalisation
- **TOUJOURS** vérifier la densité visuelle (< 70% rempli)
- **TOUJOURS** utiliser navigation DOWN si plus de 2 éléments à afficher
- **TOUJOURS** estimer le temps des exercices
- **TOUJOURS** adapter le style au public (collège/lycée/académique)
- **NE JAMAIS** oublier les balises de fermeture HTML
- **NE JAMAIS** mettre plus de 2 images côte à côte sur une même slide
- **NE JAMAIS** mettre plus de 7 items dans une liste
- **NE JAMAIS** utiliser des polices < 18px

## Workflow exercices, fragments et scripts

- Exercices (géométrie avec figures, deux colonnes, `\boxed{}`) : `references/workflow-exercices.md`.
- Classes de fragments : `references/classes-css.md` et `references/fragments-reveals.md`.
- Scripts (figures TikZ en PNG, PDF en PNG, images en base64 pour un HTML autonome) : `references/scripts.md`. `embed_images_base64.py` s'utilise UNIQUEMENT une fois toutes les modifications terminées.

---

**Ce skill fait de vous un expert reveal.js** capable de créer des présentations web interactives, élégantes et pédagogiques pour tous les publics éducatifs.
