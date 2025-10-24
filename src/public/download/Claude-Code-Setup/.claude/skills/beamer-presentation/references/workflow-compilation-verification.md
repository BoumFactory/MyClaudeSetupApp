# Workflow de compilation et vérification Beamer

## Principe

Créer une présentation Beamer de qualité nécessite un processus itératif de :
1. **Création** du code LaTeX
2. **Compilation** avec le skill tex-compiling-skill
3. **Vérification visuelle** avec le skill pdf (extraction de frames)
4. **Correction** des bugs visuels détectés
5. **Nettoyage** des fichiers temporaires

## Étape 1 : Création du contenu Beamer

### Alternance question/réponse

**Principe pédagogique** : Chaque notion doit être suivie d'une vérification.

Pattern recommandé :
```
Slide 1-3 : Introduction de la notion
Slide 4   : Question aux élèves
Slide 5   : Réponse révélée progressivement
Slide 6-8 : Approfondissement
Slide 9   : Nouvelle question
Slide 10  : Réponse
```

### Gestion des pauses dans les réponses

**Règle d'or** : Révéler une réponse = révéler un raisonnement, pas juste un résultat.

#### Pattern 1 : Pause simple

```latex
\begin{frame}{Question}
  Calculer la dérivée de $f(x) = x^2 + 3x$.

  \pause

  \textbf{Réponse :} $f'(x) = 2x + 3$
\end{frame}
```

**Usage** : Question simple, réponse immédiate.

#### Pattern 2 : Révélation par étapes

```latex
\begin{frame}{Question}
  Résoudre : $2x + 3 = 7$

  \pause

  \textbf{Méthode :}

  \begin{enumerate}
    \item<3-> Soustraire 3 de chaque côté
    \item<4-> On obtient : $2x = 4$
    \item<5-> Diviser par 2
    \item<6-> Solution : $x = 2$
  \end{enumerate}
\end{frame}
```

**Usage** : Question nécessitant plusieurs étapes de raisonnement.

#### Pattern 3 : Remplacement progressif

```latex
\begin{frame}{Développement}
  Développer : $(x+2)^2$

  \vspace{1em}

  \only<1>{%
    \textcolor{gray}{Utilisez l'identité remarquable...}
  }

  \only<2>{%
    $(x+2)^2 = x^2 + 2 \cdot x \cdot 2 + 2^2$
  }

  \only<3>{%
    $(x+2)^2 = x^2 + 4x + 4$
  }
\end{frame}
```

**Usage** : Transformation progressive d'une expression.

#### Pattern 4 : Zone de réponse avec crep (concept adapté)

Pour Beamer, on adapte le concept de `\crep` (correction espace réponse) :

```latex
% Définition d'un environnement réponse
\newenvironment{beamerrep}{%
  \par\vspace{0.5em}%
  \textcolor{blue!70!black}{\rule{\textwidth}{0.4pt}}%
  \par\vspace{0.3em}%
  \textcolor{blue!70!black}{\small\textbf{Zone de réponse :}}%
  \par\vspace{0.3em}%
}{%
  \par\vspace{0.3em}%
  \textcolor{blue!70!black}{\rule{\textwidth}{0.4pt}}%
}

% Utilisation
\begin{frame}{Exercice}
  Calculer : $3 \times 7 = ?$

  \pause

  \begin{beamerrep}
    \uncover<3->{$3 \times 7 = 21$}
  \end{beamerrep}
\end{frame}
```

### Alternance systématique

**Structure type d'une section** :

```latex
% === SECTION : Notion X ===

% Slide 1 : Introduction
\begin{frame}{Introduction à X}
  Définition...
\end{frame}

% Slide 2 : Propriété
\begin{frame}{Propriété importante}
  Théorème...
\end{frame}

% Slide 3 : Question de compréhension
\begin{frame}{Vérifions ensemble}
  \textbf{Question :} Que se passe-t-il si... ?

  \pause

  \textbf{Réponse :} ...
\end{frame}

% Slide 4 : Exemple détaillé
\begin{frame}{Exemple}
  Application...
\end{frame}

% Slide 5 : Exercice
\begin{frame}{À vous de jouer}
  \begin{exobeamer}[...]
    Énoncé...
    \pause
    Solution...
  \end{exobeamer}
\end{frame}

% === FIN SECTION ===
```

## Étape 2 : Compilation avec tex-compiling-skill

### Utilisation du skill

**OBLIGATOIRE** : Toujours compiler via le skill tex-compiling-skill.

```bash
# Via le skill tex-compiling-skill
python .claude/skills/tex-compiling-skill/scripts/quick_compile.py \
  --file "presentation.tex" \
  --passes 1
```

**Profil recommandé** : `lualatex_reims_favorite` (LuaLaTeX + shell-escape)

### Détection des erreurs

**Erreurs fréquentes en Beamer** :

1. **Caractères spéciaux dans les frames**
   ```
   Error: Missing $ inserted
   ```
   → Vérifier les `_`, `%`, `&` dans le texte

2. **Overlays mal fermés**
   ```
   Error: Extra }, or forgotten \endgroup
   ```
   → Vérifier `\only<>{}`, `\uncover<>{}` bien fermés

3. **Environnements imbriqués**
   ```
   Error: \begin{itemize} ended by \end{frame}
   ```
   → Fermer tous les environnements dans l'ordre

4. **Packages manquants**
   ```
   Error: File tikz.sty not found
   ```
   → Ajouter `\usepackage{tikz}` dans le préambule

### Workflow de correction

```
1. Compiler avec tex-compiling-skill
2. Si erreur :
   a. Analyser le log avec analyze_latex_log()
   b. Identifier la ligne problématique
   c. Obtenir le contexte avec get_file_context()
   d. Corriger l'erreur
   e. Recompiler
3. Répéter jusqu'à compilation réussie
```

## Étape 3 : Vérification visuelle avec le skill pdf

### Extraction de frames

**Principe** : Le skill pdf permet d'extraire chaque frame (slide) du PDF Beamer en image pour vérification visuelle.

```python
# Via le skill pdf
# Extraire toutes les pages (frames) en images PNG

from pdf_tools import extract_pages_as_images

extract_pages_as_images(
    pdf_path="presentation.pdf",
    output_dir="./verification_frames/",
    dpi=150,  # Résolution suffisante pour vérification
    format="png"
)
```

### Checklist de vérification visuelle

Pour chaque frame extraite, vérifier :

#### 1. Densité et espacement

- [ ] Frame < 70% remplie (60% pour collège)
- [ ] Espaces suffisants entre blocs
- [ ] Marges respectées
- [ ] Pas de texte tronqué

**Bug visuel fréquent** :
```
Texte qui déborde de la slide →→→→
```

**Correction** :
```latex
% Découper en 2 slides
% OU réduire la police
% OU reformuler plus concisément
```

#### 2. Police et lisibilité

- [ ] Police ≥ taille minimale (11pt, 12pt, 14pt)
- [ ] Titres lisibles et contrastés
- [ ] Formules mathématiques claires
- [ ] Pas de chevauchement de texte

**Bug visuel fréquent** :
```
Formule trop longue qui sort de la slide
```

**Correction** :
```latex
% Utiliser multline ou align pour découper
\begin{multline}
  \text{longue formule partie 1} \\
  \text{longue formule partie 2}
\end{multline}
```

#### 3. Couleurs et contraste

- [ ] Contraste suffisant texte/fond
- [ ] Couleurs cohérentes avec le thème
- [ ] Pas de rouge/vert ensemble
- [ ] Alertes bien visibles

**Bug visuel fréquent** :
```
Texte jaune sur fond blanc → illisible
```

**Correction** :
```latex
% Changer la couleur pour meilleur contraste
\textcolor{blue!70!black}{Texte important}
```

#### 4. Éléments graphiques

- [ ] Images nettes (pas pixelisées)
- [ ] Graphiques TikZ complets
- [ ] Tableaux bien alignés
- [ ] Pas de débordement

**Bug visuel fréquent** :
```
Graphique TikZ coupé sur les bords
```

**Correction** :
```latex
% Réduire l'échelle
\begin{tikzpicture}[scale=0.8]
  ...
\end{tikzpicture}
```

#### 5. Animations et overlays

- [ ] Pas de "fantômes" visuels
- [ ] Transitions propres
- [ ] Numérotation correcte des overlays
- [ ] Révélation progressive logique

**Bug visuel fréquent** :
```
Espaces vides qui apparaissent/disparaissent entre overlays
```

**Correction** :
```latex
% Utiliser \uncover au lieu de \only pour réserver l'espace
\uncover<2->{Texte révélé}  % Espace réservé dès overlay 1
```

### Extraction et visualisation automatisée

**Script de vérification complet** :

```python
# Script d'extraction et vérification
import os
from pdf_tools import extract_pages_as_images

# Extraire toutes les frames
output_dir = "./verification_frames/"
extract_pages_as_images(
    pdf_path="presentation.pdf",
    output_dir=output_dir,
    dpi=150
)

# Lire chaque frame pour vérification
frames = sorted([f for f in os.listdir(output_dir) if f.endswith('.png')])

print(f"Total de {len(frames)} frames extraites.")
print("Vérification visuelle nécessaire pour chaque frame.")

# L'agent lit chaque image et vérifie visuellement
for i, frame in enumerate(frames, 1):
    print(f"\n=== Frame {i}/{len(frames)} : {frame} ===")
    # Lecture de l'image et analyse visuelle
    # Détection de bugs potentiels
```

## Étape 4 : Correction des bugs visuels

### Processus itératif

```
Pour chaque bug détecté dans les frames :

1. Identifier la frame problématique (numéro de page)
2. Localiser le code LaTeX correspondant
3. Appliquer la correction appropriée
4. Recompiler avec tex-compiling-skill
5. Réextraire UNIQUEMENT les frames modifiées
6. Vérifier la correction
7. Passer à la frame suivante
```

### Corrections fréquentes

#### Bug : Slide trop dense

**Détecté visuellement** : Frame remplie à > 70%

**Correction** :

```latex
% AVANT : 1 slide surchargée
\begin{frame}{Propriétés}
  \begin{itemize}
    \item Propriété 1 avec longue explication...
    \item Propriété 2 avec longue explication...
    \item Propriété 3 avec longue explication...
    \item Propriété 4 avec longue explication...
  \end{itemize}
  Formules...
  Exemples...
\end{frame}

% APRÈS : 2 slides aérées
\begin{frame}{Propriétés (1/2)}
  \begin{itemize}
    \item Propriété 1 avec explication...
    \item Propriété 2 avec explication...
  \end{itemize}
\end{frame}

\begin{frame}{Propriétés (2/2)}
  \begin{itemize}
    \item Propriété 3 avec explication...
    \item Propriété 4 avec explication...
  \end{itemize}
\end{frame}
```

#### Bug : Formule trop longue

**Détecté visuellement** : Formule qui sort du cadre

**Correction** :

```latex
% AVANT : Formule trop longue
\[
  f(x) = a_0 + a_1 x + a_2 x^2 + a_3 x^3 + a_4 x^4 + a_5 x^5 + \cdots
\]

% APRÈS : Formule découpée
\begin{align*}
  f(x) &= a_0 + a_1 x + a_2 x^2 + a_3 x^3 \\
       &\quad + a_4 x^4 + a_5 x^5 + \cdots
\end{align*}
```

#### Bug : Police trop petite

**Détecté visuellement** : Texte illisible sur la frame extraite

**Correction** :

```latex
% AVANT : Police par défaut trop petite
\begin{frame}{Détails}
  Texte explicatif détaillé...
\end{frame}

% APRÈS : Augmenter la taille
\begin{frame}{Détails}
  {\large Texte explicatif détaillé...}
\end{frame}

% OU découper en plusieurs slides
```

#### Bug : Couleur illisible

**Détecté visuellement** : Contraste insuffisant

**Correction** :

```latex
% AVANT : Jaune sur blanc
\textcolor{yellow}{Attention !}

% APRÈS : Couleur contrastée
\textcolor{orange!80!black}{Attention !}
% OU
\alert{Attention !}  % Utilise la couleur d'alerte du thème
```

## Étape 5 : Nettoyage des fichiers temporaires

### Pourquoi nettoyer ?

**Problème** : L'extraction de frames génère de nombreux fichiers PNG temporaires qui polluent l'espace de travail.

**Solution** : Nettoyer systématiquement après vérification.

### Fichiers à nettoyer

```
verification_frames/
├── frame_001.png  ← À supprimer
├── frame_002.png  ← À supprimer
├── frame_003.png  ← À supprimer
├── ...
└── frame_050.png  ← À supprimer
```

### Script de nettoyage

```python
import os
import shutil

# Supprimer le dossier de vérification
verification_dir = "./verification_frames/"

if os.path.exists(verification_dir):
    shutil.rmtree(verification_dir)
    print(f"✓ Dossier {verification_dir} supprimé")

# Nettoyer aussi les fichiers de compilation LaTeX
latex_temp_files = [
    "presentation.aux",
    "presentation.log",
    "presentation.nav",
    "presentation.out",
    "presentation.snm",
    "presentation.toc",
    "presentation.synctex.gz"
]

for temp_file in latex_temp_files:
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"✓ {temp_file} supprimé")

print("\n✓ Nettoyage terminé. Seul le PDF final est conservé.")
```

### Commande de nettoyage via skill

```bash
# Via le skill tex-compiling-skill
python .claude/skills/tex-compiling-skill/scripts/clean_build_files.py \
  --directory "."
```

## Workflow complet résumé

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CRÉATION                                                 │
│    - Écrire le code LaTeX Beamer                           │
│    - Alterner questions/réponses                           │
│    - Gérer les pauses progressives                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. COMPILATION (skill tex-compiling-skill)                 │
│    - Compiler avec lualatex_reims_favorite                 │
│    - Analyser les erreurs si échec                         │
│    - Corriger et recompiler                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. EXTRACTION (skill pdf)                                  │
│    - Extraire toutes les frames en PNG                     │
│    - Résolution 150 dpi pour vérification                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. VÉRIFICATION VISUELLE                                   │
│    - Lire chaque frame extraite                            │
│    - Vérifier densité, lisibilité, couleurs, graphiques    │
│    - Détecter les bugs visuels                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────────────┐
                    │ Bugs détectés │
                    └───────────────┘
                            ↓
                         OUI ──→ Retour à CRÉATION (corriger)
                            │
                          NON
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. NETTOYAGE                                               │
│    - Supprimer les frames PNG                              │
│    - Nettoyer les fichiers .aux, .log, etc.               │
│    - Conserver uniquement le PDF final                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────────────┐
                    │ PRÉSENTATION  │
                    │   FINALISÉE   │
                    └───────────────┘
```

## Exemple complet : Cycle de création d'une présentation

### Itération 1

```latex
% presentation.tex
\begin{frame}{Dérivation}
  \begin{itemize}
    \item La dérivée mesure le taux de variation
    \item $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$
    \item Application : vitesse instantanée
    \item Formule : $(x^n)' = nx^{n-1}$
    \item Exemple : $(x^3)' = 3x^2$
  \end{itemize}
\end{frame}
```

**Compilation** → ✓ Réussie

**Extraction** → 1 frame PNG

**Vérification** → ❌ Bug détecté : Slide trop dense (80% remplie)

### Itération 2

```latex
% Correction : Découper en 2 slides
\begin{frame}{Dérivation : Définition}
  \begin{itemize}
    \item La dérivée mesure le taux de variation
    \item Définition formelle :
    \[
      f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
    \]
  \end{itemize}
\end{frame}

\begin{frame}{Dérivation : Formule}
  \begin{block}{Formule des puissances}
    $(x^n)' = nx^{n-1}$
  \end{block}

  \pause

  \begin{exampleblock}{Exemple}
    $(x^3)' = 3x^2$
  \end{exampleblock}
\end{frame}
```

**Compilation** → ✓ Réussie

**Extraction** → 2 frames PNG

**Vérification** → ✓ Aucun bug visuel

**Nettoyage** → Supprimer verification_frames/ et fichiers .aux

**Résultat** : Présentation finalisée, PDF prêt à l'emploi.

---

**En suivant ce workflow rigoureux, vous garantissez des présentations Beamer sans bugs visuels, lisibles et professionnelles.**
