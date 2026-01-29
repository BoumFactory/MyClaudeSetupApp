# Variables des Templates de Fiche Technique

Ce document liste toutes les variables a remplacer dans les templates LaTeX.

---

## Variables communes aux deux formats

| Variable | Description | Exemple |
|----------|-------------|---------|
| `%TITRE_RESSOURCE%` | Titre complet de la ressource | Exercices sur le produit scalaire |
| `%NIVEAU%` | Niveau court | 1ere Spe |
| `%THEME%` | Theme mathematique principal | Produit scalaire |
| `%TYPE_RESSOURCE%` | Type de document | Exercices |
| `%DUREE%` | Duree estimee | 1h30 |
| `%AUTEUR%` | Nom de l'enseignant | B. MUSIC |
| `%DATE%` | Date de creation | \today |
| `%ANNEE_SCOLAIRE%` | Annee scolaire | 2025-2026 |
| `%COMPETENCES%` | Liste des competences | Chercher, Calculer |
| `%ACTIVITES_ELEVES%` | Description des activites | Calculs, demonstrations |
| `%PREREQUIS%` | Prerequisites necessaires | Vecteurs, coordonnees |
| `%DEROULEMENT%` | Deroulement de la seance | ... |
| `%DIFFICULTES%` | Difficultes anticipees | ... |
| `%DIFFERENCIATION%` | Strategies de differenciation | ... |
| `%PROLONGEMENTS%` | Prolongements possibles | ... |

---

## Variables specifiques au format Inspecteur

### En-tete officiel

| Variable | Description |
|----------|-------------|
| `%ACADEMIE%` | Academie (ex: Reims) |
| `%TYPE_ETABLISSEMENT%` | Lycee ou College |
| `%NOM_ETABLISSEMENT%` | Nom de l'etablissement |

### Sections detaillees

| Variable | Description |
|----------|-------------|
| `%NIVEAU_DETAILLE%` | Niveau complet (ex: Premiere Specialite Mathematiques) |
| `%PRESENTATION%` | Presentation generale de la ressource |
| `%CONNAISSANCES%` | Liste des connaissances visees |
| `%CAPACITES%` | Liste des capacites travaillees |
| `%REFERENCES_BO%` | Citations exactes du BO avec references |
| `%COMPETENCES_SOCLE%` | Competences du socle commun (college) |
| `%COMPETENCES_MATHS%` | Competences mathematiques (chercher, modeliser, etc.) |
| `%PREREQUIS_MATHS%` | Prerequisites mathematiques |
| `%PREREQUIS_METHODO%` | Prerequisites methodologiques |
| `%DUREE_TOTALE%` | Duree totale et decoupage |
| `%ORGANISATION%` | Type d'organisation |
| `%MATERIEL%` | Materiel necessaire |
| `%SUPPORTS%` | Supports utilises |
| `%JUSTIFICATION_PEDAGOGIQUE%` | Justification des choix pedagogiques |
| `%MODALITES_EVALUATION%` | Modalites d'evaluation |
| `%CRITERES_REUSSITE%` | Criteres de reussite |
| `%BIBLIOGRAPHIE%` | Bibliographie et ressources |

---

## Variables specifiques au format Collegues

| Variable | Description |
|----------|-------------|
| `%TITRE_COURT%` | Titre court pour en-tete |
| `%RESUME%` | Resume en 2-3 phrases |
| `%NOTIONS%` | Liste des notions travaillees |
| `%ORGANISATION%` | Organisation de classe |
| `%MATERIEL%` | Materiel necessaire |
| `%CONSEILS_PRATIQUES%` | Conseils pratiques (optionnel) |
| `%LIEN_PROGRAMME%` | Lien avec le programme (version concise) |
