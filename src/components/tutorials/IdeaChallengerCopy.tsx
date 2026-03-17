'use client'

import { useState } from 'react'
import { Copy, Check } from 'lucide-react'

const SKILL_CONTENT = `# Idea Challenger - Clarification Iterative de Demandes

Ce skill transforme une demande brute ou vague en un prompt .md precis, reutilisable et structure selon les conventions Anthropic, via un processus iteratif de questions/reponses.

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

#### Format de question optimal

[QUESTION N] : [Question claire et directe]
Pourquoi c'est important : [impact de la reponse sur le livrable]
Options suggerees : [A] / [B] / [C] / Autre

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

## Etat de la clarification (Round N)

**Demande reformulee** : [synthese mise a jour de la demande]

**Dimensions clarifiees** :
- [Dimension] : [resume] (clarte: X/5)

**Points restants a clarifier** : [liste ou "Aucun - pret pour la generation"]

### Phase 4 : Generation du prompt final

Une fois la clarification terminee, generer un fichier .md dans le repertoire courant de l'utilisateur.

#### Structure du prompt genere

# [Titre descriptif de la tache]

## Role
[Role specifique, contextualise, oriente tache]

## Contexte
[Contexte complet de la tache : qui, quoi, pourquoi, pour qui]

## Instructions
[Instructions detaillees, etape par etape, en forme imperative]

### Etape 1 : [Titre]
[Description precise]

### Etape 2 : [Titre]
[Description precise]

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
| \`{{VARIABLE_1}}\` | [Description] | [Defaut ou "obligatoire"] |

#### Regles de generation du prompt

1. Utiliser des variables {{NOM_VARIABLE}} pour tout element susceptible de changer
2. Ecrire en forme imperative (pas de "vous devez", mais "Faire X", "Generer Y")
3. Etre explicite : chaque instruction doit etre non-ambigue
4. Structurer en sections claires avec une progression logique
5. Inclure des exemples si la tache est complexe
6. Preciser le format de sortie : type de fichier, structure, longueur attendue
7. Decrire le role de maniere contextualisee (pas generique)
8. Separer instructions et contraintes

### Phase 5 : Validation finale

Presenter le prompt genere a l'utilisateur avec :
1. Apercu du prompt complet
2. Resume des variables et leur usage
3. Suggestion d'utilisation
4. Proposition de nom de fichier : prompt-[sujet-court].md

## Gestion des cas particuliers

### Demande deja claire
Si la demande initiale est suffisamment precise (clarte >= 4/5) :
- Le signaler, proposer de passer directement a la generation
- Poser 1-2 questions de confirmation rapide maximum

### Utilisateur impatient
Si l'utilisateur veut accelerer ("c'est bon, genere") :
- Completer les zones d'ombre avec des valeurs par defaut raisonnables
- Marquer ces choix comme [DEFAUT] dans le prompt genere

### Demande trop large
Si la demande couvre trop de terrain pour un seul prompt :
- Proposer un decoupage en sous-prompts
- Generer un prompt "maitre" qui orchestre les sous-prompts

---

# Conventions de Prompt Engineering Anthropic

Reference des bonnes pratiques pour la generation de prompts reutilisables.

## Principes fondamentaux

### 1. Clarte et specificite
- Ecrire des instructions explicites et non-ambigues
- Eviter les instructions vagues ("fais quelque chose de bien")
- Preferer les instructions actionnables ("Genere une liste de 5 exercices de niveau 4eme sur les fractions")

### 2. Structure du prompt
L'ordre des sections a un impact sur la qualite de la reponse :
1. Role / Persona (contexte systeme)
2. Contexte de la tache
3. Instructions detaillees
4. Contraintes / Regles
5. Format de sortie
6. Exemples (few-shot)
7. Donnees d'entree (variables)

Les informations les plus importantes doivent etre en debut ou en fin de prompt (effet de primaute/recence).

### 3. Assignation de role
Bon : "Tu es un professeur de mathematiques experimente en college (classes de 6eme a 3eme). Tu connais parfaitement les programmes officiels."
Mauvais : "Tu es un assistant utile."
Le role doit etre specifique au domaine, contextualise, et oriente vers la tache.

### 4. Forme imperative
Bon : "Generer 5 exercices progressifs"
Mauvais : "Vous devez generer 5 exercices progressifs"

### 5. Utilisation de variables
Pour les prompts reutilisables, utiliser {{SCREAMING_SNAKE_CASE}} :
"Generer une fiche pour le niveau {{NIVEAU}} sur le theme {{THEME}}."

### 6. Delimiteurs XML pour les donnees
Quand le prompt inclut des donnees variables, utiliser des balises XML :
<texte_source>{{TEXTE}}</texte_source>
Cela evite la confusion entre instructions et donnees.

### 7. Exemples (Few-shot prompting)
Inclure des exemples concrets pour calibrer le format et le niveau de detail.
Minimum 2 exemples si le format de sortie est precis.

### 8. Chaine de pensee (Chain of Thought)
Pour les taches complexes, demander de detailler les etapes :
"Avant de generer la reponse finale, raisonner etape par etape."

### 9. Format de sortie explicite
Toujours specifier le format attendu (type de fichier, structure, longueur).

### 10. Contraintes negatives
Lister explicitement ce qu'il ne faut PAS faire.

## Patterns avances

### Prompt conditionnel
{{#SI NIVEAU == "6eme"}} Utiliser uniquement des nombres entiers. {{/SI}}

### Etapes numerotees avec dependances
Executer dans l'ordre : 1. Analyse → 2. Structuration → 3. Redaction → 4. Verification → 5. Finalisation

### Meta-instructions de qualite
Checklist d'auto-verification avant finalisation :
- [ ] Conforme au programme officiel
- [ ] Progression du simple au complexe
- [ ] Pas d'erreurs mathematiques
- [ ] Adapte au public cible
- [ ] Respecte le format demande`

export function IdeaChallengerCopy() {
  const [userRequest, setUserRequest] = useState('')
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    const full = SKILL_CONTENT + (userRequest ? `\n\n---\n\n# Ma demande\n\n${userRequest}` : '')
    navigator.clipboard.writeText(full).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2500)
    })
  }

  const lines = SKILL_CONTENT.split('\n')
  const preview = lines.slice(0, 12).join('\n') + '\n...'

  return (
    <div className="space-y-3 py-4">
      <div className="text-xs font-semibold text-violet-400">
        SKILL IDEA-CHALLENGER + CONVENTIONS ANTHROPIC ({lines.length} lignes)
      </div>

      {/* Preview */}
      <div className="relative">
        <pre className="bg-black/40 border border-violet-500/30 rounded-t-lg p-4 text-[0.78rem] leading-relaxed overflow-hidden max-h-44 text-gray-300 font-mono">
          {preview}
        </pre>
        <div className="bg-gradient-to-t from-black/60 to-transparent h-12 -mt-12 relative pointer-events-none rounded-b-none" />
      </div>

      {/* Textarea */}
      <div className="bg-black/30 border border-violet-500/30 border-t-0 rounded-b-lg p-3 space-y-2">
        <div className="text-xs text-gray-500">Votre demande (sera ajoutée à la fin du skill) :</div>
        <textarea
          value={userRequest}
          onChange={(e) => setUserRequest(e.target.value)}
          placeholder="Ex : j'aimerais quelque chose de bien pour réviser les fonctions avec mes élèves..."
          className="w-full min-h-[60px] bg-black/30 border border-white/10 rounded-md p-3 text-gray-200 text-sm placeholder-gray-600 resize-y focus:outline-none focus:ring-2 focus:ring-violet-500/50"
        />
      </div>

      {/* Copy button */}
      <button
        onClick={handleCopy}
        className={`w-full flex items-center justify-center gap-2 py-3 rounded-lg font-semibold transition-all text-sm ${
          copied
            ? 'bg-gradient-to-r from-green-600/40 to-emerald-600/40 border border-green-500/50 text-green-200'
            : 'bg-gradient-to-r from-violet-600/40 to-indigo-600/40 border border-violet-500/50 text-violet-100 hover:from-violet-600/50 hover:to-indigo-600/50'
        }`}
      >
        {copied ? (
          <>
            <Check className="w-4 h-4" />
            Copié ! ({(SKILL_CONTENT + (userRequest ? `\n\n---\n\n# Ma demande\n\n${userRequest}` : '')).length} caractères)
          </>
        ) : (
          <>
            <Copy className="w-4 h-4" />
            Copier le tout (skill complet + votre demande)
          </>
        )}
      </button>

      <p className="text-xs text-gray-500 leading-relaxed">
        <strong className="text-emerald-400">Ce que vous copiez :</strong> le skill Idea Challenger complet
        (workflow de clarification en 7 dimensions, 5 phases) + les conventions Anthropic de prompt engineering.
        Votre demande est ajoutée à la fin. L&apos;IA recevra les mêmes instructions qu&apos;un agent Claude Code professionnel.
      </p>
    </div>
  )
}
