---
name: odt
description: "Skill de creation et manipulation de documents ODT (OpenDocument Text) avec styles educatifs Sesamath. Ce skill devrait etre utilise pour creer des cahiers d'exercices, fiches eleves, et documents pedagogiques avec styles personnalises (paragraphes, tableaux, numerotation d'exercices, reponses eleves, pointilles grises). Prend en charge la creation de nouveaux documents ODT et l'edition de documents existants."
---

# ODT - Creation et manipulation de documents OpenDocument

## Purpose

Ce skill permet de creer et manipuler des fichiers ODT (OpenDocument Text) avec les styles educatifs Sesamath pour les mathematiques. Un fichier .odt est une archive ZIP contenant des fichiers XML et ressources.

## REGLES IMPERATIVES

### 1. ACCENTS FRANCAIS - OBLIGATOIRE

**Les accents francais doivent etre geres CORRECTEMENT dans tous les documents.**

- Utiliser systematiquement les caracteres accentues natifs : é, è, ê, ë, à, â, ù, û, ô, î, ï, ç, etc.
- NE JAMAIS utiliser des versions sans accent (ex: "Definition" au lieu de "Définition")
- NE JAMAIS utiliser des encodages alternatifs (ex: `\u00e9` au lieu de `é`)
- Verifier que l'encodage UTF-8 est preserve dans tous les fichiers XML du document ODT

**Exemples corrects :**
```python
doc.add_definition("Définition", "Une fraction est un quotient de deux nombres entiers.")
doc.add_propriete("Propriété", "Le carré d'un nombre négatif est positif.")
doc.add_methode("Méthode", "Pour résoudre une équation...")
```

**A PROSCRIRE :**
```python
# FAUX - pas d'accents
doc.add_definition("Definition", "Une fraction est...")
# FAUX - encodage echappes
doc.add_definition("D\u00e9finition", "...")
```

### 2. MODE MATHEMATIQUE - SYSTEMATIQUE

**Utiliser le mode maths (formules StarMath) des qu'il y a du contenu mathematique.**

Meme pour des expressions simples, TOUJOURS utiliser `add_formula()` ou `add_formula_inline()` :

| Contenu | Methode a utiliser |
|---------|-------------------|
| Fraction quelconque | `add_formula("{a} over {b}")` |
| Nombre avec exposant | `add_formula("x^{2}")` |
| Racine carree | `add_formula("sqrt{x}")` |
| Egalite/equation | `add_formula("2x + 3 = 7")` |
| Expression inline | `add_formula_inline("On a ", "x = 5", ".")` |

**Exemples corrects :**
```python
# BIEN - formules en mode maths
doc.add_paragraph("Calculer :")
doc.add_formula("{3} over {4} + {1} over {2}")

# BIEN - inline avec mode maths
doc.add_formula_inline("L'aire du cercle est ", "A = %pi r^{2}", ".")
```

**A PROSCRIRE :**
```python
# FAUX - maths en texte brut
doc.add_paragraph("Calculer : 3/4 + 1/2")
doc.add_paragraph("L'aire du cercle est A = πr²")
```

Ces deux regles sont NON-NEGOCIABLES et doivent etre appliquees dans TOUS les documents ODT generes.

## When to Use

Ce skill devrait etre utilise lorsque:
- Creation de cahiers d'exercices mathematiques
- Generation de fiches eleves avec zones de reponse
- Creation de documents avec styles personnalises Sesamath
- Edition de documents ODT existants
- Extraction de contenu depuis des fichiers ODT

## WORKFLOW RECOMMANDE - Approche par Script Python

**IMPORTANT**: L'agent ne manipule PAS directement les fichiers ODT. A la place, il:
1. Copie le script template vers le dossier de destination
2. Modifie le script Python pour y injecter le contenu
3. Execute le script pour generer l'ODT

Cette approche garantit:
- Les styles Sesamath sont toujours corrects
- Le titre du chapitre est injecte dans les en-tetes
- Le code est lisible et modifiable
- Moins d'erreurs qu'en manipulant du XML ODT

### Etape 1: Copier le template

```bash
cp ".claude/skills/odt/scripts/template_document.py" "destination/generate_mon_doc.py"
```

### Etape 2: Modifier le script

L'agent modifie les sections marquees `[AGENT: ...]`:

```python
# Metadonnees
OUTPUT_FILE = "cours_fractions.odt"
CHAPITRE = "Les Fractions"
NIVEAU = "6e"
DOMAINE = "numerique"

def build_document():
    doc = SesamathDocument(OUTPUT_FILE, chapitre=CHAPITRE, niveau=NIVEAU, domaine=DOMAINE,
                           titre_dans_contenu=False)  # Titre dans en-tete seulement

    # Ajuster la marge gauche (recommande)
    doc.set_page_margins(left="1.7cm")

    # Structure : H1 directement (pas de add_empty_line() avant)
    doc.add_heading("Rappels", level=1)

    # Environnements didactiques
    doc.add_definition("Definition", "Une fraction est un nombre qui s'ecrit sous la forme",
                       formule="{a} over {b}")

    doc.add_vocabulaire("Vocabulaire", [
        "Le numerateur est le nombre au-dessus.",
        "Le denominateur est le nombre en-dessous.",
    ])

    # Exercices en grille 2x2
    doc.add_heading("Exercices", level=1)
    doc.start_exercise_grid(2)
    doc.add_exercice("Simplifier", "Simplifie:", questions=["4/8 = ", "6/9 = "],
                     correction=["1/2", "2/3"])
    doc.add_exercice("Calculer", "Calcule:", questions=["1/2 + 1/4 = "],
                     correction=["3/4"])
    doc.end_exercise_grid()

    doc.add_corrections_page()
    doc.save()
```

### Bonnes pratiques de redaction

| A faire | A eviter |
|---------|----------|
| `doc.add_heading("Titre", level=1)` directement | `add_empty_line()` avant les H1 |
| Questions sans sous-numerotation | "a) ...", "b) ..." dans les questions |
| Utiliser `start_exercise_grid(2)` pour 4 exos | `start_columns()` pour les exercices |
| `titre_dans_contenu=False` | Titre en double (en-tete + contenu) |

### Etape 3: Executer le script

```bash
cd "destination" && python generate_mon_doc.py
```

## API SesamathDocument - Reference

### Initialisation

```python
doc = SesamathDocument(
    "fichier.odt",
    chapitre="Les Fractions",  # Injecte dans les en-tetes
    niveau="6e",                # 6e, 5e, 4e, 3e, 2nde, 1ere, tle
    domaine="numerique"         # numerique, geometrie, mesures, gestion_donnees, problemes
)
```

### Environnements didactiques

Chaque environnement a un titre encadre colore + corps avec bordure gauche.

| Methode | Couleur titre | Couleur bordure |
|---------|---------------|-----------------|
| `add_definition()` | #00a933 (vert) | #77bc65 |
| `add_vocabulaire()` | #00a933 (vert) | #77bc65 |
| `add_propriete()` | #bf0041 (rose) | #ec9ba4 |
| `add_methode()` | #2a6099 (bleu) | #729fcf |
| `add_remarque()` | #50938a (turquoise) | #78bbb2 |
| `add_exemple()` | #000000 (noir) | #eeeeee |

```python
# Avec texte simple
doc.add_definition("Definition", "Une fraction est...")

# Avec liste a puces
doc.add_methode("Methode", [
    "Etape 1...",
    "Etape 2...",
])

# Avec formule integree
doc.add_propriete("Propriete", "La formule est", formule="{a} over {b}")
```

### Exercices

```python
# Exercice simple
doc.add_exercice(
    "Titre de l'exercice",
    "Enonce...",
    questions=["Question 1", "Question 2"],
    lignes_reponse=2,
    correction=["Reponse 1", "Reponse 2"]  # Optionnel, pour page corrections
)

# Zone de reponse seule
doc.add_zone_reponse(lignes=3, style='pointilles')  # ou 'vide'
```

### Formules mathematiques (StarMath)

```python
# Formule seule sur une ligne
doc.add_formula("{3} over {4}")

# Formule inline dans du texte
doc.add_formula_inline("L'aire vaut ", "%pi r^{2}", " unites.")
```

Syntaxe StarMath courante:
- Fraction: `{a} over {b}`
- Racine: `sqrt{x}`
- Puissance: `x^{2}`
- Indice: `x_{i}`
- Multiplication: `times` ou `cdot`
- Pi: `%pi`

### Mise en page

```python
# Saut de page
doc.page_break()

# Paragraphes
doc.add_paragraph("Texte...")
doc.add_empty_line()
doc.add_heading("Titre", level=2)
```

### GRILLE d'exercices (RECOMMANDE)

**Utiliser `start_exercise_grid()` pour disposer les exercices en grille.**
Cette methode utilise un tableau ODT invisible, garantissant un alignement
parfait quelle que soit la longueur des exercices.

```
| Exo 1   | Exo 2   |
| Exo 3   | Exo 4   |
```

```python
# Grille de tableau pour les exercices (2 colonnes)
doc.start_exercise_grid(2)

# Chaque exercice occupe une cellule du tableau
doc.add_exercice("Exo 1", ...)  # Cellule 1,1
doc.add_exercice("Exo 2", ...)  # Cellule 1,2
doc.add_exercice("Exo 3", ...)  # Cellule 2,1
doc.add_exercice("Exo 4", ...)  # Cellule 2,2

doc.end_exercise_grid()
```

**Avantages vs multicolonne:**
- Alignement parfait meme si les exercices ont des tailles differentes
- Pas de probleme de saut de page inattendu
- Grille vraiment 2x2 (ou NxM)

### Multicolonne (texte libre)

Pour du texte libre (pas des exercices), utiliser `start_columns()`:

```python
doc.start_columns(2, gap="1cm", separator=True)
doc.add_paragraph("Colonne 1...")
doc.column_break()
doc.add_paragraph("Colonne 2...")
doc.end_columns()
```

### Marges de page

```python
# Ajuster les marges (utile pour la bande coloree Sesamath)
doc.set_page_margins(left="1.7cm")  # Valeur recommandee
```

### Page de corrections

```python
# Genere automatiquement depuis les exercices ayant une correction
doc.add_corrections_page(titre="CORRECTIONS", columns=2)
```

## Mise en valeur automatique des mots-cles

**FONCTIONNALITE AUTOMATIQUE** : Les mots-cles mathematiques sont automatiquement
mis en gras avec la couleur de l'environnement. Cela facilite la lecture des
documents sans travail supplementaire pour l'enseignant.

### Categories de mots-cles detectes

| Categorie | Exemples |
|-----------|----------|
| Verbes d'action | calculer, simplifier, demontrer, tracer, construire, determiner, resoudre... |
| Vocabulaire math | numerateur, denominateur, fraction, equation, fonction, triangle, cercle... |
| Mots logiques | donc, ainsi, car, si, alors, soit, de plus, en effet... |
| Expressions | est egal a, est proportionnel a, appartient a, si et seulement si... |

### Couleurs par environnement

Les mots-cles sont colores selon l'environnement dans lequel ils apparaissent:

| Environnement | Couleur mots-cles |
|---------------|-------------------|
| Definition/Vocabulaire | Vert #00a933 |
| Propriete | Rose #bf0041 |
| Methode | Bleu #2a6099 |
| Remarque | Turquoise #50938a |
| Exemple | Gris fonce #333333 |
| Exercice | Bleu #2a6099 |

### Exemple de rendu

```python
doc.add_exercice(
    "Simplifier les fractions",
    "Calculer puis simplifier les fractions suivantes:",
    questions=["Determiner le quotient...", "Trouver l'inverse..."]
)
# Les mots "Calculer", "simplifier", "Determiner", "quotient", "Trouver", "inverse"
# seront automatiquement en gras bleu (#2a6099)
```

## Style des numeros de questions

Les numeros de questions (1., 2., 3., etc.) ont automatiquement un petit cadre
decoratif bleu clair pour les differencier visuellement des donnees de l'exercice.

- Fond bleu tres clair (#e8f0fa)
- Bordure fine bleue (#2a6099)
- Texte gras bleu

Cela permet a l'eleve de reperer facilement les questions dans un exercice.

## Master Pages et En-tetes

Le domaine mathematique determine la master page utilisee:

| Domaine | Couleur laterale |
|---------|------------------|
| numerique | Jaune-vert #d7e12c |
| geometrie | Bleu-vert #1ca2b8 |
| mesures | Vert #7fb241 |
| gestion_donnees | Violet #9d0f89 |
| problemes | Rouge #d62e4e |

Le titre du chapitre est automatiquement injecte dans les bannieres d'en-tete.

## WORKFLOW ITERATIF - Modification de documents existants

**Pour modifier un ODT existant**, utiliser `odt_workspace.py` qui permet:
1. Dezipper l'ODT vers un workspace editable
2. Analyser la structure du document
3. Modifier le contenu via commandes simples
4. Re-pack en ODT
5. Convertir en PDF pour feedback visuel

### Cycle de travail user/IA

```
[User] "Modifie le titre de l'exercice 1"
   |
   v
[IA] 1. ws.unpack() + ws.analyze()    --> Voir la structure
     2. ws.replace_text("ancien", "nouveau")
     3. ws.pack()
     4. ws.to_pdf()
   |
   v
[User] Voit le PDF, demande d'autres modifs
   |
   v
[IA] Modifie encore...
```

### Usage en Python

```python
from odt_workspace import ODTWorkspace

# Ouvrir et analyser
ws = ODTWorkspace("document.odt")
ws.unpack()                          # Extrait vers document_workspace/
ws.analyze()                         # Affiche la structure

# Modifications
ws.replace_text("ancien", "nouveau") # Remplace du texte
ws.set_paragraph_text(5, "Nouveau texte")  # Modifie un paragraphe par index
ws.add_paragraph("Texte", style="Standard", after_idx=3)  # Ajoute
ws.delete_paragraph(7)               # Supprime un paragraphe

# Finalisation
ws.pack()                            # Recree l'ODT
ws.to_pdf()                          # Convertit en PDF
ws.cleanup()                         # Supprime le workspace
```

### Usage en ligne de commande

```bash
# Extraire et analyser
python odt_workspace.py unpack document.odt

# Remplacer du texte
python odt_workspace.py replace document.odt "ancien" "nouveau"

# Convertir en PDF
python odt_workspace.py topdf document.odt
```

### Methodes de modification disponibles

| Methode | Description |
|---------|-------------|
| `replace_text(old, new)` | Remplace toutes les occurrences |
| `set_paragraph_text(idx, text)` | Modifie un paragraphe par index |
| `add_paragraph(text, style, after_idx)` | Ajoute un paragraphe |
| `delete_paragraph(idx)` | Supprime un paragraphe |
| `get_paragraph(idx)` | Recupere le texte d'un paragraphe |

### Comprendre les index

L'analyse (`ws.analyze()`) affiche les paragraphes avec leurs index:

```
[PARAGRAPHES]
  [  0] Titre_Definition     | Definition
  [  1] Paragraphe_Def       | Une fraction est...
  [  2] Titre_Exercice       | 1  Simplifier
  [  3] Paragraphe           | Simplifie:
```

Utiliser ces index pour cibler les modifications.

## Scripts disponibles

| Script | Usage |
|--------|-------|
| `scripts/template_document.py` | **TEMPLATE** Script a copier et modifier |
| `scripts/create_sesamath_document.py` | Classe SesamathDocument |
| `scripts/odt_workspace.py` | **WORKSPACE** Modification iterative |
| `scripts/unpack.py` | Extraire ODT vers dossier |
| `scripts/pack.py` | Recreer ODT depuis dossier |
| `scripts/extract_text.py` | Extraire texte brut |

## Assets

| Fichier | Description |
|---------|-------------|
| `assets/template_sesamath_complet.odt` | Template avec 96 styles et master pages |
| `assets/sesamath_styles_full.json` | Documentation JSON des styles |

## Dependances

```bash
pip install odfpy
```

Pour conversion PDF: LibreOffice (`soffice --headless --convert-to pdf document.odt`)

## Structure d'un fichier ODT

```
document.odt (archive ZIP)
+-- mimetype                    # Type MIME (non compresse)
+-- META-INF/manifest.xml       # Liste des fichiers
+-- content.xml                 # Contenu du document
+-- styles.xml                  # Definitions des styles
+-- meta.xml                    # Metadonnees
+-- Object 1/content.xml        # Formule mathematique 1
```

## Encodage des noms de styles

Les caracteres speciaux dans les noms de styles ODT sont encodes:
- `_` (underscore) devient `_5f_`
- ` ` (espace) devient `_20_`
- `-` (tiret) devient `_2d_`
