# Modèle de brief commun — animateurs d'une fournée de capsules

À copier dans le dossier de la fournée (`<fournee>/BRIEF-animation.md`) et à adapter : les passages entre ⟨chevrons⟩ sont à remplir. Exemple réel (moteur HTML, même méthode) : `<dossier_capsules>/Exercices-vecteurs-corriges/BRIEF-animation.md` (23 corrections d'exercices, 03/10/2026).

---

# Brief commun — animation des capsules ⟨série, niveau, chapitre⟩

Tu écris le `spec.js` d'UNE capsule déjà préparée (script écrit, voix synthétisée, mots alignés). Tu ne touches ni à `script.md`, ni à l'audio, ni à `data/`.

## À lire avant de coder (chemins relatifs à la racine du projet)

1. `.claude/skills/capsule-video/SKILL.md` (sections « Construire, rendre, diriger », « Fournée » et « Règles du moteur »), puis **`references/moteur-canvas.md`** (format de `spec.js`, gabarits, éléments, pièges).
2. `.claude/skills/capsule-video/references/design.md` et `references/gestes.md` (gestes, ancres `'@b10~"mot"'`), et **`references/rigueur.md`** (l'écran est une copie modèle : chaînes d'égalités, brouillon, vocabulaire exact).
3. Exemples validés : `.claude/skills/capsule-video/assets/exemples/exo5-canvas/` (voie B), `tableau-croise-canvas/` (voie A), `labomaths-canvas/` (figure géométrique).
4. ⟨Capsule de la fournée déjà validée, à prendre comme modèle d'habillage pour que la série soit homogène.⟩
5. Dans le dossier de la capsule : `script.md` (le script EST le storyboard ; la section « Choix didactiques » dit ce qui doit être montré), `data/temps-forts.json`, `data/transcript.txt`.
6. ⟨La source de l'exercice et ses figures (LaTeX/TikZ…) : les figures reprennent EXACTEMENT les coordonnées de la source.⟩

## Exigences du professeur

- **Rigueur mathématique absolue** : chaque formule affichée est juste, en notation française ⟨conventions du cours : virgule décimale, notations de points, de vecteurs…⟩. L'écran affiche le juste même si la voix trébuche.
- Ce qui est dit est montré, au moment où c'est dit. Un calcul se DÉROULE ligne par ligne puis se COMPACTE (recette de `design.md`) ; les résultats restent visibles en puces.
- ⟨Thème, sous-titres⟩, mention « Voix de synthèse » discrète, rappel de l'énoncé au début. Pas d'écran presque vide plus de 3 s.
- **Rendu final en ⟨540p⟩** : texte courant ≥ 40 px, formules ≥ 60 px dans la mise en page 1920×1080, traits de figure ≥ 4 px, points ≥ 10 px de rayon.
- Couleurs sémantiques fixes (une couleur par objet), un seul foyer d'attention à la fois.
- **Chaîne d'égalités = rédaction recopiable** : un calcul s'écrit en UNE chaîne `A = … = … = résultat`, chaque « = » affiché quand la voix dit « égale » ; aucun calcul annexe dans la chaîne. Les calculs annexes (carré d'un négatif, somme intermédiaire) vont dans un encart **« Brouillon »** séparé et visuellement distinct, montré quand la voix dit « Au brouillon ». Un élève qui recopie l'écran doit obtenir une copie correcte.
- Aucune puce ni carte n'en chevauche une autre, à aucun instant : la mise en page empêche les débordements de cadre, pas les recouvrements entre zones ou entre étapes d'une pile mal enchaînées (soigner l'enchaînement à l'écriture).
- Aucun état intermédiaire mathématiquement faux à l'écran pendant une transformation (arrondi, simplification) : effacer d'abord, écrire ensuite.

## Interdits

- **Ne lance PAS le rendu vidéo** (`rendre_canvas.py` sans `--images`) : la file de rendus s'en charge, une capsule à la fois.
- Pas de `setTimeout`, de `Date`, ni de `Math.random` dans `spec.js` (`C.hasard`). `id` uniques (y compris ceux de `\cssId`).
- Ne tue aucun processus Chrome.

## Erreurs bloquantes

Pas de planche ni de revue image par image : le moteur signale seul les erreurs bloquantes (mot introuvable, id inconnu ou en double, formule fausse, débordement) et les zones réduites (« mise en page : texte à N % » : en dessous de 85 %, alléger). Les traiter si elles apparaissent.

## Mise en file de rendu

Dès que `spec.js` est écrit et que le moteur ne signale aucune erreur bloquante, crée le fichier vide `PRET-RENDU` dans le dossier de la capsule (`touch "<capsule>/PRET-RENDU"`) : la file de rendus le prend toute seule. Ne le crée pas s'il reste un doute ; signale-le.

## Compte rendu attendu (court)

Durée, scènes, zones réduites, incohérences script ↔ source (signalées, pas corrigées).
