---
name: make-blueprint-eval
description: Skill pour générer un blueprint (exosquelette pédagogique) d'une évaluation au format HTML. Le blueprint est une page web interactive avec onglets destinée aux étudiants pour réviser. Il présente la structure de l'évaluation, les compétences évaluées, des questions de compréhension du cours, et fléche les exercices types de la fiche. Le skill analyse la séquence globale (cours + exercices) pour proposer un parcours de révision intelligent. Utiliser ce skill après la création complète d'un sujet d'évaluation.
---

# Blueprint d'évaluation - Format HTML interactif

Ce skill génère un **blueprint** (fiche de préparation interactive) au format HTML avec onglets pour aider les étudiants à réviser efficacement avant une évaluation.

## Qu'est-ce qu'un blueprint ?

Un blueprint est une **page HTML autonome** qui tient sur **une page imprimable** et qui contient :

1. **La structure de l'évaluation** : types d'exercices, barème, durée
2. **Les compétences évaluées** : savoirs et savoir-faire attendus
3. **Les questions de compréhension du cours** : pour vérifier la maîtrise des notions clés
4. **Les exercices types fléchés** : références précises aux exercices de la fiche
5. **Les conseils de révision** : parcours optimisé basé sur l'analyse de la séquence

## Prérequis

Avant d'utiliser ce skill, disposer de :
- Le sujet d'évaluation complet (`enonce.tex` ou équivalent)
- Le corrigé de l'évaluation (ou une synthèse de ses compétences et de son barème)
- **Le dossier de séquence complet** contenant :
  - Le cours du chapitre
  - La fiche d'exercices
  - Les activités (si disponibles)

## Protocole de génération

### ÉTAPE 1 : Analyse de la séquence globale

1. **Lire le cours du chapitre** :
   - Extraire les définitions importantes
   - Identifier les propriétés/théorèmes clés
   - Repérer les méthodes de calcul essentielles
   - Noter les exemples types du cours

2. **Analyser la fiche d'exercices** :
   - Lister tous les exercices avec leur numéro
   - Classifier par notion/compétence
   - Évaluer le niveau de difficulté de chaque exercice

3. **Analyser le sujet d'évaluation** :
   - Identifier la structure (exercices, QCM, parties)
   - Extraire le barème
   - Lister les compétences évaluées par exercice
   - Noter la durée et les conditions (calculatrice, etc.)

### ÉTAPE 2 : Construction du mapping intelligent

1. **Créer la correspondance cours → évaluation** :
   - Pour chaque partie du cours, identifier si elle est évaluée
   - Marquer les sections prioritaires vs secondaires

2. **Créer la correspondance exercices → évaluation** :
   - Pour chaque compétence du contrôle, trouver 2-3 exercices équivalents
   - Privilégier les exercices de difficulté similaire
   - Indiquer les questions spécifiques si l'exercice est long

3. **Générer les questions de compréhension** :
   - Formuler 5-8 questions courtes sur le cours
   - Couvrir les définitions, propriétés et méthodes clés
   - Les réponses doivent être vérifiables rapidement

### ÉTAPE 3 : Génération du blueprint HTML

Copier `assets/blueprint-template.html` (gabarit complet : CSS, onglets, impression A4, script `showTab`) vers `blueprint.html`, puis remplacer les `[crochets]` et remplir les cinq onglets (contenu détaillé à l'étape 4). Le gabarit contient :

- un en-tête (titre du chapitre, durée, barème, calculatrice) ;
- cinq onglets : `structure`, `competences`, `questions`, `exercices`, `conseils` ;
- des styles de priorité (`priorite-haute`, `priorite-moyenne`, `priorite-basse`) ;
- une feuille `@media print` qui déplie tous les onglets pour l'impression.

### ÉTAPE 4 : Contenu détaillé des onglets

#### Onglet "Structure"

Tableau récapitulatif sans révéler le contenu exact :

| Partie | Type | Points | Durée conseillée |
|--------|------|--------|------------------|
| Exercice 1 | QCM (N questions) | X pts | Y min |
| Exercice 2 | Calculs | X pts | Y min |
| Exercice 3 | Problème guidé | X pts | Y min |

**Ne jamais révéler** le sujet exact des exercices.

#### Onglet "Compétences"

Pour chaque compétence évaluée :

```html
<div class="competence priorite-haute">
    <h4>📌 [Nom de la compétence]</h4>
    <ul>
        <li>Savoir [verbe d'action] : [description]</li>
        <li>Être capable de : [description]</li>
    </ul>
    <p class="niveau">Niveau attendu : ⭐⭐⭐</p>
</div>
```

Système de priorité :
- `priorite-haute` (rouge) : Compétences majeures du contrôle
- `priorite-moyenne` (jaune) : Compétences secondaires
- `priorite-basse` (vert) : Compétences mineures

Système d'étoiles :
- ⭐ : Application directe du cours
- ⭐⭐ : Exercice standard
- ⭐⭐⭐ : Exercice approfondi

#### Onglet "Quiz révision"

5-8 questions de compréhension du cours avec réponses cachées :

```html
<details class="question">
    <summary>1. [Question sur une définition/propriété]</summary>
    <div class="reponse">[Réponse courte et précise]</div>
</details>
```

Types de questions à inclure :
- Définitions clés ("Qu'est-ce qu'un vecteur ?")
- Propriétés à connaître ("Quelle est la formule de... ?")
- Méthodes ("Comment démontrer que... ?")
- Pièges courants ("Pourquoi ne peut-on pas... ?")

#### Onglet "Exercices fléchés"

Correspondance compétence → exercices de la fiche :

```html
<div class="exercice-fleche">
    <span class="notion">[Notion/Compétence]</span>
    <span class="numeros">Ex. N, M, P (questions a, b)</span>
</div>
```

Indiquer précisément :
- Le numéro de l'exercice
- Les questions spécifiques si l'exercice est long
- Le niveau de priorité (⚡ prioritaire, ✓ recommandé, ○ optionnel)

#### Onglet "Conseils"

```html
<div class="conseil">Révise d'abord [notion A] avant [notion B] car...</div>
<div class="conseil">Erreur fréquente : [description] → [comment l'éviter]</div>
<div class="conseil">Si tu manques de temps, concentre-toi sur [...]</div>
```

Inclure systématiquement :
- L'ordre de révision recommandé (basé sur les dépendances entre notions)
- Les erreurs fréquentes à éviter
- Les points de méthode essentiels
- Les priorités si le temps est limité

### ÉTAPE 5 : Validation et génération

1. **Vérifier la taille** : Le blueprint doit tenir sur une page A4 à l'impression
2. **Tester les onglets** : Vérifier que tous les onglets fonctionnent
3. **Confidentialité** : S'assurer qu'aucun exercice exact n'est révélé
4. **Utilité** : Chaque élément doit aider l'élève à réviser

## Règles importantes

1. **Confidentialité** : Le blueprint ne doit JAMAIS révéler les exercices exacts du contrôle
2. **Format** : Fichier HTML autonome, une seule page, pas de dépendances externes
3. **Interactivité** : Onglets fonctionnels, questions dépliables
4. **Exhaustivité** : Toutes les compétences évaluées doivent être mentionnées
5. **Intelligence** : Le fléchage des exercices doit être pertinent (basé sur l'analyse de la séquence)
6. **Imprimabilité** : Le document doit rester lisible à l'impression (tous onglets visibles)

## Format de sortie

Un seul fichier : `blueprint.html`
- Autonome (CSS et JS intégrés)
- Compatible avec tous les navigateurs modernes
- Imprimable sur une page A4

## Exemple d'utilisation

```
Génère le blueprint pour l'évaluation dans [chemin/vers/enonce.tex]
en analysant la séquence complète dans [chemin/vers/dossier_sequence]
```
