# 🚀 Guide de Démarrage Rapide - Problémathèque CSEN

## Installation (1 minute)

```bash
# 2. Tester l'installation
python .claude/skills/problematheque-search/scripts/problematheque.py --help
```

Si l'aide s'affiche, c'est prêt ! ✅

---

## Exemples Rapides

### 🔍 Rechercher des Problèmes

```bash
# Recherche simple
python .claude/skills/problematheque-search/scripts/problematheque.py "fractions"

# Filtrer par niveau
python .claude/skills/problematheque-search/scripts/problematheque.py "géométrie" --cycles 4

# Filtrer par domaine
python .claude/skills/problematheque-search/scripts/problematheque.py --domaines geometrie fractions

# Combinaison
python .claude/skills/problematheque-search/scripts/problematheque.py "aire" \
  --cycles 3 --domaines geometrie --limit 5
```

### 💾 Télécharger des Fiches

```bash
# PDF enseignant (par défaut)
python .claude/skills/problematheque-search/scripts/problematheque.py \
  --download "la-cigale-et-la-fourmi"

# DOCX enseignant
python .claude/skills/problematheque-search/scripts/problematheque.py \
  --download "pizzas-entre-amis" --format docx_enseignant

# Spécifier le dossier
python .claude/skills/problematheque-search/scripts/problematheque.py \
  --download "un-quart-de-gateau" --output ./mes-ressources
```

### 🔗 Voir les Liens de Téléchargement

```bash
python .claude/skills/problematheque-search/scripts/problematheque.py \
  "fractions" --cycles 3 --limit 5 --links
```

---

## Filtres Disponibles

### Par Cycle

| Option | Description |
|--------|-------------|
| `--cycles 1` | Cycle 1 (Maternelle) |
| `--cycles 2` | Cycle 2 (CP, CE1, CE2) |
| `--cycles 3` | Cycle 3 (CM1, CM2, 6ème) |
| `--cycles 4` | Cycle 4 (5ème, 4ème, 3ème) |
| `--cycles lycee` | Lycée |
| `--cycles 3 4` | Cycles 3 ET 4 |

### Par Domaine

```bash
--domaines algebre              # Algèbre & Préalgèbre
--domaines algorithmique        # Algorithmique
--domaines analyse              # Analyse
--domaines fractions            # Fractions
--domaines geometrie            # Géométrie
--domaines "grandeurs mesures"  # Grandeurs et Mesures
--domaines logique              # Logique
--domaines "nombres calculs"    # Nombres et Calculs
--domaines "organisation donnees" # Organisation des Données
--domaines probabilites         # Probabilités & Statistiques
```

### Par Mots-Clés

```bash
--keywords symetrie pavage aire
--keywords fraction partage
--keywords equation algebre
```

---

## Formats de Téléchargement

| Format | Option |
|--------|--------|
| PDF Enseignant | `--format pdf_enseignant` (défaut) |
| DOCX Enseignant | `--format docx_enseignant` |
| ODT Enseignant | `--format odt_enseignant` |
| PDF Élève | `--format pdf_eleve` (rare) |

---

## Utilisation depuis Claude Code

### Recherche Automatique

Quand tu demandes à Claude de créer une activité, il peut automatiquement rechercher des problèmes pertinents :

> **Toi :** "Crée une activité sur les fractions pour CM2"

> **Claude :** [Recherche automatique dans la Problémathèque...]
> "Pour enrichir cette activité, j'ai trouvé 2 problèmes pertinents :
> 1. 'Pizzas entre amis' - Partage équitable de 3 pizzas entre 4 amis
> 2. 'Un quart de gâteau' - Comparaison de fractions avec aires
>
> Veux-tu que je les intègre ?"

### Recherche Explicite

> **Toi :** "Cherche des problèmes sur les symétries pour 5ème"

> **Claude :** [Exécute la recherche et affiche les résultats...]

### Téléchargement et Intégration LaTeX

> **Toi :** "Intègre le problème 'La cigale et la fourmi' dans mon cours LaTeX"

> **Claude :**
> 1. Télécharge la fiche DOCX
> 2. Extrait le contenu
> 3. Convertit en LaTeX
> 4. Intègre dans le document

---

## 🔧 Maintenance du Scraper

### Si le Scraper Casse

**Symptôme :**
```
❌ Format 'pdf_enseignant' non disponible
```

**Solution rapide :**

1. **Inspecter le site :**
   - Ouvre https://www.problematheque-csen.fr/fiche-probleme/la-cigale-et-la-fourmi/
   - Clique droit sur "Télécharger PDF" → Inspecter
   - Note la classe CSS (ex: `class="new-download-btn"`)

2. **Mettre à jour la config :**

   Édite `.claude/skills/problematheque-search/scripts/scraper_config.json` :

   ```json
   "pdf_enseignant": {
     "selector": "a.new-download-btn[href*='.pdf'], a.format__download-link[href*='.pdf']"
   }
   ```

3. **Vider le cache :**
   ```bash
   rm .claude/skills/problematheque-search/scripts/download_links_cache.json
   ```

4. **Tester :**
   ```bash
   python .claude/skills/problematheque-search/scripts/problematheque.py \
     --download "la-cigale-et-la-fourmi"
   ```

---

## 📚 Documentation Complète

- **README.md** : Guide utilisateur complet
- **skill.md** : Prompt système pour Claude
- **TESTS.md** : Résultats des tests
- **rapport-faisabilite-skill-problematheque.md** : Analyse technique détaillée

---

## ❓ Dépannage Rapide

### Erreur : "Module requests not found"

```bash
python -m pip install requests beautifulsoup4 lxml python-dateutil
```

### Erreur : "Request timeout"

```bash
# Augmenter le timeout dans scraper_config.json
"timeout_seconds": 30
```

### Aucun résultat trouvé

- Essaie une recherche plus large : `python problematheque.py "fraction"` au lieu de `"fractions"`
- Vérifie l'orthographe
- Teste sans filtres : `python problematheque.py "géométrie"`

### Cache corrompu

```bash
rm .claude/skills/problematheque-search/scripts/*.json
```

---

## 💡 Astuces

1. **Recherche progressive :**
   ```bash
   # Large d'abord
   python problematheque.py "géométrie"

   # Puis affiner
   python problematheque.py "géométrie" --cycles 3

   # Préciser encore
   python problematheque.py "géométrie" --cycles 3 --keywords symetrie
   ```

2. **Sortie JSON pour automatisation :**
   ```bash
   python problematheque.py "fractions" --json > resultats.json
   ```

3. **Téléchargement batch :**
   ```bash
   python problematheque.py --download "fiche-1"
   python problematheque.py --download "fiche-2"
   python problematheque.py --download "fiche-3"
   ```

---

**Bon travail ! 🎉**

Pour toute question, consulte le README.md complet ou demande à Claude Code.
