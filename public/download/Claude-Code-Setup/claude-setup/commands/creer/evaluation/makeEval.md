# /makeEval - Génération automatique d'évaluations à partir de ressources pédagogiques

## Description

Génère automatiquement un sujet d'évaluation complet et équilibré à partir de ressources pédagogiques existantes (cours, exercices, activités). Analyse les compétences développées, sélectionne et adapte des exercices, et produit deux versions différentes mais équivalentes en difficulté.

## Usage

```
/makeEval <dossier(s)_source> [--duree <minutes>] [--qcm <nombre_questions>] [--demande "<instructions_complementaires>"]
```

## Paramètres

- `<dossier(s)_source>` : Un ou plusieurs chemins vers :
  - Un dossier de séquence complet (contenant cours, exercices, etc.)
  - Plusieurs dossiers de projets LaTeX spécifiques
  - Séparés par des virgules ou espaces
- `--duree <minutes>` : Durée prévue de l'évaluation (optionnel, défaut: 55 minutes)
- `--qcm <nombre_questions>` : Nombre de questions du QCM (optionnel, défaut: 6)
  - Mettre `0` ou `false` pour désactiver le QCM
  - Standard : 6 questions @ 1 pt = 6 points (12 questions c'est trop long)
- `--demande "<instructions>"` : Demandes complémentaires de l'utilisateur (optionnel)
  - Exemples : "insister sur les calculs", "sans calculatrice", "inclure une question de cours sur...", etc.

## Exemples d'utilisation

```bash
# Évaluation sur une séquence complète (avec QCM 6 questions @ 1 pt par défaut)
/makeEval "1. Cours\2nde\Sequence-Vecteurs" --duree 50

# Évaluation sans QCM
/makeEval "1. Cours\3eme\Sequence-Pythagore" --duree 60 --qcm 0

# QCM avec 8 questions (8 points)
/makeEval "1. Cours\4eme\Sequence-Proportionnalite" --duree 30 --qcm 8

# Avec demande complémentaire et question de cours dans le QCM
/makeEval "1. Cours\1ere_spe\Sequence-Suites" --duree 45 --demande "inclure une question de cours sur la définition d'une suite arithmétique dans le QCM, éviter les suites géométriques"

# QCM 4 questions seulement (4 points)
/makeEval "1. Cours\1ere_ens_scient\Sequence-Pourcentages" --duree 50 --qcm 4 --demande "exclure les tableaux de contingence du QCM"
```

## Protocole d'exécution

### ÉTAPE 1 : ANALYSE DES RESSOURCES

1. **Lire le contenu des dossiers fournis** :
   - Identifier tous les fichiers LaTeX pertinents (cours, exercices, activités, évaluations précédentes)
   - Extraire le contenu de chaque fichier

2. **Extraction des compétences développées** :
   - Identifier les compétences du programme officiel abordées
   - Classifier par type : Chercher, Modéliser, Représenter, Raisonner, Calculer, Communiquer

3. **Extraction des exercices** :
   - **Exercices d'application directe** : exercices simples testant une seule notion
   - **Exercices composés** : exercices mobilisant plusieurs notions
   - **Problèmes** : exercices contextualisés ou de synthèse
   - Noter le niveau de difficulté de chaque exercice

### ⚠️ VALIDATION 0 : PROPOSITION DE RECHERCHE DE RESSOURCES COMPLÉMENTAIRES

**ARRÊT OBLIGATOIRE** : Après l'analyse des ressources locales (étape 1), tu DOIS :

1. **Présenter un résumé des ressources trouvées** :
   - Nombre d'exercices disponibles dans les ressources locales
   - Notions couvertes
   - Lacunes éventuelles identifiées

2. **Proposer explicitement la recherche complémentaire** :
   - "J'ai analysé les ressources locales. Souhaitez-vous que je cherche des exercices complémentaires sur :"
   - **mathAlea (coopmaths.fr)** : Exercices paramétrables et générables automatiquement
   - **Problémathèque CSEN** : Problèmes de recherche et situations complexes
   - Les deux sources
   - Aucune recherche complémentaire (continuer avec les ressources locales uniquement)

3. **Utiliser le tool `AskUserQuestion`** pour présenter les options clairement

4. **Attendre la réponse de l'utilisateur**

### ÉTAPE 2 : RECHERCHE D'EXERCICES COMPLÉMENTAIRES (si demandé)

**IMPORTANT** : Cette étape n'est exécutée QUE si l'utilisateur l'a demandé lors de la validation 0.

1. **Si recherche mathAlea demandée** :
   - Utiliser l'agent `mathalea-scraper` pour trouver des exercices sur https://coopmaths.fr
   - Rechercher par compétences identifiées
   - Rechercher par thème/notion
   - Récupérer le code JavaScript des exercices disponibles
   - Privilégier les exercices paramétrables (pour générer plusieurs versions)
   - Vérifier la cohérence avec le niveau visé

2. **Si recherche Problémathèque demandée** :
   - Utiliser `WebFetch` pour rechercher sur https://www.problematheque-csen.fr
   - Rechercher des problèmes correspondant aux compétences identifiées
   - Privilégier les problèmes adaptés au niveau visé
   - Extraire les énoncés et les adapter au format de l'évaluation

3. **Présenter les ressources trouvées** :
   - Lister les exercices/problèmes complémentaires identifiés
   - Indiquer leur pertinence par rapport aux compétences à évaluer
   - Permettre à l'utilisateur de sélectionner ceux qu'il souhaite intégrer

### ÉTAPE 3 : CONSTITUTION DU SUJET TYPE ET SYNTHÈSE

**CONTRAINTES OBLIGATOIRES** :

1. **Barème : 20 points exactement**

2. **Exhaustivité** :
   - Couvrir le maximum de compétences identifiées dans les ressources
   - Garantir au moins une question par notion principale

3. **Diversification** :
   - Minimum 3 types de compétences différents parmi : Chercher, Modéliser, Représenter, Raisonner, Calculer, Communiquer
   - Varier les formats : QCM, questions ouvertes, exercices guidés, problèmes

4. **Adaptation temporelle** :
   - Respecter la durée spécifiée (paramètre `--duree`)
   - Estimer ~2 minutes par point en moyenne
   - Ajuster la quantité d'exercices en conséquence

5. **Questions de base** :
   - **OBLIGATOIRE** : Inclure des questions simples testant les connaissances basiques du chapitre
   - Environ 30-40% du barème consacré aux fondamentaux (définitions, applications directes)

6. **Demande complémentaire** :
   - Intégrer les instructions spécifiques de l'utilisateur (paramètre `--demande`)

**SÉLECTION DES EXERCICES** :

- Tu n'es **PAS OBLIGÉ** de prendre tous les exercices trouvés dans les ressources
- Sélectionne judicieusement pour respecter les contraintes ci-dessus
- Privilégie la qualité et la cohérence à la quantité

**STRUCTURE TYPE DU SUJET** :

```
┌─────────────────────────────────────────────────┐
│ Exercice 1 : QCM (6 points) - PAR DÉFAUT       │
│ - N questions @ 1 point chacune                │
│ - Par défaut N=6 (6 points)                    │
│ - Connaissances de base du chapitre            │
│ - Définitions, propriétés essentielles         │
│ - Applications directes du cours               │
│ - Peut intégrer une question de cours          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Partie 2 : Exercices d'application (8-10 pts)  │
│ - 2-3 exercices mobilisant les notions         │
│ - Questions progressives (guidage possible)     │
│ - Diversification des compétences               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Partie 3 : Problème ou synthèse (4-6 points)   │
│ - Exercice contextualisé ou de synthèse         │
│ - Mobilise plusieurs notions simultanément      │
│ - Compétences Chercher / Modéliser              │
└─────────────────────────────────────────────────┘
```

**CRÉATION DU FICHIER DE SYNTHÈSE** :

Créer un fichier `synthese_evaluation.md` détaillant :
- Structure du sujet (liste des exercices avec leurs barèmes)
- Compétences évaluées par exercice
- Justification des choix pédagogiques
- Estimation du temps de résolution
- Répartition du barème (QCM, application, synthèse)

### ⚠️ VALIDATION 1 : DEMANDER LES REMARQUES DE L'UTILISATEUR

**ARRÊT OBLIGATOIRE** : Après avoir créé le fichier `synthese_evaluation.md`, tu DOIS :

1. **Présenter la synthèse à l'utilisateur** (afficher le contenu du fichier)
2. **Demander explicitement ses remarques** :
   - "Voici la structure de l'évaluation que je propose. Avez-vous des remarques ou modifications à apporter ?"
   - Utiliser le tool `AskUserQuestion` si nécessaire
3. **Attendre la réponse de l'utilisateur**
4. **Prendre note des modifications demandées**

### ÉTAPE 3.5 : INTÉGRATION DES REMARQUES SUR LA SYNTHÈSE

1. **Analyser les remarques de l'utilisateur** :
   - Identifier les exercices à modifier, ajouter ou supprimer
   - Identifier les ajustements de barème
   - Identifier les changements de compétences à évaluer

2. **Mettre à jour la synthèse** :
   - Modifier le fichier `synthese_evaluation.md` selon les remarques
   - Ajuster la structure du sujet si nécessaire
   - Vérifier que les 6 contraintes obligatoires sont toujours respectées

3. **Confirmer les modifications** :
   - Résumer les changements apportés
   - Demander validation avant de passer à l'étape suivante

### ÉTAPE 4 : CRÉATION DU SUJET AVEC VARIABLES

1. **Paramétrer les exercices** :
   - Identifier les valeurs numériques modifiables
   - Créer des variables LaTeX ou des macros pour les données changeantes
   - Garantir que les modifications ne changent PAS la difficulté

2. **Structure du fichier maître** :
   - Utiliser le modèle `Devoir` avec le skill tex-document-creator
   - Définir les variables en en-tête
   - Rédiger le sujet avec ces variables

3. **Créer le fichier LaTeX standard** :
   - Implémenter avec le skill bfcours-latex le fichier `enonce.tex` avec toutes les variables définies
   - Ce fichier servira de base pour générer les versions A et B

4. **Intégration du QCM (si activé)** :
   - Créer un Exercice ( en premier ) dédié au QCM avec le skill qcm-creator

### ⚠️ VALIDATION 2 : DEMANDER LES REMARQUES SUR LE SUJET LATEX

**ARRÊT OBLIGATOIRE** : Après avoir créé le fichier LaTeX standard (`enonce.tex`), tu DOIS :

1. **Compiler le fichier LaTeX** pour générer un PDF de prévisualisation
2. **Présenter le contenu à l'utilisateur** :
   - Afficher un extrait du code LaTeX
   - Proposer d'ouvrir le PDF compilé si disponible
3. **Demander explicitement ses remarques** :
   - "Voici le sujet LaTeX standard créé. Avez-vous des remarques ou modifications à apporter avant de générer les versions A et B ?"
   - Proposer des options : "Modifier un exercice", "Ajuster le barème", "Reformuler une question", "Valider et continuer"
4. **Attendre la réponse de l'utilisateur**
5. **Prendre note des modifications demandées**

### ÉTAPE 4.5 : INTÉGRATION DES REMARQUES SUR LE SUJET LATEX

1. **Analyser les remarques de l'utilisateur** :
   - Identifier les exercices à modifier
   - Identifier les reformulations nécessaires
   - Identifier les ajustements de mise en page ou de présentation

2. **Mettre à jour le fichier LaTeX** :
   - Appliquer les modifications demandées dans `enonce.tex`
   - Vérifier la cohérence avec la synthèse
   - Recompiler pour vérification

3. **Confirmer les modifications** :
   - Résumer les changements apportés
   - Demander validation finale avant de générer les versions A et B

### ÉTAPE 5 : GÉNÉRATION DES DEUX VERSIONS

1. **Version A et Version B** :
   - les label ( remplacer le niveau par la version. Exemple : "A" au lieu de  "2nde -- version A" )
   - Modifier uniquement les valeurs des variables
   - Conserver strictement :
     - Le même nombre d'exercices
     - Le même type de questions
     - Le même niveau de difficulté
     - Le même barème
   - Seules différences : valeurs numériques, contextes mineurs

2. **Validation de l'équivalence** :
   - Vérifier que les deux versions requièrent les mêmes démarches de résolution
   - Confirmer que le temps de résolution estimé est identique

### ÉTAPE 6 : COMPILATION ET VÉRIFICATION

1. **Utiliser le skill `tex-compiling-skill`** pour compiler :
   - Sujet version A
   - Sujet version B
   - Corrections des deux versions

2. **Vérifier avec le skill `pdf`** :
   - Lisibilité des énoncés
   - Cohérence des figures et schémas
   - Absence d'erreurs typographiques

3. **Produire un résumé** :
   - Liste des compétences évaluées
   - Répartition du barème
   - Estimation du temps de résolution

### ÉTAPE 7 : GÉNÉRATION DU BLUEPRINT (FICHE DE PRÉPARATION HTML)

**ARRÊT OBLIGATOIRE** : Après la compilation et vérification, tu DOIS proposer la génération d'un blueprint.

1. **Proposer la génération du blueprint** :
   - Utiliser `AskUserQuestion` pour demander : "Souhaitez-vous que je génère un blueprint (fiche de préparation interactive pour les élèves) ?"
   - Options : "Oui, générer le blueprint" / "Non, terminer ici"

2. **Si l'utilisateur accepte** :
   - **Charger le skill `make-blueprint-eval`**
   - **Analyser la séquence globale** : cours + fiche d'exercices + activités
   - Générer le blueprint HTML interactif en suivant le protocole du skill

3. **Contenu du blueprint HTML** :
   - **Onglet Structure** : Tableau récapitulatif (sans révéler les exercices exacts)
   - **Onglet Compétences** : Liste des compétences avec niveau d'exigence et priorité
   - **Onglet Quiz révision** : 5-8 questions de compréhension du cours avec réponses cachées
   - **Onglet Exercices fléchés** : Correspondance compétence → exercices de la fiche (intelligemment mappés)
   - **Onglet Conseils** : Ordre de révision, erreurs fréquentes, priorités

4. **Fichier généré** :
   - `blueprint.html` : Page web autonome et interactive
   - Doit tenir sur une page A4 à l'impression
   - Onglets fonctionnels pour navigation
   - Questions de compréhension dépliables

5. **Validation finale** :
   - Présenter le blueprint à l'utilisateur
   - Vérifier qu'aucun exercice exact n'est révélé
   - Vérifier que le fléchage des exercices est pertinent
   - Permettre des ajustements si nécessaire

## Agents utilisés

- **mathalea-scraper** (optionnel) : Recherche et récupère des exercices sur coopmaths.fr si demandé par l'utilisateur
- **qcm-builder** : Génère automatiquement un QCM adapté au niveau (si activé, par défaut 6 questions @ 1 pt)

**⚠️ IMPORTANT - Gestion du contexte .claude** :

Tu es lancé dans un répertoire de projet qui contient un dossier `.claude` local avec toutes les ressources nécessaires (templates, skills, serveurs MCP, configuration). Tu peux y accéder directement.

**RÈGLE OBLIGATOIRE** : Si tu appelles des sous-agents (comme mathalea-scraper) avec le Task tool, tu DOIS leur transmettre le chemin absolu vers ce dossier `.claude` dans ton prompt, sinon ils chercheront dans le `.claude` à la racine (qui est vide) et échoueront.

**Comment faire** :
1. Détermine le chemin absolu du répertoire courant  Pour obtenir le chemin absolu au format Windows :  `pwd -W`ou Si PowerShell : `(Get-Location).Path`

2. Construis le chemin `.claude` : `<chemin_courant>\.claude`
3. Dans chaque prompt de sous-agent, inclus explicitement : "Utilise le dossier .claude situé à : `<chemin_absolu>`"

## Skills utilisés

- `tex-document-creator` : Initialisation du projet d'évaluation
- `bfcours-latex` : Rédaction du contenu LaTeX
- `tex-compiling-skill` : Compilation des fichiers
- `pdf` : Vérification du rendu final
- `programmes-officiels` : Validation des compétences évaluées
- `make-blueprint-eval` : Génération du blueprint HTML interactif (étape 7)

## Output attendu

À la fin de l'exécution, l'utilisateur obtient :

```
Dossier_Evaluation_[Theme]/
├── Sujet_Version_A.tex
├── Sujet_Version_B.tex
├── Correction_Version_A.tex
├── Correction_Version_B.tex
├── variables.tex (fichier de configuration)
├── synthese_evaluation.md (résumé des compétences et barème)
└── blueprint.html (fiche de préparation interactive - optionnel)
```

## Notes importantes

- **Modularité** : Si l'utilisateur n'est pas satisfait d'un exercice, proposer des alternatives
- **Respect des contraintes** : Les 6 contraintes obligatoires doivent TOUJOURS être respectées
- **Interaction** : Demander confirmation avant de générer si des choix pédagogiques sont ambigus
