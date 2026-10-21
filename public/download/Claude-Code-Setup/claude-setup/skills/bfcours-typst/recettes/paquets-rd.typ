// RECETTE : objets des paquets rd dans une fiche de calcul (niveau collège), courte et neutre.
//
// Ce qu'elle montre :
//   - `rdopp` : opérations posées (soustraction décimale, multiplication avec retenues, division) ;
//     corrigé en version professeur, quadrillage vide (`rd.encadregrille`) en version élève, par `ifcorrection` ;
//   - `rdconv` + `rdplace` / `rdconvert` / `rdconvemptyline` : tableau de conversion d'unités ;
//   - `rdtabnum` + `rdtnplace` / `rdtnconvert` : tableau de numération ; `rdtnplace(…, etoile: true)` et les
//     conversions ne s'affichent qu'en version professeur, à condition de passer la version (voir l'exercice 2) ;
//   - `rdtime` (durées posées), `rdratio` et `dratio` (proportions), `decomp-fp` et `pgcd` (arithmétique) ;
//   - deux boîtes `rd.` : `rd.methode` et `rd.tache` ;
//   - `multi-colonnes` pour poser plusieurs objets côte à côte.
// Les paquets rd gardent les couleurs de leurs auteurs : `setbfcolors` ne les change pas ; chacun se règle
// par son setter (`setrdopp`, `setrdconv`, `setrdtabnum`, `setrdtime`, `setrdratio`, `setrdarithm`, `setrdboites`).
//
// Compiler une copie placée dans le dossier de travail (pas dans le skill) ; PDF prof et élève, images :
//   python "<skill>/scripts/compiler.py" "dossier/paquets-rd.typ" --png

#import "@preview/farfadet:0.2.0": *

#show: modele("cours", niveau: "6e", theme: [Calculer avec les nombres décimaux], type-document: "exercices",
  cycle: [Cycle 3], etablissement: [Collège])

#rd.methode[*Poser une soustraction décimale.* On aligne les virgules, on complète par des zéros, puis on calcule de droite à gauche.]

#exo(level: 1)[Opérations posées][
  Poser et effectuer les opérations suivantes.
  #multi-colonnes(3)[
    - $12","5 - 3","45$
      #ifcorrection[#rdopp("12.5, 3.45", operation: "sub")][#rd.encadregrille(height: 3cm)[]]
    - $234 times 56$
      #ifcorrection[#rdopp("234, 56", mul: true, carry: true)][#rd.encadregrille(height: 3cm)[]]
    - $125 div 5$
      #ifcorrection[#rdopp("125, 5", div: true)][#rd.encadregrille(height: 3cm)[]]
  ]
]

#exo(level: 1)[Conversions][
  #multi-colonnes(2)[
    - Convertir $12$ g en cg et $3","45$ hg en g à l'aide du tableau.
      #ifcorrection[
        #rdconv(type: "mass", rdconvert(12, "g", "cg"), rdconvert("3,45", "hg", "g"))
      ][
        #rdconv(type: "mass", rdconvemptyline(2))
      ]
    - Placer #num(1500), $42$ et $3","14$, puis écrire $7","2$ dizaines en dixièmes.
      // Les éléments `etoile: true` et les conversions sont les réponses : visibles en version professeur
      // (couleur des corrections), places vides en version élève (la clé `correction` suit la version).
      #rdtabnum(width: 8cm,
        rdtnplace(1500, etoile: true), rdtnplace(42, etoile: true),
        rdtnplace("3,14", etoile: true), rdtnconvert("7,2", 1, -1))
  ]
]

#exo(level: 2)[Durées, partages et nombres premiers][
  #tcbenumerate[
    + Un film commence à 2 h 37 min et dure 3 h 49 min. Durée totale cumulée :
      #ifcorrection[#rdtime("2h37min", "3h49min")][#crep(extra-lines: 1)[]]
    + On partage 150 € dans le ratio #dratio("1:2") .
      #ifcorrection[#rdratio(width: 6cm, label-above: [150 €], "1,2")][#crep(extra-lines: 1)[]]
    + Décomposer $126$ en produit de facteurs premiers, puis calculer le #pgcd() de $60$ et $75$.
      #crep[$126 = #decomp-fp(126)$ ; $#pgcd(60, 75) = #pgcd(60, 75, etoile: true)$.]
  ]
]

#rd.tache[Défi][Le plus grand produit][Avec les chiffres $2$, $5$, $7$ et $9$ utilisés une seule fois, écrire deux nombres de deux chiffres dont le produit est le plus grand possible.]
