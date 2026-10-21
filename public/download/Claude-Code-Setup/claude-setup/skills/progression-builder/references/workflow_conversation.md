# Workflow : compléter une progression via conversation guidée

Ce document décrit la séquence de questions à poser à l'enseignant pour
construire **incrémentalement** un fichier `progression.json` puis
l'appliquer à un HTML vierge avec `apply_progression.py`.

L'objectif : ne **jamais** charger un HTML de ~100 KB dans le contexte
des agents. On manipule uniquement le JSON intermédiaire (quelques KB) et
on appelle le script de transformation à la fin.

⚠ Les programmes officiels sont **volumineux** (5E = 110 compétences,
2GT = 209, TSPE = 195, TTEC = 161). Une conversation linéaire qui
demanderait "où placer la compétence X ?" pour chaque code épuiserait
l'enseignant. Le workflow ci-dessous s'organise donc **par bloc**
(sous-domaine), pas compétence par compétence.

## Phase 0 — préparer le terrain

Avant la conversation :

1. **Vérifier le niveau cible.** S'il y a doute, demander explicitement
   *« Quel niveau ? (CM1, CM2, 6E, 5E, 4E, 3E, 2GT, 1SPE, 1ENS, 1TEC,
   TSPE, TCOMP, TTEC) »*.
2. **Générer le vierge** s'il n'existe pas déjà :
   ```bash
   python scripts/generate_vierge.py --niveau XXX --output out/progression_XXX_vierge.html
   ```
3. **Charger les codes disponibles** pour ce niveau en lisant
   `../programmes-officiels/data/json/{NIVEAU}.json` (relatif au dossier du skill `progression-builder`).
   On y trouve `competences_by_theme` (domaine → sous-domaine → liste de
   compétences) et `automatismes`. **Ne jamais inventer un code** — si un
   thème souhaité n'est pas dans le JSON, le signaler à l'utilisateur.
4. **Compter** : afficher à l'enseignant le volume du niveau choisi.
   *« Ce niveau a N compétences réparties en X domaines et Y
   sous-domaines, plus Z automatismes. »* Ça calibre les attentes.

## Phase 1 — cadrer la progression (squelette d'abord)

Poser **dans cet ordre** :

1. **Nombre et nom des séquences.** Suggérer une base : *« Typiquement
   6 à 9 séquences sur l'année »*. Proposer des titres-types adaptés au
   niveau (ex. en 5e : *« 1 – Symétrie centrale et constructions »*, *« 2 –
   Fractions et proportionnalité »*, etc.). Toujours laisser l'enseignant
   ajuster.
2. **Calendrier (vacances).** Position des coupures vacances entre les
   séquences. Format libre (Toussaint, Noël, Hiver, Printemps).
3. **Périodes.** Optionnel : un commentaire en tête de séquence pour
   marquer les dates ("du 1er septembre au 17 octobre"). Si l'enseignant
   veut, créer un item `{ "type": "commentaire", "titre": "Période 1",
   "texte": "…" }`.

À la fin de cette phase, on a un **squelette** : N séquences nommées,
M vacances, mais vides à droite. Pratique pour visualiser avant de
remplir.

## Phase 2 — répartir les sous-domaines aux séquences

C'est ici que le workflow change pour gérer la masse :

### Étape 2a — vue d'ensemble des sous-domaines

Présenter à l'enseignant la **liste des sous-domaines** du niveau (pas
les 100 codes), groupée par domaine. Exemple pour 5E :

```
🔢 Nombres et calculs (27 comp.)
  ├─ Ensembles de nombres (8)
  ├─ Calculs et opérations (12)
  └─ Fractions et proportionnalité (7)
🔷 Géométrie (42 comp.)
  ├─ Symétries (14)
  ├─ Triangles et parallélogrammes (15)
  └─ Configurations (13)
…
```

Demander : *« Pour chaque sous-domaine, dans quelle séquence le placer ?
On peut découper si nécessaire. Tu peux me répondre par lignes du type
'Symétries → S1, Triangles → S2 et S3'. »*

### Étape 2b — confirmer la répartition

Proposer à l'enseignant un **tableau récapitulatif** (texte) :

```
S1 — Démarrage             : Symétries (14)
S2 — Triangles             : Triangles et parallélogrammes (15)
S3 — Fractions             : Fractions et proportionnalité (7) + Ensembles de nombres (8)
…
```

Vérifier que **tous les sous-domaines sont placés** (ou explicitement
mis de côté). Sinon, lister ceux qui restent.

### Étape 2c — affiner si besoin

Si l'enseignant veut **éclater un sous-domaine** sur plusieurs
séquences (cas fréquent), proposer une découpe par compétences :
*« Symétries (14 compétences) → présente-moi les codes dans l'ordre du
BO et tu me dis le point de coupure. »*

Lister alors les codes du sous-domaine en **groupes de 5 max**, avec
intitulé court, pour qu'il puisse pointer.

## Phase 3 — éléments décoratifs et automatismes

Une fois les compétences réparties par séquence, demander en bloc :

1. **Commentaires de séquence** : *« Veux-tu ajouter un commentaire en
   tête d'une ou plusieurs séquences (lien Eduscol, ressource,
   intentions pédagogiques) ? »*
2. **Séparateurs Exos / RdP / Auto🛠** : *« Dans quelles séquences
   matérialiser une phase d'exercices / résolution de problèmes /
   automatismes par un séparateur ? »*
3. **Automatismes du niveau** (codes `🅰{NIV}🛠N`) :
   - *« Veux-tu en intégrer dans la progression (placés dans une
     séquence où ils seront travaillés) ou les laisser à gauche
     disponibles tout au long de l'année ? »*
   - Si placés : proposer un mapping par lots ("automatismes 1–10 en
     S1, 11–20 en S2…") pour éviter le code-à-code.

## Phase 4 — sanity-check

Avant de générer :

- Lister les séquences créées avec le nombre de compétences par
  séquence (et par domaine si pertinent).
- Compter les compétences placées vs. restantes :
  *« X compétences sur Y du programme ne sont pas placées (par domaine :
  AL=2, GEO=0, NB=5…). Souhaitez-vous en ajouter ? »*
- **L'exhaustivité n'est pas obligatoire** : l'enseignant peut
  délibérément en omettre. Mais signaler clairement.

## Phase 5 — sérialiser, valider, appliquer

1. Sérialiser le JSON construit dans `out/progression_{NIVEAU}_{slug}.json`.
2. **Valider** avant d'appliquer (capture les codes inconnus, doublons,
   types invalides) :
   ```bash
   python scripts/validate_progression.py \
     --progression out/progression_{NIVEAU}_{slug}.json
   ```
   Si exit code != 0, corriger le JSON avant de continuer.
3. Appliquer :
   ```bash
   python scripts/apply_progression.py \
     --html out/progression_{NIVEAU}_vierge.html \
     --progression out/progression_{NIVEAU}_{slug}.json \
     --output out/progression_{NIVEAU}_{slug}.html
   ```
   Le script affiche en fin de run un récap de couverture par domaine
   (placé/total + barres) — le partager avec l'enseignant.
4. Le HTML rempli est autonome : il peut être ouvert directement dans
   un navigateur. Donner le chemin à l'utilisateur.

## Mode édition directe (alternative)

Si l'utilisateur préfère une retouche ponctuelle sur un HTML déjà rempli
(*« renomme la séquence 3 »*, *« ajoute la compétence 5E-GEO-007 à la
séquence 2 »*), travailler **directement avec Edit** sur le HTML :

- Le pattern d'une séquence est stable :
  `<div class="sequence open"…><div class="sequence-header">…<div class="sequence-title" …>TITRE</div>…`
- Le pattern d'un objectif déposé est :
  `<div class="right-objectif" data-code="CODE" title="…" style="background-color: …" draggable="true">TEXTE<span class="close-btn delete-right-objectif">×</span></div>`
- Quand on ajoute un objectif via Edit, **toujours** marquer le miroir
  côté leftPanel comme `class="objectif grayed"` et `draggable="false"`.
- Quand on retire un objectif, faire l'inverse.

Cette voie est plus risquée (édition manuelle d'un fichier de ~100 KB),
elle est recommandée seulement pour 1–3 modifications ciblées. Au-delà,
préférer reconstruire un `progression.json` et passer par
`apply_progression.py`.

## Astuces pratiques pour la conversation

- **Ne jamais lister plus de ~5 compétences par message** sauf demande
  explicite ("liste-moi tout le sous-domaine"). Sinon l'enseignant lit
  en diagonale et fait des erreurs de placement.
- **Toujours afficher le code** à côté de l'intitulé : c'est la clé que
  Claude utilisera pour le JSON. Format `5E-GEO-007 — Construction d'un
  triangle connaissant…`.
- Si l'enseignant dit *« mets tout ce sous-domaine en S2 »*, exécuter
  ce raccourci au lieu de demander code par code. Le confirmer ensuite
  par un récap court.
- Pour les **gros niveaux (2GT, TSPE)**, ne pas hésiter à itérer en
  plusieurs séances. Sauvegarder le JSON intermédiaire après chaque
  phase pour pouvoir reprendre.
