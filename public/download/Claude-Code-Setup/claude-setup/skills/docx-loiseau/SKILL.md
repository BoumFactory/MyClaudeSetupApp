---
name: docx-loiseau
description: >
  Génération de documents DOCX pédagogiques mathématiques dans le style graphique F. Loiseau
  (Collège Marie Curie de Troyes). Ce skill devrait être utilisé pour créer des fiches méthodes,
  fiches d'exercices, évaluations et cours au format Word (.docx) avec le style Loiseau :
  bannières dégradées noir→gris, environnements didactiques avec label vertical noir,
  grilles Séyès pour réponses élèves, badge niveau violet, formules LaTeX converties en OMML.
  Pipeline bidirectionnel JSON ↔ DOCX pour itération facile.
---

# Skill DOCX Style Loiseau

Créer des documents Word (.docx) pédagogiques de mathématiques reproduisant fidèlement
le style graphique de F. Loiseau. Le workflow repose sur un pipeline JSON → DOCX (et DOCX → JSON
pour itération).

## Prérequis

Le venv Python du projet doit contenir : `python-docx`, `lxml`, `latex2mathml`, `Pillow`.
Les polices Windows requises : Cooper, Cooper Black, Arial Rounded MT Bold, Cambria, Wingdings.
Le fichier XSLT `MML2OMML.XSL` doit être présent (installé avec Microsoft Office).

## Workflow

### 1. Élaborer le JSON de description du document

Construire un fichier JSON structuré décrivant le document. Consulter
`references/json_schema.md` pour le schéma complet. Le JSON est volontairement léger
pour ne pas exploser le contexte des agents.

### 2. Générer le DOCX via le script

```bash
python ".claude/skills/docx-loiseau/scripts/generate_docx.py" chemin/vers/document.json
```

Le script :
- Lit le JSON
- Génère le DOCX avec tous les styles Loiseau
- **Ajoute automatiquement des spacers (2pt)** entre les composants majeurs — ne pas en mettre dans le JSON
- Exporte en PDF via Word COM ou LibreOffice
- Produit la version élève ET la version corrigée automatiquement

### 3. Itérer (optionnel)

Pour récupérer le contenu d'un DOCX existant en JSON (après modifications manuelles) :

```bash
python ".claude/skills/docx-loiseau/scripts/docx_to_json.py" chemin/vers/document.docx -o output.json
```

Modifier le JSON puis relancer la génération.

## Composants disponibles

Chaque composant JSON correspond à une fonction Python dans le script.

| Type JSON | Rendu | Description |
|-----------|-------|-------------|
| `header` | En-tête 3 colonnes | [Type+N°] [Titre] [Badge niveau] |
| `section_title` | Titre numéroté | [N° blanc/noir] [Titre gras/gris] |
| `section_band` | Bandeau dégradé | Rectangle arrondi noir→gris, texte blanc Arial Rounded MT Bold |
| `content_box` | Environnement didactique | Label vertical noir à gauche + contenu gris clair à droite |
| `exercise` | Label exercice | Wingdings F0DC + Cooper + énoncé + points/étoiles |
| `items` | Sous-questions | Labels a. b. c. avec fond noir texte blanc |
| `answer_grid` | Grille Séyès | Image tuilée/découpée aux dimensions voulues (cm) |
| `table` | Tableau données | En-tête noir + lignes alternées gris/blanc |
| `text` | Paragraphe libre | Texte avec formules $...$ et mots-clés **...** |
| `page_break` | Saut de page | Nouvelle page |

## RÈGLES CRITIQUES pour le JSON

### Espacement automatique — PAS DE SPACERS dans le JSON

Le script gère **automatiquement** l'espacement (2pt) entre tous les composants majeurs
(header, section_title, section_band, content_box, exercise, answer_grid, table, items).
**NE JAMAIS ajouter de composant `spacer`** dans le JSON. C'est le script qui s'en charge.

### Mode mathématique — OBLIGATOIRE pour tout contenu mathématique

**TOUTE expression mathématique, nombre, variable ou symbole** doit être encadré par `$...$`
pour être rendu en mode mathématique OMML natif Word. Cela inclut :

- Les formules : `$f(x) = 3x^2 + 5$`
- Les variables isolées : `la fonction $f$`, `la variable $x$`
- Les nombres dans un contexte mathématique : `$x = 3$`, `la valeur $-2$`
- Les ensembles : `$\\mathbb{R}$`, `$\\mathbb{N}$`
- Les opérateurs : `$\\times$`, `$\\leq$`, `$\\geq$`
- Les fractions : `$\\frac{1}{2}$`

**Exemples corrects** :
```
"Résoudre $2x + 3 = 7$"
"La fonction $f$ est définie sur $\\mathbb{R}$ par $f(x) = x^2 - 4$"
"On obtient $x = \\frac{-b}{2a}$"
```

**Exemples INCORRECTS** (ne pas faire) :
```
"Résoudre 2x + 3 = 7"          ← pas de $...$, rendu en texte brut
"La fonction f est définie..."   ← f sans $, pas en italique math
```

### Accents français — TOUJOURS corrects

Tous les textes doivent utiliser les accents français corrects :
é, è, ê, ë, à, â, ù, û, ô, î, ï, ç, etc.

**Jamais** d'ASCII pur sans accents, même dans les clés JSON ou les commentaires.

## Labels d'environnements didactiques

Les labels autorisés pour `content_box` : Propriété, Règle, Méthode, Définition, Rappel,
Remarque, Théorème, Exemple, Attention. Le label apparaît en vertical (rotation 90°)
dans une cellule noire étroite à gauche du contenu.

## Conventions de texte

- Formules LaTeX inline entre `$...$` : converties en OMML natif Word
- Mots-clés entre `**...**` : rendus en gras+italique (convention Loiseau)
- Les accents français doivent toujours être corrects

## Asset embarqué

- `assets/grille_seyes.png` : image de grille Séyès (1685×2224 px) extraite des documents
  originaux F. Loiseau, utilisée pour le tuilage dynamique des cadres réponse.

## Export PDF

Le script tente d'abord LibreOffice (`soffice --headless`), puis Word via COM (`comtypes`).
Au moins l'un des deux doit être disponible.

## Versions élève / corrigé

Le JSON contient un champ `versions` avec `"eleve"` et/ou `"corrige"`.
En mode élève, les corrections sont masquées et remplacées par des grilles Séyès.
En mode corrigé, les corrections sont affichées avec labels rouges.
