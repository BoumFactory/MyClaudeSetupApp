# Première utilisation (first_check)

À lire **une seule fois** : quand `premier_usage_fait` vaut `false` dans `config.json` (l'installeur l'y met ; clé absente = poste déjà en service, ne rien faire). Le matériel est déjà réglé par l'installeur ; il ne s'agit ici que de l'utilisateur. Durée visée : deux minutes. Ne jamais bloquer une demande urgente : si l'utilisateur veut sa capsule tout de suite, passer à l'étape 5 avec les valeurs par défaut et proposer les questions plus tard.

## 1. L'installation a-t-elle eu lieu ?

Vérifier, sans rien télécharger :

- `config.json` contient `python_rendu`, `python_pocket`, `python_parakeet` et la clé `mfa`, et ces fichiers existent ;
- `<dossier de base>/outils/bilan-installation.json` existe et vaut `"ok": true` (sinon, lire les briques en échec : chaque ligne donne sa solution).

Si `config.json` est vide, si les chemins n'existent pas, ou s'ils pointent vers un autre poste : **arrêter** et demander à l'utilisateur de lancer l'installeur (`.claude/skills/capsule-video/installation/installer.ps1`, clic droit > « Exécuter avec PowerShell » ; Linux et macOS : `bash installer.sh` ; mode d'emploi : `installation/LISEZMOI.md`). Ne rien installer soi-même.

Une brique facultative absente n'est pas une erreur : sans Whisper (`python_asr` à `null`), les enregistrements du professeur passent par Parakeet (moins bon sur le jargon, efface les « euh »). Le dire seulement si l'utilisateur veut animer son propre enregistrement.

## 2. Proposer le cadrage

Une seule question (outil de question à choix s'il existe, sinon en texte) :

> Bienvenue ! Avant la première capsule, je peux vous poser 6 questions rapides sur vos goûts (thème, taille des formules, rythme…). Tout reste modifiable à tout moment : il suffira de me dire « je préfère… ».
> 1. Oui, posons les questions (recommandé, 2 minutes)
> 2. Non, prends les valeurs par défaut

Si « non » : écrire dans `references/preferences.md` une ligne « Cadrage initial | valeurs par défaut, questions déclinées | <date> » et passer à l'étape 4.

## 3. Les questions

Les poser en **deux salves** de 3 questions au plus, option recommandée (le défaut) en premier, avec une phrase d'explication. Rappeler une fois : « Rien n'est définitif : dites-moi simplement “je préfère…” quand vous voulez. »

| # | Question pour le professeur | Options (défaut en premier) | Où s'applique la réponse |
|---|---|---|---|
| 1 | Quelle ambiance visuelle ? | **Nuit** : fond sombre, couleurs vives (capte l'attention) · Jour : fond clair, sobre (proche d'une fiche) | `theme` de `spec.js`, brief des animateurs |
| 2 | Quelle taille pour les formules ? | **Grandes** : la formule est l'objet principal de l'écran · Compactes : à la taille du texte, plus de contenu visible | clé `formules: 'grandes'` ou `'compactes'` de `spec.js` (aération, écarts et pilule résultat compris ; surchargeable par scène), écrite à la création par `nouvelle_capsule.py --formules <valeur>` (`moteur-canvas.md` § Taille des formules) |
| 3 | Comment la rédaction se construit-elle à l'écran ? | **Une étape à la fois, en grand** (les lignes précédentes s'effacent ou se réduisent) · Rédaction complète visible, qui se construit ligne par ligne | découpage des scènes, brief de l'animateur ; va avec la question 2 (« compactes » convient à la rédaction complète) |
| 4 | Que contient une correction ? | **Rappel de l'énoncé puis correction détaillée de chaque question** · Méthode seule, version courte · Seulement les questions choisies à chaque fois | structure du script |
| 5 | Le pointeur lumineux qui désigne ce dont on parle ? | **Visible jusqu'au geste suivant** · Discret, s'éteint seul après une seconde · Pas de pointeur | gestes `pointe` du `spec.js` |
| 6 | Quelle voix de synthèse ? | **Estelle** (voix française du catalogue, installée) · Votre propre voix, clonée plus tard (`references/cloner-sa-voix.md` : compte Hugging Face gratuit, 20 s d'enregistrement) | `voix_pocket_defaut` de `config.json` ; pour le clone, seulement noter l'intention et donner la marche à suivre |

Questions **non posées** ici, car elles ont un défaut raisonnable et se posent au moment où elles servent (salve de cadrage de `SKILL.md`) : sous-titres (défaut : non), qualité du rendu (720p par défaut, posée dans la salve de cadrage), planche de contrôle avant le rendu (non : seulement sur demande), musique de fond (non), relire le script avant la voix (oui la première fois), comment piloter le skill (l'agent enchaîne les scripts seul ; l'utilisateur ne voit que le résultat).

Ne pas proposer de notation pour le parallélisme : la règle est fixe (`//`).

**Écrire chaque réponse** dans `references/preferences.md`, une ligne par sujet, datée, même quand c'est la valeur par défaut :

```
| Style | thème `nuit` | 21/10/2026 |
| Formules | `formules: 'grandes'` | 21/10/2026 |
```

## 4. Proposer une capsule d'essai

> Voulez-vous une petite capsule d'essai (≈ 30 secondes, 3 minutes de fabrication) pour voir ces réglages en action ? Donnez-moi un exercice court, ou je prends un exemple simple (calcul de la longueur d'un vecteur).

Si oui : suivre `SKILL.md` (voie B : script de 3 ou 4 temps forts, voix Pocket, horodatage, `spec.js`, rendu 720p) dans `capsules/essai-<sujet>/`. Montrer la vidéo, puis demander ce qui ne plaît pas : chaque retour durable va dans `preferences.md`.

## 5. Marquer le premier usage comme fait

Mettre `"premier_usage_fait": true` dans `config.json` (ne toucher à aucune autre clé), même si l'utilisateur a décliné les questions ou la capsule d'essai. Ce fichier ne sera plus relu, sauf si l'utilisateur demande à « refaire le cadrage ».
