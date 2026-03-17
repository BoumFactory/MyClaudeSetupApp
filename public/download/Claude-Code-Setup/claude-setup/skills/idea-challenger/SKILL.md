---
name: idea-challenger
description: "Skill de clarification iterative des demandes utilisateur. Ce skill devrait etre utilise quand l'utilisateur formule une demande vague, complexe ou ambigue qui necessite d'etre precisee avant execution. Par une serie courte de questions ciblees et d'analyses iteratives, il transforme une idee brute en prompt .md reutilisable et structure selon les conventions Anthropic."
---

# Idea Challenger - Clarification Iterative de Demandes

Ce skill transforme une demande brute ou vague en un prompt `.md` precis, reutilisable et structure selon les conventions Anthropic, via un processus iteratif de questions/reponses.

## Quand utiliser ce skill

- L'utilisateur formule une demande vague, complexe ou ambigue
- Une demande necessite des choix architecturaux ou pedagogiques non specifies
- L'utilisateur souhaite explicitement clarifier sa pensee avant execution
- Avant de lancer une tache complexe impliquant plusieurs agents/skills

## Workflow complet

### Phase 0 : Reception et analyse initiale

A la reception de la demande principale :

1. **Reformuler** la demande en une phrase claire pour confirmer la comprehension
2. **Identifier** les dimensions a explorer (voir grille d'analyse ci-dessous)
3. **Detecter** les zones d'ombre : tout ce qui est implicite, ambigu ou manquant
4. **Evaluer** le niveau de clarte initial sur une echelle 1-5

#### Grille d'analyse des dimensions

Pour chaque demande, evaluer la clarte sur ces axes :

| Dimension | Question directrice | Exemples de zones d'ombre |
|-----------|-------------------|---------------------------|
| **Objectif** | Quel resultat final concret ? | "Ameliorer" = vague, "creer un cours" = plus clair |
| **Public** | Pour qui exactement ? | Niveau scolaire, profil, prerequis |
| **Perimetre** | Quelles limites ? | Nombre de pages, duree, profondeur |
| **Format** | Quel livrable ? | LaTeX, HTML, presentation, fichier unique/multiple |
| **Contraintes** | Quelles obligations ? | Programme officiel, style, outils imposes |
| **Contexte** | Dans quel cadre ? | Sequence pedagogique, evaluation, revision |
| **Qualite** | Quels criteres de reussite ? | Niveau de difficulte, accessibilite, originalite |

### Phase 1 : Formulation des questions (round N)

**Principes pour les questions** :

- **Maximum 4 questions par round** (ne pas submerger l'utilisateur)
- **Prioriser** : poser d'abord les questions dont les reponses conditionnent les suivantes
- **Proposer des choix** quand c'est possible (plus facile a repondre qu'une question ouverte)
- **Contextualiser** chaque question (expliquer pourquoi elle est importante)
- **Utiliser AskUserQuestion** avec des options concretes pour les questions a choix

#### Format de question optimal

```
[QUESTION N] : [Question claire et directe]
Pourquoi c'est important : [impact de la reponse sur le livrable]
Options suggerees : [A] / [B] / [C] / Autre
```

#### Strategie de priorisation

- **Round 1** : Objectif + Public + Format (les fondamentaux)
- **Round 2** : Perimetre + Contraintes (les limites)
- **Round 3+** : Qualite + Details fins (le raffinement)

### Phase 2 : Analyse des reponses

Apres chaque round de reponses :

1. **Integrer** les reponses dans la comprehension globale
2. **Mettre a jour** la grille de clarte (note par dimension)
3. **Identifier** les nouvelles zones d'ombre revelees par les reponses
4. **Detecter** les contradictions eventuelles entre reponses
5. **Evaluer** si la clarte globale est suffisante (seuil : 4/5 sur chaque dimension pertinente)

#### Criteres de sortie de boucle

La clarification est **terminee** quand :

- Toutes les dimensions pertinentes sont a 4/5 ou plus
- Aucune ambiguite majeure ne subsiste
- Les reponses convergent (pas de nouvelles questions majeures)
- L'utilisateur indique explicitement que c'est suffisant

La clarification **continue** quand :

- Une ou plusieurs dimensions sont sous 3/5
- Les reponses revelent de nouvelles questions importantes
- Une contradiction doit etre resolue
- Le perimetre a evolue et necessite re-evaluation

### Phase 3 : Synthese intermediaire (entre rounds)

Apres chaque round, presenter a l'utilisateur :

```
## Etat de la clarification (Round N)

**Demande reformulee** : [synthese mise a jour de la demande]

**Dimensions clarifiees** :
- [Dimension] : [resume] (clarte: X/5)
- ...

**Points restants a clarifier** : [liste ou "Aucun - pret pour la generation"]
```

### Phase 4 : Generation du prompt final

Une fois la clarification terminee, generer un fichier `.md` dans le repertoire courant de l'utilisateur.

#### Structure du prompt genere

Le prompt genere doit suivre les conventions Anthropic de prompt engineering :

```markdown
# [Titre descriptif de la tache]

## Role

[Role systeme clair et contextualize]

## Contexte

[Contexte complet de la tache : qui, quoi, pourquoi, pour qui]

## Instructions

[Instructions detaillees, etape par etape, en forme imperative]

### Etape 1 : [Titre]
[Description precise]

### Etape 2 : [Titre]
[Description precise]

...

## Contraintes

- [Liste des contraintes explicites]

## Format de sortie

[Description precise du format attendu]

## Exemples (si pertinent)

### Exemple d'entree
[Input]

### Exemple de sortie attendue
[Output]

## Variables

| Variable | Description | Valeur par defaut |
|----------|-------------|-------------------|
| `{{VARIABLE_1}}` | [Description] | [Defaut ou "obligatoire"] |
| `{{VARIABLE_2}}` | [Description] | [Defaut ou "obligatoire"] |
```

#### Regles de generation du prompt

1. **Utiliser des variables** `{{NOM_VARIABLE}}` pour tout element susceptible de changer entre utilisations
2. **Ecrire en forme imperative** (pas de "vous devez", mais "Faire X", "Generer Y")
3. **Etre explicite** : chaque instruction doit etre non-ambigue
4. **Structurer en sections claires** avec une progression logique
5. **Inclure des exemples** si la tache est complexe ou si le format de sortie est precis
6. **Preciser le format de sortie** : type de fichier, structure, longueur attendue
7. **Decrire le role** de maniere contextualisee (pas generique)
8. **Separer instructions et contraintes** : les instructions disent quoi faire, les contraintes disent quoi ne pas faire ou les limites

#### Conventions de variables

- Nommage : `SCREAMING_SNAKE_CASE` entre doubles accolades
- Variables obligatoires : marquees "obligatoire" dans le tableau
- Variables avec defaut : inclure la valeur par defaut
- Regrouper les variables en debut ou fin de prompt dans un tableau recapitulatif

### Phase 5 : Validation finale

Presenter le prompt genere a l'utilisateur avec :

1. **Apercu du prompt** : afficher le contenu complet
2. **Resume des variables** : lister les variables et leur usage
3. **Suggestion d'utilisation** : comment utiliser ce prompt (copier-coller, integrer dans une commande, etc.)
4. **Proposition de nom de fichier** : `prompt-[sujet-court].md`

## Gestion des cas particuliers

### Demande deja claire

Si la demande initiale est suffisamment precise (clarte >= 4/5 sur toutes les dimensions) :
- Le signaler a l'utilisateur
- Proposer de passer directement a la generation du prompt
- Poser 1-2 questions de confirmation rapide maximum

### Utilisateur impatient

Si l'utilisateur veut accelerer ("c'est bon, genere") :
- Completer les zones d'ombre avec des valeurs par defaut raisonnables
- Marquer ces choix comme `[DEFAUT]` dans le prompt genere
- Signaler les hypotheses faites

### Demande trop large

Si la demande couvre trop de terrain pour un seul prompt :
- Proposer un decoupage en sous-prompts
- Generer un prompt "maitre" qui orchestre les sous-prompts
- Chaque sous-prompt suit le meme format

## Bonnes pratiques Anthropic pour prompts

Voir `references/anthropic-prompt-conventions.md` pour les conventions detaillees.

Points cles :
- **Etre direct** : aller droit au but, pas de politesse excessive dans le prompt
- **Montrer plutot que dire** : inclure des exemples concrets
- **Utiliser des delimiteurs XML** si le prompt contient des donnees variables : `<input>`, `<context>`, etc.
- **Structurer avec du Markdown** : titres, listes, tableaux
- **Donner un role precis** : "Tu es un professeur de mathematiques en college" > "Tu es un assistant"
- **Chaine de pensee** : pour les taches complexes, demander de raisonner etape par etape
- **Prefilling** : indiquer le debut de la reponse attendue si le format est precis
