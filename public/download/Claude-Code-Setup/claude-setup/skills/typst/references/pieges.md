# Pièges de Typst 0.15, avec le message exact et la correction

Chaque piège a été reproduit avec Typst 0.15. Format : ce qu'on écrit → ce qui se passe → ce qu'il faut écrire.

## Erreurs de compilation

| On écrit | Message | Correction |
|---|---|---|
| `$ABC$` | `unknown variable: ABC` (indice : ajouter des espaces) | `$A B C$` ; un mot en texte : `$"aire"$` |
| `$lr(] -oo ; 3])$` (`;` dans l'appel d'une fonction de maths) | `expected content, found array` | dans un appel en maths, `;` sépare des lignes : `";"` |
| `#box(width: 2ex)` | `invalid floating point number: 2e` (indice : suffixe `x`) | pas d'unité `ex` : `1em` = deux `ex` environ |
| `#counter(page).get()`, `state.get()`, `measure(…)`, `here()` | `can only be used when context is known` | `#context counter(page).get()` ; une fonction renvoie `context …` |
| `_a_b` au milieu d'un mot, `x_1` en texte | `unclosed delimiter` | `\_` ou `$x_1$` ; italique dans un mot : `#emph[a]b` |
| `#"x" * 3`, `#a * b` | `unclosed delimiter` (l'étoile ouvre le gras) | `#("x" * 3)` |
| `#f[z](b: 2)` | `expected function, found content` | les parenthèses d'abord : `#f(b: 2)[z]` |
| `#image("../img.png")` | `path "../img.png" would escape the project root` | compiler avec une racine plus haute (`--racine`) ; `/x.png` part de la racine |
| `#image("/img.png")` | `file not found (searched at …)` | le chemin absolu part de la racine, pas du disque |
| `#import "@preview/cetz:9.9.9"` | `package found, but version 9.9.9 does not exist (latest is 0.5.2)` ; hors ligne, une version absente du cache échoue au téléchargement | prendre une version déjà dans `%LOCALAPPDATA%/typst/packages/preview/<nom>/` |
| `#set text(font: "Inexistante")` | avertissement `unknown font family` (le texte sort dans une police de repli) | vérifier le nom, ou passer le dossier de la police par `--font-path` |
| un nom défini plus bas dans le fichier | `unknown variable` | une fonction ne voit que les `#let` écrits AVANT elle |
| `().join()` utilisé comme chaîne (tri, concaténation) | `cannot compare string and none` | un tableau vide joint donne `none` : `if a.len() > 0 { a.join() } else { "" }` |

## Rendus faux sans erreur

| On écrit | On obtient | Correction |
|---|---|---|
| `$3,14$` | « 3, 14 » (espace après la virgule) | `$3","14$`, ou une fonction de nombres |
| `$[0 ; 1]$` | « [0; 1] » collé | `$[0 thin; thin 1]$` |
| `$0","135 / 0","15$` (quotient de décimaux) | « 0, 135/0 ,15 » : la fraction ne prend que les morceaux voisins du `/` | barre en ligne `$0","135 \/ 0","15$`, ou parenthèses `$(0","135)/(0","15)$` |
| `$]-oo thin; thin 3]$` | « ] − ∞ » : moins binaire espacé | `$lr(] -oo thin";" thin 3 ])$` |
| `#str(3) + "a"` | « 3 + « a » » : seul `#str(3)` est du code | `#(str(3) + "a")` |
| `#a-b` (soustraction voulue) | la variable `a-b` (le tiret fait partie des noms) | `#(a - b)` |
| `[#set text(fill: red); x] suite` | les crochets s'affichent ET le rouge s'applique à toute la suite | `#[#set text(fill: red); x]` borne la portée |
| `#f(x) [y]` (espace) | `f(x)`, puis « [y] » en texte | `#f(x)[y]` |
| `#pascalc` (fonction sans argument, sans parenthèses) | le nom de la fonction s'affiche en police machine | `#pascalc()` |
| `#f (x)` (espace avant la parenthèse) | « f (x) » en texte, la fonction n'est pas appelée | aucun espace entre le nom et `(` ou `[` |
| formule centrée trop longue | déborde dans la marge (les équations centrées ne se coupent pas) | couper en plusieurs lignes avec `\` et `&` |
| `sys.inputs.correction == true` | toujours faux : les entrées sont des CHAÎNES | `== "true"` |
| `$1/2$` en ligne | fraction réduite | `$display(1/2)$` si on la veut grande |
| `"guillemets"` sans `lang: "fr"` | “guillemets” anglais | `#set text(lang: "fr")` → « guillemets » |
| `@etiquette` vers un titre | « Chapitre 1 » ou « Section 1 » selon la langue | `#link(<etiquette>)[texte]` pour un texte libre |

## Habitudes LaTeX à perdre

- **Pas de deuxième passe** : références, compteurs et totaux sont justes dès la première compilation.
- **Pas de `\vspace` négatif** : il compensait un blanc que Typst ne produit généralement pas ; le reporter crée des chevauchements.
- **Pas de `%` en fin de ligne** pour tuer une espace : un saut de ligne simple dans le markup est une espace ; dans un appel en mode code, les sauts de ligne ne comptent pas.
- **Pas de macro qui « avale » la suite** : une fonction reçoit ses arguments entre `()` et `[]`, rien d'autre.
- **Les blocs de contenu `[…]` sont du markup** : on peut y mettre des paragraphes, des listes, des maths.
- **Un paragraphe vide** (ligne vide) au milieu d'un argument `[…]` crée un vrai paragraphe : utile, mais une ligne vide parasite ajoute de l'espace.
