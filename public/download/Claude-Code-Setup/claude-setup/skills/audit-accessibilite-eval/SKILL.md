---
name: audit-accessibilite-eval
description: Analyse l'accessibilité d'une évaluation (DS, contrôle, interro, sujet type bac ou brevet, en .tex, .pdf, .docx ou .odt) à la lumière des ressources Éduscol 2026 « Rendre les mathématiques accessibles pour tous » (grille d'accessibilisation en 9 dimensions, préservation des objectifs et critères de réussite, exemples de modifications d'énoncés, évaluation accessible à tous). Produit un rapport HTML local avec captures d'écran des zones problématiques (fichiers PNG surlignés par Pillow), grille complétée, explication de chaque obstacle et pistes d'amélioration avec reformulations avant/après ; l'enseignant coche, annote et copie un prompt qui fait appliquer ses choix par un agent. Gère aussi ce retour (application des modifications retenues). Utiliser dès que l'utilisateur veut rendre une évaluation plus accessible, inclusive ou lisible, parle d'élèves à besoins particuliers (EBEP, PAP, PPS, dys) face à un sujet, demande un audit, une relecture ou une analyse d'accessibilité d'un devoir, veut savoir ce qui peut faire échouer un élève pour d'autres raisons que la notion évaluée, mentionne la grille Éduscol d'accessibilisation, ou colle un prompt commençant par « Appliquer les améliorations d'accessibilité retenues » — même sans prononcer le mot « accessibilité ».
---

# Audit d'accessibilité d'une évaluation

## Ce que produit ce skill, et pour qui

L'enseignant lance l'audit sur un sujet. Il reçoit, dans un dossier à côté du sujet, un **rapport HTML qu'il ouvre localement** : chaque obstacle est montré par une capture de la zone exacte, expliqué, rattaché au référentiel Éduscol, accompagné de pistes concrètes. Il coche ce qu'il retient, écrit ses remarques, clique sur « Copier le prompt pour l'agent » et colle ce prompt dans Claude Code : un agent applique alors exactement ses choix.

La valeur du rapport tient à trois choses : la **précision** (on voit la zone, on lit la reformulation proposée), la **justesse didactique** (un obstacle est ce qui fait échouer pour une raison étrangère à l'objectif, pas la difficulté de la notion elle-même) et l'**honnêteté** (ni complaisance, ni obstacle inventé pour remplir).

## Ressources du skill

- `references/referentiel-eduscol.md` — la distillation des quatre documents Éduscol : principe directeur, grille, catalogue d'obstacles codés (MF, AL, ST…), cas d'école, avant / pendant / après, garde-fous. **Lis-le en entier avant d'analyser** : il fixe le vocabulaire, les codes et le niveau de détail attendu.
- `references/schema-constats.md` — le format du `constats.json` que tu rédiges.
- `scripts/preparer_eval.py` — PDF, aperçus de pages, blocs de texte localisés, mesures de mise en forme.
- `scripts/capturer_zones.py` — captures surlignées (Pillow) et aperçus de pages annotés.
- `scripts/generer_rapport.py` + `assets/rapport_template.html` — le rapport interactif.
- `references/eduscol/` — les quatre PDF Éduscol originaux (noms de fichiers dans l'en-tête du référentiel) ; tu n'as besoin d'y revenir que pour vérifier une citation ou mettre le référentiel à jour quand Éduscol publie une nouvelle version.

Prérequis : `pip install pymupdf pillow` ; LibreOffice pour les sujets `.docx` / `.odt` ; une distribution LaTeX seulement pour recompiler un `.tex`.

Toutes les commandes se lancent depuis la racine du projet avec `PYTHONIOENCODING=utf-8 python ".claude/skills/audit-accessibilite-eval/scripts/…"`.

## Déroulé de l'audit

### 1. Réunir le contexte

Avant de regarder le sujet, cherche ce qui dit **ce que l'évaluation veut mesurer** et **ce que l'enseignant s'impose** :
- le `CLAUDE.md` ou le `README` du dossier du sujet, les commentaires en tête du `.tex` (souvent : compétences, barème, périmètre, contraintes de pages) ;
- le niveau, la durée, le barème, le type d'évaluation (diagnostique, formative, sommative…) et l'échéance d'examen ;
- le dossier de cours voisin si les objectifs ne sont écrits nulle part.

Si une information manque, déduis-la du sujet et marque-la `"deduit": true` plutôt que d'interrompre l'enseignant. Les contraintes qu'il s'est données (nombre de pages, une compétence par exercice…) vont dans `contraintes_enseignant` : tes pistes devront s'y confronter ouvertement.

### 2. Préparer les pièces

```bash
PYTHONIOENCODING=utf-8 python ".claude/skills/audit-accessibilite-eval/scripts/preparer_eval.py" --source "<chemin du sujet>" [--compiler] [--pages 1-2]
```

- Un fragment `.tex` (sans `\documentclass`) est rattaché automatiquement à son maître. Si le script signale un PDF plus ancien que les sources, relance avec `--compiler` : analyser une version périmée ferait des captures fausses.
- Les pages de corrigé sont détectées (« Solution », « Corrigé »…) et exclues des mesures ; vérifie la ligne « Pages d'énoncé » et corrige avec `--pages` si besoin.
- Le dossier d'audit créé est `<dossier du sujet>/audit_accessibilite/<date_heure>/` ; sa dernière ligne de sortie donne le chemin.

### 3. Regarder le sujet comme un élève

Ouvre chaque `pages/page-NN.png` de l'énoncé avec Read. Le texte seul ne montre ni les colonnes, ni la densité, ni la place laissée pour répondre, ni une figure illisible. Lis ensuite la source (`.tex`, ou le texte de `mise_en_page.json`) pour le détail des formulations.

Puis fais **passer le sujet mentalement** à quelques profils d'élèves types (ou aux élèves réels de la classe si l'enseignant en parle), question par question :
- un élève qui lit lentement ou mal (dyslexie, allophone, voie technologique fragile en lecture) : où décroche-t-il ? quelle phrase doit-il relire trois fois ? quel mot ne connaît-il pas ?
- un élève qui rate la question 1 : que peut-il encore faire ensuite ?
- un élève empêché dans le geste (dyspraxie) : que lui coûte chaque tracé, chaque recopie ?
- un élève anxieux : trouve-t-il une entrée réussissable dans chaque exercice ? sait-il ce qu'on attend de lui ?

Chaque point d'achoppement est un candidat constat. Le confronter ensuite à l'objectif de l'exercice est ce qui fait le tri.

Pour ce qui est **imprimé**, l'image de la page fait foi sur la source : un environnement neutralisé, une option de classe ou une macro peuvent faire apparaître ou disparaître un cadre que la lecture du `.tex` laisse mal deviner.

### 4. Écrire les objectifs, puis les constats

Pour chaque exercice, écris d'abord l'**objectif** et les **critères de réussite** (`objectifs`). C'est le garde-fou de tout le reste : une difficulté qui *est* l'objectif n'est pas un obstacle, et une piste qui la retire dénature l'évaluation. Si l'exercice évalue « traduire une phrase en notation probabiliste », le vocabulaire « parmi » est la compétence elle-même ; s'il évalue « calculer avec un arbre », un mot rare dans l'habillage est un obstacle.

Une fois les objectifs écrits, cherche les **compétences clandestines** (code ST9) : une question qui, pour être réussie, exige une compétence non annoncée ou évaluée dans un autre exercice — traduire « arrive à l'heure » en événement contraire dans un exercice qui évalue la règle des chemins, interpréter une comparaison dans un exercice de calcul. L'élève y échoue pour une raison que la question ne prétend pas mesurer, et si l'enseignant s'est imposé « une compétence par exercice », sa propre règle est rompue. C'est l'une des sources d'obstacles les plus fréquentes et les moins visibles.

Un exercice encore à rédiger (« Question à venir ») figure dans `objectifs` comme non rédigé, sans critères inventés ni constat.

Pour chaque constat :
- **une zone précise** — ce qui permet la capture ; un problème qui se répète (trois « Recopier » dans le sujet) fait **un** constat à plusieurs zones, pas trois, rangé sous « Ensemble du sujet » s'il touche plusieurs exercices ; à l'inverse, deux constats ne surlignent jamais la même zone : chacun cible sa phrase ;
- **l'observation**, factuelle ;
- **le pourquoi**, qui nomme l'élève qui trébuche et le mécanisme, avec la source (`[EX] p. 4`) ;
- **une à trois pistes** applicables, de la plus économe à la plus ambitieuse, avec la reformulation `avant` / `apres` quand elle est textuelle — c'est ce qui fait gagner du temps à l'enseignant ;
- **ce qui est préservé**, et la **vigilance** si la piste ajoute de l'étayage, du temps ou une page ;
- l'**arbitrage** quand une piste heurte une contrainte de l'enseignant : dis le conflit et propose une façon de le trancher, plutôt que de taire la piste ou d'ignorer la contrainte. Exemple : la présentation en colonnes est déconseillée `[EX]`, mais le sujet doit tenir en deux pages — on peut linéariser l'exercice le plus dense et garder les colonnes là où le tableau n'est qu'une donnée.

Calibre-toi sur les cas d'école du référentiel : leur grain (un mot, une colonne déplacée, un rayon tracé en amorce) est le bon. Un sujet ordinaire donne en général de 8 à 20 constats ; moins, c'est que tu n'as pas regardé assez près ; beaucoup plus, c'est que tu as morcelé un même problème.

Sois franc : si le sujet est déjà très accessible sur une dimension, cote « Avancé » et dis pourquoi ; si un point fort est réel, mets-le dans `points_forts` ; si une dimension est faible, ne l'adoucis pas.

Ce que l'évaluation sommative peut porter d'étayage dépend de l'échéance (référentiel, §6 et §7) : signale quand une piste rapproche le sujet d'une évaluation de découverte alors que l'examen approche.

**Présélectionne.** L'enseignant gagne du temps s'il n'a qu'à ajuster un choix déjà fait plutôt qu'à décider de tout. Dans chaque constat, marque **une** piste `"recommandee": true` avec une phrase `pourquoi_recommandee` ; puis décide `"a_retenir"` pour le constat (traiter dans cette version du sujet ou non) et pour chaque action de passation. Le rapport s'ouvre avec ces cases déjà cochées. Pour choisir, pense en enseignant pressé : la piste qui lève l'obstacle au moindre coût, compatible avec ses contraintes et l'échéance. Avant de choisir, lis la section « Retours de l'enseignant » de `.claude/skills/bfcours-latex/references/conception-evaluations-accessibles.md` : elle consigne ce qu'il a déjà retenu ou refusé lors d'audits précédents, et ta présélection doit en tenir compte.

### 5. Compléter la grille et la passation

- `grille` : les neuf dimensions, chacune cotée avec une justification de deux ou trois phrases et les constats qui la fondent. « Non applicable » est une réponse honnête pour un sujet écrit individuel (appartenance, souvent matériel) : dis ce qui en relève autour de l'épreuve.
- `passation` : ce que le référentiel recommande avant, pendant et après (`[VERS]` p. 2-3), **choisi pour ce sujet** (pas la liste entière recopiée) — annoncer les critères, rappeler le matériel autorisé, prévoir un coup de pouce, valider les critères sur la copie…

Écris `constats.json` dans le dossier d'audit avec **Write** (format : `references/schema-constats.md`).

### 6. Capturer, vérifier, générer

```bash
PYTHONIOENCODING=utf-8 python ".claude/skills/audit-accessibilite-eval/scripts/capturer_zones.py" --dossier "<dossier_audit>"
```

S'il sort en erreur, corrige les ancres signalées (une ancre plus courte prise sur une seule ligne, ou un `bloc` de `mise_en_page.json`) et relance ; traite aussi les alertes de zones superposées. Puis **regarde** les aperçus `captures/apercu-page-NN.png` et quelques captures : chaque surlignage doit tomber sur ce que dit le constat. Une capture qui montre la mauvaise ligne ruine la confiance dans tout le rapport.

```bash
PYTHONIOENCODING=utf-8 python ".claude/skills/audit-accessibilite-eval/scripts/generer_rapport.py" --dossier "<dossier_audit>" --ouvrir
```

Le script valide `constats.json` (grille complète, gravités, pistes…) et refuse un fichier incomplet ; traite aussi ses alertes. Le rapport référence les images par chemins relatifs : le dossier d'audit doit rester entier.

### 7. Rendre compte

Dans le chat, en quelques lignes : le chemin du rapport, la **note** (ligne `NOTE` de `generer_rapport.py`, comparée à l'audit précédent s'il existe), le verdict, les trois priorités, et comment s'en servir (cocher, annoter, « Copier le prompt pour l'agent », coller dans Claude Code).

### La note d'accessibilité

`generer_rapport.py` calcule une note, affichée en tête du rapport :
- un **indice de grille** sur 100 : moyenne des dimensions applicables (aucun 0, partiel 1, avancé 2) ;
- le **nombre d'obstacles restants** par gravité.

La note est **maximale** quand l'indice vaut 100 et qu'il ne reste aucun bloquant ni aucun important. Des constats « confort » peuvent subsister. Quand un audit daté précédent existe pour le même sujet, sa note est affichée à côté, ce qui donne l'avant / après.

La note ne vaut que si l'audit est honnête. Ne relève pas une cote et n'abaisse pas une gravité pour atteindre le maximum : un obstacle qui demeure reste un constat. À l'inverse, n'invente pas d'obstacle sur un sujet devenu propre.

## Appliquer les modifications retenues

Quand l'utilisateur colle un prompt intitulé « Appliquer les améliorations d'accessibilité retenues », c'est le retour du rapport. Il contient les fichiers, les objectifs à préserver, les constats cochés avec leurs pistes et les remarques de l'enseignant.

1. Lis le fichier source en entier, puis `constats.json` du dossier d'audit si un détail manque.
2. Applique **seulement** ce qui est coché. La remarque de l'enseignant prime sur la piste ; si elle entre en conflit avec un objectif à préserver, arrête-toi sur ce point et pose la question.
3. Pour un `.tex` bfcours : charge `bfcours-latex` ; garde le corrigé aligné sur l'énoncé modifié ; conserve le barème total ; recompile avec `tex-compiling-skill`, rends les pages en PNG et regarde-les. Pour un `.docx` ou `.odt`, modifie le document avec les outils dont tu disposes.
4. Vérifie les contraintes de l'enseignant (nombre de pages notamment) et signale tout dépassement.
5. Termine par un tableau `identifiant · fait / adapté / non fait · ce qui a changé · raison`.
6. Fais remonter les préférences (ci-dessous).
7. Propose de relancer l'audit sur la nouvelle version : le nouveau dossier daté permet de comparer.

### Boucle jusqu'à la note maximale

Quand l'enseignant demande un sujet « au maximum », enchaîne audit → application → nouvel audit jusqu'à la note maximale (en général deux ou trois tours).

Ses **contraintes sont des limites dures**, pas des préférences :
- le nombre de pages ;
- aucun exercice coupé entre deux pages ;
- les conventions bfcours ;
- la partition des compétences ;
- ses remarques des tours précédents.

Une piste qui en enfreint une est exclue, même si elle ferait monter la note. Cherche alors une autre façon de lever l'obstacle, par exemple un agencement plus compact ou une reformulation plus courte.

Chaque nouvel audit est fait comme le premier, sans indulgence. Si le maximum est inatteignable sans enfreindre une contrainte, arrête la boucle et dis-le clairement : quel constat reste, quelle contrainte l'empêche de tomber, et ce que l'enseignant pourrait assouplir pour le lever.

### Faire remonter les préférences

Les principes d'accessibilité vivent aussi dans `bfcours-latex` (`references/conception-evaluations-accessibles.md`), pour que les évaluations soient écrites accessibles dès le départ. Ce fichier s'améliore avec ce que l'enseignant fait remonter. Les sources de ce signal sont la section « Écarts avec la présélection de l'agent » du prompt, ses remarques générales et ses remarques sur les constats.

Ajoute ou modifie une ligne dans la section « Retours de l'enseignant » de ce fichier **seulement** pour une préférence **durable**. Signes qu'elle l'est :
- une remarque formulée en règle (« jamais de… », « je préfère toujours… ») ;
- le même type d'écart sur plusieurs constats ou plusieurs audits (refus répété de linéariser, préférence constante pour un résultat intermédiaire plutôt qu'une piste…).

Un choix lié à ce seul sujet (« je garde la coupure de page, pas le choix ») ne remonte pas.

Suis le format daté indiqué dans le fichier. Une préférence qui en contredit une ancienne la **remplace**. Si un principe général du fichier s'avère faux à l'usage, corrige-le à sa place plutôt que d'empiler une exception. Dis dans ton compte rendu ce que tu as fait remonter, ou que rien ne le justifiait.
