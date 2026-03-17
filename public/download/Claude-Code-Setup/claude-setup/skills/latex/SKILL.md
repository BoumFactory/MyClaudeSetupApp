---
name: latex
description: Skill orchestrateur pour la production complète de documents LaTeX éducatifs. Chaîne automatiquement 3 skills spécialisés : tex-document-creator (structure), bfcours-latex (contenu), tex-compiling-skill (compilation). Utiliser quand l'utilisateur demande de créer un cours, une évaluation, une fiche ou un exercice LaTeX complet. Le résultat est un PDF prêt à imprimer.
---

# LaTeX — Orchestrateur de production complète

Skill qui chaîne 3 skills spécialisés pour produire un document LaTeX éducatif complet, du dossier vide au PDF compilé.

## Workflow en 3 étapes

### Étape 0 : Se documenter

#### Cas de reproduction de contenu  (pdf2tikz)

Extraire les contenus texte et svg du document, quelle que soit sa nature. 

**Important** Utilise obligatoirement le skill `pdf2tikz` : il permet d'obtenir la plupart des informations pour reproduire les figures tikz, extraire les images, etc.

#### Cas de création de contenu

Utiliser le skill `programmes-officiels` pour déterminer les attendus du BO concernant le document à produire.

### Étape 1 : Créer la structure (tex-document-creator)

Utiliser le skill `tex-document-creator` pour initialiser le projet :
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

Utiliser le skill `bfcours-latex` pour rédiger le contenu éducatif :
- Cours structuré avec les environnements bfcours
- Exercices adaptés au niveau demandé
- Conformité aux programmes officiels
- Notation et conventions mathématiques correctes

**IMPORTANT** : Le skill bfcours-latex connaît toutes les commandes et environnements du package. Il produit du contenu pédagogiquement adapté au niveau (6ème → Terminale).

### Étape 3 : Compiler (tex-compiling-skill)

Utiliser le skill `tex-compiling-skill` pour compiler le document :

```bash
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "chemin/vers/fichier.tex"
```

- Compilation LuaLaTeX avec shell-escape
- Analyse automatique des erreurs
- Nettoyage des fichiers auxiliaires
- PDF prêt à imprimer

## Règles

1. **Toujours suivre l'ordre** : structure → contenu → compilation
2. **Ne jamais sauter d'étape** : même pour un petit fichier, utiliser le workflow complet
3. **En cas d'erreur de compilation** : le skill tex-compiling-skill analyse le log et propose des corrections. Corriger puis recompiler.
4. **Demander le niveau** si l'utilisateur ne l'a pas précisé (6ème, 5ème, 4ème, 3ème, 2nde, 1ère, Terminale)

## Exemples d'utilisation

**Utilisateur** : "Fais-moi un cours sur les fractions en 6ème"
1. tex-document-creator → crée `Fractions/cours_fractions.tex`
2. bfcours-latex → remplit avec définitions, propriétés, exemples, exercices niveau 6ème
3. tex-compiling-skill → compile → `cours_fractions.pdf`

**Utilisateur** : "Une évaluation sur Pythagore en 4ème"
1. tex-document-creator → crée `Pythagore/eval_pythagore.tex` (type évaluation)
2. bfcours-latex → exercices progressifs, barème, présentation soignée
3. tex-compiling-skill → compile → `eval_pythagore.pdf`
