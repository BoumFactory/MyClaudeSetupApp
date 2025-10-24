# Beamer Best Practices - Guide complet

## Principes fondamentaux de conception

### La règle des 70%

**JAMAIS plus de 70% de la slide remplie**

Cette règle garantit :
- Lisibilité optimale depuis toutes les places de la classe
- Respiration visuelle pour l'attention
- Espace pour les annotations du professeur
- Mémorisation facilitée

### Calcul de la densité

Pour évaluer si une slide respecte la règle :

1. **Méthode visuelle** :
   - Imaginez la slide divisée en 10 bandes horizontales
   - Si plus de 7 bandes contiennent du texte → TROP DENSE
   - Découpez en 2 slides

2. **Méthode par comptage** :
   - Comptez les lignes de texte (y compris formules)
   - Maximum recommandé : 12 lignes pour lycée/académique, 8 pour collège
   - Au-delà → REFAIRE

### Police et lisibilité

| Public | Taille minimale | Taille recommandée | Taille titres |
|--------|-----------------|---------------------|---------------|
| Collège | 12pt | 14pt | 18-20pt |
| Lycée | 11pt | 12pt | 16-18pt |
| Académique | 10pt | 11pt | 14-16pt |

**Test de lisibilité** :
- Afficher la slide en plein écran
- Reculer de 3 mètres
- Si illisible → augmenter la police

## Gestion de l'espace

### Espacements verticaux

```latex
% Après un titre de slide
\vspace{1em}

% Entre deux blocs d'information
\vspace{0.5em}

% Avant une formule importante
\vspace{0.8em}
\[
  E = mc^2
\]
\vspace{0.8em}

% Pour pousser du contenu vers le bas
\vfill
```

### Espacements horizontaux

```latex
% Entre deux colonnes
\begin{columns}
  \begin{column}{0.45\textwidth}
    ...
  \end{column}
  \hspace{0.1\textwidth}  % Espace de 10%
  \begin{column}{0.45\textwidth}
    ...
  \end{column}
\end{columns}

% Dans du texte
Texte\quad important    % Espace moyen
Texte\qquad important   % Grand espace
```

### Marges des listes

```latex
% Réduire l'indentation des listes
\setlength{\leftmargini}{1.5em}
\setlength{\leftmarginii}{1.2em}

% Liste avec espacement personnalisé
\begin{itemize}
  \setlength{\itemsep}{0.5em}  % Espace entre items
  \item Premier
  \item Deuxième
\end{itemize}
```

## Animations et overlays

### Révélation progressive

**Pattern recommandé** : 1 overlay = 1 idée nouvelle

```latex
% BAD : Tout d'un coup
\begin{frame}{Propriétés}
  \begin{itemize}
    \item Propriété 1
    \item Propriété 2
    \item Propriété 3
  \end{itemize}
\end{frame}

% GOOD : Progressif
\begin{frame}{Propriétés}
  \begin{itemize}[<+->]
    \item Propriété 1
    \item Propriété 2
    \item Propriété 3
  \end{itemize}
\end{frame}
```

### Mise en évidence

```latex
\begin{frame}{Théorème de Pythagore}
  Dans un triangle rectangle :
  \[
    \alert<2>{a^2 + b^2 = c^2}
  \]

  \uncover<3->{
    où $c$ est l'hypoténuse.
  }
\end{frame}
```

### Remplacement dynamique

```latex
\begin{frame}{Résolution progressive}
  Résoudre : $2x + 3 = 7$

  \only<2>{
    Soustraire 3 de chaque côté...
  }

  \only<3>{
    $2x = 4$
  }

  \only<4>{
    Diviser par 2...
  }

  \only<5>{
    $x = 2$
  }
\end{frame}
```

## Structure d'une présentation complète

### Architecture recommandée

```
1. Slide de titre (1 slide)
2. Sommaire/Plan (1 slide) - si > 20 slides
3. Introduction/Rappels (2-3 slides)
4. Section 1 (5-7 slides)
   - Titre de section (1 slide)
   - Contenu (4-6 slides)
5. Section 2 (5-7 slides)
6. Exercices/Applications (3-5 slides)
7. Conclusion/Synthèse (1-2 slides)
8. Références (1 slide) - si académique
```

### Slide de titre de section

```latex
\section{Nouvelle section}

\begin{frame}
  \sectionpage  % Génère automatiquement une slide de section
\end{frame}

% OU personnalisé :

\begin{frame}
  \begin{center}
    {\Huge Section 2}

    \vspace{1em}

    {\Large Applications et exercices}
  \end{center}
\end{frame}
```

### Sommaire interactif

```latex
% Slide de sommaire initial
\begin{frame}{Plan}
  \tableofcontents
\end{frame}

% Rappel du sommaire à chaque section
\AtBeginSection[]
{
  \begin{frame}{Où en sommes-nous ?}
    \tableofcontents[currentsection]
  \end{frame}
}
```

## Couleurs et contraste

### Règles d'accessibilité

1. **Contraste minimum** : Ratio 4.5:1 entre texte et fond
2. **Éviter rouge/vert ensemble** : Daltonisme
3. **Tester en noir et blanc** : Impression éventuelle

### Palette de couleurs par style

**Collège** :
- Fond : Blanc ou bleu très clair
- Titres : Bleu vif, orange
- Texte : Noir
- Alertes : Rouge vif, vert pomme

**Lycée** :
- Fond : Blanc, gris très clair
- Titres : Bleu marine, bordeaux
- Texte : Gris foncé
- Alertes : Rouge bordeaux, bleu roi

**Académique** :
- Fond : Blanc, beige clair
- Titres : Noir, gris anthracite
- Texte : Noir
- Alertes : Rouge sombre, bleu nuit

### Utilisation des couleurs

```latex
% Définir des couleurs personnalisées
\definecolor{maincolor}{RGB}{0, 102, 204}    % Bleu
\definecolor{alertcolor}{RGB}{204, 0, 0}     % Rouge

% Utiliser dans le texte
\textcolor{maincolor}{Texte important}
\alert{Attention !}  % Utilise la couleur d'alerte du thème
```

## Formules mathématiques

### Centrage et espacement

```latex
% MAUVAIS : Formule collée au texte
On a $a^2+b^2=c^2$ donc le triangle est rectangle.

% BON : Formule mise en valeur
\begin{frame}{Théorème de Pythagore}
  Si le triangle $ABC$ est rectangle en $A$, alors :

  \vspace{0.8em}
  \[
    AB^2 + AC^2 = BC^2
  \]
  \vspace{0.8em}

  Cette relation permet de calculer des longueurs.
\end{frame}
```

### Formules progressives

```latex
\begin{frame}{Développement}
  \begin{align*}
    (a+b)^2 &= (a+b)(a+b) \\
    \uncover<2->{&= a^2 + ab + ba + b^2} \\
    \uncover<3->{&= a^2 + 2ab + b^2}
  \end{align*}
\end{frame}
```

## Images et graphiques

### Dimensionnement

```latex
% Image centrée avec taille contrôlée
\begin{center}
  \includegraphics[width=0.6\textwidth]{image.png}
\end{center}

% Image dans une colonne
\begin{columns}
  \begin{column}{0.5\textwidth}
    Texte explicatif...
  \end{column}
  \begin{column}{0.45\textwidth}
    \includegraphics[width=\textwidth]{graphique.pdf}
  \end{column}
\end{columns}
```

### Graphiques TikZ

**Règle** : Garder les graphiques TikZ simples et lisibles

```latex
\begin{frame}{Représentation graphique}
  \begin{center}
    \begin{tikzpicture}[scale=0.9]
      % Axes
      \draw[->] (-1,0) -- (6,0) node[right] {$x$};
      \draw[->] (0,-1) -- (0,5) node[above] {$y$};

      % Grille légère
      \draw[gray!30, very thin] (0,0) grid (5,4);

      % Fonction
      \draw[blue, thick, domain=0:5] plot (\x, {0.5*\x + 1});

      % Annotations
      \node[blue, above right] at (4, 3) {$f(x) = 0.5x + 1$};
    \end{tikzpicture}
  \end{center}
\end{frame}
```

## Tableaux

### Tableaux lisibles

```latex
\begin{frame}{Tableau de valeurs}
  \begin{center}
    \renewcommand{\arraystretch}{1.5}  % Espacement vertical
    \begin{tabular}{|c|c|c|c|c|}
      \hline
      \rowcolor{blue!20}  % En-tête coloré
      $x$ & 0 & 1 & 2 & 3 \\
      \hline
      $f(x)$ & 1 & 2 & 4 & 8 \\
      \hline
    \end{tabular}
  \end{center}
\end{frame}
```

### Révélation progressive

```latex
\begin{frame}{Compléter le tableau}
  \begin{tabular}{|c|c|}
    \hline
    $x$ & $f(x)$ \\
    \hline
    0 & \only<2->{1} \\
    \hline
    1 & \only<3->{2} \\
    \hline
    2 & \only<4->{4} \\
    \hline
  \end{tabular}
\end{frame}
```

## Listes et énumérations

### Types de listes

```latex
% Liste à puces classique
\begin{itemize}
  \item Point 1
  \item Point 2
\end{itemize}

% Liste numérotée
\begin{enumerate}
  \item Étape 1
  \item Étape 2
\end{enumerate}

% Liste descriptive
\begin{description}
  \item[Définition] Explication
  \item[Théorème] Énoncé
\end{description}
```

### Imbrication

**Règle** : Maximum 2 niveaux d'imbrication

```latex
% MAUVAIS : 3 niveaux
\begin{itemize}
  \item Niveau 1
    \begin{itemize}
      \item Niveau 2
        \begin{itemize}
          \item Niveau 3  % TROP !
        \end{itemize}
    \end{itemize}
\end{itemize}

% BON : 2 niveaux maximum
\begin{itemize}
  \item Catégorie A
    \begin{itemize}
      \item Sous-catégorie A1
      \item Sous-catégorie A2
    \end{itemize}
  \item Catégorie B
\end{itemize}
```

## Blocks et encadrés

### Types de blocks

```latex
% Block standard (définition, propriété)
\begin{block}{Définition}
  Une fonction est dite \emph{linéaire} si...
\end{block}

% Alertblock (attention, piège)
\begin{alertblock}{Attention}
  Ne pas confondre avec une fonction affine !
\end{alertblock}

% Exampleblock (exemple, application)
\begin{exampleblock}{Exemple}
  La fonction $f(x) = 2x$ est linéaire.
\end{exampleblock}
```

### Blocks progressifs

```latex
\begin{frame}{Propriétés}
  \begin{block}<2->{Propriété 1}
    Énoncé...
  \end{block}

  \begin{block}<3->{Propriété 2}
    Énoncé...
  \end{block}
\end{frame}
```

## Transitions et effets

### Transitions recommandées

```latex
% Pas de transition (sobre, professionnel)
\setbeameroption{transitionsoff}

% OU transition simple
\transboxin<2>      % Apparition en boîte
\transfade<3>       % Fondu
\transwipe<4>       % Balayage
```

**Règle** : Moins il y a d'effets, plus c'est professionnel.

- Collège : Transitions autorisées mais sobres
- Lycée : Transitions minimales
- Académique : Aucune transition

## Navigation

### Masquer les symboles de navigation

```latex
% Dans le préambule
\setbeamertemplate{navigation symbols}{}  % Supprime les icônes de navigation
```

### Liens internes

```latex
% Créer une ancre
\label{slide:important}

% Lien vers cette ancre
\hyperlink{slide:important}{Voir slide importante}

% Bouton de retour
\begin{frame}[label=slide:important]{Slide importante}
  ...
  \hyperlink{slide:retour}{\beamerreturnbutton{Retour}}
\end{frame}
```

## Checklist finale

Avant de valider une présentation :

### Contenu

- [ ] Chaque slide < 70% remplie
- [ ] Police ≥ taille minimale du style
- [ ] Formules mathématiques correctes
- [ ] Orthographe vérifiée
- [ ] Exercices avec temps estimé

### Visuel

- [ ] Couleurs cohérentes avec le thème
- [ ] Contraste suffisant
- [ ] Images haute résolution
- [ ] Graphiques lisibles
- [ ] Pas de slide surchargée

### Technique

- [ ] Compilation sans erreur
- [ ] Animations testées
- [ ] PDF généré et testé
- [ ] Navigation fonctionnelle
- [ ] Numérotation correcte

### Pédagogique

- [ ] Progressivité respectée
- [ ] Transitions logiques entre slides
- [ ] Exemples pertinents
- [ ] Exercices adaptés au niveau
- [ ] Durée totale estimée

## Erreurs fréquentes

### 1. Slide trop dense

❌ **Mauvais** :
```
Slide avec 15 lignes de texte, 3 formules, 2 graphiques...
```

✅ **Bon** :
```
Découper en 3 slides :
- Slide 1 : Texte principal (5-7 lignes)
- Slide 2 : Formules (2-3 maximum)
- Slide 3 : Graphiques illustratifs
```

### 2. Police trop petite

❌ **Mauvais** : Police 8pt pour tout faire rentrer

✅ **Bon** : Police 12pt et découpage en plusieurs slides

### 3. Animations excessives

❌ **Mauvais** : Effet de rotation 3D sur chaque bullet

✅ **Bon** : `\pause` simple ou `\uncover` progressif

### 4. Couleurs criardes

❌ **Mauvais** : Texte rose fluo sur fond jaune

✅ **Bon** : Contraste noir/blanc ou bleu marine/blanc

### 5. Pas de pause interactive

❌ **Mauvais** : 30 slides sans interaction

✅ **Bon** : Exercice ou question toutes les 5-7 slides

---

**En appliquant ces bonnes pratiques, vos présentations Beamer seront professionnelles, lisibles et pédagogiquement efficaces.**
