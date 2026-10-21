"""Règles de traduction LaTeX bfcours → bfcours-typst : LE fichier à modifier quand le paquet change.

Tout ce qui se déduit de l'index des fonctions (noms Typst, clés acceptées, type des arguments, nom LaTeX
de chaque option) n'est PAS écrit ici : le convertisseur le lit à chaque lancement dans l'index, régénéré
depuis les paquets par `regenerer.py`. Ce fichier ne contient que ce que l'index ne peut pas dire :

- les commandes LaTeX renommées ou fusionnées (table « Épurage » de la suite) ;
- le nom des clés que prennent les arguments facultatifs SANS nom (`\\tcbenumerate[2]` → `raster-columns`) ;
- les arguments obligatoires qui deviennent des clés nommées (`\\begin{EXO}{titre}{tags}` → `tags:`) ;
- les commandes à ignorer, les déclarations de taille, les longueurs.

Après une modification d'un paquet : `python regenerer.py` (index, fiches, signatures), puis
`python verifier_convertisseur.py` (banc d'essai) ; si un cas casse, corriger ICI la règle concernée.
"""

# NOMS : les clés des tables « nom LaTeX » restent des noms LaTeX (inchangés) ; tout NOM TYPST (valeurs de
# RENOMMAGES, FORME_ENVIRONNEMENT, clés des tables 2 et 3) est en kebab-case, comme dans la suite depuis le
# 16/10/2026 (`definition`, `exo`, `multi-colonnes`…). Table complète : `scripts/kebab.py`, `donnees/kebab.json`.
#
# ---------------------------------------------------------------------------------------------------------
# 1. Renommages : nom LaTeX → (fonction Typst, clés imposées). Source : table de renommage de la suite.
#    Une commande LaTeX absente d'ici cherche la fonction de même nom (nom LaTeX → nom Typst par `kebab.py`).
# ---------------------------------------------------------------------------------------------------------
RENOMMAGES = {
    "tcbtabc": ("tcbtab", {"align": "center"}),
    "tcbtabx": ("tcbtab", {"couleurs": '"secondaire"'}),
    "tcbtabcomp": ("tcbtab", {"style": '"CompTab"', "align": "none"}),
    "tcautocrep": ("tccrep", {}),            # \tcautocrep{x} → tccrep(auto)[x]
    "Colonnes": ("multi-colonnes", {}),
    "tcbitemize": ("tcbraster", {}),
    "tcbitempoint": ("itempoint", {}),
    "dystcbitempoint": ("itempoint", {"dys": "true"}),
    "exo": ("exo", {}),
    "exoeval": ("exo-eval", {}),
    "formuleTable": ("encadrer", {"couleur": '"red"'}),
    "wrapfigure": ("habiller", {}),
    "DecompFPA": ("decomp-fp", {"mise-en-page": '"etapes"'}),
    "DecompFPB": ("decomp-fp", {"mise-en-page": '"arbre"'}),
    "DecompFPC": ("decomp-fp", {"mise-en-page": '"tableau"'}),
    "Theo": ("theoreme", {}),
    "TheoA": ("theoreme", {}),
    "Needspace": ("needspace", {}),
}

# ---------------------------------------------------------------------------------------------------------
# 1 bis. Syntaxe environnement : un `\begin{X}…\end{X}` LaTeX dont la fonction Typst a la forme environnement
#    s'écrit `#begin(X, clés)[blocs fixes]` … `#end(X)` (corps indenté entre les deux). Les autres
#    environnements gardent leur traduction en commande (`#geo`, `#tcbtab`, `#latex`…).
#    Écartées volontairement : geo, figure-geo (dessins cetz), competence, whitebox, ColoredSmallBox, rdconv,
#    rdtabnum, rdsheet, rdopp, rdtime, rdratio, rdgrid ; tcbtab, tableaucompetence, tableaurecapsequence,
#    habiller, ClipImage, filmbox et les boîtes rd.* restent en commande (cellules ou signatures LaTeX non
#    équivalentes : filets, \multicolumn, texte hors de l'environnement wrapfigure…).
# ---------------------------------------------------------------------------------------------------------
FORME_ENVIRONNEMENT = {
    # farfadet-didactique
    "definition", "propriete", "theoreme", "demonstration", "methode", "activite", "vocabulaire", "solution",
    "exemple", "contre-exemple", "remarque", "notation", "aide", "cracked", "boite", "bfbox", "histoire", "bf-env",
    "boite-figure", "neutre",
    # farfadet-exo
    "exo", "exo-eval", "chapitre-bac", "chapitre-brevet", "exolombards", "encadre-bac", "encadre-bac-etroit",
    # farfadet-enum
    "tcbenumerate", "enumerate", "itemize", "multi-colonnes", "tcbraster",
    # farfadet-crep, farfadet-qcm, farfadet-extras
    "crep", "mcq", "bf-code-python",
}

# Fonctions dont le corps est une suite d'items : puce de chaque item (`+` numérotés, `-` cellules).
PUCE_ITEMS = {"tcbenumerate": "+", "enumerate": "+", "itemize": "-", "multi-colonnes": "-", "tcbraster": "-"}

# ---------------------------------------------------------------------------------------------------------
# 2. Arguments facultatifs sans nom → clés, dans l'ordre des crochets (règle R3).
#    `None` : l'argument est ignoré. Un argument facultatif écrit « clé=valeur » est toujours lu comme
#    une liste de clés, quelle que soit cette table. Un argument facultatif d'un environnement didactique
#    (`\\begin{Definition}[Titre]`) qui n'est pas dans cette table devient le titre (contenu positionnel).
# ---------------------------------------------------------------------------------------------------------
OPTIONNELS_NOMMES = {
    "tcbenumerate": ["raster-columns", "depart", "format"],
    "acc": ["couleur"],
    "encadrer": ["couleur"],
    "surligner": ["couleur"],
    "coordonnees": ["nom"],
    "intervalle": ["forme"],
    "competence": ["code"],
    "repsim": ["largeur"],
    "crochetg": ["taille"],
    "crochetd": ["taille"],
    "mcq": ["format"],
    "chapitre": ["niveau"],
    "chap-eval": ["niveau"],
    "itempoint": ["dy", "dx"],
    "multi-colonnes": [None],     # \begin{MultiColonnes}{n}[style LaTeX] : style sans équivalent
    "crep": [],                  # [clés] seulement
    "pgcd": [], "ppcm": [],
}

# Valeurs des arguments facultatifs sans nom : conversions particulières.
VALEURS_OPTIONNELS = {
    ("tcbenumerate", "format"): {"\\arabic": '"arabic"', "\\alph": '"alph"', "\\Alph": '"Alph"',
                                 "\\roman": '"roman"', "\\Roman": '"Roman"', "auto": '"auto"'},
}

# ---------------------------------------------------------------------------------------------------------
# 3. Arguments obligatoires qui deviennent des clés nommées (dans l'ordre des accolades).
#    `None` : argument gardé en position (contenu). Les autres arguments obligatoires restent positionnels
#    (règle R2), le corps de l'environnement toujours en dernier.
# ---------------------------------------------------------------------------------------------------------
OBLIGATOIRES_NOMMES = {
    "exo": [None, "tags"],
    "exo-eval": [None, "tags"],
    "chapitre": ["theme", "cycle", "etablissement", "zone-droite", "type"],
    "chap-eval": ["theme", "cycle", "etablissement", "apres", "type"],
}

# Clés qui prennent une CHAÎNE (et non un contenu) quand elles viennent d'un argument obligatoire.
CLES_CHAINES = {("exo", "tags"), ("exo-eval", "tags")}

# ---------------------------------------------------------------------------------------------------------
# 4. Clés LaTeX à ne jamais reporter (la version vient de `--input correction=…`, les overlays TikZ n'ont
#    pas d'équivalent…). Valeur : la raison, écrite dans le rapport.
# ---------------------------------------------------------------------------------------------------------
CLES_IGNOREES = {
    "correction": "la version professeur / élève vient de la compilation (--input correction=…)",
    "overlay": "overlay TikZ sans équivalent (étiquettes : setrdexo(display-tags: …))",
    "save lower": "sans effet en Typst",
    "score": "calculé par Typst (somme des itempoint)",
    "level": "niveau : #rdifficulty(n) avant l'exercice",
}

# ---------------------------------------------------------------------------------------------------------
# 5. Commandes LaTeX sans effet en Typst : supprimées (le nombre est donné dans le rapport).
# ---------------------------------------------------------------------------------------------------------
IGNOREES = {
    "setcounter", "stepcounter", "addtocounter", "refstepcounter", "hypersetup", "pgfplotsset",
    "usetikzlibrary", "tcbset", "noindent", "indent", "raggedbottom", "flushbottom", "relax", "protect",
    "nopagebreak", "allowbreak", "selectlanguage", "frenchsetup", "setlength", "addtolength", "pagestyle",
    "thispagestyle", "sisetup", "tikzset", "definecolor", "colorlet", "newif", "makeatletter", "makeatother",
    "ignorespaces", "unskip", "leavevmode", "strut", "linespread", "graphicspath", "bfFinFichier",
    "normalsize", "normalfont", "rmfamily", "mdseries", "upshape", "raggedright", "raggedleft", "justifying",
    "label", "nonumber", "notag", "global", "everymath", "displaystyle", "setboolean", "setbool",
    "providecommand", "DeclareMathOperator", "newtcolorbox", "newenvironment", "renewenvironment",
    "NewDocumentCommand", "RenewDocumentCommand", "DeclareDocumentCommand", "newcounter",
}

# Déclarations qui valent jusqu'à la fin du groupe : le reste du groupe est enveloppé.
TAILLES = {  # rapport à la taille du texte, comme en LaTeX à 11-12 pt
    "tiny": "0.5em", "scriptsize": "0.7em", "footnotesize": "0.8em", "small": "0.9em",
    "large": "1.2em", "Large": "1.44em", "LARGE": "1.728em", "huge": "2.07em", "Huge": "2.49em",
}
GRAISSES = {"bfseries": "strong", "itshape": "emph", "slshape": "emph", "em": "emph", "scshape": "smallcaps",
            "ttfamily": None, "sffamily": None}

# Espaces verticaux nommés (≈ 6 pt pour \medskip à 12 pt).
ESPACES_V = {"smallskip": "0.25em", "medskip": "0.5em", "bigskip": "1em"}

# ---------------------------------------------------------------------------------------------------------
# 6. Environnements et commandes rendus en extrait LaTeX (`#latex[…]`, compilé à l'enregistrement) :
#    figures et constructions sans équivalent Typst. Paquets à charger pour chacun.
# ---------------------------------------------------------------------------------------------------------
EXTRAITS = {
    "tikzpicture": ("tikz",), "tikzcd": ("tikz-cd",), "circuitikz": ("circuitikz",), "forest": ("forest",),
    "axis": ("pgfplots",), "pspicture": ("pstricks-add",), "pspicture*": ("pstricks-add",),
    "scratch": ("scratch3",), "Tableur": ("bfcours",), "tablvar": ("tablvar",), "variations": ("tabvar",),
    "longtblr": ("tabularray",), "bclogo": ("bclogo",), "asy": ("asymptote",),
}
COMMANDES_EXTRAITS = {"qrcode": ("qrcode",), "tikz": ("tikz",), "psplot": ("pstricks-add",),
                      "pstricks": ("pstricks-add",)}
# Moteur imposé (sinon : moteur par défaut de bfwatch, LuaLaTeX).
MOTEURS = {"pspicture": "xelatex", "pspicture*": "xelatex"}

# Bibliothèques TikZ chargées pour tout extrait TikZ (celles que bfcours charge lui-même).
BIBLIOTHEQUES_TIKZ = ("calc", "arrows.meta", "patterns", "decorations.pathreplacing", "decorations.markings",
                      "intersections", "positioning", "shapes.geometric", "angles", "quotes", "backgrounds",
                      "through")

# Commandes qui, dans un extrait, obligent à charger bfcours (macros du paquet LaTeX).
MARQUEURS_BFCOURS = ("\\tccrep", "\\crep", "\\tcfillcrep", "\\repsim", "\\Vecteur", "\\Coordonnees", "\\acc",
                     "\\encadrer", "\\ifcorrection", "\\tcbitem", "\\MultiColonnes", "\\Rep", "\\XAxe", "\\YAxe",
                     "\\origine", "\\point", "\\placerpoint", "\\tkzTab", "\\Mcq", "\\tcbenumerate",
                     "\\begin{crep}", "\\np", "\\CrochetG", "\\CrochetD", "\\intervalle", "\\couleur")

# ---------------------------------------------------------------------------------------------------------
# 7. Libellés courts du bandeau (clé `niveau`) : texte LaTeX nettoyé → valeur Typst.
# ---------------------------------------------------------------------------------------------------------
NIVEAUX = {"6e": "6e", "6eme": "6e", "6ème": "6e", "5e": "5e", "5eme": "5e", "5ème": "5e", "4e": "4e",
           "4eme": "4e", "4ème": "4e", "3e": "3e", "3eme": "3e", "3ème": "3e", "2nde": "2nde", "2de": "2nde",
           "2nd": "2nde", "1re": "1re", "1ere": "1re", "1ère": "1re", "1er": "1re", "Tle": "Tle", "Term": "Tle",
           "T": "Tle", "Terminale": "Tle"}

# Libellé de type de document (dernier argument de \chapitre) → valeur de la clé `type-document` du modèle.
# Un type connu suivi de « : » (« Cours : ») devient le type court : « : » est le séparateur par défaut du modèle.
TYPES_DOCUMENT = {"cours": '"cours"', "exercices": '"exercices"', "exercice": '"exercices"',
                  "activité": '"activite"', "activite": '"activite"', "fiche": '"fiche"', "devoir": None,
                  "évaluation": '"evaluation"', "evaluation": '"evaluation"'}
