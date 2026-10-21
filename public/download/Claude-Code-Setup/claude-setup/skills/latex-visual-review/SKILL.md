---
name: latex-visual-review
description: Skill compagnon de bfcours-latex pour l'auto-review visuelle et l'optimisation de la disposition d'un document LaTeX compilé. Levier principal — densification latérale des énoncés via colonnage (tcbenumerate, MultiColonnes) avec paramètres graphiques (bordures, séparateurs) pour préserver la clarté. Capture le PDF en images PNG, extrait des métriques (densité, blancs, déséquilibres), distingue les zones à compacter (énoncés, cours) des zones à laisser aérées (corrections projetées item par item, espaces réponses élèves). Utiliser systématiquement après la première compilation d'un document non trivial, OU dès que l'utilisateur demande d'optimiser l'espace, de réduire le nombre de pages, ou d'améliorer la disposition. Boucle adversariale auto-corrective avec rollback automatique si dégradation ou compilation cassée.
---

# LaTeX Visual Review — Optimisation visuelle bfcours

Skill compagnon de `bfcours-latex` pour **regarder le PDF rendu** et **optimiser sa disposition** sans intervention manuelle de l'utilisateur.

**Le levier principal est le colonnage** (`tcbenumerate[n]`, `MultiColonnes{n}`, imbrications), pas la suppression d'espaces. Toute densification s'accompagne des paramètres graphiques (bordures, séparateurs) qui préservent la lisibilité.

Ce skill traite la **mise en page** ; il ne reformule pas le contenu pédagogique (seules exceptions, signalées dans le rapport : raccourcir un titre ou une consigne trop longue, retirer une `Remarque` strictement redondante).

**Prérequis** : un document écrit avec le paquet bfcours (`EXO`, `tcbenumerate`, `MultiColonnes`, `\tcbitempoint`, `crep`…) ; toutes les recettes en dépendent. Pour un document LaTeX standard sans bfcours, seuls les scripts de capture et de métriques s'appliquent ; pour produire directement une mise en page soignée sans bfcours, voir la commande `/optiLatex` (`commands/creer/latex/optiLatex.md`).

---

## Règle d'or — Zones à compacter, zones à laisser aérées

Avant toute action, identifier la zone concernée (grep sur le `.tex`, ou sur le PNG : couleur de l'environnement, badge « Solution de l'Exercice »).

| Zone | Repérage LaTeX | Politique |
|---|---|---|
| **Énoncés d'exercices** | Entre `\begin{EXO}{...}` et `\exocorrection` | **Compacter à fond** (colonnage maximal, côte à côte) |
| **Corrections d'exercices** | Entre `\exocorrection` et `\end{EXO}` | **NE PAS TOUCHER** : l'enseignant projette item par item, l'item suivant ne doit pas être visible à l'écran. Garder très aéré. |
| **Cours** (`Definition`, `Propriete`, `Theoreme`, `Demonstration`, `Remarque`, `Notation`, `Methode`) | Environnements didactiques bfcours | Compacter le contenu, juxtaposer les blocs apparentés |
| **Exemples + espaces réponses élèves** | `\repsim`, `\tcfillcrep`, `crep` dans un `Exemple` | **NE PAS RÉDUIRE** la zone réponse ; compacter ce qui l'entoure |
| **Activités** | `\begin{Activite}...` | Compacter prudemment : le déroulé pédagogique prime |

---

## Quand déclencher

1. **Review initiale automatique** : après la première compilation réussie d'un document non trivial (≥ 2 pages, cours ou évaluation complète).
2. **Demande explicite** : « optimise l'espace », « densifie les énoncés », « fais tenir sur N pages », « passe ce tcbenumerate en 2 colonnes ».
3. **Signal suspect** : document plus long qu'attendu, `Overfull \hbox` non triviaux, dernière page quasi vide.

**Ne pas déclencher** : document de moins d'une page, brouillon intermédiaire, `enonce.tex` isolé non compilable seul, correction isolée à éditer.

---

## Fichiers de référence : lequel lire, et quand

| Fichier | Contenu | À lire |
|---|---|---|
| `references/metriques-et-score.md` | Seuils des métriques, score composite, tableau de décision entre deux versions, arbitrage métrique / lisibilité, annulation différée | Étapes 3, 5, 6 et 7 |
| `references/colonnage.md` | Leviers 1 à 4 (`tcbenumerate[n]`, `MultiColonnes`, imbrication, bordures, largeurs asymétriques), centrage `halign` (T3), Recettes A à F, grille virtuelle (T4), signaux d'arrêt | Étape 4, puis avant chaque batch de colonnage |
| `references/exemples-et-reponses.md` | Étapes d'`Exemple` côte à côte (G, H), méthode + exemple (I), tableau-réponse latéralisé (J), tableau en demi-colonne (T1), `\tcfillcrep` scindé (T2), `Remarque` redondante (Levier 6) | Étape 4 si le document contient des `Exemple`, des espaces réponses ou un cours |
| `references/pagination-et-bandeaux.md` | `\newpage` et table des matières (Levier 5), `\medskip` (5bis), `\Needspace` (D6), QCM `Mcq` scindés (M), badge de points (T5), titres d'EXO (T6), permutation d'EXO (T7), `display score=false` (T8) | Étape 4 (inventaire) et batchs de fin |
| `references/figures-et-defauts.md` | Figure latéralisée (L), courbe / tangente (K), image raster sous 150 dpi (D7), défauts D1 à D5 | Étape 4 si le document contient des figures, ou défaut résiduel |

Syntaxe bfcours de référence : `bfcours-latex/references/bfcours-conventions.md` (sections `MultiColonnes` et `tcbenumerate`).

---

## Principe

**Audit global d'abord, batch cohérent ensuite, annulation différée.** Une modification isolée gagne rarement une page ; le gain vient de l'effet cumulé d'un batch, puis de la purge des `\newpage` devenus inutiles. Raisonner sur le document entier à chaque batch : interactions entre EXO consécutifs, blocs poussés en cascade, colonnes asymétriques possibles.

Le score est un guide, pas une fin : un rendu plus clair à score égal se garde (règle d'arbitrage dans `references/metriques-et-score.md`).

```
1. Workspace versionné (.lvr-workspace/v0/, v1/, ...)
2. Audit global : capturer, mesurer, lister TOUTES les opportunités
3. Plan ordonné (zones, leviers, confiance)
4. Itération N : sauvegarder v{N} → batch de 3-8 modifs → recompiler 3 passes → mesurer, comparer
5. Annulation différée (2 itérations sans gain dont une dégradante)
6. Rapport final, puis nettoyage du workspace
```

---

## Workflow détaillé

### Étape 1 — Pré-requis

Document déjà compilé avec succès. Identifier `project_dir` (dossier du projet), `tex_path` (source à modifier, souvent `enonce.tex`), `pdf_path`, et l'objectif éventuel (« tenir sur 4 pages »). Lire d'abord, s'ils existent dans le projet, `CLAUDE.md` et `rapport_optimisation.md` : ils listent souvent des leviers déjà connus.

### Étape 2 — Workspace versionné

```
<project_dir>/.lvr-workspace/
├── plan.md        # plan des optimisations
├── runs.jsonl     # une ligne par version
├── v0/            # état initial : enonce.tex, document.pdf, metrics.json, captures/ (PNG 110 dpi)
├── v1/            # après le 1er batch
└── ...
```

Toujours créer `v0/` avant la moindre modification. Aucune version n'est supprimée avant la fin du run.

### Étape 3 — Capture et métriques initiales (v0)

```bash
python ".claude/skills/latex-visual-review/scripts/capture_pages.py" --pdf "<pdf_path>" --output "<project_dir>/.lvr-workspace/v0/captures" --dpi 110
python ".claude/skills/latex-visual-review/scripts/page_metrics.py" --pdf "<pdf_path>" --dpi 80 > "<project_dir>/.lvr-workspace/v0/metrics.json"
```

Copier `enonce.tex` et le PDF dans `v0/`. Lire les métriques avec les seuils de `references/metriques-et-score.md`.

### Étape 4 — Audit global et plan

Lire `references/colonnage.md`, puis les autres fichiers de référence selon le contenu du document (tableau ci-dessus). Inventorier de façon **exhaustive** :

1. `\newpage` et `\clearpage` (`grep -n "newpage\|clearpage"`) : justifiés structurellement ou ajoutés pour un problème désormais réglable autrement ? Table des matières sur une fiche d'exercices ? → `pagination-et-bandeaux.md`.
2. `tcbenumerate` d'énoncé (`grep -n "begin{EXO}\|exocorrection\|begin{tcbenumerate}"`) : `[n]` peut-il augmenter ? Un seul item wrappe ? → `colonnage.md` (Levier 1, T4).
3. Blocs « tableau + questions », « code + tableau », « méthode A + méthode B » empilés → Levier 2 ; tableau-réponse élève dans un EXO → Recette J.
4. `Exemple` à étapes, espaces réponses, `Remarque` de cours → `exemples-et-reponses.md`.
5. `\medskip`, `\smallskip`, `\bigskip` → Levier 5bis.
6. Pages `is_sparse` / `widow_hint` : remonter au `.tex` ; vérifier un `\Needspace` surdimensionné juste avant le saut (D6) ; QCM `Mcq` non sécable (M).
7. `low_dpi_images` non vide → D7 ; figure seule centrée dans une question → Recette L.
8. Bandeaux d'EXO sur deux lignes, badges de points qui chevauchent → T6, T5, T8.

Écrire `.lvr-workspace/plan.md` :

```markdown
# Plan d'optimisation
## Cibles fortes (confiance haute)
- [ ] L. XYZ : EXO « ... » — Levier 1 — `tcbenumerate[1]` → `[2]`
- [ ] L. ABC : `\newpage` douteux → à retirer en fin de batch
## Cibles moyennes
- [ ] L. DEF : EXO « ... » — Levier 2 — MultiColonnes{2}, boxrule=0.4pt
## Cibles incertaines (examiner visuellement avant)
## Zones interdites (rappel)
- Corrections (`\exocorrection` → `\end{EXO}`), espaces réponses (`\repsim`, `\tcfillcrep`, `crep`)
```

### Étape 5 — Itérations (v1, v2, …)

1. Copier les `.tex` qui vont changer dans `.lvr-workspace/v{N}/` **avant** toute édition.
2. Choisir un batch cohérent de 3 à 8 modifications : d'abord un batch « Levier 1 seul » (le plus sûr), puis « Levier 2 » sur des EXO comparables, puis la purge des `\newpage` **seulement après** une densification significative.
3. Relire le `.tex` immédiatement avant les Edit, puis appliquer le batch.
4. Recompiler 3 passes (les renvois et la table des matières bougent) :
   ```bash
   python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "<tex_path>" --passes 3
   ```
   Compilation en échec : restaurer depuis `v{N}/`, marquer le batch épuisé, chercher la cause (souvent une syntaxe `MultiColonnes` incorrecte).
5. Capturer et mesurer dans `v{N+1}/` (le numéro reflète l'état après le batch) ; comparer avec le tableau de décision de `references/metriques-et-score.md`. Pour visualiser l'effet : `scripts/diff_pages.py --before v{N}/captures --after v{N+1}/captures --output <dossier>`.

### Étape 6 — Annulation différée

Jamais immédiate sur un seul batch (sauf compilation cassée ou zone protégée touchée). Conditions et choix de la version à restaurer : `references/metriques-et-score.md`.

### Étape 7 — Convergence et rapport final

Arrêt quand le plan est épuisé, après 2 itérations sans gain mesurable, ou sur demande. Le rapport donne : v0 → état final (pages, `fill_mean`, `density_imbalance`, score), versions traversées et leur score, modifications retenues (extraits avant/après pour les plus parlantes), modifications abandonnées et pourquoi, captures finales.

### Nettoyage du workspace (obligatoire)

Mode normal : présenter le rapport, attendre la validation du résultat, **puis** supprimer le workspace (avant validation, il sert à revenir en arrière). Si l'utilisateur veut le garder, ne pas le supprimer et le signaler.

```bash
PYTHONIOENCODING=utf-8 python ".claude/skills/latex-visual-review/scripts/nettoyer_workspace.py" --path "<project_dir>/.lvr-workspace"
```

### Étape 8 — Capitalisation des patterns (mode normal, avant de rendre la main)

À la fin de **chaque** run, proposer à l'utilisateur d'ajouter au skill les patterns nouveaux rencontrés, sans jamais le faire en silence.

1. Repérer les nouveautés : transformation qui ne correspond à aucune recette documentée ; consigne précise de l'utilisateur qui mérite d'être généralisée ; intuition de l'agent non couverte (découpage d'un `\tcfillcrep`, choix de bordure…) ; méta-règle confirmée par l'expérience.
2. Présenter la liste en indiquant la destination : recette structurelle ou technique ponctuelle → le fichier de `references/` du thème concerné ; méta-règle ou garde-fou → ce SKILL.md.
3. Demander : tout ajouter (recommandé), une sélection, ou rien (simple trace dans le rapport) ; l'utilisateur peut nuancer chaque point.
4. Appliquer les choix. Si aucun pattern nouveau n'a émergé, le dire explicitement.

---

## Mode sous-agent

Si le skill est invoqué par un autre agent (outil `Task` ou prompt « mode sous-agent ») et non directement par l'utilisateur :

- **Workspace dans le scratchpad** de la session (`<scratchpad>/lvr-workspace-<slug>/`), jamais dans le projet appelant. Le nom doit commencer par `lvr-workspace` (condition de sécurité du script de nettoyage).
- **Aucune question** : l'Étape 8 est remplacée par une rubrique « Patterns candidats à la capitalisation — à valider par l'agent orchestrateur » dans le rapport, sans modifier le skill.
- **Tout dans le rapport** (scores avant/après, modifications retenues et abandonnées, chemins des captures utiles) : le workspace sera détruit.
- **Nettoyage systématique** avant de rendre la main, y compris en cas d'échec :
  ```bash
  PYTHONIOENCODING=utf-8 python ".claude/skills/latex-visual-review/scripts/nettoyer_workspace.py" --path "<scratchpad>/lvr-workspace-<slug>"
  ```

---

## Catalogue des leviers

| Code | Levier | Fichier |
|---|---|---|
| L1 | Augmenter `[n]` d'un `tcbenumerate` d'énoncé (dont variante asymétrique) | `colonnage.md` |
| L2 | `MultiColonnes{2}` ou `{3}` pour deux blocs apparentés (Recettes A, B, C) | `colonnage.md` |
| L3 | Imbrication asymétrique, bordure au premier niveau (Recette D) | `colonnage.md` |
| L4 | Paramètres graphiques de clarté, largeurs asymétriques `raster multicolumn` | `colonnage.md` |
| L5, L5bis | Purge des `\newpage` devenus inutiles ; suppression des `\medskip` / `\smallskip` / `\bigskip` | `pagination-et-bandeaux.md` |
| L6 | Retrait d'une `Remarque` strictement redondante | `exemples-et-reponses.md` |
| E, F | Formules `\encadrer` parallèles ; formule + commentaire | `colonnage.md` |
| G, H | Étapes d'`Exemple` côte à côte ; items 1-2 parallèles + conclusion pleine largeur | `exemples-et-reponses.md` |
| I | `bfd methode` + `bfd exemple` côte à côte | `exemples-et-reponses.md` |
| J | EXO avec tableau-réponse latéralisé | `exemples-et-reponses.md` |
| K, L | Courbe / tangente lisibles ; figure latéralisée à côté de sa consigne | `figures-et-defauts.md` |
| M | QCM `Mcq` scindé en blocs (contenu perdu, page 1 vide) | `pagination-et-bandeaux.md` |
| T1, T2 | Tableau en demi-colonne (planchers `\repsim`) ; `\tcfillcrep` scindé | `exemples-et-reponses.md` |
| T3, T4 | `halign=center` au lieu de `center` ; grille virtuelle pour un item qui wrappe | `colonnage.md` |
| T5 à T8 | Badge de points, titre d'EXO trop long, permutation d'EXO, `display score=false` | `pagination-et-bandeaux.md` |
| D1 à D7 | Veuve, figure surdimensionnée, débordement, marges, page noire, `\Needspace`, raster < 150 dpi | `figures-et-defauts.md` (D6 : `pagination-et-bandeaux.md`) |

---

## Scripts disponibles

| Script | Usage |
|---|---|
| `scripts/capture_pages.py` | PDF → PNG (PyMuPDF, DPI ajustable, sélection de pages) |
| `scripts/page_metrics.py` | PDF → métriques JSON (densité, blancs, déséquilibres, images raster sous 150 dpi) |
| `scripts/diff_pages.py` | Diff visuel page à page entre deux dossiers de captures (ajouts en rouge, retraits en bleu) |
| `scripts/nettoyer_workspace.py` | Supprime un `.lvr-workspace/` (projet) ou `lvr-workspace-*` (scratchpad) une fois les conclusions dans le rapport |

Dépendances : `pip install -r ".claude/skills/latex-visual-review/scripts/requirements.txt"` (PyMuPDF, numpy, Pillow). Sortie JSON, code retour ≠ 0 en cas d'erreur, UTF-8 forcé.

---

## Intégration

- **bfcours-latex** : invoqué après la compilation d'un document complet ou sur demande ; s'appuie sur ses conventions de colonnage.
- **tex-compiling-skill** : toute recompilation passe par `quick_compile.py`.
- Reformulation de fond, didactique : hors de ce skill. Erreurs de compilation : `tex-compiling-skill` ou l'agent `debug-tex-log`.

---

## Contraintes absolues

- Lire le `.tex` immédiatement avant chaque Edit ; identifier la zone avant toute modification.
- Jamais modifier une correction, un espace réponse (`\repsim`, `\tcfillcrep`, `crep`) ou le contenu d'une `Activite` sans demande explicite.
- Toujours accompagner une compaction des paramètres graphiques de clarté nécessaires (`colonnage.md`, Levier 4).
- Supprimer systématiquement `\medskip`, `\smallskip`, `\bigskip` (Levier 5bis).
- Jamais de `minipage` pour mettre côte à côte : `MultiColonnes`.
- Annuler si la compilation casse ou si une zone protégée est touchée ; 4 itérations au plus sans demande explicite.
- Capitalisation proposée en fin de run (mode normal) ; workspace nettoyé par `nettoyer_workspace.py`.
- Accents français corrects dans le LaTeX et les messages ; pas d'accents dans les noms de fichiers et dossiers temporaires.

---

## Auto-vérification (avant de rendre la main)

- [ ] Le PDF final compile sans erreur.
- [ ] Score final ≥ score initial, ou gain de lisibilité justifié à score équivalent.
- [ ] Aucune correction modifiée, aucun espace réponse réduit ; `\repsim` au-dessus des planchers de T1 (0,7 cm fractions, 1 cm décimaux et expressions).
- [ ] Recette H : les trois vérifications préalables ont été faites.
- [ ] Aucun `\tcbitem` ne contient seulement un `\begin{center}…\end{center}` (T3).
- [ ] `grep -nE "\\\\(medskip|smallskip|bigskip)" <tex>` ne renvoie rien.
- [ ] QCM : aucun `upper box part has become overfull`, toutes les questions présentes (M).
- [ ] Chaque compaction a ses paramètres de clarté, ou l'absence est justifiée.
- [ ] Rapport produit (retenues, abandonnées, delta du score) ; aucune modification sémantique non signalée.
- [ ] Étape 8 faite (mode normal) ou rubrique « patterns candidats » (mode sous-agent).
- [ ] Workspace supprimé (après validation en mode normal, systématiquement en mode sous-agent).
