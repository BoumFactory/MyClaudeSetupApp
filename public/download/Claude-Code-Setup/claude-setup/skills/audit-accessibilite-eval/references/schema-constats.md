# Format de `constats.json`

Fichier rédigé par l'agent (outil **Write**, jamais par un heredoc Bash : les `$...$` et antislashs y seraient altérés) dans le dossier d'audit. `generer_rapport.py` le valide et refuse un fichier incomplet.

Les champs de texte acceptent le mode mathématique `$...$` (rendu KaTeX, qui demande une connexion internet à l'ouverture du rapport). Dans du JSON, un antislash s'écrit doublé : `$P_{\\overline{M}}(C)$`.

L'exemple ci-dessous est volontairement pris hors de tout sujet réel (le cas d'école des parallélogrammes de `[EX]`) : il fixe la **forme**, pas le contenu. Tes constats viennent du sujet audité.

## Structure complète

```json
{
  "evaluation": {
    "titre": "Contrôle — Parallélogrammes",
    "niveau": "5e",
    "duree": "30 min",
    "bareme": "/10",
    "type_evaluation": "sommative",
    "echeance": "brevet (dans deux ans)",
    "champs_deduits": ["type_evaluation", "echeance"],
    "date_analyse": "2026-10-06",
    "fichier_source": "<dossier du sujet>/controle.tex",
    "fichiers_a_modifier": ["<dossier du sujet>/controle.tex"],
    "pages_analysees": [1],
    "contraintes_enseignant": ["Le sujet tient sur une page recto"]
  },

  "objectifs": [
    {
      "exercice": "Ex. 1",
      "intitule": "Compléter des parallélogrammes",
      "objectif": "Placer ou construire le quatrième sommet d'un parallélogramme.",
      "criteres_reussite": ["Utiliser l'égalité des côtés opposés ou le milieu commun des diagonales", "Respecter l'ordre des sommets"],
      "deduit": false
    }
  ],

  "synthese": {
    "verdict": "Deux à quatre phrases : le niveau global d'accessibilité et l'obstacle principal.",
    "priorites": [
      {"texte": "Séparer les deux constructions en deux questions linéaires.", "constats": ["C02"]}
    ],
    "points_forts": ["Le quadrillage rend le placement de H vérifiable sans instrument."]
  },

  "grille": [
    {"dimension": "mise_en_forme", "niveau": "partiel", "justification": "…", "constats": ["C01"]},
    {"dimension": "appartenance", "niveau": "non_applicable", "justification": "Sujet individuel ; relève de la correction collective (voir passation).", "constats": []}
  ],

  "constats": [
    {
      "id": "C02",
      "exercice": "Ex. 1",
      "question": "Q1",
      "dimension": "sequencage",
      "code": "ST1",
      "gravite": "important",
      "a_retenir": true,
      "titre": "Deux constructions dans une seule phrase",
      "observation": "« Construire les points H et D tels que EGHF et ABCD soient des parallélogrammes » : une consigne, deux tâches, deux figures côte à côte.",
      "pourquoi": "L'élève doit séparer lui-même les deux tâches et associer chaque point à sa figure ; celui qui s'y perd échoue aux deux constructions sans que sa maîtrise du parallélogramme soit en cause.",
      "source": "[EX] p. 2",
      "eleves_concernes": "Élèves avec un trouble de l'attention, lecteurs lents.",
      "zones": [
        {"page": 1, "ancre": "Construire les points H et D", "ancre_fin": "soient des parallélogrammes"},
        {"page": 1, "bloc": ["p1-b7", "p1-b8"], "cadre": true}
      ],
      "pistes": [
        {
          "titre": "Une question par construction",
          "detail": "Deux questions numérotées, chacune sous sa figure.",
          "avant": "Construire les points H et D tels que EGHF et ABCD soient des parallélogrammes.",
          "apres": "1. Placer le point H pour que le quadrilatère EFGH soit un parallélogramme.\n2. Construire le point D pour que le quadrilatère ABCD soit un parallélogramme.",
          "effort": "faible",
          "recommandee": true,
          "pourquoi_recommandee": "Lève l'obstacle sans rien retirer à l'objectif, et tient sur la page en réduisant une figure."
        },
        {
          "titre": "Deux exercices distincts",
          "detail": "Un exercice « placer sur quadrillage », un exercice « construire aux instruments », chacun avec son barème.",
          "effort": "moyen"
        }
      ],
      "preserve": "Les deux constructions restent entièrement à la charge de l'élève.",
      "vigilance": "Laisser de la place autour des points pour que la présentation n'induise pas la réponse.",
      "arbitrage": "La présentation linéaire prend quatre lignes de plus : réduire la figure ABCD pour tenir sur une page."
    }
  ],

  "passation": [
    {"id": "P01", "moment": "avant", "titre": "Annoncer les critères de réussite", "detail": "…", "source": "[VERS] p. 2", "a_retenir": true}
  ],

  "mesures_commentaire": "Facultatif : une phrase qui interprète mesures.json."
}
```

## Règles de remplissage

### Évaluation et objectifs

- **`champs_deduits`** : liste des champs de `evaluation` que tu as déduits faute de source (le rapport les marque « déduit »). Dans `objectifs`, c'est `"deduit": true` par exercice.
- **Exercice pas encore rédigé** (« Question à venir », trous) : garde-le dans `objectifs` avec `"objectif": "Non rédigé à la date de l'audit"` et `"criteres_reussite": []`, aucun constat, et une phrase dans le verdict. N'invente pas de critères.

### Grille

Les neuf dimensions, toutes présentes : `mise_en_forme`, `ancrages_linguistiques`, `sequencage`, `non_verbal`, `materiel`, `repetition`, `appartenance`, `autonomie`, `reussite`. `niveau` ∈ `aucun`, `partiel`, `avance`, `non_applicable`.

### Constats

- **`id`** : `C01`, `C02`… dans l'ordre d'apparition dans le sujet ; `P01`… pour la passation.
- **`gravite`** ∈ `bloquant`, `important`, `confort` (aucune autre valeur) :
  - `bloquant` : peut faire échouer un élève à tout ou partie d'un exercice pour une raison étrangère à l'objectif (mot inconnu qui verrouille l'exercice, cascade sans résultat intermédiaire, tâche irréalisable pour un élève empêché) ;
  - `important` : coût cognitif ou temps notable, sans échec certain ;
  - `confort` : lisibilité ou confort.
- **`exercice`** : même libellé que dans `objectifs` (le rapport regroupe les constats sous ce titre). Un constat qui touche **deux exercices ou plus** va sous `"Ensemble du sujet"`, et son titre nomme les exercices concernés.
- **`question`** : facultatif ; « Q2 », « Q3-Q4 ». Omets le champ pour un constat transversal (pas de « — »).
- **`pistes`** : de une à trois, de la plus économe à la plus ambitieuse. `avant` / `apres` donnent la reformulation exacte quand elle est textuelle — c'est ce qui permet à l'enseignant de décider vite. Retour à la ligne : `\n`. Pour un **tableau**, une ligne par rangée, cellules séparées par `|`, la première rangée servant d'en-tête :
  `"apres": "| Test positif | Test négatif | Total\nMalades | … | … | 100\nTotal | 585 | … | 5 000"`
  N'écris pas de code LaTeX dans `avant` / `apres` : l'agent qui applique s'en charge.
- **Présélection** (obligatoire, le validateur la vérifie) : le rapport s'ouvre avec tes recommandations déjà cochées, l'enseignant n'a plus qu'à ajuster.
  - dans chaque constat, **exactement une** piste porte `"recommandee": true`, avec `"pourquoi_recommandee"` en une phrase (meilleur rapport efficacité / coût, compatibilité avec les contraintes et l'échéance) ; même quand il n'y a qu'une piste ;
  - chaque constat porte `"a_retenir": true` ou `false` : `true` pour ce que tu conseilles de traiter dans cette version du sujet (en général les bloquants et les importants compatibles avec les contraintes), `false` pour ce qui peut attendre ou dont l'arbitrage penche contre ;
  - chaque action de passation porte aussi `"a_retenir"`.
- **`preserve`** : ce que la piste ne touche pas dans l'objectif et les critères de réussite. Toujours rempli.
- **`vigilance`** : risque de la piste (étayage qui en dit trop, page en plus, temps).
- **`arbitrage`** : seulement s'il y a conflit avec `contraintes_enseignant`.

### Zones (captures)

Chaque zone porte `page` et un localisateur :

| Clé | Effet |
|---|---|
| `ancre` | texte cherché mot à mot, insensible à la casse, aux ligatures et à la ponctuation. Prends 3 à 6 mots sur **une seule ligne** du PDF : une formule ou un retour à la ligne au milieu casse souvent la recherche (une césure en début d'ancre est tolérée). |
| `ancre_fin` | étend le surlignage de `ancre` jusqu'à la fin de ce second texte (une phrase ou un paragraphe entier). |
| `occurrence` | la n-ième apparition de `ancre` (1 par défaut). |
| `bloc` | un identifiant ou une liste d'identifiants de `mise_en_page.json` (`"p1-b12"`) : tableaux, figures, cadres. |
| `bbox` | rectangle `[x0, y0, x1, y1]` en points PDF, origine en haut à gauche. |
| `cadre` | `true` : un seul rectangle englobant au lieu du surlignage ligne à ligne. |
| `marge` | élargissement du surlignage en points (4 par défaut). |

Deux constats ne doivent pas surligner la même zone : chacun cible la phrase ou la cellule qui le concerne. `capturer_zones.py` alerte quand deux zones se recouvrent à plus de 60 %. Un constat transversal (police de tout le sujet) cible un ou deux passages représentatifs.
