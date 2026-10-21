# Façonner un skill à partir d'une matière brute

À lire à l'étape 4, une fois la ressource absorbée. Ce fichier traite du passage
délicat : on a de la matière, il faut en faire un outil.

## Sommaire

- [Choisir la forme](#choisir-la-forme)
- [Le test du lendemain](#le-test-du-lendemain)
- [Découper en fichiers](#découper-en-fichiers)
- [Rédiger la description](#rédiger-la-description)
- [Ce qu'on jette](#ce-quon-jette)
- [Avant / après](#avant--après)
- [Nommer le skill](#nommer-le-skill)

---

## Choisir la forme

Trois formes, décidées par **ce que l'utilisateur fera** avec le skill, pas par
la nature de la ressource.

**Procédural** — la ressource enseigne une manière de faire reproductible :
tutoriel, méthode, protocole, recette de configuration. Le SKILL.md est une
marche à suivre : conditions d'entrée, étapes ordonnées, points de contrôle,
format de sortie. Les commandes deviennent des scripts.

**Référence** — la ressource est un corpus à consulter : documentation d'API,
programme officiel, catalogue de commandes, glossaire. Le SKILL.md reste court
(quand consulter quoi) et l'essentiel vit dans `references/`, découpé pour que
Claude ne charge que la page utile.

**Hybride** — le cas le plus fréquent en pratique : un procédé court, adossé à
une référence dense. Exemple : une conférence qui expose une méthode (procédural)
en s'appuyant sur une bibliothèque d'une trentaine de primitives (référence).
Le SKILL.md porte le procédé et renvoie à `references/` pour la nomenclature.

Un doute ? Compter les décisions. Si l'utilisateur devra surtout **suivre**, c'est
procédural. S'il devra surtout **chercher**, c'est référence.

## Le test du lendemain

Avant d'écrire, se demander : *dans trois mois, un Claude qui n'a jamais vu la
ressource déclenche ce skill sur une vraie demande — a-t-il tout ce qu'il faut
pour agir, sans revenir à la source ?*

Les manques révélés par ce test sont ceux qu'il faut combler en priorité :
valeurs concrètes, noms exacts, ordre des opérations, conditions d'échec. Ce sont
aussi les choses que la ressource passe souvent sous silence parce qu'elles
« vont de soi » pour son auteur.

Corollaire : ce qu'un Claude compétent sait déjà n'a pas à figurer dans le skill.
Écrire « bien nommer ses variables » ou « penser à tester » dilue le contenu
utile. Ne garder que ce qui est propre à ce domaine et à cette ressource.

## Découper en fichiers

Le SKILL.md est chargé en entier à chaque déclenchement : ce qui n'y est pas
indispensable coûte du contexte à chaque usage. Le reste attend dans `references/`
et n'est lu qu'au besoin.

Ce qui reste dans SKILL.md :
- quand et pourquoi utiliser le skill ;
- le fil de la tâche, de bout en bout ;
- les décisions qui changent le résultat ;
- les pièges qui coûtent cher ;
- les renvois vers les autres fichiers, avec **le moment où les lire**.

Ce qui part en `references/` : nomenclatures, tables, variantes par
environnement, exemples longs, détails d'API. Un fichier par domaine ou par
variante — c'est ce qui permet de ne charger qu'un dixième du corpus. Au-delà de
300 lignes, ajouter un sommaire en tête du fichier.

Ce qui part en `scripts/` : tout ce qui est mécanique, répétitif et vérifiable.
Un script rend l'exécution déterministe et évite de re-improviser vingt lignes
de code à chaque fois.

Ce qui part en `assets/` : gabarits, fichiers de configuration, structures de
départ à copier telles quelles.

Le renvoi doit toujours dire **quand** aller lire : « lire `references/aws.md`
si le déploiement vise AWS » est utile ; « voir aussi `references/aws.md` » ne
l'est pas — le fichier ne sera jamais ouvert au bon moment.

## Rédiger la description

C'est le seul texte toujours présent dans le contexte de Claude, et le seul
critère de déclenchement. Un skill parfait avec une description tiède ne servira
jamais.

Elle doit contenir deux choses : **ce que fait le skill** et **dans quelles
situations le mobiliser** — y compris les formulations où l'utilisateur ne
nomme ni le skill, ni la technique, ni le format.

La tendance naturelle est de sous-déclencher : les skills ne sont pas consultés
alors qu'ils seraient utiles. D'où l'intérêt d'être un peu insistant et de citer
des tournures réelles.

```
❌ Aide à créer des graphes d'agents.

✅ Construit des systèmes multi-agents en graphe d'états (nœuds, arêtes
   conditionnelles, état partagé, points de reprise) plutôt qu'en boucle
   ReAct. Utilise ce skill dès que l'utilisateur parle d'orchestrer plusieurs
   agents, d'un pipeline d'IA à étapes, d'un agent qui « part en boucle » ou
   qui « oublie ce qu'il faisait », même s'il ne prononce jamais le mot graphe.
```

Écrire la description **après** le corps du skill — on sait alors ce qu'il fait
réellement —, mais ne jamais la bâcler pour autant.

**Encadrer la description par des guillemets doubles.** Une description en
français contient presque toujours un « : » (« un skill complet : extraction,
rédaction… »), et un deux-points suivi d'une espace dans une valeur YAML non
quotée casse le frontmatter. Les analyseurs tolérants laissent passer, les
stricts rejettent le skill entier — donc quoter systématiquement, et vérifier
avec `quick_validate.py`.

## Ce qu'on jette

Une transcription de vidéo de dix minutes fait 1 500 mots dont 200 sont utiles.
Sont à écarter sans regret :

- l'accroche, l'appel à l'abonnement, les remerciements aux sponsors ;
- les annonces de plan (« on va voir trois choses ») ;
- les redites d'un point déjà exposé ;
- les jugements sans conséquence pratique (« c'est vraiment puissant ») ;
- les références de version qui seront périmées avant l'usage — sauf si la
  méthode en dépend, auquel cas le dire explicitement.

Est à garder même si ça paraît accessoire : les valeurs numériques, les noms
exacts de paramètres, les avertissements (« si vous ne faites pas ça, ça
plante »), et les raisons. Ce sont eux qui font qu'un skill fonctionne dans un
cas que la ressource n'avait pas prévu.

## Avant / après

**Matière (transcription)**

> Alors ce qu'il faut comprendre c'est que quand vous faites une boucle
> classique, l'agent il repart en arrière, il refait des appels, et à la fin
> vous avez consommé genre 40 000 tokens pour rien. Donc l'idée du graphe c'est
> que chaque nœud fait UNE chose, et vous décidez à l'avance qui appelle qui.

**Résumé (à éviter)**

> Les boucles d'agents sont coûteuses. Le graphe permet de mieux contrôler
> l'exécution en découpant en nœuds spécialisés.

**Skill (à viser)**

> ## Découper en nœuds
>
> Un nœud = une responsabilité et une sortie typée. Le découpage se fait par
> décision, pas par thème : là où la boucle relançait un appel pour « voir si
> ça va mieux », le graphe tranche par une arête conditionnelle.
>
> Signal qu'un nœud est trop gros : il rappelle le même outil deux fois pour
> des raisons différentes. Le scinder.
>
> ```python
> graph.add_node("plan", plan_fn)
> graph.add_conditional_edges("plan", route_fn, {"ok": "execute", "retry": "plan"})
> ```
>
> Sans arête de sortie explicite, la reprise sur erreur relance le graphe
> depuis le début et la facture en tokens repart de zéro.

La différence n'est pas la longueur : c'est qu'on peut agir sur le troisième.

## Nommer le skill

Nom court, en minuscules, avec des tirets, sans accent (les chemins accentués
cassent les scripts Python sous Windows). Nommer par la **capacité**, pas par la
source : `graph-agents` et non `resume-video-gao-dalie`. Le nom du dossier et le
champ `name` du frontmatter doivent coïncider.
