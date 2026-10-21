---
name: specs-creator
description: Fabrique, en grande partie seul, un dossier de spécifications prêt à construire (vision, usages anticipés, fonctionnel, technique ou forme, critères d'acceptation, journal des décisions, plan de construction) et un CLAUDE.md qui l'indexe, pour une application, un outil, un site, un paquet ou une ressource (pédagogique ou non) que l'utilisateur veut faire construire. Le modèle enquête, anticipe ce que l'utilisateur fera de sa création, décide seul les points secondaires et ne lui fait trancher que les décisions essentielles, par l'interview de grill-me (manches à choix) ou la carte de wayfinder (grand chantier sur plusieurs sessions), à chaque étape où elles surgissent. Utiliser dès que l'utilisateur veut « écrire les specs », « un cahier des charges », « spécifier », « cadrer » une app ou une ressource, « préparer le terrain avant de coder », « poser les bases d'un projet pour un agent », ou décrit une chose à construire plus tard, même sans prononcer le mot « spec ».
---

# Specs-creator

Le livrable est un **dossier de specs** qu'un agent (ou un humain) peut ouvrir à froid et construire sans revenir poser de questions.

Le partage des rôles est le cœur du skill :

- **Le modèle fait le travail.** Il cherche les faits, imagine les usages, rédige, choisit les valeurs par défaut et vérifie la cohérence.
- **L'utilisateur tranche l'essentiel.** Il ne voit que les décisions qui engagent vraiment sa création, et toujours avec une recommandation argumentée.

Un utilisateur à qui l'on pose trente questions abandonne. À l'inverse, s'il découvre après coup un choix structurant pris dans son dos, il cesse de faire confiance aux specs. Le skill tient entre ces deux écueils.

## Le dossier produit

```
<dossier-specs>/
├── CLAUDE.md                  index : quoi lire, dans quel ordre, pour quelle tâche
├── 00-vision.md               le but, pour qui, ce qui compte vraiment, la définition du « réussi »
├── 01-usages.md               personas et parcours anticipés (première fois, usage courant, cas limites, l'année d'après)
├── 02-fonctionnel.md          app : fonctionnalités et règles · ressource : 02-contenu.md (contenu, déroulé, progression)
├── 03-technique.md            app : architecture, pile, données, déploiement · ressource : 03-forme.md (format, mise en page, supports)
├── 04-criteres-acceptation.md vérifications concrètes, testables une à une
├── 05-decisions.md            journal D-01, D-02… : qui a tranché, pourquoi, ce qui a été écarté
├── 06-perimetre.md            hors périmètre et évolutions envisagées
├── 07-plan-de-construction.md lots ordonnés, chacun vérifiable, avec les fichiers de specs à lire
└── glossaire.md               (facultatif) termes du domaine, dès qu'il en existe d'ambigus
```

Le nombre de fichiers s'adapte à la taille du projet. Une petite ressource peut fusionner 02 et 03, ou se passer de glossaire. Les gabarits de chaque fichier sont dans `references/gabarits.md`. Lis-le avant d'écrire.

Le `CLAUDE.md` est facultatif mais recommandé. Il n'est pas un résumé des specs : il dirige vers le bon fichier, pour que l'agent constructeur charge seulement ce dont sa tâche a besoin. Si l'utilisateur ne veut pas de CLAUDE.md, mets l'index dans un `README.md`.

**Emplacement.** Le dossier se met là où la construction aura lieu : un sous-dossier `specs/` du projet cible s'il existe, sinon le futur dossier du projet (selon les préférences de l'utilisateur). Le nom de dossier ne porte pas d'accents. L'emplacement se décide par défaut et s'annonce en une ligne : le déplacer plus tard ne coûte rien.

## Déroulé

Le premier tour fait deux choses à la fois : il lance l'enquête (étape 1) en arrière-plan et charge grill-me, dont la première question porte sur le mode (terminal ou page HTML). Garde ce mode pour toutes les questions de la session, y compris celles qui surgissent pendant la rédaction.

### 1. Enquêter avant de demander (sans l'utilisateur)

Lis la demande, puis rassemble les faits avec des sous-agents (`Explore` pour le code et les fichiers), en parallèle :

- les projets, applications ou ressources voisines qui existent déjà et que la nouvelle création devrait réutiliser ou dont elle devrait s'inspirer ;
- les skills, agents et outils du poste qui serviront à la construction ;
- les contraintes de l'environnement connues par la mémoire ou les CLAUDE.md (machines des utilisateurs finaux, outils autorisés, préférences de style) ;
- les documents que l'utilisateur a fournis ou cités.

Ne demande jamais à l'utilisateur ce qu'un sous-agent peut vérifier. Pendant que l'enquête tourne, avance sur l'étape 3.

**Aucune question essentielle ne part avant le retour de l'enquête.** Une création voisine déjà existante, une progression déjà fixée ou une contrainte de matériel peuvent changer la question elle-même, ou la rendre inutile. Un essai l'a montré : une forme technique avait été tranchée avant qu'on découvre une application voisine à réutiliser, et il a fallu rouvrir la décision. La question du mode, elle, peut partir tout de suite.

### 2. Choisir le moteur d'interview

| Situation | Moteur |
|---|---|
| Le projet tient dans une session : une app d'un écran à quelques écrans, une ressource, un outil | **grill-me** : appelle l'outil Skill avec `grill-me` |
| Le chantier dépasse une session, ou de grosses inconnues demandent des recherches ou des prototypes avant de pouvoir décider | **wayfinder** : voir « Variante wayfinder » plus bas |

Choisis toi-même et annonce le choix en une ligne. L'utilisateur peut le renverser. En cas de doute, commence avec grill-me : si la frontière ne cesse de s'élargir après deux manches, bascule sur wayfinder et dis-le.

### 3. Projeter les usages (le cœur du travail)

Avant de poser la moindre question, rédige un brouillon de `01-usages.md`. Mets-toi à la place de chaque personne qui touchera la création et déroule sa vie dans le temps : la découverte, le premier usage, l'usage courant, les ratés, le partage, la mise à jour, la réutilisation l'an prochain, ce qu'elle voudra faire *ensuite*. La grille d'anticipation de `references/anticipation.md` recense les dimensions à parcourir. Lis-la à cette étape.

Cette projection fait la différence entre des specs qui décrivent ce qui a été demandé et des specs qui servent vraiment. La plupart des besoins que l'utilisateur n'a pas formulés se trouvent ici : export, impression, usage hors ligne, version élève et version prof, sauvegarde, modification par un collègue.

### 4. Brouillon v0 et tri des décisions

Rédige une v0 rapide de 00 à 03 (dans le scratchpad, ou directement dans le dossier). Chaque point non réglé reçoit une **hypothèse par défaut**. Classe ensuite chaque décision :

**Essentielle** si l'une de ces conditions au moins est vraie :
- **Coûteuse à défaire** une fois la construction lancée : pile technique, modèle de données, format du livrable, public visé.
- **Affaire de valeurs ou de goût**, que seul l'utilisateur peut juger : intention pédagogique, ton, priorités, ce qui compte plus que le reste.
- **Incertaine** : la projection d'usage fait apparaître plusieurs options sensées qui mènent à des créations nettement différentes.
- **Hors des faits** : elle dépend d'une information que seul l'utilisateur détient (budget, calendrier, personnes concernées, cadre institutionnel).

**Secondaire** dans tous les autres cas. Tu la décides seul, avec le statut « par défaut (révisable) » dans `05-decisions.md`.

Un bon dossier compte en général entre 5 et 15 décisions essentielles. Au-delà de 20, tu fais probablement trancher par l'utilisateur ce que tu peux décider toi-même. En dessous de 3, tu as probablement pris dans son dos un choix structurant.

### 5. Faire trancher l'essentiel

Applique la méthode de grill-me (manches, frontière, options concrètes, recommandation en tête) en la restreignant ainsi :

- Seules les **décisions essentielles** deviennent des questions. La recommandation de chaque question est ton hypothèse, et son argument s'appuie sur la projection d'usage (« au conseil de classe, tu voudras… »).
- Les **décisions secondaires** passent en bloc, en fin de manche : une question à choix multiples « Parmi ces choix par défaut, lesquels veux-tu revoir ? », avec une ligne par choix. En mode terminal, regroupe les lignes par thème, 4 options par question ; en mode HTML, un seul bloc `multiple` suffit. Ce que l'utilisateur ne coche pas est accepté. C'est ainsi que specs-creator respecte la règle de grill-me selon laquelle chaque décision est posée explicitement, sans noyer l'utilisateur.
- **Un choix coché** devient une question essentielle de la manche suivante, avec ses options et ta recommandation.
- Montre en priorité les choix par défaut qu'un utilisateur a des chances de contester (visibles par le public, ou qui touchent ses habitudes). Au-delà d'une douzaine de lignes par bloc, regroupe ou remonte d'un cran : « réglages d'affichage par défaut (voir D-14 à D-19) ».
- Chaque réponse s'inscrit aussitôt dans `05-decisions.md` avec le statut « tranché ».
- La clôture de grill-me (récapitulatif et confirmation) est remplacée par l'étape 8 : après la dernière manche, enchaîne sur la rédaction sans récapitulatif intermédiaire.

### 6. Rédiger le dossier

Écris les fichiers définitifs à partir des gabarits. Quelques règles servent l'agent constructeur :

- **Une information n'a qu'un seul emplacement.** Les autres fichiers y renvoient (« voir D-04 », « voir 01-usages, parcours P3 »). Des specs qui se répètent finissent toujours par se contredire.
- **Concret et vérifiable** : « l'élève retrouve sa progression après avoir fermé l'onglet » plutôt que « gestion de la persistance ».
- **Aucun « à définir » caché.** Un point encore ouvert va dans `05-decisions.md` avec le statut « ouvert » et la raison pour laquelle il peut attendre. Il n'apparaît nulle part ailleurs sous forme de trou.
- Le contenu affiché est en français correct, avec les accents. Les noms de fichiers n'en ont pas.

**Les décisions surgissent à toute étape.** En rédigeant, en lisant le résultat d'un sous-agent ou pendant le test de l'étape 7, une nouvelle décision apparaîtra. Applique-lui le tri de l'étape 4 :

- **essentielle** : pose-la tout de suite (une question `AskUserQuestion` ou une petite manche dans le mode choisi) et n'écris pas la partie qui en dépend tant qu'elle n'est pas tranchée. Avance sur les autres fichiers en attendant ;
- **secondaire** : décide, note-la dans le journal, et garde-la pour un bloc de choix par défaut (le prochain, ou celui de la clôture).

Avant de clore, vérifie que chaque décision « par défaut » du journal a été présentée dans un bloc. Une décision oubliée est un choix pris dans le dos de l'utilisateur.

Dans `07-plan-de-construction.md`, chaque critère cité dans « Terminé quand » doit pouvoir se vérifier **à la fin de ce lot**, avec ce que ce lot et les précédents ont livré. Un critère qui suppose un lot ultérieur va dans le lot ultérieur. Les deux essais du skill ont montré que c'est la première source de blocage pour l'agent constructeur.

### 7. Test du constructeur

Lance un sous-agent **neuf**, qui ne reçoit que le chemin du dossier, avec cette mission : « Tu vas construire ce qui est spécifié ici. Lis le CLAUDE.md puis les fichiers qu'il indique. Ne construis rien : liste tout ce qui t'empêcherait de livrer sans poser de question (ambiguïtés, contradictions entre fichiers, informations manquantes, critères invérifiables, lots du plan trop gros pour une session), avec le fichier et la phrase en cause. »

Demande-lui de classer chaque point en **bloquant** (impossible de livrer sans réponse, ou deux fichiers se contredisent) ou **mineur** (un constructeur raisonnable peut trancher seul). Trie ensuite :
- la réponse est déjà dans les specs mais mal placée ou mal formulée : corrige la rédaction ;
- la décision est secondaire : décide par défaut ;
- la décision est essentielle (critères de l'étape 4) : pose la question à l'utilisateur ;
- le point est mineur et se règle au moment de coder : laisse-le au constructeur, mais écris dans le CLAUDE.md la règle qui l'arbitre (souvent « en cas de doute, suivre la priorité n° X de 00-vision »).

**Arrêt** : lance un second passage, toujours avec un sous-agent neuf, seulement si le premier a trouvé des bloquants. Ce second passage ne cherche que les bloquants. S'il en trouve encore, corrige-les sans troisième passage, et signale à la clôture qu'ils ont été corrigés sans être revérifiés.

### 8. Vérification mécanique et clôture

```
PYTHONIOENCODING=utf-8 python ".claude/skills/specs-creator/scripts/verifier_specs.py" "<dossier-specs>"
```

Le script contrôle que les liens du CLAUDE.md pointent vers des fichiers existants, que chaque fichier est indexé, que chaque décision citée (`D-07`) et chaque critère cité (`CA-03`) existent, qu'aucun marqueur de trou (« TODO », « à définir », « TBD », « ??? ») ne traîne hors du journal, et il compte les décisions par statut. Corrige jusqu'à ce qu'il ne signale plus d'erreur. Il ne contrôle que la forme : la cohérence de fond relève de l'étape 7.

Clôture dans le chat, en court :
1. l'emplacement du dossier et une ligne par fichier ;
2. les décisions tranchées par l'utilisateur, une ligne chacune ;
3. les décisions prises par défaut qu'il n'a pas encore vues (normalement aucune), et les décisions restées ouvertes avec la raison ;
4. la suite proposée : le premier lot de `07-plan-de-construction.md` et le skill ou l'agent qui le construira.

Ne lance pas la construction sans que l'utilisateur l'ait demandé : ce skill s'arrête au dossier de specs.

## Variante wayfinder

wayfinder ne s'appelle pas par l'outil Skill (`disable-model-invocation`). Lis donc `.claude/skills/wayfinder/SKILL.md` et `.claude/skills/wayfinder/issue-tracker-local.md`, puis applique leur méthode avec ces réglages :

- **Destination** : le dossier de specs complet, qui passe `verifier_specs.py` et le test du constructeur.
- **La carte vit dans le dossier de specs** : `<dossier-specs>/carte/map.md` et `<dossier-specs>/carte/issues/NN-slug.md`, au lieu de `.scratch/`. Le CLAUDE.md la cite dans une section « Chantier en cours », supprimée quand la carte est terminée.
- **Dès la session de cartographie**, crée le squelette du dossier (CLAUDE.md, 00-vision, 01-usages en brouillon) : la projection d'usage alimente les tickets.
- Un ticket `grilling` suit les étapes 4 et 5 ci-dessus. Un ticket `research` ou `prototype` est confié à un sous-agent (skills `research` et `prototype`).
- **À la résolution d'un ticket**, mets à jour le ou les fichiers de specs concernés et `05-decisions.md`. Le fichier de spec porte la décision, le ticket y renvoie.
- La carte terminée, enchaîne les étapes 6 à 8.

## Exemple

Un dossier produit lors des essais du skill (avec un utilisateur simulé qui prenait les recommandations) montre le niveau de détail attendu : `assets/exemple/activite-vecteurs/`, une ressource, une activité de 2nde à rédiger ensuite en LaTeX bfcours. Commence par son CLAUDE.md.

Pour une application plutôt qu'une ressource, remplace les parties « contenu » et « forme » par « fonctionnel » et « technique » (voir `references/gabarits.md`).
