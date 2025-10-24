# Système complet de création de diaporamas Beamer

## Vue d'ensemble

Ce système fournit une solution **complète et autonome** pour créer des diaporamas Beamer de haute qualité, adaptés au contexte éducatif ou académique.

## Composants du système

### 1. Skill : beamer-presentation

**Localisation** : `.claude/skills/beamer-presentation/`

**Description** : Expertise complète en création de diaporamas Beamer pédagogiques.

**Contenu** :

```
beamer-presentation/
├── SKILL.md                                    # Skill principal
├── README.md                                   # Ce fichier
└── references/                                 # Guides de référence
    ├── beamer-best-practices.md               # Bonnes pratiques d'espacement et densité
    ├── beamer-styles-guide.md                 # Guide des 3 styles (collège, lycée, académique)
    ├── exercices-beamer.md                    # Création d'exercices avec estimation de temps
    └── workflow-compilation-verification.md    # Workflow complet de compilation et vérification
```

**Fonctionnalités** :

- Règle d'or : **Jamais plus de 70% de slide remplie** (60% pour collège)
- Gestion de l'espace et des marges
- Animations et overlays progressifs
- Alternance question/réponse pédagogique
- Exercices avec environnement `exobeamer` et estimation de temps
- Trois styles distincts adaptés aux publics

### 2. Templates Beamer

**Localisation** : `.claude/datas/latex-modeles/beamer/`

**Templates disponibles** :

1. **template-college.tex**
   - Public : 6e à 3e (11-15 ans)
   - Police : 14pt (titres 20pt)
   - Couleurs : Vives (bleu, orange, rouge, vert)
   - Densité max : 60%
   - Animations : Fréquentes
   - Items/slide : 5 max

2. **template-lycee.tex**
   - Public : 2nde à Terminale (15-18 ans)
   - Police : 12pt (titres 16-18pt)
   - Couleurs : Équilibrées (bleu marine, bordeaux)
   - Densité max : 70%
   - Animations : Modérées
   - Items/slide : 6-7 max

3. **template-academique.tex**
   - Public : Conférences, colloques, séminaires
   - Police : 11pt (titres 14-16pt)
   - Couleurs : Sobres (noir, gris)
   - Format : 16:9
   - Densité max : 70%
   - Animations : Rares
   - Références bibliographiques

**Champs personnalisables** dans les templates :

```latex
{{TITRE_PRESENTATION}}
{{SOUS_TITRE}}
{{AUTEUR}}
{{DATE}}
{{ETABLISSEMENT}}
{{TITRE_COURT}}       % Pour en-tête (lycée/académique)
{{AUTEUR_COURT}}      % Pour en-tête (lycée/académique)
```

### 3. Agent : beamer-worker

**Localisation** : `.claude/agents/beamer-worker.md`

**Modèle** : `claude-haiku-4-5-20251001` (rapide et économique)

**Description** : Agent autonome spécialisé dans la création de diaporamas Beamer.

**Skills utilisés** :

1. **beamer-presentation** : Expertise Beamer
2. **tex-compiling-skill** : Compilation LuaLaTeX
3. **pdf** : Extraction et vérification visuelle des frames

**Workflow automatique** :

```
1. Analyse de la demande (style, sujet, durée)
   ↓
2. Lecture des guides de référence
   ↓
3. Création du contenu (structure, exercices, alternance Q/R)
   ↓
4. Compilation avec tex-compiling-skill
   ↓
5. Extraction des frames avec skill pdf
   ↓
6. Vérification visuelle de chaque frame
   ↓
7. Correction des bugs visuels détectés
   ↓
8. Nettoyage des fichiers temporaires
   ↓
9. Rapport final
```

**Autonomie** : Totale. Pas d'intervention utilisateur nécessaire.

### 4. Commande slash : /createBeamer

**Localisation** : `.claude/commands/createBeamer.md`

**Syntaxe** :

```bash
/createBeamer [--style <collège|lycée|académique>] \
              --sujet "<sujet>" \
              --duree <minutes> \
              [--output <chemin>] \
              [--exercices <nombre>] \
              [--auteur "<nom>"] \
              [--etablissement "<nom>"]
```

**Fonctionnement** :

1. Lance l'agent `beamer-worker`
2. Transmet les paramètres
3. L'agent exécute le workflow complet
4. Produit un PDF prêt à l'emploi

**Détection automatique du style** (si non spécifié) :

- Mots-clés collège : "6e", "5e", "4e", "3e", "collège"
- Mots-clés lycée : "2nde", "1ère", "Tale", "lycée"
- Mots-clés académique : "analyse", "théorème", "conférence", "séminaire"

## Utilisation

### Exemple simple

```bash
/createBeamer --sujet "Théorème de Pythagore" --duree 30
```

**Résultat** :

- Style détecté automatiquement : collège
- 15 slides créées
- 2 exercices intégrés avec estimation de temps
- Compilation + vérification automatique
- PDF prêt : `presentation.pdf`

### Exemple détaillé

```bash
/createBeamer --style lycée \
              --sujet "Dérivation des fonctions polynomiales" \
              --duree 55 \
              --exercices 4 \
              --auteur "M. Dupont" \
              --etablissement "Lycée Eugène Belgrand"
```

**Résultat** :

- Template lycée (12pt, bleu marine/bordeaux)
- 25 slides structurées
- 4 exercices avec temps estimé (5 min, 8 min, 5 min, 10 min)
- Métadonnées complétées
- Compilation + vérification exhaustive
- PDF prêt : `presentation.pdf`

## Processus de vérification visuelle

### 1. Extraction des frames

Le skill `pdf` extrait chaque page du PDF Beamer en image PNG :

```python
extract_pages_as_images(
    pdf_path="presentation.pdf",
    output_dir="./verification_frames/",
    dpi=150
)
```

### 2. Vérification de chaque frame

L'agent **lit visuellement** chaque image PNG et vérifie :

- ✅ Densité < seuil (60% collège, 70% lycée/académique)
- ✅ Police ≥ taille minimale
- ✅ Contraste suffisant
- ✅ Formules mathématiques complètes (pas tronquées)
- ✅ Graphiques entiers (pas de partie coupée)
- ✅ Couleurs cohérentes

### 3. Correction des bugs

Pour chaque bug détecté :

1. Identifier la frame problématique (numéro de page)
2. Localiser le code LaTeX correspondant
3. Appliquer la correction appropriée
4. Recompiler
5. Réextraire les frames
6. Vérifier la correction

**Bugs fréquents et corrections** :

| Bug | Correction |
|-----|------------|
| Slide > 70% remplie | Découper en 2 slides |
| Formule trop longue | Utiliser `multline` ou `align` |
| Texte illisible | Augmenter police ou réduire contenu |
| Graphique coupé | Réduire échelle (`scale=0.8`) |
| Contraste insuffisant | Changer couleur |

### 4. Nettoyage

Après validation :

```bash
# Supprimer les frames extraites
rm -rf ./verification_frames/

# Nettoyer fichiers de compilation
rm presentation.aux presentation.log ...
```

**Fichier final** : Seul `presentation.pdf` est conservé.

## Environnement exobeamer

Environnement personnalisé pour exercices avec :

- **Estimation du temps** : "Estimation : X min"
- **Difficulté** : ★☆☆, ★★☆, ★★★
- **Zone modifiable** : "Temps réel : ___" (pour le professeur)

**Syntaxe** :

```latex
\begin{exobeamer}[Estimation : 5 min | Difficulté : ★☆☆]
  \textbf{Énoncé :}

  Calculer la dérivée de $f(x) = x^2 + 3x$.

  \pause

  \textbf{Solution :}

  \uncover<2->{$f'(x) = 2x + 3$}
\end{exobeamer}
```

**Rendu** : Boîte colorée avec titre "Exercice", estimation en haut à gauche, zone de notes en haut à droite.

## Règles de densité

### Collège

- **Maximum 60% de remplissage**
- 5 items maximum par slide
- 8 lignes de texte maximum
- Police 14pt minimum

**Justification** : Attention limitée, besoin d'espace visuel important.

### Lycée

- **Maximum 70% de remplissage**
- 6-7 items maximum par slide
- 10-12 lignes de texte maximum
- Police 12pt minimum

**Justification** : Équilibre entre densité d'information et lisibilité.

### Académique

- **Maximum 70% de remplissage**
- 7 items maximum par slide
- 12-14 lignes de texte maximum
- Police 11pt minimum

**Justification** : Public expert, densité maîtrisée acceptable.

## Alternance question/réponse

**Principe pédagogique** : Chaque notion doit être suivie d'une vérification.

**Pattern recommandé** :

```
Slides 1-3 : Introduction de la notion
Slide 4    : Question aux élèves
Slide 5    : Réponse révélée progressivement
Slides 6-8 : Approfondissement
Slide 9    : Nouvelle question
Slide 10   : Réponse
```

**Exemples de révélation progressive** :

```latex
% Pause simple
\begin{frame}{Question}
  Calculer : $3 \times 7 = ?$

  \pause

  \textbf{Réponse :} $21$
\end{frame}

% Révélation par étapes
\begin{frame}{Résolution}
  Résoudre : $2x + 3 = 7$

  \begin{enumerate}
    \item<2-> Soustraire 3 : $2x = 4$
    \item<3-> Diviser par 2 : $x = 2$
    \item<4-> Vérification : $2 \times 2 + 3 = 7$ ✓
  \end{enumerate}
\end{frame}

% Remplacement dynamique
\begin{frame}{Développement}
  $(x+2)^2 = ?$

  \only<2>{Formule : $(a+b)^2 = a^2 + 2ab + b^2$}

  \only<3>{$(x+2)^2 = x^2 + 4x + 4$}
\end{frame}
```

## Estimation des temps pour exercices

**Guide de référence** (fichier `exercices-beamer.md`) :

| Type d'exercice | Temps collège | Temps lycée | Temps académique |
|-----------------|---------------|-------------|------------------|
| Application directe | 5-7 min | 3-5 min | 2-3 min |
| Exercice à étapes | 8-12 min | 5-8 min | 3-5 min |
| Problème | 15-20 min | 10-15 min | 8-12 min |
| Investigation | 25-30 min | 20-25 min | 15-20 min |

**Facteurs d'ajustement** :

- Première fois : +30%
- Nécessite réflexion : +20%
- Calculs complexes : +20%
- Classe hétérogène : +10%
- Notion connue : -20%
- Exercice routinier : -15%

## Avantages du système

### 1. Autonomie complète

- Pas d'intervention manuelle nécessaire
- L'agent gère tout de bout en bout
- Production rapide (< 5 minutes)

### 2. Qualité garantie

- Vérification visuelle exhaustive
- 0 bug visuel dans le résultat final
- Densité et lisibilité respectées

### 3. Adaptation au contexte

- 3 styles distincts (collège, lycée, académique)
- Exercices adaptés au niveau
- Animations appropriées

### 4. Pédagogie intégrée

- Alternance question/réponse automatique
- Exercices avec estimation de temps
- Révélation progressive du contenu

### 5. Économie de temps

- Création automatique en quelques minutes
- Pas de correction manuelle nécessaire
- Prêt à présenter immédiatement

## Structure des fichiers

```
.claude/
├── skills/
│   └── beamer-presentation/
│       ├── SKILL.md                                    # Skill principal
│       ├── README.md                                   # Cette documentation
│       └── references/
│           ├── beamer-best-practices.md               # Bonnes pratiques
│           ├── beamer-styles-guide.md                 # Guide des styles
│           ├── exercices-beamer.md                    # Exercices
│           └── workflow-compilation-verification.md    # Workflow complet
│
├── datas/
│   └── latex-modeles/
│       └── beamer/
│           ├── template-college.tex                    # Template collège
│           ├── template-lycee.tex                      # Template lycée
│           └── template-academique.tex                 # Template académique
│
├── agents/
│   └── beamer-worker.md                                # Agent autonome
│
└── commands/
    └── createBeamer.md                                 # Commande slash
```

## Prochaines étapes

### Pour utiliser le système

1. **Appeler la commande** :
   ```bash
   /createBeamer --sujet "Votre sujet" --duree 30
   ```

2. **L'agent travaille automatiquement** :
   - Crée le contenu
   - Compile
   - Vérifie visuellement
   - Corrige les bugs
   - Nettoie

3. **Récupérer le PDF** :
   - `presentation.pdf` prêt à l'emploi

### Pour personnaliser

1. **Modifier un template** :
   - Éditer `.claude/datas/latex-modeles/beamer/template-XXX.tex`
   - Changer couleurs, police, logo, etc.

2. **Ajouter un nouveau style** :
   - Créer `template-nouveau.tex`
   - Documenter dans `beamer-styles-guide.md`
   - Mettre à jour l'agent `beamer-worker.md`

## Références

- Documentation Beamer : https://ctan.org/pkg/beamer
- TikZ & PGF : https://ctan.org/pkg/pgf
- Tcolorbox : https://ctan.org/pkg/tcolorbox

---

**Système créé pour générer des diaporamas Beamer de qualité professionnelle en quelques minutes, sans intervention manuelle.**
