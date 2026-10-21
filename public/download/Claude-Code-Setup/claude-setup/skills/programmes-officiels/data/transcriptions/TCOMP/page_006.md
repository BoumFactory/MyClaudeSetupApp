---
niveau: TCOMP
page: 6
pdf: tcomp.pdf
page_folder: TCOMP
bo_reference: "BO Hebdo 14 du 2 avril 2026"
bo_url: "https://www.education.gouv.fr/bo/2026/Hebdo14"
page_image: ../../pages/TCOMP/page_006.png
transcription_meta:
  date: "2026-05-19T16:33:58+00:00"
  status: skeleton          # passer à 'clean' après ultrathink
  confidence: 0.5           # ré-évaluer après nettoyage
  has_formulas: false
  has_tables: true
  source: "fitz get_text('text')"
---

# Page 6 — [Titre à déduire]

> [TRANSCRIPTION SQUELETTE — à raffiner par l'agent en ultrathink]
>
> Étapes obligatoires :
> 1. Consulter l'image-preuve `../../pages/TCOMP/page_006.png` (capacité multimodale).
> 2. Réparer les formules LaTeX cassées (`$...$` inline, `$$...$$` display).
> 3. Restaurer les tableaux markdown si présents.
> 4. Préserver les citations BO en blockquote `>` (verbatim).
> 5. Mettre `status: clean` et ajuster `confidence`.

## Texte brut (matière première à raffiner)

```text-brut
 
construire de nouveaux outils d’analyse faisant intervenir les fonctions d’une variable (notamment des fonctions de 
répartition) et le calcul intégral. 
Problèmes possibles 
− Courbe de Lorenz : sur des données réelles, présentation, définition, lecture, construction d’une ligne polygonale à partir 
des quantiles, interprétation. Modélisation par la courbe représentative d’une fonction continue, croissante, convexe de 
[0,1] dans [0,1] et ayant 0 et 1 comme points fixes. Position par rapport à la première bissectrice. 
− Indice de Gini : définition, calcul, interprétation comme mesure du degré d’inégalité d’une répartition. Comparaison de 
plusieurs répartitions. Évolution de l’indice sur une période. 
Contenus associés 
− Statistique descriptive : caractéristiques de dispersion (médiane, quartiles, déciles, rapport interdécile). 
− Fonctions d’une variable. 
− Convexité. 
− Calcul intégral. 
Inférence bayésienne 
Descriptif 
Le raisonnement bayésien est à la base de nombreux algorithmes de décision et se retrouve dans de nombreux domaines 
pratiques : sport, médecine, justice, etc. où l’on doit raisonner à partir de probabilités et d’informations incomplètes. Il s’agit 
ici de décrire et mettre en œuvre les principes du calcul utilisant des probabilités conditionnelles et notamment la formule de 
Bayes pour l’inversion des conditionnements. 
La question d’intérêt est représentée par un évènement A de probabilité P(A), dite probabilité a priori. L’observation d’un 
évènement B conduit à remplacer la probabilité a priori P(A) par la probabilité conditionnelle PB(A), dite a posteriori. La 
formule de Bayes PB(A)=
PA(B)P(A)
P(B)
 permet d’exprimer la probabilité a posteriori lorsque l’expression du second membre est 
évaluable. Elle montre la distinction essentielle entre PB(A) et PA(B). Bien comprendre cette distinction est un objectif majeur. 
Problèmes possibles 
− Tests binaires pour le diagnostic médical. Notion de vrais/faux positifs et négatifs, sensibilité, spécificité, valeurs 
prédictives positive (diagnostique) et négative, lien avec les probabilités conditionnelles. Tests de dépistage de sensibilité 
et de spécificité données : étude des valeurs prédictives en fonction de la proportion de malades et interprétation. 
− Exemples de problèmes du type : « De quelle urne vient la boule ? ». 
Contenus associés 
− Probabilités conditionnelles, inversion du conditionnement, formule de Bayes. 
− Étude de fonction. 
Répétition d’expériences indépendantes, échantillonnage 
Descriptif 
Ce thème vise à illustrer le modèle probabiliste de la répétition d’expériences aléatoires indépendantes et de l’échantillonnage 
ainsi que ses applications à l’inférence statistique, où il s’agit, à partir de l’observation d’un échantillon, d’induire des propriétés 
de la population dont il est issu. 
Le schéma de Bernoulli et la loi binomiale forment un cas fondamental, où il s’agit de considérer d’une part des probabilités ou 
proportions théoriques, et d’autre part des fréquences observées. 
La réalisation de simulations est indispensable. C’est l’occasion de montrer l’intérêt de la loi uniforme sur [0,1] pour simuler 
d’autres lois parmi lesquelles les lois uniformes discrètes et les lois binomiales. 
Problèmes possibles 
− Tirages aléatoires avec remise d’une boule dans une urne contenant des boules de deux couleurs différentes. Simulations. 
Calculs de probabilité. 
− Test d’une pièce, par construction d’un intervalle I centré en n/2 tel que P(X ∈ I ) ⩾ 1 – α où X est une variable aléatoire 
suivant la loi binomiale ℬ(n, 
1
2)  
− Surréservation. Construction d’un intervalle I de la forme [0, k] tel que P(X ∈ I ) ⩾ 1 – α où X est une variable aléatoire 
suivant la loi binomiale ℬ(n, p). 
− Sondages par échantillonnage aléatoire simple. Fourchette de sondage. Réflexion sur la réalisation effective d’un sondage 
et les biais possibles (représentativité, sincérité des réponses, etc.). 
− Démarche des tests d’hypothèse et de l’estimation. Les observations étant vues comme un échantillon aléatoire 
d’expériences régies par une loi inconnue (à découvrir), il s’agit de confronter une modélisation théorique proposée avec 
les résultats mesurés. Une bonne adéquation peut permettre de valider a priori le modèle (avec un certain degré de 
confiance), tandis que l’observation d'évènements donnés avec une probabilité très faible dans le modèle peut conduire à 
rejeter le modèle et à en chercher un autre. 

```

## Notes de l'agent (décisions, ambiguïtés)

(à remplir lors du raffinement ultrathink)
