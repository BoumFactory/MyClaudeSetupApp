# Pagination, espacements et bandeaux d'EXO

À lire à l'**Étape 4** (inventaire des `\newpage`, `\Needspace`, `\medskip`, QCM, titres longs) et pour les **batchs de fin** de l'Étape 5. Couvre les Leviers 5 et 5bis, les Techniques T5 à T8, la Recette M (QCM) et le défaut D6 (`\Needspace`).

---

## Levier 5 — Retirer les `\newpage` et `\clearpage` devenus inutiles

**En fin de batch, jamais au début** : un `\newpage` a pu être ajouté pour régler un problème que seule la densification en amont fait disparaître.

1. `grep -n "newpage\|clearpage" <tex>`.
2. Classer chaque occurrence : séparation structurelle (cours → exercices) → garder ; ajout pour éviter un débordement désormais disparu → candidat ; isolé après un titre ou en fin de bloc → retirer.
3. Retirer dans un batch dédié, après un batch de colonnage ; recompiler 3 passes ; remettre le `\newpage` ciblé si un débordement réapparaît.

**Table des matières d'une fiche d'exercices** : sur une fiche de quelques `EXO`, `\tableofcontents` (avec le `\newpage` ou `\vfill\newpage` qui la suit) occupe une page sans valeur ajoutée. Candidat systématique au retrait dans le fichier principal ; la garder pour un cours, une séquence ou un recueil.

---

## Levier 5bis — Supprimer `\medskip`, `\smallskip`, `\bigskip`

Convention bfcours : ces commandes sont à supprimer partout où on les rencontre. L'aération est portée par les environnements (`EXO`, `Definition`, `Exemple`, `tcbenumerate`, `MultiColonnes`…). Si un espace supplémentaire est vraiment nécessaire : une ligne vide dans le source (`\par`), deux pour un effet plus marqué.

```bash
grep -nE "\\\\(medskip|smallskip|bigskip)" <tex>
```

Dans le même batch : ne pas redoubler les `\vspace{-X cm}` de compensation déjà présents ; remplacer les `\\` de fin de paragraphe par une ligne vide.

---

## D6 — Blanc en bas de page causé par un `\Needspace` surdimensionné

Une page finit sur un grand blanc et le source contient juste avant le saut un `\Needspace{Xcm}` dont `X` dépasse nettement la hauteur réelle du bloc protégé : LaTeX renvoie tout le bloc à la page suivante dès qu'il reste moins de `X`. Le colonnage en amont ne résout pas ce cas.

1. `grep -n "Needspace" <tex>`.
2. Pour chaque occurrence suivie d'un blanc (`bottom_fill` ou `bottom_half_fill` faibles) : estimer la hauteur du bloc (une ligne ≈ 0,5-0,6 cm en corps 11-12 ; bandeau d'EXO ≈ 1-1,5 cm ; ajouter les `raster row skip`) ou la mesurer sur une capture.
3. Si `X` dépasse la hauteur de plus de 20 % : recalibrer à la hauteur mesurée + 0,3 à 0,5 cm.

Vérifier que le blanc disparaît **et** que le bloc n'est pas coupé (valeur devenue trop faible). Calibrer, ne pas supprimer : le `\Needspace` protège d'un titre isolé en bas de page. Seule exception : bloc déjà insécable par ailleurs (tcolorbox atomique).

---

## Recette M — Scinder un QCM `Mcq` en plusieurs blocs

Un bloc `\begin{Mcq}[BFCours] … \end{Mcq}` est **non sécable**. Deux pathologies :

1. **Perte de contenu silencieuse** : dans un EXO (`save lower`), un bloc trop grand dépasse la boîte « upper » ; le `.log` affiche `Package tcolorbox Warning: The upper box part has become overfull` et **les dernières questions disparaissent du PDF**.
2. **Page 1 à moitié vide** : le bloc ne tient pas sous l'en-tête et saute en entier à la page suivante.

Remède unique : scinder ; l'option `resume` poursuit la numérotation.

```latex
\begin{Mcq}[BFCours]
... questions 1 à 4 ...
\end{Mcq}

\begin{Mcq}[BFCours, resume]
... questions 5 à 8 ...
\end{Mcq}
```

Taille du premier bloc : mesurer sur la capture l'espace libre sous l'intro (souvent 50-55 %), compter environ 10 % de page par question texte et 15 % avec figure, y caler 4 à 6 questions ; s'il saute encore, en pousser une dans le bloc suivant. Le reste en blocs d'environ 4 questions.

Vérifier : `grep -c "upper box part has become overfull"` = 0 pour les EXO de QCM ; toutes les questions apparaissent au rendu ; la page 1 est remplie. Un QCM scindé peut prendre **plus** de pages que la version tronquée : ce n'est pas une régression, on a récupéré du contenu. Toujours comparer à contenu égal.

---

## Technique T5 — Badge `\tcbitempoint` qui chevauche le texte

**Déclencheur, vu sur le PNG** : dans un `tcbenumerate[1]` d'énoncé, le badge de points (dessiné en surimpression en haut à droite, sans réserver de place) masque le dernier mot de la première ligne.

Correctif structurel : une première phrase courte (consigne et objet minimal, ≤ 70 % de la largeur), puis `\\` et le détail.

```latex
% AVANT : « entre » passe sous le badge
\tcbitem \tcbitempoint{1}\acc{Calculer} le \acc{coefficient multiplicateur global} $CM$ associé à l'évolution du nombre d'abonnés entre $2015$ et $2025$, puis en déduire le \acc{taux global d'évolution} en pourcentage.
% APRÈS
\tcbitem \tcbitempoint{1}\acc{Calculer} le coefficient $CM$ entre $2015$ et $2025$.\\
En déduire le \acc{taux global} d'évolution en pourcentage.
```

Le décalage `\tcbitempoint{X}[0cm][-0.5cm]` ne fait que déplacer le chevauchement d'une ligne : à réserver au cas d'une première ligne pleine suivie d'une deuxième courte. Ne pas appliquer sans chevauchement constaté, sur une correction, ni quand un sous-`tcbenumerate` suit immédiatement la consigne (il casse déjà la ligne).

---

## Technique T6 — Titre d'EXO qui wrappe sur deux lignes

**Déclencheur, vu sur le PNG** : le titre de `\begin{EXO}{Titre}{code}` occupe deux lignes du bandeau. Coût : une ligne pleine par EXO concerné ; deux ou trois titres longs suffisent à faire déborder une fiche.

Correctif : raccourcir en gardant le concept, souvent en supprimant le verbe d'action (l'énoncé porte la consigne, pas le bandeau).

- « Comparer moyenne arithmétique et moyenne géométrique » → « Moyennes arithmétique et géométrique »
- « Calculer des ordres de grandeur et des chiffres significatifs » → « Ordres de grandeur et chiffres significatifs »

Ne pas toucher un titre qui ne wrappe pas (la largeur dépend des coches de difficulté et de la pastille de score), ni un titre déjà minimal, ni au prix de la compétence visée. Contraintes de syntaxe du titre d'EXO bfcours : jamais de virgule, de mode math ni de commande (`\acc`, `\encadrer`…).

---

## Technique T7 — Permuter deux EXO

Déclencheurs, vus sur le PNG :

1. un bandeau d'EXO reste seul en bas de page et son premier bloc non sécable (`MultiColonnes`, figure latéralisée) part à la page suivante → l'échanger avec l'EXO suivant **s'il est sécable** (texte + liste de questions), qui remplit le bas de page ;
2. un exercice coupé par un saut de page alors qu'un autre ordre ferait tenir les deux exercices chacun en entier → estimer leurs hauteurs sur les PNG et la place restante avant de permuter.

Garde-fous : seulement des EXO de difficulté voisine (`\rdifficulty` égal ou proche) ou indépendants (jamais un contexte filé ou un résultat réutilisé) ; déplacer la ligne `\def\rdifficulty{…}` avec son EXO (par script écrit avec Write, jamais par heredoc) ; recompter les pages, le problème peut se déplacer plus loin.

---

## Technique T8 — `display score=false` sur une fiche sans barème

Fiche d'entraînement (pas une évaluation) dont le maître contient `display score` dans `\setrdexo{…}` : passer à `display score=false`. La pastille « /N » disparaît, le bandeau s'allège et les titres gagnent de la largeur (moins de T6). Premier réflexe sur une fiche à nombre de pages imposé ; garder `display score` sur les évaluations notées.
