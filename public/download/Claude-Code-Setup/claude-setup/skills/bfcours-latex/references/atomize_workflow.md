# Workflow : atomisation / monolithisation d'un `enonce.tex`

Ce document détaille le pipeline d'atomisation des environnements didactiques bfcours et son opération inverse. Charger en complément de `bfcours-conventions.md` quand on touche à un cours volumineux ou à une archive partageable.

## Pourquoi atomiser

Un `enonce.tex` de cours qui dépasse **~1000 lignes** devient un point de friction :

- Read / Edit / MultiEdit ralentissent (lecture intégrale, diff lourd).
- Le contexte de l'IA est saturé par du contenu non pertinent à la tâche courante.
- Les modifications ciblées (ajouter une remarque, corriger une propriété) entraînent inutilement le re-traitement de l'ensemble du fichier.
- Le partage d'un seul concept (une démonstration, un exemple) impose de copier-coller depuis un fichier obèse.

L'atomisation extrait chaque bloc top-level (`Definition`, `Propriete`, `Theoreme`, `Lemme`, `Corollaire`, `Demonstration`, `Exemple`, `Methode`, `Remarque`, `Notation`, `Activite`, `Histoire`, `Graphique`, `Conjecture`, `Algorithme`, **et `EXO`**) dans `sections/<Type>/<nom>.tex`, et insère un `\input{...}` à la place. Le résultat compile **strictement à l'identique** (LaTeX inline les `\input` au préprocesseur).

Les `\section{}`, `\subsection{}`, `\subsubsection{}`, les commentaires de séparation, et le texte de transition **restent dans `enonce.tex`** : ils constituent la couche d'orchestration / le squelette pédagogique du cours. Sur un cours typique de 1070 lignes, le `enonce.tex` après atomisation tombe à ~120 lignes (-89%).

## Quand atomiser

| Situation | Action |
|----------|--------|
| `enonce.tex` < 1000 lignes | **Ne rien faire.** L'atomisation prématurée fragmente sans bénéfice. |
| `enonce.tex` ≥ 1000 lignes | Lancer `atomize_didactic.py`. |
| Document destiné à être partagé en archive autonome | Lancer `monolithize_didactic.py` avant d'archiver. |
| Refactor structurel majeur d'un cours déjà atomisé | Monolithiser → refondre → re-atomiser. |

Le seuil de 1000 lignes est un indicateur, pas une règle stricte. Si un document fait 600 lignes mais que toutes les Définitions sont déjà nommées et destinées à être réutilisées dans d'autres cours, atomiser dès la rédaction est légitime (passer `--force`).

## Architecture cible après atomisation

```
Nom_Cours/
├── Nom_Cours.tex                 ← fichier principal (inchangé)
├── enonce.tex                    ← orchestration pure : \section + \subsection + \input
├── enonce_figures.tex            ← figures TikZ (inchangé)
└── sections/
    ├── Definition/
    │   ├── def01_variable_aleatoire_reelle.tex
    │   ├── def02_loi_de_probabilite.tex
    │   └── ...
    ├── Propriete/
    │   ├── prop01_linearite_de_l_esperance.tex
    │   └── ...
    ├── Theoreme/
    ├── Demonstration/
    │   ├── demo01.tex                              ← pas de titre → numéro seul
    │   └── demo02_variance_transformation_affine.tex
    ├── Exemple/
    │   └── exempleNN_<slug>.tex
    ├── Remarque/
    ├── Notation/
    └── EXO/
        ├── exo01_1sp22_tirage_d_une_boule_numerotee.tex
        ├── exo02_1sp22_salaires_d_une_entreprise.tex
        └── ...
```

### Convention de nommage

Pour chaque type, un compteur `NN` à deux chiffres (ordre d'apparition) + un slug ASCII issu du titre :

| Cas | Pattern | Exemple |
|---|---|---|
| Didactique classique | `<prefix><NN>_<slug>.tex` | `def01_variable_aleatoire_reelle.tex` |
| Didactique sans titre | `<prefix><NN>.tex` | `demo01.tex` |
| EXO complet | `exo<NN>_d<diff>_<code>_<slug>.tex` | `exo01_d1_1sp22_tirage_d_une_boule_numerotee.tex` |
| EXO difficulté décimale | `exo<NN>_d<diff>_<code>_<slug>.tex` | `exo15_d2-5_1sl19_duree_avant_la_premiere_panne.tex` |
| EXO sans `\def\rdifficulty` | `exo<NN>_<code>_<slug>.tex` | `exo03_1sp24_intitule.tex` |
| EXO sans code | `exo<NN>_d<diff>_<slug>.tex` | `exo02_d1_intitule.tex` |
| Collision (rare) | `<prefix><NN>_<slug>_v2.tex` | `def03_esperance_v2.tex` |

Préfixes : `def`, `prop`, `theo`, `lem`, `cor`, `demo`, `exemple`, `meth`, `rem`, `not`, `act`, `hist`, `graph`, `conj`, `algo`, `exo`. Un type non listé reçoit `type.lower()` comme préfixe.

### Cas particulier des EXO

Les `EXO` sont typiquement précédés d'une ligne `\def\rdifficulty{N}` qui pilote la coche de difficulté affichée. Cette ligne **fait sémantiquement partie de l'exercice** : le script l'absorbe automatiquement dans le fichier atomisé ET l'utilise pour enrichir le nom de fichier. Concrètement, pour :

```latex
\def\rdifficulty{1.5}
\begin{EXO}{Lecture d'une loi}{1SP20}
...
\end{EXO}
```

le fichier produit `sections/EXO/exo03_d1-5_1sp20_lecture_d_une_loi.tex` contient bien les deux lignes (à partir du `\def`). Le `enonce.tex` voit juste `\input{sections/EXO/exo03_d1-5_1sp20_lecture_d_une_loi.tex}` à la place.

Trois informations sont intégrées au nom de fichier dans cet ordre :

1. **`d<difficulty>`** issu de `\def\rdifficulty{X}`. Le `.` est remplacé par `-` (1.5 → `d1-5`) car les `.` rendent les globs Unix moins lisibles et perturbent certains outils.
2. **`<code_competence>`** issu du 2e argument `{1SP20}` (en minuscules : `1sp20`).
3. **`<slug>`** issu du 1er argument (titre, normalisé ASCII).

Cet ordre est choisi pour le filtrage interactif :

| Commande | Trouve |
|---|---|
| `ls sections/EXO/exo*_d1_*` | Tous les exos de difficulté 1 |
| `ls sections/EXO/exo*_d2-5_*` | Tous les exos de difficulté 2.5 |
| `ls sections/EXO/exo*_*_1sp22_*` | Tous les exos de la compétence 1SP22 |
| `ls sections/EXO/exo*` | Tous les exos, triés par ordre d'apparition (NN) |

Si un EXO n'a pas de `\def\rdifficulty` au-dessus, ce n'est pas un problème : le script détecte l'absence, omet le token `d<X>` du nom de fichier, et démarre simplement au `\begin{EXO}`.

Le slug est tronqué à 40 caractères, en ASCII minuscule, ponctuation et accents normalisés en `_`. Cela évite les chemins à accents — qui posent des problèmes `charmap`/`cp1252` sur Windows — sans rien perdre du sens.

## Script `atomize_didactic.py`

```bash
python ".claude/skills/bfcours-latex/scripts/atomize_didactic.py" --enonce <chemin/enonce.tex> [options]
```

### Options

| Option | Effet |
|--------|-------|
| `--enonce <path>` | Chemin vers le `enonce.tex` cible (obligatoire). |
| `--dry-run` | Affiche le plan d'extraction (numéros de ligne, fichiers cibles) sans rien modifier. **Toujours commencer par un dry-run.** |
| `--threshold N` | Seuil de lignes en-dessous duquel l'atomisation est refusée (défaut : 1000). |
| `--force` | Bypass du seuil. |
| `--exclude-exo` | Ne PAS atomiser les `EXO` (rare : par défaut ils sont atomisés au même titre que les Définitions). |
| `--include-exo` | [OBSOLÈTE] Compatibilité ; sans effet (EXO atomisé par défaut). |
| `--types T1,T2` | Liste explicite des types à atomiser (remplace la liste par défaut). |
| `--verbose` | Détaille chaque fichier écrit. |

### Sécurité

- **Backup automatique** : `enonce.tex.bak.<timestamp>` créé avant toute modification. Le restaurer en cas de problème.
- **Idempotence** : ré-exécuter le script sur un fichier déjà atomisé est sans effet (les blocs déjà extraits ont disparu du fichier).
- **Refus de collision** : si le fichier cible existe déjà, le script ajoute `_v2`, `_v3`... jamais d'écrasement silencieux.
- **Préservation stricte** : le contenu de chaque bloc (espaces, sauts de ligne, indentation, `\vspace` accolés) est extrait octet pour octet. Le pipeline `atomize → monolithize` est mathématiquement l'identité.

### Détection des blocs : algorithme

Le parseur suit `\begin{X}` / `\end{X}` avec une pile, en ignorant ce qui suit un `%` non échappé. Un bloc didactique est extrait **uniquement si la pile est vide** au moment de son `\begin` : cela garantit qu'une `Definition` imbriquée dans un `EXO` ou dans une autre `Definition` reste inline (elle fait partie sémantique de son contenant).

Concrètement, sur ce code :

```latex
\begin{EXO}{...}{}
\begin{Definition}[Définition contextuelle]
...
\end{Definition}
\end{EXO}
```

la `Definition` n'est **pas** extraite (elle est imbriquée dans `EXO`). Tandis qu'une `Definition` au niveau du `\section{}` est extraite.

### Limites connues

- Les environnements définis par `\newenvironment` qui ne portent pas l'un des noms reconnus ne sont pas atomisés (utiliser `--types` pour les ajouter).
- Le script ne ré-équilibre pas les sous-dossiers : si un même type contient 50 fichiers, il reste à plat. Une réorganisation thématique manuelle reste possible.
- Les `\input` relatifs à d'autres dossiers (`figures/`, `annexes/`) ne sont pas touchés.

## Script `monolithize_didactic.py`

Opération inverse : résout récursivement les `\input{sections/...}` pour reconstituer un `enonce.tex` monolithique.

```bash
python ".claude/skills/bfcours-latex/scripts/monolithize_didactic.py" --enonce <chemin/enonce.tex> [options]
```

### Options

| Option | Effet |
|--------|-------|
| `--enonce <path>` | Chemin du `enonce.tex` (obligatoire). |
| `--inplace` | Écrase le fichier source (avec backup horodaté). |
| `--output <path>` | Chemin de sortie (défaut : `<enonce>.monolith.tex`). |
| `--pattern <glob>` | Motif glob des inputs à résoudre (défaut : `sections/*`). Utiliser `*` pour tout résoudre. |
| `--cleanup` | Après écriture, supprime les fichiers `sections/<Type>/*.tex` qui ont été inlinés et les dossiers vides. Nécessite `--inplace`. |
| `--verbose` | Détaille chaque fichier inliné. |

### Cas d'usage

1. **Partage d'archive autonome** : produire un `enonce.tex` auto-suffisant à zipper :
   ```bash
   python monolithize_didactic.py --enonce ./Cours/enonce.tex --output ./Cours/enonce_archive.tex
   ```
2. **Re-monolithisation avant gros refactor** : aplatit le cours pour intervenir en un seul fichier, puis re-atomiser :
   ```bash
   python monolithize_didactic.py --enonce ./Cours/enonce.tex --inplace --cleanup
   # ... refactor ...
   python atomize_didactic.py --enonce ./Cours/enonce.tex --force
   ```
3. **Ciblage** : ne résoudre que les Définitions, conserver les Exemples atomisés :
   ```bash
   python monolithize_didactic.py --enonce ./Cours/enonce.tex --pattern "sections/Definition/*"
   ```

### Garanties

- Protection anti-cycle (si un fichier inliné `\input` lui-même, warning + skip).
- Préservation des `enonce_figures.tex` et `annexes/` (filtrés par `--pattern` qui par défaut ne cible que `sections/*`).
- Les `\input` commentés (`%\input{...}`) sont ignorés.

## Workflow d'édition complet (avec ou sans atomisation)

### A. Fichier court (< 1000 lignes) — édition directe

1. Read `enonce.tex` (ou Grep si on cherche un pattern précis).
2. Edit / MultiEdit le bloc visé.
3. Déléguer compilation à `tex-compiling-skill`.

### B. Fichier long (≥ 1000 lignes) — pré-atomiser

1. Lancer `atomize_didactic.py --dry-run` pour visualiser le plan.
2. Lancer sans `--dry-run` : `enonce.tex` raccourcit, les blocs vont dans `sections/`.
3. Compiler une fois pour valider la stabilité (le PDF doit être strictement identique au précédent).
4. Travailler ensuite par fichiers ciblés : on Read uniquement le `sections/<Type>/<fichier>.tex` qui nous intéresse — gain massif de contexte.

### C. Document atomisé reçu / à partager — monolithiser

1. Lancer `monolithize_didactic.py --output enonce_share.tex`.
2. Le `.tex` produit est auto-suffisant : copiable seul dans une archive.
3. Ou `--inplace --cleanup` pour fusionner définitivement (avec backup).

## Tests de validation

Les scripts ont été testés sur :

- **Fixture synthétique** (`scripts/tests/fixture_enonce.tex`) couvrant : titres `[opt]` et `{obl}`, EXO avec et sans `\def\rdifficulty`, imbrications (MultiColonnes, tcbenumerate, center, crep), `Definition` imbriquée dans `EXO` (NON extraite séparément), commentaires LaTeX, `\input` préexistant, codes compétence. **Round-trip strict octet pour octet** (2183 chars).
- **`Cours_Variables_Aleatoires_Reelles/enonce.tex`** (1070 lignes) :
  - 38 blocs détectés (5 Definitions, 8 Exemples, 3 Propriétés, 2 Démonstrations, 3 Remarques, 1 Notation, **16 EXO**).
  - Réduction à 122 lignes (-89%).
  - Compilation LuaLaTeX réussie sans modification de rendu.
  - Round-trip strict octet pour octet (40548 chars).
  - Les `\def\rdifficulty{...}` sont bien absorbés dans les fichiers `sections/EXO/exo*.tex`.

Si tu modifies les scripts, lance d'abord le test fixture :

```bash
python ".claude/skills/bfcours-latex/scripts/atomize_didactic.py" \
  --enonce ".claude/skills/bfcours-latex/scripts/tests/fixture_enonce.tex" \
  --dry-run --force --verbose
```

et vérifie que la sortie liste exactement **8 blocs** (Definition, Propriete, Exemple, 2 EXO avec `\def\rdifficulty` absorbé, Remarque, EXO sans `\def\rdifficulty`, Demonstration) — sans la Definition imbriquée dans le premier EXO, ni la fausse Definition commentée.
