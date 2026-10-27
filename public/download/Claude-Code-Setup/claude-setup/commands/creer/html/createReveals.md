# /createReveals - Création de présentations reveal.js interactives

## Description

Crée automatiquement une présentation reveal.js interactive et stylée de haute qualité adaptée au contexte (collège, lycée, académique).

**PAR DÉFAUT : Contenu EXHAUSTIF** - La présentation contient TOUT le contenu du document source (tous les exercices, toutes les sections, tous les exemples). Rien n'est omis sauf instruction explicite contraire.

Gère la création, test et finalisation de manière autonome via l'agent reveals-creator.

## Philosophie

**PRINCIPE FONDAMENTAL** : Produire une présentation **complète**, **interactive** et **élégante**, prête à être présentée en classe ou en conférence.

**RÈGLE D'OR : Templates prédéfinis avec CSS fixe**

Les présentations sont générées à partir de templates validés stockés dans `.claude/datas/reveal-templates/` :
- `template-college.html` : Style collège (couleurs vives, police 22px)
- `template-lycee.html` : Style lycée (équilibré, police 20px)
- `template-academique.html` : Style académique (sobre, police 18px)

**Le CSS et le design sont FIXES** - l'agent ne fait que remplir le contenu HTML.

Le système :
- Analyse le public cible et choisit le style approprié
- **Traite TOUT le contenu source de manière exhaustive**
- Détecte automatiquement si le contenu est volumineux et adapte sa stratégie
- Crée le contenu HTML/CSS/JS avec alternance pédagogique question/réponse
- Respecte les règles de densité et d'espacement
- Intègre MathJax pour les formules mathématiques
- Utilise les fragments pour révélation progressive
- Teste dans un navigateur
- Finalise et nettoie

## Gestion du contenu volumineux

**Stratégie adaptative automatique** :

| Taille du document source | Stratégie |
|---------------------------|-----------|
| < 500 lignes | Traitement direct par l'agent reveals-creator |
| 500-1000 lignes | Traitement séquentiel par sections |
| > 1000 lignes | Délégation à plusieurs agents en parallèle + assemblage |

**L'agent principal est autonome** : Il détermine lui-même s'il doit déléguer ou traiter directement. L'utilisateur n'a PAS besoin de redemander des compléments.

## Usage

```
/createReveals [--style <collège|lycée|académique>] --sujet "<sujet>" --duree <minutes> [--output <chemin>]
```

## Paramètres

- `--style <collège|lycée|académique>` : Style de présentation (optionnel, détecté automatiquement si non spécifié)
  - `collège` : Pour classes de 6e à 3e (couleurs vives, police 22px, animations fréquentes)
  - `lycée` : Pour classes de 2nde à Terminale (équilibré, police 20px)
  - `académique` : Pour conférences, colloques (sobre, police 18px)

- `--sujet "<sujet>"` : Sujet de la présentation (obligatoire)
  - Exemples : "Les nombres relatifs", "Dérivation des fonctions", "Analyse spectrale"

- `--duree <minutes>` : Durée approximative de la présentation (obligatoire)
  - Utilisé pour estimer le nombre de slides (durée ÷ 2-3 min)

- `--output <chemin>` : Chemin de sortie (optionnel, défaut: `./presentation.html`)

- `--exercices <nombre>` : Nombre d'exercices souhaités (optionnel, défaut: auto selon durée)

- `--auteur "<nom>"` : Nom de l'auteur (optionnel)

- `--etablissement "<nom>"` : Nom de l'établissement (optionnel)

## Workflow

L'agent reveals-creator est appelé avec le skill :
- **reveals-presentation** : Expertise reveal.js complète

**⚠️ IMPORTANT - Gestion du contexte .claude** :

Tu es lancé dans un répertoire de projet qui contient un dossier `.claude` local avec toutes les ressources nécessaires (templates, skills, serveurs MCP, configuration). Tu peux y accéder directement.

**RÈGLE OBLIGATOIRE** : Si tu appelles des sous-agents avec le Task tool, tu DOIS leur transmettre le chemin absolu vers ce dossier `.claude` dans ton prompt, sinon ils chercheront dans le `.claude` à la racine (qui est vide) et échoueront.

**Comment faire** :
1. Détermine le chemin absolu du répertoire courant  Pour obtenir le chemin absolu au format Windows :  `pwd -W`ou Si PowerShell : `(Get-Location).Path`

2. Construis le chemin `.claude` : `<chemin_courant>\.claude`
3. Dans chaque prompt de sous-agent, inclus explicitement : "Utilise le dossier .claude situé à : `<chemin_absolu>`"

### Étapes automatiques

1. **Analyse de la demande**
   - Identifier le style selon le public ou paramètre `--style`
   - Extraire sujet, durée, nombre de slides estimé
   - Choisir le template approprié

2. **Création du contenu HTML**
   - Charger le template prédéfini (collège/lycée/académique) depuis `.claude/datas/reveal-templates/`
   - Conserver INTÉGRALEMENT le CSS et la configuration Reveal.js
   - Remplir UNIQUEMENT le contenu HTML entre `<div class="slides">` et `</div>`
   - Utiliser les classes CSS prédéfinies du template
   - Remplir les métadonnées (titre, auteur, description)
   - Structurer le contenu :
     - Titre + plan
     - Sections thématiques
     - Exercices avec estimation de temps
     - Alternance question/réponse
     - Conclusion
   - Respecter les règles de densité (60% collège, 70% lycée/académique)
   - Intégrer MathJax pour les formules mathématiques (délimiteurs `\(...\)` et `\[...\]`)
   - Utiliser les fragments pour révélation progressive

3. **Test**
   - Lancer un serveur local (Python ou Node.js)
   - Ouvrir dans le navigateur
   - Vérifier navigation, fragments, formules
   - Tester responsive (mobile/tablette)
   - Vérifier mode présentation (touche S)

4. **Finalisation**
   - Corriger les bugs détectés
   - Optimiser la mise en page
   - Valider le responsive design

5. **Rapport final**
   - Résumé de la présentation
   - Nombre de slides
   - Exercices intégrés
   - Instructions d'utilisation

## Exemples d'utilisation

### Exemple 1 : Présentation collège automatique

```bash
/createReveals --sujet "Les nombres relatifs" --duree 20
```

**Résultat** :
- Style détecté : collège (sujet adapté à ce niveau)
- Template : `template-college.html`
- 11 slides créées (20 min ÷ 2 min/slide)
- 2 exercices intégrés
- Police 22px, couleurs vives
- Densité < 60%
- MathJax intégré
- Présentation prête : `presentation.html`

### Exemple 2 : Cours lycée

```bash
/createReveals --style lycée --sujet "Dérivation des fonctions" --duree 55 \
  --auteur "M. Dupont" --etablissement "Lycée Exemple"
```

**Résultat** :
- Style : lycée
- Template : `template-lycee.html`
- 25 slides créées (55 min = 1h de cours)
- 4 exercices intégrés avec estimation de temps
- Métadonnées remplies
- Densité < 70%
- Fragments pour révélation progressive
- Présentation prête : `presentation.html`

### Exemple 3 : Conférence académique

```bash
/createReveals --style académique \
  --sujet "Convergence des schémas volumes finis" \
  --duree 30 --output "./seminaire_2025.html"
```

**Résultat** :
- Style : académique
- Template : `template-academique.html`
- 23 slides créées (30 min de présentation)
- Sections : Contexte, Théorie, Résultats, Discussion, Conclusion, Références
- Sobre, professionnel
- Présentation prête : `seminaire_2025.html`

## Détection automatique du style

Si `--style` n'est pas spécifié, le système détecte automatiquement :

| Indice dans le sujet | Style détecté |
|----------------------|---------------|
| "6e", "5e", "4e", "3e", "collège" | Collège |
| "2nde", "1ère", "Tale", "lycée" | Lycée |
| "analyse", "théorème", "conférence", "séminaire" | Académique |
| Par défaut (si ambigu) | Lycée |

## Caractéristiques par style

### Collège

- **Police** : 22px (titres 2.5em)
- **Densité max** : 60%
- **Items/slide** : 5 max
- **Lignes** : 8 max
- **Animations** : Fréquentes (fragments sur presque tout)
- **Couleurs** : Vives (dégradés, couleurs primaires)
- **Exercices** : Interactifs, ludiques
- **Slides/heure** : 15-20
- **Font** : Comic Neue ou similaire

### Lycée

- **Police** : 20px (titres 2em)
- **Densité max** : 70%
- **Items/slide** : 6-7 max
- **Lignes** : 10-12 max
- **Animations** : Modérées
- **Couleurs** : Équilibrées (bleu marine, bordeaux)
- **Exercices** : Guidés, appliqués
- **Slides/heure** : 25-35
- **Font** : Roboto ou Arial

### Académique

- **Police** : 18px (titres 1.8em)
- **Densité max** : 70%
- **Items/slide** : 7 max
- **Lignes** : 12-14 max
- **Animations** : Rares (uniquement pour emphase)
- **Couleurs** : Sobres (noir, gris, blanc)
- **Transitions** : Simples (fade ou slide)
- **Références** : Bibliographie obligatoire
- **Slides/heure** : 40-60
- **Font** : Lato ou Georgia

## Agent et skill utilisés

### Agent : reveals-creator

**Modèle** : `claude-haiku-4-5-20251001` (rapide et efficace)

**Autonomie** : Totale (pas d'intervention utilisateur nécessaire)

**Responsabilités** :
- Création du contenu HTML/CSS/JS complet
- Intégration de MathJax
- Configuration reveal.js
- Test dans navigateur
- Finalisation

### Skill

**reveals-presentation**
- Guides de référence (fragments, MathJax, best practices, styles)
- Règles de densité et espacement
- Classes CSS pour exercices et boxes
- Estimation des temps pour exercices
- Gestion des fragments et transitions

## Vérifications effectuées

Avant de valider la présentation, l'agent vérifie :

### Contenu

- [ ] Toutes les métadonnées renseignées
- [ ] Structure cohérente (titre, plan, sections, conclusion)
- [ ] Alternance question/réponse respectée
- [ ] Exercices avec temps estimé
- [ ] Formules mathématiques avec MathJax

### Visuel

- [ ] Chaque slide < densité maximale (60% ou 70%)
- [ ] Police ≥ taille minimale (18px, 20px, 22px)
- [ ] Couleurs cohérentes avec le thème
- [ ] Contraste suffisant
- [ ] Formules mathématiques correctes
- [ ] Pas de débordement de contenu

### Technique

- [ ] HTML bien formé (balises fermées)
- [ ] MathJax chargé et fonctionnel
- [ ] Fragments testés et fonctionnels
- [ ] Navigation fluide (flèches, espace)
- [ ] Mode présentation (touche S) opérationnel
- [ ] Responsive (mobile/tablette)

## Navigation et raccourcis

### Raccourcis clavier

- **Flèches** : Navigation entre slides
- **Espace** : Slide suivante
- **S** : Mode présentation (speaker notes)
- **F** : Plein écran
- **Esc** : Vue d'ensemble (aperçu)
- **B** / **.** : Écran noir (pause)

### Mode présentation (S)

Ouvre une fenêtre séparée avec :
- Slide actuelle
- Slide suivante (preview)
- Notes du présentateur
- Chronomètre
- Temps écoulé

## Fichiers produits

À la fin de l'exécution :

```
./
├── presentation.html     # Fichier HTML principal (présentation complète)
└── [assets/]            # Dossier optionnel pour images/médias
```

**Note** : Tout est dans un seul fichier HTML (CSS inline, JS inline, CDN pour reveal.js et MathJax)

## Rapport final

L'agent fournit un rapport détaillé :

```markdown
✅ PRÉSENTATION REVEAL.JS CRÉÉE AVEC SUCCÈS

Style           : Lycée
Sujet           : Dérivation des fonctions
Nombre de slides: 25
Durée estimée   : 55 minutes

📂 FICHIER PRODUIT

- presentation.html : Présentation complète (HTML + CSS + JS)

🎯 CARACTÉRISTIQUES

✓ Fragments pour révélation progressive
✓ MathJax intégré (formules mathématiques)
✓ Transitions élégantes (slide)
✓ 4 exercices avec estimation de temps
✓ Responsive design (mobile friendly)
✓ Mode présentation activé (touche S)
✓ Navigation clavier complète

📝 CONTENU

- 25 slides créées
- 4 exercices intégrés (5 min, 8 min, 5 min, 10 min)
- 15 formules mathématiques
- 6 sections thématiques
- Alternance pédagogique respectée

🚀 COMMENT UTILISER

1. Ouvrir presentation.html dans un navigateur moderne
2. Naviguer avec les flèches ou la barre espace
3. Appuyer sur S pour mode présentation
4. Appuyer sur Esc pour vue d'ensemble

Pour présentation professionnelle :
- Lancer un serveur local : python -m http.server 8000
- Ouvrir http://localhost:8000/presentation.html
- Passer en plein écran (F11 ou F)

✅ PRÊT À PRÉSENTER
```

## Notes importantes

1. **Navigateur moderne requis**
   - Chrome, Firefox, Safari, Edge (dernières versions)
   - JavaScript activé

2. **Connexion internet recommandée**
   - Pour CDN reveal.js et MathJax
   - Alternative : télécharger en local (fichiers lourds)

3. **Serveur local pour fonctionnalités avancées**
   - Certaines fonctionnalités nécessitent un serveur
   - `python -m http.server 8000` ou `npx http-server -p 8000`

4. **Responsive design**
   - Fonctionne sur mobile/tablette
   - Mode portrait et paysage supportés
   - Swipe pour naviguer

5. **Export PDF possible**
   - Ajouter `?print-pdf` à l'URL
   - Imprimer en PDF depuis le navigateur
   - Exemple : `presentation.html?print-pdf`

## Gestion des erreurs

### Si MathJax ne charge pas

L'agent vérifie :
1. CDN accessible
2. Plugin Math activé
3. Délimiteurs corrects (`\(...\)` et `\[...\]`)

### Si fragments ne fonctionnent pas

L'agent vérifie :
1. Classes correctes (`class="fragment"`)
2. Ordre logique (`data-fragment-index`)
3. Pas de conflits CSS

### Si responsive ne fonctionne pas

L'agent vérifie :
1. Balise meta viewport présente
2. Tailles de police adaptatives
3. Débordements de contenu

## Exemples complets

### Cas d'usage 1 : Enseignant pressé

```bash
/createReveals --sujet "Pythagore" --duree 30
```

**Processus** :
- Détection auto : collège (Pythagore = niveau 4e)
- 15 slides créées
- 2 exercices
- Création automatique
- HTML prêt en < 2 minutes

**Résultat** : Présentation complète sans intervention.

### Cas d'usage 2 : Cours structuré lycée

```bash
/createReveals --style lycée --sujet "Suites numériques" --duree 55 \
  --exercices 5 --auteur "Prof. Martin" --etablissement "Lycée Exemple"
```

**Processus** :
- Template lycée
- 25 slides avec 5 exercices répartis
- Métadonnées complétées
- MathJax intégré
- HTML prêt en < 3 minutes

**Résultat** : Cours complet 1h avec exercices intégrés.

### Cas d'usage 3 : Conférence recherche

```bash
/createReveals --style académique \
  --sujet "Convergence des schémas volumes finis" \
  --duree 45 --output "./seminaire_2025.html"
```

**Processus** :
- Template académique
- 30 slides (contexte, théorie, résultats, discussion, conclusion, refs)
- Sobre et professionnel
- HTML prêt en < 4 minutes

**Résultat** : Présentation académique professionnelle.

## Avantages reveal.js vs Beamer

### Avantages reveal.js

- ✅ Interactivité (navigation clavier, souris, tactile)
- ✅ Responsive (mobile, tablette)
- ✅ Mode présentation intégré (speaker notes)
- ✅ Vue d'ensemble (Esc)
- ✅ Aucun compilateur nécessaire
- ✅ Facilement partageable (URL)
- ✅ Animations CSS personnalisables
- ✅ Export PDF possible

### Avantages Beamer

- ✅ PDF natif (universellement compatible)
- ✅ Qualité typographique LaTeX
- ✅ Hors ligne complet
- ✅ Impression professionnelle
- ✅ Annotations PDF possibles

## IMPORTANT

**Cette commande est entièrement autonome.**

Une fois lancée :
1. L'agent reveals-creator prend en charge
2. Utilise le skill reveals-presentation
3. Crée, configure, teste
4. Produit un HTML prêt à présenter

**Aucune intervention manuelle nécessaire.**

---

**Utilisez /createReveals pour générer des présentations web interactives de qualité professionnelle en quelques minutes !**
