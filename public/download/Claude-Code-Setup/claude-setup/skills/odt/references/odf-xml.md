# Patterns XML OpenDocument (ODF)

Ce fichier documente les patterns XML pour la manipulation directe des fichiers ODT.

## Namespaces

```xml
xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0"
```

## Structure de content.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    office:version="1.3">

    <office:automatic-styles>
        <!-- Styles automatiques (inline) -->
    </office:automatic-styles>

    <office:body>
        <office:text>
            <!-- Contenu du document -->
            <text:p text:style-name="Standard">Texte...</text:p>
        </office:text>
    </office:body>
</office:document-content>
```

## Structure de styles.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">

    <office:font-face-decls>
        <!-- Declarations de polices -->
    </office:font-face-decls>

    <office:styles>
        <!-- Styles nommes (reutilisables) -->
    </office:styles>

    <office:automatic-styles>
        <!-- Styles automatiques de mise en page -->
    </office:automatic-styles>

    <office:master-styles>
        <!-- Styles de pages maitres -->
    </office:master-styles>
</office:document-styles>
```

## Patterns de paragraphe

### Paragraphe simple
```xml
<text:p text:style-name="Standard">Texte du paragraphe</text:p>
```

### Paragraphe avec style personnalise
```xml
<text:p text:style-name="_5f_Paragraphe">Texte avec style Sesamath</text:p>
```

### Paragraphe vide (espacement)
```xml
<text:p text:style-name="Standard"/>
```

### Espaces multiples
```xml
<text:p text:style-name="Standard">
    Texte avec<text:s text:c="5"/>5 espaces
</text:p>
```

### Saut de ligne
```xml
<text:p text:style-name="Standard">
    Ligne 1<text:line-break/>Ligne 2
</text:p>
```

## Patterns de formatage inline

### Texte en gras (span)
```xml
<text:p text:style-name="Standard">
    Texte normal et <text:span text:style-name="Bold">texte en gras</text:span>
</text:p>
```

### Texte en couleur
```xml
<text:span text:style-name="T1">Texte colore</text:span>
<!-- Avec le style: -->
<style:style style:name="T1" style:family="text">
    <style:text-properties fo:color="#FF0000"/>
</style:style>
```

## Patterns de style

### Style de paragraphe
```xml
<style:style style:name="_5f_Paragraphe"
             style:display-name="_Paragraphe"
             style:family="paragraph"
             style:parent-style-name="Standard">
    <style:paragraph-properties
        fo:margin-left="0cm"
        fo:margin-right="0.101cm"
        fo:margin-top="0.101cm"
        fo:margin-bottom="0.101cm"
        fo:text-align="start"/>
    <style:text-properties
        fo:font-size="11pt"
        fo:font-weight="normal"/>
</style:style>
```

### Style de caractere
```xml
<style:style style:name="_5f_Caracteres_5f_gras"
             style:display-name="_Caracteres_gras"
             style:family="text">
    <style:text-properties fo:font-weight="bold"/>
</style:style>
```

### Style avec fond colore
```xml
<style:style style:name="_5f_Paragraphe_5f_Exemple"
             style:family="paragraph">
    <loext:graphic-properties draw:fill="solid" draw:fill-color="#eeeeee"/>
    <style:paragraph-properties
        fo:background-color="#eeeeee"
        fo:padding="0.049cm"
        fo:border="0.06pt solid #000000"/>
</style:style>
```

## Patterns de tableau

### Structure de tableau
```xml
<table:table table:name="Tableau1" table:style-name="Tableau1">
    <table:table-column table:style-name="Tableau1.A" table:number-columns-repeated="3"/>
    <table:table-row table:style-name="Tableau1.1">
        <table:table-cell table:style-name="Tableau1.A1">
            <text:p text:style-name="Standard">Cellule 1</text:p>
        </table:table-cell>
        <table:table-cell table:style-name="Tableau1.A1">
            <text:p text:style-name="Standard">Cellule 2</text:p>
        </table:table-cell>
        <table:table-cell table:style-name="Tableau1.A1">
            <text:p text:style-name="Standard">Cellule 3</text:p>
        </table:table-cell>
    </table:table-row>
</table:table>
```

### Style de tableau
```xml
<style:style style:name="Tableau1" style:family="table">
    <style:table-properties style:width="17cm" table:align="margins"/>
</style:style>
```

### Style de colonne
```xml
<style:style style:name="Tableau1.A" style:family="table-column">
    <style:table-column-properties style:column-width="5.667cm"/>
</style:style>
```

### Style de cellule
```xml
<style:style style:name="Tableau1.A1" style:family="table-cell">
    <style:table-cell-properties
        style:vertical-align="middle"
        fo:padding="0.1cm"
        fo:border="0.5pt solid #000000"/>
</style:style>
```

### Fusion de cellules
```xml
<table:table-cell table:style-name="Tableau1.A1"
                  table:number-columns-spanned="2">
    <text:p>Cellule fusionnee</text:p>
</table:table-cell>
<table:covered-table-cell/>
```

## Patterns de liste

### Liste a puces
```xml
<text:list text:style-name="List_20_1">
    <text:list-item>
        <text:p text:style-name="List_20_1">Premier element</text:p>
    </text:list-item>
    <text:list-item>
        <text:p text:style-name="List_20_1">Deuxieme element</text:p>
    </text:list-item>
</text:list>
```

### Style de liste numerotee
```xml
<text:list-style style:name="_5f_Numerotation_20_des_20_exercices">
    <text:list-level-style-number
        text:level="1"
        text:style-name="Numbering_20_Symbols"
        style:num-suffix=". "
        style:num-format="1">
        <style:list-level-properties
            text:list-level-position-and-space-mode="label-alignment">
            <style:list-level-label-alignment
                text:label-followed-by="listtab"
                fo:margin-left="1.27cm"
                fo:text-indent="-0.635cm"/>
        </style:list-level-properties>
    </text:list-level-style-number>
</text:list-style>
```

## Patterns d'image

### Image inline
```xml
<text:p text:style-name="Standard">
    <draw:frame draw:style-name="fr1"
                draw:name="Image1"
                text:anchor-type="as-char"
                svg:width="5cm"
                svg:height="3cm">
        <draw:image xlink:href="Pictures/image1.png"
                    xlink:type="simple"
                    xlink:show="embed"
                    xlink:actuate="onLoad"/>
    </draw:frame>
</text:p>
```

## Patterns pour zones de reponse eleve

### Pointilles grises
```xml
<text:p text:style-name="_5f_Paragraphe_5f_Reponse_5f_Pointilles_5f_Grises">
    <text:s text:c="80"/>
</text:p>
```

### Zone de reponse avec hauteur
```xml
<style:style style:name="_5f_Paragraphe_5f_Reponse_5f_Eleve" style:family="paragraph">
    <style:paragraph-properties
        fo:line-height="0.7cm"
        fo:text-align="start">
        <style:tab-stops>
            <style:tab-stop style:position="8.999cm"
                           style:type="right"
                           style:leader-style="dotted"
                           style:leader-text="."/>
        </style:tab-stops>
    </style:paragraph-properties>
    <style:text-properties fo:color="#b3b3b3"/>
</style:style>
```

## Manipulation Python avec xml.etree

```python
import zipfile
from xml.etree import ElementTree as ET

# Namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
}

# Lire content.xml
with zipfile.ZipFile('document.odt', 'r') as z:
    content = z.read('content.xml').decode('utf-8')

root = ET.fromstring(content)

# Trouver tous les paragraphes
for p in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
    style = p.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name')
    text = ''.join(p.itertext())
    print(f"Style: {style}, Texte: {text[:50]}")

# Modifier un paragraphe
for p in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
    if "ancien texte" in ''.join(p.itertext()):
        p.clear()
        p.text = "nouveau texte"
        p.set('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name', 'Standard')
```

## Validation ODT

Pour verifier qu'un fichier ODT est valide:
1. Le fichier `mimetype` doit etre non compresse et en premiere position
2. Les namespaces doivent etre correctement declares
3. Tous les styles references doivent exister
4. Le fichier doit s'ouvrir sans erreur dans LibreOffice
