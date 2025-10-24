# Guide de Référence - Scripts de Compilation LaTeX

Ce guide détaille l'utilisation des scripts de compilation selon vos préférences.

## Scripts Principaux (Les 3 Essentiels)

### 1. quick_compile.py - SCRIPT LE PLUS UTILISÉ

**Quand l'utiliser** : 99% du temps, pour tous vos documents bfcours

**Syntaxe de base** :
```bash
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "chemin/vers/fichier.tex"
```

**Arguments** :
- `--file` (OBLIGATOIRE) : Chemin vers le fichier .tex
- `--passes` (optionnel) : Nombre de passes (défaut: 1)

**Exemples** :
```bash
# Compilation standard (1 passe)
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "1. Cours/1ere_spe/mon_cours.tex"

# Compilation avec 2 passes
python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "Evaluations/DS01.tex" --passes 2
```

**Comportement** :
- Utilise LuaLaTeX avec shell-escape (profil Reims)
- Nettoie automatiquement les fichiers auxiliaires
- Affiche les erreurs principales si échec
- Retourne JSON avec le statut

**Sortie JSON** :
```json
{
  "status": "success|error",
  "message": "Compilation réussie|échouée",
  "pdf_generated": true|false,
  "pdf_path": "chemin/vers/fichier.pdf"
}
```

---

### 2. compile_document.py - Pour profils spécifiques

**Quand l'utiliser** : Si vous avez besoin d'un profil particulier (pdflatex, passes multiples)

**Syntaxe de base** :
```bash
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "chemin/vers/fichier.tex"
```

**Arguments** :
- `--file` (OBLIGATOIRE) : Chemin vers le fichier .tex
- `--type` (optionnel) : Profil de compilation (défaut: lualatex_reims_favorite)
  - `lualatex_reims_favorite` : LuaLaTeX 1 passe (RECOMMANDÉ)
  - `simple` : pdflatex 2 passes
  - `standard` : pdflatex 3 passes
  - `complete` : pdflatex 3 passes
- `--no-clean` (optionnel) : Ne pas nettoyer les fichiers auxiliaires

**Exemples** :
```bash
# Profil par défaut (lualatex_reims_favorite)
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "mon_document.tex"

# Profil simple (pdflatex 2 passes)
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "mon_document.tex" --type "simple"

# Profil standard sans nettoyage
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "mon_document.tex" --type "standard" --no-clean
```

**Sortie JSON** :
```json
{
  "status": "success|error",
  "message": "Compilation réussie|échouée",
  "compilation_type": "lualatex_reims_favorite",
  "pdf_generated": true|false,
  "pdf_path": "chemin/vers/fichier.pdf"
}
```

---

### 3. clean_build_files.py - Nettoyage

**Quand l'utiliser** : Nettoyer un répertoire après compilation ou pour résoudre des problèmes

**Syntaxe de base** :
```bash
python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "chemin/vers/repertoire"
```

**Arguments** :
- `--directory` (OBLIGATOIRE) : Répertoire à nettoyer
- `--extensions` (optionnel) : Extensions spécifiques à supprimer

**Exemples** :
```bash
# Nettoyage standard (toutes les extensions par défaut)
python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "1. Cours/1ere_spe/Sequence-Vecteurs"

# Nettoyage avec extensions spécifiques
python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "." --extensions ".aux" ".log" ".out"
```

**Extensions nettoyées par défaut** :
`.aux`, `.log`, `.toc`, `.lof`, `.lot`, `.out`, `.bbl`, `.blg`, `.synctex.gz`, `.fls`, `.fdb_latexmk`, `.nav`, `.snm`, `.vrb`

**Sortie JSON** :
```json
{
  "status": "success",
  "directory": "chemin/vers/repertoire",
  "cleaned_files": ["fichier1.aux", "fichier2.log", ...],
  "count": 5
}
```

---

## Workflows Recommandés

### Workflow Standard (99% des cas)

1. **Compiler** :
   ```bash
   python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "mon_document.tex"
   ```

2. **Si échec** : Les erreurs principales sont affichées automatiquement
   - Corriger les erreurs dans le fichier .tex
   - Relancer la compilation

3. **Si succès** : Le PDF est généré et les fichiers auxiliaires sont nettoyés

### Workflow avec Erreurs Persistantes

1. **Essayer avec plus de passes** :
   ```bash
   python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "mon_document.tex" --passes 2
   ```

2. **Si toujours en échec** : Nettoyer et recommencer
   ```bash
   python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "chemin/vers/repertoire"
   python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "mon_document.tex"
   ```

### Workflow avec Profil Spécifique

Si vous avez besoin de pdflatex au lieu de lualatex :

```bash
python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "mon_document.tex" --type "simple"
```

---

## Gestion des Erreurs

### Erreurs Affichées

En cas d'échec, les scripts affichent :

```
❌ Compilation échouée

📋 Erreurs principales:
   Ligne 42: Undefined control sequence
   Ligne 58: Missing $ inserted

💡 Pour déboguer, lancez:
   python ".claude/skills/tex-compiling-skill/scripts/analyze_latex_log.py" --log "fichier.log"
```

### Tolérance aux Erreurs

Les scripts implémentent une tolérance intelligente :
- Si un PDF est généré malgré un code retour d'erreur, la compilation continue
- Particulièrement utile avec bfcours qui génère des erreurs sur la première passe
- Les erreurs sont affichées mais ne bloquent pas si le PDF existe

---

## Résumé Rapide

| Script | Usage Principal | Commande Typique |
|--------|----------------|------------------|
| `quick_compile.py` | 99% des compilations | `python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "fichier.tex"` |
| `compile_document.py` | Profils spécifiques | `python ".claude/skills/tex-compiling-skill/scripts/compile_document.py" --file "fichier.tex" --type "simple"` |
| `clean_build_files.py` | Nettoyage | `python ".claude/skills/tex-compiling-skill/scripts/clean_build_files.py" --directory "."` |

---

## Préférences de Compilation

Selon vos préférences configurées :

- **Compilateur recommandé** : LuaLaTeX
- **Arguments par défaut** : `-synctex=1 -interaction=nonstopmode -file-line-error -shell-escape`
- **Profil par défaut** : `lualatex_reims_favorite`
- **Nettoyage automatique** : Oui
- **Timeout** : 120 secondes

---

## Notes Importantes

1. **Chemins avec espaces** : Toujours mettre entre guillemets
   ```bash
   # Correct
   python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "1. Cours/mon cours.tex"

   # Incorrect
   python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file 1. Cours/mon cours.tex
   ```

2. **Chemins relatifs** : Depuis le répertoire de travail actuel
   ```bash
   # Depuis le répertoire racine
   python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "1. Cours/1ere_spe/mon_cours.tex"
   ```

3. **Sortie JSON** : Toujours sur stdout, les messages informatifs sur stderr
   - Permet aux agents de parser le résultat facilement
   - Les humains voient les messages colorés sur stderr

4. **Fichiers auxiliaires** : Nettoyés automatiquement par défaut
   - Utiliser `--no-clean` pour les conserver
   - Utile pour le débogage ou si vous utilisez des outils externes

5. **Passes multiples** : Certains documents nécessitent plusieurs passes
   - Tables des matières : 2-3 passes
   - Références croisées : 2-3 passes
   - Documents bfcours : Souvent 1 passe suffit grâce à la tolérance

---

## Règles d'Utilisation

1. **TOUJOURS** utiliser `quick_compile.py` pour les compilations courantes
2. **TOUJOURS** utiliser le profil `lualatex_reims_favorite` (par défaut)
3. **TOUJOURS** vérifier que le PDF est généré même si des erreurs sont signalées
4. **TOLÉRER** les erreurs de setup sur les premières passes (bfcours)
5. **NETTOYER** avec `clean_build_files.py` en cas de problèmes persistants
6. Ne **JAMAIS** utiliser directement `lualatex` ou `pdflatex` en ligne de commande, toujours passer par les scripts

---

## Profils Recommandés Selon le Contexte

- **Documents standard (cours, devoirs, exercices)** : `lualatex_reims_favorite` (par défaut)
- **Documents simples sans packages complexes** : `simple`
- **Documents avec table des matières** : `standard`
- **Documents avec bibliographie** : Créer un profil personnalisé si nécessaire
