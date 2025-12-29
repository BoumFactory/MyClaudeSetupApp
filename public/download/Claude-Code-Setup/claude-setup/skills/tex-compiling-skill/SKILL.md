---
name: tex-compiling-skill
description: Skill spécialisé pour la compilation de documents LaTeX. Gère la compilation avec différents moteurs (pdflatex, lualatex, xelatex), l'analyse des erreurs de compilation, la configuration des compilateurs et le nettoyage des fichiers auxiliaires. Utiliser pour compiler des documents LaTeX et diagnostiquer les erreurs de compilation.
---

# LaTeX Compilation Expert

Système expert pour la compilation de documents LaTeX avec gestion des erreurs et support multi-compilateurs.

## Scripts Principaux

### 1. quick_compile.py - Compilation rapide (RECOMMANDÉ)

**Usage le plus courant** - Pour 99% des documents :

```bash
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "chemin/vers/fichier.tex"
```

**Avec plusieurs passes** :

```bash
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "chemin/vers/fichier.tex" --passes 2
```

- Utilise LuaLaTeX avec shell-escape (profil Reims)
- 1 passe par défaut
- Nettoie automatiquement les fichiers auxiliaires
- Retourne JSON avec le statut de compilation

### 2. compile_document.py - Compilation avec profils

**Pour choisir un profil spécifique** :

```bash
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "chemin/vers/fichier.tex"
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "chemin/vers/fichier.tex" --type "simple"
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "chemin/vers/fichier.tex" --type "standard"
```

**Profils disponibles** :
- `lualatex_reims_favorite` (par défaut) : LuaLaTeX 1 passe
- `simple` : pdflatex 2 passes
- `standard` : pdflatex 3 passes
- `complete` : pdflatex 3 passes

**Options** :
- `--no-clean` : Ne pas nettoyer les fichiers auxiliaires

### 3. clean_build_files.py - Nettoyage

**Pour nettoyer un répertoire** :

```bash
python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "chemin/vers/repertoire"
```

**Nettoyer avec extensions spécifiques** :

```bash
python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "." --extensions ".aux" ".log"
```

Extensions nettoyées par défaut : `.aux`, `.log`, `.toc`, `.lof`, `.lot`, `.out`, `.bbl`, `.blg`, `.synctex.gz`, `.fls`, `.fdb_latexmk`, `.nav`, `.snm`, `.vrb`

## Workflow de Compilation

### Cas standard (99% du temps)

1. Compiler :
```bash
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "mon_document.tex"
```

2. Si échec, les erreurs principales sont affichées automatiquement

### Cas avec erreurs persistantes

1. Compiler avec plus de passes :
```bash
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "mon_document.tex" --passes 2
```

2. Si toujours en échec, analyser les erreurs manuellement dans le fichier `.log`

### Cas avec profil spécifique

1. Utiliser `compile_document.py` avec le profil souhaité :
```bash
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "mon_document.tex" --type "standard"
```

## Logique de Tolérance aux Erreurs

Les scripts implémentent une tolérance intelligente :
- Si un PDF est généré malgré un code retour d'erreur, la compilation continue
- Utile pour les erreurs bfcours qui se résolvent aux passes suivantes
- Les erreurs sont toujours affichées mais ne bloquent pas si le PDF existe

## Sortie JSON

Tous les scripts retournent du JSON sur stdout :

**Succès** :
```json
{
  "status": "success",
  "message": "Compilation réussie",
  "pdf_generated": true,
  "pdf_path": "chemin/vers/fichier.pdf"
}
```

**Échec** :
```json
{
  "status": "error",
  "message": "Compilation échouée",
  "pdf_generated": false
}
```

## Messages d'Erreur Informatifs

En cas d'erreur, les scripts affichent :
1. Les erreurs principales avec numéros de ligne
2. Les commandes suggérées pour déboguer
3. L'usage correct si mauvais arguments

Exemple :
```
❌ Compilation échouée

📋 Erreurs principales:
   Ligne 42: Undefined control sequence
   Ligne 58: Missing $ inserted

💡 Pour déboguer, lancez:
   python ".claude/skills/tex-compiling-skill/scripts/analyze_latex_log.py" --log "fichier.log"
```

## Bonnes Pratiques : Maintenir CLAUDE.md à jour

**RÈGLE IMPORTANTE** : Après chaque compilation réussie, mettre à jour le fichier CLAUDE.md du projet.

### Pourquoi maintenir CLAUDE.md ?

Le fichier `CLAUDE.md` sert de **journal de bord** du projet. Les agents suivants ont besoin de savoir :
- L'état actuel du document (compile ou pas)
- Les erreurs rencontrées et comment elles ont été résolues
- Les modifications apportées depuis la création
- Le nombre de passes nécessaires à la compilation
- Les éventuels problèmes connus

### Quand mettre à jour CLAUDE.md ?

**Après chaque opération majeure** :
- ✅ Compilation réussie → Ajouter statut de compilation et date
- ✅ Correction d'erreurs → Documenter les erreurs et solutions
- ✅ Modification du contenu → Noter les changements apportés
- ✅ Changement de structure → Mettre à jour la structure de fichiers

### Comment mettre à jour CLAUDE.md ?

Utiliser l'outil **Edit** pour ajouter/modifier les sections pertinentes :

```markdown
## État de compilation

- **Dernière compilation réussie** : 2025-10-26 15:30
- **Compilateur utilisé** : LuaLaTeX (lualatex_reims_favorite)
- **Nombre de passes** : 1
- **PDF généré** : ✅ Oui

## Modifications récentes

- 2025-10-26 : Création du document
- 2025-10-26 : Ajout de 3 exercices sur les vecteurs
- 2025-10-26 : Correction d'une erreur de syntaxe ligne 42

## Problèmes résolus

- Erreur "Undefined control sequence" ligne 42 → Corrigé : \acc au lieu de \textbf

## Notes pour les agents suivants

- Le document utilise le package siunitx
- Les figures TikZ sont dans enonce_figures.tex
- Attention : le thème utilise des couleurs personnalisées
```

### Exemple de workflow complet

1. **Compiler le document** :
   ```bash
   python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "mon_cours.tex"
   ```

2. **Si compilation réussie** → Mettre à jour CLAUDE.md avec :
   - Date et heure de compilation
   - Statut : ✅ Compilation réussie
   - PDF généré avec succès

3. **Si compilation échouée** → Mettre à jour CLAUDE.md avec :
   - Erreurs rencontrées
   - Solutions tentées
   - Statut actuel

4. **Après modifications** → Documenter les changements dans CLAUDE.md

Cette pratique permet aux agents suivants de reprendre le travail efficacement sans répéter les mêmes erreurs.

## Rappels Importants

- **TOUJOURS** utiliser `quick_compile.py` sauf besoin spécifique
- **TOUJOURS** mettre à jour CLAUDE.md après compilation réussie
- Les chemins de fichiers doivent être entre guillemets si espaces
- Tous les scripts sont dans `.claude/skills/tex-compiling-skill/scripts/`
- Les scripts nettoient automatiquement les fichiers auxiliaires (sauf `--no-clean`)
- Le profil `lualatex_reims_favorite` est recommandé pour les documents bfcours
