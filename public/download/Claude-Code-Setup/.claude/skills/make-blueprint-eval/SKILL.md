---
name: make-blueprint-eval
description: >
  Skill pour générer un blueprint (exosquelette pédagogique) d'une évaluation au format HTML.
  Le blueprint est une page web interactive avec onglets destinée aux étudiants pour réviser.
  Il présente la structure de l'évaluation, les compétences évaluées, des questions de compréhension
  du cours, et fléche les exercices types de la fiche. Le skill analyse la séquence globale
  (cours + exercices) pour proposer un parcours de révision intelligent.
  Utiliser ce skill après la création complète d'un sujet d'évaluation.
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
- Le fichier `synthese_evaluation.md` (généré par /makeEval)
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

Créer un fichier `blueprint.html` avec la structure suivante :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blueprint - [Chapitre] - Préparation au contrôle</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 15px;
            font-size: 14px;
            line-height: 1.4;
        }

        /* En-tête compact */
        .header {
            text-align: center;
            padding: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .header h1 { font-size: 1.5em; margin-bottom: 5px; }
        .header .info { display: flex; justify-content: center; gap: 20px; font-size: 0.9em; }

        /* Onglets */
        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }
        .tab {
            padding: 8px 15px;
            background: #e0e0e0;
            border: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s;
        }
        .tab:hover { background: #d0d0d0; }
        .tab.active {
            background: #667eea;
            color: white;
        }

        /* Contenu des onglets */
        .tab-content {
            display: none;
            padding: 15px;
            border: 2px solid #667eea;
            border-radius: 0 10px 10px 10px;
            background: #fafafa;
        }
        .tab-content.active { display: block; }

        /* Structure du contrôle */
        .structure-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        .structure-table th, .structure-table td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: left;
        }
        .structure-table th { background: #667eea; color: white; }
        .structure-table tr:nth-child(even) { background: #f5f5f5; }

        /* Compétences */
        .competence {
            background: white;
            padding: 10px;
            margin: 8px 0;
            border-left: 4px solid #667eea;
            border-radius: 0 8px 8px 0;
        }
        .competence h4 { color: #667eea; margin-bottom: 5px; }
        .niveau { color: #ffc107; }

        /* Questions */
        .question {
            background: #fff3cd;
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        }
        .question summary { cursor: pointer; font-weight: 500; }
        .question .reponse {
            margin-top: 8px;
            padding: 8px;
            background: #d4edda;
            border-radius: 5px;
            font-style: italic;
        }

        /* Exercices fléchés */
        .exercice-fleche {
            display: flex;
            justify-content: space-between;
            padding: 8px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            border: 1px solid #28a745;
        }
        .exercice-fleche .notion { font-weight: 500; color: #28a745; }
        .exercice-fleche .numeros { color: #666; }

        /* Conseils */
        .conseil {
            padding: 8px;
            margin: 5px 0;
            background: #e7f3ff;
            border-radius: 5px;
        }
        .conseil::before { content: "💡 "; }

        /* Priorité */
        .priorite-haute { border-left-color: #dc3545 !important; }
        .priorite-moyenne { border-left-color: #ffc107 !important; }
        .priorite-basse { border-left-color: #28a745 !important; }

        /* Impression */
        @media print {
            .tabs { display: none; }
            .tab-content {
                display: block !important;
                border: 1px solid #ccc;
                page-break-inside: avoid;
                margin-bottom: 10px;
            }
            body { font-size: 11px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Blueprint - [Titre du chapitre]</h1>
        <div class="info">
            <span>⏱️ [Durée] min</span>
            <span>📊 /20 points</span>
            <span>🧮 Calculatrice: [Oui/Non]</span>
        </div>
    </div>

    <div class="tabs">
        <button class="tab active" onclick="showTab('structure')">📋 Structure</button>
        <button class="tab" onclick="showTab('competences')">🎯 Compétences</button>
        <button class="tab" onclick="showTab('questions')">❓ Quiz révision</button>
        <button class="tab" onclick="showTab('exercices')">📝 Exercices types</button>
        <button class="tab" onclick="showTab('conseils')">💡 Conseils</button>
    </div>

    <!-- ONGLET 1 : Structure -->
    <div id="structure" class="tab-content active">
        <h3>Structure du contrôle</h3>
        <table class="structure-table">
            <tr>
                <th>Partie</th>
                <th>Type</th>
                <th>Points</th>
                <th>Durée conseillée</th>
            </tr>
            <!-- Remplir dynamiquement -->
        </table>
    </div>

    <!-- ONGLET 2 : Compétences -->
    <div id="competences" class="tab-content">
        <h3>Ce que tu dois maîtriser</h3>
        <!-- Liste des compétences avec niveau -->
    </div>

    <!-- ONGLET 3 : Questions de compréhension -->
    <div id="questions" class="tab-content">
        <h3>Vérifie ta compréhension du cours</h3>
        <p><em>Clique sur chaque question pour voir la réponse</em></p>
        <!-- Questions avec details/summary -->
    </div>

    <!-- ONGLET 4 : Exercices fléchés -->
    <div id="exercices" class="tab-content">
        <h3>Exercices à travailler en priorité</h3>
        <!-- Liste notion → exercices -->
    </div>

    <!-- ONGLET 5 : Conseils -->
    <div id="conseils" class="tab-content">
        <h3>Conseils de révision</h3>
        <!-- Conseils personnalisés -->
    </div>

    <script>
        function showTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
```

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
