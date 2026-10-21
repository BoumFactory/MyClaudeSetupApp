# Journal des retours (étape « diriger »)

Chaque relecture de l'utilisateur produit des leçons. N'inscrire ici que ce qui vaut pour les **prochaines** capsules (goûts, règles de mise en page, pièges), daté, en une ou deux lignes. Les corrections propres à une seule capsule restent dans cette capsule.

## 02/10/2026 — première capsule (centre de loisirs, tableau croisé)

- Goût affirmé : **visuel vif et captivant**, couleurs libres (pas la palette bfcours par défaut), nombres qui « tombent au bon endroit », animations généreuses. Les éléments bfcours (`methode`, `encadrer`, `etape`, `.acc`) ne s'utilisent que sur demande.
- L'audio fourni ne correspondait pas à l'énoncé fourni : toujours vérifier, animer l'audio, le signaler.
- Lapsus oraux (« 150 sur 200 », « 42 » pour 0,42) : l'écran affiche le juste, on signale la liste à l'utilisateur.
- Première mise en page trop petite (30 % de l'écran vide en bas) : remplir la hauteur, données à 60 px et plus.
- Lignes de calcul `P(M∩B) = …` : prévoir 730 px de large et `white-space: nowrap`, sinon débordement.

## 03/10/2026 — série « Vecteurs » (3 épisodes de révision, voix siwis, thème jour, musique générée)

- Voix : « y » lu « i », « A » haché → règles de prononciation dans `voix.py` (§ Prononciation de `voix-synthese.md`).
- Calculs trop rapides pour un élève qui révise : un calcul par phrase, `[lent]`, pauses après chaque résultat ; affichage « dérouler puis compacter ».
- Lecture orale ambiguë des fractions (« 0 + 2 sur 2 ») : tableau § Rigueur orale. Vocabulaire laissé à l'oral par le cours (perpendiculaires / orthogonaux) : la vidéo le dit.
- Démarche du document plus longue que nécessaire (nature d'un quadrilatère par les diagonales) : revue critique du document + question à choix avant le script (`SKILL.md`).
- Propriété « coordonnée par coordonnée » montrée sur un segment horizontal : utiliser une figure générique (segment oblique, droites qui glissent sur chaque axe).
- Débordements de cadre dans quelques calculs longs, vus seulement sur la vidéo finale : le moteur HTML les bloquait par `controle.py` ; le moteur canvas les rend impossibles (texte réduit pour tenir).
- Le 720p suffit la plupart du temps : rendu direct en 720p par défaut.

## 03/10/2026 — fournée de 23 corrections (Vecteurs 2nde, 540p, Moodle)

- « Rigueur nécessaire » : les élèves révisent le contrôle avec. Les animateurs relisent aussi le script contre la source et ont trouvé un oubli (équivalence du cours énoncée sans « éventuellement aplati ») : leur demander de SIGNALER les écarts, Claude principal corrige le script puis `voix.py --modifies`.
- Défauts qu'aucun contrôle automatique ne voit, relevés seulement sur la planche : puce restée en place qui en recouvre d'autres pendant plusieurs questions ; état intermédiaire faux pendant une transformation (« 5,199… » lu pendant l'arrondi de 5,099… à 5,1). Règles ajoutées au brief : jamais de recouvrement, effacer avant d'écrire.
- Lenteur jugée excessive quand les rendus attendaient la fin de toutes les animations : flux tendu (fichier `PRET-RENDU` + `file_rendus.py`), 4 animateurs en parallèle. Rendu ≈ 2,3 × la durée seul, ≈ 4 × quand les animateurs tournent à côté.

## 20/10/2026 — essai Pocket TTS (tuto bfcours-typst, frise 3D)

- Voix de synthèse : Pocket TTS `french_24l`, voix `peter_yearsley` : aucun mot changé après contrôle Whisper, mais débit jugé trop rapide. Quelle que soit la voix, le débit doit rester posé (au moins celui de Piper ralenti à 1,1).
- Prononciations relevées : § « Prononciation (Pocket TTS) » de `voix-synthese.md`. Y verser chaque nouvelle trouvaille.

## 20/10/2026 — tuto « Fabriquer ses capsules animées » v2 (1080p, 3 voix Pocket, thèmes alternés, 4 vues 3D)

- **Thème par scène** : le moteur n'a qu'un thème par capsule. Un plugin propre à la capsule (`themes.js`, non fourni) (clé `theme: 'jour'` sur une scène, fond en fondu 1 s au changement de scène, `\jcyan{…}` dans les formules d'une scène claire, `C.couleurTheme('jour', 'cyan')` pour les gestes) : chargé AVANT le plugin trois. Une bascule de thème se fait donc à un changement de scène, ancré sur le mot (« clair »). Candidat à intégrer dans `assets/plugins-canvas/`.
- **3D en thème clair** : pas de lueur additive ni d'émission (`o.mat` est fait pour la nuit) ; `MeshStandardMaterial` mat, lumière ambiante forte, arêtes sombres (`#141a33`). Fond 3D derrière des cartes en verre : garder le sujet à droite (`setViewOffset`, objets ≤ 3 unités) sinon il traverse les cartes ; tunnel de cadres : estomper le fond (`opacity` selon `z`) pour que le titre reste lisible.
- **Un résultat n'a pas le temps de rester** quand la voix finit sur le dernier geste (chaîne de Pythagore, fraction) : allonger la pause du temps fort (`[pause 3.2]`), puis `voix_pocket.py --assembler-seulement` (6 s, aucune resynthèse) et `transcrire.py`.
- **Un `pulse` sur une carte réduite** la fait dépasser son cadre un instant : ne pas « pulser » l'élément qui démontre que rien ne déborde.
- **Temps réels de la voix** (36 temps forts, 307,7 s d'audio, clone + `estelle` + `peter_yearsley`) : synthèse 470 s pour 380 s d'audio produit (47 essais, ratio 1,24), mais **1 923 s de bout en bout** : les trois manches de contrôle Whisper ont dominé. `transcrire.py` : 940 s la première fois, 96 s la seconde (carte graphique libre). Prévoir 30 min de voix pour 5 min de capsule (ancienne chaîne ; voir l'entrée suivante).
- Les zéros barrés d'Atkinson reviennent dans les dessins faits main (`dessin`, `C.ajouter`) : y écrire les nombres en `"Segoe UI"`.

## 20/10/2026 — chaîne audio sur processeur (contrôle Parakeet, horodatage MFA)

- Le temps de voix venait des contrôles Whisper rechargés à chaque manche : contrôle par Parakeet (24,5 s pour les 36 temps forts du tuto), modèles chargés une fois par génération, horodatage MFA (74 s, 0 mot interpolé). La synthèse Pocket domine désormais : ≈ 10 min de voix pour 5 min de capsule. Détail : `outils-audio.md`.
- Avec MFA, plus de recalage à la main sur les silences de `voix/bXX.wav` : ancrer directement sur le mot. Les ancres-mots se décalent en moyenne de +0,09 s par rapport à Whisper (qui était en avance) : un `-0.1` posé à l'œil pour compenser devient une anticipation, sans gravité.

## 20/10/2026 — fusion des apports d'un collègue (rd)

- Intégrés (crédit : rd) : réglage `formules: 'grandes' | 'compactes'` (taille des formules, aération, écarts, gabarit figure-panneau ; clé absente = rendu inchangé), garde `jusque`, étiquettes de figure tournées (`rotation`), `capsule.py` (point d'entrée court), relecture de la forme orale des notations (`maths_parlees.py` : proposition, jamais traduction silencieuse), `config.json` facultatif, audio facultatif à la création. Parallélisme toujours « // » (`\para`).
- Leçon de l'essai : la taille des formules vient de la spec, pas du moteur ; un `ecart: [x, 0]` sur un calcul colle le « = » aux membres.
