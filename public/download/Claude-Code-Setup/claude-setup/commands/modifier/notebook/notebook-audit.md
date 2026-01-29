# Audit et refactoring de notebooks Jupyter

**Paramètre requis :** $ARGUMENTS (chemin(s) de fichier(s) .ipynb, séparés par des espaces)

---

## Étape 0 : Charger le skill

Charge le skill `jupyter-notebook` pour avoir tous les critères pédagogiques en tête.

---

## Étape 1 : Analyser les fichiers

Pour chaque fichier dans $ARGUMENTS :

1. **Lire le fichier** avec l'outil Read
2. **Vérifier si le notebook est vide** (pas de cellules ou cellules vides uniquement)

### Si le notebook est VIDE :

Afficher :
```
Le notebook [nom_fichier] est vide.
J'ai compris - j'attends vos instructions pour le créer.

Que souhaitez-vous que ce notebook contienne ?
- Niveau (Seconde/Première/Terminale) ?
- Thème mathématique ?
- Notions à couvrir ?
```

Puis **STOP** - attendre les instructions de l'utilisateur avant de continuer.

### Si le notebook contient du contenu :

Passer à l'étape 2.

---

## Étape 2 : Audit ultra-critique

Analyser le notebook selon TOUS les critères du skill jupyter-notebook :

### Structure globale
- [ ] Header complet (niveau, thème, durée)
- [ ] Objectifs listés
- [ ] Prérequis définis
- [ ] Introduction avec problème/solution
- [ ] 3-5 notions couvertes
- [ ] Synthèse finale

### Pour chaque notion
- [ ] Cours avec syntaxe
- [ ] Exemple ACTIF (formules à compléter, pas passif)
- [ ] QCM avec exactement 3 questions
- [ ] Exercice de compréhension
- [ ] Exercice d'application (préremplissage réfléchi)

### Exercices
- [ ] Code prérempli pertinent (imports, compteurs, sortie)
- [ ] Parties mathématiques à compléter (`...`)
- [ ] Indices avec noms d'outils (pas les bornes/détails)
- [ ] Questions de réflexion dans les outils si pertinent
- [ ] Corrections dans `<details>` SANS emoji dans `<summary>`

### Indépendance des unités
- [ ] Corrections ne spoilent pas les exercices suivants
- [ ] Pas de recoupements numériques (ex: 6 figurines après des dés)
- [ ] Nombres ambitieux mais <= 100 000 simulations

### Technique
- [ ] Pas d'emojis dans `<summary>` (SyntaxError)
- [ ] Balises HTML bien fermées
- [ ] Cellules de code exécutables

---

## Étape 3 : Lister les problèmes

Pour chaque problème détecté, créer une entrée :

```
PROBLÈME #X : [Titre court]
- Localisation : cellule [N] ou ligne [L]
- Critère violé : [référence au skill]
- Description : [ce qui ne va pas]
- Impact : [pourquoi c'est problématique]
```

Afficher la liste complète et demander :
```
J'ai identifié [N] problèmes. Voulez-vous que je les traite un par un ?
(oui / non / seulement les critiques)
```

---

## Étape 4 : Refactoring interactif

Pour CHAQUE problème (dans l'ordre de priorité : critiques d'abord) :

### 4.1 Présenter le problème
```
PROBLÈME #X : [Titre]
[Description du problème]

Correction proposée : [ce que je compte faire]
```

### 4.2 Poser une question simple
Utiliser l'outil AskUserQuestion avec des options claires :

**Exemples de questions :**

- "Cet exemple de cours est passif. Quelles formules l'élève doit-il compléter ?"
  - Options : "Toutes les formules mathématiques" / "Seulement le calcul final" / "Je précise..."

- "Ce QCM n'a que 2 questions. Quel type de 3ème question ajouter ?"
  - Options : "Question de syntaxe" / "Question de comportement" / "Question de compréhension"

- "Cette correction utilise 💡 dans `<summary>`. Je remplace par :"
  - Options : "Correction" / "Correction A" / "Autre texte..."

- "Cet exercice utilise 6 figurines après un exercice sur les dés. Nouveau nombre ?"
  - Options : "24 figurines" / "32 figurines" / "Je choisis..."

### 4.3 Appliquer la correction
Après confirmation, utiliser Edit ou NotebookEdit pour appliquer la correction.

### 4.4 Confirmer
```
Correction #X appliquée.
Passage au problème suivant ? (oui / annuler la correction / arrêter)
```

---

## Étape 5 : Validation finale

Après tous les problèmes traités :

1. Relire le notebook modifié
2. Vérifier qu'aucun nouveau problème n'a été introduit
3. Afficher un résumé :

```
AUDIT TERMINÉ

Fichier : [nom]
Problèmes corrigés : [N]
Problèmes ignorés : [M]

Le notebook est maintenant conforme au skill jupyter-notebook.
Voulez-vous que j'exécute une validation technique (Restart & Run All) ?
```

---

## Règles importantes

1. **TOUJOURS** poser une question avant chaque modification
2. **JAMAIS** modifier sans confirmation explicite
3. **Questions simples** avec options prédéfinies + possibilité de texte libre
4. **Un problème à la fois** pour garder le contrôle
5. **Possibilité d'arrêter** à tout moment
