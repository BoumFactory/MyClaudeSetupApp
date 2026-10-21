---
name: resource-to-skill
description: "Transforme n'importe quelle ressource — PDF, vidéo YouTube ou locale, page web, document bureautique, dossier de code, image — en un skill Claude complet et opérationnel : extraction automatique de la matière, rédaction du SKILL.md avec ses références et ses scripts, puis rapport HTML de relecture. Utilise ce skill dès que l'utilisateur fournit une ressource et veut en tirer une capacité réutilisable, même s'il ne dit pas le mot « skill » : « fais-en un skill », « transforme cette vidéo en compétence », « capitalise ce PDF », « j'ai trouvé cette méthode, garde-la », « apprends ça », ou qu'il partage un lien ou un fichier en demandant que Claude sache le refaire plus tard."
---

# Resource to Skill

Une ressource (vidéo, PDF, dépôt, article) contient un savoir-faire noyé dans du
bavardage, des redites et du contexte périmé. Ce skill en extrait la matière,
puis la reforge en skill : **un outil qui fait faire, pas un résumé qui raconte**.

C'est la ligne de partage qui décide de la qualité du résultat. Un résumé
répond à « de quoi parle la ressource ? ». Un skill répond à « comment je fais
la prochaine fois ? ». Si le fichier produit peut se lire agréablement sans
qu'on ait rien à faire ensuite, il a raté sa cible.

## Le parcours

```
ingest.py ──► matière normalisée ──► lecture ──► façonnage ──► écriture ──► rapport HTML
   │                                                              │
   └── méthode absente/faible ──► créer ou améliorer la méthode ──┘
```

Le mode est **automatique** : dérouler jusqu'au rapport sans demander de
validation intermédiaire. L'utilisateur reprend la main sur le rapport final.

---

## 1. Cadrer en une phrase

Avant d'extraire, formuler pour soi : *« Après ce skill, Claude saura faire
_______ »*. Cette phrase pilote tout le reste — c'est elle qui dira quoi garder
et quoi jeter dans la matière extraite.

Si la ressource ne permet pas de compléter la phrase (pur commentaire d'actualité,
opinion sans méthode), le dire franchement à l'utilisateur plutôt que fabriquer
un skill creux. Proposer alors une note de synthèse : c'est ce dont il a besoin.

## 2. Extraire

```bash
PYTHONIOENCODING=utf-8 python "scripts/ingest.py" \
  "<fichier | dossier | URL>" --out ".rts/<slug>"
```

Les chemins `scripts/…` sont relatifs au dossier du skill : les compléter selon le répertoire courant.

Options : `--visual auto|deep|off` (densité d'images, `deep` pour les vidéos où
les écrans défilent vite), `--lang fr` (sous-titres/transcription), `--method`
(forcer une méthode).

La commande imprime un JSON. Trois issues, trois conduites :

| `status` | Ce que ça veut dire | Conduite |
|---|---|---|
| `ok` | Matière extraite dans le workspace | Continuer en 3 |
| `no_method` | Aucune méthode ne couvre ce type de ressource | **Créer** la méthode → `references/extraction-methods.md` |
| `method_failed` | La méthode existe mais casse ou bute | **Réparer / améliorer** la méthode, puis relancer |

Ne jamais contourner une méthode manquante en lisant la ressource à la main :
le prochain PDF du même genre repose le même problème. Créer la méthode coûte
dix minutes et rend le skill plus capable à chaque usage. C'est le point qui
fait la différence entre un outil qui s'use et un outil qui grandit.

Regarder aussi `coverage` dans le JSON. Une dimension `partial` ou `missing`
(par exemple `text: missing` sur un PDF scanné) est un signal, pas un échec :
soit on complète par lecture directe, soit — si la lacune se reproduira — on
améliore la méthode et on met à jour ses `GAPS`.

Le workspace produit :

```
.rts/<slug>/
  manifest.json   couverture, statistiques, avertissements, actions suggérées
  content.md      le texte, structuré, avec ancres (page, timecode)
  assets/         planches contact et images à regarder
  raw/            sous-titres, HTML, métadonnées d'origine
```

## 3. Absorber la matière

Lire `content.md`. Puis, s'il y a des images, **regarder les planches contact
avant les frames** : une planche montre 12 vignettes horodatées d'un coup, et
permet de n'ouvrir en pleine résolution que les 2 ou 3 écrans qui portent
vraiment quelque chose (du code, un schéma, une interface).

Ce détour visuel n'est pas décoratif. Sur une vidéo technique, la bande son dit
« comme vous le voyez ici » : la substance est à l'écran, et un skill écrit à
partir de la seule transcription sera creux exactement là où il devrait être
précis.

Pendant la lecture, trier en trois tas :

- **Le procédé** — étapes, ordre, conditions, valeurs concrètes. C'est le skill.
- **Le pourquoi** — ce qui justifie une étape, les pièges, ce qui arrive quand
  on s'en écarte. C'est ce qui permettra d'adapter au lieu d'appliquer bêtement.
- **Le décor** — anecdotes, promotions, name-dropping, redites. À jeter.

Noter au passage ce que la ressource **ne dit pas** et qui manquera à l'usage.
Ces trous se comblent par une brève recherche ou s'assument explicitement dans
le skill ; ils ne se comblent jamais par invention.

## 4. Façonner

Décider de la forme avant d'écrire : procédural, référence, ou hybride. Les
critères de choix, le découpage en fichiers et la rédaction de la description
sont dans **`references/skill-shaping.md`** — le lire à cette étape, il porte
l'essentiel du métier.

## 5. Écrire

Appliquer les conventions des skills : divulgation progressive, SKILL.md sous
500 lignes, description qui déclenche, `references/` et `scripts/` en second
niveau. Ne pas lancer de boucle d'évaluations (sous-agents, benchmarks) : elle se
propose à la fin, si l'utilisateur la veut.

Écrire le skill dans `.claude/skills/<nom>/`, en français avec les accents
corrects dans tout contenu lu par un humain, et sans accent dans les noms de
fichiers et de dossiers.

Trois réflexes qui font la différence :

**Ce qui est mécanique devient un script.** Si la ressource montre une commande,
une conversion, un gabarit de fichier, l'incarner dans `scripts/` plutôt que le
décrire en prose. Une instruction en prose se re-improvise à chaque exécution,
avec une chance d'erreur à chaque fois ; un script s'exécute.

**Ce qui est réutilisable tel quel devient un asset.** Modèle de document,
fichier de configuration, structure de départ : les déposer dans `assets/`.

**Les exemples viennent de la ressource, pas de l'imagination.** Un skill tiré
d'une vidéo sur les graphes d'agents doit montrer le code de cette vidéo, pas
un pseudo-code générique. La valeur est dans le concret que l'utilisateur est
allé chercher.

Vérifier ensuite la structure : un `SKILL.md` avec son en-tête (`name`,
`description`), et que chaque fichier cité existe.

## 6. Rendre compte

```bash
PYTHONIOENCODING=utf-8 python "scripts/make_report.py" \
  --skill ".claude/skills/<nom>" \
  --extraction ".rts/<slug>" \
  --notes ".rts/<slug>/choix.md"
```

`choix.md` (facultatif mais recommandé) est une note courte écrite avant de
lancer le rapport : forme retenue et pourquoi, ce qui a été écarté, ce qui reste
incertain. C'est ce qui permet à l'utilisateur de contester une décision plutôt
que de découvrir un résultat.

Le rapport s'ouvre dans le navigateur : skill produit, matière extraite, images
agrandissables au clic, liste de points à vérifier.

Puis, en cinq lignes maximum dans la conversation :

- ce que le skill permet de faire désormais ;
- ce qui a été volontairement laissé de côté ;
- ce dont on n'est pas sûr et qui mérite son œil ;
- le chemin du rapport.

Proposer enfin — sans l'imposer — de tester le skill sur un cas réel, ou de
monter une boucle d'évaluations si l'enjeu le justifie.

---

## Pièges qui reviennent

- **La paraphrase déguisée.** Un SKILL.md qui suit le plan de la ressource
  (intro, partie 1, partie 2, conclusion) est un résumé. Un skill suit le plan
  de la **tâche** : quand l'utiliser, quoi faire, dans quel ordre, quoi vérifier.
- **La fidélité aveugle.** Une ressource peut être datée, promotionnelle ou
  simplement inexacte. Garder ce qui tient, signaler ce qui a vieilli, ne pas
  transmettre une erreur par respect pour la source.
- **Le skill fourre-tout.** Une ressource riche donne parfois deux skills
  distincts. Deux skills nets valent mieux qu'un skill qui ne se déclenche
  jamais parce que sa description essaie de couvrir deux domaines.
- **La description écrite en dernier, à la va-vite.** C'est pourtant elle qui
  décide si le skill servira un jour. Voir `references/skill-shaping.md`.

## Fichiers du skill

- `references/skill-shaping.md` — choisir la forme, découper, rédiger la
  description. À lire à l'étape 4, systématiquement.
- `references/extraction-methods.md` — contrat des méthodes, comment en créer
  une, comment en améliorer une. À lire quand `status` vaut `no_method` ou
  `method_failed`, ou quand la couverture est faible.
- `references/troubleshooting.md` — pannes concrètes (yt-dlp, whisper, encodage
  Windows, pip). À consulter au premier échec technique, pas avant.
- `scripts/ingest.py` — routeur d'extraction (`--list` affiche les méthodes,
  leur maturité et leurs lacunes connues).
- `scripts/new_method.py` — crée et enregistre une nouvelle méthode.
- `scripts/make_report.py` — rapport HTML de relecture.
