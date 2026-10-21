# Skins : changer la forme des environnements d'un cours

Un **skin** est une forme de boîte pour un environnement didactique (`definition`, `propriete`, `theoreme`, `exemple`, `methode`, `remarque`…). Numérotation, renvois `@…`, sommaire, cartes Anki et version prof/élève restent ceux de bfcours : le skin ne dessine que la boîte. Tous les types l'acceptent, sauf `neutre`.

Tout se règle par la clé `rendu` (et `skin:` pour les options). Pour **écrire un skin**, le contrat est dans `skins/CONTRAT.md` du paquet `farfadet-didactique` (`localiser.py --json` donne le dossier de la suite). Guide illustré : chapitres « Les skins » et « Écrire ses propres skins » de `docs/farfadet-didactique.pdf`.

## Les trois rendus (clé `rendu`)

| Valeur | Effet |
|---|---|
| `"bf"` (défaut) | rendu d'origine de bfcours |
| `"rd"` | boîtes de `rdboites` ; honore `couleur`, `colback`, `colframe`, `coltitle`, `arc`… quand ils sont réglés |
| un skin | nom intégré, nom enregistré par `setbfskins`, ou fonction `d => contenu` (dont `bfskin(…)`) |

## Les sept skins intégrés

Génériques (aucun texte propre à un type), sécables, fond du corps blanc (sauf `colback` demandé) ; honorent `couleur`, `colback`, `colframe`, `coltitle` et la clé `icone`. Option inconnue : la compilation s'arrête et liste les options.

| Nom | Dessin | Options (défaut) |
|---|---|---|
| `"cahier"` | surligneur, titre souligné d'un trait ondulé, filet de stylo | `icone` (`"etoile5"`), `epaisseur` (`1.3pt`) |
| `"outil"` | compartiment de boîte à outils, trait épais en bas | `icone` (`"roue"`), `epaisseur` (`2.6pt`) |
| `"pastille"` | pastille ronde à icône blanche, corps en pointillés | `icone` (`"implique"`), `epaisseur` (`0.9pt`) |
| `"manchette"` | colonne gauche étroite contre un filet ; se replie en colonne étroite ou titre long | `icone` (`"equerre"`), `largeur` (`3cm`), `repli` (`10cm`), `lignes-max` (`5`), `epaisseur` (`0.6pt`) |
| `"filet"` | cadre fin à coins arrondis, légende dans le filet du haut | `icone` (`"etoile"`), `epaisseur` (`0.7pt`), `rayon` (`5pt`) |
| `"suspendu"` | disque à icône blanche suspendu dans un retrait, filet vertical | `icone` (`"cle"`), `epaisseur` (`1pt`), `retrait` (`1.2cm`) |
| `"minimal"` | étiquette et titre seuls : le nom du type (et son numéro) en gras de la couleur de l'environnement, puis le titre en gras (noir par défaut), le corps dessous ; ni filet, ni cadre, ni icône | `icone` (`none`) |

Les noms `bf`, `rd` et ces sept noms sont réservés : `setbfskins` les refuse.

### Le skin `minimal`

Le rendu le plus discret : celui des collègues qui ne veulent que l'étiquette et le titre. Un simple bloc, sécable, sans retrait. `couleur` donne l'encre du nom et du numéro, `coltitle` celle du titre (noir par défaut), `colback` ajoute un fond au corps ; `colframe` et `embleme` sont sans effet (pas de cadre, pas d'icône par défaut). Source : `farfadet-didactique/src/galerie/minimal.typ`, guide : `farfadet-didactique/docs/guide.typ`, section « minimal ».

```typ
#setbfenvironments(rendu: "minimal")                                               // tous les environnements
#theoreme(rendu: "minimal", numero: true, coltitle: rgb("#1b5e20"))[Titre vert][Le titre prend la couleur de `coltitle`.]
#theoreme(rendu: "minimal", skin: (icone: "etoile"))[Avec icône][L'icône est remise sur demande.]
```

## Les douze icônes

`"coche"`, `"etoile"` (4 branches), `"etoile5"`, `"coeur"`, `"cle"`, `"roue"`, `"implique"`, `"fanion"`, `"equerre"`, `"attention"`, `"loupe"`, `"fleche"`.

L'option `icone` accepte : un de ces noms (nom inconnu : erreur qui les liste), une fonction `couleur => contenu`, un contenu (`[§]`), ou `none` : aucune icône (`pastille` et `suspendu` gardent alors un disque vide ; `minimal` n'en a jamais, sauf demande). Pour retirer l'icône d'un environnement quel que soit son skin : `skin: (icone: none)`. La clé `icone` de bfcours, quand elle est réglée, l'emporte sur l'option.

```typ
#propriete(rendu: "outil", skin: (icone: "cle"))[Titre][Corps.]
#propriete(rendu: "outil", skin: (icone: none))[Titre][Corps.]                  // aucune icône
#propriete(rendu: "outil", skin: (icone: c => text(fill: c, weight: "bold")[§]))[Titre][Corps.]
#theoreme(rendu: "suspendu", icone: [§])[Titre][Corps.]      // clé de bfcours : l'emporte
```

## L'emblème de chaque type (clé `embleme`)

Chaque type a une icône préférentielle que TOUS les skins reprennent (au lieu de leur icône propre). Valeurs : nom d'icône, fonction `couleur => contenu`, contenu, `none` ou `"auto"` (pas d'emblème : icône propre du skin).

| Type | Emblème | Type | Emblème |
|---|---|---|---|
| `definition` | `cle` | `exemple` | `fleche` |
| `notation` | `etoile5` | `contre-exemple` | `attention` |
| `propriete` | `roue` | `demonstration` | `equerre` |
| `theoreme` | `coeur` | `solution` | `coche` |
| `remarque` | `loupe` | `activite` | `fanion` |

Les autres types (`methode`, `aide`, `vocabulaire`, `histoire`, `bf-env`, `cracked`, `boite`…) : `auto`.

```typ
#theoreme(rendu: "filet", embleme: "etoile")[Titre][Corps.]          // un objet
#setbfenvironments(pour: "Theoreme", embleme: "coeur")               // un type
#setbfenvironments(embleme: none)                                    // tout le document : icône propre de chaque skin
```

Priorité de l'icône d'un skin : 1. clé `icone` de bfcours ; 2. option `icone` du skin (`skin:` ou `bfskin(…, icone:)`) ; 3. `embleme` ; 4. icône propre du skin. Ainsi `bfskin("suspendu", icone: "cle")` garde la clé sur un Théorème. `embleme` n'agit pas sur le rendu `"bf"` ni sur le style `"rd"`. Un skin personnel : `(d.outils.icone-choisie)("<icône propre>", …)` applique cette priorité (`d.embleme` donne l'emblème brut).

## Choisir un skin (le binding)

```typ
#definition(rendu: "manchette")[Titre][Corps.]                          // un objet
#setbfenvironments(pour: "Definition", rendu: "manchette")             // un type, la suite du document
#setbfenvironments(pour: ("Propriete", "Theoreme"), rendu: "outil")     // plusieurs types
#setbfenvironments(rendu: "filet")                                      // tous les environnements
#setbfenvironments(pour: "Propriete", rendu: "outil", skin: (icone: "cle"))   // avec options
#setbfenvironments(definir: "maison", rendu: "filet", couleur: "teal")  // style nommé…
#propriete(style: "maison")[Titre][Corps.]                              // …appelé par style:
```

Un cours à trois skins :

```typ
#setbfenvironments(pour: "Definition", rendu: "manchette")
#setbfenvironments(pour: "Propriete", rendu: "outil")
#setbfenvironments(pour: "Theoreme", rendu: "filet")
```

Un type non réglé garde le rendu bf. Un `setbfenvironments` vaut pour toute la suite du document, même écrit dans un bloc.

Style `rd` avec couleurs : `#definition(rendu: "rd", couleur: "defi", colback: "white", colframe: "green")[Titre][Corps.]` (clé `rd: (…)` : prioritaire sur les clés traduites).

## Variantes : `bfskin` et `setbfskins`

```typ
bfskin(base, ..options)                         // -> skin (fonction d => contenu)
setbfskins(reinitialiser: false, ..skins)       // skins nommés : nom: fonction
```

- `base` : nom intégré ou enregistré, ou fonction skin. `"bf"` et `"rd"` sont refusés. Base inconnue : erreur à la première boîte affichée.
- `options` : arguments nommés (`icone: "cle"`, `epaisseur: 2pt`), ce sont celles du skin de base.

```typ
#setbfskins(cle-rouge: bfskin("suspendu", icone: "cle"))        // enregistrer, puis appeler par le nom
#setbfenvironments(pour: "Theoreme", rendu: "cle-rouge")
#setbfenvironments(pour: "Definition", rendu: bfskin("manchette", icone: "fanion"))   // directe
#definition(rendu: bfskin(mon-skin, icone: "attention"))[Titre][Corps.]              // base : une fonction
```

Priorité d'une option, du plus fort au plus faible : clé `icone` de bfcours (icône seulement) ; clé `skin:` (appel, style nommé, `setbfenvironments(pour:)`, `setbfenvironments`) ; options figées de `bfskin` ; défaut du skin (pour l'icône, l'emblème du type s'intercale avant le défaut du skin).

## Un skin personnel

Une fonction `d => contenu`. Lire le contrat avant d'écrire : le skin ne numérote pas, ne pose ni étiquette, ni entrée de sommaire, ni carte Anki, ne teste pas la version.

```typ
#let pense-bete(d) = {
  let o = (icone: "loupe") + d.options                     // options de la clé skin:, avec défauts
  block(width: 100%, breakable: d.breakable, inset: (left: 0.9em, y: 0.3em),
    stroke: (left: (paint: d.couleur, thickness: 2pt, dash: "dashed")), {
      (d.outils.icone)(o.icone)                            // icône du jeu commun, teinte de l'environnement
      h(0.35em)
      text(fill: d.couleur.darken(30%), weight: "bold", smallcaps(d.nom))
      if d.numero != none [ #d.numero]
      if d.titre != none [ — #d.titre]
      parbreak()
      d.corps
    })
}
#methode(rendu: pense-bete)[Titre][Corps.]                 // direct
#setbfskins(pense-bete: pense-bete)                        // ou enregistré, puis rendu: "pense-bete"
```

Champs de `d` : `type`, `nom`, `numero` (chaîne ou `none`), `titre` (contenu ou `none`), `corps`, `couleur`, `fond`/`cadre`/`couleur-titre` (`auto` si non réglés), `icone`, `embleme`, `breakable`, `avant`/`apres` (`auto` le plus souvent), `options`, `outils`, `auteur`, `explicites`, `r`. `d.outils` : `icone(nom, taille: 1em, couleur: auto, pastille: auto)`, `icone-choisie(defaut, taille:, couleur:, pastille:)` (priorité commune), `cadre-craie`, `trait-craie`, `souligner-craie`, `cercle-craie` (un appel de fonction d'un dictionnaire s'écrit `(d.outils.icone)(…)`).

Règles : `width: 100%`, `breakable: d.breakable`, tester `d.titre != none`, dériver les fonds de `d.couleur` (`lighten`, `darken`), fond du corps blanc, jamais de `layout` autour du corps. Essai : un petit document qui importe le skin et emploie chaque type, compilé par `compiler.py <doc>.typ --png`, puis regarder les images prof et élève.

## Son paquet de skins pour tous ses documents

Modèle complet : le dossier `exemples/mes-skins/` de la suite (`typst.toml`, `lib.typ`, `mon-skin.typ`, `document-exemple.typ`, `LISEZMOI.md`). Pour l'employer : le copier dans le dossier des paquets locaux de Typst, sous `local/mes-skins/<version>/` (`localiser.py` affiche ce dossier).

```typ
// lib.typ du paquet
#import "@preview/farfadet:0.2.0": bfskin, setbfenvironments, setbfskins
#import "mon-skin.typ": skin as pense-bete
#let alerte = bfskin("outil", icone: "attention", epaisseur: 4pt)
#let mes-reglages(doc) = {
  setbfskins(alerte: alerte, pense-bete: pense-bete)
  setbfenvironments(pour: "Definition", rendu: "cahier")
  setbfenvironments(pour: "Propriete", rendu: "outil")
  setbfenvironments(pour: "Theoreme", rendu: "filet")
  setbfenvironments(pour: "Remarque", rendu: "alerte")
  setbfenvironments(pour: "Methode", rendu: "pense-bete")
  doc
}
```

Dans un document, l'activation tient en une ligne, après `modele` :

```typ
#import "@preview/farfadet:0.2.0": *
#import "@local/mes-skins:0.2.0": mes-reglages
#show: modele("cours", niveau: "2nde", theme: [Vecteurs], type-document: "cours", cycle: [Lycée], etablissement: [du Parc])
#show: mes-reglages
```

Un paquet personnel n'a pas à recopier les sept skins intégrés : il les appelle par leur nom, ou en fait des variantes.

## Pièges

- `#show: mes-reglages` (sans parenthèses) : la fonction prend `doc`. Une fonction d'activation à paramètres s'écrit `#show: reglages-sobres(pour: (…))`.
- Une option écrite dans `skin:` pour un autre skin que le sien arrête la compilation : lire la liste affichée.
- `crep`/`tccrep` restent roses dans tous les skins (couleur des corrections, `setrdcrep(correction-color:)`) ; `acc` et `voc` suivent la teinte.
- `manchette` se replie en colonne étroite (`multi-colonnes`) : c'est voulu.
