---
name: progression-builder
description: Génère et complète des fiches HTML interactives de progression annuelle de mathématiques (drag & drop, séquences, vacances, commentaires, impression). À utiliser à chaque fois que l'utilisateur veut créer, distribuer ou compléter une progression annuelle pour un niveau donné (CM1 → Terminale), faire une fiche HTML pour ses collègues, bâtir une trame de progression de maths, ou éditer/remplir une fiche existante via une discussion guidée. Le skill s'appuie sur `programmes-officiels` pour récupérer la liste exhaustive et officielle des compétences du niveau.
---

# Skill `progression-builder`

Produire des fiches HTML interactives de **progression annuelle de
mathématiques** (collège + lycée, BO 2026), avec :

- une **colonne gauche** listant TOUTES les compétences officielles du
  niveau cible (et les automatismes), groupées par domaine et
  sous-domaine, draggable,
- une **colonne droite** vide où l'enseignant glisse les compétences pour
  bâtir ses séquences, ajoute des "vacances", des commentaires, des
  séparateurs Exos/RdP, imprime…
- une logique JS auto-portée (pas de dépendance, double-clic = ça marche).

Le JS du gabarit (`assets/reference_v2.html`) est **patché au build** pour :
- appeler `updateInsertionPoints()` au `load` — indispensable pour que
  le drag & drop fonctionne dans les **séquences pré-remplies** (sans
  ce patch, dropper dans une séquence générée par le script ne fait
  rien, faute de zones de dépôt),
- ajouter deux boutons à la barre : **🖨 Imprimer** (Ctrl+P friendly)
  et **💾 Exporter JSON** (sérialise la progression actuelle dans le
  presse-papier — utile pour reprendre une fiche remplie en Mode 2),
- marquer la séquence d'intro avec `data-intro="true"` pour la
  distinguer (exclue de l'export JSON).

Le skill couvre **deux flux** :

1. **Build d'une fiche vierge** pour un niveau, à distribuer aux
   collègues (autonome, à compléter ensuite à la main, à la souris).
2. **Complétion guidée** d'une progression par dialogue avec
   l'enseignant : Claude construit un petit JSON décrivant la
   progression puis un script Python l'injecte dans le HTML — évitant de
   charger 100 KB de HTML dans le contexte de l'agent.

## Quand déclencher ce skill

- L'utilisateur demande de **créer une fiche HTML de progression** pour
  un niveau (CM1, CM2, 6e, 5e, 4e, 3e, 2nde, 1ère, Terminale).
- L'utilisateur veut **distribuer un outil** à des collègues pour qu'ils
  bâtissent eux-mêmes leur progression.
- L'utilisateur veut **bâtir / remplir** une progression : décider des
  séquences, répartir les compétences, placer les vacances.
- L'utilisateur fournit une fiche HTML existante (`Progression_XXX.html`)
  et demande d'y **ajouter, déplacer, renommer** des éléments.
- L'utilisateur évoque "le HTML drag-and-drop de progression" ou "ma
  trame annuelle".

**À ne PAS déclencher pour** : sourcer une compétence (utiliser
`programmes-officiels`) ; rédiger une fiche pédagogique d'une séance
(autre skill / autre type de document).

## Architecture du skill

```
progression-builder/
├── SKILL.md                              # ce fichier
├── assets/
│   ├── reference_v2.html                 # gabarit HTML (CSS + JS) lu par generate_vierge.py
│   └── exemple_progression.json          # exemple de JSON de progression (Mode 2)
├── out/                                  # fiches vierges déjà générées (une par niveau)
├── scripts/
│   ├── _utils.py                         # palette domaines, slugify, escape
│   ├── generate_vierge.py                # niveau → HTML vierge
│   ├── apply_progression.py              # HTML vierge + JSON → HTML rempli (+ stats couverture)
│   └── validate_progression.py           # JSON → rapport d'erreurs/warnings (codes, types, doublons)
├── tests/                                 # suite pytest (~70 tests, < 1 s)
│   ├── conftest.py
│   ├── test_utils.py
│   ├── test_generate_vierge.py
│   ├── test_validate_progression.py
│   └── test_apply_progression.py
└── references/
    ├── format_progression_json.md        # schéma du JSON de progression
    ├── workflow_conversation.md          # déroulé des questions guidées (gère 100+ comp.)
    └── couleurs_par_domaine.md           # palette officielle du skill
```

## Mode 1 — Générer une fiche vierge (à distribuer)

Quand l'utilisateur veut une fiche pour un niveau (vide à droite, prête
à remplir par un collègue) :

```bash
PYTHONIOENCODING=utf-8 python scripts/generate_vierge.py \
    --niveau 5E \
    --output out/progression_5E_vierge.html
```

Niveaux acceptés : `CM1`, `CM2`, `6E`, `5E`, `4E`, `3E`, `2GT`, `1SPE`,
`1ENS`, `1TEC`, `TSPE`, `TCOMP`, `TTEC`.

Ce que fait le script :

- lit `../programmes-officiels/data/json/{NIVEAU}.json` (skill voisin
  `programmes-officiels`, source de vérité du programme officiel),
- charge le squelette `assets/reference_v2.html` (qui contient TOUT le
  CSS et tout le JS interactif),
- reconstruit la colonne gauche **avec toutes les compétences** et **tous
  les automatismes** du niveau cible — **obligation d'exhaustivité** :
  aucune compétence du JSON ne doit être omise,
- vide la colonne droite (sauf une séquence d'intro paramétrée avec le
  lien BO et le PDF source du niveau),
- met à jour le `<title>` et le `<h4>` avec le nom du niveau,
- écrit le HTML autonome final.

**Critère de validation** : `data-code=` apparaît dans le HTML autant de
fois qu'il y a de compétences + d'automatismes dans le JSON. Sinon il y
a un bug d'extraction → ne PAS livrer.

### Complétude par niveau (état 2026-05-21)

Le skill a été enrichi en session 9 : tous les niveaux sont
désormais **complets et exhaustifs**. Volumes embarqués dans les
HTML générés :

| Niveau | Compétences | Automatismes | Total `data-code` (+intro) |
|--------|------------:|-------------:|---------------------------:|
| CM1    | 142 | 0  | 143 |
| CM2    | 129 | 0  | 130 |
| 6E     | 103 | 32 | 136 |
| 5E     | 121 | 47 | 169 |
| 4E     |  74 | 40 | 115 |
| 3E     |  62 | 37 | 100 |
| 2GT    | 209 | 33 | 243 |
| 1SPE   | 165 | 28 | 194 |
| 1ENS   |  42 | 18 |  61 |
| 1TEC   | 158 | 27 | 186 |
| TSPE   | 195 | 30 | 226 |
| TCOMP  | 177 | 27 | 205 |
| TTEC   | 161 | 34 | 196 |

Si un niveau évolue côté skill, relancer
`generate_vierge.py --niveau XXX` pour resynchroniser.

### Regroupement par grand domaine BO (collège)

Depuis 2026-06-16, les fiches **collège** (CM1→3E) ne sont plus groupées
par la taxonomie fine lycée (NB/AL/AN…) mais par les **grands domaines
réels du BO** (en-têtes de section vérifiés sur les PDF source) :

1. Nombres et calculs · 2. Espace et géométrie · 3. Organisation et
gestion de données et probabilités · 4. Proportionnalité, fonctions ·
5. Pensée informatique.

Mécanisme (cycle-aware) dans `_utils.py` : `CODE_TO_MACRO_COLLEGE` +
`SOUS_OVERRIDE_COLLEGE` + `MACRO_ORDER`, consommés par `_v2_to_data` pour
`niveau ∈ COLLEGE_NIVEAUX`. Le **lycée garde** la taxonomie fine
(`DOMAINE_INFO`). Plus aucun libellé « Analyse » au collège ; Statistiques
et Probabilités réunies ; Proportionnalité et Fonctions réunies.

### Itérer sur tous les niveaux d'un coup

```bash
for n in CM1 CM2 6E 5E 4E 3E 2GT 1SPE 1ENS 1TEC TSPE TCOMP TTEC; do
  PYTHONIOENCODING=utf-8 python scripts/generate_vierge.py --niveau "$n" \
    --output "out/progression_${n}_vierge.html"
done
```

## Mode 2 — Compléter une fiche via conversation guidée

L'utilisateur a (ou veut) une fiche pour un niveau et veut **maintenant**
y mettre sa progression. Plutôt que d'éditer 100 KB de HTML, on
construit un petit JSON intermédiaire, puis on l'applique.

### Étape A — clarifier le niveau et générer le vierge si besoin

Si la fiche vierge n'existe pas encore, la générer (voir Mode 1).

### Étape B — mener la conversation

Suivre `references/workflow_conversation.md`. Résumé du déroulé :

1. Combien de séquences, et quels titres ?
2. Où placer les vacances entre les séquences ?
3. Pour chaque séquence : quels sous-domaines / quelles compétences ?
   Présenter les codes du JSON v2 par groupes courts.
4. Commentaires / séparateurs Exos à ajouter ?
5. Sanity-check : X compétences placées / Y du programme.

⚠ **Ne JAMAIS inventer un code de compétence.** Toujours les puiser dans
le JSON `programmes-officiels/data/json/{NIVEAU}.json`. Si Claude
hésite, chercher avec le skill `programmes-officiels`
(`python ../programmes-officiels/scripts/search.py --keyword "…" --niveau 5E`).

### Étape C — sérialiser et appliquer

Écrire le JSON construit (schéma complet dans
`references/format_progression_json.md`) :

```json
{
  "niveau": "5E",
  "conserver_intro": true,
  "elements": [
    { "type": "sequence", "titre": "Séquence 1 — …", "contenu": [
        { "type": "commentaire", "titre": "Période 1", "texte": "…" },
        { "type": "objectif",    "code": "5E-GEO-001" }
    ]},
    { "type": "vacances", "label": "Vacances de la Toussaint" },
    { "type": "sequence", "titre": "Séquence 2 — …", "contenu": [
        { "type": "objectif", "code": "5E-GEO-010" }
    ]}
  ]
}
```

Avant d'appliquer, **valider** le JSON (codes inconnus, doublons, types
invalides) :

```bash
PYTHONIOENCODING=utf-8 python scripts/validate_progression.py \
    --progression out/progression_5E_v1.json
```

Exit code 0 = OK, 1 = erreur(s) bloquante(s), 2 = warnings en mode
`--strict`. Le rapport liste précisément les éléments fautifs.

Puis appliquer :

```bash
PYTHONIOENCODING=utf-8 python scripts/apply_progression.py \
    --html out/progression_5E_vierge.html \
    --progression out/progression_5E_v1.json \
    --output out/progression_5E_v1.html
```

Le script :

- grise automatiquement les compétences placées (impossibles à
  re-glisser à gauche tant qu'on ne les retire pas à droite),
- affiche en fin de run un **récap de couverture par domaine** (placé /
  total, avec barres de progression),
- signale en `[WARN]` tout code absent du leftPanel — typo ou code
  inexistant dans le BO.

Pour désactiver l'affichage des stats : `--no-stats`.

## Mode 3 — Édition directe ponctuelle

Pour 1–3 retouches ciblées sur un HTML déjà rempli (renommer une
séquence, ajouter UNE compétence), travailler avec **Edit** directement
sur le HTML. Patterns à connaître :

- titre de séquence : `<div class="sequence-title" contenteditable="true" oninput="updateExport()">TITRE</div>`
- objectif déposé : `<div class="right-objectif" data-code="CODE" …>TEXTE<span class="close-btn delete-right-objectif">×</span></div>`
- vacances : `<div class="vacances"><div class="ligne"></div><div class="texte" …>LABEL</div>…`
- ajouter un objectif à droite ⇒ **toujours** marquer son miroir gauche
  comme `class="objectif grayed"` et `draggable="false"`.

Au-delà de quelques retouches, repasser par Mode 2 (JSON + script) pour
éviter les erreurs de cohérence.

## Gabarit et fiches vierges

`assets/reference_v2.html` est le **squelette de build** (CSS + JS) lu par
`generate_vierge.py` ; il n'est jamais modifié par le skill. Le dossier
`out/` contient les fiches vierges déjà générées (une par niveau),
directement distribuables.

## Dépendances et données

- **Skill requis** : `programmes-officiels`. Si son arborescence
  change (ex: déplacement du dossier `data/json/`), ajuster la constante
  `DEFAULT_V2_JSON_DIR` dans `scripts/generate_vierge.py`.
- **Python** : aucun package externe (stdlib uniquement). Compatible
  Python 3.10+.
- **Encodage** : tous les fichiers manipulés sont UTF-8. Sur Windows,
  toujours préfixer les invocations Python avec `PYTHONIOENCODING=utf-8`.

## Tests rapides après modification

```bash
# Suite pytest complète (~70 tests, < 1 s) — couvre les 13 niveaux,
# les patches JS, validate_progression et apply_progression.
PYTHONIOENCODING=utf-8 python -m pytest tests/ -q

# Smoke tests manuels :
# 1. Le script de build fonctionne sur plusieurs niveaux
for n in CM1 6E 4E 2GT TSPE; do
  PYTHONIOENCODING=utf-8 python scripts/generate_vierge.py --niveau "$n" --output "out/p_${n}.html"
done

# 2. validate puis apply
PYTHONIOENCODING=utf-8 python scripts/validate_progression.py --progression out/test_progression_5E.json
PYTHONIOENCODING=utf-8 python scripts/apply_progression.py \
    --html out/p_5E.html \
    --progression out/test_progression_5E.json \
    --output out/p_5E_rempli.html
```

Le HTML produit doit s'ouvrir directement dans Chrome/Firefox : drag &
drop fonctionnel, boutons "Tout déplier / replier", "➕ Séquence",
"➕ Vacances", redimensionnement du panneau gauche, impression CSS
(`@media print` cache la colonne gauche).
