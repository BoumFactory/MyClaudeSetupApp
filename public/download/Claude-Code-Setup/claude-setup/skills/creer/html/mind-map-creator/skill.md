---
name: mind-map-creator
description: >
  Skill pour créer des cartes mentales (mind maps) éducatives au format Markdown
  compatible avec markdown-map.com. Ce skill devrait être utilisé pour générer
  des synthèses visuelles de chapitres, visualiser les relations entre concepts
  mathématiques, créer des supports de révision, ou structurer hiérarchiquement
  un thème pédagogique. Génère un fichier .md, ouvre le navigateur sur le site,
  et guide l'utilisateur pour le copier-coller.
---

# Mind Map Creator

Skill spécialisé dans la création de cartes mentales éducatives au format Markdown compatible avec [markdown-map.com/v1/](https://markdown-map.com/v1/).

## Cas d'utilisation

- Synthétiser un chapitre en une carte visuelle
- Visualiser les relations entre concepts mathématiques
- Créer des supports de révision pour les élèves
- Structurer hiérarchiquement un thème pédagogique
- Préparer une vue d'ensemble avant un cours

## Syntaxe Markdown pour Mind Maps

### Structure hiérarchique

```markdown
# Concept Central
## Branche 1
- Sous-élément 1.1
- Sous-élément 1.2
## Branche 2
### Sous-branche 2.1
- Détail A
- Détail B :
  - Sous-détail a
  - Sous-détail b
### Sous-branche 2.2
## Branche 3
```

### Correspondance des niveaux

| Syntaxe | Rôle | Quantité idéale |
|---------|------|-----------------|
| `#` | Noeud central (thème) | 1 seul |
| `##` | Branches principales | 3-6 |
| `###` | Sous-branches | 2-4 par branche |
| `-` | Feuilles/détails | 2-5 par niveau |

### Utilisation des emojis

Les emojis améliorent la lisibilité et permettent d'identifier rapidement les catégories.

| Catégorie | Emojis recommandés |
|-----------|-------------------|
| Définition | `📋` `📖` `📝` |
| Formule | `🧮` `🔢` `➗` |
| Méthode | `✅` `🔄` `📊` |
| Exemple | `💡` `🔍` `📌` |
| Attention | `⚠️` `❌` `🚫` |
| Géométrie | `📐` `📏` `🔺` |
| Graphique | `📈` `📉` `📊` |
| Objectif | `🎯` `🏆` `⭐` |

## Protocole d'exécution

### 1. Analyser la demande

Identifier :
- **Thème** : Sujet de la carte mentale
- **Niveau** : Collège (6e-3e) ou Lycée (2nde-Term)
- **Source** : Fichier à analyser (optionnel)
- **Profondeur** : Synthèse rapide ou détaillée

### 2. Collecter le contenu

**Avec source fournie** :
1. Lire le fichier source (cours, exercices)
2. Identifier les sections principales (branches `##`)
3. Extraire les sous-sections (sous-branches `###`)
4. Lister les points clés (feuilles `-`)

**Sans source** :
1. Structurer selon le programme officiel du niveau
2. Organiser en 3-6 branches équilibrées
3. Adapter le vocabulaire au niveau scolaire

### 3. Générer le Markdown

Construire le fichier en respectant :
- Un seul `#` pour le noeud central
- Des `##` pour les branches principales (3-6)
- Des `###` pour les sous-branches si nécessaire
- Des `-` pour les détails/feuilles
- Des emojis cohérents par catégorie

**Structure type** :
```markdown
# 🎯 [Thème Central]
## 📋 Définitions
- Point clé 1
- Point clé 2
## 🧮 Formules
### Formule principale
- Expression
- Conditions d'application
### Formules dérivées
## 💡 Applications
- Exemple 1
- Exemple 2
## ⚠️ Pièges à éviter
- Erreur courante 1
- Erreur courante 2
```

### 4. Sauvegarder le fichier

Déterminer l'emplacement approprié :
- **Lié à un cours** : `1. Cours/[niveau]/Sequence-[theme]/mindmap/mindmap_[theme].md`
- **Standalone** : Utiliser le répertoire donné ou demander la destination

Créer le dossier si nécessaire avec `mkdir -p`.

### 5. Ouvrir le navigateur

Exécuter la commande pour ouvrir markdown-map.com :

```bash
start https://markdown-map.com/v1/
```

### 6. Afficher les instructions

Présenter le résultat avec ce format :

```
## Carte mentale créée

**Fichier** : `[chemin complet]`

**Contenu à copier** :

\`\`\`markdown
[contenu de la carte]
\`\`\`

---

**Instructions** :
1. Le site markdown-map.com s'ouvre dans votre navigateur
2. Sélectionnez le contenu Markdown ci-dessus
3. Collez-le dans l'éditeur de gauche (Ctrl+V)
4. La carte apparaît instantanément à droite
5. Personnalisez les couleurs si souhaité
6. Téléchargez en HD ou FHD
```

## Exemples de référence

Pour des exemples complets de cartes mentales par niveau et par thème, consulter `references/examples.md`.

## Notation mathématique (UNICODE OBLIGATOIRE)

**IMPORTANT** : markdown-map.com ne supporte PAS LaTeX/KaTeX/MathJax. Utiliser EXCLUSIVEMENT les caractères Unicode.

### Exposants Unicode

| Chiffre | Unicode | Usage |
|---------|---------|-------|
| ⁰ | `⁰` | x⁰ = 1 |
| ¹ | `¹` | x¹ = x |
| ² | `²` | x², a² + b² = c² |
| ³ | `³` | x³, fonction cube |
| ⁴ | `⁴` | x⁴ |
| ⁵ | `⁵` | x⁵ |
| ⁶ | `⁶` | x⁶ |
| ⁷ | `⁷` | x⁷ |
| ⁸ | `⁸` | x⁸ |
| ⁹ | `⁹` | x⁹ |
| ⁿ | `ⁿ` | 2ⁿ, 10ⁿ, xⁿ |
| ⁺ | `⁺` | exposant positif |
| ⁻ | `⁻` | x⁻¹ = 1/x |
| ⁽⁾ | `⁽⁾` | groupes en exposant |

### Indices Unicode

| Chiffre | Unicode | Usage |
|---------|---------|-------|
| ₀ | `₀` | u₀, a₀ |
| ₁ | `₁` | u₁, x₁ |
| ₂ | `₂` | u₂, x₂ |
| ₃ | `₃` | u₃ |
| ₄ | `₄` | u₄ |
| ₅ | `₅` | u₅ |
| ₆ | `₆` | u₆ |
| ₇ | `₇` | u₇ |
| ₈ | `₈` | u₈ |
| ₉ | `₉` | u₉ |
| ₙ | `ₙ` | uₙ, xₙ |
| ₊ | `₊` | uₙ₊₁ |
| ₋ | `₋` | uₙ₋₁ |
| ₍₎ | `₍₎` | groupes en indice |

### Symboles mathématiques

| Symbole | Unicode | Signification |
|---------|---------|---------------|
| √ | `√` | racine carrée |
| ∛ | `∛` | racine cubique |
| π | `π` | pi |
| ∞ | `∞` | infini |
| ≈ | `≈` | environ égal |
| ≠ | `≠` | différent |
| ≤ | `≤` | inférieur ou égal |
| ≥ | `≥` | supérieur ou égal |
| × | `×` | multiplication |
| ÷ | `÷` | division |
| ± | `±` | plus ou moins |
| ∓ | `∓` | moins ou plus |
| ∑ | `∑` | somme |
| ∏ | `∏` | produit |
| ∈ | `∈` | appartient à |
| ∉ | `∉` | n'appartient pas |
| ⊂ | `⊂` | inclus dans |
| ⊃ | `⊃` | contient |
| ∩ | `∩` | intersection |
| ∪ | `∪` | réunion |
| ∅ | `∅` | ensemble vide |
| ⇒ | `⇒` | implique |
| ⇔ | `⇔` | équivalent |
| → | `→` | tend vers, fonction |
| ↦ | `↦` | associe (f: x ↦ y) |
| ∀ | `∀` | pour tout |
| ∃ | `∃` | il existe |
| ℕ | `ℕ` | entiers naturels |
| ℤ | `ℤ` | entiers relatifs |
| ℚ | `ℚ` | rationnels |
| ℝ | `ℝ` | réels |
| ℂ | `ℂ` | complexes |

### Lettres grecques courantes

| Lettre | Unicode | Usage |
|--------|---------|-------|
| α | `α` | alpha, angle |
| β | `β` | beta, angle |
| γ | `γ` | gamma |
| δ | `δ` | delta, variation |
| ε | `ε` | epsilon |
| θ | `θ` | theta, angle |
| λ | `λ` | lambda |
| μ | `μ` | mu, moyenne |
| σ | `σ` | sigma, écart-type |
| φ | `φ` | phi |
| ω | `ω` | omega |
| Δ | `Δ` | Delta, discriminant |
| Σ | `Σ` | Sigma, somme |
| Ω | `Ω` | Omega |

### Fractions précomposées

| Fraction | Unicode |
|----------|---------|
| ½ | `½` |
| ⅓ | `⅓` |
| ⅔ | `⅔` |
| ¼ | `¼` |
| ¾ | `¾` |
| ⅕ | `⅕` |
| ⅙ | `⅙` |
| ⅛ | `⅛` |

### Intervalles et crochets

| Symbole | Usage |
|---------|-------|
| [ ] | intervalle fermé [a ; b] |
| ] [ | intervalle ouvert ]a ; b[ |
| [ [ | semi-ouvert [a ; b[ |
| ] ] | semi-ouvert ]a ; b] |
| ]-∞ ; +∞[ | ℝ tout entier |

### Exemples de formules en Unicode

```
INCORRECT (LaTeX) → CORRECT (Unicode)
$x^2$             → x²
$x_n$             → xₙ
$u_{n+1}$         → uₙ₊₁
$\sqrt{2}$        → √2
$\frac{1}{x}$     → 1/x
$a \in \mathbb{R}$→ a ∈ ℝ
$\pi$             → π
$\infty$          → ∞
$x \leq y$        → x ≤ y
$\sum$            → ∑
$A \cup B$        → A ∪ B
$A \cap B$        → A ∩ B
```

## Bonnes pratiques

1. **Équilibre** : Branches de taille comparable (éviter une branche avec 10 items et une avec 1)
2. **Hiérarchie claire** : Du général au particulier
3. **Vocabulaire adapté** : Selon le niveau scolaire
4. **Notation Unicode** : JAMAIS de LaTeX (`$...$`), toujours Unicode (², √, π, ∈, etc.)
5. **Emojis cohérents** : Même emoji pour même catégorie dans toute la carte
6. **Fractions** : Écrire `1/x` ou utiliser les fractions précomposées (½, ⅓, etc.)
