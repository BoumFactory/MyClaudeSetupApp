# Référentiel : rendre une évaluation accessible (Éduscol, août 2026)

Distillation des quatre documents de la ressource « Rendre les mathématiques accessibles pour tous — Collège ». Les originaux sont dans `references/eduscol/` (dossier du skill ; à remplacer par les nouvelles versions pour mettre le référentiel à jour). Cite-les dans les constats avec leur sigle et leur page :

| Sigle | Document | Pages |
|---|---|---|
| `[GRILLE]` | Grille d'analyse du niveau d'accessibilisation (`grille-danalyse-du-niveau-d-accessibilisation-130069.pdf`) | 1 |
| `[OBJ]` | Accessibilité de l'évaluation : préserver les objectifs et critères de réussite (`accessibilite-de-levaluation-preserver-les-objectifs-et-criteres-de-reussite-130072.pdf`) | 3 |
| `[EX]` | Rendre les énoncés d'évaluation accessibles : exemples de modifications (`rendre-les-enonces-devaluation-accessibles-exemples-130075.pdf`) | 7 |
| `[VERS]` | Vers une évaluation accessible à tous en mathématiques au collège (`vers-une-evaluation-accessible-tous-en-mathematiques-au-college-130060.pdf`) | 15 |

## Sommaire

1. Le principe qui commande tout : préserver l'objectif et les critères de réussite
2. La grille en neuf dimensions (avec sa lecture pour un sujet d'évaluation)
3. Catalogue des obstacles, avec codes
4. Les trois cas d'école commentés
5. Avant, pendant, après l'évaluation (conditions de passation)
6. Garde-fous : ce que l'accessibilisation n'est pas
7. Transposer au lycée

---

## 1. Le principe qui commande tout

> « Faire évoluer les énoncés dans un cadre d'accessibilité doit permettre de maintenir les exigences initiales, en construisant différemment le projet pédagogique. […] il faut éliminer les obstacles qui pourraient faire chuter l'élève avant d'atteindre l'objectif principal. » `[OBJ]` p. 3

Toute évaluation vise un **objectif** (ce qu'on veut savoir de l'élève) décliné en **critères de réussite** observables. Exemple `[OBJ]` p. 1 : l'objectif « comparer des nombres relatifs » se décline en « l'élève manifeste une intention d'ordonner », « sait qu'un négatif est inférieur à un positif », « sait ordonner des négatifs ».

Conséquence pour l'analyse : **un obstacle est tout ce qui peut faire échouer l'élève pour une raison étrangère à l'objectif visé** (lecture, vocabulaire non évalué, mise en page, enchaînement en cascade, absence de point de départ…). À l'inverse, une difficulté qui **est** l'objectif n'est pas un obstacle : la retirer dénature l'évaluation.

Pour chaque exercice, commence donc par écrire son objectif et ses critères de réussite. Chaque piste proposée doit dire ce qu'elle préserve.

Autres points de `[OBJ]` :
- Objectifs et critères de réussite **doivent être explicités aux élèves** (p. 1).
- Après l'évaluation, valider ou invalider **explicitement sur la copie** les critères de réussite : c'est ce qui donne du sens à la note (p. 3).
- Un mot de vocabulaire hors objectif (« double ») peut faire échouer tout l'exercice : on le retire de l'évaluation et on l'évalue **ailleurs**, par exemple en automatismes (p. 3).
- Un cadre de réponse (cases à remplir, exemple travaillé) est légitime quand la notion est en découverte ; il devra disparaître à l'approche de l'examen, où l'élève doit identifier seul les étapes (p. 3).

## 2. La grille en neuf dimensions `[GRILLE]`

Chaque dimension se cote **Aucun / Partiel / Avancé**. La grille vise l'enseignement en général : certaines dimensions s'appliquent mal à un sujet écrit individuel. Ne force pas : cote « Non applicable au sujet » et dis ce qui pourrait en relever autour de l'épreuve (consignes orales, correction collective…).

| Clé JSON | Dimension | Contenu selon la grille | Lecture pour un sujet d'évaluation |
|---|---|---|---|
| `mise_en_forme` | Mise en forme des documents | Police lisible, interligne et couleurs dédiés, zonage, absence de visuels distracteurs et de justification des textes. Note : police Arial recommandée, corps 12 ou 14, interligne 1,3 à 1,5. | Police, corps, interligne (mesurés par le script), texte justifié, colonnes, zonage texte / tableau / figure, éléments décoratifs, qualité de reproduction, espace de réponse. |
| `ancrages_linguistiques` | Ancrages linguistiques | Vocabulaire expliqué, glossaire, contextualisation. | Mots hors objectif, phrases longues, verbes de consigne ambigus, contexte qui n'aide pas, définitions données au bon endroit. |
| `sequencage` | Séquençage des tâches | Objectifs ciblés, outils en adéquation avec les objectifs, découpage en étapes, progressivité, sens explicité. | Une consigne = une action, questions emboîtées, progressivité dans l'exercice, amorce, résultats intermédiaires fournis, objectifs annoncés. |
| `non_verbal` | Communication non verbale | Gestes, pictogrammes pertinents, supports visuels. | Pictogrammes utiles (calculatrice autorisée, brouillon), schéma ou tableau qui porte l'information, exemple travaillé. Les pictogrammes décoratifs sont au contraire des distracteurs. |
| `materiel` | Matériel de manipulation | Outils concrets, supports kinesthésiques, numériques. | Matériel autorisé écrit sur le sujet (calculatrice, instruments, fiche-outil) ; tâches de construction réalisables par un élève empêché dans les manipulations. |
| `repetition` | Répétition et renforcement | Répétition variée, réactivation des acquis. | Variété des formats de question (`[VERS]` p. 3 : question de cours, vrai-faux, QCM, tableau à compléter, question fermée, problème ouvert), automatismes qui réactivent, même compétence sous deux formes. |
| `appartenance` | Sentiment d'appartenance | Rôle social, coopération, synthèse collective. | Le plus souvent non applicable à un sujet individuel ; relève de la correction collective ou du tutorat après l'évaluation. |
| `autonomie` | Autonomie | Choix, outils d'aide, étayage, auto-évaluation, fiche mémo. | Exercices ou questions au choix (conséquences explicitées), coup de pouce ou appel au professeur prévu, fiche-outil autorisée, critères de réussite lisibles par l'élève, auto-positionnement. |
| `reussite` | Sentiment de réussite | Tâches dans la zone proximale de développement, feedback positif, valorisation. | Entrée accessible dans chaque exercice, première question réussissable par tous, mention « toute démarche même non aboutie est valorisée », barème lisible, pas d'échec en cascade. |

## 3. Catalogue des obstacles

Les codes servent dans le champ `code` des constats. La colonne « Exemple Éduscol » donne le cas réel qui fonde l'obstacle.

### Mise en forme (MF)

| Code | Obstacle | Pistes types | Exemple Éduscol |
|---|---|---|---|
| MF1 | Corps de police trop petit, police peu lisible | Corps 12 au moins, police sans empattement | Note de `[GRILLE]` |
| MF2 | Interligne ou espacement des lettres serrés | Interligne 1,3 à 1,5 ; espacement augmenté | `[EX]` p. 4 et 6 |
| MF3 | Présentation en colonnes : texte d'un côté, tableau ou figure de l'autre, ou deux tâches côte à côte | Présentation linéaire, de haut en bas | `[EX]` p. 2 et 4 : « Présentation en colonnes coûteuse cognitivement » |
| MF4 | Visuel distracteur : illustration, photo, pictogramme décoratif | Supprimer ce qui n'aide pas à comprendre | `[EX]` p. 1 |
| MF5 | Texte justifié (espaces irréguliers entre les mots) | Aligner à gauche | `[GRILLE]` |
| MF6 | Zonage confus : texte, tableau et figure mêlés ; support éloigné de la question où l'élève agit dessus | Mettre le tableau dans la question qui le fait compléter, la figure dans celle qui la fait tracer | `[EX]` p. 4 |
| MF7 | Reproduction de mauvaise qualité (scan, photocopie de manuel) | Retaper l'exercice | `[EX]` p. 4 et 6 |
| MF8 | Pas d'espace de réponse ou de recherche ; consigne « recopier » qui fait refaire un travail sans enjeu | Espace dédié à chaque question, brouillon encouragé ; fournir le support à compléter | `[EX]` p. 1 : « Un espace dédié est prévu pour chaque question afin de permettre, et même d'encourager, la recherche intermédiaire » |

### Ancrages linguistiques (AL)

| Code | Obstacle | Pistes types | Exemple Éduscol |
|---|---|---|---|
| AL1 | Mot hors objectif dont la méconnaissance fait échouer | Remplacer par un mot courant ; évaluer ce vocabulaire ailleurs | « double » retiré `[OBJ]` p. 3 ; « Dégagement » → « Couloir » `[EX]` p. 4 |
| AL2 | Phrase longue, imbriquée, négations, informations dispersées | Phrases courtes, une information par phrase, données regroupées | `[EX]` p. 1 |
| AL3 | Verbe de consigne ambigu ou mal choisi | Distinguer « placer » et « construire », « calculer » et « justifier » | `[EX]` p. 2 |
| AL4 | Contexte qui n'aide pas, ou dont la lecture coûte plus qu'il n'apporte | Contexte court et familier, ou contexte retiré | `[EX]` p. 1 |
| AL5 | Notation ou nommage déroutant (ordre alphabétique cassé, lettres proches) | Rétablir l'ordre, nommer de façon parlante | « EGHF » → « EFGH » `[EX]` p. 2 |

### Séquençage des tâches (ST)

| Code | Obstacle | Pistes types | Exemple Éduscol |
|---|---|---|---|
| ST1 | Double consigne dans une phrase unique | Une question par action, numérotée | `[EX]` p. 2 et 4 |
| ST2 | Questions emboîtées : échouer à l'une empêche la suivante | Donner le résultat intermédiaire, ou une piste (« il est utile d'effectuer deux calculs ») | `[EX]` p. 6 |
| ST3 | Saut de difficulté, pas de progressivité | Ajouter une question intermédiaire qui isole l'obstacle | Ajout « Quelle est la condition pour qu'un rectangle soit un carré ? » `[EX]` p. 6-7 |
| ST4 | Tâche complexe sans point de départ | Amorce : un rayon déjà tracé, une case déjà remplie, un exemple travaillé | `[EX]` p. 4-5 ; exemple travaillé `[OBJ]` p. 2 |
| ST5 | Objectif ou critères de réussite non annoncés à l'élève | Annoncer les compétences évaluées, au moins par exercice. En bfcours, le cartouche est généré à partir des titres d'`EXO` : la piste consiste à raccourcir le titre pour qu'il nomme la compétence du programme, sans ajouter de libellé | `[OBJ]` p. 1 ; `[VERS]` p. 2 |
| ST6 | Donnée ou unité manquante qui fait perdre le sens | Ajouter l'unité (« en m² »), le total | `[EX]` p. 4 |
| ST7 | Ordre des données qui complique la tâche | Rapprocher la donnée la plus simple de celle qui sert de référence | Colonne « Cuisine » rapprochée du « Total » `[EX]` p. 4 |
| ST8 | Question de généralisation ou de contre-exemple posée sans étape | Scinder : choisir une valeur, calculer, puis conclure | `[EX]` p. 6-7 |
| ST9 | Compétence clandestine : la question exige, en plus de ce qu'elle évalue, une compétence non annoncée ou évaluée ailleurs (traduire un mot en événement, interpréter une comparaison, un calcul hors objectif) | Fournir l'élément non visé (la notation, le résultat), ou déplacer la question vers l'exercice qui évalue cette compétence | Le mot « double » retiré parce que le vocabulaire n'est pas l'objectif `[OBJ]` p. 3 ; « il est utile d'effectuer deux calculs » `[EX]` p. 6 |

### Les autres dimensions

| Code | Dimension | Obstacle |
|---|---|---|
| NV1 | `non_verbal` | Aucun support visuel là où il porterait l'information (schéma, tableau à compléter, arbre amorcé) |
| NV2 | `non_verbal` | Pictogramme ou couleur sans fonction (relève aussi de MF4) |
| MA1 | `materiel` | Matériel autorisé non écrit sur le sujet (calculatrice, instruments, fiche-outil) `[VERS]` p. 2-3 |
| MA2 | `materiel` | Tâche de tracé ou de construction irréalisable pour un élève empêché dans les manipulations, sans alternative (« on admet l'à-peu-près d'un placement à main levée ») `[EX]` p. 2 |
| RE1 | `repetition` | Un seul format de question dans tout le sujet `[VERS]` p. 3 |
| AU1 | `autonomie` | Aucun étayage prévu : ni coup de pouce, ni appel au professeur, ni fiche-outil `[VERS]` p. 3 |
| AU2 | `autonomie` | Choix laissés à l'élève sans que leurs conséquences soient explicitées `[VERS]` p. 3 |
| RS1 | `reussite` | Exercice sans entrée réussissable par tous |
| RS2 | `reussite` | Démarches non valorisées, ou non annoncées comme valorisées `[VERS]` p. 3 |
| RS3 | `reussite` | Barème qui fait reposer une large part de la note sur une seule question bloquante |

## 4. Les trois cas d'école commentés `[EX]`

Ils fixent le niveau de détail attendu : une difficulté identifiée a priori, une réponse précise.

**Parallélogrammes** (p. 2-3). Original : « Construire les points H et D tels que EGHF et ABCD soient des parallélogrammes », deux figures côte à côte. Difficultés : lecture en colonnes, double consigne en une phrase, ordre alphabétique cassé, construction impossible pour un élève empêché, verbe « construire » trompeur pour un placement sur quadrillage. Version modifiée : deux questions linéaires, « 1. Placer le point H pour que EFGH soit un parallélogramme », « 2. Construire le point D… ». Remarque : on laisse de la place autour des points pour que la présentation n'induise pas la réponse.

**Tableau de proportionnalité et diagramme circulaire** (p. 4-5). Original : photocopie de manuel, tableau dans le texte, cercle à côté, une consigne double. Modifié : texte retapé et aéré, deux questions linéaires, tableau dans la question 1 et disque dans la question 2, « Dégagement » remplacé par « Couloir », total de 90 ajouté dans le tableau, colonne « Cuisine » (10 m², le calcul le plus simple) rapprochée du total, « en m² » ajouté, un rayon tracé en amorce dans le disque. Remarque : on aurait pu scinder en deux exercices ; on garde un seul exercice parce que l'enseignant veut travailler la proportionnalité au service du diagramme, quitte à compléter le tableau pour l'élève bloqué afin qu'il puisse tracer.

**Rectangle et calcul littéral** (p. 6-7). Original : photocopie floue, « 1. Prouver que si x = 2, alors ce rectangle est un carré. 2. Est-ce le cas pour n'importe quelle valeur de x ? ». Modifié : « 1. Quelle est la condition pour qu'un rectangle soit un carré ? » (obstacle : croire qu'un carré n'est pas un rectangle) ; « 2. À l'aide de deux calculs, prouver que si x = 2… » (piste donnée) ; « 3. Choisir une autre valeur pour x : je choisis x = …, je calcule 3x + 1 = …, 2x + 3 = … » ; « 4. Ce rectangle est-il carré pour toutes les valeurs de x ? ». Lignes de réponse sous chaque question. L'enseignant identifie ainsi plus finement les réussites et les obstacles.

**Programmes de calcul** `[OBJ]` p. 1-3. Objectif : produire une expression littérale à partir d'un programme en langage naturel. Critères : traduire les opérations, respecter les priorités (parenthèses). Version modifiée : un exemple travaillé en tête (« Voici un exemple de ce que tu dois faire »), des chaînes de cases fléchées, deux programmes courts ajoutés avant les programmes originaux pour une progression graduée, le mot « double » remplacé par « Multiplie-le par 2 ».

## 5. Avant, pendant, après l'évaluation `[VERS]` p. 2-3

Ces recommandations alimentent la section « Conditions de passation » du rapport. Certaines se traduisent dans le sujet (une ligne d'en-tête), d'autres dans la pratique de l'enseignant.

**Avant** : annoncer pour chaque évaluation les objectifs, les compétences évaluées et les critères de réussite ; préciser le matériel autorisé ; concevoir des énoncés lisibles aux consignes explicites ; respecter les PAP, PAI et PPS (format du sujet, temps, matériel, fiches-outils, matrices) ; alterner écrit, oral, numérique ; associer les élèves (autoévaluation, pairs).

**Pendant** : expliciter les consignes à l'écrit et, si utile, à l'oral ; rappeler le matériel autorisé ; varier les types de questionnement ; encourager le brouillon et préciser que toute démarche, même non aboutie, sera valorisée ; selon la finalité, autoriser des « appels au professeur » ou des exercices différenciés, conséquences explicitées en amont ; inciter à relire et à vérifier la vraisemblance des résultats.

**Après** : feedback constructif, correction détaillée impliquant les élèves ; éviter classements et comparaisons ; valoriser les progrès et donner des pistes concrètes ; remédiation (correction collaborative, tutorat, exercices ciblés) ; droit à l'erreur et rattrapage quand c'est possible ; robustesse de la moyenne ; appréciation centrée sur les niveaux de maîtrise ; vigilance sur les biais de genre ; travail sur le statut de l'erreur.

Les types d'évaluation (p. 1-2) : diagnostique, formative, formatrice, sommative, certificative, pronostique. Le type change le niveau d'étayage acceptable : l'annexe 1 (p. 8-10) montre, sur les équations, un coup de pouce possible en sommative et un sujet sans étayage en certificative (DNB).

## 6. Garde-fous

- **Accessibiliser n'est pas simplifier l'objectif.** Un guidage qui fait à la place de l'élève ce que l'exercice évalue supprime l'information recherchée. Exemple : si l'exercice évalue « construire un arbre pondéré », fournir l'arbre déjà dessiné avec ses branches retire la compétence ; en fournir la structure vide peut être légitime en découverte, pas en fin de cycle.
- **Accessibilisation pour tous ≠ adaptations individuelles.** Le PAP, le PPS, les fiches-outils et les matrices d'accompagnement répondent à des besoins individuels `[VERS]` p. 3-5. Le rapport peut les mentionner, il ne les remplace pas.
- **Une matrice d'accompagnement ne contient jamais de connaissances** dans un cadre d'examen ou de contrôle continu, et elle est propre à un élève `[VERS]` p. 5 et 11.
- **L'étayage diminue à l'approche de l'examen** `[OBJ]` p. 3 : ce qui convient à une évaluation de découverte ne convient plus à un sujet type bac ou DNB. Le rapport le signale quand une piste ajoute de l'étayage à un sujet proche de l'échéance.
- **La longueur n'est pas un obstacle en soi** : la version accessible du rectangle est plus longue que l'originale. Mais un sujet allongé sans changer la durée crée un autre obstacle (le temps) : quand une piste ajoute des questions, dis si elle demande d'en retirer ailleurs ou d'allonger la durée.

## 7. Transposer au lycée

Les documents visent le collège ; les principes valent au lycée. Deux nuances :
- l'échéance de l'examen (épreuve anticipée de mathématiques en 1re, bac) justifie de rapprocher progressivement le format du sujet de celui de l'épreuve ; un étayage fort doit donc être assumé comme transitoire ;
- les élèves de voie technologique sont plus souvent mis en difficulté par la lecture d'un énoncé long que par la technique : les obstacles AL2, MF3 et ST1 y pèsent davantage.
