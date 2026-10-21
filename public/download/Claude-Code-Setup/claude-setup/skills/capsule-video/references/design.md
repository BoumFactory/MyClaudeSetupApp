# Système de conception « capsule »

Une capsule réussie est **captivante** (ça bouge, c'est beau, ça récompense) et **lisible** (on sait toujours où regarder). Les deux ne s'opposent pas si chaque mouvement a un sens.

## Principes (Mayer, appliqués)

1. **Contiguïté temporelle** : le geste arrive sur le mot. Ancrer sur l'index du mot, anticiper de 0,1 à 0,3 s.
2. **Signalisation** : un seul foyer d'attention à la fois (`focus`, `allume`, `pointe`). Si tout brille, rien ne brille.
3. **Mouvement = sens** :
   - `vole` = « on prend ce nombre et on le met là » (prélèvement dans une donnée) ;
   - `tombe` = « voilà la donnée / le résultat, posé » ;
   - `allume` ligne/colonne = « on se restreint à cette population » (conditionnement, total de ligne) ;
   - `entoure` = « celui-ci précisément » ; `encadre` = résultat final ; `eclat` = récompense (réservé aux résultats).
4. **Persistance** : les données et les résultats déjà établis restent à l'écran (le tableau, les lignes de calcul empilées). L'élève peut toujours revenir à ce qui précède. Un résultat ou une conclusion reste lisible **en entier au moins 1,5 s** avant tout effacement : finir son `ecrit` tôt (`dur` ≤ 0,8), effacer la scène au début du temps fort suivant (`'@b19-0.4'`), jamais à `'@b18.fin+0.2'` ; si la pause est trop courte, l'allonger dans le script (`[pause 1.5]`, sans resynthèse).
5. **Pas de redondance** : pas de sous-titres intégraux par défaut (la voix les dit déjà) ; à l'écran, des **mots-clés** et des **formules**, jamais la phrase prononcée. Sous-titres (`sousTitres: true` + `corrections`) seulement sur demande (accessibilité).
6. **Le visuel est juste même quand la voix trébuche** : l'écran corrige les lapsus, la réponse précise s'affiche.
7. **Rythme** : un élément nouveau toutes les 2 à 6 s environ. Un silence de plus de 3 s sans rien à l'écran est un trou : y placer une respiration (pulse, pointeur, mise au point).

## Thème « nuit » (défaut)

- Fond bleu nuit, halos colorés flous en mouvement lent (`ambiance: true`), trame de points.
- Cartes en verre (`{ carte, couleur: 'violet' }`), puces (`{ puce }`), lettres d'événements (`{ lettre: 'M' }`), résultats en pilule (`{ resultat }`).
- Couleurs **sémantiques**, fixées pour toute la capsule : une couleur par objet mathématique (ex. M = violet, B = cyan, intersection/total = ambre, résultat = vert ou couleur de l'objet). Ne jamais réutiliser une couleur pour un autre objet.
- Police Atkinson Hyperlegible (lisibilité maximale en projection), formules en TeX (MathJax).
- **Atkinson barre ses zéros** (« 2ØØ patients », « Ø,Ø4 ») : glyphe étranger aux documents de maths français. Toute **valeur numérique** (poids d'un arbre, pourcentage, effectif, résultat), même dans une phrase ou une pastille, se rend en TeX (`$0{,}04$`, `$60~\%$`, `\mathbf{250}` pour un nombre en gras ; les nombres d'un `tableau` le sont d'office) ; Atkinson reste pour les mots. Relevé le 04/10/2026 sur une planche de cours.
- Tailles minimales à 1920×1080 : texte courant 34 px, données 56 px et plus, résultats 60 px et plus. Une capsule est souvent vue sur un téléphone : grossir plutôt que réduire.

`theme: 'jour'` : même système sur fond clair, pour une projection en salle très éclairée.

## Mises en page types

### Correction d'exercice à données (tableau, effectifs, pourcentages)
```
┌ bandeau : contexte (gauche) ··················· puce « Question n » (droite) ┐
│ cartes des événements / données de l'énoncé (une ligne)                       │
│ ┌──── tableau / figure (≈ 960 px) ────┐   ┌── panneau de calcul (≈ 730 px) ──┐ │
│ │ { tableau }, cases 'tab-l1c2'       │   │ ligne 1 : P(M) = □/□ = résultat  │ │
│ │                                     │   │ ligne 2 …  (les lignes s'empilent)│ │
│ └─────────────────────────────────────┘   └──────────────────────────────────┘ │
│ bandeau bas : remarque, mot-clé, piège (« et » ⟶ ∩)                            │
└────────────────────────────────────────────────────────────────────────────────┘
```
Scène d'ouverture plein écran (titre, contexte en grand, compteur des effectifs), puis bascule sur cette scène unique jusqu'à la fin.

### Calcul en chaîne (équation, factorisation, dérivée)
Une colonne centrale de lignes de calcul ; chaque nouvelle ligne `ecrit`, le terme transformé `allume` sur la ligne d'avant puis `vole` vers la nouvelle ; justification en puce à droite de la ligne.

### Taille des formules : un préréglage, pas des valeurs en dur
La clé `formules` de `spec.js` (préférence de l'utilisateur, `moteur-canvas.md` § Taille des formules) décide du découpage des scènes :
- **`grandes`** (formule ≈ 64 px, objet principal de l'écran) : une étape par écran, les lignes précédentes s'effacent ou se compactent (`C.compacte`). Si le moteur avertit « formules réduites de plus de 20 % », couper la scène en deux étapes.
- **`compactes`** (formule à la taille du texte, aérée) : la rédaction complète reste visible et se construit ligne par ligne ; la place gagnée ne sert que si la scène contient vraiment plus.
Une scène peut surcharger le réglage (`formules: 'compactes'` sur une scène de rédaction finale). Ne jamais poser `tailleTex` ou `taille` en dur sur une carte de calcul pour imiter l'autre préréglage.

### Figure ou graphique (fonction, géométrie)
Élément `figure` (primitives : segments, droites, arcs, codages, étiquettes TeX), objets tracés par `C.trace`, points qui `tombe`nt, lecture graphique par `pointe` + traits pointillés tracés. Courbe de fonction : `chemin` (chemin SVG calculé dans spec.js) tracé par `C.trace`.

### Explication sur l'IA (concepts, schémas)
Scènes plus nombreuses (une idée par scène), schémas de blocs reliés par `fleche`, métaphores visuelles (jetons qui défilent, tableau de probabilités du mot suivant avec barres animées via `compte` + largeur). Garder le même système de couleurs.

## Recettes éprouvées

- **Tableau qui se remplit** : `montre('#tab')` puis `tombe([...cases intérieures], t, {stagger:0.28})`, puis les totaux, puis le grand total en dernier avec `eclat` modeste.
- **« Chaque nombre est un effectif »** : `pointe` sur une case + `allume` + bulle explicative reliée par `fleche`.
- **Probabilité = case / total** : `allume` la ligne ou colonne concernée, `vole` l'effectif vers le numérateur, `allume` le total, `vole` vers le dénominateur, `montre('=')`, `tombe` du résultat + `eclat`.
- **Intersection** : `allume` la ligne (couleur A) puis la colonne (couleur B) : la case au croisement est éclairée deux fois ; `pulse` sur elle ; carte « « et » ⟶ ∩ ».
- **Fin** : `defocus`, `pulse` en cascade sur tous les résultats, `encadre` du dernier.

### Dérouler puis compacter un calcul (rigueur + trace du raisonnement)

Une étape qui demande des calculs intermédiaires (coordonnées d'un vecteur, distance, milieu, résolution) :
1. **Dérouler** : la carte de l'étape affiche une ligne par opération, au rythme de la voix (formule générale → valeurs remplacées, nombres qui `vole`nt depuis la figure → calcul → résultat qui `tombe`). Rien n'est sauté : c'est la rigueur.
2. **Compacter** : quand la voix conclut, `C.compacte(lignesDetaillees, '#resume-etape', t, { depuis: '#resultat', couleur: '--vert' })` replie les lignes et range le résultat dans une puce de l'en-tête de l'étape (« Étape 2 · AB(3 ; 2) »). La carte redevient petite : place libre pour l'étape suivante.
3. **Trace** : les puces de résultat restent affichées jusqu'à la fin de l'exercice ; la conclusion les `allume` une à une en les citant (« AB = DC, donc… »).

Mise en page : puce de résumé dans l'en-tête, AU-DESSUS des lignes détaillées (les positions sont mesurées à la construction) ; empiler les étapes en colonne, chacune repliée après usage. Le repli fait remonter tout ce qui suit et rétrécit les cartes traversées ; la mise en page garantit que les lignes longues tiennent dans la carte.

### Milieu, moyenne et lecture de coordonnées

Une propriété « coordonnée par coordonnée » se montre sur une figure **générique** (segment oblique, points non alignés avec les axes), jamais sur un cas où une coordonnée est constante. Exemple, milieu = moyenne : segment [AB] oblique ; une droite verticale glisse sur l'axe des abscisses de x_A à x_B et s'arrête à la moyenne (x_I) ; une droite horizontale glisse sur l'axe des ordonnées jusqu'à y_I ; I apparaît à l'intersection des deux droites, avec ses deux coordonnées.
