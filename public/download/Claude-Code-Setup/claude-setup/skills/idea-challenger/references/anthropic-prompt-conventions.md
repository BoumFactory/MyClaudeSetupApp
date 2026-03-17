# Conventions de Prompt Engineering Anthropic

Reference des bonnes pratiques pour la generation de prompts reutilisables, basee sur la documentation officielle Anthropic.

## Principes fondamentaux

### 1. Clarte et specificite

- Ecrire des instructions explicites et non-ambigues
- Eviter les instructions vagues ("fais quelque chose de bien")
- Preferer les instructions actionnables ("Genere une liste de 5 exercices de niveau 4eme sur les fractions")

### 2. Structure du prompt

L'ordre des sections dans un prompt a un impact sur la qualite de la reponse :

```
1. Role / Persona (contexte systeme)
2. Contexte de la tache
3. Instructions detaillees
4. Contraintes / Regles
5. Format de sortie
6. Exemples (few-shot)
7. Donnees d'entree (variables)
```

Les informations les plus importantes doivent etre en debut ou en fin de prompt (effet de primaute/recence).

### 3. Assignation de role

**Bon** :
```
Tu es un professeur de mathematiques experimente en college (classes de 6eme a 3eme).
Tu connais parfaitement les programmes officiels de l'Education Nationale.
Tu privilegies une approche progressive et bienveillante.
```

**Mauvais** :
```
Tu es un assistant utile.
```

Le role doit etre :
- Specifique au domaine
- Contextualize (niveau, institution, public)
- Oriente vers la tache

### 4. Forme imperative

Ecrire les instructions en forme imperative/infinitive :

**Bon** : "Generer 5 exercices progressifs"
**Mauvais** : "Vous devez generer 5 exercices progressifs"
**Mauvais** : "Il faudrait generer 5 exercices progressifs"

### 5. Utilisation de variables

Pour les prompts reutilisables, utiliser des variables au format `{{VARIABLE}}` :

```markdown
Generer une fiche d'exercices pour le niveau {{NIVEAU}} sur le theme {{THEME}}.
La fiche doit contenir {{NB_EXERCICES}} exercices de difficulte {{DIFFICULTE}}.
```

#### Conventions de nommage des variables

| Convention | Exemple | Usage |
|-----------|---------|-------|
| `SCREAMING_SNAKE_CASE` | `{{NB_EXERCICES}}` | Standard pour les variables |
| Descriptif | `{{THEME_DU_CHAPITRE}}` | Preferer la clarte a la concision |
| Valeur par defaut | `{{NIVEAU:4eme}}` | Notation avec `:` pour les defauts |

### 6. Delimiteurs XML pour les donnees

Quand le prompt inclut des donnees variables ou du contenu a traiter, utiliser des balises XML :

```xml
Analyser le texte suivant et en extraire les competences :

<texte_source>
{{TEXTE}}
</texte_source>

Presenter les competences dans un tableau.
```

Cela evite la confusion entre les instructions et les donnees.

### 7. Exemples (Few-shot prompting)

Inclure des exemples concrets pour calibrer le format et le niveau de detail :

```markdown
## Exemples

### Exemple 1
**Entree** : Theme = "fractions", Niveau = "6eme"
**Sortie** :
Exercice 1 : Colorier 3/4 d'un rectangle.
Exercice 2 : Placer 1/2 sur une droite graduee.

### Exemple 2
**Entree** : Theme = "equations", Niveau = "4eme"
**Sortie** :
Exercice 1 : Resoudre 2x + 3 = 7.
Exercice 2 : Trouver x tel que 5x - 1 = 3x + 5.
```

### 8. Chaine de pensee (Chain of Thought)

Pour les taches de raisonnement complexe, demander explicitement de detailler les etapes :

```markdown
Avant de generer la reponse finale, raisonner etape par etape :
1. Identifier les prerequis necessaires
2. Determiner la progression logique
3. Verifier la coherence avec le programme officiel
4. Generer le contenu final
```

### 9. Format de sortie explicite

Toujours specifier le format attendu :

```markdown
## Format de sortie

Generer un fichier LaTeX utilisant le package bfcours avec :
- Un en-tete \bfTitre{} pour le titre principal
- Des \bfPropriete{} pour chaque propriete mathematique
- Des \bfExercice{} pour les exercices
- Le tout compile sans erreur avec pdflatex
```

### 10. Contraintes negatives

Lister explicitement ce qu'il ne faut PAS faire :

```markdown
## Contraintes

- Ne pas utiliser de notations non vues au programme de {{NIVEAU}}
- Ne pas depasser {{NB_PAGES}} pages
- Ne pas inclure de correction dans le document eleve
- Ne pas simplifier les fractions intermediaires dans les exemples
```

## Patterns avances

### Prompt conditionnel

```markdown
{{#SI NIVEAU == "6eme"}}
Utiliser uniquement des nombres entiers et des fractions simples.
{{/SI}}

{{#SI NIVEAU == "3eme"}}
Introduire les racines carrees et les identites remarquables.
{{/SI}}
```

### Prompt avec etapes numerotees

Pour les workflows complexes, numeroter les etapes et indiquer les dependances :

```markdown
## Instructions

Executer les etapes suivantes dans l'ordre :

1. **Analyse des prerequis** : Identifier les notions necessaires pour {{THEME}}
2. **Structuration** : Organiser le contenu en {{NB_PARTIES}} parties progressives
3. **Redaction** : Rediger chaque partie en respectant le format {{FORMAT}}
4. **Verification** : Relire et verifier la coherence avec le programme de {{NIVEAU}}
5. **Finalisation** : Mettre en forme selon les conventions {{STYLE}}
```

### Meta-instructions pour la qualite

```markdown
## Criteres de qualite

Avant de finaliser, verifier que le contenu :
- [ ] Est conforme au programme officiel de {{NIVEAU}}
- [ ] Respecte la progression annoncee (du simple au complexe)
- [ ] Ne contient pas d'erreurs mathematiques
- [ ] Est adapte au public cible (vocabulaire, niveau de formalisme)
- [ ] Respecte le format de sortie demande
```
