/* Capsule : droites parallèles et angles alternes-internes (voix de synthèse) — moteur canvas.
   Portage de labomaths-edge (index.html + scenes.js) : mêmes contenus, même ordre, mêmes ancres. */
CAPSULE({
  titre: 'Droites parallèles et angles alternes-internes',
  audio: 'audio.wav', theme: 'nuit', ambiance: true, mention: 'Voix de synthèse',
  macros: { BAC: '\\cyan{\\widehat{BAC}}', CAI: '\\violet{\\widehat{CAI}}', BAI: '\\ambre{\\widehat{BAI}}', ABC: '\\ambre{\\widehat{ABC}}' },

  scenes: [
    /* ===== SCÈNE 1 — titre et objectif ===== */
    { id: 's-titre', gabarit: 'titre', debut: 0,
      haut: [
        { surTitre: "Correction d'exercice · Géométrie", id: 't-sur' },
        { titre: 'Droites parallèles [et angles]{.grad}', id: 't-titre', nowrap: true },
      ],
      centre: { ecart: 110, contenu: [
        { carte: { ligne: [{ icone: '🎯' }, { texte: 'Je connais et sais utiliser les relations entre droites parallèles et angles' }], ecart: 34 },
          couleur: 'vert', id: 't-obj', l: 1560, marge: [30, 44], taille: 50 },
        { id: 'decor', l: 1300, h: 330, figure: { vue: [0, 0, 1300, 330], objets: [
          { id: 'd-l1', segment: [[0, 70], [1300, 70]], couleur: 'rose', epaisseur: 9 },
          { id: 'd-l2', segment: [[0, 250], [1300, 250]], couleur: 'rose', epaisseur: 9 },
          { id: 'd-sc', segment: [[470, -10], [830, 330]], couleur: 'vert', epaisseur: 9 },
        ] } },
      ] } },

    /* ===== SCÈNE 2 — figure + panneau ===== */
    { id: 's-main', gabarit: 'figure-panneau', debut: '@b02-0.3',
      bandeau: { valign: 'centre', contenu: [{ pile: [
        { puce: 'Lire le schéma', couleur: 'cyan', id: 'q0', taille: 38, margeH: 32 },
        { puce: 'Question 1', couleur: 'rose', id: 'q1', taille: 38, margeH: 32 },
        { puce: 'Question 2', couleur: 'rose', id: 'q2', taille: 38, margeH: 32 },
        { puce: 'Rédaction', couleur: 'ambre', id: 'q3', taille: 38, margeH: 32 },
        { puce: 'À retenir', couleur: 'vert', id: 'q4', taille: 38, margeH: 32 },
      ] }] },

      // schéma à main levée : quadrilatère I, A, C, B
      figure: [{ id: 'fig', l: 960, h: 500, figure: { vue: [0, -25, 960, 500],
        points: { I: [70, 105], A: [455, 70], B: [230, 395], C: [850, 345] },
        objets: [
          { id: 'strip', bande: [['A', 'I'], ['B', 'C']], remplir: 'rose', opacite: 0.13 },
          { id: 's-cai', secteur: ['C', 'A', 'I'], r: 118, remplir: 'violet', opacite: 0.16 },
          { id: 's-bac', secteur: ['C', 'A', 'B'], r: 96, remplir: 'cyan', opacite: 0.38 },
          { id: 's-bai', secteur: ['B', 'A', 'I'], r: 96, remplir: 'ambre', opacite: 0.38 },
          { id: 's-abc', secteur: ['A', 'B', 'C'], r: 96, remplir: 'ambre', opacite: 0.38 },
          { id: 'L-ai', droite: ['A', 'I'], couleur: 'rose', epaisseur: 6 },
          { id: 'L-bc', droite: ['B', 'C'], couleur: 'rose', epaisseur: 6 },
          { id: 'ray-ab', segment: ['A', 'B'], t: [0, 1.1846], couleur: 'vert', epaisseur: 7 },
          { id: 'ext-ab', segment: ['A', 'B'], t: [0, -0.2923], couleur: 'vert', epaisseur: 7 },
          { id: 'e-ia', segment: ['I', 'A'], main: [3, -4] },
          { id: 'e-ac', segment: ['A', 'C'], main: [5, 3] },
          { id: 'e-cb', segment: ['C', 'B'], main: [-3, 5] },
          { id: 'e-bi', segment: ['B', 'I'], main: [-18, -8] },
          { id: 'e-ab', segment: ['A', 'B'], main: [4, -3] },
          { id: 'ang-droit', droit: ['C', 'A', 'B'], r: 34, couleur: 'cyan' },
          { id: 'a-cai', angle: ['C', 'A', 'I'], r: 118, couleur: 'violet', epaisseur: 6 },
          { id: 'a-abc', angle: ['A', 'B', 'C'], r: 96, couleur: 'ambre', epaisseur: 6 },
          { id: 'a-bai', angle: ['B', 'A', 'I'], r: 96, couleur: 'ambre', epaisseur: 6 },
          { id: 'lI', etiquette: 'I', en: [34, 78] }, { id: 'lA', etiquette: 'A', en: [424, 40] },
          { id: 'lB', etiquette: 'B', en: [276, 440] }, { id: 'lC', etiquette: 'C', en: [886, 374] },
          { id: 'l140', etiquette: '\\violet{140^\\circ}', en: [414, 232] },
          { id: 'l50b', etiquette: '\\ambre{50^\\circ}', en: [346, 330] },
          { id: 'lq', etiquette: '\\ambre{?}', en: [318, 150] },
          { id: 'l50a', etiquette: '\\ambre{50^\\circ}', en: [318, 150] },
          { id: 't-ai', etiquette: '\\rose{(AI)}', en: [862, 6] },
          { id: 't-bc', etiquette: '\\rose{(BC)}', en: [70, 452] },
          { id: 't-ab', etiquette: '\\vert{(AB)}', en: [590, -2] },
        ] } }],

      'sous-figure': [
        { texte: 'schéma à main levée', id: 'note', taille: 34, it: true, doux: true },
        { puce: 'Données', couleur: 'cyan', id: 'dh' },
        { ligne: [
          { carte: [{ tex: '\\BAC=\\cssId{dv1}{90^\\circ}' }, { texte: 'angle droit en A', doux: true }], couleur: 'cyan', id: 'dc1', marge: [14, 18], ecart: 4 },
          { carte: [{ tex: '\\CAI=\\cssId{dv2}{140^\\circ}' }, { texte: 'grand angle en A', doux: true }], couleur: 'violet', id: 'dc2', marge: [14, 18], ecart: 4 },
          { carte: [{ tex: '\\ABC=\\cssId{dv3}{50^\\circ}' }, { texte: 'angle en B', doux: true }], couleur: 'ambre', id: 'dc3', marge: [14, 18], ecart: 4 },
        ], ecart: 18, egal: true, taille: 34, tailleTex: 46 },
      ],

      panneau: [{ pile: [
        // b02 : pas de rapporteur
        { carte: [
          { id: 'pas-ic', l: 440, h: 264, figure: { vue: [0, 0, 300, 180], objets: [
            { chemin: 'M20 160 A130 130 0 0 1 280 160 Z', remplir: 'rgba(255,255,255,0.07)', couleur: 'doux', epaisseur: 6 },
            { chemin: 'M44 160 A106 106 0 0 1 256 160', couleur: 'doux', epaisseur: 22, pointilles: [2.5, 8.3], bout: 'butt' },
            { chemin: 'M150 160 L150 112', couleur: 'doux', epaisseur: 6, bout: 'butt' },
            { id: 'rx', chemin: 'M18 8 L284 172', couleur: 'corail', epaisseur: 18 },
          ] } },
          { texte: 'Pas de rapporteur !', id: 'pas-t1', taille: 62, gras: true, couleur: 'corail', nowrap: true },
          { texte: 'On lit les [codages]{.cyan}', id: 'pas-t2', taille: 50, gras: true, nowrap: true },
        ], couleur: 'corail', id: 'pas', alignEnfants: 'centre', ecart: 18, marge: [30, 30], margeBas: 34, dy: 50 },

        // Question 1
        { colonne: [
          { carte: "Déterminer la mesure de l'angle $\\BAI$.", couleur: 'rose', id: 'p-q1', taille: 46, marge: [22, 34] },
          { carte: { ligne: [{ tex: '\\CAI', id: 'sm1' }, { tex: '=\\BAC', id: 'sm2' }, { tex: '+\\BAI', id: 'sm3' }], ecart: 14, justifie: 'centre' },
            id: 'p-sum', marge: [14, 34], tailleTex: 60 },
          { carte: { calcul: [
            [{ tex: '\\BAI', id: 'c1l' }, { tex: '=', id: 'c1e' }, '\\cssId{c1a}{\\CAI}\\cssId{c1m}{-}\\cssId{c1b}{\\BAC}'],
            ['', { tex: '=', id: 'c2e' }, '\\cssId{r2a}{\\violet{140^\\circ}}\\cssId{r2m}{-}\\cssId{r2b}{\\cyan{90^\\circ}}'],
            ['', { tex: '=', id: 'c3e' }, { tex: '\\ambre{50^\\circ}', id: 'r3' }],
          ], colonnesL: [200, 66], hauteurLigne: 92, ecart: [12, 0] }, couleur: 'ambre', id: 'ch', marge: [22, 34], margeBas: 26, tailleTex: 64 },
          { carte: "L'angle $\\widehat{BAI}$ mesure $\\ambre{50^\\circ}$.", couleur: 'vert', id: 'p-res', taille: 50, marge: [18, 34], nowrap: true },
        ], ecart: 22 },

        // Question 2
        { colonne: [
          { carte: 'Justifier que les droites $(AI)$ et $(BC)$ sont parallèles.', couleur: 'rose', id: 'p-q2', taille: 46, marge: [22, 34] },
          { carte: '[Droites]{.tt} $(AI)$ et $(BC)$', couleur: 'rose', id: 'c-dr', taille: 44, marge: [16, 34] },
          { carte: '[Sécante]{.tt} $(AB)$', couleur: 'vert', id: 'c-sec', taille: 44, marge: [16, 34] },
          { carte: [
            { texte: '$\\ABC$ et $\\BAI$', id: 'al1', taille: 46 },
            { texte: "de part et d'autre de la sécante", id: 'al2', taille: 38 },
            { texte: 'entre les deux droites', id: 'al3', taille: 38 },
            { texte: 'alternes-internes', id: 'al4', taille: 60, gras: true, couleur: 'ambre', align: 'gauche' },
          ], couleur: 'ambre', id: 'c-alt', ecart: 6, marge: [18, 34], margeBas: 22 },
        ], ecart: 16 },

        // Rédaction en trois cartouches
        { colonne: [
          { carte: [
            { tex: '\\cssId{e1}{\\widehat{ABC}}\\cssId{e2}{=}\\cssId{e3}{\\widehat{BAI}}\\cssId{e4}{=}\\cssId{e5}{50^\\circ}', taille: 56 },
            { texte: '[$\\widehat{ABC}$]{#t1} [et]{#t2} [$\\widehat{BAI}$]{#t3} [sont des angles]{#t4} [alternes-internes]{#t5 .kw}', interligne: 1.45, tailleTex: 1.25 },
          ], titre: 'Ce que je sais :', couleur: 'cyan', id: 'k1', taille: 40, marge: [26, 32] },
          { carte: { texte: 'Si deux droites coupées par une | [sécante]{.kw} | forment deux angles | [alternes-internes]{.kw} | de même | [mesure,]{.kw} | alors ces deux droites sont | [parallèles.]{.kw}',
            decoupe: 'p', interligne: 1.5 }, titre: 'Propriété :', couleur: 'violet', id: 'k2', taille: 40, marge: [26, 32] },
          { carte: { tex: '\\cssId{z1}{(BC)}\\cssId{z2}{{}\\parallel(AI)}', id: 'k3f', taille: 66, align: 'centre' },
            titre: 'Conclusion :', couleur: 'vert', id: 'k3', marge: [26, 32], margeBas: 34 },
        ], id: 'redac', ecart: 30 },

        // À retenir
        { colonne: [
          { carte: 'Des angles [alternes-internes]{#f1a .kw} de même [mesure]{#f1b .kw} prouvent que deux droites sont [parallèles]{#f1c .kw}.',
            puce: 'À retenir', couleur: 'vert', id: 'fin1', taille: 44, interligne: 1.38, ecart: 18, marge: [28, 34] },
          { carte: { ligne: [
            { id: 'rap2', l: 190, h: 114, figure: { vue: [0, 0, 300, 180], objets: [
              { chemin: 'M20 160 A130 130 0 0 1 280 160 Z', remplir: 'rgba(255,255,255,0.07)', couleur: 'doux', epaisseur: 6 },
              { chemin: 'M44 160 A106 106 0 0 1 256 160', couleur: 'doux', epaisseur: 22, pointilles: [2.5, 8.3], bout: 'butt' },
              { id: 'rx2', chemin: 'M18 8 L284 172', couleur: 'corail', epaisseur: 18 },
            ] } },
            { texte: 'Sur un schéma à main levée, on raisonne avec les [codages]{#f2a .kw}, jamais avec le rapporteur.', interligne: 1.38 },
          ], ecart: 28 }, couleur: 'corail', id: 'fin2', taille: 44, marge: [28, 34] },
        ], ecart: 110 },
      ] }],
    },
  ],

  gestes(C) {
    /* ===== SCÈNE 1 — titre et objectif (b01) ===== */
    C.montre('#t-sur', 0.2);
    C.ecrit('#t-titre', '@b01+0.3', { dur: 0.9 });
    C.montre('#t-obj', '@b01~"corrige"+0.1');
    C.trace('#d-l1', '@b01~"droites"', 0.8);
    C.trace('#d-l2', '@b01~"parallèles"', 0.8);
    C.trace('#d-sc', '@b01~"angles"-0.2', 0.7);
    C.pulse('#t-titre', '@b01~"angles"', { scale: 1.04 });

    /* ===== SCÈNE 2 — figure + panneau ===== */
    C.montre('#q0', '@b02-0.1');

    /* ---- b02 : la figure se dessine, pas de rapporteur ---- */
    C.trace('#e-ia', '@b02~"schéma"-0.1', 0.6);
    C.trace('#e-ac', '@b02~"schéma"+0.45', 0.6);
    C.trace('#e-cb', '@b02~"schéma"+0.9', 0.6);
    C.trace('#e-bi', '@b02~"schéma"+1.35', 0.6);
    C.trace('#e-ab', '@b02~"schéma"+1.8', 0.6);
    C.montre(['#lI', '#lA', '#lC', '#lB'], '@b02~"levée"+0.4', { stagger: 0.2, y: 20 });
    C.montre('#note', '@b02~"main"+0.4');
    C.montre('#pas', '@b02~"mesure"-0.3');
    C.trace('#rx', '@b02~"rien"', 0.5);
    C.secoue('#pas-ic', '@b02~"rien"+0.55');
    C.ecrit('#pas-t1', '@b02~"rapporteur"+0.1', { dur: 0.7 });
    C.ecrit('#pas-t2', '@b02~"informations"', { dur: 0.8 });

    /* ---- b03 : angle droit BAC = 90° ---- */
    C.montre('#dh', '@b03~"codage"');
    C.allume('#lA', '@b03~"En"', { couleur: '--cyan', jusque: '@b03~"droit".fin+0.5' });
    C.trace('#ang-droit', '@b03~"droit"-0.2', 0.45);
    C.clignote('#ang-droit', '@b03~"droit"+0.45', 2, 0.15);
    C.tombe('#dc1', '@b03~"90"-0.15', { hauteur: 200, couleur: '--cyan' });

    /* ---- b04 : grand angle CAI = 140° ---- */
    C.trace('#a-cai', '@b04~"grand"-0.1', 0.9);
    C.apparait('#s-cai', '@b04~"grand"+0.3', 0.6);
    C.montre('#l140', '@b04~"140"-0.3', { y: 20 });
    C.tombe('#dc2', '@b04~"140"-0.1', { hauteur: 200, couleur: '--violet' });
    C.pulse('#l140', '@b04~"140".fin', { scale: 1.2 });

    /* ---- b05 : angle ABC = 50° ---- */
    C.allume('#lB', '@b05~"en"', { couleur: '--ambre', jusque: '@b05~"mesure"' });
    C.trace('#a-abc', '@b05~"mesure"-0.7', 0.6);
    C.apparait('#s-abc', '@b05~"mesure"-0.2', 0.5);
    C.montre('#l50b', '@b05~"mesure"+0.1', { y: 20 });
    C.tombe('#dc3', '@b05~"50"-0.15', { hauteur: 200, couleur: '--ambre' });

    /* ---- b06 : question 1 ---- */
    C.cache('#pas', '@b06-0.3');
    C.remplace('#q0', '#q1', '@b06-0.1');
    C.montre('#p-q1', '@b06~"Déterminer"-0.2');
    C.allume('#lA', '@b06~"mesure"', { couleur: '--ambre', jusque: '@b06.fin' });
    C.montre('#lq', '@b06~"mesure"+0.3', { y: 20 });

    /* ---- b07 : la demi-droite [AB) partage l'angle CAI ---- */
    C.trace('#ray-ab', '@b07~"demi"-0.1', 0.9);
    C.montre(['#p-sum', '#sm1'], '@b07~"grand"-0.1');   // la carte p-sum restait cachée dans la version HTML
    C.clignote('#s-cai', '@b07~"grand"+0.2', 2, 0.05);
    C.apparait('#s-bac', '@b07~"angles"+0.3', 0.5);
    C.montre('#sm2', '@b07~"angles"+0.55');
    C.apparait('#s-bai', '@b07~"et"+0.1', 0.5);
    C.montre('#sm3', '@b07~"et"+0.25');

    /* ---- b08 : on retire l'angle droit ---- */
    C.clignote('#s-bai', '@b08~"Donc"', 2, 0.1);
    C.pulse('#sm1', '@b08~"grand"', { scale: 1.2 });
    C.clignote('#s-bac', '@b08~"retire"-0.1', 2, 0.1);
    C.pulse('#sm2', '@b08~"retire"', { scale: 1.2 });

    /* ---- b09 : BAI = CAI − BAC (membre par membre) ---- */
    C.montre('#ch', '@b09~"écrit"-0.3');
    C.montre('#c1l', '@b09~"écrit"+0.3');
    C.montre('#c1e', '@b09~"égale"-0.05');
    C.montre('#c1a', '@b09~"égale"+0.6');
    C.montre('#c1m', '@b09~"moins"-0.05');
    C.montre('#c1b', '@b09~"moins"+0.3');
    C.clignote('#s-cai', '@b09~"égale"+0.6', 1, 0.05);
    C.clignote('#s-bac', '@b09~"moins"+0.3', 1, 0.1);

    /* ---- b10 : = 140° − 90° ---- */
    C.montre('#c2e', '@b10~"égale"-0.05');
    C.vole('#dv2', '#r2a', '@b10~"140"-0.25', { couleur: '--violet', dur: 0.8 });
    C.montre('#r2m', '@b10~"moins"-0.05');
    C.vole('#dv1', '#r2b', '@b10~"90"-0.3', { couleur: '--cyan', dur: 0.8 });

    /* ---- b11 : = 50°, résultat encadré, arc en A ---- */
    C.montre('#c3e', '@b11~"égale"-0.05');
    C.tombe('#r3', '@b11~"50"-0.15', { hauteur: 160, couleur: '--ambre' });
    C.encadre('#r3', '@b11~"50"+0.35', { couleur: '--vert', jusque: '@b12-0.4' });
    C.eclat('#r3', '@b11~"50"+0.5', { n: 18, force: 150 });
    C.trace('#a-bai', '@b11~"50"-0.1', 0.7);
    C.cache('#lq', '@b11~"égale"', { dur: 0.3 });
    C.montre('#l50a', '@b11~"50"+0.4', { y: 20 });
    C.montre('#p-res', '@b11~"mesure"-0.8');
    C.pulse('#l50a', '@b11~"mesure"+0.3', { scale: 1.25 });

    /* ---- b12 : question 2, les deux droites ---- */
    C.cache(['#p-q1', '#p-sum', '#ch', '#p-res'], '@b12-0.35');
    C.remplace('#q1', '#q2', '@b12-0.2');
    C.montre('#p-q2', '@b12~"Justifier"-0.2');
    C.trace('#L-ai', '@b12~"droites"+0.1', 0.9);
    C.montre('#t-ai', '@b12~"droites"+0.8', { y: 20 });
    C.trace('#L-bc', '@b12~"et"+0.1', 0.9);
    C.montre('#t-bc', '@b12~"et"+0.8', { y: 20 });
    C.montre('#c-dr', '@b12~"droites"+0.2');

    /* ---- b13 : les deux angles de 50°, la sécante (AB) ---- */
    C.clignote(['#s-bai', '#s-abc'], '@b13~"angles"', 3, 0.1);
    C.onde('#l50a', '@b13~"50"', { couleur: '--ambre' });
    C.onde('#l50b', '@b13~"50"+0.15', { couleur: '--ambre' });
    C.clignote(['#L-ai', '#L-bc'], '@b13~"droites"', 2, 0.3);
    C.trace('#ext-ab', '@b13~"coupées"-0.1', 0.7);
    C.montre('#t-ab', '@b13~"coupées"+0.5', { y: 20 });
    C.montre('#c-sec', '@b13~"sécante"-0.1');
    C.pulse('#c-sec', '@b13~"sécante"+0.3', { scale: 1.08 });
    C.clignote('#ray-ab', '@b13~"sécante"+0.1', 2, 0.25);

    /* ---- b14 : alternes-internes ---- */
    C.montre('#c-alt', '@b14~"situés"-0.5');
    C.ecrit('#al1', '@b14~"situés"-0.2', { dur: 0.7 });
    C.ecrit('#al2', '@b14~"part"-0.2', { dur: 0.9 });
    C.clignote(['#s-bai', '#s-abc'], '@b14~"part"', 2, 0.1);
    C.apparait('#strip', '@b14~"entre"-0.1', 0.7);
    C.ecrit('#al3', '@b14~"entre"-0.1', { dur: 0.8 });
    C.ecrit('#al4', '@b14~"alternes"-0.2', { dur: 0.8 });
    C.surligne('#al4', '@b14~"alternes"+0.4', { couleur: '--ambre' });
    C.clignote(['#s-bai', '#s-abc'], '@b14~"alternes"+0.5', 2, 0.1);

    /* ---- b15 → b16 : ce que je sais ---- */
    C.cache(['#p-q2', '#c-dr', '#c-sec', '#c-alt'], '@b15-0.35');
    C.apparait('#strip', '@b15-0.3', 0.5, 0);
    C.remplace('#q2', '#q3', '@b15-0.2');
    C.montre('#k1', '@b15~"temps"-0.3');
    C.montre('#e1', '@b16~"angle"+0.2');
    C.montre('#e2', '@b16~"égale"-0.05');
    C.montre('#e3', '@b16~"angle"2+0.25');
    C.montre('#e4', '@b16~"égale"2-0.05');
    C.tombe('#e5', '@b16~"50"-0.15', { hauteur: 120, couleur: '--ambre' });
    C.clignote(['#s-bai', '#s-abc'], '@b16~"50"+0.3', 2, 0.1);
    C.montre('#t1', '@b16~"angles"+0.25');
    C.montre('#t2', '@b16~"et"2-0.05');
    C.montre('#t3', '@b16~"et"2+0.1');
    C.montre('#t4', '@b16~"sont"-0.05');
    C.montre('#t5', '@b16~"alternes"-0.1');
    C.surligne('#t5', '@b16~"alternes"+0.4', { couleur: '--ambre' });

    /* ---- b17 → b18 : la propriété ---- */
    C.montre('#k2', '@b17~"propriété"-0.5');
    C.montre('#p1', '@b18~"Si"-0.05');
    C.montre('#p2', '@b18~"sécante"-0.1');
    C.clignote('#ext-ab', '@b18~"sécante"', 2, 0.2);
    C.montre('#p3', '@b18~"forment"-0.05');
    C.montre('#p4', '@b18~"alternes"-0.1');
    C.clignote(['#s-bai', '#s-abc'], '@b18~"alternes"+0.1', 2, 0.1);
    C.montre('#p5', '@b18~"même"-0.25');
    C.montre('#p6', '@b18~"mesure"-0.05');
    C.montre('#p7', '@b18~"alors"-0.05');
    C.montre('#p8', '@b18~"parallèles"-0.1');
    C.clignote(['#L-ai', '#L-bc'], '@b18~"parallèles"', 2, 0.3);

    /* ---- b19 → b20 : la conclusion ---- */
    C.montre('#k3', '@b19~"Enfin"');
    C.montre('#z1', '@b20~"droites"+0.1');
    C.montre('#z2', '@b20~"et"-0.05');
    C.encadre('#k3f', '@b20~"parallèles"-0.4', { couleur: '--vert', jusque: '@b21-0.4', marge: 24 });
    C.eclat('#k3f', '@b20~"parallèles"', { n: 24, force: 190 });
    C.clignote(['#L-ai', '#L-bc'], '@b20~"parallèles"', 2, 0.3);

    /* ---- b21 : à retenir ---- */
    C.cache('#redac', '@b21-0.4');
    C.remplace('#q3', '#q4', '@b21-0.2');
    C.montre('#fin1', '@b21~"retenir"-0.2');
    C.surligne('#f1a', '@b21~"alternes"+0.3', { couleur: '--ambre' });
    C.surligne('#f1b', '@b21~"mesure"', { couleur: '--ambre' });
    C.surligne('#f1c', '@b21~"parallèles"-0.1', { couleur: '--ambre' });
    C.montre('#fin2', '@b21~"schéma"-0.3');
    C.surligne('#f2a', '@b21~"codages"', { couleur: '--ambre' });
    C.trace('#rx2', '@b21~"jamais"+0.1', 0.5);
    C.eclat('#fin1', '@b21~"parallèles".fin', { n: 20, force: 170 });
  },
});
