# /optiLatex - Création LaTeX autonome optimisée

Génère des documents LaTeX de qualité. Conçu pour aider l'utilisateur débutant en LaTeX.

## Protocole

### 1. QUESTIONS (si non précisé)
- Style : cadres visibles ou discrets ?
- Colonnes : 1 ou 2 ?

### 2. EN-TÊTE STANDARD

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}
\usepackage[french]{babel}\usepackage{fourier}
\usepackage[left=1cm,right=1cm,top=1.5cm,bottom=1.5cm]{geometry}
\usepackage{multicol,amsmath,amssymb,mathtools}
\usepackage[most]{tcolorbox}\tcbuselibrary{skins,breakable}
\usepackage{eurosym,csquotes}

%% STYLES
\newtcolorbox{boxtitre}[1]{colback=blue!5,colframe=blue!50!black,fonttitle=\bfseries,title=#1,breakable}
\newtcolorbox{boxdiscret}[1]{enhanced,colback=gray!5,boxrule=0pt,frame hidden,borderline west={3pt}{0pt}{blue!60},fonttitle=\bfseries,title=#1,breakable}
\newtcolorbox{definition}[1][Définition]{enhanced,colback=blue!3,boxrule=0pt,frame hidden,borderline west={3pt}{0pt}{blue!70},fonttitle=\bfseries\color{blue!70!black},title=#1}
\newtcolorbox{methode}[1][Méthode]{enhanced,colback=orange!5,boxrule=0pt,frame hidden,borderline west={3pt}{0pt}{orange!70},fonttitle=\bfseries\color{orange!70!black},title=#1}
\newtcolorbox{attention}[1][Attention]{enhanced,colback=red!5,boxrule=0pt,frame hidden,borderline west={3pt}{0pt}{red!70},fonttitle=\bfseries\color{red!70!black},title=#1}
\newtcolorbox{exercice}[1][Exercice]{enhanced,colback=green!3,boxrule=0pt,frame hidden,borderline west={3pt}{0pt}{green!60!black},fonttitle=\bfseries\color{green!60!black},title=#1}

\newcommand{\acc}[1]{\textcolor{blue!70!black}{\textbf{#1}}}
\newcommand{\err}[1]{\textcolor{red!70!black}{\textbf{#1}}}
\newcommand{\ok}[1]{\textcolor{green!60!black}{\textbf{#1}}}
\newenvironment{grille}[1][2]{\begin{multicols}{#1}}{\end{multicols}}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.3em}

\begin{document}
\input{enonce}
\end{document}
```

### 3. RÈGLES D'ÉCRITURE

| Syntaxe | Usage |
|---------|-------|
| `\frquote{ texte }` | Guillemets français (jamais « ») |
| `\acc{verbe}` | Verbes d'action : calculer, tracer, déterminer, justifier... |
| `\acc{format}` | Formats de réponse : notation scientifique, fraction irréductible... |
| `\acc{crucial}` | Mots-clés : quoi, où, comment, pourquoi, condition, règle... |
| `\err{erreur}` | Erreurs fréquentes |
| `\ok{correct}` | Exemples corrects |

### 4. AIDE-MÉMOIRE

| Besoin | Code |
|--------|------|
| Cadre visible | `\begin{boxtitre}{T}...\end{boxtitre}` |
| Cadre discret | `\begin{boxdiscret}{T}...\end{boxdiscret}` |
| Définition | `\begin{definition}...\end{definition}` |
| Méthode | `\begin{methode}...\end{methode}` |
| Attention | `\begin{attention}...\end{attention}` |
| Exercice | `\begin{exercice}[Exo N]...\end{exercice}` |
| 2 colonnes | `\begin{grille}...\columnbreak...\end{grille}` |
| Guillemets | `\frquote{ mot }` |
| Euro/Degré | `25\euro` / `15$^\circ$C` |

### 5. EXÉCUTION

1. Questions si style/colonnes manquants
2. Créer dossier + `document.tex` + `enonce.tex`
3. Compiler et afficher résultat
