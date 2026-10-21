# Contenu

Les chemins courts `Cours/…` désignent `1. Cours/2nde/Sequence-Vecteur_par_coordonnees-P1/Cours/…` (depuis la racine du projet).

## Objectifs

À la fin des deux séances, l'élève sait :
- reconnaître une translation et construire l'image d'une figure sur quadrillage ;
- décrire le vecteur $\Vecteur{AB}$ par sa direction, son sens et sa longueur, et nommer origine et extrémité ;
- reconnaître deux vecteurs égaux et en tracer un représentant d'origine donnée ;
- relier $\Vecteur{AB}=\Vecteur{DC}$ au parallélogramme $ABCD$, en respectant l'ordre des sommets ;
- construire l'image d'un point par une translation, avec ou sans quadrillage.

Programme (skill `programmes-officiels`, base `data/json/2GT.json`) :
- 2GT-GEO-009 « Égalité de deux vecteurs. Notation 𝑢⃗. Vecteur nul. » (le vecteur nul reste au cours : D-21) ;
- 2GT-GEO-010 « Représentants d'un vecteur. » ;
- vocabulaire du BO « vecteur déplacement de A à B » (D-19).

Prérequis réactivés du cycle 4 : 3E-GEO-011 « Définir et utiliser la translation : définition ponctuelle avec parallélogramme » et 3E-GEO-012 « Définir et utiliser les notions de vecteur, de vecteurs égaux… ».

## Déroulé

Chaque séance dure 55 minutes (D-03), installation comprise dans la première ligne de chaque tableau (environ 3 minutes). Modalités : scène projetée, recherche en binômes avec cadres, mise en commun (D-04).

### Séance 1 — Glisser une figure

| Minutes | Temps | Modalité | Version minimale si retard |
|---|---|---|---|
| 0-8 | Installation, scène S1 | projeté, oral | — |
| 8-23 | Partie A : construire l'image d'une figure | binômes | construire seulement K' et L' |
| 23-33 | Mise en commun A | classe entière | — |
| 33-45 | Partie B : trier des flèches | binômes | trier quatre flèches au lieu de six (f1 à f4) |
| 45-48 | Mise en commun B | classe entière | — |
| 48-55 | Trous du cours P1 | individuel | — |

Partie qui peut sauter en premier : le « Pour aller plus loin ».

### Séance 2 — Parallélogramme et vecteurs égaux

| Minutes | Temps | Modalité | Version minimale si retard |
|---|---|---|---|
| 0-7 | Installation, rappel flash en tête de fiche | individuel | — |
| 7-10 | Scène S2 | projeté, oral | — |
| 10-25 | Partie C : du glissement au parallélogramme | binômes | sauter la question C4 |
| 25-35 | Mise en commun C | classe entière | — |
| 35-45 | Partie D : image d'un point et représentant | binômes | D1 seulement ; D2 passe en travail à la maison |
| 45-50 | Trous du cours P1 | individuel | — |
| 50-55 | Billet de sortie (D-14) | individuel | — |

## Contenus détaillés

Les déplacements sont donnés en carreaux : « (5 ; 2) » signifie 5 carreaux vers la droite et 2 vers le haut. Cette écriture sert uniquement à l'agent rédacteur pour placer les figures ; elle n'apparaît jamais dans la fiche élève, qui ne parle pas de coordonnées (voir D-05, conséquences). Les coordonnées de points ci-dessous se lisent sur le quadrillage, origine en bas à gauche ; elles ne sont pas imprimées non plus : la fiche montre un quadrillage sans axes, avec les points placés.

Figures sans coordonnées données ci-dessous (scènes, rappel flash, $EFGH$, $P$, $R$, $S$, billet, « Pour aller plus loin » S2) : l'agent choisit les données, en respectant D-17 et les contraintes écrites dans la partie concernée, puis les inscrit dans `enonce_figures.tex` et en déduit les réponses de la Solution (D-25).

Trou dans une égalité vectorielle (C3, C4, billet) : la zone de réponse contient le vecteur entier, par exemple `$\Vecteur{AB} = $ \repsim[1.5cm]{$\Vecteur{DC}$}`, et jamais une flèche au-dessus d'un trou (D-26).

### Scène S1 (projetée)
- **Figure** : sur un quadrillage, une figure $\mathcal{F}$ (quadrilatère non symétrique), son image $\mathcal{F}'$ par une translation de déplacement (6 ; 1), et une troisième copie $\mathcal{G}$ obtenue par une symétrie axiale (la figure est retournée).
- **Question orale du professeur** : « Laquelle des deux copies a seulement glissé ? Comment passe-t-on de $\mathcal{F}$ à cette copie ? »
- **Réponse attendue** : $\mathcal{F}'$ ; les élèves décrivent un glissement (« vers la droite et un peu vers le haut »). Le professeur rappelle le mot **translation** (cycle 4).

### Partie A — Construire l'image d'une figure
- **Figure** : quadrillage de 12 × 10 carreaux. Points $A(1;7)$ et $B(6;9)$, flèche tracée de $A$ vers $B$. Quadrilatère $KLMN$ avec $K(1;1)$, $L(4;1)$, $M(3;4)$, $N(1;3)$. Point $Q(10;2)$ pour le « Pour aller plus loin » S1.
- **A1** : « On fait glisser le quadrilatère $KLMN$ comme on passe de $A$ à $B$. Construire son image $K'L'M'N'$. »
  Réponse : $K'(6;3)$, $L'(9;3)$, $M'(8;6)$, $N'(6;5)$.
- **A2** : « Tracer les flèches de $K$ vers $K'$, de $L$ vers $L'$, de $M$ vers $M'$ et de $N$ vers $N'$. »
- **A3** (cadre où l'élève écrit) : « Ces quatre flèches et la flèche de $A$ vers $B$ sont portées par des droites \repsim… ; elles vont toutes \repsim… ; elles ont toutes la même \repsim… »
  Réponse : parallèles ; dans le même sens (de la figure vers son image) ; longueur.
- **Coup de pouce A** : « Pour placer $K'$, pars de $K$ et refais exactement le trajet de $A$ à $B$ sur le quadrillage. »
- **Erreurs prévisibles** : compter le trajet de $B$ vers $A$ (image du mauvais côté) ; confondre longueur de la flèche et nombre de carreaux horizontaux.

### Mise en commun A
Le professeur fixe au tableau : la translation qui transforme $A$ en $B$ fait glisser tous les points dans la même **direction** (celle de $(AB)$), le même **sens** (de $A$ vers $B$) et de la même **longueur** ($AB$). Elle s'appelle la **translation de vecteur $\Vecteur{AB}$** ; $A$ est l'**origine**, $B$ l'**extrémité** ; on parle aussi du **vecteur déplacement de $A$ à $B$** (D-19). Encadré « Ce que l'on retient » de la fiche, placé juste après la partie A et avant la partie B : « Une translation fait glisser tous les points de la même façon : même direction, même sens, même longueur. Les définitions sont dans le cours. » (D-07)

### Partie B — Même translation ou pas ?
- **Figure** : quadrillage d'environ 18 × 8 carreaux, la flèche de référence de $A$ vers $B$ de déplacement (5 ; 2), et six flèches nommées f1 à f6. Les déplacements sont imposés ; l'agent place les origines librement, à condition qu'aucune flèche n'en croise une autre.

  | Flèche | Déplacement | Direction | Sens | Longueur |
  |---|---|---|---|---|
  | f1 | (5 ; 2) | même | même | même |
  | f2 | (−5 ; −2) | même | contraire | même |
  | f3 | (2 ; 5) | autre | — | même |
  | f4 | (10 ; 4) | même | même | double |
  | f5 | (5 ; 2) | même | même | même |
  | f6 | (5 ; −2) | autre | — | même |

- **B1** : tableau à cocher (direction, sens, longueur) pour chaque flèche, comparée à la flèche de $A$ vers $B$. Le sens ne se compare que si la direction est la même : la case est grisée sinon (pas de couleur, D-10 : hachures ou case barrée).
- **B2** : « Quelles flèches représentent la translation de vecteur $\Vecteur{AB}$ ? » Réponse : f1 et f5.
- **Mise en commun B** : une flèche représente la translation de vecteur $\Vecteur{AB}$ seulement si les trois caractéristiques sont les mêmes ; f2 montre que la direction ne suffit pas, f4 que la longueur compte.
- **Erreur prévisible n° 1** : « même direction » compris comme « même sens » (f2 retenue).

### Pour aller plus loin S1
Le point $Q(10;2)$ est placé dès le départ sur la figure de la partie A ; l'exercice, en fin de fiche, renvoie à cette figure : « Sur la figure de la partie A, placer le point $P$ dont l'image par la translation de vecteur $\Vecteur{AB}$ est $Q$. » Réponse : $P(5;0)$.

### Trous du cours P1, séance 1
Les élèves complètent dans leur exemplaire du cours : `Cours/Definition/translation.tex` (« Translation et vecteur »), `Cours/Definition/vecteur.tex` (« Vecteur ») et `Cours/Remarque/vecteur_deplacement_position.tex` (le professeur explique en une minute le « vecteur position », que l'activité ne traite pas).

### Rappel flash, début de séance 2 (en tête de la fiche S2)
Les trois questions sont imprimées en haut de la fiche de la séance 2 et les élèves y répondent par écrit. Il n'y a pas de page projetée pour le rappel.
1. « Citer les trois caractéristiques du vecteur $\Vecteur{AB}$. » — direction, sens, longueur.
2. Une figure : un vecteur $\Vecteur{AB}$, un point $M$ et trois points candidats ; « Lequel est l'image de $M$ par la translation de vecteur $\Vecteur{AB}$ ? » — un seul candidat est juste ; un autre correspond au sens contraire, le dernier à une longueur différente.
3. « Vrai ou faux : $\Vecteur{AB}$ et $\Vecteur{BA}$ ont le même sens. » — faux.

### Scène S2 (projetée)
- **Figure** : quatre points $A$, $B$, $C$, $D$ formant un parallélogramme $ABCD$ non rectangle et non losange, avec les flèches de $A$ vers $B$ et de $D$ vers $C$, sans les côtés $[AD]$ et $[BC]$.
- **Question orale** : « La translation de vecteur $\Vecteur{AB}$ transforme-t-elle $D$ en $C$ ? Que forment les quatre points ? »

### Partie C — Du glissement au parallélogramme
- **Figure** : quadrillage de 10 × 9 carreaux ; $A(1;1)$, $B(6;3)$, $D(2;5)$.
- **C1** : « Construire le point $C$, image de $D$ par la translation de vecteur $\Vecteur{AB}$. » Réponse : $C(7;7)$.
- **C2** : « Tracer le quadrilatère $ABCD$. Quelle est sa nature ? Justifier. » Réponse : parallélogramme, car $(AB)$ et $(DC)$ sont parallèles et $AB = DC$ (deux côtés opposés parallèles et de même longueur, propriété de collège).
- **C3** (cadre) : « Les flèches de $A$ vers $B$ et de $D$ vers $C$ représentent la même translation. On écrit $\Vecteur{AB} = $ [trou de vecteur, D-26]. » Réponse : $\Vecteur{DC}$ (D-20).
- **C4** : « $EFGH$ est un parallélogramme (figure fournie). Compléter : $\Vecteur{EF} = $ [trou de vecteur, D-26]. A-t-on $\Vecteur{EF} = \Vecteur{GH}$ ? » Réponse : $\Vecteur{HG}$ ; non, $\Vecteur{GH}$ va dans le sens contraire.
- **Coup de pouce C** : « Refais pour $D$ le trajet de $A$ à $B$. »
- **Erreurs prévisibles** : écrire $\Vecteur{AB} = \Vecteur{CD}$ ; nommer le quadrilatère $ABDC$ (sommets dans le mauvais ordre).

### Mise en commun C
Deux vecteurs sont **égaux** lorsqu'ils définissent la même translation : même direction, même sens, même longueur. Chaque flèche est un **représentant** du vecteur ; on peut nommer le vecteur d'une seule lettre, $\Vecteur{u}$. Propriété : $\Vecteur{AB} = \Vecteur{DC}$ si et seulement si $ABCD$ est un parallélogramme, avec l'ordre des sommets du cours (D-20) ; le professeur ajoute oralement que les diagonales d'un parallélogramme ont le même milieu (propriété du collège, item 2 du bloc du cours : D-23). Encadré « Ce que l'on retient », placé juste après la partie C et avant la partie D : « Des flèches de même direction, même sens et même longueur représentent le même vecteur. Le lien avec le parallélogramme est dans le cours. »

### Partie D — Image d'un point et représentant
- **D1** (sans quadrillage, zone blanche) : trois points $A$, $B$, $M$ non alignés, $AB$ d'environ 5 cm, l'angle $\widehat{BAM}$ non droit. « Construire à la règle et au compas le point $M'$, image de $M$ par la translation de vecteur $\Vecteur{AB}$. Quel quadrilatère forment $A$, $B$, $M'$ et $M$ ? »
  Réponse : $ABM'M$ est un parallélogramme ; on reporte $AB$ depuis $M$ et $AM$ depuis $B$ au compas. Aucune méthode n'est encadrée (D-08).
- **Coup de pouce D** : « D'après la partie C, quel quadrilatère doit former $ABM'M$ ? Quelles longueurs reporter au compas ? »
- **D2** (quadrillage) : un vecteur $\Vecteur{u}$ représenté par une flèche de déplacement (4 ; −1), et trois points $P$, $R$, $S$. « Tracer le représentant de $\Vecteur{u}$ d'origine $P$, puis ceux d'origine $R$ et $S$. »

### Pour aller plus loin S2
Sans quadrillage, à la règle et au compas. « $A$, $B$, $C$ sont trois points non alignés. Placer $D$ tel que $ABCD$ soit un parallélogramme, puis $E$ tel que $ABEC$ soit un parallélogramme. Que semble être le point $C$ pour le segment $[DE]$ ? » Réponse : son milieu (conjecture seulement ; la caractérisation du milieu viendra avec le cours).

### Trous du cours P1, séance 2
`Cours/Definition/egalite_vecteurs.tex`, `Cours/Definition/representants_notation.tex`, `Cours/Propriete/proprietes_egalite.tex` (« Représentant d'origine donnée », qui formalise D2) et `Cours/Propriete/parallelogramme_vecteurs.tex` (les deux items, D-23).

Le cours suivant reprend le cours P1 à la sous-section « Vecteur nul et vecteur opposé », puis le suit dans l'ordre en sautant les blocs déjà complétés (D-24).

### Billet de sortie (D-14)
1. Figure d'un parallélogramme $RSTU$ : « Compléter : $\Vecteur{RS} = $ [trou de vecteur, D-26]. » — $\Vecteur{UT}$.
2. Quatre flèches sur quadrillage : « Lesquelles représentent le même vecteur que la première ? » — deux sur trois, la troisième a le sens contraire.
3. Quadrillage, un vecteur et un point $N$ : « Placer l'image de $N$ par la translation de ce vecteur. »

## Différenciation et variantes
- Coups de pouce : un texte par partie (A, C, D), rédigé ci-dessus ; chaque carte est imprimée en deux exemplaires (03-forme, D-13).
- « Pour aller plus loin » : un par séance, ci-dessus.
- Version professeur : partie « Solution » et « Notes pour le professeur » (réponses, erreurs prévisibles, minutage : 03-forme).
