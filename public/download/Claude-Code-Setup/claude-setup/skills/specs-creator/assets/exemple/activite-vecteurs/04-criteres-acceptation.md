# Critères d'acceptation

Chaque critère se vérifie en moins de 5 minutes, sur le PDF compilé ou dans les sources du dossier `Activite_translations/`.

## Déroulé (lot 1)

| ID | Critère | Comment vérifier | Lié à |
|---|---|---|---|
| CA-01 | Le déroulé minute par minute des deux séances totalise 55 minutes par séance et nomme, pour chaque temps, ce que fait le professeur et ce que font les élèves | Additionner les durées ; lire chaque ligne | D-03, D-12 |
| CA-02 | L'utilisateur a validé le déroulé avant toute rédaction LaTeX | Message de validation dans la session du lot 1 | D-12 |

## Contenu

| ID | Critère | Comment vérifier | Lié à |
|---|---|---|---|
| CA-03 | Chaque question de 02-contenu (rappel flash, parties A à D, « Pour aller plus loin », billet) figure dans le document, à l'endroit prévu par 03-forme, avec sa réponse dans la Solution ou les notes pour le professeur | Cocher la liste des questions de 02-contenu sur le PDF | 02-contenu, D-27 |
| CA-04 | La fiche élève ne parle ni de somme de vecteurs, ni de Chasles, ni de produit par un réel, ni de coordonnées | Rechercher « somme de », « Chasles », « produit », « coordonnée », « abscisse », « ordonnée » dans `enonce_seance1.tex`, `enonce_seance2.tex`, `annexes.tex` : aucun résultat ; aucun quadrillage n'a d'axes | D-05, 06-perimetre |
| CA-05 | Les figures respectent les données de 02-contenu : points des parties A et C, déplacements des six flèches de la partie B, $Q$ du « Pour aller plus loin » S1 | Lire les coordonnées dans `enonce_figures.tex` | D-17 |
| CA-06 | Aucune flèche de la partie B n'en croise une autre | Inspection de `planche_figures.pdf` | 02-contenu |
| CA-07 | Le parallélogramme de la séance 2 s'appelle $ABCD$ et l'égalité attendue est $\Vecteur{AB}=\Vecteur{DC}$ | Lire C3 et sa réponse | D-20 |
| CA-08 | Le vocabulaire (translation de vecteur, direction, sens, longueur, origine, extrémité, vecteur déplacement, représentant) est celui des blocs du cours P1 cités dans 02-contenu | Comparer avec `Cours/Definition/translation.tex`, `vecteur.tex`, `egalite_vecteurs.tex`, `representants_notation.tex` | D-07, D-11 |
| CA-09 | Les fiches élèves ne contiennent aucun environnement `Definition`, `Propriete` ou `Methode`, et exactement deux encadrés « Ce que l'on retient » | Rechercher ces noms d'environnements dans `enonce_seance1.tex` et `enonce_seance2.tex` ; compter les encadrés | D-07, D-08 |
| CA-10 | La page de cartes contient les trois coups de pouce (A, C, D), chacun deux fois, et chaque fiche finit par son « Pour aller plus loin » | Inspection du PDF | D-13 |

## Forme

| ID | Critère | Comment vérifier | Lié à |
|---|---|---|---|
| CA-11 | Le document compile en LuaLaTeX sans erreur ; son `.log` n'a aucune ligne « Overfull » ou « Underfull », et aucun avertissement absent de `Cours/Cours.log` du cours P1 | Commande de compilation de 03-forme, puis comparer `grep -E "Warning"` des deux `.log` et `grep -c -E "Overfull|Underfull"` (résultat 0) | D-30 |
| CA-12 | Chaque fiche élève tient sur deux pages au plus et commence sur une nouvelle page | Compter les pages du PDF | D-18 |
| CA-13 | Un seul accent de couleur, aucun aplat ni titre en boîte colorée ; chaque fiche reste lisible en niveaux de gris | `pdftoppm -gray -r 80 -png` sur les pages des fiches (MiKTeX fournit `pdftoppm`), puis lecture des images | D-10, D-28 |
| CA-14 | Les deux pages de scène sont en paysage, figure seule, sans texte de question, placées après les fiches | Inspection du PDF | D-15 |
| CA-15 | Les macros du cours P1 sont chargées par `\input{../Cours/commands_def}` et `\Vecteur` n'est redéfini nulle part dans le dossier | Recherche de `\newcommand{\Vecteur` et `\renewcommand{\Vecteur` dans le dossier | D-11 |
| CA-16 | Le `CLAUDE.md` du dossier donne la commande de compilation, les plages de pages à imprimer et l'emplacement des figures | Lecture du fichier | 03-forme |
| CA-17 | Le texte est en français correct, avec accents ; les noms de fichiers n'en ont pas | Relecture ; liste des fichiers | 03-forme |
