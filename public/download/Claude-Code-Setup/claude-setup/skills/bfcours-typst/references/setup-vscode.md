# Installer et configurer l'environnement (VS Code, Tinymist, extension, extraits, skill)

Procédure à suivre quand l'utilisateur demande d'installer la suite, de configurer VS Code pour Typst, ou quand l'aperçu, le Ctrl+Maj+B ou les formules se comportent mal. Principe : **diagnostiquer d'abord, n'installer que ce qui manque, vérifier à la fin.** Le guide illustré destiné à l'utilisateur est `docs/installation.pdf` dans la suite.

## 1. Diagnostic

```bash
python "<skill>/scripts/localiser.py"            # ce qui est trouvé et ce qui manque
python "<skill>/scripts/localiser.py" --json     # idem, avec les chemins réels (suite, polices, installer)
python "<installer>" --verifier                  # bilan détaillé, ne modifie rien
```

- `<installer>` : la ligne « installer.py » de `localiser.py`, c'est-à-dire `<suite>/tools/installer.py`. Le lancer avec **le Python qui a le module `typst`**.
- `--verifier` marque chaque ligne `[ok]`, `[manque]` ou `[!]` : paquet `@preview/farfadet`, module `typst`, PyMuPDF, polices, réglages `tinymist.*`, extension, extraits de code, skill. Les extraits et le skill sont facultatifs (signalés, non comptés).
- Si `localiser.py` ne trouve pas la suite : demander à l'utilisateur où est le dépôt, ou définir `BFCOURS_TYPST_SUITE` (dossier du dépôt) ; pour des paquets rangés ailleurs, `TYPST_PACKAGE_PATH` (dossier qui contient `local/`) et `TYPST_PACKAGE_CACHE_PATH` (dossier qui contient `preview/`).

## 2. Installer ce qui manque, dans cet ordre

| Manque | Action |
|---|---|
| Typst et Tinymist | extension VS Code **Tinymist Typst** (embarque le compilateur et fournit l'aperçu) |
| Python, module `typst` | `python -m pip install typst pymupdf` (`pymupdf` : facultatif, images de contrôle de `compiler.py --png`, et allègement des PDF s'il est activé dans `bfwatch.json`, `"allegement": true`) |
| paquet `@preview/farfadet` et polices | `installer.ps1` (Windows : `powershell -ExecutionPolicy Bypass -File .\installer.ps1`) ou `sh installer.sh` (macOS, Linux), à la racine du dépôt. |
| extension VS Code et réglages | `python <installer> --vscode` |
| extraits de code | `python <installer> --snippets` |
| skill pour assistant IA | `python <installer> --skill` (l'installeur demande où le poser) ou `--skill "<dossier de skills>"` |

`--vscode` construit le `.vsix` et l'installe par `code --install-extension` ; si la commande `code` est introuvable, il laisse l'archive à côté de `installer.py` : l'installer par *Extensions, …, Install from VSIX…*. Il écrit aussi les réglages de polices et d'export manquants (§ 4) **en fusionnant**. `--snippets` copie `bfcours-typst.code-snippets` dans le dossier des extraits utilisateur (§ 3). `--skill` demande où poser le dossier du skill (par défaut le dossier de cours du projet, sinon le dossier global de l'assistant utilisé), le copie dans `<dossier de skills>/bfcours-typst/` et y écrit `chemin-suite.txt` (le dépôt à utiliser).

Après `installer.ps1` / `installer.sh`, `--vscode` ou une mise à jour de l'extension : **fermer puis rouvrir VS Code** (au minimum *Developer: Reload Window*) pour que Tinymist voie les polices et que l'extension soit chargée. Un nouveau skill ne se charge qu'au redémarrage de l'assistant.

## 3. Où vont les fichiers

| Fichier | Windows | macOS | Linux |
|---|---|---|---|
| `settings.json` utilisateur de VS Code | `%APPDATA%\Code\User\settings.json` | `~/Library/Application Support/Code/User/settings.json` | `~/.config/Code/User/settings.json` |
| extraits de code utilisateur | `%APPDATA%\Code\User\snippets\` | `~/Library/Application Support/Code/User/snippets/` | `~/.config/Code/User/snippets/` |
| paquets locaux de Typst | `%APPDATA%\typst\packages\local\` | `~/Library/Application Support/typst/packages/local/` | `$XDG_DATA_HOME` ou `~/.local/share/typst/packages/local/` |
| skill pour assistant IA (tous les projets) | Claude Code : `%USERPROFILE%\.claude\skills\` ; Codex, Gemini CLI : `%USERPROFILE%\.agents\skills\` | `~/.claude/skills/`, `~/.agents/skills/` | `~/.claude/skills/`, `~/.agents/skills/` |

VS Code Insiders et VSCodium ont leurs propres dossiers (`Code - Insiders`, `VSCodium`) : `installer.py` ne traite que « Code » ; pour les autres, faire les réglages à la main. Réglages d'un seul projet : `<projet>/.vscode/settings.json`. Pour limiter les extraits à un projet, copier le fichier dans `<projet>/.vscode/` (pas aussi dans les extraits utilisateur : propositions en double).

## 4. Réglages

### Tinymist (clés à poser dans `settings.json`)

| Clé | Valeur | Rôle |
|---|---|---|
| `tinymist.fontPaths` | `["<dépôt>/polices"]` | polices de la suite pour le compilateur de Tinymist |
| `tinymist.preview.fontPaths` | `["<dépôt>/polices"]` | idem pour l'aperçu en direct |
| `tinymist.exportPdf` | `"never"` | Tinymist n'écrit pas de PDF : ils viennent de Ctrl+Maj+B (sinon un PDF de plus à chaque Ctrl+S, aux extraits LaTeX non rendus). Sans l'extension `bfcours-typst`, `"onSave"` donne un PDF unique |

Chemins écrits avec des `/`, même sous Windows. Ces réglages sont recommandés (rendu Erewhon), non obligatoires. Si les polices sont installées dans le système par `installer.ps1` / `installer.sh`, les deux `fontPaths` restent conseillés : ils rendent l'aperçu indépendant de l'état du système.

### Extension `bfcours-typst` (clés `bfcoursTypst.*`)

| Clé | Valeurs (défaut en premier) | Effet |
|---|---|---|
| `ctrlS` | `apercu`, `pdf`, `rien` | ce que fait Ctrl+S : aperçu en direct (aucun PDF), PDF prof + élève, ou rien |
| `versionApercu` | `prof`, `eleve` | version montrée par l'aperçu ouvert au Ctrl+S |
| `apercuAuto` | `false`, `true` | ouvre l'aperçu dès l'ouverture d'un `.typ` |
| `apercuColonne` | `cote`, `active` | où s'ouvre l'aperçu |
| `allerAuCode` | `ctrl+clic`, `clic`, `jamais` | comment passer de l'aperçu au code source |
| `suiviCurseur` | `souris`, `curseur`, `jamais` | l'aperçu suit le curseur |
| `ouvrirPdf` | `non`, `prof`, `eleve`, `deux` | PDF ouverts après Ctrl+Maj+B |
| `prechauffage` | `true`, `false` | compile en arrière-plan le document de l'onglet actif à chaque changement d'onglet vers un `.typ` (sans écrire de PDF) : le premier Ctrl+Maj+B ne coûte qu'une compilation incrémentale |
| `seuilMemoireMo` | `4000` | garde-fou : mémoire privée au-delà de laquelle le service est recyclé (un neuf, préchauffé, prend le relais) ; pris en compte au prochain lancement du service |
| `diagnostics` | `true` | erreurs de Ctrl+Maj+B dans l'onglet Problèmes |
| `pdfUnique` | `auto`, `toujours`, `jamais` | PDF unique des documents hors suite |
| `actif` | `true` | `false` coupe l'effet de Ctrl+S ; Ctrl+Maj+B reste |
| `python`, `script`, `polices` | chemins | Python avec `typst`, `bfwatch.py`, dossier des polices ; **vides : ceux que `installer.py --vscode` a notés dans l'extension** (à ne remplir qu'à la main si l'extension a été installée sans lui) |

Deux gestes seulement : **Ctrl+S** = aperçu Tinymist en direct (Ctrl+clic → code) ; **Ctrl+Maj+B** (fichier `.typ`) = extraits LaTeX nouveaux ou modifiés, puis PDF prof et élève, compilés en parallèle.

Le compilateur de l'extension est un **service partagé** (`bfwatch.py --service`) : un seul pour toute la session et toutes les fenêtres VS Code. La première fenêtre qui travaille sur un `.typ` le lance ; les suivantes s'y branchent (fichier d'annonce avec jeton dans `%LOCALAPPDATA%/bfcours-typst/services/`, verrou contre un double service, journal `bfwatch-service-<clé>.log` au même endroit et dans le canal de sortie « bfcours-typst »). Il garde deux compilateurs (prof, élève) qui passent d'un document à l'autre avec un cache commun, et s'arrête 30 s après la fermeture de la dernière fenêtre (une fenêtre tuée ou figée est détectée ; un « Reload Window » retrouve le service et son cache). Il sert aussi `compiler.py`, qui ne s'y inscrit pas. Réglages de bfwatch lui-même, dans `tools/bfwatch.json` de la suite : `allegement` (`false` par défaut), `parallele` (`true`), `service` (`true`), `arret_sans_client_s` (`30`), `rogner_apres_s` (`60` : mémoire vive rendue à Windows après une minute sans requête, cache gardé).

### Dans le document

Un document qui contient des `#latex[…]` porte une fois, après l'import : `#setbflatex(lire: p => read(p, encoding: none))`. Sans elle, l'aperçu montre les extraits en encadré « non rendu ». LaTeX introuvable : `"bfcours-latex.chemin": "<dossier qui contient lualatex>"`.

## 5. Modifier `settings.json` sans rien perdre

Règle absolue : **ne jamais écraser un `settings.json`, ne jamais le réécrire d'après une copie lue plus tôt.**

1. Le **lire** (c'est du JSON avec commentaires et virgules finales permis : `//`, `/* */`).
2. **Fusionner** : ajouter ou changer seulement les clés voulues ; les autres réglages, les commentaires et l'ordre restent. Une clé déjà présente avec la bonne valeur n'est pas touchée.
3. Faire une **sauvegarde** à côté (`settings.json.avant-bfcours-<date>`) avant d'écrire.
4. Relire le fichier après écriture : il doit rester lisible et porter les valeurs.

`installer.py --vscode` applique ces quatre points pour les trois clés Tinymist du § 4 ; **le préférer** à une édition manuelle. S'il dit « settings.json illisible », il n'écrit rien : corriger la syntaxe avec l'utilisateur d'abord. Pour une clé qu'il ne gère pas (`bfcoursTypst.*`, `bfcours-latex.chemin`), utiliser Edit sur la ligne exacte, après lecture.

## 6. Vérifications finales

1. `python <installer> --verifier` : « Tout est en place ».
2. Un dossier d'essai avec un `cours.typ` minimal (recette `recettes/cours.typ` du skill) : `python "<skill>/scripts/compiler.py" "essai/cours.typ" --png` donne `cours-prof.pdf` et `cours-eleve.pdf` ; **regarder l'image** : la taille des formules est celle du texte, la version élève n'a pas les réponses.
3. Dans VS Code, rechargé : Ctrl+S ouvre l'aperçu ; Ctrl+Maj+B écrit les deux PDF ; la barre d'état affiche « Typst : prof + élève ».
4. Supprimer le dossier d'essai ensuite.

## 7. Pannes connues

| Symptôme | Cause et remède |
|---|---|
| Rendu sans les polices Erewhon (Libertinus Serif et New Computer Modern Math à la place), sans erreur | Les polices de `polices/` sont facultatives : les formules gardent la bonne taille. Pour retrouver Erewhon, vérifier que `polices/` du dépôt est dans `tinymist.fontPaths` et `tinymist.preview.fontPaths` (`--verifier`), que `installer.ps1` / `installer.sh` a été lancé, puis rouvrir VS Code. En ligne de commande : `--font-path polices` ou `BFCOURS_TYPST_POLICES` |
| `package not found: @preview/farfadet` | Paquet non installé (l'installateur pose la copie du dépôt dans le cache de Typst), ou Typst lit un autre dossier (Typst par Snap ou Flatpak : `typst info`, « Package path ») ; `--verifier` liste ce qui manque |
| Extrait `#latex` en encadré « non rendu » dans l'aperçu | `#setbflatex(lire: …)` absent du document, ou l'index des rendus n'existe pas : `rendus-tex/index.json` est créé par `compiler.py` au premier passage ou par l'ouverture de l'aperçu ; un extrait nouveau ou modifié attend le prochain Ctrl+Maj+B |
| Cadre rouge à la place d'un extrait | LaTeX introuvable (`lualatex`, `pdflatex`, `xelatex` absents du PATH) : l'installer, ou régler `bfcours-latex.chemin` |
| Ctrl+clic sans effet dans l'aperçu | L'aperçu passe par un **relais** local devant le serveur de Tinymist, qui retire les clics sans Ctrl. Vérifier `allerAuCode` (`ctrl+clic` par défaut), recharger la fenêtre après une mise à jour de l'extension, rouvrir l'aperçu ; si l'aperçu ne s'ouvre pas du tout, l'extension Tinymist Typst est absente ou son binaire introuvable (`tinymist.serverPath`) |
| Ctrl+Maj+B ne produit rien | Extension non installée ou fenêtre non rechargée (*Developer: Reload Window*) ; sinon ouvrir le journal (clic sur la barre d'état, canal « bfcours-typst ») |
| « compilateur indisponible » | `bfcoursTypst.python` faux, ou ce Python n'a pas `typst` : `python -m pip install typst` |
| Trois PDF au lieu de deux | `tinymist.exportPdf` pas à `"never"` |
| « écriture impossible … ouvert dans un lecteur » | un lecteur PDF verrouille le fichier : le fermer |
| L'extension a perdu ses chemins après un déplacement du dépôt | relancer `python <installer> --vscode` depuis le nouvel emplacement |
| Le skill ne retrouve pas la suite | relancer `python <installer> --skill` (réécrit `chemin-suite.txt`), ou définir `BFCOURS_TYPST_SUITE` |

Chemins avec accents, espaces ou noms courts Windows (`NOM~1`) : écrire le chemin complet et nommer les dossiers de travail sans accents ; LuaLaTeX refuse un `~` dans un chemin.
