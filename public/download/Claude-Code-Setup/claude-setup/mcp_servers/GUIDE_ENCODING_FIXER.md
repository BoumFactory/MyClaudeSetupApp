# Guide du Serveur MCP encoding-fixer-server

## 📋 Description

Le serveur MCP `encoding-fixer-server` résout automatiquement les problèmes d'encodage des fichiers LaTeX sous Windows. Il détecte l'encodage actuel d'un fichier et le convertit vers UTF-8 de manière fiable.

## 🎯 Objectif

**Résoudre le problème récurrent** : Quand Claude Code génère du contenu avec des caractères accentués français (é, è, à, ç, etc.), Windows peut mal interpréter l'encodage, ce qui produit des caractères corrompus dans VSCode.

## 🚀 Installation

```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\.claude\mcp_servers"
setup_encoding_fixer_mcp.bat
```

Le script installe automatiquement les dépendances nécessaires (package `mcp`).

## 🔧 Outils Disponibles

### 1. `fix_file_encoding(file_path, output_path="", create_backup=true)`

Corrige l'encodage d'un fichier en le convertissant vers UTF-8.

**Paramètres** :
- `file_path` (string, obligatoire) : Chemin du fichier à corriger
- `output_path` (string, optionnel) : Chemin du fichier de sortie (vide = écrase l'original)
- `create_backup` (bool, optionnel) : Créer une sauvegarde `.backup` (défaut: true)

**Retour** : JSON avec :
```json
{
  "success": true,
  "file": "chemin/vers/fichier.tex",
  "original_encoding": "cp1252",
  "new_encoding": "utf-8",
  "characters_count": 1234,
  "backup_created": true,
  "backup_path": "chemin/vers/fichier.tex.backup"
}
```

**Exemples** :
```python
# Corriger un fichier (avec backup automatique)
fix_file_encoding("cours.tex")

# Corriger sans backup
fix_file_encoding("draft.tex", create_backup=false)

# Corriger vers un nouveau fichier
fix_file_encoding("ancien.tex", output_path="nouveau.tex")
```

---

### 2. `detect_file_encoding(file_path)`

Détecte l'encodage d'un fichier sans le modifier.

**Paramètres** :
- `file_path` (string, obligatoire) : Chemin du fichier à analyser

**Retour** : JSON avec :
```json
{
  "success": true,
  "file": "chemin/vers/fichier.tex",
  "detected_encoding": "cp1252",
  "is_utf8": false,
  "needs_conversion": true,
  "statistics": {
    "total_chars": 1234,
    "lines": 56,
    "accented_chars": 78,
    "invalid_chars": 0
  }
}
```

**Exemple** :
```python
# Analyser l'encodage d'un fichier
detect_file_encoding("cours.tex")
```

---

### 3. `fix_directory_encoding(directory_path, pattern="*.tex", create_backup=true, recursive=false)`

Corrige l'encodage de tous les fichiers correspondant au pattern dans un répertoire.

**Paramètres** :
- `directory_path` (string, obligatoire) : Chemin du répertoire à traiter
- `pattern` (string, optionnel) : Pattern de fichiers (défaut: "*.tex")
- `create_backup` (bool, optionnel) : Créer des backups (défaut: true)
- `recursive` (bool, optionnel) : Traiter les sous-répertoires (défaut: false)

**Retour** : JSON avec :
```json
{
  "success": true,
  "directory": "chemin/vers/dossier",
  "pattern": "*.tex",
  "recursive": false,
  "files_found": 10,
  "files_processed": 10,
  "files_converted": 3,
  "files_already_utf8": 7,
  "files_failed": 0,
  "details": [...]
}
```

**Exemples** :
```python
# Corriger tous les .tex d'un dossier
fix_directory_encoding("./cours/")

# Corriger récursivement tous les .tex et .md
fix_directory_encoding("./projet/", pattern="*.tex", recursive=true)
```

---

### 4. `get_encoding_stats()`

Retourne la liste des encodages supportés par le serveur.

**Retour** : JSON avec :
```json
{
  "supported_encodings": [
    "utf-8",
    "latin-1",
    "iso-8859-1",
    "cp1252",
    "cp850",
    "utf-8-sig"
  ],
  "default_output": "utf-8",
  "description": "Serveur MCP pour la correction automatique d'encodage des fichiers LaTeX"
}
```

---

## 📖 Cas d'Usage Typiques

### Cas 1 : Fichier généré par Claude avec caractères corrompus

**Problème** : Vous ouvrez un fichier `.tex` dans VSCode et vous voyez `Ã©` au lieu de `é`.

**Solution** :
```python
fix_file_encoding("cours_genere.tex")
```

Le fichier sera automatiquement corrigé et une sauvegarde `.backup` sera créée.

---

### Cas 2 : Workflow /adaptTex (OBLIGATOIRE)

**Contexte** : La commande `/adaptTex` transforme un fichier LaTeX vers bfcours.

**Protocole** :
1. Effectuer toutes les transformations
2. **AVANT** de livrer le fichier final :
   ```python
   fix_file_encoding("fichier_modified.tex")
   ```
3. Vérifier que le fichier s'affiche correctement dans VSCode

---

### Cas 3 : Batch processing d'un projet entier

**Problème** : Vous avez récupéré un ancien projet avec des fichiers mal encodés.

**Solution** :
```python
# Corriger tous les fichiers .tex récursivement
fix_directory_encoding("./MonProjet/", pattern="*.tex", recursive=true)
```

---

### Cas 4 : Diagnostic avant correction

**Usage** : Vérifier si un fichier a besoin d'être converti.

**Solution** :
```python
# Analyser l'encodage
detect_file_encoding("fichier_suspect.tex")

# Si needs_conversion = true, corriger
fix_file_encoding("fichier_suspect.tex")
```

---

## 🔍 Encodages Détectés

Le serveur essaie les encodages dans cet ordre :
1. **utf-8** : Encodage moderne standard
2. **latin-1** / **iso-8859-1** : Europe occidentale classique
3. **cp1252** : Windows Western European (le plus courant sous Windows)
4. **cp850** : DOS Western European
5. **utf-8-sig** : UTF-8 avec BOM (Byte Order Mark)

L'encodage détecté est celui qui produit le moins de caractères invalides (`�`).

---

## ⚠️ Précautions

### Backups Automatiques
- Par défaut, un fichier `.backup` est créé avant toute modification
- Si le backup existe déjà, un avertissement est émis mais la conversion continue
- Pour désactiver les backups : `create_backup=false`

### Fichiers Déjà UTF-8
- Si un fichier est déjà en UTF-8, il est **préservé tel quel**
- Aucune modification n'est effectuée (sauf si `output_path` est spécifié)

### Vérification Post-Conversion
- Le serveur teste systématiquement la lecture UTF-8 après conversion
- Si la vérification échoue, une erreur est retournée

---

## 🎯 Intégration dans le Workflow Claude

### Pour Claude Code

**RÈGLE CRITIQUE** : Utiliser `fix_file_encoding()` systématiquement après avoir généré/modifié un fichier contenant des caractères accentués français.

**Workflow recommandé** :
```python
# 1. Générer/modifier le fichier
Write("cours.tex", contenu_avec_accents)

# 2. IMMÉDIATEMENT corriger l'encodage
fix_file_encoding("cours.tex")

# 3. Livrer le fichier
# Le fichier est maintenant garanti UTF-8
```

### Pour /adaptTex

**Étape 6 du workflow** (ajoutée) :
```
### 6. Correction d'encodage UTF-8 (CRITIQUE)
   - OBLIGATOIRE : Utiliser encoding-fixer-server
   - fix_file_encoding(file_path)
   - Vérifier UTF-8 sans corruption
```

---

## 📊 Statistiques et Rapports

### Rapport de Correction Individuelle

Exemple de retour pour un fichier converti :
```json
{
  "success": true,
  "file": "C:/Users/.../cours.tex",
  "original_encoding": "cp1252",
  "new_encoding": "utf-8",
  "characters_count": 3456,
  "backup_created": true,
  "backup_path": "C:/Users/.../cours.tex.backup"
}
```

### Rapport de Batch Processing

Exemple de retour pour un répertoire :
```json
{
  "success": true,
  "directory": "C:/Users/.../MonProjet",
  "pattern": "*.tex",
  "recursive": true,
  "files_found": 15,
  "files_processed": 15,
  "files_converted": 5,
  "files_already_utf8": 10,
  "files_failed": 0,
  "details": [
    {
      "file": "cours1.tex",
      "status": "converted",
      "original_encoding": "cp1252",
      "new_encoding": "utf-8"
    },
    {
      "file": "cours2.tex",
      "status": "skipped",
      "encoding": "utf-8"
    },
    ...
  ]
}
```

---

## 🐛 Dépannage

### Problème : "Impossible de détecter l'encodage"

**Cause** : Le fichier utilise un encodage rare non supporté.

**Solution** : Ouvrir manuellement dans un éditeur et sauvegarder en UTF-8.

---

### Problème : "Fichier introuvable"

**Cause** : Chemin invalide ou fichier supprimé.

**Solution** : Vérifier le chemin avec `ls` ou `dir`.

---

### Problème : Caractères toujours corrompus après correction

**Cause** : Le fichier source était déjà corrompu avant la conversion.

**Solution** :
1. Restaurer depuis le `.backup`
2. Corriger manuellement les caractères dans l'éditeur
3. Relancer `fix_file_encoding()`

---

## 🚀 Performance

- **Rapidité** : < 1 seconde pour fichiers < 1 Mo
- **Fiabilité** : Détection automatique avec vérification post-conversion
- **Sécurité** : Backups automatiques par défaut
- **Compatibilité** : Tous les encodages Windows/Unix courants

---

## 📝 Exemples Complets

### Exemple 1 : Correction Simple

```python
# Fichier avec caractères corrompus
fix_file_encoding("cours_problematique.tex")

# Résultat :
# ✓ Backup créé : cours_problematique.tex.backup
# ✓ Encodage : cp1252 → utf-8
# ✓ 2345 caractères convertis
```

---

### Exemple 2 : Workflow /adaptTex

```python
# 1. Transformation bfcours
# ... transformations LaTeX ...

# 2. Écriture du fichier
Write("cours_modified.tex", contenu_transforme)

# 3. CORRECTION ENCODAGE OBLIGATOIRE
fix_file_encoding("cours_modified.tex")

# 4. Rapport final
# ✓ Fichier livré en UTF-8 garanti
```

---

### Exemple 3 : Batch Processing

```python
# Corriger tous les fichiers d'un projet
fix_directory_encoding(
    "C:/Users/.../MonProjet",
    pattern="*.tex",
    recursive=true
)

# Résultat :
# ✓ 15 fichiers trouvés
# ✓ 5 convertis (cp1252 → utf-8)
# ✓ 10 déjà UTF-8 (préservés)
# ✓ 0 échecs
```

---

## 🎓 Bonnes Pratiques

1. **Toujours corriger avant de livrer** un fichier généré/modifié
2. **Utiliser les backups** (défaut) pour sécurité
3. **Analyser d'abord** avec `detect_file_encoding()` si incertain
4. **Batch processing** pour projets entiers récupérés
5. **Vérifier dans VSCode** que les accents s'affichent correctement

---

## 📞 Support

Pour tout problème avec le serveur :
1. Vérifier les logs dans `stderr`
2. Tester avec `get_encoding_stats()` pour vérifier que le serveur fonctionne
3. Utiliser `detect_file_encoding()` pour diagnostiquer

---

## 🔄 Mises à Jour Futures

**Extensions prévues** :
- Support d'encodages asiatiques (Shift-JIS, GB2312, etc.)
- Détection BOM (Byte Order Mark)
- Mode interactif pour valider chaque conversion
- Intégration avec `latex-compiler-server` (détection automatique)
