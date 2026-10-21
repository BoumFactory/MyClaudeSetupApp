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

**Avec vérification du contenu texte du PDF** (pages, nombre de caractères, via pymupdf) :

```bash
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "chemin/vers/fichier.tex" --verifier-texte
```

- Utilise LuaLaTeX avec shell-escape (profil Reims)
- 1 passe par défaut
- Ne supprime jamais le PDF avant de compiler (l'utilisateur peut être en train de le lire) ; la réussite est déterminée en comparant l'état du PDF avant/après
- Verrouille le dossier le temps de la compilation (voir « Compilation concurrente » plus bas)
- Retourne JSON avec le statut de compilation et l'analyse complète du `.log`

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

## Logique de Vérification de Réussite

`quick_compile.py` ne se fie plus jamais à la seule présence d'un fichier PDF sur le disque (un vieux PDF périmé y reste toujours présent puisque le script ne le supprime jamais avant de compiler). Trois statuts distincts sont possibles :

- **`success`** : le PDF a été réécrit par CETTE compilation (mtime + taille comparés à l'état d'avant) **ET** le `.log` ne contient aucune ligne `!` ni aucune erreur `fichier:ligne:` **ET** le code retour de la dernière passe est 0.
- **`success_with_errors`** : le PDF a bien été réécrit par cette compilation, mais des erreurs sont présentes dans le `.log` (ou le code retour de la dernière passe est non nul) — **du contenu peut manquer**, ne jamais considérer le document terminé dans ce cas sans relire le rendu.
- **`error`** : soit aucun PDF n'a été produit, soit le PDF présent est celui d'AVANT la compilation (non réécrit) — la compilation a réellement échoué, même si un vieux PDF traîne dans le dossier.

Pendant les passes intermédiaires (`--passes 2` ou plus), un code retour non nul n'interrompt pas l'enchaînement : c'est fréquent avec bfcours (références non encore résolues) et cela se corrige souvent à la passe suivante. Seuls l'état du `.log` et le code retour de la **dernière** passe déterminent le statut final. Un échec de lancement (LuaLaTeX introuvable, timeout) interrompt en revanche immédiatement les passes restantes.

## Sortie JSON

Tous les scripts retournent du JSON sur stdout. Pour `quick_compile.py`, le contrat complet est :

**Succès** :
```json
{
  "status": "success",
  "message": "Compilation réussie",
  "pdf_generated": true,
  "pdf_fresh": true,
  "pdf_path": "chemin/vers/fichier.pdf",
  "passes_run": 1,
  "return_codes": [0],
  "errors": [],
  "warnings": []
}
```

**PDF produit malgré des erreurs** (statut intermédiaire, à ne jamais confondre avec un succès) :
```json
{
  "status": "success_with_errors",
  "message": "PDF produit malgré des erreurs signalées dans le .log : du contenu peut manquer, vérifier le rendu avant de considérer le document terminé",
  "pdf_generated": true,
  "pdf_fresh": true,
  "pdf_path": "chemin/vers/fichier.pdf",
  "return_codes": [1],
  "errors": [{"file": "./enonce.tex", "line": 13, "message": "Undefined control sequence."}],
  "warnings": ["Undefined control sequence : commande LaTeX inconnue (1 occurrence)"]
}
```

**Échec réel** (PDF absent, ou PDF présent mais NON réécrit par cette compilation) :
```json
{
  "status": "error",
  "message": "Compilation échouée : le PDF existant n'a pas été réécrit par cette compilation",
  "pdf_generated": true,
  "pdf_fresh": false,
  "pdf_path": "chemin/vers/fichier.pdf",
  "errors": [{"file": "./Activite_Equation_Coeur.tex", "line": 2, "message": "Emergency stop."}],
  "warnings": ["Emergency stop : la compilation s'est interrompue brutalement (1 occurrence)"]
}
```

**Champs additionnels** :
- `pdf_fresh` (bool) : le PDF a bien été réécrit par CETTE compilation (comparaison mtime + taille avant/après). C'est ce champ, et non `pdf_generated`, qu'il faut lire pour savoir si la compilation a réellement produit quelque chose de nouveau.
- `errors` : TOUTES les erreurs du `.log` — celles au format `fichier:ligne: message` (`-file-line-error`, quel que soit le fichier : `.tex`, `.sty`, `.cls`) avec `file`/`line` renseignés, et les autres lignes `! message` sans position connue (`file`/`line` alors à `null`).
- `warnings` : motifs d'échec muet détectés dans le `.log` (voir section dédiée ci-dessous).
- `text_check` (présent seulement avec `--verifier-texte`) : `{"available": true, "pages": N, "chars": N, "has_text": bool}`.

Les clés historiques (`status`, `message`, `pdf_generated`, `pdf_path`) restent toujours présentes : les agents qui ne lisent que ces champs continuent de fonctionner sans modification.

## Messages d'Erreur Informatifs

En cas d'erreur, les scripts affichent :
1. Les erreurs principales avec numéros de ligne
2. Les commandes suggérées pour déboguer
3. L'usage correct si mauvais arguments

Exemple :
```
❌ Compilation échouée

📋 Erreurs (fichier:ligne quand disponible):
   ./enonce.tex:42: Undefined control sequence.
   ./enonce.tex:58: Missing $ inserted.

💡 Pour déboguer, lancez:
   python ".claude/skills/tex-compiling-skill/scripts/analyze_latex_log.py" --log "fichier.log"
```

## Détection des échecs muets

Certains défauts ne provoquent aucune erreur fatale mais font disparaître du contenu du PDF **sans avertissement explicite**. `quick_compile.py` analyse systématiquement le `.log` (plus seulement en cas d'échec) et remonte dans `warnings` :

- `\vsplit needs a \vbox` / `Incompatible list can't be unboxed` — un tableau ou bloc tcolorbox non sécable a été rogné, les derniers items ont disparu.
- `Package tcolorbox Warning: ... upper box part has become overfull` — un raster (`tcbenumerate`) déborde, du contenu est tronqué.
- `Emergency stop`, `Missing $ inserted`, `Undefined control sequence`, `Paragraph ended before` — signalés même quand ils n'interrompent pas la compilation jusqu'à `\end{document}`.

Deux défauts classiques restent **invisibles dans le `.log`** par nature et ne peuvent pas être détectés par une regex :
- du texte qui déborde d'une tcolorbox sans déclencher d'`Overfull \hbox` ;
- un marqueur de gabarit resté en commentaire (document rendu presque vide).

Pour ces deux cas, utiliser `--verifier-texte` (nombre de pages/caractères anormalement bas = signal d'alerte) et, pour tout document non trivial, relire le rendu avec le skill `latex-visual-review` ou un rendu PDF → PNG : **ne jamais considérer un document terminé sur la seule foi du JSON de compilation.**

## Compilation concurrente : un verrou par dossier

**Ne jamais compiler en parallèle deux maîtres d'un même dossier** (ex. `Exercices.tex` et `Exercices_ELEVE.tex`) : ils partagent des fichiers auxiliaires bfcours (`bfpoints_*`, `.comp`, `.voc`, sauvegardes rdexo) qui s'écrasent mutuellement, dégradant silencieusement la mise en page sans la moindre erreur.

`quick_compile.py` pose un verrou `.quick_compile.lock` (PID + horodatage) dans le dossier du fichier compilé, le temps de la compilation :
- une seconde compilation lancée dans le même dossier **attend** la fin de la première (jusqu'à 5 minutes), avec un message d'attente affiché toutes les 10 secondes ;
- au-delà du délai maximal, elle échoue explicitement (`status: "error"`) plutôt que de risquer un écrasement silencieux ;
- un verrou orphelin (processus mort, ou plus vieux que 15 minutes) est détecté et nettoyé automatiquement, sans jamais toucher au processus lui-même.

**Règle pratique** : compiler séquentiellement les maîtres d'un même dossier, jamais en tâches de fond simultanées.

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
- **TOUJOURS** lire `pdf_fresh` et `status` (pas seulement `pdf_generated`) avant d'annoncer une réussite : un vieux PDF périmé reste présent sur le disque même en cas d'échec
- **NE JAMAIS** compiler en parallèle deux maîtres d'un même dossier — compiler séquentiellement (le verrou `.quick_compile.lock` fait attendre automatiquement, mais mieux vaut ne pas y recourir systématiquement)
- Les chemins de fichiers doivent être entre guillemets si espaces
- Tous les scripts sont dans `.claude/skills/tex-compiling-skill/scripts/`
- Les scripts nettoient automatiquement les fichiers auxiliaires (sauf `--no-clean`)
- Le profil `lualatex_reims_favorite` est recommandé pour les documents bfcours
