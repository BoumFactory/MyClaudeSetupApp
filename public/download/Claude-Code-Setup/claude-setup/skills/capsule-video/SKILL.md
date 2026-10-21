---
name: capsule-video
description: Fabrique une capsule vidéo animée (MP4) de correction d'exercice, d'explication de cours ou de vulgarisation (maths, IA…), à partir d'un enregistrement du professeur OU d'un texte rédigé par Claude et lu par une voix de synthèse française locale. Chaque geste visuel est calé sur un mot prononcé (nombres qui volent du tableau vers la formule, lignes qui s'allument, résultats qui tombent en place). La capsule est décrite dans un seul fichier de données (spec.js : scènes, cartes, formules TeX, figures géométriques, tableaux, gestes, scènes 3D three.js) ; le moteur canvas fait la mise en page sans débordement possible, dessine et encode la vidéo dans Chromium en quelques secondes, sur tout PC Windows (carte graphique, puce intégrée ou processeur seul). 100 % local et gratuit. Accompagne l'utilisateur dans ses choix (voix, style, contenu) et retient ses préférences. C'est le skill par défaut pour TOUTE nouvelle capsule : l'utiliser dès que l'utilisateur veut une capsule, une vidéo de correction ou d'explication, un tuto animé, « mettre en images » un audio (.m4a, .mp3, .wav), transformer un corrigé ou un support en vidéo commentée, ou générer une voix off pour un exercice — même sans prononcer le mot « capsule ». Pour reprendre une capsule existante qui contient un scenes.js (moteur HTML), utiliser capsule-video-html.
---

# Capsule vidéo animée (moteur canvas)

La voix est la colonne vertébrale : chaque geste est ancré sur un **mot prononcé**, jamais sur un minutage tapé à la main. L'écran montre ce que la voix désigne, à l'instant où elle le désigne.

Trois temps : **voix** (enregistrée ou synthétisée) → **animation** décrite dans un `spec.js` → **rendu** dans Chromium (canvas + H.264, ≈ 10 s pour 2 min) et montage ffmpeg. Puis l'utilisateur **dirige** (relecture horodatée) et le skill retient ses goûts.

**Chemin par défaut** : script → voix → calage des mots (indispensable aux ancres) → `spec.js` → rendu MP4 → livraison. Ni planche, ni revue image par image, ni contrôle de fidélité séparé, ni page de contrôle : l'agent est assez sûr de lui. Ces vérifications ne se lancent que si l'utilisateur les demande ou signale un défaut (§ Vérifications à la demande). Les erreurs bloquantes des outils (compilation de `spec.js`, débordement, ancre introuvable) sont toujours traitées.

Skill jumeau : `capsule-video-html` (chaque scène est une page HTML/CSS filmée, ≈ 5 fois plus lent). Mêmes voix, mêmes ancres, mêmes gestes : une capsule à `scenes.js` se reprend avec lui ; tout ce qu'il fait, le canvas le fait aussi (portages validés dans `assets/exemples/`).

## Outillage

Tous les chemins sont dans `config.json` (rempli par `installation/installer.ps1` chez un nouvel utilisateur ; fichier facultatif, une clé indispensable absente donne un message clair). `$PY` = la valeur `python_rendu` ; lancer depuis la racine du projet, `PYTHONIOENCODING=utf-8` devant.

**Point d'entrée court** (pour l'utilisateur qui veut lancer lui-même, ou un collègue hors Claude Code) : `capsule.py` à la racine du skill, depuis n'importe quel dossier. `<capsule>` = chemin ou nom dans `dossier_capsules`. Options complètes : `--help` de chaque commande.

```bash
$PY .claude/skills/capsule-video/capsule.py nouvelle <capsule> [--audio f] [--formules grandes|compactes]   # nouvelle_capsule.py
$PY .claude/skills/capsule-video/capsule.py relire <capsule> [--appliquer]     # relire_script.py (rigueur + forme orale)
$PY .claude/skills/capsule-video/capsule.py voix <capsule> [--voix X | --piper] [--modifies]   # voix_pocket.py (Piper en secours)
$PY .claude/skills/capsule-video/capsule.py caler <capsule> [--vocab "…"]      # transcrire.py (MFA)
$PY .claude/skills/capsule-video/capsule.py planche <capsule> [--images …]     # À LA DEMANDE : défaut = milieu de chaque temps fort
$PY .claude/skills/capsule-video/capsule.py rendu <capsule> [--qualite …] [--brouillon --debut X --fin Y]
$PY .claude/skills/capsule-video/capsule.py tout <capsule> [--rendu] [--planche]   # relire → voix → caler (→ rendu ; planche seulement avec --planche)
```

Scripts directs (Claude, réglages fins) :

```bash
S=.claude/skills/capsule-video/scripts
$PY $S/voix_pocket.py "<capsule>" [--seulement b07,b12 | --modifies] [--modele french_24l|french]   # voie B, VOIX PAR DÉFAUT : Pocket TTS, une voix par temps fort ([estelle], [ma-voix]…) ; contrôle de fidélité À LA DEMANDE (--controle, ou controle_fidelite_auto dans config.json)
$PY $S/controle_fidelite.py --capsule "<capsule>"                # À LA DEMANDE : recontrôle les voix déjà produites, sans resynthèse (data/controle-fidelite.json)
$PY $S/voix.py "<capsule>" [--voix-piper siwis|tom|upmc] [--modifies]   # voie B, voix de SECOURS (Piper, instantané) : mêmes sorties
$PY $S/nouvelle_capsule.py "<capsule>" ["<audio>"] --titre "..." [--formules grandes|compactes]   # moteur-canvas/, index.html (aperçu), spec.js, audio (facultatif en voie B)
$PY $S/transcrire.py "<capsule>/audio.xxx" "<capsule>" [--vocab "notations, mots rares"] [--asr whisper|parakeet]   # mots horodatés : MFA sur le texte connu (voie B) ou transcrit (voie A)
$PY $S/mots.py "<capsule>"                                 # mots horodatés : la référence d'ancrage
$PY $S/rendre_canvas.py "<capsule>" --images 12,40.5,63    # À LA DEMANDE : planche, PNG dans planches/, sans vidéo (2-3 s)
$PY $S/rendre_canvas.py "<capsule>" [--qualite 540|envoi|projection] [--finition auto|aucune|x264] [--allegees 370,220] [--fenetre] [--gpu auto]
$PY $S/maj_moteur.py "<capsule>" [...]                     # recopie le moteur à jour dans des capsules existantes
$PY $S/musique.py "<capsule>" [--bpm 104 --niveau -21 --graine 3]  # musique de fond générée + audio-mix.wav
$PY $S/relire_script.py "<capsule ou fournée>"             # rigueur des scripts (references/rigueur.md), AVANT toute voix
$PY $S/fournee_voix.py "<fournee>" [--prefixes F1,F2]      # fournée : relecture + voix + capsule + alignement en lot
$PY $S/file_rendus.py "<fournee>" --qualite 540            # fournée : rend chaque capsule marquée PRET-RENDU, une à la fois
```

- **Suivre un rendu** : `--fenetre` (Windows) ouvre le rendu dans une console visible de l'utilisateur (grand pourcentage, barre, vitesse, temps restant) ; elle se ferme 60 s après la fin.
- **N'importe quel PC Windows** : `--gpu auto` (défaut) essaie Vulkan (carte dédiée), puis Direct3D 11 (puce intégrée), puis le rendu logiciel (avertissement, plus lent). Le nombre de workers s'adapte aux cœurs et à la mémoire libre (pointe ≈ 0,6 Go). La première ligne du rendu dit le mode et la carte utilisés.
- **Musique de fond** (sur demande) : `musique.py` compose une boucle procédurale (aucun échantillon externe, déterministe), effacée sous la voix et qui respire dans les silences ; batterie coupée et tic par seconde pendant chaque silence ≥ 4 s (compte à rebours d'un défi). Il écrit `audio-mix.wav` au même minutage que `audio.wav` (`audio: 'audio-mix.wav'` dans `spec.js`). ≈ 18 dB sous la voix parlée. À relancer après chaque `voix.py`.

- **Chaîne audio sur processeur** (depuis le 20/10/2026) : contrôle de fidélité (à la demande) par **Parakeet** (ONNX, ≈ 0,5 s par temps fort, arbitre Whisper sur les seuls temps forts signalés), horodatage par **MFA** (alignement forcé du texte connu, ≈ 20 ms de précision, aucun mot interpolé), **Whisper** seulement pour transcrire un enregistrement du prof (carte graphique si disponible). Les modèles de contrôle sont chargés une fois par génération. Rôle, poids, installation, pièges, clés de `config.json` : `references/outils-audio.md`.
- **Nettoyer l'audio du prof** (blancs, « euh », reprises ; `nettoyer_audio.py`) : `references/nettoyage-audio.md`.
- **Voix mixtes prof enregistré + voix de synthèse (Pocket `[estelle]`, `[ma-voix]`… ou Piper `[tom]`)** (`assembler_voix.py`, badge « Voix de synthèse » seulement pendant la synthèse) : `references/voix-mixtes.md`.
- **Cloner une voix (Pocket TTS)** : `references/cloner-sa-voix.md` (accès Hugging Face, échantillon, déclaration dans `config.json`). Le clone est **PERSONNEL** : `voix_clonees` de `config.json` et l'échantillon ne se partagent jamais avec le skill (vider `voix_clonees` avant de le donner ; l'installeur écrit un `config.json` neuf, sans voix clonée).
- **Tutoriel logiciel : code qui s'écrit, terminal, geste `compile`** (plugin `installer_blocs.py`) : `references/bloc-code.md`, exemple `assets/exemples/blocs-demo/`.
- **Animations 3D three.js (fond plein écran ou élément `scene3d`, géométrie dans l'espace, frise voyageuse)** (plugin `installer_trois.py`) : `references/trois-d.md`. Le rendu passe seul en 720p avec finition x264 (aplats et lueurs 3D pixellisés en 540p).

**Fichiers de travail** : tout essai (extraits, planches-contacts, rendus d'essai nommés `essai-*.mp4`, jamais `capsule*.mp4`) se fait dans le dossier de la capsule, jamais dans un dossier temporaire ; après validation de la vidéo, supprimer `planches/`, extraits, essais et `*.bak.js` (détail : `CLAUDE.md` du dossier des capsules).

**Première utilisation** : si `premier_usage_fait` vaut `false` dans `config.json`, lire et suivre `references/first_check.md` avant tout (installation vérifiée, préférences, capsule d'essai).

Nouvel utilisateur sans outillage : lui faire lancer `installation/installer.ps1` (voir `installation/LISEZMOI.md`). L'installeur prépare un dossier de base (`<base>/.claude/skills/capsule-video/`, `CLAUDE.md` et `AGENTS.md`, `outils/` pour tout le lourd, `capsules/`), écrit `config.json` et essaie chaque brique ; relancé, il complète sans rien refaire. Le moteur embarque MathJax, GSAP et les polices : seuls Chromium (Playwright) et ffmpeg servent au rendu.

**Matériel requis** : un PC Windows (Linux et macOS : `installation/installer.sh`, non testé), processeur seul suffisant pour toute la chaîne (voix Pocket, contrôle Parakeet, horodatage MFA, rendu). Une carte NVIDIA n'accélère que Whisper (transcription des enregistrements du prof, arbitre du contrôle). Sans MFA ni Parakeet, le skill retombe sur Whisper (ancienne chaîne, plus lente).

## Accompagner les choix

Le skill guide sans interroger : **une seule salve de questions au cadrage** (outil AskUserQuestion, 4 questions au plus, option recommandée en premier), uniquement pour ce qui n'est pas déjà dans `references/preferences.md` ni dans la demande. Après réponse, **écrire les choix durables dans `references/preferences.md`** : la fois suivante, on ne redemande pas, on annonce (« voix siwis, thème jour, 540p comme d'habitude »).

| Moment | Choix | Options (défaut en gras) |
|---|---|---|
| Cadrage | Où ranger la capsule | **`<dossier_capsules de config.json>/<nom-court-sans-accents>/`** |
| Cadrage | Source de la voix | **A. enregistrement du professeur** s'il fournit un audio · **B. texte rédigé par Claude + voix de synthèse** sinon |
| Cadrage (B) | Voix | **Pocket TTS** : la voix par défaut de `config.json` (`voix_pocket_defaut` : un clone si l'utilisateur en a un, sinon `estelle`), une autre voix par temps fort si demandé (`[estelle]`…) · secours : Piper siwis (femme), tom ou upmc (hommes), si Pocket n'est pas installé. |
| Cadrage | Contenu | **rappel de l'énoncé + correction détaillée de chaque question** · questions choisies · version courte « méthode seule » |
| Cadrage | Style | **nuit** (sombre, vif) · jour (clair) · composants bfcours (`methode`, `encadrer`, `etape`) ; sous-titres : **non** · oui (accessibilité) ; taille des formules : clé `formules` de `spec.js`, **grandes** (une étape par écran) · compactes (rédaction complète visible) (`moteur-canvas.md` § Taille des formules) |
| **Revue du document** (avant le script) | Démarche plus simple, ou point de rigueur absent du document | voir ci-dessous : question à choix **par point relevé** |
| Après le script (B) | Relire le texte avant la voix ? | **montrer le script en une page** si c'est une première fois, sinon enchaîner |
| Avant le rendu | Planche ? | **aucune** : on rend directement ; planche seulement si l'utilisateur la demande ou signale un défaut |
| Rendu | Qualité | **720p** (`config.json` : `qualite_rendu: "envoi"`) · 540p (`--qualite 540`) ou 1080p (`--qualite projection`) sur demande ; versions allégées (`--allegees`) sur demande |
| Après le rendu | Diriger | relecture dans `index.html` (« Commenter », « Copier pour Claude ») |

## Rigueur : la capsule est une copie modèle

**Lire `references/rigueur.md` avant d'écrire tout script de correction ou d'explication.** Les élèves recopient l'écran et révisent avec : chaque calcul est une chaîne d'égalités dite « égale » (calculs annexes dans un encart Brouillon), chaque phrase a le bon objet et le bon verbe (« les coordonnées du vecteur », « prouver qu'un quadrilatère est… »), chaque conclusion nomme ses objets, aucune étape n'est sautée. Avant toute synthèse de voix : `$PY $S/relire_script.py "<capsule ou fournée>"` doit finir sans alerte (`fournee_voix.py` le lance et s'arrête sinon). Tout retour du professeur sur une formulation est généralisé : règle abstraite ajoutée à `rigueur.md`, motif ajouté à `relire_script.py`, recherche sur TOUTE la fournée (scripts et `spec.js`).

## Revue critique du document source (toute vidéo qui explique un document)

Avant d'écrire le script (voie B) ou le storyboard (voie A), relire le document **en enseignant exigeant, puis en inspecteur** : la vidéo sera vue sans le professeur, elle doit être mathématiquement impeccable.

1. **Démarche plus simple ?** Pour chaque démonstration ou correction, chercher une démarche plus courte ou plus naturelle avec les outils du niveau. S'il y en a une : **AskUserQuestion** avec `1. Démarche plus simple (recommandé)` · `2. Garder celle du document` · `3. Présenter les deux`.
2. **Rigueur que le document laisse à l'oral** : vocabulaire précis non écrit dans le cours (droites *perpendiculaires* mais vecteurs *orthogonaux* ; norme / longueur ; égalité / équivalence), hypothèses implicites (repère orthonormé), cas particuliers passés sous silence. La vidéo le DIT. Si le bon choix n'est pas évident : question à choix à l'utilisateur, option recommandée en premier.
3. **Lecture orale des écritures** : chaque fraction, parenthèse, carré, racine, opposé doit être lu sans ambiguïté (« 0 plus 2, le tout divisé par 2 ») ; règles dans `references/voix-synthese.md` § Rigueur orale.
4. Noter les points relevés et les choix faits en tête de `script.md` (section « Choix didactiques »).

## Voie A — l'enregistrement du professeur

1. `nouvelle_capsule.py` puis `transcrire.py` avec `--vocab` (notations de la source, sans mots hors sujet) : Whisper transcrit, MFA refait le temps de chaque mot sur ce texte. **Lire toute la transcription.**
2. **L'audio fait foi** : s'il traite un autre exercice que la source fournie, animer l'audio et le dire.
3. Remettre deux listes : **erreurs de reconnaissance** (« tableau 6 contre » = croisé) et **lapsus** (« 150 sur 200 » pour 250). L'écran affiche toujours le juste (et `corrections` corrige les sous-titres). Les points de la revue critique deviennent des suggestions au professeur (l'audio n'est pas réécrit).
4. Données non dites mais nécessaires : les reconstituer par le calcul et le signaler.
5. `storyboard.md` : temps forts, plage de mots `#a–#b`, dit, montré, gestes. Ancres `'#147'`, `'#147.fin+0.2'`. Exemple : `assets/exemples/tableau-croise-canvas/`.

## Voie B — texte rédigé, voix de synthèse (« script d'abord »)

Lire `references/voix-synthese.md` (écriture pour l'oreille, rigueur orale, prononciation, rythme des calculs). En bref :
1. Écrire `<capsule>/script.md` : temps forts `## b01 [pause s]` (voix par défaut) ou `## b01 [estelle] [pause s]` (voix choisie : catalogue Pocket ou alias de voix clonée), écrits pour l'oreille, nombres en chiffres, **un calcul intermédiaire par phrase** (`[lent 1.15]` ne vaut que pour Piper).
2. `voix_pocket.py` (un essai par temps fort, sans contrôle ; mots mal dits corrigés par `prononciation.json` ; avec `--controle` : Parakeet, arbitre Whisper, jusqu'à 3 essais, bilan dans `data/fidelite-voix.json` ; Piper en secours : `voix.py`) → `nouvelle_capsule.py "<capsule>" "<capsule>/audio.wav"` → `transcrire.py` (MFA pose le texte dit de chaque temps fort sur sa voix, puis les **mots exacts du script** y sont recollés ; la fin affiche les mots « interpolés » : 0 attendu avec MFA).
3. Le script EST le storyboard : y ajouter seulement les visuels et les gestes. Ancres `'@b10'`, `'@b10.fin'`, `'@b10~"240"'` : elles se résolvent sur les mots du script, et le même `spec.js` sert pour plusieurs voix. Exemple : `assets/exemples/exo5-canvas/`.
4. Afficher « Voix de synthèse » en permanence (`mention: 'Voix de synthèse'`).

## Construire, rendre, diriger (les deux voies)

- **Construire** : écrire `spec.js` en suivant **`references/moteur-canvas.md`** (gabarits de mise en page, éléments typés, figures en primitives, `\cssId` pour viser un nombre dans une formule, échappatoires JS) et **`references/gestes.md`** (catalogue des gestes et des ancres). Lire aussi `references/design.md` (principes, mises en page, recettes dont **« dérouler puis compacter » un calcul**). Exemples validés : `assets/exemples/labomaths-canvas/` (figure géométrique), `tableau-croise-canvas/` (voie A), `exo5-canvas/` (voie B).
- **Tuiles algébriques** (relatifs, calcul littéral) : éléments `tuiles`, `produit`, `tapis` et gestes `deplace`, `retourne`, `annule`, `ajoutePaire` ; voir les § Tuiles de `moteur-canvas.md` et `gestes.md`, exemple `assets/exemples/tuiles-canvas/`.
- **Déléguer pour le coût** : Claude principal fait la revue critique et écrit le script ; un sous-agent **Sonnet** écrit `spec.js` avec : le script, les chemins du skill, un exemple et les exigences de l'utilisateur. Il ne fait pas de planche.
- **Erreurs bloquantes** : le rendu refuse une capsule en erreur (mot introuvable, id inconnu ou en double, formule fausse, débordement) : les corriger, rien d'autre à contrôler. Les avertissements de zone réduite (en dessous de 85 %) se traitent si le moteur les signale.
- **Rendre** : `rendre_canvas.py` → **`capsule-540p.mp4`** (le standard, ≈ 2,2 Mo/min) ; `--qualite envoi` → `capsule-envoi.mp4` (720p) ; `--qualite projection` → `capsule.mp4` (1080p) ; `--allegees 370,220` ajoute des versions très légères. Mesuré le 09/10/2026 à froid (RTX 3060) : 2 min 05 en ≈ 9 s, 3 min 50 en 16 s ; puce Intel seule ≈ 1,2 fois plus lent, sans carte graphique ≈ 1,4 fois. Le résumé final détaille préparation, dessin, encodage, assemblage et mémoire de pointe. **Un seul rendu à la fois.**
- **Diriger** : donner le MP4 et `index.html` (Espace = lecture, C = commenter, « Copier pour Claude »). Appliquer les retours (§ suivant) ; inscrire les leçons générales dans `references/retours.md`.

### Vérifications à la demande

Seulement si l'utilisateur les demande ou signale que quelque chose ne convient pas ; alors on cible la scène ou le temps fort signalé, jamais toute la capsule.

```bash
$PY $S/rendre_canvas.py "<capsule>" --images t1,t2     # planche (ou capsule.py planche) ; Claude regarde les images : chevauchements, trous de plus de 3 s, gestes en retard, tracés persistants (oubli de `jusque`)
$PY $S/voix_pocket.py "<capsule>" --seulement b07 --controle   # resynthèse contrôlée (Parakeet + arbitre Whisper) d'un temps fort mal dit
$PY $S/controle_fidelite.py --capsule "<capsule>"      # recontrôle des voix déjà produites
$PY .claude/skills/capsule-video/capsule.py rendu <capsule> --brouillon --debut X --fin Y   # extrait MP4, images extraites au temps signalé
```

Page `controle-capsules.html` (fournée) : seulement sur demande, exemple `<dossier_capsules>/Exercices-vecteurs-corriges/controle-capsules.html`.

## Fournée : plusieurs capsules d'un coup (série de corrections, fiche entière)

Chaîne en flux tendu : aucune étape n'attend que toute la fournée ait fini l'étape précédente.

1. **Un dossier par capsule** dans un dossier de fournée : `<fournee>/F1-E3-<nom-court>/` (fiche, exercice). Claude principal fait la revue critique et écrit TOUS les `script.md` (section « Choix didactiques » en tête : elle n'est jamais lue, seuls les `## b01` le sont).
2. **Voix en lot**, en arrière-plan : `$PY $S/fournee_voix.py "<fournee>" [--prefixes F2,F3] [--titre "Fiche {fiche} - Exercice {exo}"]` (saute les capsules déjà préparées).
3. **Brief commun** : copier `references/brief-fournee-modele.md` en `<fournee>/BRIEF-animation.md` et le remplir (exigences, sources, modèle d'habillage). La mission de chaque animateur se réduit alors à : lire le brief + chemin de la capsule + source + visuels clés propres à l'exercice.
4. **Animateurs en parallèle** (sous-agents Sonnet, 3 à 4 à la fois) : chacun écrit `spec.js` (sans planche), traite les erreurs bloquantes du moteur, puis pose le fichier vide `PRET-RENDU` dans sa capsule. Dès la première capsule validée, la donner en **modèle d'habillage** aux suivantes (série homogène).
5. **File de rendus** lancée tôt, en arrière-plan : `$PY $S/file_rendus.py "<fournee>" --qualite 540 [--total N]`. Elle rend une capsule à la fois dès qu'un `PRET-RENDU` apparaît, journalise dans `<fournee>/rendus.log`, s'arrête quand tout est rendu ou si `<fournee>/STOP-RENDUS` existe. Ne jamais lancer `rendre_canvas.py` (sans `--images`) à côté.
6. Livraison : les MP4 rendus et leur dossier. Pas de revue des planches ni de page de contrôle, sauf demande de l'utilisateur (alors : § Vérifications à la demande, ciblées sur la capsule signalée).

## Modifier une capsule existante (réutiliser au maximum)

Ne jamais repartir de zéro : le script, `spec.js`, le moteur et les réglages se réutilisent ; on ne refait que ce qui a changé.

Raccourci pour un lot de capsules : `$PY $S/reprise.py <capsule> [...]` fait les étapes 0 à 2 (sauvegarde `version-N/`, retrait des vidéos et de `PRET-RENDU`, `relire_script.py`, `voix.py --modifies`, `transcrire.py`) ; reste l'étape 3 (animateur) puis `PRET-RENDU`.

0. **Sauvegarder d'abord** : copier `script.md`, `spec.js` et `data/temps-forts.json` dans `<capsule>/version-N/` AVANT toute modification.
1. **Texte** : modifier `script.md` (garder les ids des temps forts inchangés ; insérer `b12a` plutôt que renuméroter). Puis `voix.py --modifies` : seuls les temps forts modifiés sont resynthétisés ; l'assemblage et les bornes sont refaits.
2. `transcrire.py` (les bornes ont bougé), puis `musique.py` (même minutage).
3. **Animation** : les ancres `@bXX~"mot"` suivent la voix automatiquement. Le moteur signale chaque ancre dont le mot a disparu du script : ne retoucher que ces gestes et les scènes dont le contenu change. Déléguer à un sous-agent Sonnet en lui donnant la **liste des temps forts modifiés** et les retours, avec consigne de modifier, pas de réécrire.
4. Moteur : si `assets/moteur-canvas/` a évolué, `maj_moteur.py "<capsule>"`.
5. `rendre_canvas.py` (planche seulement si l'utilisateur la demande).

Une capsule à `scenes.js` (ancien moteur) se modifie avec `capsule-video-html`, ou se porte en `spec.js` geste pour geste (exemples de portage : les trois dossiers `assets/exemples/`).

## Règles du moteur

- Tout mouvement est une fonction du temps (gestes GSAP ou `C.surSeek`) : pas de `setTimeout`, de `Date` ni de `Math.random` (`C.hasard(graine)`). Même spec → mêmes images.
- `id` uniques dans toute la capsule, y compris ceux de `\cssId` : un doublon est une erreur bloquante.
- Taille des formules par la clé `formules` (capsule, scène ou carte), jamais par `tailleTex` / `taille` en dur sur une carte de calcul ; en `grandes`, l'avertissement « formules réduites de plus de 20 % » impose de couper la scène.
- Erreurs bloquantes ajoutées le 20/10/2026 : `jusque` qui ne suit pas le début de son geste ; `$` dans une étiquette de figure (déjà du TeX). Parallélisme : `\para` / `\parallel` affichent « // ».
- Chromium n'est lancé que par Playwright (profil temporaire, `browser.close()`). Ne jamais tuer de processus Chrome par nom.
