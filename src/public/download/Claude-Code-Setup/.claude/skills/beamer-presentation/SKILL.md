---
name: beamer-presentation
description: Skill spécialisé pour la création de diaporamas Beamer de haute qualité pour l'enseignement. Gère la mise en page, l'espacement, les animations, les exercices avec estimation de temps. Trois styles disponibles : collège, lycée, académique. Utiliser pour créer des présentations professionnelles adaptées au contexte éducatif.
---

# Beamer Presentation Expert

Système expert pour la création de diaporamas Beamer pédagogiques de haute qualité avec gestion précise de l'espacement, animations progressives et styles contextuels.

## Objectif

Créer des présentations Beamer professionnelles et lisibles, parfaitement adaptées au contexte (classe collège, classe lycée, présentation académique) avec une attention particulière à la densité d'information par slide et à la progressivité pédagogique.

## 📖 Guides de référence

**LIRE IMPÉRATIVEMENT** les guides suivants avant de créer une présentation :

- `.claude/skills/beamer-presentation/references/overlays-explicites.md` : **PRIORITÉ ABSOLUE** - Overlays explicites et package siunitx
- `.claude/skills/beamer-presentation/references/pauses-et-ordre.md` : **IMPORTANT** - Règles strictes pour les pauses et l'ordre des frames
- `.claude/skills/beamer-presentation/references/beamer-best-practices.md` : Bonnes pratiques et règles d'espacement
- `.claude/skills/beamer-presentation/references/beamer-styles-guide.md` : Guide des trois styles disponibles
- `.claude/skills/beamer-presentation/references/exercices-beamer.md` : Création d'exercices avec estimation de temps
- `.claude/skills/beamer-presentation/references/workflow-compilation-verification.md` : **WORKFLOW COMPLET** de compilation, vérification visuelle et nettoyage

## Principes Fondamentaux

### 1. Règle d'or : L'espace est votre allié

**JAMAIS plus de 70% de la slide remplie**

Une slide surchargée = une slide illisible. L'espace vide permet :
- La respiration visuelle
- La focalisation de l'attention
- La mémorisation efficace
- La lisibilité depuis le fond de la classe

### 2. Progressivité pédagogique avec overlays EXPLICITES

**RÈGLE ABSOLUE** : NE JAMAIS utiliser `\pause` - TOUJOURS utiliser les overlays explicites

Overlays à utiliser systématiquement :
- `\only<2->{...}` : Apparition à partir du slide 2 (sans réserver espace avant)
- `\uncover<3->{...}` : Dévoilement au slide 3 (avec espace réservé)
- `\alert<4>{...}` : Mise en évidence au slide 4
- `\visible<2->{...}` : Identique à `\uncover`
- `\item<2->` : Item visible à partir du slide 2

**Contrôle précis** : Savoir exactement ce qui s'affiche à chaque clic

Voir le guide complet : `.claude/skills/beamer-presentation/references/overlays-explicites.md`

### 3. Adaptation au contexte

Chaque style (collège, lycée, académique) a ses propres contraintes :
- **Collège** : Police grande, couleurs vives, animations fréquentes
- **Lycée** : Équilibre entre rigueur et accessibilité
- **Académique** : Sobriété, densité maîtrisée, références

## Structure type d'une présentation Beamer

### Préambule minimal

```latex
\documentclass[xcolor={svgnames}]{beamer}

% Choix du thème selon le style
\usetheme{college}  % ou lycee, ou academique

% Packages essentiels
\usepackage[french]{babel}
\usepackage{amsmath, amssymb}
\usepackage{tikz}
\usepackage{siunitx}

% Configuration siunitx pour affichage français des nombres
\sisetup{
  locale = FR,
  output-decimal-marker = {,},
  group-separator = {\,}
}

% Métadonnées
\title{Titre de la présentation}
\subtitle{Sous-titre si nécessaire}
\author{Votre nom}
\date{\today}
\institute{Établissement}

\begin{document}
```

### Slide de titre

```latex
\begin{frame}
  \titlepage
\end{frame}
```

### Slide de contenu type

```latex
\begin{frame}{Titre de la slide}
  \begin{itemize}[<+->]  % Révélation progressive
    \item Premier point
    \item Deuxième point
    \item Troisième point
  \end{itemize}

  \pause

  \begin{block}{Point important}
    Une information clé à retenir
  \end{block}
\end{frame}
```

### Slide avec exercice (avec overlays explicites et siunitx)

```latex
\begin{frame}{Exercice : Application directe}
  % ========================================
  % SLIDE 1-3 : Énoncé présent partout
  % ========================================
  \only<1->{%
    \textbf{Énoncé :} Résoudre l'équation suivante :
    \[
      \num{2}x + \num{3} = \num{7}
    \]
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 2-3 : Étapes de résolution
  % ========================================
  \uncover<2->{%
    \textbf{Solution :}
    \begin{align*}
      \num{2}x + \num{3} &= \num{7} \\
      \num{2}x &= \num{4} \\
      x &= \num{2}
    \end{align*}
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 3 : Résultat encadré
  % ========================================
  \uncover<3>{%
    \begin{alertblock}{Résultat}
      $x = \num{2}$
    \end{alertblock}
  }
\end{frame}
```

**Pages PDF** : 3 pages (contrôle précis des étapes)

## Workflow de création d'une présentation

### Étape 1 : Analyse du contexte

Identifier :
1. **Public cible** : Collège (6e-3e), Lycée (2nde-Tale), Académique (conférence)
2. **Durée prévue** : Adapter le nombre de slides (1 slide ≈ 2-3 minutes)
3. **Niveau de détail** : Introduction, approfondissement, synthèse
4. **Interactivité** : Exercices, questions, activités

### Étape 2 : Choix du template

Utiliser le template approprié dans `.claude/datas/latex-modeles/beamer/` :
- `template-college.tex` : Police 14pt, couleurs vives, animations nombreuses
- `template-lycee.tex` : Police 12pt, style équilibré, rigueur mathématique
- `template-academique.tex` : Police 11pt, sobriété, références bibliographiques

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

**Marges et espacements** :

```latex
% Pour une meilleure lisibilité
\setlength{\leftmargini}{1.5em}  % Marge des listes
\setlength{\parskip}{0.5em}      % Espace entre paragraphes

% Dans une slide
\begin{frame}{Titre}
  \vspace{1em}  % Espace après le titre

  Contenu...

  \vfill  % Remplissage flexible (pousse vers le bas)

  Note de bas de slide
\end{frame}
```

**Vérification de densité** :
- Compiler et vérifier visuellement
- Si slide > 70% remplie → découper en 2 slides
- Préférer 2 slides aérées à 1 slide dense

### Étape 5 : Animations et overlays

**Révélation progressive des items** :

```latex
\begin{itemize}[<+->]  % Chaque item apparaît l'un après l'autre
  \item Premier
  \item Deuxième
  \item Troisième
\end{itemize}
```

**Mise en évidence** :

```latex
\begin{itemize}
  \item Point normal
  \item \alert<2>{Point important révélé au clic 2}
  \item Point normal
\end{itemize}
```

**Remplacement dynamique** :

```latex
\only<1>{Texte initial}
\only<2>{Texte de remplacement}
```

### Étape 6 : Exercices avec estimation

Utiliser l'environnement `exobeamer` :

```latex
\begin{frame}{Exercice guidé}
  \begin{exobeamer}[Estimation : 8 min]
    \textbf{Partie 1 :} Question de compréhension

    \pause

    \textbf{Partie 2 :} Application

    \pause

    \textbf{Correction :} ...
  \end{exobeamer}
\end{frame}
```

### Étape 7 : Compilation et vérification

**OBLIGATOIRE** : Utiliser le skill `tex-compiling-skill` pour compiler.

1. **Compiler** avec le profil `lualatex_reims_favorite`
   ```bash
   python .claude/skills/tex-compiling-skill/scripts/quick_compile.py --file "presentation.tex" --passes 1
   ```

2. **Extraire les frames** avec le skill `pdf` pour vérification visuelle
   ```python
   # Extraction de toutes les frames en images PNG
   extract_pages_as_images(pdf_path="presentation.pdf", output_dir="./verification_frames/", dpi=150)
   ```

3. **Vérifier visuellement** chaque frame extraite :
   - Densité < 70% (< 60% pour collège)
   - Police lisible
   - Couleurs contrastées
   - Pas de débordement de texte/formules
   - Graphiques complets

4. **Corriger les bugs visuels** détectés et recompiler

5. **Nettoyer les fichiers temporaires** :
   ```bash
   # Supprimer les frames PNG extraites
   rm -rf ./verification_frames/
   # Nettoyer les fichiers de compilation
   python .claude/skills/tex-compiling-skill/scripts/clean_build_files.py --directory "."
   ```

6. **Tester** les overlays/animations dans le PDF final

7. **Chronométrer** la présentation complète

**Voir guide détaillé** : `.claude/skills/beamer-presentation/references/workflow-compilation-verification.md`

## Environnements Beamer Essentiels

### Blocks

```latex
\begin{block}{Définition}
  Contenu de la définition
\end{block}

\begin{alertblock}{Attention}
  Point important ou piège
\end{alertblock}

\begin{exampleblock}{Exemple}
  Illustration concrète
\end{exampleblock}
```

### Colonnes

```latex
\begin{columns}[T]  % [T] = alignement en haut
  \begin{column}{0.48\textwidth}
    Contenu colonne gauche
  \end{column}

  \begin{column}{0.48\textwidth}
    Contenu colonne droite
  \end{column}
\end{columns}
```

### Figures TikZ

```latex
\begin{frame}{Illustration graphique}
  \begin{center}
    \begin{tikzpicture}[scale=0.8]
      % Dessin TikZ
      \draw[->] (0,0) -- (5,0) node[right] {$x$};
      \draw[->] (0,0) -- (0,4) node[above] {$y$};
    \end{tikzpicture}
  \end{center}
\end{frame}
```

## Estimation des temps pour exercices

**Guide de référence** (fichier `exercices-beamer.md`) :

| Type d'exercice | Temps estimé | Complexité |
|-----------------|--------------|------------|
| Application directe | 3-5 min | ★☆☆ |
| Exercice guidé | 5-8 min | ★★☆ |
| Problème ouvert | 10-15 min | ★★★ |
| Investigation | 15-25 min | ★★★ |

**Encadré de temps** :

L'environnement `exobeamer` affiche automatiquement :
- Le temps estimé en haut à droite
- Un symbole de complexité
- Une zone modifiable pour le professeur (temps réel)

## Vérifications finales

**Checklist avant finalisation** :

- [ ] Chaque slide < 70% remplie
- [ ] Animations testées et fonctionnelles
- [ ] Police lisible depuis 5 mètres
- [ ] Cohérence des couleurs (thème respecté)
- [ ] Orthographe et mathématiques vérifiées
- [ ] Numérotation correcte
- [ ] Références citées si nécessaire
- [ ] Exercices avec estimations de temps
- [ ] Compilation sans erreur
- [ ] PDF généré et testé

## Bonnes pratiques

1. **Une idée = une slide** : Ne pas surcharger
2. **Couleurs cohérentes** : Respecter le thème choisi
3. **Taille de police** : Minimum 10pt pour le texte principal
4. **Formules mathématiques** : Centrées et aérées
5. **Images** : Haute résolution, vectorielles si possible
6. **Transitions** : Simples et discrètes (éviter les effets tape-à-l'œil)
7. **Navigation** : Inclure sommaire pour présentations > 20 slides
8. **Accessibilité** : Contraste suffisant, pas de rouge/vert ensemble

## Erreurs fréquentes à éviter

❌ **Slide surchargée** : > 10 lignes de texte
✅ **Slide aérée** : 5-7 points clés maximum

❌ **Police trop petite** : < 10pt
✅ **Police adaptée** : 11-14pt selon le contexte

❌ **Animations excessives** : Effets distrayants
✅ **Animations utiles** : Révélation progressive pédagogique

❌ **Pas d'estimation** : Exercice sans indication de temps
✅ **Temps estimé** : Permet au professeur de gérer la séance

❌ **Références manquantes** : Sources non citées
✅ **Bibliographie** : Slide dédiée en fin de présentation

## Rappels critiques

- **PRIORITÉ ABSOLUE** : Utiliser UNIQUEMENT les overlays explicites (`\only<2->{...}`, `\uncover<3->{...}`) - JAMAIS `\pause`
- **OBLIGATOIRE** : Utiliser `\num{nombre}` pour TOUS les nombres (package siunitx)
- **TOUJOURS** compiler avec LuaLaTeX pour une meilleure gestion des polices
- **TOUJOURS** vérifier la densité visuelle (< 70% rempli)
- **TOUJOURS** limiter à 2-3 pauses/overlays maximum par frame de solution
- **TOUJOURS** estimer le temps des exercices
- **TOUJOURS** adapter le style au public (collège/lycée/académique)
- **NE JAMAIS** utiliser `\pause` (contrôle imprécis)
- **NE JAMAIS** mettre plus de 7 items dans une liste
- **NE JAMAIS** utiliser des polices < 10pt
- **NE JAMAIS** écrire les nombres sans `\num{}` (3.14 → \num{3.14})

## Référence rapide des commandes

### Overlays explicites (TOUJOURS les utiliser)

```latex
\only<2->{...}             % Visible à partir du slide 2 (sans réserver espace)
\uncover<3->{...}          % Dévoilé au slide 3 (avec espace réservé)
\visible<3->{...}          % Identique à \uncover
\alert<4>{...}             % Mis en évidence au slide 4
\item<5-> Point            % Item visible à partir du slide 5
\invisible<7>{...}         % Invisible au slide 7
```

### Package siunitx (TOUJOURS pour les nombres)

```latex
\num{3}                    % Affichage: 3
\num{3.14}                 % Affichage: 3,14 (virgule française)
\num{1234}                 % Affichage: 1 234 (espace fine)
\num{-5}                   % Affichage: -5
\num{6.022e23}             % Affichage: 6,022 × 10²³
```

---

**Ce skill fait de vous un expert Beamer** capable de créer des présentations pédagogiques professionnelles, lisibles et efficaces pour tous les publics éducatifs.
