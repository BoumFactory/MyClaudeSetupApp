# Format JSON d'une progression

Le fichier JSON consommé par `scripts/apply_progression.py` décrit la
*progression* à injecter dans une fiche vierge déjà générée. Sa structure
volontairement plate permet à Claude de la construire incrémentalement
au fil d'une conversation, sans manipuler le HTML lourd (~100 KB).

## Schéma

```json
{
  "niveau": "5E",               // informatif (pour traçabilité), pas vérifié
  "conserver_intro": true,      // si true (défaut), garde la séquence d'intro du vierge
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
| `sequence` | `titre`, `contenu` | Crée un bloc `<div class="sequence open">` dans le rightPanel. |
| `vacances` | `label` (optionnel, défaut `"Vacances"`) | Insère une bande "Vacances" entre deux séquences. |

### Items à l'intérieur d'une séquence (`contenu[*].type`)

| `type`        | Champs requis | Effet |
|---------------|---------------|-------|
| `objectif`    | `code` | Cherche `code` dans la colonne gauche, récupère **sa couleur** et **son intitulé**, puis crée un `<div class="right-objectif">` correspondant. L'objectif est **automatiquement grisé** côté gauche. |
| `commentaire` | `titre` (optionnel), `texte` (optionnel) | Bloc jaune contenteditable avec titre + zone de texte (les URL sont automatiquement transformées en liens cliquables côté JS). |
| `separateur`  | `label` (optionnel, défaut `"Exos / RdP / Auto🛠"`) | Trait horizontal foncé séparant deux phases dans la séquence. |

## Règles d'usage

- Les `code` doivent être ceux **présents dans la colonne gauche** du HTML
  vierge cible (donc générés depuis `data/json/{NIVEAU}.json` du skill
  `programmes-officiels`). Les codes inconnus sont signalés en `[WARN]`
  par le script et **ignorés**.
- L'ordre des `elements` est respecté tel quel : pas de tri automatique.
- L'ordre des `contenu` à l'intérieur d'une séquence est lui aussi respecté.
- Un même `code` placé deux fois sera dédupliqué côté UI (le JS marque le
  bouton gauche grisé une seule fois). Évitez quand même les doublons.
- `conserver_intro: false` supprime la séquence d'intro pré-remplie
  (Programmes officiels + liens). Utile si l'enseignant veut tout
  reconstruire à la main.

## Construction conversationnelle

Quand Claude bâtit ce JSON via une conversation guidée, il doit :

1. demander combien de séquences (et le nom de chacune)
2. demander la position des vacances (à insérer entre quelles séquences)
3. pour chaque séquence : proposer une répartition des compétences en
   se basant sur le JSON du skill (ordre canonique du BO recommandé)
4. itérer avec l'utilisateur sur les ajustements (déplacer une compétence,
   ajouter un commentaire, etc.)

Voir `workflow_conversation.md` pour la séquence de questions recommandée.
