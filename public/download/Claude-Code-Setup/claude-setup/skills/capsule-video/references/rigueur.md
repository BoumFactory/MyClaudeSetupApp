# Référentiel de rigueur — toute capsule qui corrige ou explique des mathématiques

Une capsule de correction est une **copie modèle animée** : les élèves la regardent seuls, recopient ce qu'ils voient et révisent leur contrôle avec. Tout ce qui est dit ou affiché doit pouvoir être recopié tel quel dans une copie notée par un professeur exigeant.

Ce référentiel est abstrait (valable pour tout chapitre). Il a été construit à partir des retours du professeur sur une fournée de 23 corrections (03/10/2026) ; les exemples entre parenthèses viennent de là. Il complète `voix-synthese.md` (écriture pour l'oreille) et `design.md` (mise en scène).

`scripts/relire_script.py` détecte automatiquement une partie de ces fautes (liste en fin de fichier). Il ne remplace pas la relecture.

## 1. Rédaction des calculs

1. **Une égalité se dit « égale ».** Un calcul est une chaîne `A = B = C = résultat` ; chaque membre se prononce « égale … ». Interdits pour enchaîner deux membres : « soit », « ça fait », « c'est », « donne », un résultat jeté après deux-points (« … : 5 »).
2. **L'écran montre la copie.** Une seule chaîne d'égalités, chaque « = » affiché au moment où il est dit, les lignes de suite alignées sur le « = ».
3. **Le brouillon est séparé.** Tout calcul annexe (carré d'un négatif, somme de décimaux, produit intermédiaire) est annoncé « Au brouillon : … » et affiché dans un encart Brouillon distinct, jamais inséré entre deux membres de la chaîne.
4. **Aucune étape sautée dans une chaîne** (√(9 + 16) = √25 = 5, pas √(9 + 16) = 5) ; aucune valeur affirmée sans avoir été calculée à l'écran (une longueur qui sert d'argument est calculée). Pour une formule à différences élevées au carré, la chaîne type est : formule remplacée √((0 − 13)² + (0 − 1)²) → différences calculées √((−13)² + (−1)²) → carrés √(169 + 1) → résultat ; une quantité déjà connue entre par sa valeur au carré écrite (AC² + BC² = 5² + 10² = 25 + 100).
4 bis. **Un choix « par exemple » se justifie** : quand plusieurs objets jouent le même rôle (deux plus longs côtés de même longueur, deux sommets possibles), dire pourquoi le choix ne change rien ou traiter chaque cas.
5. **Formule générale, puis substitution, puis calcul** : on écrit d'abord la formule avec ses notations (x_B − x_A), ensuite les valeurs, avec parenthèses autour des négatifs.
6. **Équations** : une équation par ligne, l'opération effectuée des deux côtés est dite (« on soustrait 1 des deux côtés »). Toute solution est **vérifiée** par substitution, rédigée elle aussi en chaîne d'égalités.
7. **Valeur exacte, puis valeur approchée** avec la précision demandée et sa justification (chiffre suivant).

## 2. Vocabulaire : le bon objet, le bon verbe

8. **On calcule une grandeur attachée à un objet, pas l'objet** : les coordonnées d'un vecteur, la norme d'un vecteur, la longueur d'un segment, l'aire d'une figure (jamais « on calcule le vecteur / le point / le triangle »).
9. **On prouve qu'un objet a une propriété** : « prouver qu'un quadrilatère est un parallélogramme », « montrer que le triangle est rectangle » (jamais « prouver un parallélogramme », « pour un carré, … »).
10. **Une conclusion nomme ses objets** : « les vecteurs EF et HG ont les mêmes coordonnées : ils sont égaux. Donc EFGH est un parallélogramme. » (jamais « Égaux : … », « Mêmes coordonnées : … » sans sujet).
11. **Équivalence et implication dites comme telles** : « si, et seulement si » pour une équivalence ; nommer la propriété ou le théorème utilisé, avec ses hypothèses (repère orthonormé, triangle rectangle en…).
12. **Énoncer les propriétés du cours en entier**, cas limites compris (« parallélogramme, éventuellement aplati »).
13. **Unités et objets de mesure** : un déplacement « d'un côté de carré », « de deux carreaux », jamais « d'un carré » ; une longueur a une unité.
14. **Pas de raccourci d'élève** dans un « À retenir » : la phrase de synthèse est une propriété ou une méthode énoncée complètement, sujet, verbe, conditions.
14 bis. **Le parallélisme s'écrit toujours `//`** (notation française), jamais ∥ : règle fixe, pas une préférence. Dans une formule, écrire `\para` (ou `\parallel`) : le moteur affiche « // » dans les deux cas (`(AB) \para (CD)`). À l'oral : « la droite A B est parallèle à la droite C D ».

## 3. Écran

15. Aucun **état intermédiaire faux** lisible pendant une transformation (« 5,199… » pendant un arrondi) : effacer d'abord, écrire ensuite.
16. Aucun **recouvrement** de puces ou de cartes (la mise en page n'empêche que les débordements de cadre : soigner l'enchaînement à l'écriture ; planche seulement sur demande).
17. L'écran affiche le juste même si la voix trébuche ; il n'affiche rien que la voix ne justifie.

## 4. Synthèse vocale (Piper)

18. **Pas de lettre-étiquette après un mot à liaison** (« Cas a » est lu « saza ») : « Premier cas », « Deuxième cas ».
19. **Grammaire des formules dites** : « la racine carrée de : moins 5, entre parenthèses, au carré, plus … » (jamais « la racine carrée de le carré de … »).
20. Le reste (lettres isolées, fractions, parenthèses) : `voix-synthese.md` § Rigueur orale et § Prononciation.

## 5. Traiter un retour du professeur

21. **Un retour ponctuel révèle une règle.** Avant de corriger, formuler la règle générale (ex. « on calcule les vecteurs » → règle 8) ; la chercher par **motif large** dans TOUTE la fournée, scripts ET textes d'écran (`spec.js`), pas seulement l'occurrence citée.
22. Ajouter la règle ici (forme abstraite) et, si elle est détectable, son motif dans `relire_script.py`.
23. Reprise : sauvegarder (`version-N/`), corriger le script, `voix.py --modifies`, `transcrire.py`, faire raccrocher les ancres par l'animateur, re-contrôler, re-rendre.

## Motifs détectés par `relire_script.py`

« soit » / « ça fait » / « c'est » suivis d'un nombre, résultat après deux-points dans une phrase de calcul, « Cas a » (liaison), « calcule… le vecteur / point / triangle », « prouver un parallélogramme », conclusion « Égaux : », « racine carrée de : le carré ». Ajouter un motif à chaque nouveau retour généralisable.

**Forme orale** (`scripts/maths_parlees.py`) : toute notation qui serait lue telle quelle dans une phrase dite (`$`, `\`, `^`, `_`, `/`, ≤, ×, `[AB]`, « triangle RIS » collé…) donne une alerte qui **propose** la phrase réécrite (« le triangle $R-I-S$ » → « le triangle R I S »). Corriger `script.md` soi-même : les mots du script restent les mots dits, l'ancrage reste exact. `--appliquer` réécrit les phrases concernées (sauvegarde `script.avant-oral.md`). Les lignes `> visuel : …` ne sont pas relues (elles ne sont pas dites).
