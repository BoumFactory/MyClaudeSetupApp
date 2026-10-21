# Gabarits des fichiers de specs

Chaque gabarit donne la structure attendue. Les phrases entre `<…>` décrivent ce qu'il faut écrire et ne restent jamais dans le fichier final. Supprime une section vide plutôt que d'écrire « néant », sauf si son absence pourrait être prise pour un oubli.

Sommaire : [CLAUDE.md](#claudemd) · [00-vision](#00-visionmd) · [01-usages](#01-usagesmd) · [02-fonctionnel](#02-fonctionnelmd) · [03-technique / 03-forme](#03-techniquemd-ou-03-formemd) · [04-criteres-acceptation](#04-criteres-acceptationmd) · [05-decisions](#05-decisionsmd) · [06-perimetre](#06-perimetremd) · [07-plan-de-construction](#07-plan-de-constructionmd) · [glossaire](#glossairemd)

---

## CLAUDE.md

Un index court (moins de 60 lignes) : on y trouve où lire, pas ce qui est décidé.

```markdown
# <Nom du projet> : specs

<Une phrase : ce qu'on construit et pour qui.>

Statut : <en chantier | prêt à construire | en construction (lot N)>

## Avant toute tâche

Lire `00-vision.md` (2 minutes). Les choix déjà faits sont dans `05-decisions.md` : ne pas les remettre en cause sans l'utilisateur.

## Où trouver quoi

| Tâche | Fichiers à lire |
|---|---|
| Comprendre le besoin | `00-vision.md`, `01-usages.md` |
| Construire un lot | `07-plan-de-construction.md` (le lot), puis les fichiers que ce lot cite |
| Choix technique ou de format | `03-technique.md` (ou `03-forme.md`), `05-decisions.md` |
| Vérifier une livraison | `04-criteres-acceptation.md` |
| Une demande hors du plan | `06-perimetre.md` d'abord |
| Un terme ambigu | `glossaire.md` |

## Règles pour l'agent constructeur

- <3 à 6 règles propres au projet : skills à charger, conventions, ce qu'il ne faut jamais faire.>
- Une nouvelle décision essentielle se pose à l'utilisateur. Une décision secondaire se note dans `05-decisions.md` avec le statut « par défaut ».

<## Chantier en cours : seulement en variante wayfinder, avec le lien vers carte/map.md>
```

---

## 00-vision.md

```markdown
# Vision

## En une phrase
<Ce que c'est, pour qui, pour quoi faire.>

## Le problème
<Ce qui ne va pas aujourd'hui, ou ce qui manque. Concret, situé.>

## Pour qui
<Les publics, du principal au secondaire. Renvoi vers les personas de 01-usages.>

## Ce qui compte le plus
<3 à 5 priorités ORDONNÉES. Elles servent à arbitrer quand deux exigences se contredisent. Ex. : 1. utilisable en classe sans réseau, 2. lisible au vidéoprojecteur, 3. …>

## Réussi, c'est quand…
<2 à 4 signes observables que la création remplit son rôle.>

## Contraintes fixes
<Ce qui ne se discute pas : matériel, calendrier, cadre institutionnel, outils imposés.>
```

---

## 01-usages.md

Le fichier le plus important pour l'anticipation. Voir `anticipation.md` pour la grille.

```markdown
# Usages

## Personas
### <P1 — Nom de rôle>
<Qui, contexte, compétences, matériel, ce qu'il attend, ce qui le ferait renoncer.>

## Parcours
### <U1 — Titre du parcours> (P1)
<Une suite numérotée d'étapes concrètes, du déclencheur au résultat. Les moments délicats sont signalés.>

<Couvrir au moins : la première utilisation, l'usage courant, un cas qui tourne mal, le partage ou la transmission, la reprise plus tard (semaine ou année suivante).>

## Besoins anticipés
<Ce que les parcours révèlent sans que la demande l'ait formulé. Pour chacun : la source (parcours), puis la décision qui en découle (D-xx) ou le renvoi vers 06-perimetre.>
```

---

## 02-fonctionnel.md

Pour une ressource, le fichier s'appelle `02-contenu.md`.

**Variante app :**

```markdown
# Fonctionnel

## Vue d'ensemble
<Les écrans ou modules et comment on passe de l'un à l'autre.>

## F1 — <Fonctionnalité>
- **But** : <le parcours qu'elle sert (U2)>
- **Comportement** : <ce que voit et fait l'utilisateur, étape par étape>
- **Règles** : <calculs, validations, cas limites, messages d'erreur>
- **Critères** : renvoi vers 04 (CA-xx)
```

**Variante ressource :**

```markdown
# Contenu

## Objectifs
<Ce que le public saura faire ensuite. En éducation : capacités du programme officiel visées, prérequis.>

## Déroulé ou structure
<Les parties dans l'ordre, avec pour chacune : contenu, durée ou volume, modalité (individuel, groupe, projeté…).>

## Contenus détaillés
<Par partie : notions, exemples à construire, exercices et leur progression, données à utiliser, points de vigilance.>

## Différenciation et variantes
<Versions (élève / prof, avec / sans corrigé), aides, approfondissements.>
```

---

## 03-technique.md (ou 03-forme.md)

**Variante app (`03-technique.md`) :**

```markdown
# Technique

## Pile
<Langage, framework, bibliothèques, avec la raison (D-xx).>

## Architecture
<Modules et responsabilités. Un schéma texte si utile.>

## Données
<Modèle, format, où elles vivent, sauvegarde, migration.>

## Environnement d'exécution
<Machines cibles, navigateur, hors ligne, installation, performance attendue.>

## Distribution et mise à jour
<Comment l'utilisateur obtient la création, la met à jour, la partage.>

## Sécurité et données personnelles
<Si des données de personnes réelles sont manipulées : ce qui est stocké, où, qui y accède.>
```

**Variante ressource (`03-forme.md`) :**

```markdown
# Forme

## Format et outils
<LaTeX bfcours, Typst, HTML, H5P, diaporama… avec les skills à charger.>

## Mise en page
<Nombre de pages ou d'écrans, colonnes, lisibilité (projection, impression N&B), espaces de réponse.>

## Supports dérivés
<Corrigé, version projetée, version élève, export Moodle…>

## Fichiers livrés
<Arborescence attendue et nommage.>
```

---

## 04-criteres-acceptation.md

```markdown
# Critères d'acceptation

<Chaque critère se vérifie en moins de 5 minutes, par un humain ou un script. Le regrouper par fonctionnalité ou par partie.>

| ID | Critère | Comment vérifier | Lié à |
|---|---|---|---|
| CA-01 | <Observable, sans ambiguïté> | <Action précise, ou commande> | F1, U2 |
```

---

## 05-decisions.md

Le seul endroit où une décision est écrite en entier. Les autres fichiers y renvoient par l'identifiant.

```markdown
# Journal des décisions

Statuts : **tranché** (par l'utilisateur) · **par défaut** (décidé par le modèle, révisable sans discussion) · **ouvert** (peut attendre ; la raison suit sur la même ligne : `**Statut** : ouvert, parce que…`).

## D-01 — <Titre court>
- **Statut** : tranché, le <date>
- **Choix** : <ce qui est retenu>
- **Pourquoi** : <l'argument, souvent tiré d'un parcours d'usage>
- **Écarté** : <les alternatives, et pourquoi en une ligne chacune>
- **Conséquences** : <ce que ce choix impose ailleurs : fichiers, lots>
```

---

## 06-perimetre.md

```markdown
# Périmètre

## Hors périmètre
<Ce qui a été consciemment écarté de cette version, avec la raison. Évite qu'un agent l'ajoute « pour bien faire ».>

## Évolutions envisagées
<Ce qui viendra peut-être plus tard. Pour chacune : ce que l'architecture actuelle doit préserver pour la rendre possible (ou « rien de particulier »).>
```

---

## 07-plan-de-construction.md

```markdown
# Plan de construction

<Des lots ordonnés. Chacun tient dans une session d'agent, produit quelque chose de vérifiable et laisse le projet dans un état utilisable.>

## Lot 1 — <Titre>
- **Livre** : <ce qui existe à la fin du lot>
- **Lire** : <fichiers et sections de specs nécessaires, et seulement eux>
- **Outils** : <skills, agents, scripts à utiliser>
- **Terminé quand** : CA-01, CA-02… (uniquement des critères vérifiables avec ce que ce lot et les précédents ont livré)
- **Dépend de** : <lots précédents, ou rien>
```

---

## glossaire.md

```markdown
# Glossaire

| Terme | Sens dans ce projet | À ne pas confondre avec |
|---|---|---|
```

À créer dès qu'un terme est employé dans deux sens, ou qu'un terme courant prend un sens précis dans le projet. Pour un projet de code qui a déjà un `CONTEXT.md` (skill domain-modeling), renvoyer vers lui au lieu de dupliquer.
