---
name: tex-fiche-technique
description: Creer des fiches techniques pedagogiques au format LaTeX a partir de ressources educatives (cours, exercices, activites). Propose deux formats adaptes selon le destinataire (inspecteurs ou collegues). Utiliser ce skill pour documenter et valoriser des ressources pedagogiques.
---

# Skill : Creation de Fiches Techniques Pedagogiques LaTeX

## Description

Ce skill genere des fiches techniques professionnelles pour documenter des ressources pedagogiques. Il produit des documents LaTeX structures avec deux niveaux de formalisme selon le destinataire.

## Quand utiliser ce skill

- Documenter une ressource pedagogique pour inspection
- Partager une ressource avec des collegues avec explications detaillees
- Creer un document de presentation pour une sequence pedagogique
- Justifier les choix didactiques d'une ressource

---

## REGLE OBLIGATOIRE : Integration programmes-officiels

**TOUJOURS utiliser le skill `programmes-officiels`** pour sourcer les competences.

### Workflow obligatoire

1. **Analyser la ressource** pour identifier niveau et theme
2. **Lancer une recherche** avec le script de programmes-officiels
3. **Integrer les competences** trouvees dans la fiche technique

### Exemple de recherche

```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026"
python ".claude/skills/programmes-officiels/scripts/search_competences.py" --niveau 1S --keyword "suite" --format json
```

### Resultat attendu

Les competences trouvees sont integrees dans :
- Section "References au Bulletin Officiel" (format inspecteur)
- Section "Lien avec le programme" (format collegues)

Chaque competence citee doit inclure :
- Le code normalise (ex: `1SY16`)
- L'intitule exact du programme
- La source PDF et page d'origine

---

## Templates disponibles

### 1. Format Inspecteur (officiel, academique)

**Fichier :** `assets/templates/fiche-technique-inspecteur.tex`

**Caracteristiques :**
- En-tete officiel avec logo Republique Francaise
- Format academique sobre et professionnel
- Structure complete en 10 sections
- Citations sourcees des programmes officiels (BO)
- Mention "Document confidentiel"
- Compilation avec **lualatex** (pour support SVG du logo)

**Quand l'utiliser :**
- Documents pour inspection
- Presentations institutionnelles
- Dossiers de candidature (agregation, certifications)
- Communication avec la hierarchie

**Sections incluses :**
1. Presentation de la ressource
2. Objectifs pedagogiques (connaissances, competences, capacites)
3. Inscription dans les programmes officiels (BO, socle commun)
4. Activites prevues des eleves
5. Prerequis (mathematiques et methodologiques)
6. Modalites de mise en oeuvre (duree, organisation, materiel)
7. Choix didactiques et pedagogiques (justification, differenciation, difficultes)
8. Evaluation des acquis
9. Prolongements possibles
10. Bibliographie et ressources

### 2. Format Collegues/Personnel (sobre, pratique)

**Fichier :** `assets/templates/fiche-technique-collegues.tex`

**Caracteristiques :**
- Format compact et lisible (vise 1-2 pages)
- Pas de logo officiel
- En-tete simplifie
- Sections concises et pratiques
- Espace pour notes personnelles
- Compilation avec **pdflatex** ou **lualatex**

**Quand l'utiliser :**
- Partage entre collegues
- Notes personnelles d'organisation
- Documentation interne d'equipe
- Mutualisation de ressources

**Sections incluses :**
1. En bref (resume)
2. Objectifs (notions et competences)
3. Ce que font les eleves
4. Prerequis
5. Deroulement
6. Points d'attention (difficultes, differenciation)
7. Conseils pratiques (optionnel)
8. Lien avec le programme
9. Prolongements possibles
10. Notes personnelles

---

## Workflow de creation

### Etape 1 : Analyse de la ressource

1. **Lire la ressource pedagogique complete** (fichier .tex principal et sections/enonce.tex)
2. **Identifier** :
   - Type de ressource (cours, exercices, activite, evaluation)
   - Niveau et theme
   - Structure et organisation
   - Notions mathematiques abordees

### Etape 2 : Recherche des competences (OBLIGATOIRE)

**Utiliser le skill `programmes-officiels`** pour recuperer les competences liees au contenu.

```bash
# Exemple pour des exercices sur les suites en 1ere Spe
python ".claude/skills/programmes-officiels/scripts/search_competences.py" \
    --niveau 1S \
    --keyword "suite" \
    --format json \
    --limit 30
```

**Conserver pour la fiche :**
- Les codes des competences pertinentes (ex: `1SY16`, `1SY17`)
- Les intitules exacts
- Les sources (PDF + page)

### Etape 3 : Extraction des informations

#### Objectifs pedagogiques
- **Connaissances** : Notions introduites/consolidees
- **Competences** : Competences mathematiques developpees
- **Capacites** : Ce que les eleves doivent savoir faire

#### Activites des eleves
- Que font concretement les eleves ?
- Quelles taches sont demandees ?
- Quelle autonomie est attendue ?

#### Prerequisites
- **Mathematiques** : Notions prealables
- **Methodologiques** : Methodes maitrisees

#### Lien avec le programme (alimente par programmes-officiels)
- References exactes au BO avec codes normalises
- Competences du socle commun (college)
- Competences mathematiques travaillees (chercher, modeliser, etc.)

#### Modalites pratiques
- Duree estimee totale et par partie
- Organisation de classe recommandee
- Materiel necessaire

### Etape 4 : Selection du template

| Destinataire | Template |
|--------------|----------|
| Inspecteur | `assets/templates/fiche-technique-inspecteur.tex` |
| Collegues | `assets/templates/fiche-technique-collegues.tex` |
| Personnel | `assets/templates/fiche-technique-collegues.tex` |

### Etape 5 : Remplissage du template

1. **Copier le template** dans le repertoire de la ressource
2. **Nommer le fichier** : `Fiche_technique_[NomRessource].tex`
3. **Remplacer les variables** `%VARIABLE%` (voir `references/variables-templates.md`)
4. **Integrer les competences** trouvees via programmes-officiels

### Etape 6 : Compilation

**Format Inspecteur :**
```bash
lualatex -synctex=1 -interaction=nonstopmode -shell-escape "Fiche_technique_[nom].tex"
```

**Format Collegues :**
```bash
pdflatex -interaction=nonstopmode "Fiche_technique_[nom].tex"
```

---

## Conseils de redaction

### Pour le format Inspecteur

- **Ton** : Formel, academique, professionnel
- **Vocabulaire** : Utiliser le vocabulaire institutionnel
- **Citations** : Toujours sourcer les references au BO avec precision
- **Justification** : Expliquer tous les choix pedagogiques
- **Completude** : Remplir toutes les sections sans exception

### Pour le format Collegues

- **Ton** : Pratique, direct, amical
- **Concision** : Aller a l'essentiel
- **Conseils** : Partager des astuces concretes
- **Flexibilite** : Sections optionnelles omissibles
- **Lisibilite** : Privilegier les listes a puces

---

## Integration avec d'autres skills

| Skill | Usage |
|-------|-------|
| **programmes-officiels** | OBLIGATOIRE - Sourcer les references au BO |
| **bfcours-latex** | Analyser le contenu LaTeX des ressources |
| **tex-compiling-skill** | Compiler les fiches techniques |

---

## Structure du skill

```
tex-fiche-technique/
├── SKILL.md                           # Ce fichier
├── assets/
│   └── templates/
│       ├── fiche-technique-inspecteur.tex   # Template format officiel
│       ├── fiche-technique-collegues.tex    # Template format pratique
│       └── modele_fiche_technique.tex       # Modele generique (legacy)
├── references/
│   └── variables-templates.md         # Liste des variables a remplacer
└── scripts/                           # (reserve pour futurs scripts)
```

---

## Notes importantes

- Le logo Republique Francaise est dans `.claude/datas/latex-modeles/logo-republique-francaise.png`
- Le format inspecteur necessite **lualatex** pour le support SVG
- Les deux templates sont compatibles impression noir et blanc
- Les fiches doivent etre autonomes et compilables sans dependances complexes
