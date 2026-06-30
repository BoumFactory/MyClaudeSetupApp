// =====================================================================
// bfd-html.js — Post-substitution LaTeX -> HTML (POC v0.4 2026-05-16)
// =====================================================================
// S'exécute APRÈS DOMContentLoaded, AVANT MathJax (qui démarre async).
// Modifie innerHTML des conteneurs .bfd-body et des titres pour
// transformer le source LaTeX brut écrit par bfd-html.sty en HTML lisible.
//
// Ordre d'application :
//   1. Préservation des zones math ($...$, $$...$$, \(...\), \[...\])
//      => remplacées par des placeholders MATHnn
//   2. Substitutions accents LaTeX (\'e -> é, etc.) sur le reste
//   3. Conversion environnements (MultiColonnes, tcbenumerate, crep, center)
//   4. Conversion commandes inline (\acc, \encadrer, \tcfillcrep, \repsim, ...)
//   5. Restauration des zones math (les placeholders sont remis en place)
//   6. MathJax rend les zones math (handled by the loaded mathjax script)
// =====================================================================

(function () {
  // -------------------------------------------------------------------
  // Config MathJax v3
  // -------------------------------------------------------------------
  window.MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']],
      processEscapes: true,
      packages: { '[+]': ['ams', 'cancel', 'color', 'newcommand', 'configmacros'] },
      macros: {
        // Ensembles de nombres
        R: '\\mathbb{R}',
        N: '\\mathbb{N}',
        Z: '\\mathbb{Z}',
        Q: '\\mathbb{Q}',
        C: '\\mathbb{C}',
        // Constantes bfcours
        bfe: 'e',
        // Commandes pédagogiques (utilisées EN MODE MATH par les cours)
        Donc: '\\Longrightarrow',
        iere: ['{}^{\\text{re}}', 0],
        // \tcfillcrep et \repsim en mode math : juste contenu coloré rouge (inline).
        // Pas de \boxed, car en HTML le PDF "autofill" ne se reproduit pas et boxed
        // créerait une bordure parasite dans la formule.
        tcfillcrep: ['{\\color{red}#1}', 1],
        // \repsim[size]{contenu} : MathJax macro avec arg optionnel
        // (la taille [size] est ignorée en mode math : juste le contenu coloré)
        repsim: ['{\\color{red}#2}', 2, ''],
        acc: ['{\\color{orange}#1}', 1],
        encadrer: ['\\boxed{#1}', 1],
        // \hfill, \hspace, \vspace en mode math : MathJax ne les supporte pas
        // nativement, on les neutralise pour éviter l'erreur "Unsupported use".
        hfill: '\\quad',
        // \phantom : NE PAS redéfinir — MathJax v3 le gère nativement et
        // toute redéfinition crée une récursion infinie (max macro substitution).
      }
    },
    loader: { load: ['[tex]/ams', '[tex]/cancel', '[tex]/color', '[tex]/newcommand', '[tex]/configmacros'] },
    options: { renderActions: { addMenu: [] } }
  };

  // -------------------------------------------------------------------
  // 1. Préservation des zones math
  // -------------------------------------------------------------------
  // On extrait $...$, $$...$$, \(...\), \[...\], \begin{align*}...\end{align*}
  // et on les remplace par des marqueurs MATHnn pour qu'aucune substitution
  // texte ne les altère. On les remet à la fin.
  function protectMath(html) {
    var slots = [];
    function stash(match) {
      var idx = slots.length;
      slots.push(match);
      return 'MATHSLOT' + idx + 'END';
    }
    // Ordre : display math d'abord ($$, \[, align*) puis inline ($, \()
    html = html.replace(/\\begin\s*\{align\*?\}[\s\S]*?\\end\s*\{align\*?\}/g, stash);
    html = html.replace(/\\begin\s*\{(?:equation|gather|cases)\*?\}[\s\S]*?\\end\s*\{(?:equation|gather|cases)\*?\}/g, stash);
    html = html.replace(/\$\$[\s\S]*?\$\$/g, stash);
    html = html.replace(/\\\[[\s\S]*?\\\]/g, stash);
    html = html.replace(/\\\([\s\S]*?\\\)/g, stash);
    // $...$ (sans matcher $$) : pattern non-greedy
    html = html.replace(/\$(?:[^$\\]|\\.)+?\$/g, stash);
    return { html: html, slots: slots };
  }
  function restoreMath(html, slots) {
    return html.replace(/MATHSLOT(\d+)END/g, function (_, i) {
      return slots[parseInt(i, 10)];
    });
  }

  // -------------------------------------------------------------------
  // 2. Substitutions accents LaTeX -> UTF-8
  // -------------------------------------------------------------------
  // \detokenize laisse un espace entre la commande et son arg :
  //   \'e          -> "\'e"          (avec ou sans espace)
  //   \'{e}        -> "\' {e}"
  //   \c{c}        -> "\c {c}"
  //   \oe          -> "\oe " ou "\oe {}"
  //
  // Table exhaustive : accents aigus, graves, circonflexes, trémas
  // sur a/e/i/o/u/y minuscules et majuscules + ç, œ, æ, ß.
  var ACCENT_TABLE = {
    "'": { a: 'á', e: 'é', i: 'í', o: 'ó', u: 'ú', y: 'ý',
           A: 'Á', E: 'É', I: 'Í', O: 'Ó', U: 'Ú', Y: 'Ý' },
    '`': { a: 'à', e: 'è', i: 'ì', o: 'ò', u: 'ù',
           A: 'À', E: 'È', I: 'Ì', O: 'Ò', U: 'Ù' },
    '^': { a: 'â', e: 'ê', i: 'î', o: 'ô', u: 'û',
           A: 'Â', E: 'Ê', I: 'Î', O: 'Ô', U: 'Û' },
    '"': { a: 'ä', e: 'ë', i: 'ï', o: 'ö', u: 'ü', y: 'ÿ',
           A: 'Ä', E: 'Ë', I: 'Ï', O: 'Ö', U: 'Ü', Y: 'Ÿ' }
  };

  function substituteAccents(html) {
    // \'e, \'E, \`a, \^o, \"u, etc. (avec ou sans accolades, avec ou sans espace)
    // Pattern : \ACCENT[espace]?{?LETTRE}?
    html = html.replace(/\\(['`^"])\s*\{?\s*([aeiouyAEIOUY])\s*\}?/g, function (m, acc, ltr) {
      var sub = ACCENT_TABLE[acc] && ACCENT_TABLE[acc][ltr];
      return sub || m;
    });
    // \c{c} -> ç, \c{C} -> Ç
    html = html.replace(/\\c\s*\{?\s*([cC])\s*\}?/g, function (m, ltr) {
      return ltr === 'c' ? 'ç' : 'Ç';
    });
    // \oe, \OE, \ae, \AE, \ss (avec ou sans {} ou espace final)
    html = html.replace(/\\oe\s*\{?\s*\}?/g, 'œ');
    html = html.replace(/\\OE\s*\{?\s*\}?/g, 'Œ');
    html = html.replace(/\\ae\s*\{?\s*\}?/g, 'æ');
    html = html.replace(/\\AE\s*\{?\s*\}?/g, 'Æ');
    html = html.replace(/\\ss\s*\{?\s*\}?/g, 'ß');
    // \~n -> ñ, \~N -> Ñ
    html = html.replace(/\\~\s*\{?\s*([nN])\s*\}?/g, function (m, l) {
      return l === 'n' ? 'ñ' : 'Ñ';
    });
    return html;
  }

  // -------------------------------------------------------------------
  // 3. Conversion environnements (block-level)
  // -------------------------------------------------------------------
  // Note : ordre important. On traite d'abord tcbenumerate (qui peut être
  // imbriqué dans MultiColonnes) pour que ses \tcbitem soient consommés
  // avant que MultiColonnes ne les voie.

  function extractTitle(opt) {
    if (!opt) return '';
    var m = opt.match(/title\s*=\s*\{([^}]*)\}/);
    return m ? m[1] : '';
  }
  function hasRasterFull(opt) {
    return opt && /raster\s+multicolumn/.test(opt);
  }

  // Découpe le contenu d'un env sur \tcbitem (avec opt optionnel).
  // Retourne une liste d'objets { opt, content }.
  function splitOnTcbitem(inner) {
    var parts = inner.split(/\\tcbitem\s*(?:\[([^\]]*)\])?/);
    var items = [];
    for (var i = 1; i < parts.length; i += 2) {
      items.push({ opt: parts[i] || '', content: parts[i + 1] || '' });
    }
    return items;
  }

  function convertTcbenumerate(html) {
    return html.replace(
      /\\begin\s*\{tcbenumerate\}(?:\s*\[(\d+)\])?([\s\S]*?)\\end\s*\{tcbenumerate\}/g,
      function (m, cols, inner) {
        var items = splitOnTcbitem(inner);
        var n = cols || '1';
        var out = '<ol class="bfd-enum" data-cols="' + n + '">';
        items.forEach(function (it) {
          var cls = 'bfd-item';
          if (hasRasterFull(it.opt)) cls += ' bfd-item-full';
          var title = extractTitle(it.opt);
          var head = title ? '<strong class="bfd-item-title">' + title + '</strong> ' : '';
          out += '<li class="' + cls + '">' + head + it.content.trim() + '</li>';
        });
        out += '</ol>';
        return out;
      }
    );
  }

  function convertMultiColonnes(html) {
    return html.replace(
      /\\begin\s*\{MultiColonnes\}\s*\{(\d+)\}([\s\S]*?)\\end\s*\{MultiColonnes\}/g,
      function (m, cols, inner) {
        var items = splitOnTcbitem(inner);
        var out = '<div class="bfd-cols" data-cols="' + cols + '">';
        items.forEach(function (it) {
          var cls = 'bfd-col';
          if (hasRasterFull(it.opt)) cls += ' bfd-col-full';
          var title = extractTitle(it.opt);
          var head = title ? '<div class="bfd-col-title">' + title + '</div>' : '';
          out += '<div class="' + cls + '">' + head + it.content.trim() + '</div>';
        });
        out += '</div>';
        return out;
      }
    );
  }

  // crep : zone réponse élève. En HTML, on l'expose comme bloc visible
  // avec un toggle "Correction" (l'élève peut comparer).
  function convertCrep(html) {
    return html.replace(
      /\\begin\s*\{crep\}([\s\S]*?)\\end\s*\{crep\}/g,
      function (m, inner) {
        return '<details class="bfd-crep" open><summary>Correction</summary>' +
               '<div class="bfd-crep-body">' + inner.trim() + '</div></details>';
      }
    );
  }

  function convertRemarque(html) {
    return html.replace(
      /\\begin\s*\{Remarque\}([\s\S]*?)\\end\s*\{Remarque\}/g,
      function (m, inner) {
        return '<aside class="bfd-remarque-inline"><span class="bfd-remarque-lbl">Remarque</span> ' +
               inner.trim() + '</aside>';
      }
    );
  }

  function convertCenter(html) {
    return html.replace(
      /\\begin\s*\{center\}([\s\S]*?)\\end\s*\{center\}/g,
      '<div class="bfd-center">$1</div>'
    );
  }

  function convertItemize(html) {
    return html.replace(
      /\\begin\s*\{itemize\}([\s\S]*?)\\end\s*\{itemize\}/g,
      function (m, inner) {
        var parts = inner.split(/\\item\s*/).filter(function (s) { return s.trim() !== ''; });
        return '<ul class="bfd-list">' +
               parts.map(function (p) { return '<li>' + p.trim() + '</li>'; }).join('') +
               '</ul>';
      }
    );
  }

  function convertEnumerate(html) {
    return html.replace(
      /\\begin\s*\{enumerate\}([\s\S]*?)\\end\s*\{enumerate\}/g,
      function (m, inner) {
        var parts = inner.split(/\\item\s*/).filter(function (s) { return s.trim() !== ''; });
        return '<ol class="bfd-list">' +
               parts.map(function (p) { return '<li>' + p.trim() + '</li>'; }).join('') +
               '</ol>';
      }
    );
  }

  // -------------------------------------------------------------------
  // 4. Conversion commandes inline (post-blocks)
  // -------------------------------------------------------------------
  // Helper : remplace \cmd[opt]{X} ou \cmd{X} par un wrapper HTML
  // Supporte 1 niveau d'imbrication d'accolades dans l'argument.
  function repCmd(html, name, openTag, closeTag) {
    var inner = '([^{}]*(?:\\{[^{}]*\\}[^{}]*)*)';
    var reOpt = new RegExp('\\\\' + name + '\\s*\\[([^\\]]*)\\]\\s*\\{' + inner + '\\}', 'g');
    html = html.replace(reOpt, openTag + '$2' + closeTag);
    var re = new RegExp('\\\\' + name + '\\s*\\{' + inner + '\\}', 'g');
    html = html.replace(re, openTag + '$1' + closeTag);
    return html;
  }

  function substituteInlineCommands(html) {
    // Commandes de mise en valeur
    html = repCmd(html, 'voc', '<span class="bfd-voc">', '</span>');
    html = repCmd(html, 'emph', '<em>', '</em>');
    html = repCmd(html, 'textbf', '<strong>', '</strong>');
    html = repCmd(html, 'textit', '<em>', '</em>');
    html = repCmd(html, 'underline', '<u>', '</u>');
    html = repCmd(html, 'liencontent', '<span class="bfd-lien">', '</span>');

    // \acc{X} : accentuation pédagogique bfcours
    html = repCmd(html, 'acc', '<mark class="bfd-acc">', '</mark>');

    // \encadrer{X} ou \encadrer[style]{X}
    html = repCmd(html, 'encadrer', '<span class="bfd-boxed">', '</span>');

    // \tcfillcrep{X} : correction qui REMPLIT la ligne / l'espace dispo
    // (block-level full-width, contrairement à \repsim qui est inline)
    html = repCmd(html, 'tcfillcrep', '<span class="bfd-corr-autofill">', '</span>');

    // \repsim[size]{X} : zone réponse INLINE avec taille de boîte en cm/em/pt.
    // size devient min-width inline pour reproduire la taille fixe du PDF.
    html = html.replace(
      /\\repsim\s*\[([^\]]*)\]\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}/g,
      function (m, size, content) {
        var safeSize = size.trim().replace(/[^0-9.\-+a-zA-Z]/g, '');
        var style = safeSize ? ' style="min-width:' + safeSize + '"' : '';
        return '<span class="bfd-corr-fill"' + style + '>' + content + '</span>';
      }
    );
    html = repCmd(html, 'repsim', '<span class="bfd-corr-fill">', '</span>');

    // \phantom{X} : espace de la largeur d'un X (rendu visuel : invisible)
    html = repCmd(html, 'phantom', '<span class="bfd-phantom">', '</span>');

    // Commandes sans argument
    html = html.replace(/\\Donc(?![a-zA-Z])/g, '<span class="bfd-donc">⟹</span>');
    html = html.replace(/\\hfill(?![a-zA-Z])/g, '<span class="bfd-hfill"></span>');
    html = html.replace(/\\quad(?![a-zA-Z])/g, '&emsp;');
    html = html.replace(/\\qquad(?![a-zA-Z])/g, '&emsp;&emsp;');
    html = html.replace(/\\noindent(?![a-zA-Z])/g, '');
    html = html.replace(/\\iere\s*\{?\s*\}?/g, '<sup>re</sup>');
    html = html.replace(/\\ieme\s*\{?\s*\}?/g, '<sup>e</sup>');

    // \vspace{X} : marge verticale (positif = ajoute, négatif = remonte le suivant).
    // CSS supporte directement les unités LaTeX usuelles : cm, mm, pt, em, ex, in, px.
    html = html.replace(/\\vspace\s*\*?\s*\{([^{}]*)\}/g, function (m, val) {
      val = val.trim();
      // Si valeur invalide ou vide, supprimer
      if (!val) return '';
      // Échappement sécurité de la valeur pour éviter l'injection CSS
      val = val.replace(/[^0-9.\-+a-zA-Z]/g, '');
      return '<div class="bfd-vspace" style="margin-top:' + val + ';"></div>';
    });
    // \hspace{X} : marge horizontale (inline)
    html = html.replace(/\\hspace\s*\*?\s*\{([^{}]*)\}/g, function (m, val) {
      val = val.trim().replace(/[^0-9.\-+a-zA-Z]/g, '');
      if (!val) return '';
      return '<span class="bfd-hspace" style="margin-left:' + val + ';"></span>';
    });

    // \par : nouveau paragraphe -> saut visuel simple
    html = html.replace(/\\par(?![a-zA-Z])/g, '<br>');

    // \\ -> <br> (hors zones math protégées)
    html = html.replace(/\\\\(?![a-zA-Z])/g, '<br>');

    // Nettoyage final : accolades vides résiduelles
    html = html.replace(/\{\s*\}/g, '');

    return html;
  }

  // -------------------------------------------------------------------
  // 5. Pipeline complet sur un élément
  // -------------------------------------------------------------------
  function processElement(root) {
    var protect = protectMath(root.innerHTML);
    var html = protect.html;

    // Substitutions accents (sur tout sauf math)
    html = substituteAccents(html);

    // Conversion environnements (ordre : inner-most first).
    // MultiColonnes AVANT tcbenumerate : un MultiColonnes imbrique dans un
    // tcbenumerate doit consommer ses propres \tcbitem en premier, sinon
    // le tcbenumerate capture aussi les \tcbitem internes.
    html = convertCrep(html);
    html = convertRemarque(html);
    html = convertCenter(html);
    html = convertItemize(html);
    html = convertEnumerate(html);
    html = convertMultiColonnes(html);
    html = convertTcbenumerate(html);

    // Substitutions commandes inline
    html = substituteInlineCommands(html);

    // Restauration math
    html = restoreMath(html, protect.slots);

    root.innerHTML = html;
  }

  // -------------------------------------------------------------------
  // 6. Application au DOM
  // -------------------------------------------------------------------
  function processAll() {
    document.querySelectorAll('.bfd-body').forEach(processElement);
    document.querySelectorAll('h1, h2, h3, h4').forEach(processElement);
    document.querySelectorAll('.bfd-title').forEach(processElement);
    document.querySelectorAll('.bfd-toc-list a').forEach(processElement);
    // Force MathJax à retypeset après nos modifs (idempotent)
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
      window.MathJax.startup.promise.then(function () {
        window.MathJax.typesetPromise && window.MathJax.typesetPromise();
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', processAll);
  } else {
    processAll();
  }
})();
