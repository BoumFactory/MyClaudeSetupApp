# Palette de couleurs par domaine

La palette est définie dans `scripts/_utils.py` (constante `DOMAINE_INFO`).
Chaque domaine du skill `programmes-officiels` reçoit une couleur de
base, un emoji et une étiquette lisible. Les sous-domaines sont colorés
par dégradé HSL (éclaircissement progressif).

| Code  | Emoji | Couleur de base | Étiquette                                  |
|-------|-------|-----------------|--------------------------------------------|
| `NB`  | 🔢    | `#a30f33`       | Nombres et calculs                         |
| `AL`  | ❎    | `#5d3d70`       | Algèbre                                    |
| `AN`  | ∫     | `#1e5b9c`       | Analyse                                    |
| `GEO` | 🔷    | `#57117a`       | Géométrie                                  |
| `GM`  | 📏    | `#c75c04`       | Grandeurs et mesures                       |
| `STA` | 📊    | `#2a6a48`       | Statistiques                               |
| `PR`  | 🎲    | `#6da43e`       | Probabilités                               |
| `OGD` | 📋    | `#007a8c`       | Organisation et gestion de données         |
| `ALGO`| 💻    | `#404040`       | Algorithmique et programmation             |
| `TRG` | 📐    | `#006eb5`       | Trigonométrie                              |
| `LOG` | 🔀    | `#6e4b2f`       | Vocabulaire ensembliste et logique         |
|       | 🛠    | `#444444`       | **Automatismes** (bloc séparé, pas domaine)|

## Pourquoi cette palette

La palette est généralisée à tous les niveaux :

- choisissant une couleur **distincte** pour chaque domaine du skill,
- réservant les rouges/violets aux domaines numériques/algébriques (haute
  saturation pour le contraste blanc),
- attribuant des bleus aux domaines analyse/trigonométrie (continuité
  visuelle Géo→Trig pour les niveaux lycée),
- un gris foncé à `ALGO` (code, programmation) — ne se confond pas avec
  les domaines mathématiques "purs".

## Comment la modifier

Éditer **uniquement** `DOMAINE_INFO` dans `scripts/_utils.py`. Pas besoin
de toucher au HTML ni aux fiches déjà générées — la prochaine
régénération via `generate_vierge.py` reflètera les nouvelles couleurs.

Si vous voulez une palette différente par cycle (par exemple plus douce
pour le cycle 3, plus formelle pour le lycée), envisager d'ajouter un
paramètre `--cycle` au script et un second dict `DOMAINE_INFO_CYCLE3`.
Pour l'instant, **une seule palette pour tous les niveaux** : c'est ce
qui assure que les fiches restent reconnaissables entre niveaux
(continuité visuelle d'une année à l'autre).
