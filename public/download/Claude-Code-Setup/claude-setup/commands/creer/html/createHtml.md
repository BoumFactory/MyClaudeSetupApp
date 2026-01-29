# /createHtml - Création automatique de cours HTML/KaTeX

## Description

Crée automatiquement un projet de cours HTML interactif avec rendu mathématique KaTeX. Le fichier final est un HTML autonome fonctionnant 100% hors-ligne avec :
- Sélecteur d'univers visuel (8 styles disponibles)
- Mode clair/sombre (avec détection auto du système)
- Infobulles de vocabulaire interactives
- Formules mathématiques LaTeX rendues par KaTeX

## Usage

```
/createHtml <description_du_cours>
```

## Exemples d'utilisation

```bash
# Cours classique
/createHtml cours sur les vecteurs en seconde
→ Niveau: 2nde, Thème: vecteurs, Univers: standard

# Cours fun pour collège
/createHtml cours de géométrie en sixième style manga
→ Niveau: 6eme, Thème: geometrie, Univers: manga

# Cours avancé style tech
/createHtml cours sur l'analyse en terminale style futuriste
→ Niveau: tle, Thème: analyse, Univers: futuriste

# Cours minimaliste
/createHtml probabilités en première style minimal
→ Niveau: 1ere, Thème: probabilites, Univers: minimal
```

## Protocole d'exécution

### ÉTAPE 1 : ANALYSE DE LA REQUÊTE

Extraire de la description de l'utilisateur :

1. **Niveau** (obligatoire) :
   | Alias | ID |
   |-------|-----|
   | Sixième, 6ème, 6eme | `6eme` |
   | Cinquième, 5ème, 5eme | `5eme` |
   | Quatrième, 4ème, 4eme | `4eme` |
   | Troisième, 3ème, 3eme | `3eme` |
   | Seconde, 2nde, 2de | `2nde` |
   | Première, 1ère, 1ere | `1ere` |
   | Terminale, Term, Tle | `tle` |
   | Supérieur, Sup, BTS, Prépa | `sup` |

2. **Thème mathématique** (obligatoire) :
   | Thème | ID |
   |-------|-----|
   | Géométrie | `geometrie` |
   | Analyse, Fonctions, Dérivées | `analyse` |
   | Algèbre, Équations | `algebre` |
   | Probabilités | `probabilites` |
   | Statistiques | `statistiques` |
   | Arithmétique | `arithmetique` |
   | Trigonométrie | `trigonometrie` |
   | Nombres complexes | `complexes` |
   | Suites | `suites` |
   | Vecteurs | `vecteurs` |

3. **Univers graphique** (optionnel, défaut: `standard`) :
   | Alias | ID | Description |
   |-------|-----|-------------|
   | Classique, Standard, Normal | `standard` | Sobre, professionnel |
   | Minimal, Épuré | `minimal` | Beaucoup de blanc |
   | Cahier, Paper | `paper` | Effet cahier avec lignes |
   | Nature, Naturel | `nature` | Tons terreux, organique |
   | Retro, Vintage | `retro` | Sépia, typographie ancienne |
   | Manga, Dynamique | `manga` | Badges colorés, ombres |
   | Futuriste, Cyber, Tech | `futuriste` | Dark mode, néon |
   | Gaming, Gamer, RGB | `gaming` | Énergique, contrasté |

4. **Titre** : Extraire ou générer un titre approprié.

### ÉTAPE 2 : DÉTERMINATION DE L'EMPLACEMENT

Structure recommandée :
```
1. Cours/
└── [niveau]/
    └── Sequence-[theme]/
        └── Cours_HTML/
            └── [nom-projet]/
                ├── parts/
                │   └── 01-introduction.html
                ├── config.json
                └── output/
```

Proposer l'emplacement à l'utilisateur :
```
Je vais créer le projet HTML/KaTeX :
  Titre: "Les Vecteurs du Plan"
  Niveau: Seconde (2nde)
  Thème: vecteurs
  Univers: standard

📁 Emplacement proposé : 1. Cours/2nde/Sequence-Vecteurs/Cours_HTML/vecteurs-seconde/

Cela vous convient-il ?
```

### ÉTAPE 3 : INITIALISATION DU PROJET

Exécuter le script d'initialisation :

```bash
python ".claude/skills/creer/html/html-katex-compiler/scripts/init_project.py" "<chemin>" --titre "<titre>" --niveau <niveau> --theme <theme> --univers <univers>
```

### ÉTAPE 4 : ÉDITION DU CONTENU

Utiliser le skill `html-cours-editor` pour éditer les fichiers `parts/*.html`.

Le contenu doit être structuré avec :
- Titres `<h2>`, `<h3>` pour la structure
- Blocs pédagogiques : `.definition`, `.theoreme`, `.propriete`, `.exemple`, `.methode`, `.remarque`, `.exercice`
- Formules LaTeX : `$...$` (inline) et `$$...$$` (display)
- Vocabulaire interactif : `<span class="vocab" data-definition="...">mot</span>`

### ÉTAPE 5 : COMPILATION

Compiler le projet en fichier HTML autonome :

```bash
python ".claude/skills/creer/html/html-katex-compiler/scripts/compile_project.py" "<chemin>"
```

Le fichier compilé sera dans `output/[titre]-ONEFILE.html`.

### ÉTAPE 6 : VÉRIFICATION

Annoncer la création et les fonctionnalités :
```
✅ Projet HTML/KaTeX créé !

📁 Fichiers :
  - parts/01-introduction.html (à éditer)
  - config.json (configuration)
  - output/[titre]-ONEFILE.html (fichier final)

🎨 Fonctionnalités :
  - Sélecteur d'univers (⚙️ en haut à droite)
  - Mode clair/sombre
  - Infobulles de vocabulaire
  - Fonctionne 100% hors-ligne

Voulez-vous que j'édite le contenu maintenant ?
```

## Skill utilisé

- `html-katex-compiler` : Initialisation, édition et compilation

## Différences avec /createTex

| Aspect | /createTex | /createHtml |
|--------|-----------|-------------|
| Format | PDF via LaTeX | HTML autonome |
| Interactivité | Statique | Dynamique (sélecteur, dark mode) |
| Compilation | pdflatex/lualatex | Script Python |
| Usage | Impression, documents officiels | Projection, consultation web |
| Hors-ligne | Oui (PDF) | Oui (HTML embarqué) |

## Quand utiliser /createHtml vs /createTex ?

| Situation | Recommandation |
|-----------|---------------|
| Projection en classe | `/createHtml` |
| Document à imprimer | `/createTex` |
| Cours interactif | `/createHtml` |
| Évaluation officielle | `/createTex` |
| Consultation sur tablette | `/createHtml` |
| Archive pédagogique | `/createTex` |
