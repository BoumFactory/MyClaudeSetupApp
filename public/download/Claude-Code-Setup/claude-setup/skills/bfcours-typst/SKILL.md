---
name: bfcours-typst
description: Skill par défaut pour tout travail en Typst — écrire, compiler, corriger ou relire un fichier .typ, comprendre une erreur de compilation (unknown variable, expected content…), traduire du LaTeX en Typst — et surtout pour les documents de maths faits avec la suite farfadet (@preview/farfadet) - cours avec Définition, Propriété, Exemple, Méthode ; fiches d'exercices EXO avec corrigés ; évaluations avec barème itempoint et compétences ; zones de réponse crep et lignes Seyès ; QCM ; tableaux tcbtab ; colonnes ; figures de géométrie ; versions prof et élève d'un même fichier. Préconvertit un .tex bfcours en .typ prêt à retoucher (convertir.py), compile prof, élève et extraits LaTeX comme l'extension VS Code (compiler.py), trouve la bonne fonction ou clé (chercher.py, aussi par nom de commande LaTeX) et donne des documents complets à imiter. Utiliser dès que l'utilisateur mentionne Typst, un fichier .typ, Tinymist, bfcours en Typst ou veut convertir un document LaTeX en Typst, même sans dire « bfcours ».
---

# Typst et la suite farfadet

Ce skill sert à tout travail en Typst. Il apporte :

- **le langage** : `references/typst-essentiel.md` (modes, `set`/`show`, `context`, maths, correspondance LaTeX → Typst, pièges, lecture d'une erreur). À lire dès qu'on n'est pas sûr d'une syntaxe ;
- **la suite farfadet** : vingt-deux paquets réunis par le méta-paquet `@preview/farfadet:0.2.0`, qui reprennent les commandes LaTeX de bfcours sous des **noms en kebab-case** (`\Definition` → `#definition`, `\begin{EXO}` → `#exo`, `\MultiColonnes` → `#multi-colonnes`, `\Vecteur` → `vect` en maths ; une option devient une clé, espaces → tirets). Les NOMS LaTeX ne changent pas, et les chaînes (`pour: "Definition"`) non plus ; `chercher.py` et `kebab.py` retrouvent une fonction par son ancien nom (`EXO`, `MultiColonnes`, `tkzTabLine`) ;
- **des scripts** : diagnostic de l'installation, compilation prof + élève, recherche dans l'index des fonctions, préconversion d'un `.tex`.

Il ne met pas tout en mémoire : il donne une **carte** des besoins courants, une **recherche** précise (`chercher.py`) et des **documents complets à imiter** (`recettes/`). Une clé ne se devine jamais : elle se cherche, parce qu'une clé inconnue arrête la compilation.

## Comment lire les commandes de ce skill

- `<skill>` désigne le dossier de ce skill (celui qui contient ce `SKILL.md`). Écrire son chemin réel, entre guillemets.
- `python` désigne **le Python qui a le module `typst`** (un venv, ou le Python du système). Si une commande échoue sur `import typst`, c'est le mauvais Python : `localiser.py` le dit.
- Les scripts ne contiennent aucun chemin propre à un poste : ils retrouvent eux-mêmes paquets, polices et outils.

## Installation et diagnostic

À lancer au premier usage sur un poste, et dès qu'une compilation échoue sans raison visible :

```bash
python "<skill>/scripts/localiser.py"
```

Il affiche ce qui est trouvé et ce qui manque :

| Ligne | Si elle manque |
|---|---|
| module typst | `pip install typst` dans ce Python |
| version de farfadet, paquet du cache `@preview` | installer la suite : l'installateur du dépôt bfcours-typst (`installer.ps1` sous Windows, `installer.sh` ailleurs), puis `python tools/installer.py --verifier` pour le bilan |
| polices | facultatives : sans elles, Typst compose avec ses polices intégrées (Libertinus Serif, New Computer Modern Math) et les formules ont la bonne taille. Pour le rendu Erewhon du professeur, l'installateur les déclare ; sinon définir `BFCOURS_TYPST_POLICES` vers le dossier `polices/` de la suite |
| bfwatch, rendu des extraits LaTeX | sans eux, `compiler.py` compile quand même les deux versions, mais sans rendre les extraits `#latex[…]` |
| LaTeX (extraits) | facultatif : seulement pour rendre les extraits `#latex[…]` (figures TikZ gardées telles quelles) |
| PyMuPDF | facultatif : images de contrôle (`pip install pymupdf`) |

`python "<skill>/scripts/localiser.py" --json` donne la même chose en JSON, avec le dossier réel de la suite (on y trouve les guides PDF de chaque paquet, `docs/<paquet>.pdf`). Installer ou configurer VS Code (extension, extraits de code, polices, réglages Tinymist, skill) : suivre `references/setup-vscode.md`.

## Règle forte : travailler dans le dossier que l'utilisateur indique

L'utilisateur range ses documents lui-même. Il veut retrouver le `.typ`, ses PDF et ses images là où il l'a dit, et rien ailleurs. Donc :

- « Travaille dans `xxx/` » : **tous** les fichiers vont dans `xxx/` (`.typ`, PDF prof et élève, `images/` copiées, cache `rendus-tex/`).
- « Place le `.typ` dans `yyy/` » alors que la source est dans `xxx/` : on travaille dans `yyy/` (`convertir.py source.tex -o yyy/`) et **on ne crée rien dans `xxx/`**.
- Le livrable ne passe jamais par un dossier temporaire : les PDF s'écrivent à côté du `.typ`, là où l'utilisateur les ouvrira, et l'extension VS Code y écrira les mêmes au Ctrl+Maj+B (le Ctrl+S, lui, ouvre l'aperçu en direct).
- Un essai jetable (petit `.typ` pour tester une syntaxe) va dans le dossier de travail et se supprime à la fin. En fin de travail, `compiler.py <doc>.typ --nettoyer` retire les images de contrôle (`.apercu/`). On garde `rendus-tex/` : c'est le cache des extraits LaTeX.
- **Les `.tex` d'origine ne se modifient jamais** : ils restent la référence de l'utilisateur.
- Sans dossier indiqué : pour un document, prendre le dossier de la source ou celui que la conversation désigne, et le dire ; pour vérifier la réponse à une simple question de syntaxe, un essai dans un dossier temporaire de session suffit, puisque rien n'est livré.

## Compiler : professeur, élève et extraits LaTeX

Un même fichier donne les deux versions. La version professeur montre les réponses en couleur et les corrigés ; la version élève garde les mêmes places, vides.

```bash
python "<skill>/scripts/compiler.py" "dossier/doc.typ" --png        # doc-prof.pdf, doc-eleve.pdf, images
python "<skill>/scripts/compiler.py" "dossier/doc.typ" --png --ppi 110
python "<skill>/scripts/compiler.py" "dossier/doc.typ" --version eleve
python "<skill>/scripts/compiler.py" "dossier/chapitre2.typ"         # fragment inclus : le maître est retrouvé
python "<skill>/scripts/compiler.py" "dossier/doc.typ" --nettoyer   # fin de travail : retire .apercu/
```

- Moteur : `bfwatch` de la suite, donc **exactement** ce que l'utilisateur obtient au Ctrl+Maj+B avec l'extension VS Code `bfcours-typst` : `-prof.pdf`, `-eleve.pdf`, extraits `#latex[…]` rendus par LaTeX et mis en cache dans `rendus-tex/`. Les deux versions se compilent en parallèle.
- Si une fenêtre VS Code travaille sur un `.typ` avec l'extension, `compiler.py` passe par son service partagé (ligne « service bfwatch de VS Code ») : compilateurs et cache déjà chauds, moins d'une seconde sur un document déjà vu. Il ne s'y inscrit pas : le service vit tant qu'une fenêtre VS Code l'utilise et s'arrête 30 s après la dernière. Sinon `compiler.py` compile lui-même, à froid (3 à 10 s pour un cours). `--sans-service` force la compilation locale.
- Images : `.apercu/doc-prof/page-01.png`… et `.apercu/doc-eleve/…`. **Regarder les images des deux versions avant de livrer** : une compilation réussie ne dit rien d'un débordement, d'une réponse visible chez l'élève ou d'une figure vide.
- En cas d'erreur, le diagnostic complet s'affiche (fichier:ligne:colonne, indices). Lecture : `references/typst-essentiel.md`, section 10.
- Une compilation dure une à dix secondes : compiler souvent, par petits morceaux.
- L'extension VS Code `bfcours-typst` (0.6.0) n'a que deux gestes : **Ctrl+S** = aperçu Tinymist en direct (version professeur, Ctrl+clic → code) ; **Ctrl+Maj+B** (fichier `.typ`) = tout : extraits LaTeX nouveaux ou modifiés, puis PDF prof et élève. Un seul service bfwatch pour toute la session et toutes les fenêtres VS Code (la seconde fenêtre se branche sur celui de la première) ; le document de l'onglet actif est préchauffé à chaque changement d'onglet : même le premier Ctrl+Maj+B ne coûte qu'une compilation incrémentale. Mémoire : deux compilateurs (prof, élève) qui changent de document, cache de Typst commun, bornée par le plus gros document (1 à 2,5 Go), mémoire vive rendue à Windows après une minute sans requête ; arrêt 30 s après la fermeture de la dernière fenêtre. Réglages : volet de l'extension (`bfcoursTypst.*`) et `tools/bfwatch.json`.

Dans le document : `#ifcorrection[prof][élève]`, `#ifcorrection[prof]` (rien chez l'élève), `#ifcorrection[][élève]`, et `context ifcorrection()` pour le booléen. Ne pas lire `sys.inputs` soi-même.

## Document minimal

```typ
#import "@preview/farfadet:0.2.0": *

#show: modele(
  "cours",
  niveau: "2nde",                 // "6e" … "3e", "2nde", "1re", "Tle", ou un texte
  theme: [Vecteurs du plan],
  type-document: "cours",         // "cours", "exercices", "activite", "fiche", "evaluation"
  cycle: [Lycée],
  etablissement: [du Parc],
)

= Repérage dans le plan
#definition[Repère][Un repère du plan est la donnée de trois points $O$, $I$, $J$ non alignés.]
#exo(level: 1)[Une équation][
  Résoudre $3 x + 5 = 17$.
  #crep(extra-lines: 1)[$3 x = 12$, donc $x = 4$.]
  #exocorrection
  $3 x = 12$, donc $x = 4$.
]
#ifcorrection[#rdexocorrection(0)]   // corrigés à la fin, version professeur seulement
```

Toutes les clés du modèle : `chercher.py --fiche modele`. Avant un document d'un type courant, ouvrir la recette qui lui correspond (plus bas).

## La carte : je veux… → fonction

La table des besoins courants (page, définition, exercice, évaluation, zones de réponse, QCM, tableaux, maths, skins, figures, tableaux de variations, extraits LaTeX, diaporamas…) est dans `references/carte-des-besoins.md` : **la lire dès qu'on cherche la fonction d'un besoin**, avant `chercher.py`. Tout autre besoin : `chercher.py "<besoin en mots>"`.

## Chercher (ne jamais deviner une clé)

```bash
python "<skill>/scripts/chercher.py" "conversion d'unités"   # je veux faire X : fonctions classées
python "<skill>/scripts/chercher.py" --latex tcbtabc         # équivalent d'une commande LaTeX (renommages compris)
python "<skill>/scripts/chercher.py" --fiche exo             # tout sur une fonction : signature, clés, valeurs, exemple
python "<skill>/scripts/chercher.py" --paquet rdopp          # les fonctions d'un paquet
python "<skill>/scripts/chercher.py" --cle position          # les fonctions qui acceptent une clé
```

- **Fiches par paquet** : `references/paquets/<paquet>.md` (liste : `references/paquets/INDEX.md`), utiles quand on travaille longtemps avec un paquet. Elles sont générées : ne pas les éditer.
- **Documentation complète** : `farfadet-documentation.pdf` à la racine de la suite (installation et tous les guides, sommaire général, signets par paquet).
- **Guides par paquet** avec un exemple rendu par fonction : `docs/<paquet>.pdf` dans la suite (dossier donné par `localiser.py`), sources `docs/*.typ` lisibles directement. Le guide du méta-paquet `farfadet` explique l'usage famille par famille et l'installation.

## Personnaliser

Chaque paquet a **un seul setter**, de signature commune `set…(pour: none, definir: none, reinitialiser: false, ..clés)` : `setbfenvironments`, `setbfsections`, `setbfmodele`, `setbfmaths`, `sisetup`, `setbfenum`, `setbftableaux`, `setrdcrep`, `setrdexo`, `setrdmcq`, `setbfextras`, `setbfsocle`, `setbflatex`, et `setrd…` pour chaque paquet rd.

```typ
#setbfenvironments(sommaire: false)                                 // réglage global
#setbfenvironments(pour: "Definition", numero: true)                // un type
#setbfenvironments(definir: "sobre", drop-shadow: false)            // style nommé…
#propriete(style: "sobre")[Titre][Corps]                            // …appelé par style:
#setrdexo(pour: "itempoint", position: "gauche")                    // les boîtes de points
#setbfcolors(defi: rgb("#c2410c"))                                  // couleur nommée : Definition ET Notation
#setbfenvironments(pour: "Definition", couleur: rgb("#c2410c"))     // Definition seule
#definition(couleur: "teal")[Titre][Corps]                          // cet objet seul
#setbftableaux(align: center)                                       // tous les tcbtab centrés
#setbfcolors(reinitialiser: true)                                   // retour aux couleurs d'origine
```

- Priorité : clé écrite sur l'objet > style nommé > réglage du type > réglage global > défaut. Une clé ou une valeur inconnue arrête la compilation et liste les possibilités : lire le message.
- Couleurs : `setbfcolors` change d'un coup les couleurs nommées de tous les paquets `farfadet-*`. Une couleur peut servir à plusieurs types : `defi` colore `definition` et `notation`, `nota` colore `vocabulaire` et `aide` ; `prop`, `thm`, `ex`, `rem`, `meth`, `demo`, `act` un seul type ; `monrose` les corrections. Les paquets `rd*` se règlent par leur propre setter.
- **Portée** : un setter vaut pour **toute la suite du document**, même écrit dans un bloc `#[…]` (ce sont des états, pas des règles `set`). Revenir en arrière : `set…(reinitialiser: true)`, ou rappeler le setter avec l'ancienne valeur.
- **Identité, en-tête, façade** : un nouvel utilisateur veut ses défauts (établissement, nom, logo, en-tête, pied) dans tous ses documents → lire d'abord `references/facade.md` et suivre sa procédure.

## Pièges

Les pièges du langage lui-même (lettres séparées en maths, `;` dans un appel, virgule décimale, `context`) sont dans `references/typst-essentiel.md`, section 9. Ceux des paquets :

1. **Corrigés visibles chez l'élève** : `rdexocorrection(0)` s'affiche dans les deux versions ; l'entourer de `#ifcorrection[…]`, comme le `\ifcorrection … \fi` du LaTeX.
2. **Points invisibles** : `itempoint` compte les points mais n'affiche ses boîtes qu'après `#displayitempoints(true)`. Écriture : `+ #itempoint(2)[Énoncé.]`, points en tête, texte entre crochets.
3. **`tcbenumerate`, `enumerate`, `itemize`, `multi-colonnes`, `tcbraster` : un seul corps**, un item par `+` (`tcbenumerate`, `enumerate`) ou par `-` (les trois autres). Un bloc par item, `#tcbenumerate[Q1][Q2]`, est refusé (l'erreur montre l'écriture en items). Mélanger `+` et `-` ou écrire du texte avant le premier item est une erreur ; un texte entre deux items est rattaché au précédent.
4. **Colonnes** : `multi-colonnes` ou `tcbenumerate(columns: n)`, jamais `columns()` de Typst, qui ne transmet pas la largeur aux boîtes.
5. **`#tcbitem(…)[…]` s'écrit dans le corps**, à la place d'un `+` ou d'un `-` (`#multi-colonnes(3)[ #tcbitem(halign: "center")[…] - … ]`), jamais `+ #tcbitem(…)` ni entre les parenthèses de la liste (ancienne écriture, refusée).
6. **`#exocorrection` et `#tcblower` sont des marqueurs**, pas des clés d'`exo` (une clé `exocorrection:` arrête la compilation). Une fois chacun, au premier niveau du corps : pas dans une liste, des colonnes, ni après un `#set` écrit dans le corps.
7. **Le contenu d'une `crep` est la réponse** : en couleur chez le professeur, absent chez l'élève. L'énoncé s'écrit avant la `crep`, jamais dedans. La place laissée à l'élève est la hauteur de la réponse rédigée plus `extra-lines` : rédiger la réponse sur autant de lignes (`\`) que l'élève en aura besoin, ou fixer `lines:` / `height:`. Pas de fraction `display` dans une `crep` Seyès (elle déborde de l'interligne) : `12 div (-3)`.
8. **Maths des paquets** : les fonctions de maths s'écrivent dans `$…$` sans `#` (`$coordonnees(1, 2, nom: A)$`) ; `$AB$` est une erreur, écrire `$A B$` ; virgule décimale `$3","5$` ou `#num(3.5)`.
9. **Une fonction sans argument s'appelle avec `()`** : `#si()`, `#pascalc()`, `#printvocindex()`. Sans parenthèses, son nom s'affiche en police machine, sans erreur.
10. **œ au milieu d'un mot** : `c#oe;ur`. Sans le `;`, Typst lit `#oeur` et s'arrête sur « unknown variable ».
11. **`tcbtab` est collé à gauche** par défaut, comme `\tcbtab`, avec des filets horizontaux entre toutes les rangées. Centré : `align: center` (= `\tcbtabc`) ; seulement les filets verticaux de la spécification : `filets: "verticaux"`.
12. **Formules minuscules** sur l'image : le dossier des polices n'a pas été passé. Compiler par `compiler.py` ; sinon `localiser.py`.
13. **`\vspace` négatifs, `\newpage` de calage** du LaTeX : ne pas les reporter ; régler la mise en page sur l'image Typst.
14. **`farfadet-geom`** : toute macro de dessin s'écrit DANS `geo({ … })`. Les points sont des couples `(x, y)`, pas des noms de nœuds. `milieu`, `projete`, `intersection`, `distance` calculent (renvoient un point ou un nombre), ils ne tracent pas. `fleche(A, B)` trace une flèche ; `$vect(A B)$` écrit un vecteur en maths. Un `#let point = …` dans le document masque la fonction importée. `etiquette` écrit du texte libre sans tracer de croix (`point` en trace une) ; son texte est du contenu : `$A$` pour une formule, `[3 cm]` pour du texte.
15. **`farfadet-tabvar`** : nom et hauteur d'une ligne dans `tkz-tab-line`/`tkz-tab-var` (pas de `tkzTabInit`) ; longueurs avec unité (`espcl: 2cm`) ; `"-oo"` est lu comme une formule. Sans `a-completer`, l'élève reçoit le tableau rempli.
16. **Extraits `#latex` absents de l'aperçu Tinymist** : la ligne `lire: p => read(p, encoding: none)` manque dans `setbflatex` (un paquet ne peut pas lire les fichiers du projet). Avec elle, un extrait nouveau ou modifié reste en encadré jusqu'au Ctrl+Maj+B.
17. **`separateur-type: [ - ]`** est lu comme une puce : écrire `" - "`. Le séparateur par défaut est « : » (« Cours : Thème »).
19. **`#begin(f, …)` … `#end(f)`** : on passe la fonction elle-même (`exo`, pas `"exo"`). Un `#begin` sans `#end` arrête la compilation avec le texte qui précède (pas de numéro de ligne). Un `#begin` écrit dans un élément opaque (cellule de `grid`, `block`, `box`, figure, formule) exige `environnements[…]` dans cet élément. `#begin(revelable(definition))` avec `#pause` ne marche pas : garder la commande ou `etapes`. Restent des commandes : `geo`, `figure-geo`, `competence`, `whitebox`, `tccrep` et les autres boîtes de `crep`, `rdopp`, `rdtime`, `rdconv`…

Comportements à vérifier sur l'image :

- question séparée de sa `crep` par un saut de page : `#needspace(7cm)` juste avant l'exercice (il change de page seulement si la place manque ; dans un conteneur : `needspace(…, conteneur: true)`). Le bandeau d'`exo` ne reste jamais seul en bas de page ;
- deux bandeaux `chapitre(…)` sur la même page : le pied porte le dernier ; pour garder le premier, mettre le second en tête de la page suivante (`#pagebreak()`) ;
- une liste `- …` n'obéit pas à `#set list(indent: …)` : `#itemize(leftmargin: 10pt)[ - … - … ]`, ou `#setbfenum(pour: "itemize", leftmargin: …)` ;
- `tableau-eval` et les boîtes qui suivent prennent le réglage `seyes` courant : placer chaque `setrdcrep` au même endroit que dans le LaTeX.

## Documents complets à imiter

`recettes/INDEX.md` liste des documents qui compilent en version professeur et élève : un cours, une fiche d'exercices, une évaluation, un QCM, des objets rd. Avant d'écrire un document d'un de ces types, **ouvrir la recette correspondante** et en reprendre la structure (en-tête, réglages, enchaînement des environnements, corrigés) : c'est plus sûr que de reconstruire de mémoire. Chaque recette commence par un commentaire qui dit ce qu'elle montre. Pour un document destiné aux élèves, les choix de fond (échéances, jeux de données, format de fiche) relèvent du skill `choix-didactiques` s'il est installé.

## Convertir un document LaTeX

### D'abord : la source est-elle écrite avec bfcours ?

`convertir.py` est fait pour les sources **déjà écrites avec bfcours** (`\usepackage{bfcours}`, `\Definition`, `\begin{EXO}`, `\tcbtab`…) : il traduit commande par commande. Sur un `.tex` ordinaire (article, autre paquet de cours, sujet récupéré), il ne produit que du texte brut et des extraits `#latex` : la conversion se fait alors **à la main, par adaptation sémantique**.

1. **Regarder le préambule et quelques lignes du corps** pour trancher (pas besoin de demander si c'est évident).
2. **Ne poser que les questions dont la réponse n'est ni dans la demande ni dans la source**, en une seule fois :
   - la source suit-elle le formalisme bfcours (si le préambule ne le dit pas clairement) ?
   - les figures : garder le dessin LaTeX en extrait `#latex` (fidèle, **défaut**) ou le redessiner en Typst (`farfadet-geom`, cetz) ?
   - faut-il une version élève (corrections cachées, zones de réponse) en plus de la version professeur ?
3. **Défaut sans réponse** : adapter le contenu au formalisme bfcours (un théorème devient `#propriete`, un exercice `#exo`, un tableau `#tcbtab`…), figures gardées en `#latex`, versions prof et élève.

**Source bfcours** : chemins ci-dessous. **Source non bfcours** : confier le travail à **un sous-agent si l'outil en propose, sinon le faire soi-même**. Un modèle intermédiaire suffit (ex. Sonnet chez Anthropic) ; éviter les plus petits modèles, trop peu sûrs pour réorganiser un cours et garder les maths exactes (le plus gros modèle n'est utile que pour une réécriture didactique demandée). Lui donner : le `.tex`, le dossier cible, les réponses aux questions, et la consigne de partir de la recette du même type (`recettes/`), de chercher chaque fonction avec `chercher.py`, de compiler les deux versions avec `compiler.py` et de lister ce qu'il a dû interpréter. Pour un document long, un sous-agent par grande partie, puis un assemblage.

### Conversion simple d'une source bfcours : un seul appel, puis s'arrêter

Quand l'utilisateur demande seulement de convertir un `.tex` bfcours (sans retouche ni relecture demandées), tout tient en **une commande**, sans rien lire d'autre :

```bash
python "<skill>/scripts/convertir.py" "source/Cours.tex" -o "dossier/demandé/" --compiler
```

- Ne lire ni `references/conversion.md`, ni les recettes, ni le `.typ` produit, ni les images : le script convertit, répare, rend les extraits LaTeX et compile les deux versions.
- Répondre en trois lignes à partir de sa sortie : fichiers produits, nombre de pages, entrées « À reprendre » s'il y en a.
- Chaque appel d'outil supplémentaire relit tout le contexte : ne pas ajouter d'étapes (statistiques, chronométrages, vérifications) qui n'ont pas été demandées.
- Seulement si le rapport liste des entrées « À reprendre » ou une erreur, ou si l'utilisateur demande une relecture : passer au processus complet ci-dessous.

### Processus complet (retouches, relecture)

Le chemin principal est la **préconversion automatique** : `convertir.py` écrit un `.typ` qui compile déjà en version professeur et élève, et liste ce qui reste à reprendre. Il ne reste que des retouches.

1. **Préconvertir directement dans le dossier demandé** :
   ```bash
   python "<skill>/scripts/convertir.py" "source/Cours.tex" -o "dossier/de/travail/"
   ```
   Fragment (`\input` isolé) : `--fragment --maitre "source/Maitre.tex"`. Un `.typ` existant n'est remplacé qu'avec `--remplacer` (sinon `-converti.typ`).
2. **Lire le rapport** affiché : compilation, extraits LaTeX, replis, « À reprendre », options écartées, commandes inconnues.
3. **Compiler et regarder** : `compiler.py dossier/de/travail/Cours.typ --png`, puis les images prof ET élève. Les comparer au PDF LaTeX d'origine s'il existe à côté de la source.
4. **Retoucher le `.typ`** : chercher `a-reprendre`, traiter chaque entrée du rapport ; vérifier les extraits `#latex[…]` : les garder (ils sont fidèles), ou redessiner une figure de géométrie plane avec `farfadet-geom` seulement si c'est demandé ou nettement utile.
5. **Relancer** `compiler.py --png`, regarder de nouveau ; à la fin, `--nettoyer`.

Le détail (ce que fait le convertisseur et ce qu'il ne fait pas, lecture du rapport catégorie par catégorie, partie « Solutions » enveloppée dans `ifcorrection`, zones de réponse sorties des formules, tables de correspondance pour retoucher à la main, maintenance du convertisseur quand un paquet change) : `references/conversion.md`.

## Quand un paquet change

```bash
python "<skill>/scripts/regenerer.py"              # index des fonctions, fiches references/paquets/, signatures
```

Ensuite, recompiler un document converti pour vérifier ; une règle à corriger se trouve dans `scripts/tex2typ/regles.py` (renommages, arguments sans nom, commandes ignorées).

Noms kebab-case : `scripts/kebab.py` traduit un nom LaTeX ou un ancien nom Typst vers le nom actuel (`python "<skill>/scripts/kebab.py" MultiColonnes` → `multi-colonnes`), d'après `scripts/donnees/kebab.json` (copie de `outils/kebab/table-finale.json` de la suite ; `kebab.py --maj` la relit). Le convertisseur, `chercher.py` et les lecteurs d'index l'utilisent : un index ou des clés de guides produits avant le passage au kebab-case sont mis à niveau à la lecture.

## Autres skills, s'ils sont installés

- `typst` : le langage en plus long (cetz détaillé, compilation en ligne de commande). Ce skill-ci suffit sans lui.
- `typst-creation` : concevoir un nouvel environnement ou enrichir un paquet, avec aperçu en direct. Les paquets ne se modifient pas pour écrire un document.
- `typst-documentation` : rédiger la doc d'un paquet ou d'un outil.
- `choix-didactiques` : le fond pédagogique d'un document élève.
