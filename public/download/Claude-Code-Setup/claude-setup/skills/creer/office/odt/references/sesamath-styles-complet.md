# Catalogue complet des styles Sesamath pour ODT

Ce document decrit en detail les styles educatifs Sesamath extraits des cahiers officiels.

## Architecture visuelle des environnements pedagogiques

Les environnements pedagogiques Sesamath utilisent un systeme de **bordure gauche coloree** pour identifier visuellement le type de contenu :

```
+--+--------------------------------------------------+
|  |                                                  |
|B |  Contenu de l'environnement                     |
|O |  (Definition, Propriete, Methode, etc.)         |
|R |                                                  |
|D |                                                  |
+--+--------------------------------------------------+
```

### Couleurs par type d'environnement

| Environnement | Couleur bordure | Code hex | Fond titre |
|---------------|-----------------|----------|------------|
| Definition | Vert | #77bc65 | #00a933 |
| Vocabulaire | Vert | #77bc65 | #00a933 |
| Propriete | Rose | #ec9ba4 | #bf0041 |
| Methode | Bleu | #729fcf | #2a6099 |
| Remarque | Turquoise | #78bbb2 | #50938a |
| Exemple | Gris | #000000 | #eeeeee |

### Structure complete d'un environnement

Un environnement Sesamath se compose de :

1. **Titre** (style `_Caracteres_Titre_*`) :
   - Texte blanc gras
   - Fond colore (background-color)
   - Petite bordure noire (0.06pt)
   - Padding de 0.049cm

2. **Corps** (style `_Paragraphe_*`) :
   - Bordure gauche epaisse (4.51pt solid)
   - Padding de 0.25cm
   - Line-height 115%
   - Marges haut/bas de 0.049cm

3. **Puces** (style `_Paragraphe_*_bullet`) :
   - Memes proprietes que le corps
   - Pour les listes a puces dans l'environnement

## Dictionnaire des styles Python

```python
# -*- coding: utf-8 -*-
"""
Dictionnaire des styles Sesamath pour utilisation avec odfpy.

Les noms contiennent des caracteres accentues encodes en UTF-8.
"""

SESAMATH_STYLES = {
    # =========================================================================
    # PARAGRAPHES DE BASE
    # =========================================================================
    'paragraphe': {
        'name': '_5f_Paragraphe',
        'family': 'paragraph',
        'description': 'Texte courant standard',
        'margins': {'left': '0cm', 'right': '0.101cm', 'top': '0.101cm', 'bottom': '0.101cm'},
        'font': {'size': '10pt', 'family': 'Bitstream Vera Sans'},
    },

    # =========================================================================
    # VOCABULAIRE (bordure verte #77bc65)
    # =========================================================================
    'titre_vocabulaire': {
        'name': '_5f_Titre_5f_Vocabulaire',
        'family': 'paragraph',
        'description': 'Titre de bloc vocabulaire',
    },
    'para_vocabulaire': {
        'name': '_5f_Paragraphe_5f_Vocabulaire',
        'family': 'paragraph',
        'description': 'Contenu bloc vocabulaire',
        'border': {'left': '4.51pt solid #77bc65'},
        'padding': '0.25cm',
    },
    'para_vocabulaire_bullet': {
        'name': '_5f_Paragraphe_5f_Vocabulaire_5f_bullet',
        'family': 'paragraph',
        'description': 'Puce dans bloc vocabulaire',
    },
    'car_titre_vocabulaire': {
        'name': '_5f_Caractères_5f_Titre_5f_Vocabulaire',
        'family': 'text',
        'description': 'Style du texte titre vocabulaire',
        'background': '#00a933',
        'color': 'white',
        'font_weight': 'bold',
    },

    # =========================================================================
    # DEFINITION (bordure verte #77bc65)
    # =========================================================================
    'titre_definition': {
        'name': '_5f_Titre_5f_Définition',
        'family': 'paragraph',
        'description': 'Titre de bloc definition',
    },
    'para_definition': {
        'name': '_5f_Paragraphe_5f_Définition',
        'family': 'paragraph',
        'description': 'Contenu bloc definition',
        'border': {'left': '4.51pt solid #77bc65'},
        'padding': '0.25cm',
        'line_height': '115%',
    },
    'para_definition_bullet': {
        'name': '_5f_Paragraphe_5f_Définition_5f_bullet',
        'family': 'paragraph',
        'description': 'Puce dans bloc definition',
    },
    'car_titre_definition': {
        'name': '_5f_Caractères_5f_Titre_5f_Définition',
        'family': 'text',
        'description': 'Style du texte titre definition',
        'background': '#00a933',
        'color': 'white',
        'font_weight': 'bold',
        'padding': '0.049cm',
        'border': '0.06pt solid #000000',
    },

    # =========================================================================
    # PROPRIETE (bordure rose #ec9ba4)
    # =========================================================================
    'titre_propriete': {
        'name': '_5f_Titre_5f_Propriété',
        'family': 'paragraph',
        'description': 'Titre de bloc propriete',
        'font_weight': 'bold',
    },
    'para_propriete': {
        'name': '_5f_Paragraphe_5f_Propriété',
        'family': 'paragraph',
        'description': 'Contenu bloc propriete',
        'border': {'left': '4.51pt solid #ec9ba4'},
        'padding': '0.25cm',
    },
    'para_propriete_bullet': {
        'name': '_5f_Paragraphe_5f_Propriété_5f_bullet',
        'family': 'paragraph',
        'description': 'Puce dans bloc propriete',
    },
    'car_titre_propriete': {
        'name': '_5f_Caractères_5f_Titre_5f_Propriété',
        'family': 'text',
        'description': 'Style du texte titre propriete',
        'background': '#bf0041',
        'color': 'white',
        'font_weight': 'bold',
    },

    # =========================================================================
    # METHODE (bordure bleue #729fcf)
    # =========================================================================
    'titre_methode': {
        'name': '_5f_Titre_5f_Méthode',
        'family': 'paragraph',
        'description': 'Titre de bloc methode',
        'font_weight': 'bold',
    },
    'para_methode': {
        'name': '_5f_Paragraphe_5f_Méthode',
        'family': 'paragraph',
        'description': 'Contenu bloc methode',
        'border': {'left': '4.51pt solid #729fcf'},
        'padding': '0.25cm',
        'line_height': '115%',
    },
    'para_methode_bullet': {
        'name': '_5f_Paragraphe_5f_Méthode_5f_Bullet',
        'family': 'paragraph',
        'description': 'Puce dans bloc methode',
    },
    'car_titre_methode': {
        'name': '_5f_Caractères_5f_Titre_5f_Méthode',
        'family': 'text',
        'description': 'Style du texte titre methode',
        'background': '#2a6099',
        'color': 'white',
        'font_weight': 'bold',
    },

    # =========================================================================
    # REMARQUE (bordure turquoise #78bbb2)
    # =========================================================================
    'titre_remarque': {
        'name': '_5f_Titre_5f_Remarque',
        'family': 'paragraph',
        'description': 'Titre de bloc remarque',
    },
    'para_remarque': {
        'name': '_5f_Paragraphe_5f_Remarque',
        'family': 'paragraph',
        'description': 'Contenu bloc remarque',
        'border': {'left': '4.51pt solid #78bbb2'},
        'padding': '0.25cm',
        'line_height': '115%',
    },
    'para_remarque_bullet': {
        'name': '_5f_Paragraphe_5f_Remarque_5f_bullet',
        'family': 'paragraph',
        'description': 'Puce dans bloc remarque',
    },
    'car_titre_remarque': {
        'name': '_5f_Caractères_5f_Titre_5f_Remarque',
        'family': 'text',
        'description': 'Style du texte titre remarque',
        'background': '#50938a',
        'color': 'white',
        'font_weight': 'bold',
    },

    # =========================================================================
    # EXEMPLE (fond gris #eeeeee)
    # =========================================================================
    'titre_exemple': {
        'name': '_5f_Titre_5f_Exemple',
        'family': 'paragraph',
        'description': 'Titre de bloc exemple',
    },
    'para_exemple': {
        'name': '_5f_Paragraphe_5f_Exemple',
        'family': 'paragraph',
        'description': 'Contenu bloc exemple',
    },
    'para_exemple_avec_titre': {
        'name': '_5f_Paragraphe_5f_Exemple_5f_avec_5f_Titre',
        'family': 'paragraph',
        'description': 'Exemple avec titre',
        'background': '#eeeeee',
        'border': '0.06pt solid #000000',
        'padding': '0.049cm',
    },
    'para_exemple_sans_titre': {
        'name': '_5f_Paragraphe_5f_Exemple_5f_sans_5f_Titre',
        'family': 'paragraph',
        'description': 'Exemple sans titre',
        'background': '#eeeeee',
        'border': '0.06pt solid #000000',
    },
    'car_titre_exemple': {
        'name': '_5f_Caractères_5f_Titre_5f_Exemple',
        'family': 'text',
        'description': 'Style du texte titre exemple',
    },

    # =========================================================================
    # EXERCICES
    # =========================================================================
    'titre_exercice_avec_titre': {
        'name': '_5f_Titre_5f_Exercices_5f_avec_5f_Titre',
        'family': 'paragraph',
        'description': 'Titre exercice avec nom',
        'font_size': '12pt',
        'font_weight': 'bold',
        'margins': {'top': '0.3cm', 'bottom': '0.101cm'},
    },
    'titre_exercice_sans_titre': {
        'name': '_5f_Titre_5f_Exercices_5f_sans_5f_Titre',
        'family': 'paragraph',
        'description': 'Titre exercice numerote seul',
    },
    'premier_titre_exercice': {
        'name': '_5f_Premier_5f_Titre_5f_Exercices_5f_avec_5f_Num_5f_Exo_5f_sans_5f_Titre',
        'family': 'paragraph',
        'description': 'Premier exercice de la page',
    },
    'para_num_question': {
        'name': '_5f_Paragraphe_5f_avec_5f_Num_5f_Question',
        'family': 'paragraph',
        'description': 'Question numerotee (1., 2., 3.)',
    },
    'car_numero_exercice': {
        'name': '_5f_Numéros_20_exercices',
        'family': 'text',
        'description': 'Numero exercice en jaune',
        'background': '#e8c32a',
        'border': '0.2pt double #e8c32a',
    },

    # =========================================================================
    # REPONSES ELEVE
    # =========================================================================
    'para_reponse_eleve': {
        'name': '_5f_Paragraphe_5f_Réponse_5f_Elève',
        'family': 'paragraph',
        'description': 'Zone de reponse eleve',
        'line_height': '0.7cm',
        'color': '#b3b3b3',
    },
    'para_reponse_eleve_bullet': {
        'name': '_5f_Paragraphe_5f_Réponse_5f_Elève_5f_Bullet',
        'family': 'paragraph',
        'description': 'Reponse eleve avec puce',
    },
    'para_reponse_pointilles': {
        'name': '_5f_Paragraphe_5f_Réponse_5f_Pointillés_5f_Grisés',
        'family': 'paragraph',
        'description': 'Lignes pointillees grises',
        'color': '#b3b3b3',
    },
    'para_reponse_pointilles_bordure': {
        'name': '_5f_Paragraphe_5f_Réponse_5f_Pointillés_5f_Grisés_5f_avec_5f_bordure_5f_supérieure',
        'family': 'paragraph',
        'description': 'Pointilles avec bordure en haut',
        'border': {'top': '0.06pt solid #000000'},
    },
    'para_reponse_fraction': {
        'name': '_5f_Paragraphe_5f_Réponse_5f_Elève_5f_Fraction',
        'family': 'paragraph',
        'description': 'Zone reponse pour fractions (hauteur adaptee)',
    },
    'para_reponse_fraction_numerote': {
        'name': '_5f_Paragraphe_5f_Réponse_5f_Elève_5f_Fraction_5f_Numéroté',
        'family': 'paragraph',
        'description': 'Zone fraction numerotee',
    },

    # =========================================================================
    # TABLEAUX
    # =========================================================================
    'tableau_centre': {
        'name': '_5f_Tableau_5f_Centré',
        'family': 'paragraph',
        'description': 'Cellule tableau centree',
        'text_align': 'center',
    },
    'tableau_gauche': {
        'name': '_5f_Tableau_20_Gauche',
        'family': 'paragraph',
        'description': 'Cellule tableau alignee a gauche',
    },
    'tableau_droit': {
        'name': '_5f_Tableau_20_Droit',
        'family': 'paragraph',
        'description': 'Cellule tableau alignee a droite',
    },
    'tableau_centre_gras': {
        'name': '_5f_Tableau_5f_Centré_5f_Gras',
        'family': 'paragraph',
        'description': 'Cellule tableau centree en gras (en-tetes)',
        'font_weight': 'bold',
    },
    'tableau_centre_gras_vertical': {
        'name': '_5f_Tableau_5f_Centré_5f_Gras_5f_Vertical',
        'family': 'paragraph',
        'description': 'Cellule en-tete rotation 270 degres',
    },
    'tableau_pointilles': {
        'name': '_5f_Tableau_5f_Pointillés_5f_Grisés',
        'family': 'paragraph',
        'description': 'Cellule avec pointilles (a completer)',
    },

    # =========================================================================
    # CORRECTION
    # =========================================================================
    'para_correction': {
        'name': '_5f_Paragraphe_5f_Correction',
        'family': 'paragraph',
        'description': 'Paragraphe de correction',
    },
    'car_correction': {
        'name': '_5f_Caractères_5f_correction',
        'family': 'text',
        'description': 'Texte de correction (rouge gras)',
        'color': '#FF0000',
        'font_weight': 'bold',
    },

    # =========================================================================
    # CARACTERES SPECIAUX
    # =========================================================================
    'car_gras': {
        'name': '_5f_Caractères_5f_gras',
        'family': 'text',
        'description': 'Texte en gras',
        'font_weight': 'bold',
    },
    'car_encadre': {
        'name': '_5f_Caractères_5f_encadré',
        'family': 'text',
        'description': 'Texte encadre',
        'border': '0.06pt solid #000000',
        'padding': '0.049cm',
    },
    'car_indice': {
        'name': '_5f_Caractères_5f_indice',
        'family': 'text',
        'description': 'Texte en indice',
    },
    'car_exposant': {
        'name': '_5f_Caractères_5f_exposant',
        'family': 'text',
        'description': 'Texte en exposant',
    },

    # =========================================================================
    # DOMAINES MATHEMATIQUES
    # =========================================================================
    'para_geometrie': {
        'name': '_5f_Paragraphe_5f_Geometrie_5f_Clr_5f_1ca2b8',
        'family': 'paragraph',
        'description': 'Paragraphe domaine geometrie',
        'color': '#1ca2b8',
    },
    'para_numerique': {
        'name': '_5f_Paragraphe_5f_Numerique_5f_Clr_5f_d7e12c',
        'family': 'paragraph',
        'description': 'Paragraphe domaine numerique',
        'color': '#d7e12c',
    },
    'para_mesures': {
        'name': '_5f_Paragraphe_5f_Mesures_5f_Clr_5f_7fb241',
        'family': 'paragraph',
        'description': 'Paragraphe domaine mesures',
        'color': '#7fb241',
    },
    'para_gestion_donnees': {
        'name': '_5f_Paragraphe_5f_Gestion_5f_de_5f_donnee_5f_Clr_5f_9d0f89',
        'family': 'paragraph',
        'description': 'Paragraphe domaine gestion donnees',
        'color': '#9d0f89',
    },
    'para_problemes': {
        'name': '_5f_Paragraphe_5f_Problemes_5f_Clr_5f_d62e4e',
        'family': 'paragraph',
        'description': 'Paragraphe domaine problemes',
        'color': '#d62e4e',
    },
}

# Raccourcis pour acces rapide par type
STYLES_BY_TYPE = {
    'definition': ['titre_definition', 'para_definition', 'para_definition_bullet', 'car_titre_definition'],
    'propriete': ['titre_propriete', 'para_propriete', 'para_propriete_bullet', 'car_titre_propriete'],
    'methode': ['titre_methode', 'para_methode', 'para_methode_bullet', 'car_titre_methode'],
    'remarque': ['titre_remarque', 'para_remarque', 'para_remarque_bullet', 'car_titre_remarque'],
    'exemple': ['titre_exemple', 'para_exemple', 'para_exemple_avec_titre', 'para_exemple_sans_titre'],
    'vocabulaire': ['titre_vocabulaire', 'para_vocabulaire', 'para_vocabulaire_bullet', 'car_titre_vocabulaire'],
    'exercice': ['titre_exercice_avec_titre', 'titre_exercice_sans_titre', 'para_num_question', 'car_numero_exercice'],
    'reponse': ['para_reponse_eleve', 'para_reponse_pointilles', 'para_reponse_fraction'],
    'tableau': ['tableau_centre', 'tableau_gauche', 'tableau_droit', 'tableau_centre_gras'],
}

# Couleurs principales
SESAMATH_COLORS = {
    'definition': {'border': '#77bc65', 'title_bg': '#00a933'},
    'vocabulaire': {'border': '#77bc65', 'title_bg': '#00a933'},
    'propriete': {'border': '#ec9ba4', 'title_bg': '#bf0041'},
    'methode': {'border': '#729fcf', 'title_bg': '#2a6099'},
    'remarque': {'border': '#78bbb2', 'title_bg': '#50938a'},
    'exemple': {'background': '#eeeeee', 'border': '#000000'},
    'exercice': {'title_bg': '#e8c32a'},

    # Domaines
    'geometrie': '#1ca2b8',
    'numerique': '#d7e12c',
    'mesures': '#7fb241',
    'gestion_donnees': '#9d0f89',
    'problemes': '#d62e4e',
}
```

## En-tetes et pieds de page

Les styles d'en-tete et pied de page sont geres automatiquement par les master pages du template.

| Style | Position | Description |
|-------|----------|-------------|
| `_Header N page paire (G)` | Gauche, page paire | En-tete chapitre Numerique |
| `_Header N page impaire (D)` | Droite, page impaire | En-tete chapitre Numerique |
| `_Header G page paire (G)` | Gauche, page paire | En-tete chapitre Geometrie |
| `_Footer page paire (G)` | Gauche, page paire | Pied de page |
| `_Footer page impaire (D)` | Droite, page impaire | Pied de page |

Les en-tetes utilisent les couleurs des domaines mathematiques.

## Formules mathematiques

Les formules sont gerees via des objets ODF Formula integres :
- Format : MathML avec annotation StarMath
- Voir `scripts/math_formulas.py` pour la syntaxe

## Utilisation recommandee

```python
from odf.opendocument import load
from odf.text import P, Span

# Charger le template
doc = load('template_sesamath_complet.odt')

# Creer un bloc Definition avec titre boxed
titre = P(stylename='_5f_Titre_5f_Définition')
titre_span = Span(stylename='_5f_Caractères_5f_Titre_5f_Définition', text='Definition')
titre.addElement(titre_span)
doc.text.addElement(titre)

# Contenu avec bordure verte
p = P(stylename='_5f_Paragraphe_5f_Définition', text='Une fraction est...')
doc.text.addElement(p)
```
