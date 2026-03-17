# Adversarial Optimisation — Review multi-agents de documents pédagogiques

Skill d'optimisation adversariale de documents éducatifs. Orchestre 4 agents critiques + 1 arbitre en débat structuré pour produire la meilleure version possible d'un document de cours, exercice ou évaluation. Fonctionne principalement sur du LaTeX mais le principe s'applique à tout document pédagogique.

## Quand utiliser ce skill

- Optimiser un fichier `.tex` existant pour meilleure lisibilité élève
- Revoir les formulations d'un cours, exercice ou évaluation
- Valider qu'un document est clair, concis et pédagogiquement optimal
- Vérifier la conformité d'un document avec le programme officiel
- Quand la tâche est techniquement difficile et qu'on veut éviter les allers-retours
- Quand on veut explorer des pistes d'amélioration auxquelles on n'a pas pensé
- Intégrable dans la commande `optiLatex` comme étape de review

## Principe

**4 agents critiquent, 1 arbitre tranche.**

Chaque agent lit le document source et produit une critique structurée depuis son angle. L'arbitre synthétise les propositions, résout les conflits, et produit les modifications concrètes.

## Les 5 rôles

| Rôle | Fichier prompt | Focus |
|------|---------------|-------|
| Expert didactique (enseignant) | `agents/expert-didactique.md` | Contenu maths correct, progression cognitive, conformité habitudes |
| Élève-testeur | `agents/eleve-testeur.md` | Compréhension, confusions, charge cognitive, besoins pour réussir |
| Critique éditorial (développeur) | `agents/critique-editorial.md` | Concision, espace, hiérarchie visuelle, amplification des possibilités |
| Inspecteur pédagogique | `agents/inspecteur-pedagogique.md` | Activité mathématique élève, changements de registre, conformité programme |
| Arbitre | `agents/arbitre.md` | Synthèse, résolution des conflits, diff final |

## Workflow

### Phase 1 : Analyse parallèle (4 agents)

Lancer 4 agents en parallèle via `Task()` :

```
Agent 1 : Expert didactique       → critique contenu + didactique
Agent 2 : Élève-testeur           → rapport de confusion + besoins
Agent 3 : Critique éditorial      → audit concision + possibilités techniques
Agent 4 : Inspecteur pédagogique  → conformité programme + registres
```

Chaque agent reçoit :
- Le fichier `.tex` complet (ou la section ciblée)
- Le niveau scolaire cible (6e→Tle)
- Le contexte (cours, exercice, évaluation, fiche)

Chaque agent retourne un JSON structuré :
```json
{
  "role": "nom-du-role",
  "verdict": "acceptable|améliorable|problématique",
  "issues": [
    {
      "location": "ligne ou environnement",
      "severity": "critique|important|mineur",
      "problem": "description du problème",
      "suggestion": "proposition concrète",
      "rationale": "pourquoi c'est mieux"
    }
  ],
  "strengths": ["ce qui est bien et ne doit pas changer"]
}
```

Note : l'élève-testeur ajoute un champ `"besoins"` et l'inspecteur ajoute `"registres_observes"`, `"registres_manquants"` et `"competences_travaillees"`.

### Phase 2 : Arbitrage (1 agent)

L'arbitre reçoit les 4 critiques et :

1. **Identifie les consensus** — points soulevés par ≥2 agents → appliqués directement
2. **Résout les conflits** — quand des agents se contredisent → tranche avec justification
3. **Filtre le bruit** — rejette les suggestions qui ajoutent de la complexité sans gain
4. **Intègre les besoins élève** — transforme les besoins en annexes ou supports complémentaires
5. **Produit le diff** — modifications concrètes (old → new) prêtes à appliquer

### Phase 3 : Application

Appliquer les modifications via `Edit` tool. Proposer un avant/après pour validation user.

Si les besoins de l'élève-testeur ont donné lieu à des annexes, les créer comme fichiers séparés.

## Paramètres

| Variable | Description | Défaut |
|----------|-------------|--------|
| `{{FICHIER}}` | Chemin du fichier .tex à optimiser | obligatoire |
| `{{NIVEAU}}` | Niveau scolaire (6eme, 5eme, ..., Tle) | détecté depuis le contenu |
| `{{TYPE}}` | Type de document (cours, exercice, eval, fiche) | détecté |
| `{{FOCUS}}` | Focus spécifique (formulation, espace, registres, tout) | tout |
| `{{INTENSITE}}` | light (suggestions) / deep (réécriture) | light |

## Intégration avec optiLatex

Dans la commande `optiLatex`, ajouter une étape optionnelle :

```
Étape N : Review adversariale
  → Invoquer adversarial-optimisation sur le .tex généré
  → Appliquer les corrections avant compilation
```

## Contraintes absolues

- **JAMAIS modifier la sémantique mathématique** — les agents optimisent la forme, pas le fond (sauf si le contenu est faux — l'expert didactique le signale en priorité)
- **Respecter les conventions bfcours** — `\acc{}`, `tcbenumerate`, `\voc{}`, etc.
- **Ne pas gonfler** — si une suggestion ajoute du texte, elle doit en retirer ailleurs (sauf annexes élève)
- **Langue parfaite** — accents français obligatoires dans tout output .tex
- **Changements de registre** — l'inspecteur a un droit de veto si le document reste dans un seul registre
