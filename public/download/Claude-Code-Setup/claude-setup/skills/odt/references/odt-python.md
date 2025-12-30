# Tutoriel odfpy - Creation de documents ODT en Python

**Important: Lire ce document entierement avant de commencer.** Ce guide couvre la creation de documents ODT avec la bibliotheque odfpy.

## Installation

```bash
pip install odfpy
```

## Imports essentiels

```python
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, TableProperties
from odf.style import TableColumnProperties, TableCellProperties, TableRowProperties
from odf.style import ListLevelProperties, ListLevelStyleBullet, ListLevelStyleNumber
from odf.text import P, Span, List, ListItem, ListStyle, H
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.draw import Frame, Image
```

## Creation de document basique

```python
from odf.opendocument import OpenDocumentText
from odf.text import P

# Creer un nouveau document
doc = OpenDocumentText()

# Ajouter un paragraphe
p = P(text="Bonjour le monde!")
doc.text.addElement(p)

# Sauvegarder
doc.save("document.odt")
```

## Styles de paragraphe

### Definir un style personnalise

```python
from odf.style import Style, TextProperties, ParagraphProperties

# Style de paragraphe
style = Style(name="MonStyle", family="paragraph")
style.addElement(ParagraphProperties(
    margintop="0.5cm",
    marginbottom="0.5cm",
    textalign="justify"
))
style.addElement(TextProperties(
    fontsize="12pt",
    fontname="Bitstream Vera Sans",
    fontweight="bold",
    color="#000000"
))
doc.styles.addElement(style)

# Utiliser le style
p = P(stylename="MonStyle", text="Texte avec style personnalise")
doc.text.addElement(p)
```

### Styles automatiques (inline)

```python
from odf.style import Style, TextProperties

# Style automatique (non reutilisable, inline)
auto_style = Style(name="T1", family="text")
auto_style.addElement(TextProperties(fontweight="bold", color="#FF0000"))
doc.automaticstyles.addElement(auto_style)
```

## Formatage du texte

### Texte avec plusieurs styles

```python
from odf.text import P, Span
from odf.style import Style, TextProperties

# Style gras
bold_style = Style(name="Bold", family="text")
bold_style.addElement(TextProperties(fontweight="bold"))
doc.automaticstyles.addElement(bold_style)

# Style italique
italic_style = Style(name="Italic", family="text")
italic_style.addElement(TextProperties(fontstyle="italic"))
doc.automaticstyles.addElement(italic_style)

# Paragraphe avec texte mixte
p = P()
p.addText("Texte normal, ")
bold_span = Span(stylename="Bold", text="texte en gras")
p.addElement(bold_span)
p.addText(", et ")
italic_span = Span(stylename="Italic", text="texte en italique")
p.addElement(italic_span)
p.addText(".")
doc.text.addElement(p)
```

### Couleurs et tailles

```python
# Style avec couleur
red_style = Style(name="Red", family="text")
red_style.addElement(TextProperties(
    color="#FF0000",
    fontsize="14pt"
))
doc.automaticstyles.addElement(red_style)
```

## Titres et sections

```python
from odf.text import H, P

# Titre de niveau 1
h1 = H(outlinelevel=1, text="Chapitre 1")
doc.text.addElement(h1)

# Titre de niveau 2
h2 = H(outlinelevel=2, text="Section 1.1")
doc.text.addElement(h2)

# Paragraphe
p = P(text="Contenu de la section...")
doc.text.addElement(p)
```

## Listes

### Liste a puces

```python
from odf.text import List, ListItem, P
from odf.style import ListLevelStyleBullet, ListLevelProperties

# Creer le style de liste
list_style = ListStyle(name="BulletList")
bullet = ListLevelStyleBullet(level=1, bulletchar="\u2022")
bullet.addElement(ListLevelProperties(
    spacebefore="0.5cm",
    minlabelwidth="0.5cm"
))
list_style.addElement(bullet)
doc.automaticstyles.addElement(list_style)

# Creer la liste
lst = List(stylename="BulletList")
for item_text in ["Premier element", "Deuxieme element", "Troisieme element"]:
    item = ListItem()
    item.addElement(P(text=item_text))
    lst.addElement(item)
doc.text.addElement(lst)
```

### Liste numerotee

```python
from odf.style import ListLevelStyleNumber

list_style = ListStyle(name="NumberedList")
number = ListLevelStyleNumber(
    level=1,
    numformat="1",
    numsuffix=". "
)
number.addElement(ListLevelProperties(
    spacebefore="0.5cm",
    minlabelwidth="0.75cm"
))
list_style.addElement(number)
doc.automaticstyles.addElement(list_style)
```

## Tableaux

### Tableau simple

```python
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.text import P
from odf.style import Style, TableProperties, TableColumnProperties, TableCellProperties

# Style du tableau
table_style = Style(name="TableStyle", family="table")
table_style.addElement(TableProperties(width="17cm", align="margins"))
doc.automaticstyles.addElement(table_style)

# Style des colonnes
col_style = Style(name="ColStyle", family="table-column")
col_style.addElement(TableColumnProperties(columnwidth="4cm"))
doc.automaticstyles.addElement(col_style)

# Style des cellules
cell_style = Style(name="CellStyle", family="table-cell")
cell_style.addElement(TableCellProperties(
    padding="0.1cm",
    border="0.5pt solid #000000"
))
doc.automaticstyles.addElement(cell_style)

# Creer le tableau
table = Table(name="Tableau1", stylename="TableStyle")

# Ajouter les colonnes
for _ in range(3):
    table.addElement(TableColumn(stylename="ColStyle"))

# Ajouter les lignes
data = [
    ["Nom", "Prenom", "Age"],
    ["Dupont", "Jean", "25"],
    ["Martin", "Marie", "30"]
]

for row_data in data:
    row = TableRow()
    for cell_data in row_data:
        cell = TableCell(stylename="CellStyle")
        cell.addElement(P(text=cell_data))
        row.addElement(cell)
    table.addElement(row)

doc.text.addElement(table)
```

### Cellule avec fond colore

```python
# Style cellule avec fond
header_cell_style = Style(name="HeaderCell", family="table-cell")
header_cell_style.addElement(TableCellProperties(
    padding="0.1cm",
    border="0.5pt solid #000000",
    backgroundcolor="#E0E0E0"
))
doc.automaticstyles.addElement(header_cell_style)
```

### Fusion de cellules

```python
# Cellule fusionnee sur 2 colonnes
cell = TableCell(
    stylename="CellStyle",
    numbercolumnsspanned=2
)
cell.addElement(P(text="Cellule fusionnee"))
row.addElement(cell)

# Ajouter une cellule couverte
from odf.table import CoveredTableCell
row.addElement(CoveredTableCell())
```

## Images

### Inserer une image

```python
from odf.draw import Frame, Image
from odf.text import P
import os

# Le fichier image doit etre ajoute au document
image_path = "image.png"

# Creer le frame
frame = Frame(
    name="Image1",
    anchortype="paragraph",
    width="5cm",
    height="3cm"
)

# Ajouter l'image au document
href = doc.addPicture(image_path)
image = Image(href=href)
frame.addElement(image)

# Ajouter dans un paragraphe
p = P()
p.addElement(frame)
doc.text.addElement(p)
```

## Sauts de page

```python
from odf.style import Style, ParagraphProperties

# Style avec saut de page avant
page_break_style = Style(name="PageBreak", family="paragraph")
page_break_style.addElement(ParagraphProperties(breakbefore="page"))
doc.automaticstyles.addElement(page_break_style)

# Utiliser
p = P(stylename="PageBreak", text="Nouveau chapitre")
doc.text.addElement(p)
```

## Charger et modifier un document existant

```python
from odf.opendocument import load

# Charger un document existant
doc = load("existant.odt")

# Ajouter du contenu
p = P(text="Nouveau paragraphe ajoute")
doc.text.addElement(p)

# Sauvegarder (ecrase ou nouveau fichier)
doc.save("modifie.odt")
```

## Copier les styles d'un document modele

```python
from odf.opendocument import load, OpenDocumentText
from copy import deepcopy

# Charger le modele avec les styles
template = load("modele.odt")

# Creer un nouveau document
doc = OpenDocumentText()

# Copier les styles du modele
for style in template.styles.childNodes:
    doc.styles.addElement(deepcopy(style))

for style in template.automaticstyles.childNodes:
    doc.automaticstyles.addElement(deepcopy(style))

# Maintenant le nouveau document a acces aux memes styles
p = P(stylename="_5f_Paragraphe", text="Texte avec style Sesamath")
doc.text.addElement(p)

doc.save("nouveau_avec_styles.odt")
```

## Bonnes pratiques

1. **Toujours definir les styles avant de les utiliser**
2. **Utiliser `automaticstyles` pour les styles uniques, `styles` pour les reutilisables**
3. **Les noms de styles avec caracteres speciaux doivent etre encodes** (`_` devient `_5f_`, espace devient `_20_`)
4. **Sauvegarder regulierement pour eviter la perte de donnees**
5. **Tester l'ouverture dans LibreOffice apres creation**

## Encodage des noms de styles

Dans les fichiers XML ODT, les caracteres speciaux dans les noms de styles sont encodes:
- `_` (underscore) devient `_5f_`
- ` ` (espace) devient `_20_`
- `-` (tiret) devient `_2d_`
- `'` (apostrophe) devient `_27_`

Exemple: `_Paragraphe_Reponse_Eleve` devient `_5f_Paragraphe_5f_Reponse_5f_Eleve`

## References

- Documentation odfpy: https://github.com/eea/odfpy
- Specification ODF: https://docs.oasis-open.org/office/OpenDocument/v1.3/
