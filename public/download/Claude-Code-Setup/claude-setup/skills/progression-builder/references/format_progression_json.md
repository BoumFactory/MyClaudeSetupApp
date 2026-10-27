# Format JSON d'une progression

Le fichier JSON consommé par `scripts/apply_progression.py` décrit la
*progression* à injecter dans une fiche déjà générée (vierge ou remplie).
C'est aussi le format lu par le bouton « Importer » de la fiche. Sa structure
volontairement plate permet à Claude de la construire incrémentalement
au fil d'une conversation, sans manipuler le HTML lourd (~100 KB).

## Schéma

```json
{
  "niveau": "5E",               // vérifié par validate_progression.py
  "titre": "Progression 5e",    // facultatif : remplace le titre de la fiche
  "sous_titre": "Année 2026-2027", // facultatif
  "elements": [
    {
      "type": "sequence",
      "titre": "Séquence 1 — Démarrage",
      "contenu": [
        { "type": "commentaire", "titre": "Période 1", "texte": "1er septembre → 17 octobre." },
        { "type": "objectif",    "code": "5E-GEO-001" },
        { "type": "objectif",    "code": "5E-GEO-002" },
        { "type": "separateur",  "label": "Exos / RdP" },
        { "type": "objectif",    "code": "5E-GEO-003" }
      ]
    },
    { "type": "vacances", "label": "Vacances de la Toussaint" },
    {
      "type": "sequence",
      "titre": "Séquence 2 — Triangles",
      "contenu": [
        { "type": "objectif", "code": "5E-GEO-010" },
        { "type": "objectif", "code": "5E-GEO-011" }
      ]
    }
  ]
}
```

## Types acceptés

### Éléments racine (`elements[*].type`)

| `type`     | Champs requis | Effet |
|------------|---------------|-------|
| `sequence` | `titre`, `contenu` | Crée une séquence dans la colonne droite (`"replie": true` pour la replier). |
| `vacances` | `label` (optionnel, défaut `"Vacances"`) | Insère un séparateur doré entre deux séquences (`couleur` facultative). |
| `separateur` | `label`, `color` (optionnels) | Séparateur libre entre deux séquences (format du bouton « JSON » de la fiche). |

### Items à l'intérieur d'une séquence (`contenu[*].type`)

| `type`        | Champs requis | Effet |
|---------------|---------------|-------|
| `objectif`    | `code` | À l'ouverture, la fiche **déplace** l'objectif de la colonne gauche vers la séquence (couleur, intitulé, lien BO conservés) ; le compteur « placés / restants » est à jour. |
| `commentaire` | `titre` (optionnel), `texte` (optionnel) | Commentaire jaune ouvert, placé sous les objectifs de la séquence. Les URL deviennent des liens, les retours à la ligne sont conservés. |
| `separateur`  | `label` (optionnel, défaut `"Exos / RdP / Auto"`) | La fiche n'a pas de séparateur interne : il devient un commentaire « 🛠 label » qui indique le premier objectif de la phase. |

## Règles d'usage

- Les `code` doivent être ceux **présents dans la colonne gauche** du HTML
  vierge cible (donc générés depuis `data/json/{NIVEAU}.json` du skill
  `programmes-officiels`). Les codes inconnus sont signalés en `[WARN]`
  par le script et **ignorés**.
- L'ordre des `elements` est respecté tel quel : pas de tri automatique.
- L'ordre des `contenu` à l'intérieur d'une séquence est lui aussi respecté.
- Un même `code` placé deux fois : seule la première place est gardée
  (`[WARN]` du script, avertissement du validateur).
- Les commentaires d'une séquence s'affichent toujours sous ses objectifs
  (structure de la fiche) : leur position relative dans `contenu` est perdue.
- `conserver_intro` (ancien gabarit) est accepté mais sans effet : les
  fiches actuelles n'ont pas de séquence d'intro.

## Construction conversationnelle

Quand Claude bâtit ce JSON via une conversation guidée, il doit :

1. demander combien de séquences (et le nom de chacune)
2. demander la position des vacances (à insérer entre quelles séquences)
3. pour chaque séquence : proposer une répartition des compétences en
   se basant sur le JSON du skill (ordre canonique du BO recommandé)
4. itérer avec l'utilisateur sur les ajustements (déplacer une compétence,
   ajouter un commentaire, etc.)

Voir `workflow_conversation.md` pour la séquence de questions recommandée.
