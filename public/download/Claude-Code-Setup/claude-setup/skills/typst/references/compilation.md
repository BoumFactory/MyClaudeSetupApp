# Compiler un document Typst

## Les trois moyens

| Moyen | Quand | Commande |
|---|---|---|
| Script du skill (module pip `typst`, à installer par `pip install typst`) | par défaut, pour un agent | `python "<skill>/scripts/compiler.py" doc.typ [--png <dossier>] [--input clé=valeur]` |
| CLI de Tinymist (même compilateur, syntaxe de `typst compile`), ou CLI `typst` si elle est installée | en ligne de commande pure | `tinymist compile doc.typ sortie.pdf --font-path "<polices>" --input correction=false --root "<racine>"` (l'exécutable de Tinymist est dans le dossier de l'extension VS Code, sous `out/`) |
| Aperçu Tinymist dans VS Code | à l'écriture, recompilation à chaque frappe | réglages `tinymist.fontPaths` et `tinymist.preview.fontPaths` (chemins à `/`) |

Un binaire `typst` n'est pas forcément dans le PATH : le module pip suffit. Pour un document farfadet, le skill `bfcours-typst` donne `compiler.py` (versions professeur et élève, extraits LaTeX) ; le script de ce skill-ci compile une seule version et affiche les erreurs avec leur position.

## Où écrire les fichiers

- Le PDF d'un document va dans le dossier du document (défaut du script : à côté du `.typ`).
- Les essais (`.typ` de test, PDF et PNG de contrôle) vont dans un dossier temporaire de session, avec le chemin **complet** : `-o "<dossier temporaire>/essai.pdf" --png "<dossier temporaire>/png"`.
- Interdit : racine d'un disque, dossier personnel, `Documents`, Bureau, Téléchargements, et tout chemin raccourci tapé à la main (`C:/NOMCOU~1/…`). Le script de ce skill refuse ces destinations ; en appelant `typst` ou `tinymist` directement, appliquer soi-même la règle.

## Options qui comptent

- **`--font-path` / `font_paths`** : dossiers de polices ajoutés aux polices système. Les paquets farfadet utilisent les polices du dossier `polices/` de la suite (Erewhon, Erewhon Math, Latin Modern Sans, TeX Gyre Heros, Font Awesome ; dossier donné par `bfcours-typst/scripts/localiser.py`, ou variable `BFCOURS_TYPST_POLICES`). Ce dossier est recommandé (rendu Erewhon) mais facultatif : sans lui, Typst compose avec ses polices intégrées (Libertinus Serif, New Computer Modern Math) et les formules ont la bonne taille. Le script l'ajoute quand il le trouve ; une police inconnue donne seulement l'avertissement `unknown font family`.
- **`--input clé=valeur` / `sys_inputs`** : valeurs lues dans le document par `sys.inputs.at("clé", default: "…")`. Ce sont des **chaînes** (`"true"`, pas `true`). Sert à produire plusieurs versions d'un même fichier (professeur et élève).
- **`--root` / `root`** : racine du projet. Aucun fichier hors de la racine n'est lisible (`would escape the project root`), et un chemin qui commence par `/` part d'elle. Le script prend par défaut le dossier du fichier ; `--racine` la remonte.
- **PNG** : `format="png"`, `ppi=…`, sortie avec un motif de page (`page-{0p}.png`). Le script écrit `page-1.png`, `page-2.png`… (ou `page-01.png` au-delà de 9 pages) dans le dossier donné, après avoir vidé les anciennes pages.

## Lire une erreur

```text
ÉCHEC de la compilation

error: unknown variable: ABC
   ┌─ C:\…\t1.typ:35:12
   │
35 │ $A B C$ et $ABC$
   │             ^^^
   │
   = hint: if you meant to display multiple letters as is, try adding spaces between each letter: `A B C`
```

1. `error:` : la cause. `warning:` : la compilation a réussi mais quelque chose est suspect (police, étiquette).
2. `fichier:ligne:colonne` : l'endroit exact ; le soulignement `^^^` montre l'expression fautive. Si le fichier est celui d'un **paquet** (`@local/…`), l'erreur vient souvent d'un argument mal formé dans TON appel : remonter la `trace` (« error occurred in this call of function … »), qui pointe la ligne du document.
3. `hint:` : souvent la correction exacte.
4. Une seule erreur est affichée à la fois quand elles s'enchaînent : corriger, recompiler.

Le module pip seul (`typst.compile`) lève `typst.TypstError` dont `str(e)` ne contient que le message ; la position est dans `e.diagnostic`, les indices dans `e.hints`, la pile d'appels dans `e.trace`. `typst.compile_with_warnings(…)` renvoie aussi les avertissements.

## Regarder le résultat

Une compilation réussie ne garantit pas la mise en page : débordements, formules trop petites, pages blanches ne lèvent aucune erreur. Produire les PNG (`--png`, 100 à 130 ppi suffisent) et les regarder avec l'outil Read avant de livrer. Pour comparer deux versions page à page, assembler les PNG côte à côte avec Pillow.
