/**
 * Tutoriel Typst pas à pas (parcours `typst`), capsules 10 à 15 :
 * tableaux, géométrie, compléments et extraits LaTeX, ressources collège rd*, travail avec Claude Code.
 * Chaque exemple et chaque solution compile avec @preview/farfadet:0.2.0 (vérifié le 21/10/2026).
 * Les capsules 1 à 9 sont dans parcours-typst-a.ts.
 */
import { Capsule } from '@/types/tutorial'

export const TYPST_CAPSULES_B: Record<string, Capsule> = {
  'ty-tableaux': {
    id: 'ty-tableaux',
    title: "Tableaux de valeurs, de signes et de variations",
    description: "Encadrer un tableau avec tcbtab, dresser un bilan de séquence, puis construire des tableaux de signes et de variations à compléter",
    parcours: 'typst',
    order: 9,
    sections: {
      info: `
<h3>Deux paquets pour les tableaux</h3>
<p>Un cours de maths contient sans cesse des tableaux : valeurs d'une fonction, proportionnalité, signes, variations. La suite farfadet en couvre deux familles, toutes deux chargées par la ligne habituelle <code>#import "@preview/farfadet:0.2.0": *</code>.</p>
<ul>
  <li><strong>farfadet-tableaux</strong> : <code>tcbtab</code>, le tableau encadré de bfcours (cadre arrondi, ombre, titre), et <code>tableaurecapsequence</code>, le bilan de séquence avec les colonnes MI, MF, MS, TBM.</li>
  <li><strong>farfadet-tabvar</strong> : <code>tabvar</code>, l'équivalent du paquet LaTeX <code>tkz-tab</code>, pour les tableaux de signes et de variations.</li>
</ul>

<h4>tcbtab : les cellules à la suite</h4>
<p>On donne d'abord le nombre de colonnes, puis les cellules rangée après rangée, chacune entre crochets. Les clés utiles au quotidien :</p>
<ul>
  <li><code>title: [...]</code> : un bandeau de titre ;</li>
  <li><code>entete: true</code> : la première rangée en en-tête coloré ;</li>
  <li><code>align: center</code> : le tableau centré (par défaut, il est collé à gauche, comme <code>\\tcbtab</code> en LaTeX).</li>
</ul>
<p>On peut aussi donner une spécification de colonnes à la LaTeX, par exemple <code>"|c|c|c|"</code>, et placer des filets avec <code>hline()</code>.</p>

<h4>tabvar : une liste de x, puis des lignes</h4>
<p>Le tableau commence par la liste des valeurs de x, entre guillemets : <code>("-oo", "1", "+oo")</code>. <code>"-oo"</code> et <code>"+oo"</code> s'affichent en −∞ et +∞.</p>
<ul>
  <li><code>tkz-tab-line(nom, spec)</code> ajoute une ligne de signes. Pour N valeurs de x, la spécification a 2N − 1 éléments séparés par des virgules : un élément sous chaque valeur de x (vide, <code>z</code> pour un zéro, <code>t</code> pour un simple trait, <code>d</code> pour une double barre), et un signe entre deux valeurs.</li>
  <li><code>tkz-tab-var(nom, ...)</code> ajoute une ligne de variations : un élément par valeur de x, comme <code>("+", "5")</code> (5 en haut) ou <code>("-", "-1")</code> (−1 en bas). Les flèches se tracent seules.</li>
  <li><code>a-completer: true</code> : la version élève reçoit le tableau vide, avec seulement les x et les noms des lignes. <code>a-completer: (2,)</code> ne vide que la ligne 2.</li>
</ul>
<p><strong>Attention</strong> : sans <code>a-completer</code>, l'élève reçoit le tableau rempli.</p>
<div class="doc-links">
  <span class="doc-links-label">Guides des paquets</span>
  <div class="doc-links-buttons">
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/farfadet-tableaux.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">farfadet-tableaux (PDF)</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/farfadet-tabvar.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">farfadet-tabvar (PDF)</a>
  </div>
</div>
      `,
      exemple: `
<h3>Quatre tableaux dans un même document</h3>
<p>Copiez ce code dans un fichier <code>.typ</code> : il compile tel quel.</p>
<pre><code>#import "@preview/farfadet:0.2.0": *

// 1. Un tableau de valeurs : 5 colonnes, première rangée en en-tête, centré
#tcbtab(5, title: [Valeurs de $f(x) = x^2 - 2 x$], entete: true, align: center,
  [$x$],    [$-1$], [$0$],  [$1$],  [$3$],
  [$f(x)$], [$3$],  [$0$],  [$-1$], [$3$],
)

// 2. Un tableau de signes : 3 valeurs de x, donc 2 × 3 − 1 = 5 éléments
//    (vide, signe, z pour zéro, signe, vide)
#tabvar(
  ("-oo", "1", "+oo"),
  tkz-tab-line($2 x - 2$, ",-,z,+,"),
)

// 3. Un tableau de variations, à compléter par l'élève
#tabvar(
  ("-oo", "1", "+oo"),
  tkz-tab-line($f'(x)$, ",-,z,+,"),
  tkz-tab-var($f(x)$, ("+", "+oo"), ("-", "-1"), ("+", "+oo")),
  a-completer: true,
)

// 4. Le bilan de séquence : MI, MF, MS, TBM
#tableaurecapsequence(hline(), ..entete-contenu(),
  [Dresser un tableau de valeurs], [], [], [], [], hline(),
  [Lire un tableau de variations], [], [], [], [], hline(),
)</code></pre>
<p>Le rendu, en version professeur :</p>
<img src="/images/tutorials/typst/ty-10-tableaux.png" alt="Rendu : un tableau de valeurs encadré, un tableau de signes, un tableau de variations en couleur de correction et un bilan de séquence MI, MF, MS, TBM" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
<p>Remarquez que le tableau de variations est en couleur de correction : c'est la version professeur. Dans la version élève, les signes, le 0, les nombres et les flèches disparaissent ; il ne reste que la grille, les valeurs de x et les noms des lignes.</p>
      `,
      pratique: `
<p>Ces exercices se font dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst. Chaque code de départ compile déjà.</p>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 1 : du tableau brut au tcbtab</span>
  </div>
  <div class="exercise-body">
    <p>Ce tableau de proportionnalité est écrit avec la fonction <code>table</code> de Typst. Transformez-le en <code>tcbtab</code> centré, avec le titre « Prix des pommes » et la première colonne en en-tête. Écrivez les nombres en mode maths, avec une virgule décimale.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

// Un tableau Typst natif : à transformer en tcbtab
#table(columns: 4,
  [Masse (kg)], [1], [2,5], [4],
  [Prix (€)], [3,20], [8], [12,80],
)</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#tcbtab(4, title: [Prix des pommes], entete: true, align: center,
  [Masse (kg)], [$1$], [$2","5$], [$4$],
  [Prix (€)], [$3","20$], [$8$], [$12","80$],
)</code></pre>
      <p>En mode maths, la virgule décimale s'écrit entre guillemets : <code>$2","5$</code>. Sans les guillemets, Typst ajoute une espace après la virgule, comme après une virgule de liste.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 2 : le signe d'un produit</span>
  </div>
  <div class="exercise-body">
    <p>Complétez le tableau de signes de (x + 3)(2 − x) : ajoutez la ligne du facteur 2 − x, puis celle du produit.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

// Signe de (x + 3)(2 − x) : il manque deux lignes
#tabvar(
  ("-oo", "-3", "2", "+oo"),
  tkz-tab-line($x + 3$, ",-,z,+,t,+,"),
)</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#tabvar(
  ("-oo", "-3", "2", "+oo"),
  tkz-tab-line($x + 3$, ",-,z,+,t,+,"),
  tkz-tab-line($2 - x$, ",+,t,+,z,-,"),
  tkz-tab-line($(x + 3)(2 - x)$, ",-,z,+,z,-,"),
)</code></pre>
      <p>Quatre valeurs de x donnent 2 × 4 − 1 = 7 éléments par ligne. Sous la valeur où le facteur ne s'annule pas, on écrit <code>t</code> : un simple trait pointillé, sans zéro.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 3 : des variations à compléter</span>
  </div>
  <div class="exercise-body">
    <p>La fonction g(x) = −x² + 4x + 1 atteint son maximum 5 en x = 2. Ajoutez la ligne de variations de g, puis faites en sorte que seule cette ligne soit vide dans la version élève (la ligne de g'(x) reste donnée).</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

// g(x) = -x² + 4x + 1 : la ligne de g'(x) est écrite
#tabvar(
  ("-oo", "2", "+oo"),
  tkz-tab-line($g'(x)$, ",+,z,-,"),
)</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#tabvar(
  ("-oo", "2", "+oo"),
  tkz-tab-line($g'(x)$, ",+,z,-,"),
  tkz-tab-var($g(x)$, ("-", "-oo"), ("+", "5"), ("-", "-oo")),
  a-completer: (2,),
)</code></pre>
      <p>Les lignes sont numérotées à partir de 1, sans compter la ligne des x : la ligne de g est la ligne 2. Pour vérifier, compilez la version élève (dans VS Code avec l'extension bfcours-typst : Ctrl+Maj+B ; dans l'application : passez l'aperçu en version élève).</p>
    </div>
  </details>
</div>
      `,
    },
    duration: "20 min",
    tags: ["typst", "farfadet", "tableaux", "tabvar", "variations"],
  },
  'ty-geom': {
    id: 'ty-geom',
    title: "Figures de géométrie avec farfadet-geom",
    description: "Tracer repères, points, polygones et codages en quelques lignes, puis savoir quand écrire directement en cetz",
    parcours: 'typst',
    order: 10,
    sections: {
      info: `
<h3>Une couche légère sur cetz</h3>
<p>En Typst, les figures se dessinent avec <strong>cetz</strong>, l'équivalent de TikZ. cetz sait tout faire, mais chaque figure demande les mêmes réglages : épaisseur des traits, croix des points, place des noms, codages. <strong>farfadet-geom</strong> les fixe une fois pour toutes, aux couleurs de bfcours, et donne une trentaine de macros pour les figures du collège et du lycée.</p>

<h4>Les règles d'écriture</h4>
<ul>
  <li><strong>Tout se dessine dans <code>geo({ ... })</code></strong> : <code>geo</code> ouvre le canevas. <code>figure-geo(legende: [...], { ... })</code> fait la même chose avec une légende numérotée.</li>
  <li><strong>Un point est un couple de nombres</strong> : <code>(2, 1.5)</code>. On le range dans une variable : <code>let A = (0, 0)</code>. On ne modifie ensuite le point qu'à un seul endroit.</li>
  <li><strong>Un nom est une chaîne</strong> : <code>"A"</code> s'affiche en maths. Sa position se règle par <code>pos: "ne"</code> (nord-est), <code>"so"</code>, <code>"n"</code>…</li>
  <li><strong>Les couleurs se nomment</strong> : <code>couleur: "bleu"</code>, <code>"rouge"</code>, <code>"vert"</code>, <code>"gris"</code>…</li>
  <li><code>unite: 0.8cm</code> dans <code>geo</code> règle la longueur d'une unité.</li>
</ul>

<h4>Les macros principales</h4>
<ul>
  <li><strong>Repère et courbes</strong> : <code>repere(x: (-2, 4), y: (-1, 3))</code>, <code>courbe(x =&gt; x * x)</code>, <code>quadrillage</code>, <code>axes</code>.</li>
  <li><strong>Objets</strong> : <code>point</code>, <code>segment</code>, <code>droite</code>, <code>demi-droite</code>, <code>fleche</code> (vecteur), <code>cercle</code>, <code>arc</code>, <code>polygone</code>, <code>triangle</code>, <code>ligne-brisee</code>, <code>etiquette</code> (un texte sans croix).</li>
  <li><strong>Codages</strong> : <code>codage-segment(A, B, n: 2)</code>, <code>angle-droit</code>, <code>angle-marque</code>, <code>codage-parallele</code> ; ou directement des clés : <code>triangle(..., angles-droits: (0,))</code>, <code>segment(..., codage: 1)</code>.</li>
  <li><strong>Constructions</strong> : <code>mediatrice</code>, <code>bissectrice</code>, <code>hauteur</code>.</li>
  <li><strong>Calculs</strong> : <code>milieu(A, B)</code>, <code>projete(P, A, B)</code>, <code>intersection</code>, <code>distance</code> <em>renvoient</em> un point ou un nombre ; ils ne tracent rien.</li>
</ul>

<h4>Quand passer à cetz directement ?</h4>
<p>farfadet-geom ne fait ni la 3D, ni la géométrie dynamique, et ne cherche pas à remplacer cetz. Dès qu'il vous faut une courbe libre (Bézier), un schéma qui n'est pas une figure de géométrie, un diagramme ou un graphe, importez cetz et utilisez ses fonctions <strong>dans le même canevas</strong> : <code>import cetz.draw: bezier, content</code>, à l'intérieur de <code>geo</code>. Les macros de farfadet et celles de cetz cohabitent (exercice 3).</p>
<p><strong>Piège</strong> : un <code>#let point = ...</code> écrit dans votre document masque la fonction <code>point</code> de la suite. Nommez vos variables <code>A</code>, <code>B</code>, <code>M</code>…</p>
<div class="doc-links">
  <span class="doc-links-label">Guide du paquet</span>
  <div class="doc-links-buttons">
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/farfadet-geom.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">farfadet-geom (PDF)</a>
    <a href="https://typst.app/universe/package/cetz" target="_blank" rel="noopener noreferrer" class="doc-link">cetz sur Typst Universe</a>
  </div>
</div>
      `,
      exemple: `
<h3>Un triangle codé et un vecteur dans un repère</h3>
<pre><code>#import "@preview/farfadet:0.2.0": *

#grid(columns: (1fr, 1fr), column-gutter: 1cm,
  // Figure 1 : triangle rectangle et milieu de l'hypoténuse
  figure-geo(legende: [$I$ est le milieu de $[B C]$.], {
    let A = (0, 0)
    let B = (4, 0)
    let C = (0, 3)
    let I = milieu(B, C)              // milieu calcule un point, il ne trace rien
    triangle(A, B, C, noms: ("A", "B", "C"), angles-droits: (0,))
    segment(A, I, style: "tirets", couleur: "bleu")
    codage-segment(B, I, n: 1)        // les deux moitiés portent le même codage
    codage-segment(I, C, n: 1)
    point(I, "I", pos: "ne", couleur: "bleu")
  }),
  // Figure 2 : un repère, deux points et un vecteur
  geo(unite: 0.8cm, {
    repere(x: (-2, 4), y: (-1, 3))
    let A = (-1, 1)
    let B = (3, 2)
    fleche(A, B, nom: "u", couleur: "rouge")
    point(A, "A", pos: "so")
    point(B, "B", pos: "se")
  }),
)</code></pre>
<img src="/images/tutorials/typst/ty-11-geom.png" alt="Rendu : à gauche un triangle ABC rectangle en A avec le milieu I de l&#x27;hypoténuse codé, à droite un repère avec les points A et B et le vecteur u" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
<p>Remarquez que <code>milieu(B, C)</code> ne trace rien : il calcule le point I, que l'on dessine ensuite avec <code>point</code>. Les deux figures sont placées côte à côte par <code>grid</code> ; dans une grille, on écrit <code>figure-geo(...)</code> et <code>geo(...)</code> sans <code>#</code>, puisqu'on est déjà en mode code.</p>
      `,
      pratique: `
<p>À faire dans VS Code (Tinymist) ou dans l'application Écriture Typst.</p>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 1 : la médiatrice</span>
  </div>
  <div class="exercise-body">
    <p>Tracez la médiatrice de [AB], placez un point M de cette médiatrice, reliez-le à A et à B en bleu et codez l'égalité MA = MB.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

#geo({
  let A = (0, 0)
  let B = (5, 0)
  segment(A, B)
  point(A, "A", pos: "so")
  point(B, "B", pos: "se")
})</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#geo({
  let A = (0, 0)
  let B = (5, 0)
  let M = (2.5, 2)                  // un point de la médiatrice
  segment(A, B)
  mediatrice(A, B)
  segment(A, M, couleur: "bleu")
  segment(B, M, couleur: "bleu")
  codage-segment(A, M, n: 2)
  codage-segment(B, M, n: 2)
  point(A, "A", pos: "so")
  point(B, "B", pos: "se")
  point(M, "M", pos: "e", couleur: "bleu")
})</code></pre>
      <p>Le milieu de [AB] a pour abscisse 2,5 : tout point d'abscisse 2,5 est sur la médiatrice. <code>mediatrice</code> code elle-même les deux moitiés de [AB] et l'angle droit.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 2 : la parabole</span>
  </div>
  <div class="exercise-body">
    <p>Dans ce repère, tracez en bleu la courbe de la fonction carré, puis placez ses points A(2 ; 4) et B(−1 ; 1).</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

#geo(unite: 0.8cm, {
  repere(x: (-3, 3), y: (-1, 5))
})</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#geo(unite: 0.8cm, {
  repere(x: (-3, 3), y: (-1, 5))
  courbe(x =&gt; x * x, couleur: "bleu")
  point((2, 4), "A", pos: "e")
  point((-1, 1), "B", pos: "o")
})</code></pre>
      <p><code>x =&gt; x * x</code> est une fonction anonyme de Typst : elle associe x² à x. <code>courbe</code> la trace sur toute la largeur du repère et s'arrête à ses bords.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 3 : un peu de cetz</span>
  </div>
  <div class="exercise-body">
    <p>Sous ce cercle, ajoutez une courbe libre rouge (une courbe de Bézier) et la légende « une courbe de Bézier », avec les fonctions <code>bezier</code> et <code>content</code> de cetz. cetz est déjà importé en tête du fichier.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *
#import "@preview/cetz:0.5.2"

#geo({
  let O = (0, 0)
  cercle(O, 2)
  point(O, "O", pos: "so")
})</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *
#import "@preview/cetz:0.5.2"

#geo({
  import cetz.draw: bezier, content
  let O = (0, 0)
  cercle(O, 2)
  point(O, "O", pos: "so")
  // cetz directement, dans le même canevas : une courbe libre et un texte
  bezier((-2, -2.5), (2, -2.5), (-1, -1), (1, -4), stroke: red)
  content((0, -3.3), [une courbe de Bézier])
})</code></pre>
      <p><code>bezier(début, fin, contrôle 1, contrôle 2)</code> : les deux points de contrôle donnent la forme de la courbe. Les fonctions de cetz prennent leurs propres clés (<code>stroke: red</code>), pas celles de farfadet (<code>couleur: "rouge"</code>).</p>
    </div>
  </details>
</div>
      `,
    },
    duration: "20 min",
    tags: ["typst", "farfadet", "géométrie", "cetz", "figures"],
  },
  'ty-extras-latex': {
    id: 'ty-extras-latex',
    title: "Habiller, coder en Python, insérer du LaTeX",
    description: "Les compléments de farfadet-extras (habillage, code Python, pellicule, icônes) et, en dernier recours, un extrait LaTeX compilé avec farfadet-latex",
    parcours: 'typst',
    order: 11,
    sections: {
      info: `
<h3>farfadet-extras : quatre compléments de mise en page</h3>
<ul>
  <li><strong><code>habiller(figure)[texte]</code></strong> : le texte coule à côté de la figure, puis reprend toute la largeur dessous. La figure est à droite par défaut ; <code>cote: "gauche"</code> la met à gauche, <code>ecart: 2em</code> l'éloigne du texte.</li>
  <li><strong><code>bf-code-python(...)</code></strong> : un programme Python coloré, dans un cadre. Le code s'écrit entre trois accents graves suivis de <code>python</code>. Clés utiles : <code>numeros: true</code> (numéros de ligne), <code>title: "..."</code>, <code>surligner: (2,)</code> (surligne la ligne 2).</li>
  <li><strong><code>filmbox[...]</code></strong> : une pellicule de cinéma, une image ou une étape par item <code>-</code>. <code>mode: "texte"</code> pour des étiquettes, <code>mode: "rogne"</code> pour des images recadrées.</li>
  <li><strong><code>icone("book")</code></strong> : une icône du jeu Feather (environ 280 : <code>"check"</code>, <code>"clock"</code>, <code>"edit-2"</code>, <code>"help-circle"</code>…), avec <code>couleur</code> et <code>taille</code>.</li>
</ul>

<h3>farfadet-latex : le dernier recours</h3>
<p>Vous avez une figure TikZ réussie, une macro ProfCollege, un dessin en perspective que Typst ne sait pas encore faire ? Gardez-les en LaTeX. <code>#latex[...]</code> accueille un extrait <strong>tel quel</strong> : LaTeX le compile, et le résultat est inséré comme une image vectorielle, nette à tous les zooms.</p>
<p>C'est un dernier recours, pas une habitude : un extrait LaTeX est dessiné par LaTeX, avec ses propres polices, sans les réglages de la suite ; il ralentit la première compilation et il demande une installation complète. Avant d'y passer, cherchez l'équivalent Typst : <code>tabvar</code> remplace tkz-tab, <code>farfadet-geom</code> et cetz remplacent la plupart des figures TikZ, les paquets rd* remplacent beaucoup de macros ProfCollege (capsule suivante).</p>

<h4>Ce qu'il faut sur la machine</h4>
<ul>
  <li>une distribution LaTeX (MiKTeX, TeX Live ou MacTeX) avec les paquets nommés dans l'extrait ;</li>
  <li>Python avec le module <code>typst</code> (<code>pip install typst</code>) ;</li>
  <li>VS Code avec l'extension <strong>bfcours-typst</strong>, posée par l'installateur de la suite quand Python et son module <code>typst</code> sont présents.</li>
</ul>
<p><strong>Ctrl+S</strong> met à jour l'aperçu mais ne lance jamais LaTeX : un extrait nouveau s'affiche comme un encadré « Extrait LaTeX non rendu ». <strong>Ctrl+Maj+B</strong> compile les extraits nouveaux ou modifiés (et eux seuls), puis produit les PDF professeur et élève. Pour voir ensuite les extraits dans l'aperçu, écrivez une fois en tête du document : <code>#setbflatex(lire: p =&gt; read(p, encoding: none))</code>. Cette ligne lit le dossier <code>rendus-tex/</code>, que l'extension crée à l'ouverture de l'aperçu ou au premier Ctrl+Maj+B.</p>
<p>L'application Écriture Typst, qui tourne dans le navigateur, ne peut pas lancer LaTeX : les extraits LaTeX se travaillent dans VS Code.</p>
<div class="doc-links">
  <span class="doc-links-label">Guides des paquets</span>
  <div class="doc-links-buttons">
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/farfadet-extras.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">farfadet-extras (PDF)</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/farfadet-latex.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">farfadet-latex (PDF)</a>
  </div>
</div>
      `,
      exemple: `
<h3>Les quatre compléments de farfadet-extras</h3>
<pre><code>#import "@preview/farfadet:0.2.0": *
#set text(lang: "fr")

// 1. Des icônes dans le texte (jeu Feather)
#icone("book") Lire le cours, #icone("edit-2") faire l'exercice, #icone("check", couleur: green) vérifier.

// 2. Habiller une figure : le texte coule à côté, puis reprend toute la largeur
#let fig = geo(unite: 0.6cm, {
  triangle((0, 0), (4, 0), (0, 3), noms: ("A", "B", "C"), angles-droits: (0,))
})
#habiller(fig)[
  Dans le triangle $A B C$ rectangle en $A$, l'hypoténuse est $[B C]$.
  Le théorème de Pythagore donne $B C^2 = A B^2 + A C^2$.
  Avec $A B = 4$ et $A C = 3$, on obtient $B C^2 = 16 + 9 = 25$, donc $B C = 5$.
  On repère d'abord l'hypoténuse, on écrit l'égalité, puis on calcule.
]

// 3. Du code Python, coloré et numéroté
#bf-code-python(numeros: true, title: "Calcul de l'hypoténuse", \`\`\`python
from math import sqrt
def hypotenuse(a, b):
    return sqrt(a**2 + b**2)
\`\`\`)

// 4. Une pellicule : les étapes d'une méthode
#let etape(t) = box(fill: white, inset: 3pt)[#t]
#filmbox(mode: "texte", largeur: 3.4cm)[
  - #etape[Repérer]
  - #etape[Écrire]
  - #etape[Calculer]
  - #etape[Conclure]
]</code></pre>
<img src="/images/tutorials/typst/ty-12-extras.png" alt="Rendu : une ligne d&#x27;icônes, un paragraphe sur Pythagore habillé autour d&#x27;un triangle rectangle, un programme Python numéroté et une pellicule de quatre étapes" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
<p>Remarquez la ligne <code>#let fig = geo(...)</code> : la figure est rangée dans une variable, puis passée à <code>habiller</code>. On peut y mettre une image (<code>image("figure.png")</code>) de la même façon.</p>

<h3>Un extrait LaTeX : un pavé droit en TikZ</h3>
<p>Dans le code Typst, l'extrait LaTeX s'écrit entre trois accents graves suivis de <code>latex</code>, le tout entre crochets. Tout ce qui s'y trouve, antislashs et dollars compris, passe tel quel à LaTeX.</p>
<pre><code>#import "@preview/farfadet:0.2.0": *
#setbflatex(lire: p =&gt; read(p, encoding: none))  // pour voir les rendus dans l'aperçu Tinymist

Un pavé droit en perspective cavalière, dessiné en TikZ :

#latex(paquets: ("tikz",))[\`\`\`latex
\\begin{tikzpicture}[scale=0.8]
  \\draw (0,0) -- (4,0) -- (4,2) -- (0,2) -- cycle;
  \\draw (4,0) -- (5.5,1) -- (5.5,3) -- (4,2);
  \\draw (0,2) -- (1.5,3) -- (5.5,3);
  \\draw[dashed] (0,0) -- (1.5,1) -- (5.5,1);
  \\draw[dashed] (1.5,1) -- (1.5,3);
  \\node[below] at (2,0) {4 cm};
  \\node[left] at (0,1) {2 cm};
  \\node[below right] at (4.75,0.5) {3 cm};
\\end{tikzpicture}
\`\`\`]</code></pre>
<img src="/images/tutorials/typst/ty-12-latex.png" alt="Rendu après Ctrl+Maj+B : un pavé droit de 4 cm sur 3 cm sur 2 cm en perspective cavalière, arêtes cachées en pointillés" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
<p>Les paquets LaTeX se donnent par la clé <code>paquets</code> ; un préambule propre à l'extrait (une bibliothèque TikZ par exemple) par la clé <code>preambule</code>. <code>echelle: 80%</code> ou <code>largeur: 6cm</code> règlent la taille du rendu.</p>
      `,
      pratique: `
<p>Les exercices 1 et 2 se font dans VS Code (Tinymist) ou dans l'application Écriture Typst ; l'exercice 3 demande VS Code avec l'extension bfcours-typst et une distribution LaTeX.</p>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 1 : habiller une figure</span>
  </div>
  <div class="exercise-body">
    <p>La figure et le paragraphe sont l'un sous l'autre. Faites couler le texte à droite de la figure, figure à gauche.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

#let fig = geo(unite: 0.5cm, {
  cercle((0, 0), 2)
  segment((0, 0), (2, 0), codage: 1)
  point((0, 0), "O", pos: "so")
})

#fig

Le cercle de centre $O$ et de rayon $r$ est l'ensemble des points situés à la distance $r$ du point $O$. Tous ses rayons ont donc la même longueur, ce que l'on code par un même signe sur chacun d'eux. Son diamètre mesure le double du rayon.</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#let fig = geo(unite: 0.5cm, {
  cercle((0, 0), 2)
  segment((0, 0), (2, 0), codage: 1)
  point((0, 0), "O", pos: "so")
})

#habiller(fig, cote: "gauche")[
  Le cercle de centre $O$ et de rayon $r$ est l'ensemble des points situés à la distance $r$ du point $O$. Tous ses rayons ont donc la même longueur, ce que l'on code par un même signe sur chacun d'eux. Son diamètre mesure le double du rayon.
]</code></pre>
      <p>Le texte passe entre les crochets de <code>habiller</code> : c'est lui qui s'enroule autour de la figure.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 2 : un programme Python</span>
  </div>
  <div class="exercise-body">
    <p>Ajoutez un bloc de code Python numéroté, intitulé « Carrés », qui affiche les nombres de 1 à 10 et leurs carrés.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

Le programme suivant affiche les dix premiers carrés.

// Votre bloc de code Python ici</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

Le programme suivant affiche les dix premiers carrés.

#bf-code-python(numeros: true, title: "Carrés", \`\`\`python
for n in range(1, 11):
    print(n, n**2)
\`\`\`)</code></pre>
      <p>Le bloc Python garde ses indentations telles quelles : écrivez-les comme dans votre éditeur Python, avec quatre espaces.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 3 : un extrait LaTeX</span>
  </div>
  <div class="exercise-body">
    <p>Insérez les trois identités remarquables, alignées sur le signe égal, avec l'environnement <code>align*</code> de LaTeX. Faites Ctrl+Maj+B pour obtenir le rendu.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

Les identités remarquables :

// Votre extrait LaTeX ici</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

Les identités remarquables :

#latex[\`\`\`latex
\\begin{align*}
  (a+b)^2 &amp;= a^2 + 2ab + b^2 \\\\
  (a-b)^2 &amp;= a^2 - 2ab + b^2 \\\\
  (a+b)(a-b) &amp;= a^2 - b^2
\\end{align*}
\`\`\`]</code></pre>
      <p><code>amsmath</code> est déjà chargé par le préambule commun : pas besoin de clé <code>paquets</code>. Bien sûr, ces identités s'écrivent aussi très bien en Typst ; c'est ici un simple essai du mécanisme. Gardez <code>#latex</code> pour ce que Typst ne sait pas faire.</p>
    </div>
  </details>
</div>
      `,
    },
    duration: "20 min",
    tags: ["typst", "farfadet", "python", "habillage", "latex", "tikz"],
  },
  'ty-rd-calcul': {
    id: 'ty-rd-calcul',
    title: "Ressources collège : calcul, numération, conversions",
    description: "Décompositions et fractions irréductibles, opérations et durées posées, tableaux de numération et de conversion, barres de proportion, avec leur version élève",
    parcours: 'typst',
    order: 12,
    sections: {
      info: `
<h3>Six paquets rd* pour le calcul au collège</h3>
<p>Les paquets rd* prolongent en Typst les paquets LaTeX de Régis Deleuze. Ils sont <strong>compris dans farfadet</strong> : la ligne <code>#import "@preview/farfadet:0.2.0": *</code> suffit, aucun autre import n'est nécessaire. Pour n'en charger qu'un, on importe son module : <code>#import "@preview/farfadet:0.2.0": rd-arithm</code> puis <code>#import rd-arithm: *</code>.</p>
<ul>
  <li><strong>rdarithm</strong> (arithmétique) : <code>decomp-fp(126)</code> (décomposition en facteurs premiers, en ligne, en étapes, en arbre ou en tableau avec <code>mise-en-page</code>), <code>liste-diviseurs</code>, <code>pgcd(60, 75)</code> et <code>ppcm</code> (avec <code>etoile: true</code>, on obtient la valeur), <code>fracirr</code> et <code>dfracirr</code> (fraction irréductible), <code>decomp-frac</code> (la simplification détaillée).</li>
  <li><strong>rdopp</strong> (opérations posées) : <code>rdopp("234, 56", mul: true)</code>. Les nombres s'écrivent dans une chaîne, avec un point décimal ; l'opération se choisit par <code>add</code>, <code>sub</code>, <code>mul</code>, <code>div</code> ou <code>divint</code>. Clés utiles : <code>carry: true</code> (retenues), <code>zero: true</code> (zéros ajoutés), <code>precision</code> (chiffres après la virgule d'un quotient).</li>
  <li><strong>rdtime</strong> (durées posées) : <code>rdtime("2h37min", "3h49min")</code> pose l'addition avec la conversion des minutes ; <code>sub: true</code> pour une soustraction.</li>
  <li><strong>rdtabnum</strong> (tableaux de numération) : <code>rdtabnum(rdtnplace("3,14"))</code> place un nombre, <code>rdtnconvert</code> convertit d'un rang à l'autre, <code>rdtn-arrow</code> dessine une flèche « × 10 ».</li>
  <li><strong>rdconv</strong> (conversions d'unités) : <code>rdconv(rdconvert(4500, "mg", "g"))</code>, avec <code>type: "mass"</code>, <code>"capacity"</code>, <code>"area"</code> ou <code>"volume"</code> (longueurs par défaut).</li>
  <li><strong>rdratio</strong> (barres de proportion) : <code>rdratio("1,2,3")</code> partage une barre selon un ratio, avec accolades et légendes.</li>
</ul>

<h4>La version élève, sans rien réécrire</h4>
<p>La clé <code>correction: true</code> sur <code>rdopp</code>, <code>rdtime</code>, <code>rdconv</code> ou <code>rdtabnum</code> garde la place du calcul mais <strong>vide les cases calculées</strong> dans la version élève. Dans la version professeur, la résolution apparaît dans la couleur des corrections. Dans <code>rdtabnum</code>, on marque en plus par <code>etoile: true</code> les lignes et les flèches que l'élève doit écrire.</p>
<div class="doc-links">
  <span class="doc-links-label">Guides des paquets</span>
  <div class="doc-links-buttons">
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdarithm.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdarithm</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdopp.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdopp</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdtime.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdtime</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdtabnum.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdtabnum</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdconv.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdconv</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdratio.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdratio</a>
  </div>
</div>
      `,
      exemple: `
<h3>Une page de calcul, en deux versions</h3>
<pre><code>#import "@preview/farfadet:0.2.0": *   // les outils rd* sont compris dans farfadet
#set text(lang: "fr")

// 1. Arithmétique (rdarithm) : décomposition et fraction irréductible
$126 = #decomp-fp(126) = #decomp-fp(powers: true, 126)$ #h(1cm)
$display(105/273) = #decomp-frac(105, 273) = #dfracirr(105, 273)$

// 2. Opérations posées (rdopp) et durées (rdtime) : correction: true
//    vide les cases calculées dans la version élève
#grid(columns: 3, column-gutter: 1.2cm, align: horizon,
  rdopp("234, 56", mul: true, carry: true, correction: true),
  rdopp("125, 5", div: true, correction: true),
  rdtime("2h37min", "3h49min", correction: true),
)

// 3. Numération (rdtabnum) et conversions (rdconv)
//    etoile: true marque ce que l'élève doit écrire
#rdtabnum(width: 8cm, stop: "dixiemes", correction: true,
  rdtnplace("4,2"),
  rdtnplace(42, etoile: true),
  rdtn-arrow(1, 2, $times 10$, etoile: true))

#rdconv(type: "mass", correction: true,
  rdconvert(4500, "mg", "g"),
  rdconvert("1,5", "kg", "g"),
)

// 4. Proportions (rdratio) : une barre partagée selon le ratio 1 : 2 : 3
#rdratio(width: 6cm, label-above: [150 €], label-below-auto-colors: true, "1,2,3")</code></pre>
<p>Version professeur :</p>
<img src="/images/tutorials/typst/ty-13-rd-calcul.png" alt="Version professeur : décomposition de 126, simplification de 105 sur 273, multiplication et division posées, addition de durées, tableau de numération, tableau de conversion et barre de proportion, résultats en couleur" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
<p>Version élève, compilée à partir du <strong>même fichier</strong> :</p>
<img src="/images/tutorials/typst/ty-13-rd-calcul-eleve.png" alt="Version élève : les mêmes outils, avec les cases calculées vides et la place réservée pour l&#x27;élève" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
<p>Remarquez ce qui reste visible chez l'élève : les données de l'énoncé (les nombres à opérer, le 4,2 placé, les grandeurs à convertir). Les lignes 1 et 4, sans <code>correction</code>, sont identiques dans les deux versions.</p>
      `,
      pratique: `
<p>À faire dans VS Code (Tinymist) ou dans l'application Écriture Typst. Pensez à regarder aussi la version élève.</p>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 1 : deux opérations posées</span>
  </div>
  <div class="exercise-body">
    <p>Posez la soustraction et la multiplication de l'énoncé, côte à côte, avec leur résolution visible seulement dans la version professeur. Dans la soustraction, faites apparaître le zéro qui complète 47,5.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

Posez et effectuez : $47","5 - 18","75$ et $36 times 24$.

// Vos deux opérations posées ici</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

Posez et effectuez : $47","5 - 18","75$ et $36 times 24$.

#rdopp("47.5, 18.75", sub: true, zero: true, correction: true) #h(1cm)
#rdopp("36, 24", mul: true, correction: true)</code></pre>
      <p>Dans la chaîne, le séparateur décimal est le point (<code>47.5</code>) ; le rendu affiche bien une virgule. <code>zero: true</code> écrit le zéro ajouté (47,50). <code>#h(1cm)</code> laisse un espace horizontal entre les deux opérations.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 2 : PGCD et fraction irréductible</span>
  </div>
  <div class="exercise-body">
    <p>Rédigez la correction de cet exercice : les arbres de décomposition de 60 et 75, les décompositions avec puissances, le PGCD, puis la simplification détaillée de la fraction.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

+ Décomposer 60 et 75 en produits de facteurs premiers.
+ Donner leur PGCD.
+ Rendre irréductible la fraction $60/75$.</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

+ Décomposer 60 et 75 en produits de facteurs premiers.
+ Donner leur PGCD.
+ Rendre irréductible la fraction $60/75$.

#decomp-fp(mise-en-page: "arbre", 60) #h(1cm) #decomp-fp(mise-en-page: "arbre", 75)

$60 = #decomp-fp(powers: true, 60)$ et $75 = #decomp-fp(powers: true, 75)$.

Le #pgcd() de 60 et 75 est $#pgcd(60, 75, etoile: true)$, donc $display(60/75) = #decomp-frac(60, 75) = #dfracirr(60, 75)$.</code></pre>
      <p><code>#pgcd()</code>, sans nombres, écrit simplement le mot « PGCD » ; <code>pgcd(60, 75, etoile: true)</code> donne sa valeur, 15. Dans une formule, une fonction de la suite s'appelle avec <code>#</code> : <code>$60 = #decomp-fp(60)$</code>.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 3 : des conversions à compléter</span>
  </div>
  <div class="exercise-body">
    <p>Préparez les deux tableaux de conversion de l'énoncé, vides dans la version élève. Le second porte sur des capacités ; affichez le litre par un L majuscule.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

Convertir $2","5$ km en m, puis 350 cL en L.

// Vos deux tableaux de conversion ici</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

Convertir $2","5$ km en m, puis 350 cL en L.

#rdconv(correction: true, rdconvert("2,5", "km", "m"))

#rdconv(type: "capacity", liter: [L], correction: true, rdconvert(350, "cL", "L"))</code></pre>
      <p><code>rdconvert(valeur, unité de départ, unité d'arrivée)</code> range les chiffres, ajoute les zéros, déplace la virgule et barre les zéros inutiles. La clé <code>liter: [L]</code> remplace le symbole ℓ par défaut.</p>
    </div>
  </details>
</div>
      `,
    },
    duration: "20 min",
    tags: ["typst", "farfadet", "collège", "rdarithm", "rdopp", "rdconv", "rdtime"],
  },
  'ty-rd-supports': {
    id: 'ty-rd-supports',
    title: "Ressources collège : boîtes, grilles, feuilles de calcul",
    description: "Les boîtes de cours et d'activités de rdboites (Scratch, GeoGebra, vrai ou faux), les grilles de rdgrid, les feuilles de calcul de rdsheet, et un mot de bfdoc",
    parcours: 'typst',
    order: 13,
    sections: {
      info: `
<h3>rdboites : soixante-seize boîtes sous un seul nom</h3>
<p>Toutes les boîtes de rdboites s'appellent par <code>rd.&lt;nom&gt;</code>. Comme les autres paquets rd*, elles sont comprises dans <code>#import "@preview/farfadet:0.2.0": *</code>. Quelques familles :</p>
<ul>
  <li><strong>Cours</strong> : <code>rd.zone[Titre][Corps]</code> (zone « À retenir »), <code>rd.attention[...]</code> (alerte à bande rouge), <code>rd.methode[...]</code>, <code>rd.cours[Titre][Corps]</code>, <code>rd.exemple[...]</code>, <code>rd.rappelbox[...]</code>.</li>
  <li><strong>Activités</strong> : <code>rd.acocher(juste: true)[...]</code> (case cochée chez le professeur seulement), <code>rd.vf(reponse: true)[...]</code> (vrai ou faux numéroté), <code>rd.domino</code>, <code>rd.tache[Étiquette][Titre][Corps]</code> (tâche complexe).</li>
  <li><strong>Scratch</strong> : <code>rd.scratchblock[...]</code> (étapes numérotées « Programme 1, 2… »), <code>rd.scratchfig</code>, <code>rd.scratchcapture</code> pour une capture d'écran.</li>
  <li><strong>GeoGebra</strong> : <code>rd.ggbentrainer[Gauche][Droite]</code> (bloc « S'entraîner en autonomie »), <code>rd.ggbqr("url", capture: ..., qr: ...)</code> (capture et QR code vers une ressource).</li>
</ul>
<p>Chaque boîte accepte les options de tcolorbox sous forme de clés (<code>colframe</code>, <code>colback</code>, <code>arc</code>…). Le réglage pour tout le document passe par <code>setrdboites(pour: "zone", colframe: ...)</code>.</p>

<h3>rdgrid et rdsheet</h3>
<ul>
  <li><strong>rdgrid</strong> dessine des grilles pour les pavages, les solides et les jeux : <code>rdgrid(type: "iso", 8, 5)</code> (isométrique), <code>"equi"</code> (triangles équilatéraux), <code>"hexa"</code> et <code>"rhexa"</code> (hexagones). <code>width</code> règle la taille d'une case ; <code>polygon-style</code> colore des cases.</li>
  <li><strong>rdsheet</strong> imite une capture de tableur (en-têtes A, B, C et 1, 2, 3) : une rangée par liste de chaînes, <code>rdsheet(("Mois", "Recettes"), ("Janvier", "1250"))</code>. Les clés <code>cell</code>, <code>row</code> et <code>column</code> mettent en forme une cellule, une ligne ou une colonne.</li>
</ul>

<h3>Et pour documenter vos propres paquets : bfdoc</h3>
<p>Les guides PDF de la suite sont écrits avec <strong>bfdoc</strong>, un paquet de documentation stylée : couverture, exemples de code Typst et LaTeX avec leur rendu réel, fiches de fonction, index. Si vous écrivez un jour vos propres fonctions Typst et voulez les partager, il s'importe à part, depuis les paquets installés par la suite : <code>#import "@local/bfdoc:0.2.0": *</code>, puis <code>#show: doc-modele.with(titre: "Mon paquet", version: "1.0", auteur: "Moi")</code>. Son guide décrit tout le reste.</p>
<div class="doc-links">
  <span class="doc-links-label">Guides des paquets</span>
  <div class="doc-links-buttons">
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdboites.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdboites</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdgrid.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdgrid</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/rdsheet.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">rdsheet</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/docs/bfdoc.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">bfdoc</a>
  </div>
</div>
      `,
      exemple: `
<h3>Boîtes de cours, d'activité, grille et tableur</h3>
<pre><code>#import "@preview/farfadet:0.2.0": *   // rdboites, rdgrid et rdsheet sont compris
#set text(lang: "fr")

// 1. Boîtes de cours (rdboites) : toutes s'appellent par rd.&lt;nom&gt;
#rd.zone[À retenir][Dans un triangle rectangle, le carré de l'hypoténuse est égal à la somme des carrés des deux autres côtés.]
#rd.attention[*Attention !* Cette égalité ne vaut que si le triangle est rectangle.]

// 2. Boîtes d'activité : case à cocher (cochée chez le professeur seulement),
//    étapes Scratch numérotées, encart GeoGebra
#rd.acocher(juste: true)[Un carré est un rectangle.]
#rd.scratchblock[quand le drapeau vert est cliqué] #rd.scratchblock[avancer de 10 pas]
#rd.ggbentrainer[Suis le lien pour t'entraîner.][Construire un triangle équilatéral avec GeoGebra.]

// 3. Une grille isométrique (rdgrid) et une feuille de calcul (rdsheet)
#grid(columns: 2, column-gutter: 1cm, align: horizon,
  rdgrid(type: "iso", width: 0.5, 8, 5),
  rdsheet(
    cell: ("A1:C1": (bg: "cyan!20", font: "bfseries")),
    ("Mois", "Recettes", "Dépenses"),
    ("Janvier", "1250", "1420"),
    ("Février", "1380", "1510"),
  ),
)</code></pre>
<img src="/images/tutorials/typst/ty-14-rd-supports.png" alt="Rendu : une zone À retenir, une alerte Attention, une case cochée, deux étapes Scratch numérotées, un bloc S&#x27;entraîner en autonomie avec GeoGebra, une grille isométrique et une feuille de calcul" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
<p>Remarquez que les étapes Scratch se numérotent seules (« Programme 1 », « Programme 2 ») et que la case de <code>rd.acocher</code> n'est cochée que dans la version professeur.</p>
      `,
      pratique: `
<p>À faire dans VS Code (Tinymist) ou dans l'application Écriture Typst.</p>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 1 : une méthode et deux vrai ou faux</span>
  </div>
  <div class="exercise-body">
    <p>Mettez la première phrase dans une boîte de méthode, puis transformez les deux affirmations en questions vrai ou faux (la première est vraie, la seconde fausse).</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

// À mettre dans une boîte de cours, puis deux affirmations vrai ou faux
Pour calculer une longueur avec Pythagore : repérer l'hypoténuse, écrire l'égalité, calculer.

Tout carré est un losange.

Tout losange est un carré.</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#rd.methode[Pour calculer une longueur avec Pythagore : repérer l'hypoténuse, écrire l'égalité, calculer.]

#rd.vf(reponse: true)[Tout carré est un losange.]
#rd.vf(reponse: false)[Tout losange est un carré.]</code></pre>
      <p>La clé <code>reponse</code> coche la bonne case dans la version professeur ; dans la version élève, les deux cases restent vides. Les questions se numérotent seules (01, 02).</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 2 : des grilles</span>
  </div>
  <div class="exercise-body">
    <p>Dessinez une grille d'hexagones de 6 sur 3 dont deux cases sont colorées en orange, puis, à côté, une grille de triangles équilatéraux de 5 sur 2.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

// Une grille pour un exercice de pavage</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#rdgrid(type: "hexa", width: 0.5, 6, 3,
  polygon-style: ("hexa-2-1": (fill: "orange!40"), "hexa-3-2": (fill: "orange!40")))
#h(1cm)
#rdgrid(type: "equi", width: 0.9, 5, 2)</code></pre>
      <p>Une case se désigne par son nom, <code>"hexa-colonne-ligne"</code> ; <code>show-num: true</code> affiche ces numéros sur la grille quand on les cherche. Les couleurs s'écrivent à la manière de xcolor : <code>"orange!40"</code>.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 3 : une feuille de calcul</span>
  </div>
  <div class="exercise-body">
    <p>Représentez une feuille de tableur avec, en colonne A, le nombre de cahiers (1, 2, 3) et, en colonne B, la formule qui calcule leur prix à 1,80 € pièce. La première ligne est en gras sur fond gris.</p>
    <pre><code>#import "@preview/farfadet:0.2.0": *

// Le prix de 1, 2 et 3 cahiers à 1,80 € : une feuille de calcul à écrire</code></pre>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>#import "@preview/farfadet:0.2.0": *

#rdsheet(
  row: ("1": (font: "bfseries", bg: "gray!15")),
  ("Nombre de cahiers", "Prix (€)"),
  ("1", "=A2*1,80"),
  ("2", "=A3*1,80"),
  ("3", "=A4*1,80"),
)</code></pre>
      <p>rdsheet affiche ce qu'on lui donne : il ne calcule pas les formules. C'est utile pour demander aux élèves la formule à saisir, ou le résultat qu'elle affichera.</p>
    </div>
  </details>
</div>
      `,
    },
    duration: "15 min",
    tags: ["typst", "farfadet", "collège", "rdboites", "rdgrid", "rdsheet", "bfdoc"],
  },
  'ty-avec-claude': {
    id: 'ty-avec-claude',
    title: "Travailler avec Claude Code",
    description: "Le skill bfcours-typst pour écrire, convertir et compiler vos documents farfadet avec Claude Code, des exemples de demandes, et où trouver la documentation",
    parcours: 'typst',
    order: 14,
    sections: {
      info: `
<h3>Le skill bfcours-typst</h3>
<p>Un <strong>skill</strong> est un dossier d'instructions et de scripts que Claude Code charge quand la tâche s'y prête. Le skill <strong>bfcours-typst</strong> est fourni dans les bundles <strong>LaTeX Enseignant</strong> et <strong>Power User</strong> de la page <a href="/claude-code/download-ai-packages">Packages IA</a>. Il se déclenche dès que vous parlez de Typst, d'un fichier <code>.typ</code>, de Tinymist ou d'une conversion depuis LaTeX ; vous pouvez aussi l'appeler par <code>/bfcours-typst</code>.</p>
<p>Il apporte à Claude :</p>
<ul>
  <li><strong>une carte des besoins</strong> : « je veux un tableau de variations » → <code>tabvar</code> ;</li>
  <li><strong>des recettes</strong> : un cours, une fiche d'exercices, une évaluation, un QCM et une fiche de calcul complets, qui compilent en versions professeur et élève, à imiter plutôt que de tout reconstruire ;</li>
  <li><strong>la liste des pièges</strong> de la suite (corrigés visibles chez l'élève, énoncé écrit dans une <code>crep</code>…) ;</li>
  <li><strong>des scripts</strong>, qu'il lance lui-même :</li>
</ul>
<table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
  <thead>
    <tr><th style="text-align: left; padding: 0.4rem; border-bottom: 1px solid rgba(255,255,255,0.2);">Script</th><th style="text-align: left; padding: 0.4rem; border-bottom: 1px solid rgba(255,255,255,0.2);">Ce qu'il fait</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 0.4rem;"><code>localiser.py</code></td><td style="padding: 0.4rem;">Diagnostic : Python et son module <code>typst</code>, paquets installés, polices, LaTeX. À lancer au premier usage.</td></tr>
    <tr><td style="padding: 0.4rem;"><code>compiler.py</code></td><td style="padding: 0.4rem;">Compile les versions professeur et élève (et les extraits LaTeX), exactement comme le Ctrl+Maj+B de VS Code ; <code>--png</code> produit des images que Claude regarde avant de vous livrer.</td></tr>
    <tr><td style="padding: 0.4rem;"><code>convertir.py</code></td><td style="padding: 0.4rem;">Préconvertit un <code>.tex</code> écrit avec bfcours en <code>.typ</code> qui compile, et liste ce qui reste à reprendre ; <code>--compiler</code> enchaîne avec les PDF.</td></tr>
    <tr><td style="padding: 0.4rem;"><code>chercher.py</code></td><td style="padding: 0.4rem;">Trouve la bonne fonction ou la bonne clé : par un besoin en mots, par le nom d'une commande LaTeX (<code>--latex tkzTabLine</code>), ou la fiche complète d'une fonction (<code>--fiche exo</code>).</td></tr>
  </tbody>
</table>
<p>La règle d'or du skill : <strong>une clé ne se devine pas, elle se cherche</strong>. Une clé inconnue arrête la compilation ; Claude vérifie avec <code>chercher.py</code> au lieu d'inventer.</p>

<h4>Ce qu'il faut sur la machine</h4>
<ul>
  <li>la suite farfadet, installée par la commande d'une ligne de la page <a href="/claude-code/download-typst-packages">Packages Typst</a> ;</li>
  <li>Python avec le module <code>typst</code> (<code>pip install typst</code>) pour les scripts de compilation ;</li>
  <li>en option, une distribution LaTeX pour les extraits <code>#latex</code>.</li>
</ul>
<p>Si quelque chose manque, demandez simplement à Claude : « Lance le diagnostic du skill bfcours-typst ». Le skill sait lire la réponse et vous dire quoi installer.</p>

<h4>Où trouver la documentation</h4>
<ul>
  <li><strong>La documentation complète</strong> (installation et guides de tous les paquets, avec un exemple rendu par fonction) : un seul PDF sur la Forge.</li>
  <li><strong>Un guide par paquet</strong> : les liens donnés dans chaque capsule de ce parcours.</li>
  <li><strong>L'application Écriture Typst</strong> et sa <strong>vidéo de prise en main</strong> (moins de quatre minutes) : page <a href="/claude-code/download-typst-packages">Packages Typst</a>. L'application contient aussi un bouton « Prompt IA » : un texte à coller dans une IA de conversation pour qu'elle rédige directement avec la suite.</li>
</ul>
<div class="doc-links">
  <span class="doc-links-label">Ressources</span>
  <div class="doc-links-buttons">
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation farfadet (PDF)</a>
    <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt sur la Forge</a>
    <a href="/claude-code/download-typst-packages" class="doc-link">Packages Typst et application</a>
    <a href="https://code.claude.com/docs/fr/skills" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">Les skills (doc officielle)</a>
  </div>
</div>
      `,
      exemple: `
<h3>Une demande, un document, deux PDF</h3>
<p>Dans un dossier ouvert avec Claude Code, on écrit simplement :</p>
<pre><code>Avec le skill bfcours-typst, écris une petite fiche de 2nde sur les
équations : un exercice d'application avec zones de réponse, puis un
tableau de signes à compléter. Compile les versions prof et élève.</code></pre>
<p>Claude part de la recette « fiche d'exercices », vérifie les fonctions avec <code>chercher.py</code>, écrit le fichier, puis lance <code>compiler.py --png</code> et regarde les deux images avant de répondre. Voici un fichier du type de celui qu'il produit :</p>
<pre><code>// Demande faite à Claude Code :
//   « Avec le skill bfcours-typst, écris une petite fiche de 2nde sur les
//     équations : un exercice d'application avec zones de réponse, puis
//     un tableau de signes à compléter. Compile les versions prof et élève. »
#import "@preview/farfadet:0.2.0": *

#show: modele(
  "cours",
  niveau: "2nde",
  theme: [Équations et signes],
  type-document: "exercices",
)

#exo(level: 1)[Résoudre une équation][
  Résoudre l'équation $3 x + 5 = 17$.
  #crep(extra-lines: 1)[$3 x = 12$, donc $x = 4$.]
]

#exo(level: 2)[Signe d'une expression][
  Compléter le tableau de signes de $2 x - 6$.
  #tabvar(
    ("-oo", "3", "+oo"),
    tkz-tab-line($2 x - 6$, ",-,z,+,"),
    a-completer: true,
  )
]</code></pre>
<p>Les deux PDF obtenus, version professeur à gauche, version élève à droite :</p>
<img src="/images/tutorials/typst/ty-15-prof-eleve.png" alt="À gauche la version professeur avec la réponse en couleur sur les lignes Seyès et le tableau de signes rempli ; à droite la version élève, mêmes places, vides" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />

<h3>D'autres demandes qui marchent bien</h3>
<ul>
  <li>« Convertis <code>Cours-vecteurs.tex</code> en Typst dans le dossier <code>typst/</code> et compile. » (un cours écrit avec bfcours)</li>
  <li>« Dans <code>fiche.typ</code>, mets les questions de l'exercice 2 sur deux colonnes. »</li>
  <li>« Quelle est la fonction farfadet qui remplace <code>\\tcbtabc</code> ? »</li>
  <li>« La compilation de <code>evaluation.typ</code> plante : trouve et corrige l'erreur. »</li>
  <li>« Ajoute un tableau de conversion des masses à compléter, vide dans la version élève. »</li>
  <li>« Regarde la version élève : une réponse est-elle visible ? »</li>
</ul>
<p>Précisez toujours <strong>le dossier de travail</strong> : le skill y range le <code>.typ</code>, les PDF professeur et élève et les images, et ne crée rien ailleurs. Il ne modifie jamais vos <code>.tex</code> d'origine.</p>
      `,
      pratique: `
<p>Ces exercices se font dans un terminal, avec Claude Code lancé dans un dossier de travail.</p>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 1 : le diagnostic</span>
  </div>
  <div class="exercise-body">
    <p>Vérifiez que le skill est installé et que votre poste est prêt. Quelle demande faire à Claude, et que doit-il vous répondre ?</p>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>Lance le diagnostic du skill bfcours-typst et dis-moi ce qui manque.</code></pre>
      <p>Claude lance <code>localiser.py</code>, qui affiche une ligne par élément : module <code>typst</code> de Python, paquets locaux, polices, outils de compilation, LaTeX. Pour chaque ligne manquante, il vous dit quoi faire : <code>pip install typst</code> pour le module, la commande d'installation de la suite pour les paquets. Les polices et LaTeX sont facultatifs.</p>
      <p>Si Claude ne connaît pas le skill, il n'est pas installé : téléchargez le bundle LaTeX Enseignant ou Power User sur la page Packages IA.</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 2 : convertir un cours LaTeX</span>
  </div>
  <div class="exercise-body">
    <p>Vous avez un cours <code>Cours-fonctions.tex</code> écrit avec bfcours. Demandez sa conversion en Typst dans un dossier <code>typst/</code>, avec les deux PDF. Que vous rend Claude, et que faire ensuite ?</p>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>Convertis Cours-fonctions.tex en Typst dans typst/ et compile les versions prof et élève.</code></pre>
      <p>Claude lance <code>convertir.py Cours-fonctions.tex -o typst/ --compiler</code>. Il répond en quelques lignes : les fichiers produits (<code>Cours-fonctions.typ</code>, <code>-prof.pdf</code>, <code>-eleve.pdf</code>), le nombre de pages et les éventuels points « à reprendre ». Les figures TikZ sont gardées en extraits <code>#latex</code>, fidèles à l'original.</p>
      <p>Ensuite, ouvrez le <code>.typ</code> dans VS Code et comparez les PDF avec votre PDF LaTeX. S'il reste des points à reprendre, demandez : « Traite les points à reprendre et montre-moi les images des deux versions. » Pour un <code>.tex</code> qui n'est pas écrit avec bfcours, la conversion se fait par adaptation : Claude peut d'abord vous poser une ou deux questions (garder les figures en LaTeX ou les redessiner, faire ou non une version élève).</p>
    </div>
  </details>
</div>
<div class="exercise-card">
  <div class="exercise-header">
    <span class="exercise-badge">Exercice 3 : retrouver une commande LaTeX</span>
  </div>
  <div class="exercise-body">
    <p>En LaTeX, vous écriviez vos tableaux de signes avec <code>\\tkzTabLine</code>. Demandez à Claude son équivalent dans farfadet, puis faites-lui écrire le tableau de signes de 2x − 6 à compléter par l'élève.</p>
  </div>
  <details class="exercise-solution">
    <summary>Voir la solution</summary>
    <div class="solution-content">
      <pre><code>Quel est l'équivalent farfadet de \\tkzTabLine ? Écris ensuite dans signes.typ
le tableau de signes de 2x - 6, à compléter par l'élève, et compile.</code></pre>
      <p>Claude lance <code>chercher.py --latex tkzTabLine</code> : la réponse est <code>tkz-tab-line</code>, du paquet farfadet-tabvar, à placer dans un <code>tabvar</code>. Il écrit alors un tableau comme celui de l'exemple ci-dessus, avec <code>a-completer: true</code>, et vérifie sur l'image élève que le tableau est bien vide.</p>
      <p>Retenez le réflexe : les noms LaTeX deviennent des noms en minuscules avec des tirets (<code>\\MultiColonnes</code> → <code>multi-colonnes</code>, <code>\\begin{EXO}</code> → <code>exo</code>), et <code>chercher.py</code> fait le lien.</p>
    </div>
  </details>
</div>
      `,
    },
    duration: "15 min",
    tags: ["typst", "farfadet", "claude-code", "skill", "conversion"],
  },
}
