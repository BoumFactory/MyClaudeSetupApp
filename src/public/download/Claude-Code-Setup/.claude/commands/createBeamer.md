# /createBeamer - Création de diaporamas Beamer de haute qualité

## Description

Crée automatiquement un diaporama Beamer pédagogique de haute qualité adapté au contexte (collège, lycée, académique). Gère la création, compilation, vérification visuelle et nettoyage de manière autonome via l'agent beamer-worker.

## Philosophie

**PRINCIPE FONDAMENTAL** : Produire une présentation **complète**, **lisible** et **sans bugs visuels**, prête à être utilisée en classe ou en conférence.

Le système :
- Analyse le public cible et choisit le style approprié
- Crée le contenu avec alternance pédagogique question/réponse
- Respecte les règles de densité et d'espacement
- Compile avec LuaLaTeX
- Vérifie visuellement chaque frame
- Corrige les bugs détectés
- Nettoie les fichiers temporaires

## Usage

```
/createBeamer [--style <collège|lycée|académique>] --sujet "<sujet>" --duree <minutes> [--output <chemin>]
```

## Paramètres

- `--style <collège|lycée|académique>` : Style de présentation (optionnel, détecté automatiquement si non spécifié)
  - `collège` : Pour classes de 6e à 3e (couleurs vives, police 14pt, animations fréquentes)
  - `lycée` : Pour classes de 2nde à Terminale (équilibré, police 12pt)
  - `académique` : Pour conférences, colloques (sobre, police 11pt, format 16:9)

- `--sujet "<sujet>"` : Sujet de la présentation (obligatoire)
  - Exemples : "Les nombres relatifs", "Dérivation des fonctions", "Analyse spectrale"

- `--duree <minutes>` : Durée approximative de la présentation (obligatoire)
  - Utilisé pour estimer le nombre de slides (durée ÷ 2-3 min)

- `--output <chemin>` : Chemin de sortie (optionnel, défaut: `./presentation.tex`)

- `--exercices <nombre>` : Nombre d'exercices souhaités (optionnel, défaut: auto selon durée)

- `--auteur "<nom>"` : Nom de l'auteur (optionnel)

- `--etablissement "<nom>"` : Nom de l'établissement (optionnel)

## Workflow

L'agent beamer-worker est appelé avec les skills :
- **beamer-presentation** : Expertise Beamer complète
- **tex-compiling-skill** : Compilation avec LuaLaTeX
- **pdf** : Extraction et vérification visuelle des frames

### Étapes automatiques

1. **Analyse de la demande**
   - Identifier le style selon le public ou paramètre `--style`
   - Extraire sujet, durée, nombre de slides estimé
   - Choisir le template approprié

2. **Création du contenu**
   - Copier le template (collège/lycée/académique)
   - Remplir les métadonnées
   - Structurer le contenu :
     - Titre + plan
     - Sections thématiques
     - Exercices avec estimation de temps
     - Alternance question/réponse
     - Conclusion
   - Respecter les règles de densité (60% collège, 70% lycée/académique)

3. **Compilation**
   - Compiler avec skill `tex-compiling-skill`
   - Profil `lualatex_reims_favorite`
   - Analyser et corriger les erreurs si échec
   - Recompiler jusqu'à succès

4. **Vérification visuelle**
   - Extraire toutes les frames en PNG (skill `pdf`)
   - Vérifier chaque frame :
     - Densité < seuil (60% ou 70%)
     - Lisibilité (police, contraste)
     - Graphiques complets
     - Formules non tronquées
   - Détecter les bugs visuels

5. **Correction des bugs**
   - Pour chaque bug détecté :
     - Localiser le code LaTeX
     - Appliquer la correction (découpage, réduction, reformulation)
     - Recompiler
     - Vérifier la correction
   - Continuer jusqu'à 0 bug

6. **Nettoyage**
   - Supprimer les frames PNG (`./verification_frames/`)
   - Nettoyer les fichiers de compilation (`.aux`, `.log`, etc.)
   - Conserver uniquement le PDF final

7. **Rapport final**
   - Résumé de la présentation
   - Nombre de slides
   - Exercices intégrés
   - Vérifications effectuées

## Exemples d'utilisation

### Exemple 1 : Présentation collège automatique

```bash
/createBeamer --sujet "Les nombres relatifs" --duree 20
```

**Résultat** :
- Style détecté : collège (sujet adapté à ce niveau)
- Template : `template-college.tex`
- 11 slides créées (20 min ÷ 2 min/slide)
- 2 exercices intégrés
- Police 14pt, couleurs vives
- Densité < 60%
- PDF prêt : `presentation.pdf`

### Exemple 2 : Cours lycée

```bash
/createBeamer --style lycée --sujet "Dérivation des fonctions" --duree 55 \
  --auteur "M. Dupont" --etablissement "Lycée Eugène Belgrand"
```

**Résultat** :
- Style : lycée
- Template : `template-lycee.tex`
- 25 slides créées (55 min = 1h de cours)
- 4 exercices intégrés avec estimation de temps
- Métadonnées remplies
- Densité < 70%
- PDF prêt : `presentation.pdf`

### Exemple 3 : Conférence académique

```bash
/createBeamer --style académique --sujet "Analyse spectrale des opérateurs compacts" \
  --duree 30 --output "./conference_2025.tex"
```

**Résultat** :
- Style : académique
- Template : `template-academique.tex`
- Format 16:9
- 23 slides créées (30 min de présentation)
- Sections : Contexte, Théorie, Résultats, Discussion, Conclusion, Références
- Sobre, professionnel
- PDF prêt : `conference_2025.pdf`

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

- **Police** : 14pt (titres 20pt)
- **Densité max** : 60%
- **Items/slide** : 5 max
- **Lignes** : 8 max
- **Animations** : Fréquentes (`\pause`, `\uncover`)
- **Couleurs** : Vives (bleu, orange, rouge, vert)
- **Exercices** : Interactifs, ludiques
- **Slides/heure** : 15-20

### Lycée

- **Police** : 12pt (titres 16-18pt)
- **Densité max** : 70%
- **Items/slide** : 6-7 max
- **Lignes** : 10-12 max
- **Animations** : Modérées
- **Couleurs** : Équilibrées (bleu marine, bordeaux)
- **Exercices** : Guidés, appliqués
- **Slides/heure** : 25-35

### Académique

- **Police** : 11pt (titres 14-16pt)
- **Densité max** : 70%
- **Items/slide** : 7 max
- **Lignes** : 12-14 max
- **Animations** : Rares
- **Couleurs** : Sobres (noir, gris)
- **Format** : 16:9
- **Références** : Bibliographie obligatoire
- **Slides/heure** : 40-60

## Skills et agent utilisés

### Agent : beamer-worker

**Modèle** : `claude-haiku-4-5-20251001` (rapide et efficace)

**Autonomie** : Totale (pas d'intervention utilisateur nécessaire)

**Responsabilités** :
- Création du contenu complet
- Compilation et gestion des erreurs
- Vérification visuelle exhaustive
- Correction des bugs
- Nettoyage final

### Skills

1. **beamer-presentation**
   - Guides de référence (best practices, styles, exercices, workflow)
   - Règles de densité et espacement
   - Environnements Beamer (blocks, colonnes, TikZ)
   - Estimation des temps pour exercices

2. **tex-compiling-skill**
   - Compilation avec LuaLaTeX
   - Analyse des erreurs de compilation
   - Nettoyage des fichiers auxiliaires

3. **pdf**
   - Extraction des pages (frames) en images PNG
   - Permet la vérification visuelle par l'agent

## Vérifications effectuées

Avant de valider la présentation, l'agent vérifie :

### Contenu

- [ ] Toutes les métadonnées renseignées
- [ ] Structure cohérente (titre, plan, sections, conclusion)
- [ ] Alternance question/réponse respectée
- [ ] Exercices avec temps estimé

### Visuel

- [ ] Chaque slide < densité maximale (60% ou 70%)
- [ ] Police ≥ taille minimale (11pt, 12pt, 14pt)
- [ ] Couleurs cohérentes avec le thème
- [ ] Contraste suffisant
- [ ] Formules mathématiques correctes et non tronquées
- [ ] Graphiques complets et lisibles

### Technique

- [ ] Compilation sans erreur
- [ ] Animations/overlays fonctionnels
- [ ] PDF généré et testé
- [ ] Fichiers temporaires nettoyés

## Gestion des erreurs

### Si compilation échoue

L'agent :
1. Analyse le log de compilation
2. Identifie l'erreur (ligne, type)
3. Applique la correction appropriée
4. Recompile
5. Répète jusqu'à succès

### Si bug visuel détecté

L'agent :
1. Identifie la frame problématique
2. Détermine le type de bug (densité, débordement, contraste, etc.)
3. Applique la correction (découpage, réduction, reformulation)
4. Recompile
5. Vérifie la correction
6. Passe à la frame suivante

**Aucune intervention manuelle requise.**

## Fichiers produits

À la fin de l'exécution :

```
./
├── presentation.tex      # Source LaTeX
├── presentation.pdf      # Document final (SEUL FICHIER CONSERVÉ)
└── [fichiers temporaires supprimés]
```

Fichiers nettoyés automatiquement :
- `presentation.aux`, `.log`, `.nav`, `.out`, `.snm`, `.toc`, `.synctex.gz`
- `./verification_frames/` (images PNG d'extraction)

## Rapport final

L'agent fournit un rapport détaillé :

```markdown
✅ PRÉSENTATION BEAMER CRÉÉE AVEC SUCCÈS

Style           : Lycée
Sujet           : Dérivation des fonctions
Nombre de slides: 25
Durée estimée   : 55 minutes

📂 FICHIERS PRODUITS

- presentation.pdf : Document final prêt à l'emploi

🎯 VÉRIFICATIONS EFFECTUÉES

✓ Compilation réussie (LuaLaTeX)
✓ 25 frames vérifiées visuellement
✓ Densité respectée (< 70%)
✓ Aucun bug visuel détecté
✓ Animations fonctionnelles
✓ 4 exercices avec estimation de temps
✓ Fichiers temporaires nettoyés

📝 CARACTÉRISTIQUES

- 4 exercices intégrés (5 min, 8 min, 5 min, 10 min)
- 6 questions/réponses interactives
- 3 graphiques TikZ
- Alternance pédagogique respectée

✅ PRÊT À PRÉSENTER
```

## Notes importantes

1. **Durée ≠ nombre de slides exact**
   - L'agent estime 1 slide = 2-3 minutes
   - Ajuste selon le contenu (exercices = plus de temps)

2. **Style peut être remplacé automatiquement**
   - Si le sujet ne correspond pas au style demandé
   - Exemple : Style "académique" + sujet "tables de multiplication" → style collège

3. **Exercices adaptés au niveau**
   - Collège : Application directe, ludique
   - Lycée : Guidé, plusieurs étapes
   - Académique : Optionnel, peut être remplacé par exemple théorique

4. **Vérification visuelle exhaustive**
   - Chaque frame est extraite et lue par l'agent
   - Garantit 0 bug visuel dans le résultat final

5. **Nettoyage obligatoire**
   - Les images PNG (potentiellement nombreuses) sont supprimées
   - Espace utilisateur non pollué

## Exemples complets

### Cas d'usage 1 : Enseignant pressé

```bash
/createBeamer --sujet "Pythagore" --duree 30
```

**Processus** :
- Détection auto : collège (Pythagore = niveau 4e)
- 15 slides créées
- 2 exercices
- Compilation + vérification automatique
- PDF prêt en < 2 minutes

**Résultat** : Présentation complète sans intervention.

### Cas d'usage 2 : Cours structuré lycée

```bash
/createBeamer --style lycée --sujet "Suites numériques" --duree 55 \
  --exercices 5 --auteur "Prof. Martin" --etablissement "Lycée Jamyn"
```

**Processus** :
- Template lycée
- 25 slides avec 5 exercices répartis
- Métadonnées complétées
- Vérification exhaustive
- PDF prêt en < 3 minutes

**Résultat** : Cours complet 1h avec exercices intégrés.

### Cas d'usage 3 : Conférence recherche

```bash
/createBeamer --style académique \
  --sujet "Convergence des schémas volumes finis" \
  --duree 45 --output "./seminaire_2025.tex"
```

**Processus** :
- Template académique (16:9)
- 30 slides (contexte, théorie, résultats, discussion, conclusion, refs)
- Vérification sobriété et professionnalisme
- PDF prêt en < 4 minutes

**Résultat** : Présentation académique professionnelle.

## IMPORTANT

**Cette commande est entièrement autonome.**

Une fois lancée :
1. L'agent beamer-worker prend en charge
2. Utilise les 3 skills (beamer-presentation, tex-compiling-skill, pdf)
3. Crée, compile, vérifie, corrige, nettoie
4. Produit un PDF prêt à l'emploi

**Aucune intervention manuelle nécessaire.**

---

**Utilisez /createBeamer pour générer des diaporamas Beamer de qualité professionnelle en quelques minutes !**
