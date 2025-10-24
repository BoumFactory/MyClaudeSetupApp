---
name: tex-fiche-technique
description: Créer des fiches techniques pédagogiques au format LaTeX à partir de ressources éducatives (cours, exercices, activités). Propose deux formats adaptés selon le destinataire (inspecteurs ou collègues). Utiliser ce skill pour documenter et valoriser des ressources pédagogiques.
---

# Skill : Création de Fiches Techniques Pédagogiques LaTeX

## Description

Skill spécialisé dans la génération de fiches techniques professionnelles pour documenter des ressources pédagogiques (cours, exercices, évaluations, activités). Produit des documents LaTeX structurés avec deux niveaux de formalisme selon le destinataire.

## Quand utiliser ce skill

Utiliser ce skill lorsqu'il faut :
- Documenter une ressource pédagogique pour inspection
- Partager une ressource avec des collègues avec explications détaillées
- Créer un document de présentation pour une séquence pédagogique
- Justifier les choix didactiques d'une ressource

## Templates disponibles

Deux templates LaTeX sont disponibles selon le destinataire :

### 1. Format Inspecteur (officiel, académique)

**Fichier :** `C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/.claude/datas/latex-modeles/fiche-technique-inspecteur.tex`

**Caractéristiques :**
- En-tête officiel avec logo République Française
- Format académique sobre et professionnel
- Structure complète en 10 sections
- Citations sourcées des programmes officiels (BO)
- Mention "Document confidentiel"
- Compilation avec **lualatex** (pour support SVG du logo)

**Quand l'utiliser :**
- Documents pour inspection
- Présentations institutionnelles
- Dossiers de candidature (agrégation, certifications)
- Communication avec la hiérarchie

**Sections incluses :**
1. Présentation de la ressource
2. Objectifs pédagogiques (connaissances, compétences, capacités)
3. Inscription dans les programmes officiels (BO, socle commun)
4. Activités prévues des élèves
5. Prérequis (mathématiques et méthodologiques)
6. Modalités de mise en œuvre (durée, organisation, matériel)
7. Choix didactiques et pédagogiques (justification, différenciation, difficultés)
8. Évaluation des acquis
9. Prolongements possibles
10. Bibliographie et ressources

### 2. Format Collègues/Personnel (sobre, pratique)

**Fichier :** `C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/.claude/datas/latex-modeles/fiche-technique-collegues.tex`

**Caractéristiques :**
- Format compact et lisible (vise 1-2 pages)
- Pas de logo officiel
- En-tête simplifié
- Sections concises et pratiques
- Espace pour notes personnelles
- Compilation avec **pdflatex** ou **lualatex**

**Quand l'utiliser :**
- Partage entre collègues
- Notes personnelles d'organisation
- Documentation interne d'équipe
- Mutualisation de ressources

**Sections incluses :**
1. En bref (résumé)
2. Objectifs (notions et compétences)
3. Ce que font les élèves
4. Prérequis
5. Déroulement
6. Points d'attention (difficultés, différenciation)
7. Conseils pratiques (optionnel)
8. Lien avec le programme
9. Prolongements possibles
10. Notes personnelles

## Workflow de création

### Étape 1 : Analyse de la ressource

Avant de créer la fiche technique :

1. **Lire la ressource pédagogique complète** (fichier .tex principal et sections/enonce.tex)
2. **Identifier** :
   - Type de ressource (cours, exercices, activité, évaluation)
   - Niveau et thème
   - Structure et organisation
   - Notions mathématiques abordées
   - Niveau de difficulté des exercices/activités

### Étape 2 : Extraction des informations

Pour remplir chaque section de la fiche :

#### Objectifs pédagogiques
- **Connaissances** : Quelles notions sont introduites/consolidées ?
- **Compétences** : Quelles compétences mathématiques sont développées ?
- **Capacités** : Que doivent savoir faire les élèves concrètement ?

#### Activités des élèves
- Que font concrètement les élèves ?
- Quelles sont les tâches demandées ?
- Quelle autonomie est attendue ?
- Quels types de raisonnement sont mobilisés ?

#### Prérequis
- **Mathématiques** : Quelles notions doivent être acquises avant ?
- **Méthodologiques** : Quelles méthodes doivent être maîtrisées ?

#### Lien avec le programme
- **Utiliser le skill `programmes-officiels`** pour sourcer les références au BO
- Citer précisément les extraits pertinents du programme officiel
- Relier aux compétences du socle commun (collège)
- Identifier les compétences mathématiques travaillées

#### Modalités pratiques
- Durée estimée totale et par partie
- Organisation de classe recommandée (individuel, binômes, groupes, classe entière)
- Matériel nécessaire (calculatrice, logiciels, matériel de géométrie, etc.)
- Supports (fiches, vidéoprojecteur, etc.)

#### Choix didactiques
- Pourquoi cette approche pédagogique ?
- Comment différencier (aide, approfondissement) ?
- Quelles difficultés anticiper ?
- Quels points de vigilance ?

### Étape 3 : Sélection du template

Choisir le template selon le destinataire :

```
Destinataire : Inspecteur → fiche-technique-inspecteur.tex
Destinataire : Collègues   → fiche-technique-collegues.tex
Destinataire : Personnel   → fiche-technique-collegues.tex
```

### Étape 4 : Remplissage du template

1. **Copier le template** dans le même répertoire que la ressource
2. **Nommer le fichier** : `Fiche_technique_[NomRessource].tex`
3. **Remplacer toutes les variables** `%VARIABLE%` par les valeurs réelles
4. **Remplir chaque section** avec le contenu extrait et analysé
5. **Vérifier la cohérence** et l'exhaustivité

### Étape 5 : Compilation

**Pour le format Inspecteur :**
```bash
lualatex -synctex=1 -interaction=nonstopmode -shell-escape "Fiche_technique_[nom].tex"
```

**Pour le format Collègues :**
```bash
pdflatex -interaction=nonstopmode "Fiche_technique_[nom].tex"
```

Puis vérifier le PDF généré et corriger les erreurs éventuelles.

## Variables des templates

### Variables communes aux deux formats

- `%TITRE_RESSOURCE%` : Titre complet de la ressource
- `%NIVEAU%` : Niveau (ex: 1ère Spécialité, 3ème, 2nde)
- `%THEME%` : Thème mathématique principal
- `%TYPE_RESSOURCE%` : Type (Cours, Exercices, Activité, Évaluation, etc.)
- `%DUREE%` : Durée estimée
- `%AUTEUR%` : Nom de l'enseignant
- `%DATE%` : Date de création (format : \today ou date explicite)
- `%ANNEE_SCOLAIRE%` : Année scolaire (ex: 2025-2026)

### Variables spécifiques au format Inspecteur

En-tête :
- `%ACADEMIE%` : Académie (ex: Reims)
- `%TYPE_ETABLISSEMENT%` : Type (Lycée, Collège)
- `%NOM_ETABLISSEMENT%` : Nom de l'établissement

Sections détaillées :
- `%PRESENTATION%` : Présentation générale de la ressource
- `%CONNAISSANCES%` : Liste des connaissances visées
- `%COMPETENCES%` : Liste des compétences développées
- `%CAPACITES%` : Liste des capacités travaillées
- `%REFERENCES_BO%` : Citations exactes du BO avec références
- `%COMPETENCES_SOCLE%` : Compétences du socle commun (collège)
- `%COMPETENCES_MATHS%` : Compétences mathématiques (chercher, modéliser, etc.)
- `%ACTIVITES_ELEVES%` : Description des activités des élèves
- `%PREREQUIS_MATHS%` : Prérequis mathématiques
- `%PREREQUIS_METHODO%` : Prérequis méthodologiques
- `%DUREE_TOTALE%` : Durée totale et découpage
- `%ORGANISATION%` : Type d'organisation (individuel, groupes, etc.)
- `%MATERIEL%` : Matériel nécessaire
- `%SUPPORTS%` : Supports utilisés
- `%DEROULEMENT%` : Déroulement détaillé de la séance
- `%JUSTIFICATION_PEDAGOGIQUE%` : Justification des choix pédagogiques
- `%DIFFERENCIATION%` : Stratégies de différenciation
- `%DIFFICULTES%` : Difficultés anticipées
- `%MODALITES_EVALUATION%` : Modalités d'évaluation
- `%CRITERES_REUSSITE%` : Critères de réussite
- `%PROLONGEMENTS%` : Prolongements possibles
- `%BIBLIOGRAPHIE%` : Bibliographie et ressources

### Variables spécifiques au format Collègues

- `%TITRE_COURT%` : Titre court pour en-tête
- `%RESUME%` : Résumé en 2-3 phrases
- `%NOTIONS%` : Liste des notions travaillées
- `%ORGANISATION%` : Organisation de classe
- `%MATERIEL%` : Matériel nécessaire
- `%PREREQUIS%` : Prérequis (version concise)
- `%DEROULEMENT%` : Déroulement (version concise)
- `%CONSEILS_PRATIQUES%` : Conseils pratiques (optionnel)
- `%LIEN_PROGRAMME%` : Lien avec le programme (version concise)

## Conseils de rédaction

### Pour le format Inspecteur

- **Ton** : Formel, académique, professionnel
- **Vocabulaire** : Utiliser le vocabulaire institutionnel approprié
- **Citations** : Toujours sourcer les références au BO avec précision (numéro, date)
- **Justification** : Expliquer et justifier tous les choix pédagogiques et didactiques
- **Rigueur** : Être exhaustif et précis
- **Complétude** : Remplir toutes les sections sans exception
- **Cohérence** : Assurer la cohérence entre objectifs, activités et évaluation

### Pour le format Collègues

- **Ton** : Pratique, direct, amical
- **Concision** : Aller à l'essentiel, éviter les longueurs
- **Conseils** : Partager des astuces concrètes et testées
- **Flexibilité** : Les sections optionnelles peuvent être omises
- **Honnêteté** : Mentionner les points d'attention réels et les difficultés rencontrées
- **Lisibilité** : Privilégier les listes à puces aux paragraphes longs

## Intégration avec d'autres skills

Ce skill s'intègre avec :

- **`programmes-officiels`** : Pour sourcer les références aux BO et aux compétences officielles
- **`bfcours-latex`** : Pour analyser le contenu LaTeX des ressources
- **`tex-compiling-skill`** : Pour compiler les fiches techniques

## Notes importantes

- Le logo République Française est situé dans `.claude/datas/latex-modeles/logo-republique-francaise.png`
- La compilation du format inspecteur nécessite **lualatex** pour le support SVG
- Le format collègues peut être compilé avec **pdflatex** ou **lualatex**
- Les deux templates utilisent des couleurs sobres adaptées à l'impression noir et blanc
- Les fiches doivent être autonomes et compilables sans dépendances complexes

## Exemple de nommage

Pour des exercices sur le produit scalaire en 1ère spécialité :

```
Fiche_technique_Exercices_Produit_scalaire.tex
```

Pour un cours sur les fonctions affines en 2nde :

```
Fiche_technique_Cours_Fonctions_affines.tex
```
