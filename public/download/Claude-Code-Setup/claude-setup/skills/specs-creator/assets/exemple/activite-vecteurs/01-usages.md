# Usages

## Personas

### P1 — Le professeur
Enseigne en seconde (classe 2-C cette année). Prépare la veille : imprime les fiches, ouvre le PDF pour projeter. En classe, il projette la scène, circule entre les binômes, mène la mise en commun au tableau. Il a besoin d'une version professeur qui lui donne les réponses attendues, les erreurs prévisibles et le minutage. Il renoncerait si l'activité débordait systématiquement de 15 minutes ou si le vocabulaire divergeait de son cours.

### P2 — L'élève de seconde
Classe hétérogène. Prérequis réels : il a vu les translations en 4e-3e (« faire glisser »), parfois oubliées ; il sait utiliser règle, équerre, compas, se repérer sur un quadrillage. Il travaille sur la fiche papier, en binôme. Il garde la fiche dans son classeur, la trace écrite étant dans le cours (D-07).

### P3 — L'agent rédacteur
Un agent qui ouvre ce dossier à froid et rédige le document LaTeX bfcours. Il doit trouver ici tout le contenu (questions, réponses attendues, données des figures ou la règle pour les choisir : D-25) et la forme, sans revenir demander. Seule la validation du déroulé l'arrête (D-12).

### P4 — Le professeur l'année suivante, ou un collègue de l'équipe
Reprend l'activité en septembre prochain, éventuellement avec un autre emploi du temps. Il doit pouvoir recompiler, changer une figure, ajuster le minutage sans comprendre tout le paquet.

## Parcours

### U1 — Préparer la séance (P1)
1. La veille, il ouvre le PDF professeur et relit le déroulé de la séance (02-contenu).
2. Il imprime la fiche élève de la séance, une par élève, en noir et blanc (D-10, D-18).
3. Il vérifie que la page de scène s'affiche en plein écran au vidéoprojecteur (D-15).
4. Moment délicat : il doit retrouver la fiche de la séance 1 seule, sans imprimer la séance 2. D'où une fiche par séance (D-03, 03-forme).

### U2 — Séance 1 en classe (P1, P2)
1. Le professeur projette la scène « une figure qui glisse » et demande à l'oral : « Comment passe-t-on de l'une à l'autre ? »
2. Les binômes construisent l'image d'une figure sur quadrillage, tracent les flèches point → image et remplissent le cadre « ce qu'ont en commun ces flèches ».
3. Mise en commun : le professeur nomme direction, sens, longueur ; vecteur, origine, extrémité.
4. Les binômes trient des flèches (même translation ou non).
5. En fin de séance, les élèves complètent les trous du cours P1 listés dans 02-contenu (« Trous du cours P1, séance 1 »).
6. Moment délicat : la mise en commun commence à l'heure prévue même si des binômes n'ont pas fini (02-contenu donne la version minimale de chaque partie).

### U3 — Ce qui tourne mal (P1, P2)
- Un binôme bloque sur la construction de l'image : le professeur donne le coup de pouce de la partie (D-13).
- Un binôme a fini en dix minutes : il passe au « Pour aller plus loin » (D-13).
- Un élève confond « même direction » et « même sens » : c'est l'erreur prévue n° 1, la fiche de tri (partie B) contient exactement des flèches qui séparent les deux.
- Un élève écrit $ABDC$ au lieu de $ABCD$ en séance 2 : erreur prévue, traitée en mise en commun et reliée à la remarque sur l'ordre des sommets du cours P1 (D-20).
- La séance prend du retard : la fiche professeur indique, pour chaque séance, la partie qui peut sauter (02-contenu).

### U4 — Séance 2, puis le cours (P1, P2)
1. Rappel flash en tête de fiche (trois questions sur la séance 1).
2. Recherche en binômes sur la figure du parallélogramme, mise en commun sur l'égalité de vecteurs.
3. Construction de l'image d'un point par le parallélogramme (D-08).
4. Les élèves complètent les trous du cours P1 listés dans 02-contenu (« Trous du cours P1, séance 2 »).
5. Billet de sortie (D-14). La séance suivante, le professeur reprend le cours P1 au point fixé par D-24.

### U5 — L'élève absent (P2)
Il récupère la fiche de la séance manquée et la version corrigée (la partie « Solution » imprimée par le professeur). La fiche se comprend seule : chaque partie rappelle sa consigne sans renvoyer à l'oral.

### U6 — L'année suivante (P4)
1. Il ouvre `Activite_translations/CLAUDE.md` (03-forme) : il y trouve comment compiler et où sont les figures.
2. Il change un jeu de données dans `enonce_figures.tex` sans toucher aux énoncés.
3. Il adapte le minutage si son emploi du temps diffère : le minutage est seulement dans la fiche professeur.

## Besoins anticipés
- **Version professeur et version élève** (U1, U5) → un seul maître avec partie « Solution », comme l'activité Échantillonnage : D-06, 03-forme.
- **Une fiche par séance** (U1, U5) → D-03.
- **Minutage et version minimale de chaque partie** (U2, U3) → 02-contenu.
- **Coups de pouce et prolongement** (U3) → D-13.
- **Mesure de l'atteinte de l'objectif** (U4) → D-14.
- **Raccord des noms avec le cours** (U3, U4) → D-11, D-20.
- **Changer une figure sans toucher aux énoncés** (U6) → figures centralisées, 03-forme.
- **Version GeoGebra, version Typst, version numérique Moodle** → 06-perimetre.
