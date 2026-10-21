# Guider un nouvel utilisateur vers sa façade

Une **façade** est un petit paquet `@local` qui réexporte toute la suite `farfadet` et pose, une fois pour toutes, les défauts d'un professeur : son identité (établissement, nom, logo, année…), son en-tête, son pied de page, le rendu de ses environnements et de ses tableaux. Ses documents n'importent plus que ce paquet :

```typ
#import "@local/ma-facade:0.1.0": *
#show: cours(niveau: "2nde", theme: [Vecteurs du plan])
```

Le modèle à copier est livré avec la suite : `farfadet-modele/exemples/ma-facade/` (dossier de la suite donné par `localiser.py --json`). Il contient `lib.typ` (quatre sections à adapter), `logo.svg`, `document-demo.typ` et un `LISEZMOI.md`. On **part toujours de cette copie** : on ne réécrit pas une façade de mémoire.

Toutes les clés citées ici : `chercher.py --fiche chapitre`, `--fiche pied-de-page`, `--fiche setbfmodele` ; le guide de `farfadet-modele`, chapitre « Personnaliser l'identité et l'en-tête ».

## Étape 1 — Poser les questions

Poser les questions **en une seule fois**, avec une valeur proposée pour chacune, pour que l'utilisateur n'ait qu'à corriger. Ne rien inventer : un champ sans réponse reste vide (il ne s'affiche pas).

| Question | Clé | Proposition par défaut |
|---|---|---|
| Nom du paquet ? | `name` de `typst.toml`, dossier d'installation | `ma-facade` (sans accent ni espace) |
| Établissement, cycle ? | `etablissement`, `cycle` | — , `[Lycée]` ou `[Collège]` |
| Votre nom, tel qu'il doit apparaître ? | `professeur` | — |
| Académie, année scolaire, discipline ? | `academie`, `annee`, `matiere` | — , `[2026-2027]`, `[Mathématiques]` |
| Un logo ? Où est le fichier ? | `logo` | aucun (`none`) |
| Mention de pied de page (licence…) ? | `mentions` | aucune |
| Quel en-tête ? Montrer les quatre rendus (étape 2) | `rendu` | `"bf"` (rendu de bfcours) |
| Quels champs dans l'en-tête ? | `champs` | ceux du rendu |
| Une couleur dominante ? | `couleur-filet`, `couleur-titre` | aucune (rendu d'origine) |
| Quel pied de page ? | `disposition`, `gauche`, `centre`, `droite` | `"bfcours"` (disque du numéro) |
| Des skins pour les environnements ? | `setbfenvironments(pour: …, rendu: …)` | aucun (rendu `"bf"`) ; voir `references/skins.md` |
| Tableaux centrés ? | `setbftableaux(align: center)` | non |
| Jeu de titres ? | `titres` | `"bfcours"` |

## Étape 2 — Montrer avant de choisir

Pour l'en-tête, compiler un petit essai qui montre les quatre rendus avec SES données, et lui envoyer l'image : il choisit sur pièce.

```typ
#import "@preview/farfadet:0.2.0": *
#setbfmodele(pour: "identite", etablissement: […], professeur: […], annee: […])
#chapitre(niveau: "2nde", theme: [Rendu « bf »])
#chapitre(niveau: "2nde", theme: [Rendu « rd »], rendu: "rd")
#chapitre(niveau: "2nde", theme: [Rendu « sobre »], rendu: "sobre")
#chapitre(niveau: "2nde", theme: [Rendu « encadre »], rendu: "encadre")
#chap-eval(niveau: "2nde", theme: [Une évaluation], rendu: "encadre")
```

- `"bf"` : bandeau gris de bfcours ; `"rd"` : bandeau dégradé de rdboites ; `"sobre"` : une ligne, un filet fin ; `"encadre"` : cadre fin à trois cases (identité | titre | niveau, classe, année).
- Un rendu qui ne lui convient qu'à moitié se règle : `champs: (droite: ("logo", "professeur", "annee"))`, couleurs, polices, `largeurs`.
- Un dessin vraiment à lui : une fonction `d => contenu` (contrat dans `chercher.py --fiche chapitre` et le guide de `farfadet-modele`). La lui proposer seulement s'il la demande.

Cet essai est jetable : le placer dans un dossier temporaire et le supprimer ensuite.

## Étape 3 — Produire le paquet

1. **Copier** `farfadet-modele/exemples/ma-facade/` dans le dossier que l'utilisateur indique (sinon, le lui demander : c'est un dossier qu'il gardera). Renommer le dossier comme le paquet.
2. **`typst.toml`** : `name`, `authors`, `description`. Garder `version = "0.1.0"` et `entrypoint = "lib.typ"`.
3. **`lib.typ`** : remplir les sections 1 à 4, **et rien d'autre** (les fonctions `mes-reglages`, `cours`, `evaluation`, `exercices` ne se modifient pas).
   - Section 1, `mon-identite` : ses réponses. Le logo : copier son fichier dans le dossier du paquet et écrire `logo: image("nom-du-fichier.png")` ; le chemin est lu depuis `lib.typ`, le logo voyage avec le paquet. Sans logo : `logo: none`, et retirer `"logo"` des `champs`.
   - Section 2, `mon-entete`, `mon-pied` : le rendu choisi et ses réglages. Une zone du pied est un texte (`[…]`) ou une liste de champs (`("professeur", "annee")`) ; à éviter : `centre` avec la disposition `"bfcours"` (il chevauche la zone de droite).
   - Section 3, `mes-environnements` : skins et tableaux. Retirer les lignes qu'il n'a pas demandées.
   - Section 4, `mes-defauts` : clés de `modele("cours", …)` (`titres`, `fontsize`…).
4. **Un nom de champ est entre guillemets, un texte libre entre crochets** : `("professeur", [Bureau 12])`. Un nom inconnu arrête la compilation et liste les champs possibles.
5. **Ne jamais toucher aux paquets de la suite** pour personnaliser : tout passe par la façade.

## Étape 4 — Installer en `@local`

Typst cherche les paquets personnels dans :

| Système | Dossier |
|---|---|
| Windows | `%APPDATA%/typst/packages/local/<nom>/0.1.0/` |
| macOS | `~/Library/Application Support/typst/packages/local/<nom>/0.1.0/` |
| Linux | `~/.local/share/typst/packages/local/<nom>/0.1.0/` |

Deux façons, à proposer :

- **Lien** (recommandé : une retouche de la façade est vue tout de suite). Windows, en PowerShell :
  ```powershell
  New-Item -ItemType Directory -Force "$env:APPDATA/typst/packages/local/<nom>" | Out-Null
  New-Item -ItemType Junction -Path "$env:APPDATA/typst/packages/local/<nom>/0.1.0" -Target "<chemin complet du dossier>"
  ```
  macOS ou Linux : `mkdir -p <dossier>/<nom> && ln -s "<chemin complet>" <dossier>/<nom>/0.1.0`.
- **Copie** (figée) : copier le contenu du dossier dans `<dossier>/<nom>/0.1.0/`. À refaire après chaque retouche.

`@preview/farfadet:0.2.0` doit déjà être installé (`localiser.py` le dit).

## Étape 5 — Vérifier

1. Écrire, dans le dossier de travail de l'utilisateur, un document d'essai qui n'importe que la façade (partir de `document-demo.typ` en changeant l'import en `@local/<nom>:0.2.0`).
2. Compiler les deux versions et regarder les images :
   ```bash
   python "<skill>/scripts/compiler.py" "dossier/essai.typ" --png
   ```
3. Contrôler sur l'image : l'en-tête porte le bon rendu, le logo et les bons champs ; le pied porte les champs voulus sans chevauchement ; les environnements ont leurs skins ; la version élève n'a pas de réponse visible.
4. Montrer une surcharge pour un seul document, pour qu'il sache garder la main :
   ```typ
   #show: cours(niveau: "Tle", theme: […], rendu: "sobre", classe: [T#super[le] 2])
   #setbfmodele(pour: "chapitre", rendu: "rd")   // la suite de CE document
   ```
5. Fin : `compiler.py essai.typ --nettoyer`, et supprimer l'essai s'il n'est pas à garder.

## Pièges

- **Réglages après le modèle** : dans la façade, `mes-reglages()` est appelé AVANT `modele(…)` ; c'est ce qui permet au bandeau de les voir. Ne pas inverser.
- **Clé du bandeau dans `cours(…)`** : seules l'identité, `rendu`, `skin` et `champs` passent par le modèle. Les autres clés de l'en-tête (`couleur-filet`, `hauteur`…) se règlent par `setbfmodele(pour: "entete", …)` : sinon, « clé inconnue … pour « bfcours » ».
- **Un champ réglé ne s'affiche pas tout seul** : le rendu `"bf"` ne montre que niveau, titre et zone de droite ; pour y voir le professeur : `champs: (droite: ("professeur", "annee"))`.
- **Logo trop grand ou trop petit** : `hauteur-logo` (en-tête) ; dans le pied, `setbfmodele(pour: "pied-de-page", hauteur-logo: 0.8em)`.
