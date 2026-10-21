// RECETTE : QCM et vrai/faux (paquet farfadet-qcm), courte et neutre.
//
// Ce qu'elle montre :
//   - un QCM `mcq` dans un `exo` : questions `mcq-quest(br: n)[question][rép. 1][rép. 2]…`, bonne(s) réponse(s)
//     par `br` (un numéro ou un tableau), mises en valeur dans la version professeur seulement ;
//   - les formats (clé `style`) : `Troyes` en horizontal, `BFCours` en vertical ; autres formats :
//     `default`, `Tokyo`, `Boston`, `Miami`, `Reims`, `Millau`, `Melun`, `Paris` ;
//   - la numérotation poursuivie d'un QCM à l'autre (`resume: true`) ;
//   - un exercice « vrai ou faux » (`vrai-faux` + `affirmation`) avec justification côté professeur
//     et lignes de justification côté élève ;
//   - les points d'une affirmation (`points:`) qui alimentent le score de l'exercice.
//
// Compiler une copie placée dans le dossier de travail (pas dans le skill) ; PDF prof et élève, images :
//   python "<skill>/scripts/compiler.py" "dossier/qcm.typ" --png   (version élève : rien n'est coché)

#import "@preview/farfadet:0.2.0": *

// Identité de l'auteur, réglée une fois pour les bandeaux et le pied de page (dans une façade,
// ces lignes disparaissent du document : voir references/facade.md).
#setbfmodele(pour: "identite", cycle: [Lycée], etablissement: [du Parc])

#show: modele("cours", niveau: "2nde", theme: [Fonctions de référence], type-document: "exercices")

#exo(level: 1)[QCM : une seule bonne réponse][
  Pour chaque question, cocher la bonne réponse.

  // Format Troyes : question à gauche, réponses côte à côte à droite, bonne réponse sur fond rouge
  // (le format par défaut ne la met qu'en gras : invisible quand la réponse est une formule)
  #mcq(style: "Troyes", question-width: 7cm)[
    #mcq-quest(br: 2)[L'image de $-3$ par la fonction carré est :][$-9$][$9$][$6$]
    #mcq-quest(br: 1)[L'antécédent positif de $16$ par la fonction carré est :][$4$][$8$][$256$]
  ]

  // Format BFCours, réponses en colonne ; la numérotation continue (resume)
  #mcq(style: "BFCours", orientation: "vertical", question-width: 8cm, resume: true)[
    #mcq-quest(br: 3)[La fonction inverse est définie sur :][$RR$][$[0 thin; +oo[$][$RR^*$]
    #mcq-quest(br: (1, 2))[Quels nombres ont pour carré $25$ ?][$5$][$-5$][$12","5$]
  ]
]

#exo(level: 2)[Vrai ou faux][
  Pour chaque affirmation, cocher #frquote[Vrai] ou #frquote[Faux], puis justifier.

  #vrai-faux(
    lignes-justification: 1,
    affirmation(vrai: true, points: 1, justification: [$(-2)^2 = 4$ et $2^2 = 4$.])[
      Deux nombres opposés ont le même carré.
    ],
    affirmation(vrai: false, points: 1, justification: [Contre-exemple : $0","5^2 = 0","25 < 0","5$.])[
      Le carré d'un nombre positif est toujours supérieur à ce nombre.
    ],
    affirmation(vrai: false, points: 1, justification: [$1/0$ n'existe pas.])[
      Tout nombre réel a un inverse.
    ],
  )
]
