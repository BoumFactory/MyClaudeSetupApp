---
name: latex
description: Skill pour la production de documents LaTeX. Enchaînement obligatoire des skills latex documents standardisés (création, rédaction, compilation, review visuelle).
---

# LaTeX — Orchestrateur de production complète

Skill qui chaîne les skills spécialisés pour produire un document LaTeX éducatif complet, du dossier vide au PDF compilé puis optimisé visuellement.
`pdf2tikz` pour reprendre les figures d'un PDF source, tex-document-creator pour créer l'archive, bfcours-latex pour implémenter, tex-compiling-skill pour compiler, et latex-visual-review pour optimiser la disposition.

## Workflow en 4 étapes

### Étape 0 : Se documenter

#### Cas de reproduction de contenu depuis un PDF

Quand la source est un PDF contenant des figures, invoquer le skill `pdf2tikz` avant la rédaction, pour ne pas approximer un graphique à partir de la lecture visuelle du PDF.

Le skill `pdf2tikz` :
1. Extrait les chemins vectoriels SVG de chaque page (courbes, axes, grilles, points)
2. Analyse la disposition (layout) : positions, dimensions, espacements
3. Produit du code TikZ fidèle aux figures originales (coordonnées exactes, styles)
4. Extrait les images raster si présentes

**Workflow pour chaque figure du PDF source** :
1. Appeler `pdf2tikz` sur la ou les pages contenant des figures
2. Récupérer le code TikZ généré
3. L'intégrer dans le document bfcours en l'adaptant au style (couleurs, labels)
4. Ne modifier les coordonnées que si un changement de repère est nécessaire

Sans extraction vectorielle, les graphiques risquent d'être approximatifs.

#### Cas de création de contenu

Utiliser le skill `programmes-officiels` pour déterminer les attendus du BO concernant le document à produire.

### Étape 1 : Créer la structure (tex-document-creator)

Utiliser le skill /tex-document-creator pour initialiser le projet :
- Créer le dossier et la structure de fichiers
- Générer le .tex avec le préambule bfcours adapté
- Configurer le type de document (cours, évaluation, fiche, activité, DM)

**IMPORTANT** : Lire impérativement la référence du skill :
`.claude/skills/tex-document-creator/references/scripts_to_use.md`

Les scripts Python du skill gèrent automatiquement :
- La structure de dossiers
- Le préambule LaTeX avec les bons packages
- Les métadonnées (titre, niveau, thème)

### Étape 2 : Remplir le contenu (bfcours-latex)

Utiliser le skill /bfcours-latex pour rédiger le contenu éducatif :
- Cours structuré avec les environnements bfcours
- Exercices adaptés au niveau demandé
- Conformité aux programmes officiels
- Notation et conventions mathématiques correctes

**IMPORTANT** : Le skill bfcours-latex connaît toutes les commandes et environnements du package. Il produit du contenu pédagogiquement adapté au niveau (6ème → Terminale).

### Étape 3 : Compiler (tex-compiling-skill)

Utiliser le skill /tex-compiling-skill` pour compiler le document :

```bash
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "chemin/vers/fichier.tex"
```

- Compilation LuaLaTeX avec shell-escape
- Analyse automatique des erreurs
- Nettoyage des fichiers auxiliaires
- PDF prêt à imprimer

### Étape 4 : Review visuelle et optimisation (latex-visual-review)

**OBLIGATOIRE pour tout document non-trivial** : Une fois la première compilation réussie, appliquer le skill `latex-visual-review` pour :

- Capturer le PDF en images PNG (page par page)
- Mesurer la densité, les blancs, les déséquilibres de mise en page
- Détecter les chevauchements (badges de points sur texte, encadrés qui débordent, etc.)
- Distinguer les zones à compacter (énoncés, cours) des zones à laisser aérées (corrections projetées, espaces de réponse)
- Proposer puis appliquer des optimisations ciblées (colonnage, ajustements `\tcbitempoint[xshift][yshift]`, MultiColonnes, etc.)
- Boucle adversariale avec rollback automatique si la modification dégrade le rendu ou casse la compilation

**Quand l'utiliser systématiquement** :
- Après la première compilation d'une évaluation, fiche d'exercices, cours
- Dès que l'utilisateur signale un problème de disposition, chevauchement, ou trop-plein de pages
- Pour densifier un document trop aéré ou aérer un document trop dense

**Quand sauter cette étape** :
- Pour un brouillon ultra-court (< 1 page)
- Pour une correction immédiate déjà identifiée et localisée (utiliser Edit directement)

## Règles

1. **Toujours suivre l'ordre** : structure → contenu → compilation → review visuelle
2. **Ne jamais sauter d'étape** : même pour un petit fichier, utiliser le workflow complet
3. **En cas d'erreur de compilation** : le skill tex-compiling-skill analyse le log et propose des corrections. Corriger puis recompiler.
4. **Demander le niveau** si l'utilisateur ne l'a pas précisé (6ème, 5ème, 4ème, 3ème, 2nde, 1ère, Terminale)
5. **La review visuelle est partie intégrante du workflow** : un document non revu visuellement est un document non terminé.

## Exemples d'utilisation

**Utilisateur** : "Fais-moi un cours sur les fractions en 6ème"
1. tex-document-creator → crée `Fractions/cours_fractions.tex`
2. bfcours-latex → remplit avec définitions, propriétés, exemples, exercices niveau 6ème
3. tex-compiling-skill → compile → `cours_fractions.pdf`
4. latex-visual-review → capture, mesure, optimise → PDF final

**Utilisateur** : "Une évaluation sur Pythagore en 4ème"
1. tex-document-creator → crée `Pythagore/eval_pythagore.tex` (type évaluation)
2. bfcours-latex → exercices progressifs, barème, présentation soignée
3. tex-compiling-skill → compile → `eval_pythagore.pdf`
4. latex-visual-review → vérifie qu'aucun badge de points ne chevauche le texte, que les zones réponses sont suffisamment aérées, que le sujet tient bien sur le nombre de pages prévu
