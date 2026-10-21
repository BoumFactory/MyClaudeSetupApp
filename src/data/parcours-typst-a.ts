/**
 * Tutoriel Typst pas à pas (suite farfadet), capsules 1 à 9.
 * Fichier généré : chaque exemple et chaque solution ont été compilés en versions professeur et élève.
 */
import { Capsule } from '@/types/tutorial'

export const TYPST_CAPSULES_A: Record<string, Capsule> = {
  'ty-demarrer': {
    id: 'ty-demarrer',
    title: 'Démarrer avec Typst et farfadet',
    description: 'Pourquoi Typst, installer la suite farfadet, écrire et compiler un premier document prof/élève',
    parcours: 'typst',
    order: 0,
    sections: {
      info: `
        <h3>Pourquoi Typst quand on écrit en LaTeX ?</h3>
        <p>
          Typst est un langage de composition de documents, comme LaTeX : on écrit du texte et des commandes,
          un compilateur produit un PDF. Il a été pensé trente ans après LaTeX, et cela se sent au quotidien.
        </p>
        <table>
          <tr><th>Au quotidien</th><th>LaTeX</th><th>Typst</th></tr>
          <tr><td>Compilation</td><td>quelques secondes à une minute, plusieurs passes</td><td><strong>instantanée</strong> : l'aperçu suit la frappe</td></tr>
          <tr><td>Erreurs</td><td>un journal de plusieurs pages, ligne approximative</td><td>la ligne exacte, soulignée, avec une suggestion</td></tr>
          <tr><td>Syntaxe</td><td><code>\\textbf{…}</code>, <code>\\begin{itemize}</code>, <code>\\frac{a}{b}</code></td><td><code>*…*</code>, <code>- item</code>, <code>a/b</code></td></tr>
          <tr><td>Installation</td><td>une distribution de plusieurs Go</td><td>un exécutable de quelques dizaines de Mo</td></tr>
        </table>
        <p>
          Exemple d'erreur réelle : écrire <code>$AB$</code> au lieu de <code>$A B$</code>. Typst répond
          « <em>unknown variable: AB</em> », souligne les deux lettres et propose : « <em>try adding spaces between each letter: A B</em> ».
        </p>

        <h3>La suite farfadet</h3>
        <p>
          <strong>farfadet</strong> réunit 25 paquets Typst pour les cours de maths : environnements Définition,
          Propriété, Méthode…, exercices avec corrigés et barème, zones de réponse, lignes Seyès, QCM, tableaux,
          figures de géométrie. Les noms suivent ceux du paquet LaTeX <code>bfcours</code> : <code>\\Definition</code>
          devient <code>#definition</code>, <code>\\begin{EXO}</code> devient <code>#exo</code>.
        </p>
        <p>
          Son principe central : <strong>un seul fichier donne deux PDF</strong>. La version professeur montre les
          réponses en couleur et les corrigés ; la version élève garde exactement la même place, vide.
        </p>

        <h3>Installer</h3>
        <h4>Option 1 : l'installateur de la Forge (recommandé)</h4>
        <p>Une ligne à coller dans un terminal, sans droits d'administrateur, relançable sans risque.</p>
        <p><strong>Windows (PowerShell) :</strong></p>
        <pre><code>irm https://forge.apps.education.fr/romaindeschamps/farfadet/-/raw/main/install/windows.ps1 | iex</code></pre>
        <p><strong>macOS :</strong></p>
        <pre><code>curl -fsSL https://forge.apps.education.fr/romaindeschamps/farfadet/-/raw/main/install/macos.sh | bash</code></pre>
        <p><strong>Linux :</strong></p>
        <pre><code>curl -fsSL https://forge.apps.education.fr/romaindeschamps/farfadet/-/raw/main/install/linux.sh | bash</code></pre>
        <p>
          Il prépare les paquets, la police Erewhon (facultative), et VS Code s'il est présent : l'extension
          <strong>Tinymist</strong> (aperçu en direct, complétion, erreurs soulignées) et l'extension
          <strong>bfcours-typst</strong> (les deux PDF d'un coup). Fermez puis rouvrez VS Code à la fin.
        </p>
        <h4>Option 2 : sans rien installer</h4>
        <p>
          L'application <strong>Écriture Typst</strong> est un seul fichier HTML (environ 29 Mo) qui contient le
          compilateur, les polices et toute la suite. Elle s'ouvre par un double-clic dans Chrome ou Edge,
          fonctionne hors ligne et tient sur une clé USB. Elle propose des modèles, un aperçu prof/élève et une
          formation en 13 leçons.
        </p>

        <h3>Les deux gestes à retenir dans VS Code</h3>
        <ul>
          <li><strong>Ctrl+S</strong> : ouvre l'aperçu en direct (version professeur), mis à jour pendant la frappe.</li>
          <li><strong>Ctrl+Maj+B</strong> : écrit <code>cours-prof.pdf</code> et <code>cours-eleve.pdf</code> à côté du fichier.</li>
        </ul>
        <p>
          Si VS Code affiche « Mode restreint » à l'ouverture du dossier, cliquez sur « Faire confiance au dossier » :
          sinon les extensions restent désactivées.
        </p>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/raw/main/application/ecriture-typst.html" target="_blank" rel="noopener noreferrer" class="doc-link">Application Écriture Typst</a>
            <a href="https://typst.app/docs/" target="_blank" rel="noopener noreferrer" class="doc-link">Site officiel de Typst</a>
          </div>
        </div>
`,
      exemple: `
        <h3>Un premier document complet</h3>
        <p>Créez un dossier de travail, ouvrez-le dans VS Code, puis créez <code>cours.typ</code> :</p>
        <pre><code>// Mon premier document farfadet : un cours de 2nde sur les fonctions affines.
#import "@preview/farfadet:0.2.0": *

// Le modèle « cours » pose la page A4, le bandeau et le pied de page.
#show: modele(
  "cours",
  niveau: "2nde",                  // affiché dans le bandeau : 2nde
  theme: [Fonctions affines],      // titre du chapitre
  type-document: "cours",          // "cours", "exercices", "activite", "fiche", "evaluation"
)

= Définition

#definition[Fonction affine][
  Une fonction $f$ est #voc[affine] s'il existe deux réels $a$ et $b$ tels que,
  pour tout réel $x$, $f(x) = a x + b$.
]

#exo(level: 1)[Reconnaître une fonction affine][
  La fonction $g : x |-&gt; 3 x - 5$ est-elle affine ? Justifier.

  // Le contenu de la zone de réponse est la réponse du professeur.
  #crep(extra-lines: 1)[Oui : $g(x) = a x + b$ avec $a = 3$ et $b = -5$.]
]</code></pre>
        <p>Les trois lignes indispensables :</p>
        <ul>
          <li><code>#import "@preview/farfadet:0.2.0": *</code> charge toute la suite ;</li>
          <li><code>#show: modele("cours", …)</code> applique le gabarit à tout ce qui suit (page A4, bandeau, pied de page) ;</li>
          <li>le reste est le contenu : un titre <code>=</code>, une définition, un exercice.</li>
        </ul>
        <p>Ctrl+Maj+B produit les deux PDF. Ci-dessous, côte à côte :</p>
        <img src="/images/tutorials/typst/ty-01-premier-document.png" alt="Rendu du premier document : version professeur avec la réponse en rose, version élève avec les mêmes lignes vides" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>
          Le contenu de <code>#crep[…]</code> est <strong>la réponse</strong> : en rose chez le professeur, absente
          chez l'élève, qui garde les mêmes lignes Seyès pour écrire. Rien à dupliquer, rien à masquer à la main.
        </p>
        <p>
          <em>Écriture équivalente :</em> <code>#show: farfadet.with(niveau: "2nde", theme: […])</code> fait la même chose
          que <code>modele("cours", …)</code>, avec les mêmes clés.
        </p>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Installez la suite (option 1 ou 2). Créez <code>cours.typ</code> avec le code ci-dessous, ouvrez l'aperçu, puis produisez les deux PDF.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "2nde", theme: [Essai], type-document: "cours")

#definition[Fonction affine][Une fonction affine s'écrit $f(x) = a x + b$.]
#exo(level: 1)[Une équation][
  Résoudre $3 x + 5 = 17$.
  #crep[$x = 4$]
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Dans VS Code : Ctrl+S ouvre l'aperçu à droite, Ctrl+Maj+B écrit <code>cours-prof.pdf</code> (réponse <em>x = 4</em> en rose) et <code>cours-eleve.pdf</code> (la même zone, vide), dans le même dossier que <code>cours.typ</code>.</p>
              <p>Dans l'application Écriture Typst : collez le code dans l'éditeur, basculez l'aperçu entre version professeur et version élève, puis utilisez <strong>Télécharger</strong> pour récupérer le <code>.typ</code> et les deux PDF. Les documents ne vivent que dans la page : pensez à télécharger.</p>
              <p>Si rien ne s'affiche : vérifiez que le dossier n'est pas en « Mode restreint » et relancez l'installateur, qui se termine par un récapitulatif de ce qui a été fait ou sauté.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Transformez ce document en fiche d'exercices de 3e sur le théorème de Thalès : niveau, thème, type de document <code>"exercices"</code>, une définition, puis deux exercices (un ★, un ★★) avec chacun une zone de réponse d'une ligne de plus que la réponse.</p>
            <p>Partez du code de l'exercice 1.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Théorème de Thalès], type-document: "exercices")

#definition[Triangles emboîtés][
  Deux triangles $A B C$ et $A M N$ sont emboîtés quand $M in [A B]$, $N in [A C]$ et $(M N) parallel (B C)$.
]
#exo(level: 1)[Un rapport][
  Avec $A M = 2$ et $A B = 6$, calculer $(A M) / (A B)$.
  #crep(extra-lines: 1)[$(A M) / (A B) = 2 / 6 = 1 / 3$.]
]
#exo(level: 2)[Une longueur][
  Avec $(A M) / (A B) = 1 / 3$ et $B C = 9$, calculer $M N$.
  #crep(extra-lines: 1)[$M N = 9 / 3 = 3$.]
]</code></pre><p><code>level: 2</code> donne deux étoiles ; <code>extra-lines: 1</code> ajoute une ligne Seyès vide sous la réponse rédigée. Le bandeau affiche « 3<sup>e</sup> · Exercices : Théorème de Thalès ».</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Découverte</span>
          </div>
          <div class="exercise-body">
            <p>Ouvrez l'application Écriture Typst et faites la première leçon de sa <strong>Formation</strong>. Repérez où se règle la version professeur ou élève de l'aperçu.</p>
            
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>La Formation propose 13 leçons courtes, chacune avec une explication, un exemple, un point de départ et un exercice corrigé automatiquement (chaque critère se coche quand il est rempli). Le sélecteur de version de l'aperçu bascule entre professeur et élève sans changer le fichier. Ce tutoriel reprend ces notions et va plus loin : barème, compétences, Seyès, QCM.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '15 min',
    tags: ['typst', 'installation', 'farfadet', 'vs-code'],
  },
  'ty-syntaxe': {
    id: 'ty-syntaxe',
    title: 'La syntaxe de Typst',
    description: 'Les trois modes, titres, listes, set et show, fonctions et arguments nommés : ce qu\'il faut désapprendre de LaTeX',
    parcours: 'typst',
    order: 1,
    sections: {
      info: `
        <h3>Trois modes, trois signes</h3>
        <table>
          <tr><th>Mode</th><th>On y entre par</th><th>Exemple</th></tr>
          <tr><td><strong>Balisage</strong> (le texte)</td><td>c'est le mode par défaut</td><td><code>Un *carré* a quatre côtés.</code></td></tr>
          <tr><td><strong>Code</strong></td><td><code>#</code></td><td><code>#definition[…]</code>, <code>#let n = 3</code>, <code>#(n + 1)</code></td></tr>
          <tr><td><strong>Maths</strong></td><td><code>$…$</code></td><td><code>$x^2 + 1$</code></td></tr>
        </table>

        <h3>Le balisage</h3>
        <ul>
          <li><code>= Titre</code>, <code>== Sous-titre</code>, <code>=== …</code> en début de ligne : la numérotation est automatique.</li>
          <li><code>*gras*</code>, <code>_italique_</code> ; une ligne vide sépare deux paragraphes ; <code>\\</code> force un retour à la ligne.</li>
          <li><code>- item</code> pour une liste à puces, <code>+ item</code> pour une liste numérotée (un signe par ligne, l'indentation crée les sous-listes).</li>
          <li><code>// commentaire</code> jusqu'au bout de la ligne, <code>/* … */</code> sur plusieurs lignes.</li>
        </ul>

        <h3>Le code : fonctions, arguments nommés, contenus</h3>
        <p>Tout est fonction. Un appel s'écrit <code>#nom(arguments)[contenu]</code> :</p>
        <ul>
          <li>les <strong>arguments nommés</strong> se placent entre parenthèses : <code>#text(fill: red, size: 14pt)[Attention]</code> ;</li>
          <li>un <strong>bloc de contenu</strong> <code>[…]</code> contient du balisage : on peut y mettre du gras, des maths, d'autres commandes ;</li>
          <li>plusieurs blocs se suivent : <code>#definition[Titre][Corps]</code>.</li>
        </ul>
        <p><code>#let</code> crée une variable ou une fonction : <code>#let rappel(corps) = …</code>.</p>

        <h3>Deux règles qui remplacent le préambule</h3>
        <ul>
          <li><code>#set</code> change une valeur par défaut pour toute la suite : <code>#set text(size: 11pt)</code>, <code>#set list(marker: [▸])</code>.</li>
          <li><code>#show</code> transforme un élément partout : <code>#show "opposé": it =&gt; strong(it)</code> met ce mot en gras dans tout le document.</li>
        </ul>
        <p><code>#show: modele(…)</code> est une règle <code>show</code> sans cible : elle s'applique à tout le reste du document.</p>

        <h3>Ce qu'un utilisateur de LaTeX doit désapprendre</h3>
        <table>
          <tr><th>Réflexe LaTeX</th><th>En Typst</th></tr>
          <tr><td><code>\\textbf{…}</code>, <code>\\emph{…}</code></td><td><code>*…*</code>, <code>_…_</code></td></tr>
          <tr><td>accolades <code>{…}</code> pour le contenu</td><td>crochets <code>[…]</code> ; les accolades sont des blocs de code</td></tr>
          <tr><td><code>$AB$</code> (deux lettres collées)</td><td><code>$A B$</code> : lettres collées = un nom de variable</td></tr>
          <tr><td><code>$3,5$</code></td><td><code>$3","5$</code> ou <code>#num(3.5)</code> (la virgule seule sépare)</td></tr>
          <tr><td><code>\\frac{a}{b}</code>, <code>\\sqrt{2}</code>, <code>\\times</code></td><td><code>a/b</code>, <code>sqrt(2)</code>, <code>times</code></td></tr>
          <tr><td><code>\\[ … \\]</code></td><td><code>$ … $</code> avec une espace après le premier dollar et avant le second</td></tr>
          <tr><td><code>%</code> commentaire</td><td><code>//</code> (le <code>%</code> s'écrit tel quel)</td></tr>
          <tr><td>compiler deux fois pour les références</td><td>une seule compilation, toujours</td></tr>
        </table>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
          </div>
        </div>`,
      exemple: `
        <h3>Les trois modes dans un même fichier</h3>
        <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Nombres relatifs])

// 1. Une règle « set » : règle un réglage par défaut pour toute la suite.
#set list(marker: [▸])
// 2. Une règle « show » : chaque mot « opposé » sera écrit en gras.
#show "opposé": it =&gt; strong(it)
// 3. Une variable et une fonction à soi.
#let annee = 2026
#let piege(corps) = text(fill: red)[⚠ #corps]

= Les nombres relatifs            // titre de niveau 1
== Vocabulaire                    // titre de niveau 2

Un nombre relatif a un *signe* et une _distance à zéro_.
Deux nombres qui ont la même distance à zéro et des signes contraires sont opposés.

- $-3$ et $3$ sont opposés ;    // liste à puces : un tiret par item
- $0$ est son propre opposé.

+ Placer $-2$ sur la droite graduée.   // liste numérotée : un plus par item
+ Donner l'opposé de $-7","5$.

#piege[Ne pas confondre opposé et inverse.]

Mode code au milieu du texte : nous sommes en #annee, l'an prochain sera #(annee + 1).

Formule centrée, avec des espaces à l'intérieur des dollars :
$ -(-5) = 5 quad "et" quad -3 + 3 = 0 $</code></pre>
        <img src="/images/tutorials/typst/ty-02-syntaxe.png" alt="Rendu : titres numérotés, gras et italique, listes à puces et numérotées, texte rouge, calcul en mode code, formule centrée" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>À observer :</p>
        <ul>
          <li>la règle <code>show</code> a mis « opposé » en gras partout, même dans « opposés » ;</li>
          <li><code>#(annee + 1)</code> calcule : le mode code est un vrai langage de programmation ;</li>
          <li>les listes numérotées <code>+</code> prennent les pastilles de farfadet ;</li>
          <li>la formule centrée est alignée à gauche avec un retrait, comme l'option <code>fleqn</code> de bfcours.</li>
        </ul>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Traduisez cet extrait LaTeX en Typst, dans un document <code>modele("cours", niveau: "6e", theme: [Angles])</code>.</p>
            <pre><code>% Vocabulaire à revoir avec la classe.
\\section{Les angles}
\\subsection{Nommer un angle}

Un angle est formé de \\textbf{deux demi-droites} de même origine, appelée le \\emph{sommet}.

\\begin{itemize}
  \\item un angle aigu mesure moins de $90^\\circ$ ;
  \\item un angle obtus mesure entre $90^\\circ$ et $180^\\circ$.
\\end{itemize}

\\begin{enumerate}
  \\item Tracer un angle aigu.
  \\item Tracer un angle obtus.
\\end{enumerate}</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "6e", theme: [Angles])

// Vocabulaire à revoir avec la classe.
= Les angles
== Nommer un angle

Un angle est formé de *deux demi-droites* de même origine, appelée le _sommet_.

- un angle aigu mesure moins de $90°$ ;
- un angle obtus mesure entre $90°$ et $180°$.

+ Tracer un angle aigu.
+ Tracer un angle obtus.</code></pre><p><code>\\section</code> devient <code>=</code>, <code>itemize</code> des tirets, <code>enumerate</code> des plus. Le degré s'écrit <code>°</code> directement.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Écrivez une fonction <code>rappel</code> qui encadre un texte et le fait précéder d'un titre en gras. Le titre vaut « Rappel » par défaut et peut être changé par un argument nommé <code>titre</code>. Utilisez-la deux fois.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Priorités opératoires])

// Écrire ici la fonction rappel, puis l'utiliser deux fois.</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Priorités opératoires])

// Une fonction à soi : un argument nommé (avec une valeur par défaut) et un contenu.
#let rappel(titre: [Rappel], corps) = block(
  stroke: 0.6pt + gray, inset: 8pt, radius: 4pt, width: 100%,
)[*#titre :* #corps]

#rappel[On calcule d'abord les multiplications et les divisions.]

#rappel(titre: [Attention])[Les calculs entre parenthèses passent avant tout.]</code></pre><p><code>titre: [Rappel]</code> dans la définition donne la valeur par défaut. <code>block</code> est une fonction native de Typst : <code>stroke</code> (le cadre), <code>inset</code> (la marge intérieure), <code>radius</code> (les coins).</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Ce fichier a été écrit avec des réflexes LaTeX : il ne compile pas. Lisez le message d'erreur, puis corrigez les quatre fautes.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Proportionnalité])

#definition{Coefficient}{Le segment $AB$ mesure $3,5$ cm ; le coefficient vaut $\\frac{1}{2}$.}

Le \\textbf{double} de $AB$ vaut $7$ cm.</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Typst s'arrête sur la première : « <em>unknown variable: AB</em> », avec la suggestion « <em>try adding spaces between each letter: A B</em> ». Les quatre corrections :</p><ul><li>accolades → crochets : <code>#definition[…][…]</code> ;</li><li><code>$AB$</code> → <code>$A B$</code> ;</li><li><code>$3,5$</code> → <code>$3","5$</code> ;</li><li><code>\\frac{1}{2}</code> → <code>1/2</code>, et <code>\\textbf{…}</code> → <code>*…*</code>.</li></ul><pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Proportionnalité])

#definition[Coefficient][Le segment $A B$ mesure $3","5$ cm ; le coefficient vaut $1/2$.]

Le *double* de $A B$ vaut $7$ cm.</code></pre>
            </div>
          </details>
        </div>
      `,
    },
    duration: '20 min',
    tags: ['typst', 'syntaxe', 'latex'],
  },
  'ty-socle-modele': {
    id: 'ty-socle-modele',
    title: 'Le socle et le modèle de document',
    description: 'farfadet-socle (versions prof/élève, couleurs, réglages) et farfadet-modele (gabarit, bandeau, titres, variante dys)',
    parcours: 'typst',
    order: 2,
    sections: {
      info: `
        <h3>farfadet-socle : ce que tous les paquets partagent</h3>
        <h4>Version professeur ou élève</h4>
        <p>La version se choisit à la compilation (Ctrl+Maj+B produit les deux). Dans le document, <code>ifcorrection</code> écrit selon la version :</p>
        <table>
          <tr><th>Écriture</th><th>Professeur</th><th>Élève</th></tr>
          <tr><td><code>#ifcorrection[A][B]</code></td><td>A</td><td>B</td></tr>
          <tr><td><code>#ifcorrection[A]</code></td><td>A</td><td>rien</td></tr>
          <tr><td><code>#ifcorrection[][B]</code></td><td>rien</td><td>B</td></tr>
        </table>
        <p>
          <code>ifcorrection</code> écrit le texte tel quel. Pour une réponse <em>en couleur</em> qui laisse sa place vide chez l'élève :
          <code>#correction-box[…]</code> dans une phrase, ou une zone de réponse <code>#crep[…]</code> (capsule 8).
        </p>
        <h4>Couleurs nommées</h4>
        <p>
          Chaque environnement a sa couleur : <code>defi</code> (Définition, Notation), <code>prop</code>, <code>thm</code>,
          <code>ex</code>, <code>rem</code>, <code>meth</code>, <code>demo</code>, <code>act</code>, et <code>monrose</code> pour les corrections.
          <code>#setbfcolors(defi: rgb("#c2410c"))</code> les change d'un coup dans tous les paquets ;
          <code>#setbfcolors(reinitialiser: true)</code> revient aux couleurs d'origine. Une couleur s'écrit aussi
          à la manière de xcolor : <code>"prop!30"</code>, <code>"thm!60!black"</code>.
        </p>
        <h4>Un réglage par paquet, une même logique</h4>
        <p>
          Chaque paquet a un seul setter : <code>setbfsocle</code>, <code>setbfmodele</code>, <code>setbfenvironments</code>,
          <code>setrdexo</code>, <code>setrdcrep</code>… Un réglage vaut <strong>pour toute la suite du document</strong>.
          Priorité : la clé écrite sur l'objet l'emporte sur le réglage global. Une clé mal orthographiée arrête la
          compilation et <strong>liste les clés possibles</strong> : on ne devine jamais une clé, on lit le message.
        </p>

        <h3>farfadet-modele : le gabarit</h3>
        <p><code>#show: modele("cours", …)</code> pose la page A4, les polices, le bandeau et le pied de page. Ses clés principales :</p>
        <table>
          <tr><th>Clé</th><th>Valeurs</th></tr>
          <tr><td><code>niveau</code></td><td><code>"6e"</code> … <code>"3e"</code>, <code>"2nde"</code>, <code>"1re"</code>, <code>"Tle"</code> (exposant ajouté) ou un texte</td></tr>
          <tr><td><code>theme</code></td><td>le titre du chapitre, entre crochets</td></tr>
          <tr><td><code>type-document</code></td><td><code>"cours"</code>, <code>"exercices"</code>, <code>"activite"</code>, <code>"fiche"</code>, <code>"evaluation"</code> (bandeau avec cases Classe et Date)</td></tr>
          <tr><td><code>cycle</code>, <code>etablissement</code></td><td>le pied de page</td></tr>
          <tr><td><code>titres</code></td><td><code>"bfcours"</code> (bandeaux noirs), <code>"sobre"</code>, <code>"classique"</code>, <code>"rd"</code></td></tr>
          <tr><td><code>numeros</code></td><td><code>"arabe"</code>, <code>"romain"</code>, <code>"lettres"</code></td></tr>
          <tr><td><code>sommaire</code></td><td><code>true</code> : table des matières sous le bandeau</td></tr>
          <tr><td><code>dys</code></td><td><code>true</code> : police sans empattement, 14 pt, interligne × 1,2, mots espacés, texte non justifié</td></tr>
        </table>
        <p>
          Sans <code>niveau</code> ni <code>theme</code>, aucun bandeau n'est posé. Pour poser un bandeau en cours de document
          (une partie « Solutions », un second chapitre) : <code>#chapitre(niveau: …, theme: […])</code>.
        </p>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
          </div>
        </div>`,
      exemple: `
        <h3>Une fiche de 1re, réglée en tête de fichier</h3>
        <pre><code>#import "@preview/farfadet:0.2.0": *

// Le gabarit : bandeau, pied de page, titres et sommaire réglés en une fois.
#show: modele(
  "cours",
  niveau: "1re",
  theme: [Suites numériques],
  type-document: "fiche",          // libellé du bandeau : « Fiche »
  cycle: [Lycée],                  // pied de page, à droite
  etablissement: [du Parc],
  titres: "sobre",                 // "bfcours" (défaut), "sobre", "classique", "rd"
  numeros: "romain",               // I, II… puis 1., 2.…
  sommaire: true,                  // table des matières sous le bandeau
  colonnes-sommaire: 1,
)

// Le socle : couleurs nommées et couleur des corrections.
#setbfcolors(defi: rgb("#c2410c"))           // les Définitions passent en orange
#setbfsocle(correction-color: "prop")        // les réponses du prof en bleu « prop »

= Définir une suite
#definition[Suite numérique][Une suite associe à chaque entier naturel $n$ un réel $u_n$.]

= Calculer des termes
Pour $u_n = 2 n + 1$ : $u_3 =$ #correction-box[$7$].

// Un texte différent selon la version.
#ifcorrection[Rappel prof : insister sur l'indice.][Astuce : remplace $n$ par $3$.]</code></pre>
        <img src="/images/tutorials/typst/ty-03-socle-modele.png" alt="Rendu prof et élève : bandeau Fiche, sommaire, titres sobres en chiffres romains, définition orange, réponse 7 en bleu chez le professeur seulement" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>À observer :</p>
        <ul>
          <li>le sommaire liste les titres <em>et</em> les environnements titrés ;</li>
          <li>la Définition a pris la couleur orange de <code>setbfcolors</code> ;</li>
          <li>la réponse <em>7</em> est en bleu chez le professeur et laisse un blanc chez l'élève ;</li>
          <li>les deux lignes <code>ifcorrection</code> ont donné un texte différent dans chaque version.</li>
        </ul>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Transformez ce cours en évaluation (bandeau avec cases Classe et Date), en version adaptée aux élèves dys, avec la famille de polices Latin Modern Sans.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Calcul littéral])

#exo(level: 1)[Développer][
  Développer $3(x + 2)$.
  #crep[$3 x + 6$]
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
// Famille de la variante dys, avant le modèle : "Fira" (défaut), "lmodern", "tgheros".
#choice-fonts-dys("lmodern")
#show: modele(
  "cours",
  niveau: "4e",
  theme: [Calcul littéral],
  type-document: "evaluation",   // bandeau d'évaluation : cases Classe et Date
  dys: true,                     // police sans empattement, 14 pt, interligne élargi
)

#exo(level: 1)[Développer][
  Développer $3(x + 2)$.
  #crep[$3 x + 6$]
]</code></pre><p><code>choice-fonts-dys</code> s'écrit <strong>avant</strong> <code>#show: modele</code>. La famille par défaut, Fira, n'est pas fournie avec la suite : sans ses fichiers, Typst prend une police de repli ; <code>"lmodern"</code> et <code>"tgheros"</code> sont fournies.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Faites en sorte que la consigne « Écris d'abord… » n'apparaisse que chez l'élève, que la note « Prévoir 10 minutes… » n'apparaisse que chez le professeur, et que la probabilité soit écrite en couleur chez le professeur et laissée en blanc chez l'élève.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Probabilités], type-document: "activite")

On lance un dé équilibré à six faces.

Écris d'abord toutes les issues possibles.

Prévoir 10 minutes ; certains oublient l'issue 6.

La probabilité d'obtenir un nombre pair vaut ...</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Probabilités], type-document: "activite")

On lance un dé équilibré à six faces.

// Consigne pour l'élève seulement (rien chez le professeur).
#ifcorrection[][Écris d'abord toutes les issues possibles.]

// Note pour le professeur seulement (rien chez l'élève).
#ifcorrection[Prévoir 10 minutes ; certains oublient l'issue 6.]

// Une réponse en couleur chez le professeur, la même place vide chez l'élève.
La probabilité d'obtenir un nombre pair vaut #correction-box[$3/6 = 1/2$].</code></pre><p>Vérifiez dans les deux PDF : la note du professeur ne doit jamais apparaître dans <code>…-eleve.pdf</code>.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Écrivez le modèle avec <code>farfadet.with</code>, numérotez les parties par lettres (A, B…), passez la première propriété en vert foncé, puis revenez aux couleurs d'origine pour la seconde.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "Tle", theme: [Logarithme])

= Définition
#propriete[Logarithme d'un produit][Pour tous réels $a &gt; 0$ et $b &gt; 0$, $ln(a b) = ln(a) + ln(b)$.]

= Propriétés
#propriete[Logarithme d'un quotient][Pour tous réels $a &gt; 0$ et $b &gt; 0$, $ln(a / b) = ln(a) - ln(b)$.]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
// farfadet.with(…) est l'autre écriture du modèle « cours » : mêmes clés.
#show: farfadet.with(niveau: "Tle", theme: [Logarithme], numeros: "lettres")

= Définition
// Toutes les Propriétés en vert foncé, à partir d'ici.
#setbfcolors(prop: rgb("#15803d"))
#propriete[Logarithme d'un produit][Pour tous réels $a &gt; 0$ et $b &gt; 0$, $ln(a b) = ln(a) + ln(b)$.]

= Propriétés
// Retour aux couleurs d'origine pour la suite du document.
#setbfcolors(reinitialiser: true)
#propriete[Logarithme d'un quotient][Pour tous réels $a &gt; 0$ et $b &gt; 0$, $ln(a / b) = ln(a) - ln(b)$.]</code></pre><p>Un setter vaut pour toute la suite du document, même écrit dans un bloc : <code>reinitialiser: true</code> est le moyen de revenir en arrière.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '20 min',
    tags: ['typst', 'farfadet-socle', 'farfadet-modele', 'prof-eleve', 'dys'],
  },
  'ty-didactique': {
    id: 'ty-didactique',
    title: 'Les environnements didactiques',
    description: 'Définition, Propriété, Exemple, Méthode, Remarque… : clés, vocabulaire, sommaire et skins (farfadet-didactique)',
    parcours: 'typst',
    order: 3,
    sections: {
      info: `
        <h3>Les boîtes du cours sont des commandes</h3>
        <table>
          <tr><th>Commande</th><th>Usage</th><th>Couleur</th></tr>
          <tr><td><code>#definition</code>, <code>#notation</code></td><td>définir, noter</td><td><code>defi</code></td></tr>
          <tr><td><code>#propriete</code>, <code>#theoreme</code></td><td>énoncer</td><td><code>prop</code>, <code>thm</code></td></tr>
          <tr><td><code>#demonstration</code></td><td>prouver</td><td><code>demo</code></td></tr>
          <tr><td><code>#methode</code></td><td>savoir-faire</td><td><code>meth</code></td></tr>
          <tr><td><code>#exemple</code>, <code>#contre-exemple</code></td><td>illustrer</td><td><code>ex</code></td></tr>
          <tr><td><code>#remarque</code>, <code>#aide</code>, <code>#histoire</code></td><td>compléter</td><td><code>rem</code>, <code>nota</code></td></tr>
          <tr><td><code>#activite</code>, <code>#vocabulaire</code>, <code>#solution</code></td><td>découvrir, lexique, corriger</td><td><code>act</code>, <code>nota</code></td></tr>
        </table>
        <ul>
          <li>Deux paires de crochets : titre puis corps, <code>#definition[Titre][Corps]</code>. Une seule : pas de titre, <code>#remarque[Corps]</code>.</li>
          <li>Les noms s'écrivent <strong>sans accent</strong> : <code>#propriete</code>, <code>#methode</code>.</li>
          <li>Les clés vont entre parenthèses, avant les crochets : <code>#propriete(numero: true)[…][…]</code>.</li>
        </ul>
        <h4>Les clés les plus utiles</h4>
        <ul>
          <li><code>numero: true</code> numérote (« Propriété 1.1 ») ; <code>label: &lt;nom&gt;</code> permet d'y renvoyer par <code>@nom</code> ;</li>
          <li><code>couleur: "teal"</code> ou <code>couleur: rgb("#c2185b")</code> pour un seul objet ;</li>
          <li><code>version: "prof"</code> ou <code>"eleve"</code> : l'objet n'apparaît que dans cette version ;</li>
          <li><code>breakable: true</code> autorise la coupure entre deux pages ; <code>sommaire: false</code> le retire du sommaire.</li>
        </ul>
        <h4>À la manière de LaTeX</h4>
        <p>Pour un long corps, la forme environnement évite les crochets imbriqués :</p>
        <pre><code>#begin(propriete, numero: true)[Chasles]
  Pour tous points $A$, $B$, $C$ : $vect(A B) + vect(B C) = vect(A C)$.
#end(propriete)</code></pre>

        <h3>Vocabulaire et sommaire</h3>
        <ul>
          <li><code>#voc[mot]</code> met un mot de vocabulaire en valeur <em>et</em> le range dans l'index ; <code>#printvocindex()</code> affiche cet index ;</li>
          <li><code>#acc[…]</code> met en couleur une notion importante (la couleur suit l'environnement où il se trouve) ;</li>
          <li><code>#tableofcontents()</code> pose le sommaire où l'on veut (ou <code>sommaire: true</code> dans le modèle).</li>
        </ul>
        <p>Une fonction sans argument s'appelle avec <code>()</code> : sans les parenthèses, son nom s'affiche au lieu de l'index.</p>

        <h3>Les skins : changer la forme, pas le contenu</h3>
        <p>
          La clé <code>rendu</code> choisit la forme de la boîte : <code>"bf"</code> (défaut, rendu bfcours), <code>"rd"</code>,
          ou un des skins <code>"cahier"</code>, <code>"outil"</code>, <code>"pastille"</code>, <code>"manchette"</code>,
          <code>"filet"</code>, <code>"suspendu"</code>, <code>"minimal"</code>. Pour un objet : <code>#methode(rendu: "manchette")[…]</code> ;
          pour tout un type : <code>#setbfenvironments(pour: "Definition", rendu: "pastille")</code>.
        </p>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
          </div>
        </div>`,
      exemple: `
        <h3>Un début de cours de 4e</h3>
        <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Le théorème de Pythagore])

= Le théorème

// Titre puis corps : deux paires de crochets.
#definition[Hypoténuse][
  Dans un triangle rectangle, l'#voc[hypoténuse] est le côté opposé à l'angle droit.
  C'est #acc[le plus long] des trois côtés.
]

// Une clé se place entre parenthèses, avant les crochets.
#propriete(numero: true)[Pythagore][
  Si le triangle $A B C$ est rectangle en $A$, alors $B C^2 = A B^2 + A C^2$.
]

#exemple[Un calcul][Si $A B = 3$ et $A C = 4$, alors $B C^2 = 9 + 16 = 25$, donc $B C = 5$.]

// Un seul contenu : la boîte n'a pas de titre.
#remarque[On n'applique le théorème qu'à un triangle #acc[rectangle].]

// Un skin change la forme de la boîte, pas son contenu.
#methode(rendu: "manchette")[Rédiger][
  On cite le triangle rectangle, on écrit l'égalité, on remplace, on calcule.
]</code></pre>
        <img src="/images/tutorials/typst/ty-04-didactique.png" alt="Rendu : Définition verte avec vocabulaire en gras, Propriété 1.1 bleue numérotée, Exemple dans un cadre à équerre, Remarque avec crayon, Méthode au skin manchette" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>
          Chaque environnement garde son identité (couleur, icône), et <code>#acc</code> prend la couleur de la boîte
          qui l'entoure : vert dans la Définition, rouge dans la Remarque. La Méthode, en skin <code>manchette</code>,
          place son étiquette dans la marge gauche.
        </p>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Écrivez une Définition intitulée « Parallélogramme » (le mot marqué comme vocabulaire, « parallèles » mis en valeur), une Propriété sur ses diagonales et une Remarque sans titre.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Parallélogrammes])

// Un parallélogramme est un quadrilatère dont les côtés opposés sont parallèles deux à deux.
// Ses diagonales se coupent en leur milieu.
// Un rectangle est un parallélogramme particulier.</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Parallélogrammes])

#definition[Parallélogramme][
  Un #voc[parallélogramme] est un quadrilatère dont les côtés opposés sont #acc[parallèles] deux à deux.
]

#propriete[Diagonales][Les diagonales d'un parallélogramme se coupent en leur #acc[milieu].]

#remarque[Un rectangle est un parallélogramme particulier.]</code></pre>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Numérotez la propriété et donnez-lui une étiquette. Ajoutez une Méthode, un Exemple qui renvoie à la propriété par son numéro, et un Contre-exemple.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Arithmétique])

#propriete[Divisibilité par 3][
  Un entier est divisible par $3$ si la somme de ses chiffres est divisible par $3$.
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Arithmétique])

#propriete(numero: true, label: &lt;prop-divisible-3&gt;)[Divisibilité par 3][
  Un entier est divisible par $3$ si la somme de ses chiffres est divisible par $3$.
]

#methode[Tester la divisibilité par 3][On additionne les chiffres, puis on regarde si la somme est dans la table de $3$.]

#exemple[Le nombre 471][$4 + 7 + 1 = 12$ et $12$ est divisible par $3$ : d'après la propriété @prop-divisible-3, $471$ l'est aussi.]

#contre-exemple[Le nombre 472][$4 + 7 + 2 = 13$ : $472$ n'est pas divisible par $3$.]</code></pre><p>Le renvoi <code>@prop-divisible-3</code> affiche le numéro de la propriété ; il se met à jour tout seul si l'on ajoute une propriété avant.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Ajoutez un sommaire en tête et l'index du vocabulaire à la fin. Donnez le skin <code>pastille</code> à toutes les Définitions, et le skin <code>filet</code> à la seule Propriété.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "2nde", theme: [Vecteurs])

= Translation
#definition[Translation][La #voc[translation] qui envoie $A$ sur $B$ fait glisser chaque point dans la même direction.]

= Vecteur
#definition[Vecteur][Le #voc[vecteur] $vect(A B)$ est associé à cette translation.]

#propriete[Égalité][$vect(A B) = vect(C D)$ si et seulement si $A B D C$ est un parallélogramme.]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "2nde", theme: [Vecteurs])

// Toutes les Définitions du document avec le skin « pastille ».
#setbfenvironments(pour: "Definition", rendu: "pastille")

#tableofcontents()

= Translation
#definition[Translation][La #voc[translation] qui envoie $A$ sur $B$ fait glisser chaque point dans la même direction.]

= Vecteur
#definition[Vecteur][Le #voc[vecteur] $vect(A B)$ est associé à cette translation.]

// Ce seul objet avec un autre skin.
#propriete(rendu: "filet")[Égalité][$vect(A B) = vect(C D)$ si et seulement si $A B D C$ est un parallélogramme.]

#printvocindex()</code></pre><p>Le nom du type dans <code>pour:</code> s'écrit comme dans bfcours, avec une majuscule : <code>"Definition"</code>, <code>"Propriete"</code>, <code>"Methode"</code>.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '20 min',
    tags: ['typst', 'farfadet-didactique', 'environnements', 'skins'],
  },
  'ty-enum-colonnes': {
    id: 'ty-enum-colonnes',
    title: 'Questions numérotées et colonnes',
    description: 'farfadet-enum : tcbenumerate, sous-questions, colonnes, multi-colonnes et tcbitem',
    parcours: 'typst',
    order: 4,
    sections: {
      info: `
        <h3>tcbenumerate : les questions à pastilles</h3>
        <ul>
          <li>Un seul bloc de crochets, une question par <code>+</code> en début de ligne.</li>
          <li>Sous-questions : un second <code>#tcbenumerate</code> décalé sous la question (numéros a., b.…).</li>
          <li><code>columns: 3</code> répartit les questions sur trois colonnes, dans l'ordre de lecture.</li>
          <li><code>depart: 4</code> reprend la numérotation à 4 (utile après un texte ou une figure).</li>
        </ul>
        <p><strong>Piège :</strong> <code>#tcbenumerate[Q1][Q2]</code> (un bloc par question) est refusé ; le message d'erreur montre l'écriture en items.</p>

        <h3>multi-colonnes : du contenu côte à côte</h3>
        <ul>
          <li>Un <code>-</code> par colonne : <code>#multi-colonnes[ - texte - figure ]</code>.</li>
          <li><code>#multi-colonnes(3)[…]</code> : trois colonnes égales ; <code>largeurs: (2, 1)</code> : deux tiers et un tiers.</li>
          <li><code>filets: 0.5pt + gray</code> trace un trait entre les colonnes.</li>
          <li>Une case plus large : <code>#tcbitem(raster-multicolumn: 2)[…]</code>, écrit <em>à la place</em> d'un <code>-</code> (jamais <code>- #tcbitem</code>). Autres clés de <code>tcbitem</code> : <code>halign: "center"</code>, <code>colback: …</code>.</li>
        </ul>
        <p>
          <strong>N'utilisez pas</strong> <code>columns()</code> natif de Typst : il ne transmet pas la largeur des colonnes aux boîtes
          (définitions, zones de réponse), qui débordent.
        </p>

        <h3>Les listes ordinaires</h3>
        <p>
          Les listes <code>-</code> et <code>+</code> du texte suivent les règles de bfcours. Pour régler leur retrait :
          <code>#itemize(leftmargin: 10pt)[ - … - … ]</code> (un <code>#set list(indent: …)</code> n'a pas d'effet sur elles).
        </p>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
          </div>
        </div>`,
      exemple: `
        <h3>Une page de calcul mental</h3>
        <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "6e", theme: [Calcul mental], type-document: "exercices")

// Questions numérotées : un « + » par question, un seul bloc de crochets.
#tcbenumerate[
  + Calculer $125 + 75$.
  + Écrire ce résultat :
    // Sous-questions : un tcbenumerate dans la question.
    #tcbenumerate[
      + en lettres ;
      + comme un nombre de dizaines.
    ]
]

// Une liste sur trois colonnes, qui reprend au numéro 3.
#tcbenumerate(columns: 3, depart: 3)[
  + $7 times 8$
  + $9 times 6$
  + $12 times 5$
  + $56 div 7$
  + $54 div 9$
  + $60 div 12$
]

// Texte et encadré côte à côte : un « - » par colonne, largeurs 2/3 et 1/3.
#multi-colonnes(largeurs: (2, 1), filets: 0.5pt + gray)[
  - Pour multiplier par $5$, on multiplie par $10$ puis on divise par $2$ :
    $48 times 5 = 480 div 2 = 240$.
  - #remarque[Astuce à retenir.]
]

// Une case qui prend deux colonnes sur trois : tcbitem à la place d'un « - ».
#multi-colonnes(3)[
  #tcbitem(raster-multicolumn: 2)[Cette case occupe deux colonnes : idéal pour un énoncé long.]
  - Une figure ici.
]</code></pre>
        <img src="/images/tutorials/typst/ty-05-enum-colonnes.png" alt="Rendu : questions 1 et 2 avec sous-questions a et b, questions 3 à 8 sur trois colonnes, texte et remarque côte à côte séparés par un filet, case sur deux colonnes" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>
          La seconde liste commence bien à 3. Le filet vertical sépare le texte de la remarque ; la dernière ligne
          montre une case qui occupe deux colonnes sur trois.
        </p>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Disposez ces six calculs sur trois colonnes, sans en perdre.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "6e", theme: [Calcul mental], type-document: "exercices")

#tcbenumerate[
  + $25 + 17$
  + $63 - 28$
  + $15 times 4$
  + $72 div 8$
  + $125 + 75$
  + $100 - 37$
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "6e", theme: [Calcul mental], type-document: "exercices")

#tcbenumerate(columns: 3)[
  + $25 + 17$
  + $63 - 28$
  + $15 times 4$
  + $72 div 8$
  + $125 + 75$
  + $100 - 37$
]</code></pre><p>Avec <code>columns: 2</code>, on obtient trois rangées de deux : essayez les deux et gardez la plus lisible.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Placez les trois définitions côte à côte, en donnant un peu plus de place à la troisième, avec un filet entre les colonnes.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Quadrilatères])

#definition[Un #voc[rectangle] est un quadrilatère qui a quatre angles droits.]

#definition[Un #voc[losange] est un quadrilatère qui a quatre côtés de même longueur.]

#definition[Un #voc[carré] est un quadrilatère qui est à la fois un rectangle et un losange.]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Quadrilatères])

#multi-colonnes(largeurs: (1, 1, 1.3), filets: 0.5pt + gray)[
  - #definition[Un #voc[rectangle] est un quadrilatère qui a quatre angles droits.]
  - #definition[Un #voc[losange] est un quadrilatère qui a quatre côtés de même longueur.]
  - #definition[Un #voc[carré] est un quadrilatère qui est à la fois un rectangle et un losange.]
]</code></pre><p>Il y a autant de colonnes que de nombres dans <code>largeurs</code> : <code>(1, 1, 1.3)</code> donne trois colonnes, la dernière 30 % plus large.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Mettez les trois questions à gauche (trois cinquièmes de la largeur) et l'exemple à droite. La dernière question, plus bas, doit porter le numéro 4.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Puissances], type-document: "exercices")

#tcbenumerate[
  + Écrire $10 times 10 times 10$ sous la forme $10^n$.
  + Calculer $2^5$.
  + Comparer $3^2$ et $2^3$.
]

#exemple[Un rappel][$5^3 = 5 times 5 times 5 = 125$.]

// Plus loin dans la fiche : cette question doit porter le numéro 4.
#tcbenumerate[
  + Écrire $1 / 10^2$ en écriture décimale.
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Puissances], type-document: "exercices")

#multi-colonnes(largeurs: (3, 2))[
  - #tcbenumerate[
      + Écrire $10 times 10 times 10$ sous la forme $10^n$.
      + Calculer $2^5$.
      + Comparer $3^2$ et $2^3$.
    ]
  - #exemple[Un rappel][$5^3 = 5 times 5 times 5 = 125$.]
]

// La suite de la numérotation, plus loin dans la fiche.
#tcbenumerate(depart: 4)[
  + Écrire $1 / 10^2$ en écriture décimale.
]</code></pre><p>Une colonne de <code>multi-colonnes</code> peut contenir n'importe quoi, y compris une liste numérotée. <code>depart: 4</code> poursuit la numérotation.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '15 min',
    tags: ['typst', 'farfadet-enum', 'colonnes', 'tcbenumerate'],
  },
  'ty-maths': {
    id: 'ty-maths',
    title: 'Écrire des maths',
    description: 'Les maths natives de Typst (fractions, racines, alignements, cases) et les ajouts de farfadet-maths',
    parcours: 'typst',
    order: 5,
    sections: {
      info: `
        <h3>Les maths natives</h3>
        <p><code>$x + 1$</code> est dans la phrase ; <code>$ x + 1 $</code> (une espace après le premier dollar et avant le second) est posé sur sa ligne.</p>
        <table>
          <tr><th>Pour écrire</th><th>Typst</th><th>LaTeX</th></tr>
          <tr><td>fraction</td><td><code>3/4</code>, <code>(n + 1)/2</code></td><td><code>\\frac{3}{4}</code></td></tr>
          <tr><td>puissance, indice</td><td><code>10^(-3)</code>, <code>u_(n+1)</code></td><td><code>10^{-3}</code>, <code>u_{n+1}</code></td></tr>
          <tr><td>racines</td><td><code>sqrt(2)</code>, <code>root(3, 8)</code></td><td><code>\\sqrt{2}</code>, <code>\\sqrt[3]{8}</code></td></tr>
          <tr><td>opérations</td><td><code>times</code>, <code>div</code>, <code>!=</code>, <code>&lt;=</code>, <code>approx</code></td><td><code>\\times</code>, <code>\\div</code>, <code>\\neq</code>, <code>\\leq</code></td></tr>
          <tr><td>ensembles</td><td><code>NN</code>, <code>ZZ</code>, <code>QQ</code>, <code>RR</code>, <code>in</code>, <code>subset</code></td><td><code>\\mathbb{N}</code>, <code>\\in</code></td></tr>
          <tr><td>infini, flèches</td><td><code>+oo</code>, <code>-&gt;</code>, <code>|-&gt;</code>, <code>=&gt;</code></td><td><code>+\\infty</code>, <code>\\to</code>, <code>\\mapsto</code></td></tr>
          <tr><td>somme, limite</td><td><code>sum_(k=1)^n</code>, <code>lim_(x -&gt; +oo)</code></td><td><code>\\sum_{k=1}^n</code></td></tr>
          <tr><td>système, accolade</td><td><code>cases(x + y = 5, x - y = 1)</code></td><td><code>\\begin{cases}</code></td></tr>
          <tr><td>texte dans une formule</td><td><code>"pour tout"</code></td><td><code>\\text{pour tout}</code></td></tr>
        </table>
        <p>Les parenthèses <em>regroupent</em> sans s'afficher : <code>(n + 1)/2</code> met tout <code>n + 1</code> au numérateur. Dans une formule posée, <code>&amp;</code> aligne les lignes et <code>\\</code> passe à la ligne suivante.</p>
        <h4>Trois pièges</h4>
        <ul>
          <li><code>$AB$</code> est lu comme une variable nommée AB : écrire <code>$A B$</code>.</li>
          <li><code>$3,5$</code> donne « 3, 5 » : écrire <code>$3","5$</code> ou <code>#num(3.5)</code>.</li>
          <li>Dans les dollars, les fonctions s'écrivent <strong>sans</strong> <code>#</code> : <code>$sqrt(2)$</code>, <code>$vect(A B)$</code>.</li>
        </ul>

        <h3>Les ajouts de farfadet-maths</h3>
        <table>
          <tr><th>Écriture</th><th>Rendu</th></tr>
          <tr><td><code>$vect(A B)$</code></td><td>vecteur, flèche qui s'étire</td></tr>
          <tr><td><code>$coordonnees(3, -1, nom: A)$</code></td><td>A(3 ; −1), valeurs sur fond gris, point-virgule à la française</td></tr>
          <tr><td><code>$rep$</code></td><td>le repère (O ; I ; J)</td></tr>
          <tr><td><code>$intervalle(0, 1, forme: "fo")$</code></td><td>[0 ; 1[ ; formes <code>"ff"</code>, <code>"oo"</code>, <code>"fo"</code>, <code>"of"</code></td></tr>
          <tr><td><code>$dd$</code></td><td>l'ensemble 𝔻 des décimaux</td></tr>
          <tr><td><code>#num(1234.5)</code></td><td>1 234,5 (espaces fines, virgule)</td></tr>
          <tr><td><code>#qty(9.81, "m/s^2")</code></td><td>9,81 m·s<sup>−2</sup> ; <code>#unit("cm")</code> pour l'unité seule</td></tr>
          <tr><td><code>#si()</code>, <code>#alors()</code>, <code>#donc()</code>, <code>#car()</code>, <code>#ssi()</code></td><td>connecteurs logiques colorés</td></tr>
          <tr><td><code>#encadrer[…]</code>, <code>#surligner[…]</code>, <code>#frquote[…]</code></td><td>encadré pâle, surligné, « guillemets »</td></tr>
        </table>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
          </div>
        </div>`,
      exemple: `
        <h3>Tour d'horizon en une page</h3>
        <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "2nde", theme: [Écrire des maths], sommaire: false)

= Maths natives de Typst

// Dans la phrase : $…$ collé. Formule centrée : une espace après $ et avant $.
Fraction $3/4$, puissance $10^(-3)$, indice $u_(n+1)$, racine $sqrt(2)$ et $root(3, 8) = 2$.

$ (a + b)^2 = a^2 + 2 a b + b^2 quad "pour tous réels" a, b $

// Alignement : &amp; marque la colonne, \\ passe à la ligne.
$ f(x) &amp;= 2(x - 1)^2 + 3 \\
       &amp;= 2 x^2 - 4 x + 5 $

// Accolade d'un système ou d'une fonction définie par morceaux.
$ cases(2 x - y = 4, x + 3 y = 9) quad |x| = cases(x &amp;"si" x &gt;= 0, -x &amp;"si" x &lt; 0) $

= Les ajouts de farfadet-maths

// Sans # dans les dollars.
$NN subset ZZ subset dd subset QQ subset RR$ ; $x in intervalle(-1, 3, forme: "fo")$ ;
dans le repère $rep$, $coordonnees(2, -1, nom: A)$ et $vect(A B) coordonnees(3, 4)$.

// Avec # dans le texte : nombres et grandeurs à la française.
#num(1234567.891) ; #qty(9.81, "m/s^2") ; #qty(2.5, "cm") ;
#si() $x &gt; 0$, #alors() $x^2 &gt; 0$. À retenir : #encadrer[$a^2 + b^2 = c^2$].</code></pre>
        <img src="/images/tutorials/typst/ty-06-maths.png" alt="Rendu : fractions, puissances, racines, identité remarquable, calcul aligné sur le signe égal, système et valeur absolue, ensembles, intervalle, repère, coordonnées, vecteur, nombres à la française, connecteurs colorés, formule encadrée" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>
          Les deux lignes de <code>f(x)</code> sont alignées sur le signe <code>=</code> grâce à <code>&amp;</code>. Dans
          <code>cases</code>, le <code>&amp;</code> aligne les conditions « si ». <code>#num</code> a regroupé les chiffres par trois.
        </p>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Maths de collège : réécrivez en Typst les calculs écrits en toutes lettres (fractions, puissance, racine, ligne centrée, longueurs à la française).</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Calculs])

// Les calculs sont écrits en toutes lettres : réécrivez-les entre dollars.
Calculer : 3 quarts plus 1 huitième, puis 2 puissance 5, et la racine carrée de 81.

Sur une ligne à part : 3 fois 32 égale 96, et 96 divisé par 8 égale 12.

Un côté du carré mesure 2,5 cm ; son aire vaut 6,25 cm².</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Calculs])

Calculer : $3/4 + 1/8 = 6/8 + 1/8 = 7/8$, puis $2^5 = 32$ et $sqrt(81) = 9$.

$ 3 times 32 = 96 quad "et" quad 96 div 8 = 12 $

Un côté du carré mesure #qty(2.5, "cm") ; son aire vaut #qty(6.25, "cm^2").</code></pre>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Maths de lycée : réécrivez les quatre lignes avec les écritures de la suite (<code>vect</code>, <code>coordonnees</code>, <code>intervalle</code>) et les écritures natives (<code>cases</code>, <code>sum</code>).</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "1re", theme: [Écritures de lycée])

// Réécrivez les maths entre dollars, avec les écritures de la suite.
Le vecteur u a pour coordonnées (-2 ; 5).

Pour tout x de l'intervalle [-1 ; 3[, on a f(x) &gt; 0.

Résoudre le système : 2x - y = 4 et x + 3y = 9.

La somme des entiers de 1 à n vaut n(n + 1)/2.</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "1re", theme: [Écritures de lycée])

Le vecteur $vect(u)$ a pour coordonnées $coordonnees(-2, 5)$.

Pour tout $x in intervalle(-1, 3, forme: "fo")$, on a $f(x) &gt; 0$.

Résoudre le système : $ cases(2 x - y = 4, x + 3 y = 9) $

La somme des entiers de $1$ à $n$ vaut $sum_(k=1)^n k = (n(n + 1))/2$.</code></pre><p>Attention à <code>(n(n + 1))/2</code> : sans les parenthèses extérieures, seul <code>(n + 1)</code> passerait au numérateur.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Posez la résolution en quatre lignes alignées sur le signe égal, et écrivez la distance Terre-Soleil à la française.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Équations])

Résolvons 5x - 3 = 2x + 9 :

5x - 3 = 2x + 9, puis 5x - 2x = 9 + 3, puis 3x = 12, enfin x = 4.

La Terre est à environ 149600000 km du Soleil.</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Équations])

Résolvons $5 x - 3 = 2 x + 9$ :
$ 5 x - 3 &amp;= 2 x + 9 \\
  5 x - 2 x &amp;= 9 + 3 \\
  3 x &amp;= 12 \\
  x &amp;= 4 $

La Terre est à environ #num(149600000) km du Soleil, soit $1","496 times 10^8$ km.</code></pre><p><code>#num(149600000)</code> affiche 149 600 000 avec des espaces fines insécables.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '25 min',
    tags: ['typst', 'maths', 'farfadet-maths'],
  },
  'ty-exo': {
    id: 'ty-exo',
    title: 'Exercices, corrigés et barème',
    description: 'farfadet-exo : exercices numérotés, niveaux, corrigés en fin de document, points par question, compétences',
    parcours: 'typst',
    order: 6,
    sections: {
      info: `
        <h3>Un exercice</h3>
        <p><code>#exo(level: 2, tags: "…")[Titre][Énoncé #exocorrection Correction]</code> :</p>
        <ul>
          <li>le bandeau « ■ Exercice n – Titre » est numéroté automatiquement ;</li>
          <li><code>level</code> donne les étoiles, de 0 à 3 (demi-étoiles permises, <code>none</code> pour aucune) ;</li>
          <li><code>tags</code> : étiquettes (compétence, chapitre), une chaîne <code>"a, b"</code> ou un tableau ;</li>
          <li><code>#exocorrection</code> est un <strong>marqueur</strong>, pas une clé : ce qui le suit est la correction. Il se place une fois, au premier niveau du corps (pas dans une liste ni des colonnes).</li>
        </ul>
        <h3>Les corrigés regroupés</h3>
        <p>
          Les corrections sont mises de côté, puis <code>#rdexocorrection(0)</code> les affiche toutes, avec un bandeau
          « Solution de l'exercice n ». Il s'affiche dans les deux versions : l'entourer de <code>#ifcorrection[…]</code>,
          comme le <code>\\ifcorrection … \\fi</code> de LaTeX.
        </p>
        <h3>Points et barème</h3>
        <ul>
          <li><code>+ #itempoint(2)[Énoncé.]</code> : les points en tête de la question, l'énoncé entre crochets ;</li>
          <li><code>#displayitempoints(true)</code> rend les boîtes « 2 pts » visibles (sans lui, les points sont comptés mais cachés) ;</li>
          <li><code>#setrdexo(display-score: true)</code> affiche dans chaque bandeau le total de l'exercice, calculé ;</li>
          <li><code>#getsavedtotalpoints()</code> écrit le total du sujet, n'importe où, même avant les exercices.</li>
        </ul>
        <h3>Évaluer par compétences</h3>
        <ul>
          <li><code>#exo-eval(tags: "Raisonner")[Titre][…]</code> : un exercice dont l'en-tête porte une grille de maîtrise à quatre niveaux ;</li>
          <li><code>#printcompindex()</code> dresse le tableau des compétences évaluées (étiquettes des <code>exo-eval</code> et titres des <code>exo</code>) ;</li>
          <li>cartouche d'évaluation : <code>#tableau-eval(55)</code> (durée en minutes), <code>#chrono(30)</code>, <code>#pascalc()</code> (calculatrice interdite).</li>
        </ul>
        <h3>Autres réglages</h3>
        <p>
          <code>skin</code> change l'en-tête : <code>"bouyachakka"</code> (défaut), <code>"default"</code>, <code>"pooja"</code>,
          <code>"rikid"</code>, <code>"griba"</code>, <code>"exobac"</code>, <code>"exobrevet"</code>, <code>"exolombards"</code>.
          <code>#needspace(7cm)</code> avant un exercice le fait passer à la page suivante s'il ne reste pas assez de place.
        </p>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
          </div>
        </div>`,
      exemple: `
        <h3>Une évaluation courte, barème calculé</h3>
        <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Équations], type-document: "evaluation")

// Réglages des exercices : score calculé dans le bandeau, boîtes de points visibles.
#setrdexo(display-score: true)
#displayitempoints(true)

Note : #h(2cm) / #getsavedtotalpoints()   // total du sujet, calculé tout seul

// level = étoiles (0 à 3) ; tags = étiquettes (compétence, chapitre…).
#exo(level: 1, tags: "Calculer")[Équations du premier degré][
  // Les points en tête de la question, l'énoncé entre crochets.
  #tcbenumerate[
    + #itempoint(1)[Résoudre $x + 7 = 12$.]
      #crep[$x = 12 - 7 = 5$.]
    + #itempoint(2)[Résoudre $3 x - 4 = 11$.]
      #crep[$3 x = 15$, donc $x = 5$.]
  ]
  // Après ce marqueur : la correction, rangée en fin de document.
  #exocorrection
  + $x + 7 = 12$ donne $x = 12 - 7$, soit $x = 5$.
  + $3 x - 4 = 11$ donne $3 x = 15$, puis $x = 15 / 3 = 5$.
]

// Un exercice d'évaluation par compétences : grille de maîtrise dans l'en-tête.
#exo-eval(tags: "Raisonner")[Mettre en équation][
  #itempoint(2)[Le triple d'un nombre, augmenté de $4$, vaut $19$. Quel est ce nombre ?]
  #crep[$3 x + 4 = 19$, donc $x = 5$.]
  #exocorrection
  On note $x$ le nombre : $3 x + 4 = 19$, donc $3 x = 15$ et $x = 5$.
]

// Les corrigés, en version professeur seulement.
#ifcorrection[#rdexocorrection(0)]</code></pre>
        <img src="/images/tutorials/typst/ty-07-exo.png" alt="Rendu prof et élève : bandeau d'évaluation, note sur 5 calculée, exercice 1 sur 3 points avec boîtes 1 pt et 2 pts, exercice 2 avec grille de compétences, solutions regroupées chez le professeur seulement" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>À observer :</p>
        <ul>
          <li>« / 5 » en tête et « / 3 », « / 2 » dans les bandeaux : tout est calculé à partir des <code>itempoint</code> ;</li>
          <li>la correction de la liste (<code>+ …</code> après <code>#exocorrection</code>) reprend les mêmes pastilles ;</li>
          <li>les solutions n'existent que dans la version professeur ;</li>
          <li>chez l'élève, la place de chaque réponse est identique : on peut projeter le corrigé sur la copie.</li>
        </ul>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Complétez l'exercice : un titre, une zone de réponse avec le résultat, puis une correction rédigée, affichée en fin de document dans la version professeur.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "6e", theme: [Aires], type-document: "exercices")

#exo(level: 1)[
  Calculer l'aire d'un triangle rectangle dont les côtés de l'angle droit mesurent $6$ cm et $4$ cm.
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "6e", theme: [Aires], type-document: "exercices")

#exo(level: 1)[Aire d'un triangle rectangle][
  Calculer l'aire d'un triangle rectangle dont les côtés de l'angle droit mesurent $6$ cm et $4$ cm.
  #crep(extra-lines: 1)[$cal(A) = (6 times 4) / 2 = 12$ cm².]
  #exocorrection
  Le triangle est la moitié d'un rectangle de $6$ cm sur $4$ cm :
  $cal(A) = (6 times 4) / 2 = 24 / 2 = 12$ cm².
]

#ifcorrection[#rdexocorrection(0)]</code></pre><p><code>$cal(A)$</code> écrit le 𝒜 calligraphique de l'aire. Compilez en version élève : ni la réponse ni la correction n'apparaissent.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Ajoutez un barème : 1 point, 1 point et 2 points. Les boîtes doivent être visibles, le total de l'exercice dans son bandeau, et le total du sujet écrit en tête.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Nombres relatifs], type-document: "evaluation")

#exo(level: 1)[Additions][
  #tcbenumerate[
    + Calculer $-5 + 8$.
      #crep[$3$]
    + Calculer $-4 + (-6)$.
      #crep[$-10$]
    + Calculer $-3 + 7 + (-9)$.
      #crep[$-3 + 7 = 4$, puis $4 + (-9) = -5$.]
  ]
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Nombres relatifs], type-document: "evaluation")

#setrdexo(display-score: true)
#displayitempoints(true)

Total du sujet : #getsavedtotalpoints() points.

#exo(level: 1)[Additions][
  #tcbenumerate[
    + #itempoint(1)[Calculer $-5 + 8$.]
      #crep[$3$]
    + #itempoint(1)[Calculer $-4 + (-6)$.]
      #crep[$-10$]
    + #itempoint(2)[Calculer $-3 + 7 + (-9)$.]
      #crep[$-3 + 7 = 4$, puis $4 + (-9) = -5$.]
  ]
]</code></pre><p>Changez un <code>itempoint(2)</code> en <code>itempoint(3)</code> : le bandeau et le total du sujet se mettent à jour seuls.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Donnez deux et trois étoiles aux exercices, une étiquette de compétence à chacun, puis regroupez les corrigés dans une partie « Solutions », sur une nouvelle page, en version professeur seulement.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "2nde", theme: [Fonctions], type-document: "exercices")

#exo[Image d'un nombre][
  Soit $f(x) = x^2 - 3$. Calculer $f(4)$.
  #exocorrection
  $f(4) = 4^2 - 3 = 16 - 3 = 13$.
]

#exo[Antécédents][
  Soit $f(x) = x^2 - 3$. Déterminer les antécédents de $6$ par $f$.
  #exocorrection
  $x^2 - 3 = 6$ donne $x^2 = 9$, donc $x = -3$ ou $x = 3$.
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "2nde", theme: [Fonctions], type-document: "exercices")

#exo(level: 2, tags: "Calculer")[Image d'un nombre][
  Soit $f(x) = x^2 - 3$. Calculer $f(4)$.
  #exocorrection
  $f(4) = 4^2 - 3 = 16 - 3 = 13$.
]

#exo(level: 3, tags: "Raisonner")[Antécédents][
  Soit $f(x) = x^2 - 3$. Déterminer les antécédents de $6$ par $f$.
  #exocorrection
  $x^2 - 3 = 6$ donne $x^2 = 9$, donc $x = -3$ ou $x = 3$.
]

// Une partie « Solutions », en version professeur seulement, sur une nouvelle page.
#ifcorrection[
  #pagebreak()
  = Solutions
  #rdexocorrection(0)
]</code></pre><p>Tout ce qui est dans <code>#ifcorrection[…]</code>, y compris le saut de page et le titre, disparaît de la version élève.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '25 min',
    tags: ['typst', 'farfadet-exo', 'evaluation', 'bareme', 'competences'],
  },
  'ty-crep': {
    id: 'ty-crep',
    title: 'Zones de réponse et lignes Seyès',
    description: 'farfadet-crep : crep, trous dans une phrase, lignes Seyès, cases à cocher, et ce que voit l\'élève',
    parcours: 'typst',
    order: 7,
    sections: {
      info: `
        <h3>La règle d'or : le contenu d'une crep est la réponse</h3>
        <p>
          Version professeur : la réponse en couleur (rose par défaut). Version élève : la même place, vide.
          L'énoncé s'écrit donc <strong>avant</strong> la zone, jamais dedans.
        </p>
        <h3>Les zones en bloc</h3>
        <ul>
          <li><code>#crep[réponse]</code> : des lignes Seyès sous la question, autant que la réponse rédigée en occupe ;</li>
          <li><code>extra-lines: 2</code> ajoute deux lignes vides sous la réponse ; <code>\\</code> dans la réponse passe à la ligne : rédigez-la sur autant de lignes que l'élève en aura besoin ;</li>
          <li><code>lines: 4</code> : quatre lignes, même sans réponse rédigée ; <code>height: 3cm</code> impose une hauteur ;</li>
          <li><code>seyes: false</code> : un cadre gris au lieu des lignes ; <code>#setrdcrep(seyes: …)</code> le règle pour tout le document ;</li>
          <li><code>#seyesrep[réponse][énoncé]</code> : énoncé et lignes dans un même cadre arrondi.</li>
        </ul>
        <h3>Les trous dans une phrase</h3>
        <table>
          <tr><th>Commande</th><th>Effet</th></tr>
          <tr><td><code>#tccrep(2cm)[…]</code></td><td>trou de largeur fixe ; <code>#tccrep(auto)[…]</code> : largeur de la réponse</td></tr>
          <tr><td><code>#repsim[…]</code></td><td>petit trou de 1,5 cm</td></tr>
          <tr><td><code>#tcfillcrep[…]</code></td><td>trou jusqu'au bout de la ligne ; vide (<code>#tcfillcrep[]</code>) : des pointillés</td></tr>
          <tr><td><code>$#tcfraccrep[2][6]$</code></td><td>fraction à trous</td></tr>
          <tr><td><code>#correction-box[…]</code></td><td>réponse en couleur sans cadre, place invisible chez l'élève</td></tr>
        </table>
        <h3>Les cases à cocher</h3>
        <ul>
          <li><code>#checkbox()</code>, <code>#cb()</code> : une case ; <code>checked-corr: true</code> la coche dans la version professeur seulement ;</li>
          <li><code>#tccheckboxlist(columns: 2, checked-corr: (1, 3))[A][B][C][D]</code> : une liste de propositions, les numéros donnés cochés chez le professeur.</li>
        </ul>
        <h3>Ce que voit l'élève</h3>
        <p>
          Avant de distribuer, ouvrez toujours <code>…-eleve.pdf</code> : une réponse écrite hors d'une zone (dans l'énoncé,
          dans un <code>#ifcorrection</code> mal placé) y serait visible. Deux pièges : pas de fraction de grande taille
          (<code>display</code>) dans une zone Seyès, elle déborde de l'interligne ; et une question séparée de sa zone par un
          saut de page se règle par <code>#needspace(7cm)</code> juste avant.
        </p>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
          </div>
        </div>`,
      exemple: `
        <h3>Une fiche à trous de 5e</h3>
        <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Fractions], type-document: "fiche")

// 1. Une zone de réponse sous la question : la réponse rédigée + 1 ligne vide.
Simplifier $12/18$.
#crep(extra-lines: 1)[$12/18 = (6 times 2)/(6 times 3) = 2/3$.]

// 2. Des trous dans la phrase.
Le double de $7$ est #tccrep(1.5cm)[$14$] et la moitié de $9$ est #repsim[$4","5$].

// 3. Un trou jusqu'au bout de la ligne, et une fraction à trous.
Un quart de $20$, c'est : #tcfillcrep[$20 div 4 = 5$]

$1/3 = #tcfraccrep[2][6]$

// 4. Énoncé et lignes Seyès dans un même cadre.
#seyesrep[$3/10 = 0","3$][Écrire $3/10$ en écriture décimale.]

// 5. Cases à cocher : les cases 1 et 2 sont cochées dans la version professeur.
Quelles fractions sont égales à $1/2$ ?
#tccheckboxlist(columns: 3, checked-corr: (1, 2))[$2/4$][$5/10$][$3/5$]</code></pre>
        <img src="/images/tutorials/typst/ty-08-crep.png" alt="Rendu prof et élève : réponses roses sur lignes Seyès, trous dans les phrases, fraction à trous, cadre Seyès avec énoncé, cases cochées chez le professeur et vides chez l'élève" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>
          Chaque zone garde exactement sa hauteur d'une version à l'autre : la mise en page de la version élève
          est celle du corrigé. On peut donc projeter le corrigé par-dessus la fiche distribuée.
        </p>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Remplacez chaque « … » par un trou : 2 cm pour le premier, 2,5 cm pour le deuxième, jusqu'au bout de la ligne pour le dernier.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "6e", theme: [Le cercle], type-document: "fiche")

Le cercle de centre $O$ et de rayon $3$ cm est l'ensemble des points situés à ... du point $O$.

Un segment qui joint deux points du cercle en passant par $O$ est un ...

Sa longueur vaut le double du rayon : ...</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "6e", theme: [Le cercle], type-document: "fiche")

Le cercle de centre $O$ et de rayon $3$ cm est l'ensemble des points situés à #tccrep(2cm)[$3$ cm] du point $O$.

Un segment qui joint deux points du cercle en passant par $O$ est un #tccrep(2.5cm)[diamètre].

Sa longueur vaut le double du rayon : #tcfillcrep[$2 times 3 = 6$ cm.]</code></pre>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Sous la première question, une zone avec la réponse rédigée sur deux lignes et une ligne vide en plus. Sous la seconde, quatre lignes vides, sans réponse rédigée.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Statistiques], type-document: "fiche")

Calculer la moyenne de la série $12$ ; $15$ ; $9$.

Expliquer en une phrase ce que représente la moyenne.</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "3e", theme: [Statistiques], type-document: "fiche")

Calculer la moyenne de la série $12$ ; $15$ ; $9$.
// La réponse rédigée sur deux lignes, plus une ligne vide pour l'élève.
#crep(extra-lines: 1)[$(12 + 15 + 9) div 3 = 36 div 3$ \\ $= 12$.]

Expliquer en une phrase ce que représente la moyenne.
// Aucune réponse rédigée : quatre lignes Seyès vides, dans les deux versions.
#crep(lines: 4)[]</code></pre><p>Le <code>\\</code> coupe la réponse en deux lignes : l'élève aura la même place que la rédaction modèle.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Transformez la liste en cases à cocher sur deux colonnes (les triangles 1 et 3 existent), et « oui / non » en deux cases dont « oui » est cochée chez le professeur.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Triangles], type-document: "fiche")

Quels triangles existent ?
- 3 cm, 4 cm, 5 cm
- 2 cm, 3 cm, 6 cm
- 5 cm, 5 cm, 5 cm
- 1 cm, 1 cm, 3 cm

Le triangle de côtés 3 cm, 4 cm et 5 cm est-il rectangle ? oui / non</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "5e", theme: [Triangles], type-document: "fiche")

Quels triangles existent ?
#tccheckboxlist(columns: 2, checked-corr: (1, 3))[3 cm, 4 cm, 5 cm][2 cm, 3 cm, 6 cm][5 cm, 5 cm, 5 cm][1 cm, 1 cm, 3 cm]

Le triangle de côtés 3 cm, 4 cm et 5 cm est-il rectangle ?
#checkbox(checked-corr: true) oui #h(2em) #checkbox() non</code></pre><p>Inégalité triangulaire : 2 + 3 &lt; 6 et 1 + 1 &lt; 3, les triangles 2 et 4 n'existent pas.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '20 min',
    tags: ['typst', 'farfadet-crep', 'seyes', 'zones-de-reponse'],
  },
  'ty-qcm': {
    id: 'ty-qcm',
    title: 'QCM et vrai-faux',
    description: 'farfadet-qcm : questionnaires à choix multiples, formats, plusieurs bonnes réponses, vrai-faux avec justification',
    parcours: 'typst',
    order: 8,
    sections: {
      info: `
        <h3>Un QCM</h3>
        <pre><code>#mcq[
  #mcq-quest(br: 2)[Question][réponse 1][réponse 2][réponse 3]
]</code></pre>
        <ul>
          <li><code>br</code> donne la bonne réponse (son numéro), ou plusieurs : <code>br: (1, 3)</code> ;</li>
          <li>la version professeur met les bonnes réponses en valeur, la version élève ne coche rien ;</li>
          <li>autant de <code>#mcq-quest</code> que de questions dans un même <code>#mcq</code>.</li>
        </ul>
        <h4>Les réglages de mcq</h4>
        <ul>
          <li><code>style</code> : le format. <code>"Troyes"</code> (question à gauche, réponses côte à côte, bonne réponse sur fond rouge), <code>"BFCours"</code>, et aussi <code>"default"</code>, <code>"Tokyo"</code>, <code>"Boston"</code>, <code>"Miami"</code>, <code>"Reims"</code>, <code>"Millau"</code>, <code>"Melun"</code>, <code>"Paris"</code> ;</li>
          <li><code>orientation: "vertical"</code> : réponses en colonne ;</li>
          <li><code>question-width: 7cm</code> : largeur de la colonne des questions ;</li>
          <li><code>resume: true</code> : la numérotation continue celle du QCM précédent.</li>
        </ul>
        <p>Le format par défaut ne marque la bonne réponse qu'en gras, ce qui ne se voit pas sur une formule : préférez <code>"Troyes"</code> ou <code>"BFCours"</code>.</p>

        <h3>Un vrai-faux</h3>
        <pre><code>#vrai-faux(
  lignes-justification: 1,
  affirmation(vrai: true, justification: […], points: 1)[L'affirmation.],
  affirmation(vrai: false)[Une autre.],
)</code></pre>
        <ul>
          <li><code>vrai</code> : la bonne colonne, cochée chez le professeur ;</li>
          <li><code>justification</code> : affichée en couleur chez le professeur seulement ;</li>
          <li><code>lignes-justification</code> : la place laissée à l'élève pour justifier ;</li>
          <li><code>points</code> alimente le score de l'exercice, comme <code>itempoint</code> ;</li>
          <li>autres clés : <code>cases: "rond"</code>, <code>colonnes: 2</code>, <code>libelles: ([Oui], [Non])</code>, <code>melanger: true</code> (même ordre dans les deux versions).</li>
        </ul>
        <p>Pour rédiger les distracteurs à partir des erreurs réelles des élèves, le skill <strong>qcm-creator</strong> peut aider (côté LaTeX).</p>

        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet" target="_blank" rel="noopener noreferrer" class="doc-link">Dépôt farfadet (Forge)</a>
            <a href="https://forge.apps.education.fr/romaindeschamps/farfadet/-/blob/main/farfadet-documentation.pdf" target="_blank" rel="noopener noreferrer" class="doc-link">Documentation complète (PDF)</a>
          </div>
        </div>`,
      exemple: `
        <h3>Automatismes de 1re</h3>
        <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "1re", theme: [Automatismes], type-document: "exercices")

#exo(level: 1)[QCM][
  Pour chaque question, cocher la ou les bonnes réponses.

  // br = numéro de la bonne réponse ; puis [question][réponse 1][réponse 2]…
  #mcq(style: "Troyes", question-width: 7cm)[
    #mcq-quest(br: 2)[15~% de $80$ vaut :][$8$][$12$][$15$]
    #mcq-quest(br: 3)[Le prix passe de $50$ € à $60$ €. Il a augmenté de :][10~%][12~%][20~%]
  ]

  // Réponses en colonne ; la numérotation continue (resume) ; deux bonnes réponses.
  #mcq(style: "BFCours", orientation: "vertical", question-width: 8cm, resume: true)[
    #mcq-quest(br: (1, 3))[Quelles écritures valent $0","25$ ?][$1/4$][$2/5$][25~%]
  ]
]

#exo(level: 2)[Vrai ou faux][
  #vrai-faux(
    lignes-justification: 1,    // lignes pour justifier, chez l'élève
    affirmation(vrai: true, justification: [$(-3)^2 = 9$ et $3^2 = 9$.])[
      Deux nombres opposés ont le même carré.
    ],
    affirmation(vrai: false, justification: [Contre-exemple : $0","5^2 = 0","25$.])[
      Le carré d'un nombre est toujours plus grand que ce nombre.
    ],
  )
]</code></pre>
        <img src="/images/tutorials/typst/ty-09-qcm.png" alt="Rendu prof et élève : QCM format Troyes avec bonnes réponses surlignées chez le professeur, QCM vertical avec deux cases cochées, tableau vrai-faux avec justifications roses chez le professeur et cases vides chez l'élève" loading="lazy" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; background: #fff;" />
        <p>
          La troisième question a deux bonnes réponses : deux cases cochées. La numérotation continue de 2 à 3
          grâce à <code>resume: true</code>, bien que le format change.
        </p>
`,
      pratique: `<p><em>À faire dans VS Code (extension Tinymist, aperçu au Ctrl+S) ou dans l'application Écriture Typst.</em></p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Transformez ces trois questions en QCM au format Troyes, dans un exercice. Les bonnes réponses sont indiquées en commentaire.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "2nde", theme: [Automatismes], type-document: "exercices")

// Bonnes réponses : 1, puis 3, puis 2.
+ $2^3 times 2^2$ est égal à : $2^5$ ; $2^6$ ; $4^5$.
+ L'inverse de $4$ est : $-4$ ; $0","4$ ; $0","25$.
+ Une hausse de 10~% puis une baisse de 10~% donnent : une stabilité ; une baisse de 1~% ; une hausse de 1~%.</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "2nde", theme: [Automatismes], type-document: "exercices")

#exo(level: 1)[Questions flash][
  #mcq(style: "Troyes", question-width: 7cm)[
    #mcq-quest(br: 1)[$2^3 times 2^2$ est égal à :][$2^5$][$2^6$][$4^5$]
    #mcq-quest(br: 3)[L'inverse de $4$ est :][$-4$][$0","4$][$0","25$]
    #mcq-quest(br: 2)[Une hausse de 10~% puis une baisse de 10~% donnent :][une stabilité][une baisse de 1~%][une hausse de 1~%]
  ]
]</code></pre>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Faites de ces trois affirmations un vrai-faux noté sur 3 (un point par affirmation), avec la justification côté professeur et une ligne de justification côté élève. Affichez le score dans le bandeau.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Puissances], type-document: "evaluation")

// Faux : 2^3 = 8 et 3^2 = 9. Vrai : par convention. Faux : (-2)^2 = 4.
- $2^3 = 3^2$.
- $10^0 = 1$.
- Le carré d'un nombre négatif est négatif.</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "4e", theme: [Puissances], type-document: "evaluation")

#setrdexo(display-score: true)

#exo(level: 2)[Vrai ou faux][
  Cocher Vrai ou Faux, puis justifier.
  #vrai-faux(
    lignes-justification: 1,
    affirmation(vrai: false, points: 1, justification: [$2^3 = 8$ et $3^2 = 9$.])[$2^3 = 3^2$.],
    affirmation(vrai: true, points: 1, justification: [$10^0 = 1$ par convention.])[$10^0 = 1$.],
    affirmation(vrai: false, points: 1, justification: [$(-2)^2 = 4$, positif.])[Le carré d'un nombre négatif est négatif.],
  )
]</code></pre>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Ajoutez la question en commentaire comme un QCM vertical à deux bonnes réponses, dont la numérotation continue celle du premier QCM.</p>
            <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "1re", theme: [Second degré], type-document: "exercices")

#exo(level: 2)[QCM en deux temps][
  #mcq(style: "Troyes", question-width: 7cm)[
    #mcq-quest(br: 2)[Le discriminant de $x^2 - 4 x + 4$ vaut :][$4$][$0$][$-8$]
  ]
  Plus difficile : plusieurs réponses peuvent être justes.
  // Quelles fonctions s'annulent en x = 2 ? (x - 2)(x + 1) ; x^2 - 4 ; x^2 + 4
]</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>#import "@preview/farfadet:0.2.0": *
#show: modele("cours", niveau: "1re", theme: [Second degré], type-document: "exercices")

#exo(level: 2)[QCM en deux temps][
  #mcq(style: "Troyes", question-width: 7cm)[
    #mcq-quest(br: 2)[Le discriminant de $x^2 - 4 x + 4$ vaut :][$4$][$0$][$-8$]
  ]
  Plus difficile : plusieurs réponses peuvent être justes.
  #mcq(style: "BFCours", orientation: "vertical", question-width: 8cm, resume: true)[
    #mcq-quest(br: (1, 2))[Quelles fonctions s'annulent en $x = 2$ ?][$(x - 2)(x + 1)$][$x^2 - 4$][$x^2 + 4$]
  ]
]</code></pre><p>(x − 2)(x + 1) et x² − 4 s'annulent en 2 ; x² + 4 ne s'annule jamais. Le second QCM porte le numéro 2.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '15 min',
    tags: ['typst', 'farfadet-qcm', 'qcm', 'vrai-faux'],
  },
}
