# Standard : refondre la présentation d'un skill

Référence : la refonte du skill `latex` (octobre 2026).
À appliquer aux autres skills présentés sur le site : reveals, capsules vidéo, typst, barème détaillé…

Fichiers de la référence :

- diaporama : `public/render/Reveals/bfcours-latex-system.html` ;
- page : `src/data/skill-pages.ts` (contenu) et `src/components/skills/SkillPackPanel.tsx` (rendu) ;
- pack : `SKILL_PACKS` dans `src/data/ai-packages.ts` ;
- installation : `src/lib/skill-install.ts`.

---

## 1. Principes du discours

- **Partir de ce que le prof demande, finir sur ce qu'il obtient.**
  Une demande en français en entrée, un livrable vérifié en sortie.
- **Raconter le flux de l'agent, pas sa technique.**
  Chaque étape = un verbe (Créer, Écrire, Compiler, Regarder) + ce que fait l'agent + ce que le prof y gagne.
- **Le nom du skill technique reste discret.**
  Il apparaît en petit sous l'étape (`tex-document-creator`), jamais comme titre.
- **Pas de jargon superflu dans le fil principal.**
  Ni ligne de commande, ni nom de script, ni « tokens », ni profil de compilation sur les diapos horizontales.
  Seule exception : la dernière diapo, qui donne les dossiers d'installation.
  La technique n'est pas supprimée : elle descend dans les piles verticales (§ 2 bis).
- **Deux lectures, deux axes.**
  En ne faisant que → , on lit l'histoire complète (demande → étapes → livrable → installation).
  En descendant ↓ sous une étape, on voit ce que fait réellement l'agent, en profondeur et avec exactitude.
- **Une diapo = une idée**, lisible sans le présentateur.
- **Le prof garde la main** : le dire (« votre rôle : demander, puis relire »).

---

## 2. Trame type du diaporama (fil principal de 8 diapos + piles verticales)

Fil principal (horizontal, → ) :

| # | Titre type | Rôle | Pile ↓ |
|---|---|---|---|
| 1 | « Le skill X » + sous-titre « de votre demande à … » | Où l'on veut en venir : bulle avec une demande réaliste du prof → flèche → livrable (pastille rouge). Compréhensible seule. Petite ligne d'aide à la navigation en bas (« → la suite · ↓ les détails · Échap : vue d'ensemble »). | non |
| 2 | « Ce que fait l'agent, en N étapes » | Fil conducteur : N cartes colorées (une couleur par étape), une phrase chacune. | 1 diapo : « En coulisse » (étape → skill appelé, préparation éventuelle) |
| 3 à 2+N | Une diapo par étape (« Il part d'un modèle », « Il rédige… ») | Frise des étapes en haut (étape courante colorée). Deux colonnes : « Ce que fait l'agent » / « Ce que vous y gagnez ». Une maquette visuelle (HTML/CSS) plutôt que du code quand l'étape produit quelque chose de visible. | 1 à 3 diapos de détail par étape |
| avant-dernière | « Ce que vous obtenez » | Trois cartes : le livrable, les sources, les retouches en français. Rappel du rôle du prof. | 1 à 2 diapos : bien formuler sa demande, limites |
| dernière | « L'installer » | Pack à ajouter au panier ; quatre cartes : Claude Code projet (recommandé), Claude Code global (déconseillé), Codex projet (recommandé), Codex global (déconseillé) ; prérequis ; exemple de demande. | non |

Piles verticales (↓) : voir § 2 bis.

Style : thème clair (`white.css`), Segoe UI, palette `#2c3e50 / #3498db / #27ae60 / #f39c12 / #8e44ad`, Font Awesome.
Couleurs d'étapes : vert (créer), bleu (écrire), orange (compiler/produire), violet (relire).
Guillemets français avec espaces insécables (`«&nbsp;…&nbsp;»`).

---

## 2 bis. Navigation à deux dimensions : fil principal → , détails ↓

reveal.js imbrique des `<section>` : une `<section>` qui contient d'autres `<section>` forme une **pile verticale**.
La première diapo de la pile est celle du fil principal ; les suivantes sont les détails.

```html
<section>                                   <!-- pile de l'étape « Compiler » -->
  <section> … diapo du fil principal … <div class="indice-details">↓ détails</div></section>
  <section> … détail 1 … </section>
  <section> … détail 2 … </section>
</section>
```

### Règles

- **Le fil principal se suffit à lui-même.**
  Quelqu'un qui ne fait que → doit tout comprendre. Aucune diapo horizontale ne renvoie à un détail pour être comprise.
- **Quand créer une pile** : sous une diapo d'étape, sous « Ce que fait l'agent, en N étapes » (une diapo « En coulisse ») et sous « Ce que vous obtenez » (formuler sa demande, limites).
  Pas de pile sous la diapo de titre ni sous « L'installer ».
  Pas de pile si on n'a rien d'exact à dire : une pile vide de substance est pire que pas de pile.
- **Combien** : 1 à 3 diapos verticales par pile ; au-delà, couper ou renvoyer vers la page du skill.
- **Ce qui y va** (la technique a sa place ici, en profondeur) :
  - les fichiers produits (arborescence) ;
  - les skills et scripts appelés en coulisse, les options ;
  - un extrait réel du code produit ou une commande, si elle éclaire ;
  - un exemple réel de demande et de résultat, un avant / après ;
  - les erreurs typiques corrigées automatiquement, les garde-fous ;
  - les limites, et les astuces de formulation de la demande pour le prof.
- **Exactitude** : chaque détail est vérifié dans le `SKILL.md` **source** (et ses scripts), jamais déduit. Pas de nom réel d'établissement ou d'élève, pas de chemin personnel.
- **Lisibles seules** : pas de fragments dans les diapos verticales (elles sont souvent consultées isolément, et imprimées).
  Une diapo verticale tient dans 960 × 700 sans défilement : tableau ou deux colonnes plutôt qu'une longue liste.

### Repères visuels

- **Indice « ↓ détails »** sur la diapo du fil principal qui a une pile : pastille discrète en bas à droite (classe `indice-details`, gris, petite police), jamais sur une diapo sans pile.
- **Fil d'Ariane** en haut de chaque diapo verticale (classe `fil-detail`) : pastille de la couleur de l'étape + « Détail 1 / 2 ».
  Le titre `h3` de la diapo verticale est en couleur d'étape, plus petit que le `h2` du fil principal.
- Ligne d'aide sur la diapo 1 : « → la suite · ↓ les détails · Échap : vue d'ensemble ».

### Configuration reveal

```js
Reveal.initialize({
  navigationMode: 'default',     // → saute à l'étape suivante (haut de pile), ↓ descend dans la pile
  controls: true,
  controlsLayout: 'bottom-right',// les 4 flèches groupées en croix : la 2D se voit
  controlsTutorial: true,        // la flèche ↓ rebondit tant qu'on n'est jamais descendu
  controlsBackArrows: 'faded',
  slideNumber: 'h.v',            // « 5.1 » = 5e diapo du fil, « 5.2 » = son 1er détail (numérotation à partir de 1)
  overview: true,                // Échap : grille des piles
  hash: true,                    // l'URL #/4/1 (indices à partir de 0) cible ce même détail ; le PresentationViewer gère h/v
  progress: true,
  center: true
});
```

Ne pas utiliser `navigationMode: 'linear'` (→ parcourrait aussi les détails) ni `'grid'`.

---

## 3. Structure type de la page du skill

Page : `/claude-code/presentations/<slug>`. Le slug dérive du nom du fichier HTML.
Si le slug figure dans `SKILL_PAGES`, la page affiche, dans l'ordre :

1. **En-tête** : `titre` et `accroche` de `SKILL_PAGES` (remplacent le titre tiré du nom de fichier).
2. **Diaporama** (composant existant `PresentationViewer`).
3. **« Ce que fait l'agent »** : bulle de demande → cartes d'étapes (même texte que le diaporama) → résultat ; puis « Ce que vous obtenez » et « Pour le lancer ».
4. **« Le pack »** : contenu du pack, bouton « Ajouter au panier » (composant `AddToCartButton`, item `package-<id>`), mention des bundles qui l'incluent déjà.
5. **« Installer le pack »** : bascule Windows (PowerShell) / macOS-Linux ; quatre cartes (Claude Code projet/global, Codex projet/global) avec badge recommandé/déconseillé et `CodeBlock` (bouton Copier) ; modules Python ; prérequis avec liens ; encart Codex.

---

## 4. Mécanique technique réutilisable

### Où vivent les choses

| Élément | Emplacement |
|---|---|
| Diaporamas | `public/render/Reveals/<slug>.html` (assets reveal locaux dans `assets/reveal/`) |
| Classement des diaporamas | `public/render/Reveals/categories.json` (commentaire, tags) |
| Menu | `src/components/layout/MainNav.tsx` (entrées « presentations ») |
| Titre dans la recherche | `presentationTitles` dans `src/data/search-index.ts` |
| Fichiers publiés des skills | `public/download/Claude-Code-Setup/claude-setup/` (`skills/`, `datas/`, `mcp_servers/`…) : copies nettoyées, à ne pas confondre avec les sources du poste |

### Déclarer un pack dans le panier

Un « pack » est déjà une notion du site (bundles de `AI_PACKAGES`) ; un pack de skill en est une variante.

1. `src/data/ai-packages.ts` : ajouter l'id à `SkillPackId`, puis une entrée dans `SKILL_PACKS` :
   `tier: 0`, `skillOnly: true`, `skills` (le skill + ceux qu'il enchaîne), `dataPaths`, `mcpServerPaths`, `pythonDeps`, `highlights`.
2. Rien d'autre à brancher :
   - l'API `/api/download-package` résout l'id dans `ALL_PACKAGES` et construit l'archive avec `buildPackageZip` (`src/lib/package-zip.ts`) ;
   - le panier (`CartDrawer`) télécharge tout item `package-<id>` par cette API ;
   - la détection des doublons (`packageIncludes`) considère qu'un bundle inclut un pack de skill s'il contient tous ses skills.
3. Archive d'un pack de skill : `claude-setup-<id>.zip`, contenant **uniquement** `.claude/` (`skills/`, `mcp_servers/`, `datas/`, `LISEZMOI-<id>.md`). Elle se décompresse donc telle quelle dans un projet existant.

### Déclarer la page

`src/data/skill-pages.ts` : une entrée `SKILL_PAGES['<slug>']` (titre, accroche, packId, demandeExemple, resultat, etapes, obtient, prerequis, invocation).
Icônes d'étape possibles : celles du type `SkillPageStep['icone']` (ajouter l'icône lucide dans `ICONES` de `SkillPackPanel` si besoin).

### Commandes d'installation

`src/lib/skill-install.ts` génère, pour un id de pack, les quatre variantes (Windows et Unix) ; le même texte alimente la page et le LISEZMOI de l'archive.

| Outil | Projet (recommandé) | Global (déconseillé) |
|---|---|---|
| Claude Code | `.claude/skills/` : `Expand-Archive <zip> -DestinationPath . -Force` | `~/.claude/skills/` : `-DestinationPath $HOME` |
| Codex | `.agents/skills/` : décompresser dans un dossier temporaire, puis copier le contenu de `.claude/` dans `.agents/` | `~/.agents/skills/` |

Source Codex : https://learn.chatgpt.com/docs/build-skills (ex-`developers.openai.com/codex/skills`) — `$CWD/.agents/skills`, dossiers parents jusqu'à la racine du dépôt, `$HOME/.agents/skills`.

On copie **tout** `.claude/` (pas seulement `skills/`) : les scripts retrouvent `mcp_servers/` et `datas/` par chemin relatif (`../../../mcp_servers`).

### Vérifier un pack sans serveur

`buildPackageZip` est hors du `route.ts` (un `route.ts` ne peut exporter que `GET`, `POST`…), donc appelable par un script Node via `jiti` (`node_modules/.pnpm/jiti@*/node_modules/jiti`, alias `@` → `src`). Puis : décompresser dans un projet vide, lancer les scripts principaux du skill depuis ce projet.

---

## 5. Checklist pour un autre skill

1. [ ] Lire le `SKILL.md` **source** et celui **publié** (`public/download/.../skills/`) : flux réel, skills appelés, scripts.
2. [ ] Lister les dépendances des scripts : `grep` de `.claude/`, `mcp_servers`, `datas`, `Path(__file__).parent…`, imports Python (`pip`). Ajouter dans `claude-setup/` ce qui manque (sans données personnelles).
3. [ ] Écrire la trame en verbes : demande → étapes → livrable.
4. [ ] Réécrire le diaporama selon la trame du § 2 (fichier existant si des liens y pointent, sinon nouveau `<slug>.html` + entrées `categories.json`, `MainNav.tsx`, `search-index.ts`).
   - [ ] Fil principal relu en ne faisant que → : l'histoire est complète sans aucun détail.
   - [ ] Piles verticales selon le § 2 bis (1 à 3 détails, contenu vérifié dans le `SKILL.md` source), indice « ↓ détails » sur chaque tête de pile et seulement là, fil d'Ariane sur chaque détail.
   - [ ] Configuration reveal du § 2 bis (`navigationMode: 'default'`, `controlsLayout: 'bottom-right'`, `controlsTutorial`, `slideNumber: 'h.v'`, `overview`).
5. [ ] Déclarer le pack dans `SKILL_PACKS` (+ id dans `SkillPackId`).
6. [ ] Déclarer la page dans `SKILL_PAGES`, avec le même discours que le diaporama.
7. [ ] Mettre à jour le commentaire de `categories.json`, le libellé du menu et le titre de recherche.
7 bis. [ ] Vérifier qu'aucun texte propre à un autre skill ne reste en dur dans le code commun (`SkillPackPanel.tsx`, `skill-install.ts`, LISEZMOI de `package-zip.ts`) : ce qui diffère d'un pack à l'autre se déclare dans `SKILL_PACKS` / `SKILL_PAGES` (champs `annexes`, prérequis, `commandPaths`…).
7 ter. [ ] Liens du diaporama vers le site : URL absolues `https://bfcours.dev/…` (jamais `href="/…"`, qui donne `file:///C:/…` quand le diaporama est ouvert ou téléchargé hors du site), avec `target="_top"` pour une page, `target="_blank"` pour un fichier.
8. [ ] `npx tsc --noEmit` (ignorer les erreurs de `.next/` périmé).
9. [ ] Construire l'archive (jiti), la décompresser dans un projet vide (variante Claude Code ET variante Codex), lancer les scripts clés.
10. [ ] Capturer le diaporama (skill `capture-html`, URL `?print-pdf&pdfSeparateFragments=false`, `--pleine-page`) et relire chaque diapo, **diapos verticales comprises** (en mode impression, chaque détail occupe sa propre page, juste après sa tête de pile). Vérifier aussi une diapo verticale isolée (`#/h/v`) en mode normal : contrôles en croix, numéro `h.v`, aucun débordement.
11. [ ] Faire relire la page à l'utilisateur sur son serveur de développement (on ne lance pas `pnpm dev`).
