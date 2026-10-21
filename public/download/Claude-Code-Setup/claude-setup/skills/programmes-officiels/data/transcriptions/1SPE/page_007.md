---
niveau: 1SPE
page: 7
pdf: 1spe.pdf
page_folder: 1SPE
bo_reference: "BO Hebdo 14 du 2 avril 2026"
bo_url: "https://www.education.gouv.fr/bo/2026/Hebdo14"
page_image: ../../pages/1SPE/page_007.png
transcription_meta:
  date: "2026-05-19T16:33:58+00:00"
  status: skeleton          # passer à 'clean' après ultrathink
  confidence: 0.5           # ré-évaluer après nettoyage
  has_formulas: true
  has_tables: true
  source: "fitz get_text('text')"
---

# Page 7 — [Titre à déduire]

> [TRANSCRIPTION SQUELETTE — à raffiner par l'agent en ultrathink]
>
> Étapes obligatoires :
> 1. Consulter l'image-preuve `../../pages/1SPE/page_007.png` (capacité multimodale).
> 2. Réparer les formules LaTeX cassées (`$...$` inline, `$$...$$` display).
> 3. Restaurer les tableaux markdown si présents.
> 4. Préserver les citations BO en blockquote `>` (verbatim).
> 5. Mettre `status: clean` et ajuster `confidence`.

## Texte brut (matière première à raffiner)

```text-brut
 
Analyse  
Objectifs  
Deux points fondamentaux du programme de première sont ici étudiés : le concept de dérivée, avec ses applications à l’étude 
des fonctions, et la fonction exponentielle.  
L’étude de la dérivation distingue le point de vue local (nombre dérivé) et le point de vue global (fonction dérivée). Les 
fonctions étudiées sont toutes régulières et le nombre dérivé est introduit à partir de la perception intuitive de la limite du 
taux de variation. On n’en donne pas de définition formelle, mais on s’appuie sur :  
− des représentations graphiques fournies par les outils logiciels (calculatrice, tableur, logiciel de géométrie dynamique) ;  
− le calcul algébrique du taux de variation dans des cas qui s’y prêtent : fonctions du second degré, fonction inverse ;  
− le calcul numérique d’expressions ƒ (a + h) – ƒ (a), où h prend des valeurs proches de 0, faisant apparaitre une 
approximation linéaire, par exemple avec a = 1 et ƒ étant une des fonctions carré, inverse, racine carrée.  
Il est intéressant d’exploiter ces divers registres dans l’étude d’un même nombre dérivé. Taux de variation et nombre dérivé 
gagnent à être illustrés dans des contextes variés :  
− en géométrie, ils représentent la pente d’une sécante et la pente d’une tangente ;  
− en cinématique, on peut interpréter un taux de variation comme une vitesse moyenne et un nombre dérivé comme une 
vitesse instantanée ;  
− dans un cadre économique, le nombre dérivé est relié au cout marginal.  
Compte tenu de son importance en mathématiques et dans de nombreux champs disciplinaires, et de ses interactions avec le 
concept de dérivée, le programme prévoit l’étude de la fonction exponentielle. On donnera des exemples d’utilisation dans les 
autres disciplines (calculs d’intérêts, dilution d’une solution, décroissance radioactive). En liaison avec les suites géométriques, 
c’est aussi l’occasion de proposer des modélisations discrètes ou continues de phénomènes d’évolution. 
En liaison avec les autres disciplines, on peut signaler et utiliser la notation 
∆𝑦
∆𝑥 pour un taux de variation et 
d𝑦
d𝑥  pour une dérivée ; 
si 𝑦 = ƒ (𝑥), on peut ainsi écrire 
d𝑦
d𝑥 = ƒ ‘ (𝑥) en adaptant selon le contexte : 𝑥 = ƒ (𝑡), 𝑞 = ƒ (𝑡), etc. 
Histoire des mathématiques  
Le calcul différentiel s’est imposé par sa capacité à donner des solutions simples à des problèmes nombreux d’origines variées 
(cinématique, mécanique, géométrie, optimisation).  
Le développement d’un calcul des variations chez Leibniz et Newton se fonde sur l’hypothèse que les phénomènes naturels 
évoluent linéairement quand on leur applique des petites variations. Leurs approches partent de notions intuitives mais floues 
d’infiniment petit. Ce n’est que très progressivement que les notions de limites et de différentielles, qui en fondent l’exposé 
actuel, ont été clarifiées au XIXe siècle.  
La notation exponentielle et les fonctions exponentielles apparaissent vers la fin du XVIIe siècle, procédant d’une volonté de 
traiter des phénomènes de croissance comparables à ceux des intérêts composés. La modélisation de ces situations fait 
naturellement apparaitre la caractérisation de la fonction exponentielle comme seule fonction vérifiant l'équation 
différentielle 𝑦‘ = 𝑦 et la condition initiale 𝑦(0) = 1.  
La trigonométrie a été utilisée chez les Anciens dans des problèmes de natures diverses (géométrie, géographie, astronomie). 
Elle est à l'époque fondée sur la fonction corde, d'un maniement bien moins facile que les fonctions sinus et cosinus de la 
présentation actuelle.  
Dérivation  
Contenus  
Point de vue local  
− Taux de variation. Sécantes à la courbe représentative d’une fonction en un point donné. 
− Nombre dérivé d’une fonction en un point, comme limite du taux de variation. Notation ƒ ’(a).  
− Tangente à la courbe représentative d’une fonction en un point, comme « limite des sécantes ». Pente. Équation : la 
tangente à la courbe représentative de ƒ au point d’abscisse a est la droite d’équation 𝑦 = ƒ (a) + ƒ ‘(a)(𝑥 – a).  
− Approximation linéaire : fonction affine tangente 𝑥 ↦ ƒ (a) + ƒ ‘(a)(𝑥 – a) et approximation de ƒ (a + h) par ƒ (a) + ƒ ‘(a)h. 
Point de vue global  
− Fonction dérivable sur un intervalle. Fonction dérivée.  
− Fonction dérivée des fonctions carré, cube, inverse, racine carrée.  
− Opérations sur les fonctions dérivables : somme, produit, inverse, quotient.   
− Pour 𝑛 dans ℤ, fonction dérivée de la fonction 𝑥 ↦ 𝑥 𝑛. 
− Fonction valeur absolue : étude de la dérivabilité en 0.  
Capacités attendues  
− Calculer un taux de variation, la pente d’une sécante.  
− Interpréter le nombre dérivé en contexte : pente d’une tangente, vitesse instantanée, cout marginal, etc. 
− Déterminer graphiquement un nombre dérivé par la pente de la tangente. Construire la tangente en un point à une courbe 
représentative connaissant le nombre dérivé.  
− Déterminer l’équation de la tangente en un point à la courbe représentative d’une fonction.  
− Calculer une valeur approchée de ƒ (a + h). 
− Dans des cas simples, calculer une fonction dérivée en utilisant les propriétés des opérations sur les fonctions dérivables.  
  

```

## Notes de l'agent (décisions, ambiguïtés)

(à remplir lors du raffinement ultrathink)
