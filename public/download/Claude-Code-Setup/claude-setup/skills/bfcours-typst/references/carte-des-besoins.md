# La carte : je veux… → fonction

Tableau des besoins courants et de la fonction à utiliser (le paquet est entre parenthèses). Tout autre besoin : `chercher.py "<besoin en mots>"`.

| Je veux… | Fonction (paquet) |
|---|---|
| la page, le bandeau, le pied | `#show: modele("cours", …)` ; bandeau seul `chapitre` ; évaluation `type-document: "evaluation"` (modele) |
| un sommaire | `tableofcontents()` ou clé `sommaire: true` (didactique) |
| définition, propriété, théorème | `#definition[Titre][Corps]` ou `#definition[Corps]` ; `propriete`, `theoreme` |
| exemple, contre-exemple, méthode, remarque, notation | `exemple`, `contre-exemple`, `methode`, `remarque`, `notation` |
| démonstration, solution, activité, aide, histoire | `demonstration`, `solution`, `activite`, `aide`, `histoire` |
| un mot de vocabulaire et son index | `voc[mot]`, `printvocindex()` ; lien `vocref("url")[mot]` |
| un cadre libre, une figure légendée | `boite`, `bfbox`, `bf-env`, `boite-figure` (didactique) |
| un exercice numéroté, étoiles, corrigé | `#exo(level: 2)[Titre][Énoncé #exocorrection Correction]` : marqueur `#exocorrection` sans parenthèses (exo) |
| une zone de réponse sous l'énoncé (partie basse) | `#exo[Titre][Énoncé #tcblower Réponse #exocorrection Correction]` (exo) |
| encadrer un exercice entier | `cadre:` / `cadre-correction:` d'`exo`, de `setrdexo` ou de `rdexo-skin` (fonction `(info, contenu) => block(…)`) ; `cadre: none` (exo) |
| les corrigés à la fin | `#ifcorrection[#rdexocorrection(0)]` (exo) |
| un exercice d'évaluation, ses compétences | `exo-eval(tags: "…")`, `competence`, `tableaucompetence`, `printcompindex` (exo) |
| des points par question, le total | `+ #itempoint(2)[Énoncé.]`, `displayitempoints(true)`, `getsavedtotalpoints()` (exo) |
| le cartouche nom/durée d'une évaluation | `tableau-eval(55)`, `chrono(30)`, `pascalc()` (exo, maths) |
| des questions numérotées, en colonnes | `#tcbenumerate(columns: 2)[ + Q1 + Q2 ]` (un `+` par ligne, pastilles centrées sur la ligne ; `columns` = `raster-columns`) (enum) |
| reprendre la numérotation | `#tcbenumerate(depart: 3)[ + Q3 ]` ou un numéro sur le premier item (`5. Q5`) ; sous-questions : `tcbenumerate` imbriqué |
| texte et figure côte à côte | `#multi-colonnes(largeurs: (3, 2))[ - texte - figure ]` (un `-` par colonne) (enum) ; jamais `columns()` natif |
| une question à options, une case de transition | `#tcbitem(colback: …)[…]` ou `#tcbitem(numerote: false)[…]` dans le corps, à la place d'un `+` ou d'un `-` (enum) |
| écrire un environnement à la LaTeX | `#begin(exo, level: 2)[Titre]` … `#end(exo)` : options et titre dans `begin`, corps entre les deux ; vaut pour tous les environnements (socle) |
| une zone de réponse sous la question | `crep(extra-lines: 2)[réponse prof]` (crep) |
| un trou dans une phrase, une fraction à trous | `tccrep(3cm)[réponse]`, `tcfillcrep[…]`, `repsim`, `tcfraccrep[num][den]` (crep) |
| une réponse en couleur sans zone | `correction-box[…]` (crep) |
| lignes Seyès, énoncé + réponse | `seyesrep`, `seyestab`, `seyesarray`, `assosbox`, `dembox` (crep) |
| des cases à cocher | `cb`, `ccb`, `checkbox`, `tccheckbox`, `tccheckboxlist` (crep) |
| un QCM, un vrai/faux | `#mcq[#mcq-quest(br: 2)[Question][rép. 1][rép. 2][rép. 3]]`, `vrai-faux`, `affirmation` (qcm) |
| un tableau encadré, de valeurs | `#tcbtab(3, entete: true, …cellules)` : collé à gauche comme `\tcbtab`, centré par `align: center` (= `\tcbtabc`) ; `multicolumn`, `cellcolor` (tableaux) |
| vecteur, coordonnées, repère, intervalle | `$vect(A B)$`, `$coordonnees(3, -2, nom: A)$`, `$rep$`, `$intervalle(0, 1, forme: "fo")$` (maths) |
| un nombre, une grandeur à la française | `num(1234.5)` → 1 234,5 ; `qty(3.5, "cm")` ; `sisetup` (maths) |
| œ, Œ, € dans un source ASCII | `c#oe;ur`, `#oe-maj;uvre`, `#euro` (socle) ; ou taper `œ`, `€` directement |
| mettre en valeur, encadrer, guillemets | `acc`, `encadrer`, `surligner`, `frquote` (maths) |
| connecteurs logiques colorés | `#si() $x > 0$, #alors() …` : `si`, `alors`, `donc`, `car`, `ssi` (maths) |
| code Python, icône, texte autour d'une figure | `bf-code-python`, `icone("book")`, `habiller` (extras) |
| une boîte rd (zone, attention, méthode, tâche) | `rd.zone`, `rd.attention`, `rd.methode`, `rd.tache` (rdboites) |
| opération posée, durées, proportions | `rdopp`, `rdtime`, `rdratio` |
| tableau de conversion, de numération | `rdconv` + `rdplace`/`rdconvert` ; `rdtabnum` + `rdtnplace`/`rdtnconvert` |
| PGCD, diviseurs, décomposition | `pgcd`, `liste-diviseurs`, `decomp-fp`, `fracirr` (rdarithm) |
| grille de triangles, feuille de calcul | `rdgrid`, `rdsheet` |
| changer la boîte d'un environnement (skin) | `#definition(rendu: "manchette")[…]` ; sept skins `"cahier"`, `"outil"`, `"pastille"`, `"manchette"`, `"filet"`, `"suspendu"`, `"minimal"` (étiquette et titre seuls) ; sans icône : `skin: (icone: none)` ; par type : `setbfenvironments(pour: "Definition", rendu: …)` (didactique) ; tout le détail : `references/skins.md` |
| changer l'icône d'un type pour tous les skins | `embleme` : `#theoreme(embleme: "etoile")[…]`, `setbfenvironments(pour: "Theoreme", embleme: "coeur")` |
| créer, enregistrer, écrire un skin | `bfskin("suspendu", icone: "cle")`, `setbfskins(mien: …)`, `rendu: "mien"` ; `references/skins.md` |
| organiser un concours de skins ou d'enveloppes de diapos | `references/concours-skins.md`, `references/concours-enveloppes.md` |
| une figure de géométrie plane, un repère, une courbe | `#geo({ repere(x: (-1, 5), y: (-1, 4)); triangle(A, B, C, noms: (…)); courbe(x => …) })` ; `point`, `segment`, `droite`, `fleche`, `cercle`, `arc`, `polygone`, `angle-droit`, `codage-segment`, `mediatrice`, `milieu`, `intersection` ; légendée `figure-geo` (geom) ; au-delà : cetz dans le même `geo` |
| du texte libre, une ligne brisée (escalier, pointillés, forme remplie), un quadrillage, des axes dans une figure | `etiquette(p, corps, pos: "se", couleur:, taille:)`, `ligne-brisee(pts, ferme:, remplissage:, couleur:, style:)`, `quadrillage(x:, y:, pas:)`, `axes(x:, y:)`, `axe(a, b)` (geom) ; chacun est un seul élément cetz : à préférer aux `d.line` / `d.content` |
| un tableau de signes, de variations | `#tabvar(("-oo", "0", "+oo"), tkz-tab-line($f'(x)$, ",-,z,+,"), tkz-tab-var($f(x)$, ("+", "+oo"), ("-", "-1"), ("+", "+oo")))` ; élève : `a-completer: true` (tabvar) |
| garder un morceau de LaTeX tel quel (figure TikZ) | `#latex[…]` (un bloc brut LaTeX entre les crochets), réglé par `setbflatex(paquets: …)` ; rendu par `compiler.py` (latex). **Dès qu'un document a des `#latex`, y écrire une fois `#setbflatex(lire: p => read(p, encoding: none))`** (ou ajouter `lire:` au `setbflatex` existant) : l'aperçu Tinymist (Ctrl+S) montre alors les extraits déjà rendus ; sans cette ligne il les montre en encadré « non rendu ». Les extraits nouveaux ou modifiés, et les PDF prof + élève, viennent de Ctrl+Maj+B (ou de `compiler.py`). `rendus-tex/index.json` doit exister (bfwatch le crée à l'ouverture de l'aperçu ; `compiler.py` au premier passage) |
| un diaporama, une correction révélée pas à pas | import séparé **après** le méta-paquet : `#import "@local/farfadet-slides:0.2.0": *`, `#show: bfcours-theme.with(titre: […])`, `#title-slide()`, `==` diapo, `#pause`, `#etapes(genre: "calcul")[…][…]` (slides) |
