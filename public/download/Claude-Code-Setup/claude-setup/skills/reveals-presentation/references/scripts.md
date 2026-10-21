# Scripts utilitaires

Scripts Python prêts à l'emploi dans le dossier `scripts/` du skill (chemins ci-dessous relatifs au dossier du skill).

### extract_tikz_figures.py

**Usage** : Extraire automatiquement les graphiques TikZ d'un fichier LaTeX et les compiler en images PNG.

```bash
python scripts/extract_tikz_figures.py <fichier.tex> [--output-dir images_graphiques] [--prefix graph] [--dpi 300]
```

**Quand l'utiliser** :
- Vous avez un fichier LaTeX (enonce.tex, correction.tex) contenant des figures TikZ
- Vous voulez générer automatiquement des images PNG pour les intégrer dans la présentation
- Le script détecte tous les `\begin{tikzpicture}...\end{tikzpicture}` et les compile individuellement

**Workflow** :
1. Le script extrait chaque bloc TikZ
2. Crée un fichier LaTeX standalone pour chaque graphique
3. Compile avec LuaLaTeX → génère les PDF
4. Convertit les PDF en PNG haute résolution (300 DPI par défaut)
5. Nomme les fichiers `graph_01.png`, `graph_02.png`, etc.

**Template inclus** : Le script contient un template LaTeX avec tous les styles TikZ communs (points, vecteurs, axes, repères).

### convert_pdf_to_png.py

**Usage** : Convertir des fichiers PDF existants en PNG haute résolution.

```bash
python scripts/convert_pdf_to_png.py <dossier_ou_fichier.pdf> [--dpi 300] [--output-dir .]
```

**Quand l'utiliser** :
- Vous avez déjà des PDF de figures à convertir
- Vous voulez changer la résolution DPI d'images existantes
- Le script tente plusieurs méthodes (pdftoppm, Ghostscript, ImageMagick)

**Méthodes de conversion** (par ordre de priorité) :
1. pdftoppm (souvent le plus fiable sur Windows)
2. Ghostscript 64-bit
3. Ghostscript 32-bit
4. ImageMagick (magick)
5. ImageMagick (convert)

### embed_images_base64.py

**Usage** : Convertir toutes les images d'un fichier HTML en base64 pour créer une version autonome.

```bash
python scripts/embed_images_base64.py <presentation.html> [--output presentation_embedded.html]
```

**⚠️ IMPORTANT** : Utiliser UNIQUEMENT pour partager le document une fois TOUTES les modifications terminées !

**Quand l'utiliser** :
- Vous voulez envoyer la présentation par mail
- Vous voulez héberger sans dossier images externe
- Vous avez terminé TOUTES les modifications (le fichier embedded sera plus lourd)

**Avantages** :
- Fichier HTML totalement portable (pas de dépendances externes)
- Plus besoin du dossier `images_graphiques/`
- Fonctionne même sans serveur web

**Inconvénients** :
- Fichier plus lourd (+300-500 KB selon le nombre d'images)
- Pas pratique pour édition (préférer travailler avec images externes)

**Workflow recommandé** :
1. Travailler avec images externes pendant le développement
2. Une fois toutes les modifications terminées → créer la version embedded
3. Partager uniquement le fichier `*_embedded.html`
