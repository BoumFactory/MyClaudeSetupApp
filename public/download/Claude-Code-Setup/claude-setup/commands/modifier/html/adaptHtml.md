# /adaptHtml - Adaptation de documents vers HTML/KaTeX

## Description

Adapte automatiquement un document existant (LaTeX, PDF, texte, Markdown) vers le format HTML/KaTeX interactif. Le résultat est un cours HTML autonome avec toutes les fonctionnalités du système (sélecteur d'univers, dark mode, vocabulaire interactif).

## Usage

```
/adaptHtml <chemin_source> [--niveau <niveau>] [--theme <theme>] [--univers <univers>]
```

## Exemples d'utilisation

```bash
# Adapter un fichier LaTeX
/adaptHtml "1. Cours/2nde/Sequence-Vecteurs/Cours/enonce.tex"

# Adapter avec options
/adaptHtml "document.tex" --niveau 3eme --theme geometrie --univers manga

# Adapter un PDF (extraction de contenu)
/adaptHtml "cours-probabilites.pdf" --niveau 1ere --theme probabilites

# Adapter depuis Markdown
/adaptHtml "notes.md" --niveau tle --theme analyse
```

## Protocole d'exécution

### ÉTAPE 1 : ANALYSE DE LA SOURCE

1. **Lire le fichier source** pour identifier :
   - Type de document (LaTeX, PDF, Markdown, texte)
   - Niveau scolaire (si détectable)
   - Thème mathématique
   - Structure du contenu

2. **Extraire les métadonnées** :
   - Titre du cours
   - Auteur (si disponible)
   - Sections principales

### ÉTAPE 2 : MAPPING CONCEPTUEL

Transformer les éléments selon leur **rôle pédagogique** :

#### Depuis LaTeX (bfcours ou autre)

| Environnement source | Classe HTML cible |
|---------------------|-------------------|
| `Definition`, `definition`, `defi` | `.definition` |
| `Theoreme`, `theorem`, `thm` | `.theoreme` |
| `Propriete`, `prop`, `property` | `.propriete` |
| `Exemple`, `example`, `ex` | `.exemple` |
| `Methode`, `method` | `.methode` |
| `Remarque`, `remark`, `rem` | `.remarque` |
| `EXO`, `exercice`, `exercise` | `.exercice` |
| `Demonstration`, `proof` | `.demonstration` |

#### Formules LaTeX

| Source | HTML |
|--------|------|
| `$...$` | `$...$` (conservé) |
| `$$...$$` | `$$...$$` (conservé) |
| `\(...\)` | `$...$` |
| `\[...\]` | `$$...$$` |
| `\begin{align}...\end{align}` | `$$\begin{aligned}...\end{aligned}$$` |
| `\begin{equation}...\end{equation}` | `$$...$$` |

#### Structure

| Source | HTML |
|--------|------|
| `\section{...}` | `<h2>...</h2>` |
| `\subsection{...}` | `<h3>...</h3>` |
| `\textbf{...}` | `<strong>...</strong>` |
| `\textit{...}` | `<em>...</em>` |
| `\begin{itemize}` | `<ul>` |
| `\begin{enumerate}` | `<ol>` |

### ÉTAPE 3 : CRÉATION DU PROJET

1. **Initialiser le projet HTML/KaTeX** :
```bash
python ".claude/skills/html-katex-compiler/scripts/init_project.py" "<chemin>" --titre "<titre>" --niveau <niveau> --theme <theme> --univers <univers>
```

2. **Créer les fichiers parts/** selon la structure détectée.

### ÉTAPE 4 : TRANSFORMATION DU CONTENU

Pour chaque section du document source :

1. **Créer un fichier** `parts/XX-nom-section.html`
2. **Convertir le contenu** avec les règles de mapping
3. **Identifier le vocabulaire clé** et ajouter les spans `.vocab`
4. **Mettre à jour** `config.json` avec `parts_order`

### ÉTAPE 5 : ENRICHISSEMENT (optionnel)

Proposer des améliorations :
- Ajout d'infobulles de vocabulaire
- Restructuration pédagogique
- Ajout d'exemples interactifs

### ÉTAPE 6 : COMPILATION ET VÉRIFICATION

```bash
python ".claude/skills/html-katex-compiler/scripts/compile_project.py" "<chemin>"
```

Vérifier :
- Les formules s'affichent correctement
- Les blocs pédagogiques sont bien stylés
- Le sélecteur d'univers fonctionne
- Le mode dark/light fonctionne

### ÉTAPE 7 : RAPPORT

```
✅ Adaptation terminée !

📄 Source : [chemin_source]
📁 Projet : [chemin_projet]

📊 Statistiques :
  - Sections : X
  - Définitions : X
  - Théorèmes : X
  - Exemples : X
  - Exercices : X

🔗 Fichier final : output/[titre]-ONEFILE.html

Souhaitez-vous :
1. Ouvrir le fichier pour vérification
2. Modifier le contenu
3. Changer le style/univers
```

## Gestion des cas particuliers

### LaTeX avec packages non standards

Si le document source utilise des commandes spécifiques :
1. Identifier les commandes personnalisées
2. Proposer une traduction ou demander clarification
3. Documenter les choix dans un commentaire HTML

### PDF avec formules en images

1. Utiliser OCR pour extraire le texte
2. Identifier les formules et les réécrire en LaTeX
3. Demander validation pour les formules complexes

### Contenu sans structure claire

1. Proposer une structure pédagogique
2. Identifier les blocs selon le contenu (définitions, exemples...)
3. Demander confirmation avant transformation

## Skills utilisés

- `html-katex-compiler` : Initialisation, édition et compilation
- `pdf` : Lecture de PDF si nécessaire

## Différences avec /adaptTex

| Aspect | /adaptTex | /adaptHtml |
|--------|-----------|------------|
| Format cible | LaTeX (bfcours) | HTML/KaTeX |
| Interactivité | Non | Oui (univers, dark mode) |
| Usage typique | Documents imprimés | Projection, web |
