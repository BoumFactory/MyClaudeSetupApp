# Guide d'Utilisation - Second Degré Partie 2

Guide complet pour utiliser l'application de révision interactive.

## Démarrage Rapide

### Pour les élèves (Exécutable)

1. **Lancer l'application**
   - Double-cliquer sur `SecondDegre_Partie2.exe`
   - Attendre quelques secondes (démarrage du serveur)
   - L'application s'ouvre automatiquement dans votre navigateur

2. **Si le navigateur ne s'ouvre pas automatiquement**
   - Ouvrir votre navigateur (Chrome, Firefox, Edge...)
   - Aller à l'adresse : http://localhost:5000

3. **Navigation**
   - Page d'accueil : Cours complet
   - Onglet "Exercices" : Exercices interactifs

### Pour les enseignants (Depuis les sources)

```bash
# Se placer dans le répertoire
cd Applications_educatives/app_second_degre_partie2

# Lancer l'application
python app.py
```

## Utilisation du Cours

### Structure du cours

Le cours est divisé en 3 sections principales :

1. **Factorisation d'un trinôme**
   - Définition du discriminant Δ
   - Forme factorisée selon le signe de Δ

2. **Signe du trinôme et discriminant**
   - Tableau de signes
   - Méthode pour construire le tableau

3. **Équations et inéquations du second degré**
   - Résolution d'équations
   - Résolution d'inéquations

### Navigation dans le cours

- **Sommaire interactif** : Cliquez sur une section pour y accéder directement
- **Scroll** : Parcourez les sections en défilant
- **Highlight** : La section active est mise en évidence dans le sommaire

### Compétences travaillées

Au début du cours, vous trouvez les 4 compétences principales :
1. Calculer le discriminant
2. Connaître le lien entre discriminant et signe
3. Dresser le tableau de signes
4. Résoudre équations et inéquations

## Utilisation des Exercices

### Vue d'ensemble

4 exercices corrigés couvrant l'ensemble du cours :

| Exercice | Thème | Points | Difficulté |
|----------|-------|--------|------------|
| 1 | Racines et forme factorisée | 3 | Facile |
| 2 | Résoudre une équation | 5 | Facile |
| 3 | Résoudre une inéquation (1) | 6 | Moyen |
| 4 | Résoudre une inéquation (2) | 6 | Moyen |

**Total : 20 points**

### Comment faire un exercice

#### Étape 1 : Lire l'énoncé

Lisez attentivement la question affichée dans le cadre gris.

#### Étape 2 : Répondre

- Remplissez **tous les champs** demandés
- Pour les nombres : utilisez `.` comme séparateur décimal
- Pour les fractions : écrivez `1/2` ou `0.5`
- Pour les intervalles : respectez la notation mathématique

**Exemples de réponses valides :**
- Nombre entier : `25` ou `-3`
- Nombre décimal : `1.5` ou `-2.4`
- Fraction : `1/2`, `-3/2`, `0.5`
- Intervalle : `[1;3]`, `]-∞;2[`, etc.

#### Étape 3 : Vérifier

- Cliquez sur **"Vérifier ma réponse"** ou appuyez sur **Entrée**
- Le système vérifie automatiquement vos réponses
- Un feedback s'affiche immédiatement

#### Étape 4 : Consulter le feedback

**Si tout est correct (✅) :**
- Message de félicitation
- Points gagnés
- Statut ✅ sur l'exercice

**Si une erreur (❌) :**
- Message d'erreur
- Indication des champs incorrects (✗ rouge)
- Possibilité de voir la solution détaillée

#### Étape 5 : Utiliser l'indice (optionnel)

Si vous êtes bloqué :
- Cliquez sur **"💡 Afficher l'indice"**
- Un conseil s'affiche pour vous aider

### Système de progression

#### Barre de progression

En haut de la page des exercices :
- **Nombre d'exercices complétés** : X / 4
- **Score actuel** : XX%

La barre se remplit au fur et à mesure.

#### Sauvegarde automatique

- Votre progression est **sauvegardée automatiquement**
- Stockage local dans votre navigateur (localStorage)
- Vous pouvez fermer et rouvrir l'application sans perdre vos données

**Attention** : Ne pas utiliser le mode navigation privée !

### Résumé final

Quand les 4 exercices sont complétés :

- **Score final** : pourcentage de réussite
- **Exercices réussis** : nombre d'exercices avec 100%
- **Temps total** : durée totale passée

Possibilité de :
- **Recommencer** tous les exercices
- **Retourner au cours** pour réviser

## Fonctionnalités Avancées

### Formules mathématiques

Les formules sont rendues avec **MathJax** :
- Notation LaTeX standard
- Rendu professionnel
- Nécessite une connexion internet

**Si les formules ne s'affichent pas** :
1. Vérifier votre connexion internet
2. Recharger la page (F5)
3. Vider le cache du navigateur

### Raccourcis clavier

- **Entrée** : Vérifier la réponse (dans un champ)
- **Tab** : Naviguer entre les champs
- **Ctrl + R** / **F5** : Recharger la page
- **F12** : Ouvrir la console (pour debug)

### Mode responsive

L'application s'adapte automatiquement :
- **Desktop** : Affichage large
- **Tablette** : Affichage adapté
- **Mobile** : Affichage vertical optimisé

## Dépannage

### L'application ne démarre pas

**Symptômes** : L'exe se ferme immédiatement

**Solutions** :
1. Vérifier que le **port 5000** n'est pas utilisé
2. Désactiver temporairement **l'antivirus**
3. Exécuter en tant qu'**administrateur**
4. Vérifier les **logs** (voir section ci-dessous)

### Le navigateur ne s'ouvre pas

**Solution** :
1. Ouvrir manuellement votre navigateur
2. Aller à : http://localhost:5000

### Les formules mathématiques ne s'affichent pas

**Symptômes** : Les formules apparaissent en texte brut

**Solutions** :
1. Vérifier votre **connexion internet**
2. Attendre le **chargement complet** de la page
3. **Recharger la page** (F5)
4. Essayer un **autre navigateur**

### Ma progression a disparu

**Causes possibles** :
- Navigation privée utilisée
- Cache du navigateur effacé
- Changement de navigateur

**Solution** :
- Utiliser toujours le **même navigateur**
- **Ne pas** utiliser le mode navigation privée
- **Ne pas** effacer les données de navigation

### Les réponses ne sont pas acceptées

**Vérifications** :
1. Tous les champs sont remplis ?
2. Format correct (voir exemples ci-dessus) ?
3. Pas d'espaces inutiles ?

**Formats acceptés** :
- Fractions : `1/2`, `-3/2`, `0.5`, `-1.5`
- Intervalles : `[1;3]`, `]2;5[`, `]-∞;1]`

## Conseils Pédagogiques

### Pour bien utiliser l'application

1. **Lire d'abord le cours** en entier
2. **Prendre des notes** sur papier
3. **Faire les exercices** sans aide
4. **Utiliser l'indice** seulement si bloqué
5. **Analyser la solution** en cas d'erreur
6. **Refaire les exercices** jusqu'à 100%

### Méthode de révision recommandée

**Session 1** (30-45 min) :
1. Lire le cours complet
2. Noter les formules importantes
3. Faire les exercices 1 et 2

**Session 2** (30-45 min) :
1. Relire la section 2 et 3 du cours
2. Faire les exercices 3 et 4
3. Analyser les erreurs

**Session 3** (15-30 min) :
1. Refaire tous les exercices
2. Viser 100% de réussite

### Points clés à retenir

1. **Discriminant** : Δ = b² - 4ac
2. **Trois cas** : Δ < 0, Δ = 0, Δ > 0
3. **Signe du trinôme** : dépend de a et de Δ
4. **Entre les racines** : signe de -a

## Support et Contact

### Problèmes techniques

1. Consulter ce guide d'utilisation
2. Vérifier le README.md
3. Consulter la console du navigateur (F12)

### Questions pédagogiques

Contacter votre enseignant :
- Lycée Camille Claudel
- Cours de Première Spécialité Mathématiques

## Informations Techniques

### Configuration requise

**Minimale** :
- Windows 7 ou supérieur
- 2 Go de RAM
- 50 Mo d'espace disque
- Navigateur web moderne

**Recommandée** :
- Windows 10 ou supérieur
- 4 Go de RAM
- Connexion internet (pour MathJax)
- Chrome ou Firefox récent

### Navigateurs supportés

- ✅ Google Chrome (recommandé)
- ✅ Mozilla Firefox (recommandé)
- ✅ Microsoft Edge
- ✅ Safari
- ⚠️ Internet Explorer (non supporté)

### Données et confidentialité

- **Aucune donnée** n'est envoyée sur internet
- **Sauvegarde locale** uniquement (localStorage)
- **Pas de tracking** ni d'analyse
- **Totalement offline** (sauf MathJax)

---

**Version** : 1.0.0
**Dernière mise à jour** : 20 octobre 2025
**Auteur** : Lycée Camille Claudel
