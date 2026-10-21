/* Exercice 5 — tableau croisé d'un énoncé en pourcentages (voix de synthèse, ancres @bNN).
   Portage canvas d'exo5 (index.html + scenes.js) : mêmes contenus, même ordre, mêmes ancres.
   b13 et b14 : décalages relatifs au temps fort (la transcription de la voix tom n'a aucun mot entre 108 et 134 s). */
CAPSULE({
  titre: 'Exercice 5 — tableau croisé',
  audio: 'audio.wav', theme: 'nuit', ambiance: true, mention: 'Voix de synthèse', tailleMention: 24,

  scenes: [
    /* ===== SCÈNE 1 — rappel de l'énoncé ===== */
    { id: 's-enonce', gabarit: 'plein', debut: 0,
      zones: { titre: { x: 90, y: 58, l: 900, h: 280, ecart: 0 }, compteur: { x: 1010, y: 52, l: 850, h: 260 },
        dons: { x: 75, y: 345, l: 1770, h: 380 }, ghost: { x: 330, y: 372, l: 1260, h: 480 },
        evts: { x: 75, y: 752, l: 1770, h: 130 }, qs: { x: 75, y: 906, l: 1770, h: 110 } },
      titre: [
        { surTitre: 'Correction · Exercice 5', id: 't-sur' },
        { titre: '[Tableau croisé]{.grad}', id: 't-titre', nowrap: true },
        { espace: 27 },
        { puce: '🏬 Un magasin de sport', couleur: 'cyan', id: 't-mag' },
      ],
      compteur: [{ carte: { ligne: [
        { tex: '\\mathbf{600}', id: 't-n', taille: 176, gras: true, degrade: ['ambre', 'rose'] },
        { texte: 'clients', taille: 56, doux: true, nowrap: true },
      ], ecart: 24, valign: 'base' }, id: 't-cpt', marge: [6, 20], rayon: 28, align: 'gauche' }],
      dons: [{ ligne: [
        { carte: [{ tex: '\\mathbf{40\\,\\%}', taille: 138, couleur: 'ambre', lueur: 30 }, 'des clients possèdent la carte de fidélité',
          { puce: 'sur tous les clients', couleur: 'ambre', id: 'g1' }], couleur: 'ambre', id: 'd1c', l: 570, h: 372, justifie: 'entre', marge: [22, 30], taille: 40, interligne: 1.25 },
        { carte: [{ tex: '\\mathbf{75\\,\\%}', taille: 138, couleur: 'violet', lueur: 30 }, 'ont fait leurs achats un samedi',
          { puce: 'chez les porteurs de la carte', couleur: 'violet', id: 'g2' }], couleur: 'violet', id: 'd2c', l: 570, h: 372, justifie: 'entre', marge: [22, 30], taille: 40, interligne: 1.25 },
        { carte: [{ tex: '\\mathbf{30\\,\\%}', taille: 138, couleur: 'corail', lueur: 30 }, 'ont fait leurs achats un samedi',
          { puce: 'chez les autres clients', couleur: 'corail', id: 'g3' }], couleur: 'corail', id: 'd3c', l: 570, h: 372, justifie: 'entre', marge: [22, 30], taille: 40, interligne: 1.25 },
      ], ecart: 30 }],
      ghost: [{ id: 'ghost', hauteurCase: 118, taille: 80, tailleEntete: 38, tableau: [
        ['', { texte: 'Samedi', couleur: 'cyan' }, 'Autre jour', 'Total'],
        [{ texte: 'Avec carte', couleur: 'violet' }, { texte: '?', doux: true }, { texte: '?', doux: true }, { texte: '?', doux: true }],
        [{ texte: 'Sans carte', couleur: 'corail' }, { texte: '?', doux: true }, { texte: '?', doux: true }, { texte: '?', doux: true }],
        ['Total', { texte: '?', doux: true }, { texte: '?', doux: true }, { texte: '?', doux: true }],
      ] }],
      evts: [{ ligne: [
        { carte: { ligne: [{ lettre: 'C', couleur: 'violet', id: 'e-c-l' }, { texte: '« possède la carte »', id: 'e-c-t', nowrap: true }], ecart: 24 },
          couleur: 'violet', id: 'e-c', l: 870, marge: [16, 30], taille: 42 },
        { carte: { ligne: [{ lettre: 'S', couleur: 'cyan', id: 'e-s-l' }, { texte: '« achats un samedi »', id: 'e-s-t', nowrap: true }], ecart: 24 },
          couleur: 'cyan', id: 'e-s', l: 870, marge: [16, 30], taille: 42 },
      ], ecart: 30 }],
      qs: [{ ligne: [
        { carte: { ligne: [{ texte: '1', gras: true, couleur: 'rose' }, { texte: 'Tableau croisé', nowrap: true }], ecart: 16, justifie: 'centre' }, couleur: 'rose', id: 'k1', marge: [12, 20], taille: 38, tailleTex: 44 },
        { carte: { ligne: [{ texte: '2', gras: true, couleur: 'rose' }, { tex: 'P(C),\\ P(S)' }], ecart: 16, justifie: 'centre' }, couleur: 'rose', id: 'k2', marge: [12, 20], taille: 38, tailleTex: 44 },
        { carte: { ligne: [{ texte: '3', gras: true, couleur: 'rose' }, { tex: 'P_C(S)' }], ecart: 16, justifie: 'centre' }, couleur: 'rose', id: 'k3', marge: [12, 20], taille: 38, tailleTex: 44 },
        { carte: { ligne: [{ texte: '4', gras: true, couleur: 'rose' }, { tex: 'P_S(C)' }], ecart: 16, justifie: 'centre' }, couleur: 'rose', id: 'k4', marge: [12, 20], taille: 38, tailleTex: 44 },
      ], ecart: 22, egal: true }],
    },

    /* ===== SCÈNE 2 — le tableau et les calculs ===== */
    { id: 's-main', gabarit: 'plein', debut: '@b08-0.2',
      zones: { bandeau: { x: 70, y: 34, l: 1780, h: 80 }, tableau: { x: 70, y: 148, l: 1020, h: 650 },
        bas: { x: 70, y: 818, l: 1020, h: 200 }, panneau: { x: 1130, y: 148, l: 720, h: 860 } },
      bandeau: { valign: 'centre', contenu: [{ ligne: [
        { pile: ['Question 1', 'Question 2', 'Question 3', 'Question 4'].map((q, i) => ({ puce: q, couleur: 'rose', id: 'q' + (i + 1), taille: 38, margeH: 32 })) },
        { ligne: [
          { puce: 'Dresser', numero: 1, couleur: 'ambre', id: 'st1', taille: 34, margeV: 8, margeH: 22 },
          { puce: 'Au total', numero: 2, couleur: 'ambre', id: 'st2', taille: 34, margeV: 8, margeH: 22 },
          { puce: 'Au total de la ligne', numero: 3, couleur: 'ambre', id: 'st3', taille: 34, margeV: 8, margeH: 22 },
          { puce: 'Compléter', numero: 4, couleur: 'ambre', id: 'st4', taille: 34, margeV: 8, margeH: 22 },
        ], ecart: 16 },
      ], ecart: 26 }] },
      tableau: [{ id: 'tab', hauteurCase: 158, taille: 72, tailleEntete: 36, totaux: true, tableau: [
        [{ texte: 'Effectifs', taille: 32 },
          { ligne: [{ lettre: 'S', couleur: 'cyan', taille: 50 }, { texte: 'Samedi', couleur: 'cyan', gras: true, nowrap: true }], ecart: 12, id: 'h-s' },
          { texte: 'Autre jour', id: 'h-a' }, 'Total'],
        [{ ligne: [{ lettre: 'C', couleur: 'violet', taille: 50 }, { texte: 'Avec carte', couleur: 'violet', gras: true }], ecart: 12, id: 'r-c' },
          { n: 180, id: 'v-cs' }, { n: 60, id: 'v-ca' }, { n: 240, id: 'v-ct' }],
        [{ texte: 'Sans carte', couleur: 'corail', id: 'r-n' }, { n: 108, id: 'v-ns' }, { n: 252, id: 'v-na' }, { n: 360, id: 'v-nt' }],
        ['Total', { n: 288, id: 'v-xs' }, { n: 312, id: 'v-xa' }, { n: 600, id: 'v-xx', couleur: 'ambre' }],
      ] }],
      bas: [{ pile: [
        { ligne: [
          { carte: [{ tex: '\\mathbf{40\\,\\%}', id: 'dn1', couleur: 'ambre', taille: 60 }, { texte: 'tous les clients', taille: 34, nowrap: true }], couleur: 'ambre', id: 'rc1', marge: [10, 15], rayon: 24, ecart: 0 },
          { carte: [{ tex: '\\mathbf{75\\,\\%}', id: 'dn2', couleur: 'violet', taille: 60 }, { texte: 'chez les porteurs', taille: 34, nowrap: true }], couleur: 'violet', id: 'rc2', marge: [10, 15], rayon: 24, ecart: 0 },
          { carte: [{ tex: '\\mathbf{30\\,\\%}', id: 'dn3', couleur: 'corail', taille: 60 }, { texte: 'chez les autres', taille: 34, nowrap: true }], couleur: 'corail', id: 'rc3', marge: [10, 15], rayon: 24, ecart: 0 },
        ], ecart: 12, egal: true },
        { carte: 'Le « [sachant]{#f-mot .kw} » donne le [dénominateur]{.kw}', couleur: 'ambre', id: 'fin', taille: 46, marge: [16, 30], alignEnfants: 'centre', nowrap: true, dy: 8 },
      ] }],
      panneau: [{ pile: [
        // la méthode en quatre étapes (b08 → b10)
        { colonne: [1, 2, 3, 4].map(i => ({ carte: { ligne: [{ pastille: i, taille: 56 },
          { texte: ['Dresser le tableau', 'Appliquer au total', 'Appliquer au total de sa ligne', 'Compléter par différence'][i - 1], gras: true, nowrap: true }], ecart: 20 },
          couleur: 'ambre', id: 'et' + i, marge: [28, 28], taille: 39 })), ecart: 26 },
        // étape 2
        { colonne: [
          { carte: [{ texte: '40 % de tous les clients', couleur: 'ambre' }, { ligne: [{ tex: '\\cssId{a0}{0{,}40}\\times\\cssId{a1}{600}=' }, { tex: '\\mathbf{240}', id: 'x240', couleur: 'violet', taille: 84, lueur: 22, lueurForce: 0.5 }], ecart: 18, h: 130 }],
            couleur: 'ambre', id: 'l2a', h: 250, justifie: 'centre', marge: [14, 30], ecart: 0, taille: 36, gras: true, tailleTex: 70 },
          { carte: [{ texte: 'les autres clients', couleur: 'corail' }, { ligne: [{ tex: '\\cssId{b1}{600}-\\cssId{b2}{240}=' }, { tex: '\\mathbf{360}', id: 'x360', couleur: 'corail', taille: 84, lueur: 22, lueurForce: 0.5 }], ecart: 18, h: 130 }],
            couleur: 'corail', id: 'l2b', h: 250, justifie: 'centre', marge: [14, 30], ecart: 0, taille: 36, gras: true, tailleTex: 70 },
        ], ecart: 26 },
        // étape 3
        { colonne: [
          { carte: { ligne: [{ texte: '« chez les »', id: 'pg-m', taille: 52, gras: true, couleur: 'corail', nowrap: true },
            { texte: '⟶ le total de la [ligne]{.kw},\npas 600 !', taille: 36, interligne: 1.2, nowrap: true }], ecart: 18 },
            couleur: 'corail', id: 'pg', h: 170, justifie: 'centre', marge: [14, 22] },
          { carte: [{ texte: '75 % de la ligne « avec carte »', couleur: 'violet' }, { ligne: [{ tex: '\\cssId{c0}{0{,}75}\\times\\cssId{c1}{240}=' }, { tex: '\\mathbf{180}', id: 'x180', couleur: 'ambre', taille: 84, lueur: 22, lueurForce: 0.5 }], ecart: 18, h: 130 }],
            couleur: 'violet', id: 'l3a', h: 250, justifie: 'centre', marge: [14, 30], ecart: 0, taille: 36, gras: true, tailleTex: 70 },
          { carte: [{ texte: '30 % de la ligne « sans carte »', couleur: 'corail' }, { ligne: [{ tex: '\\cssId{y0}{0{,}30}\\times\\cssId{y1}{360}=' }, { tex: '\\mathbf{108}', id: 'x108', couleur: 'ambre', taille: 84, lueur: 22, lueurForce: 0.5 }], ecart: 18, h: 130 }],
            couleur: 'corail', id: 'l3b', h: 250, justifie: 'centre', marge: [14, 30], ecart: 0, taille: 36, gras: true, tailleTex: 70 },
        ], ecart: 22 },
        // étape 4
        { colonne: [
          ['l4a', 'violet', 'Avec carte · autre jour', '\\cssId{e1}{240}-\\cssId{e2}{180}=', 'x60', '60', 'violet'],
          ['l4b', 'corail', 'Sans carte · autre jour', '\\cssId{f1}{360}-\\cssId{f2}{108}=', 'x252', '252', 'corail'],
          ['l4c', 'cyan', 'Total samedi', '\\cssId{w1}{180}+\\cssId{w2}{108}=', 'x288', '288', 'cyan'],
          ['l4d', 'cyan', 'Total autre jour', '\\cssId{h1}{60}+\\cssId{h2}{252}=', 'x312', '312', 'cyan'],
          ['l4e', 'vert', 'Vérification', '\\cssId{i1}{288}+\\cssId{i2}{312}=', 'x600', '600', 'ambre'],
        ].map(([id, c, tag, f, idn, v, cn]) => ({ carte: [{ texte: tag, couleur: c }, { ligne: [{ tex: f }, { tex: '\\mathbf{' + v + '}', id: idn, couleur: cn, taille: 66, lueur: 22, lueurForce: 0.5 }], ecart: 18, h: 84 }],
          couleur: c, id, marge: [10, 26], margeBas: 12, ecart: 0, taille: 34, gras: true, tailleTex: 58 })), ecart: 12 },
        // questions 2 à 4 : les quatre lignes restent empilées
        { colonne: [
          ['lq1', 'violet', 'Sans condition : le total', 'P(C)=\\dfrac{\\cssId{p1}{240}}{\\cssId{p2}{600}}', 'eq1', 'rq1', '0{,}4'],
          ['lq2', 'cyan', 'Sans condition : le total', 'P(S)=\\dfrac{\\cssId{p3}{288}}{\\cssId{p4}{600}}', 'eq2', 'rq2', '0{,}48'],
          ['lq3', 'violet', 'Sachant C : la ligne « avec carte »', 'P_C(S)=\\dfrac{\\cssId{p5}{180}}{\\cssId{p6}{240}}', 'eq3', 'rq3', '0{,}75'],
          ['lq4', 'cyan', 'Sachant S : la colonne « samedi »', 'P_S(C)=\\dfrac{\\cssId{p7}{180}}{\\cssId{p8}{288}}', 'eq4', 'rq4', '0{,}625'],
        ].map(([id, c, tag, f, eq, r, v]) => ({ carte: [{ texte: tag, couleur: c }, { ligne: [{ tex: f }, { tex: '=', id: eq }, { resultat: '$\\mathbf{' + v + '}$', couleur: 'vert', id: r, taille: 64 }], ecart: 18, h: 128 }],
          couleur: c, id, marge: [10, 26], margeBas: 12, ecart: 0, taille: 34, gras: true, tailleTex: 58 })), ecart: 14 },
      ] }],
    },
  ],

  gestes(C) {
    const ligC = ['#tab-l1c0', '#tab-l1c1', '#tab-l1c2', '#tab-l1c3'];
    const ligN = ['#tab-l2c0', '#tab-l2c1', '#tab-l2c2', '#tab-l2c3'];
    const colS = ['#tab-l0c1', '#tab-l1c1', '#tab-l2c1', '#tab-l3c1'];
    const colA = ['#tab-l0c2', '#tab-l1c2', '#tab-l2c2', '#tab-l3c2'];
    const V = { dur: 0.8 };               // durée des vols courts

    /* ===== SCÈNE 1 — rappel de l'énoncé (b01 → b07) ===== */
    C.montre('#t-sur', 0.2);
    C.ecrit('#t-titre', '@b01+0.5', { dur: 1.1 });
    C.montre('#ghost', '@b01~"tableau"+0.2', { dur: 0.9 });
    C.cache('#ghost', '@b03-0.3', { dur: 0.3 });
    C.pulse('#t-titre', '@b01~"tableau"', { scale: 1.06 });

    // b02 : 600 clients
    C.montre('#t-mag', '@b02~"magasin"-0.2');
    C.montre('#t-cpt', '@b02~"600"-0.5');
    C.compte('#t-n', '@b02~"600"-0.4', { de: 0, a: 600, dur: 1.2 });
    C.eclat('#t-n', '@b02~"600"+0.9', { n: 24 });

    // b03 : 40 % — sur tous les clients
    C.tombe('#d1c', '@b03-0.15', { hauteur: 300, couleur: '--ambre' });
    C.montre('#g1', '@b03~"clients"+0.2');
    C.allume('#t-cpt', '@b03~"clients"', { couleur: '--ambre', jusque: '@b03.fin' });

    // b04 : 75 % — chez les porteurs de la carte
    C.tombe('#d2c', '@b04~"75"-0.15', { hauteur: 300, couleur: '--violet' });
    C.montre('#g2', '@b04~"75"+0.5');

    // b05 : 30 % — chez les autres clients
    C.tombe('#d3c', '@b05~"tombe"-0.2', { hauteur: 300, couleur: '--corail' });
    C.montre('#g3', '@b05~"tombe"+0.6');

    // b06 : les événements C et S
    C.montre('#e-c', '@b06~"hasard".fin+0.4');
    C.pulse('#e-c-l', '@b06~"hasard".fin+0.7', { scale: 1.3 });
    C.ecrit('#e-c-t', '@b06~"possède"-0.8', { dur: 1.0 });
    C.montre('#e-s', '@b06~"et s"-0.1');
    C.pulse('#e-s-l', '@b06~"et s"+0.2', { scale: 1.3 });
    C.ecrit('#e-s-t', '@b06~"achats"-0.7', { dur: 1.0 });

    // b07 : les quatre questions
    C.tombe('#k1', '@b07~"construire"-0.1', { hauteur: 200, couleur: '--rose' });
    C.tombe('#k2', '@b07~"calculer"-0.1', { hauteur: 200, couleur: '--rose' });
    C.tombe('#k3', '@b07~"puis"-0.1', { hauteur: 200, couleur: '--rose' });
    C.tombe('#k4', '@b07~"probabilités"-0.1', { hauteur: 200, couleur: '--rose' });

    /* ===== SCÈNE 2 — le tableau et les calculs (b08 → fin) ===== */
    C.montre('#q1', '@b08+0.2');
    C.montre(['#rc1', '#rc2', '#rc3'], '@b08~"méthode"', { stagger: 0.18 });
    C.tombe('#et1', '@b08~"étapes".fin+0.2', { hauteur: 160, couleur: '--ambre' });
    C.tombe('#et2', '@b08~"total"-0.6', { hauteur: 160, couleur: '--ambre' });
    C.tombe('#et3', '@b08~"total"2-0.8', { hauteur: 160, couleur: '--ambre' });
    C.tombe('#et4', '@b08~"ligne".fin+0.15', { hauteur: 160, couleur: '--ambre' });

    /* ---- b09 : étape 1, dresser le tableau ---- */
    C.tombe('#st1', '@b09+0.05', { hauteur: 100, couleur: '--ambre' });
    C.allume('#et1', '@b09+0.1', { couleur: '--ambre', jusque: '@b10' });
    C.allume('#st1', '@b09+0.15', { couleur: '--ambre', jusque: '@b10' });
    C.montre('#tab', '@b09~"dresse"-0.2', { dur: 0.8 });
    C.tombe('#r-c', '@b09~"avec"-0.1', { hauteur: 120, couleur: '--violet' });
    C.tombe('#r-n', '@b09~"sans"-0.1', { hauteur: 120, couleur: '--corail' });
    C.tombe('#h-s', '@b09~"samedi"-0.1', { hauteur: 120, couleur: '--cyan' });
    C.tombe('#h-a', '@b09~"et".fin+0.1', { hauteur: 120, couleur: '--cyan' });
    C.allume('#tab-l3c3', '@b09~"dans"', { couleur: '--ambre', jusque: '@b09~"600".fin+0.5' });
    C.pointe('#v-xx', '@b09~"dans"+0.1');
    C.tombe('#v-xx', '@b09~"600"-0.15', { hauteur: 300, couleur: '--ambre' });
    C.eclat('#v-xx', '@b09~"600"+0.4', { n: 18, force: 150 });
    C.pointe(null, '@b09~"600".fin+0.5');

    /* ---- b10 : étape 2, appliquer au total ---- */
    C.tombe('#st2', '@b10+0.05', { hauteur: 100, couleur: '--ambre' });
    C.allume('#et2', '@b10+0.1', { couleur: '--ambre', jusque: '@b10~"donc"-0.3' });
    C.cache(['#et1', '#et2', '#et3', '#et4'], '@b10~"donc"-0.3');
    C.allume('#st2', '@b10+0.2', { couleur: '--ambre', jusque: '@b11' });
    C.allume('#rc1', '@b10~"40"', { couleur: '--ambre', jusque: '@b10~"donc"' });
    C.allume('#tab-l3c3', '@b10~"tous"', { couleur: '--ambre', jusque: '@b10~"donc".fin' });
    C.montre('#l2a', '@b10~"donc"-0.2');
    C.vole('#dn1', '#a0', '@b10~"donc"+0.1', { couleur: '--ambre', tex: '0{,}40', ...V });
    C.vole('#v-xx', '#a1', '@b10~"fait"-1.4', { couleur: '--ambre', ...V });
    C.tombe('#x240', '@b10~"fait"+0.1', { hauteur: 160, couleur: '--violet' });
    C.vole('#x240', '#v-ct', '@b10~"avec"-0.1', { couleur: '--violet', dur: 0.9 });
    C.montre('#l2b', '@b10~"reste"-0.3');
    C.vole('#v-xx', '#b1', '@b10~"reste"-0.1', { couleur: '--ambre', ...V });
    C.vole('#v-ct', '#b2', '@b10~"moins"-0.15', { couleur: '--violet', ...V });
    C.tombe('#x360', '@b10~"soit"+0.05', { hauteur: 160, couleur: '--corail' });
    C.vole('#x360', '#v-nt', '@b10~"sans"-0.1', { couleur: '--corail', dur: 0.9 });

    /* ---- b11 : étape 3, le piège « chez les » ---- */
    C.cache(['#l2a', '#l2b'], '@b11~"piège"-0.6');
    C.tombe('#st3', '@b11+0.05', { hauteur: 100, couleur: '--ambre' });
    C.allume('#st3', '@b11+0.2', { couleur: '--ambre', jusque: '@b13' });
    C.montre('#pg', '@b11~"piège"-0.2');
    C.secoue('#pg', '@b11~"piège".fin');
    C.allume('#rc2', '@b11~"75"-0.1', { couleur: '--violet', jusque: '@b11~"30"-0.1' });
    C.allume('#rc3', '@b11~"30"-0.1', { couleur: '--corail', jusque: '@b11~"introduits"+0.5' });
    C.surligne('#pg-m', '@b11~"par"', { couleur: '--corail' });
    C.pulse('#pg-m', '@b11~"par"+0.3', { scale: 1.15 });
    C.entoure('#tab-l3c3', '@b11~"pas"-0.4', { couleur: '--corail', jusque: '@b11~"mais"' });
    C.secoue('#tab-l3c3', '@b11~"pas"');
    C.allume(ligC, '@b11~"total"-0.2', { couleur: '--violet', jusque: '@b12' });
    C.allume(ligN, '@b11~"total"+0.3', { couleur: '--corail', jusque: '@b12' });

    /* ---- b12 : étape 3, 0,75 × 240 et 0,30 × 360 ---- */
    C.allume(ligC, '@b12', { couleur: '--violet', jusque: '@b12~"sans"-0.2' });
    C.montre('#l3a', '@b12');
    C.vole('#dn2', '#c0', '@b12~"donne"-3.4', { couleur: '--violet', tex: '0{,}75', ...V });
    C.vole('#v-ct', '#c1', '@b12~"donne"-2.2', { couleur: '--violet', ...V });
    C.tombe('#x180', '@b12~"donne"-0.1', { hauteur: 160, couleur: '--ambre' });
    C.eclat('#x180', '@b12~"donne"+0.5', { n: 10, force: 110 });
    C.vole('#x180', '#v-cs', '@b12~"donne".fin+0.2', { couleur: '--ambre', dur: 0.9 });
    C.allume(ligN, '@b12~"sans"-0.1', { couleur: '--corail', jusque: '@b13' });
    C.montre('#l3b', '@b12~"sans"-0.3');
    C.vole('#dn3', '#y0', '@b12~"sans"+0.9', { couleur: '--corail', tex: '0{,}30', ...V });
    C.vole('#v-nt', '#y1', '@b12~"sans"+2.1', { couleur: '--corail', ...V });
    C.tombe('#x108', '@b12~"donne"2-0.1', { hauteur: 160, couleur: '--ambre' });
    C.eclat('#x108', '@b12~"donne"2+0.5', { n: 10, force: 110 });
    C.vole('#x108', '#v-ns', '@b12~"donne"2.fin+0.25', { couleur: '--ambre', dur: 0.9 });

    /* ---- b13 : étape 4, compléter par différence (décalages relatifs au temps fort) ---- */
    C.cache(['#pg', '#l3a', '#l3b'], '@b13');
    C.tombe('#st4', '@b13+0.05', { hauteur: 100, couleur: '--ambre' });
    C.allume('#st4', '@b13+0.15', { couleur: '--ambre', jusque: '@b16' });
    C.montre('#l4a', '@b13+2.8');
    C.allume('#tab-l1c2', '@b13+3.0', { couleur: '--violet', jusque: '@b13+7.6' });
    C.vole('#v-ct', '#e1', '@b13+3.9', { couleur: '--violet', ...V });
    C.vole('#v-cs', '#e2', '@b13+4.8', { couleur: '--ambre', ...V });
    C.tombe('#x60', '@b13+6.9', { hauteur: 160, couleur: '--violet' });
    C.vole('#x60', '#v-ca', '@b13+7.6', { couleur: '--violet', dur: 0.9 });
    C.montre('#l4b', '@b13+8.0');
    C.allume('#tab-l2c2', '@b13+8.2', { couleur: '--corail', jusque: '@b13+12.9' });
    C.vole('#v-nt', '#f1', '@b13+9.1', { couleur: '--corail', ...V });
    C.vole('#v-ns', '#f2', '@b13+10.2', { couleur: '--ambre', ...V });
    C.tombe('#x252', '@b13+12.0', { hauteur: 160, couleur: '--corail' });
    C.vole('#x252', '#v-na', '@b13+12.9', { couleur: '--corail', dur: 0.9 });

    /* ---- b14 : les totaux des colonnes ---- */
    C.montre('#l4c', '@b14+1.2');
    C.allume(colS, '@b14+1.2', { couleur: '--cyan', jusque: '@b14+5.6' });
    C.vole('#v-cs', '#w1', '@b14+1.5', { couleur: '--ambre', ...V });
    C.vole('#v-ns', '#w2', '@b14+2.6', { couleur: '--ambre', ...V });
    C.tombe('#x288', '@b14+4.5', { hauteur: 160, couleur: '--cyan' });
    C.vole('#x288', '#v-xs', '@b14+5.4', { couleur: '--cyan', dur: 0.9 });
    C.montre('#l4d', '@b14+6.0');
    C.allume(colA, '@b14+6.0', { couleur: '--cyan', jusque: '@b14+10.8' });
    C.vole('#v-ca', '#h1', '@b14+6.4', { couleur: '--violet', ...V });
    C.vole('#v-na', '#h2', '@b14+7.2', { couleur: '--corail', ...V });
    C.tombe('#x312', '@b14+9.7', { hauteur: 160, couleur: '--cyan' });
    C.vole('#x312', '#v-xa', '@b14+10.4', { couleur: '--cyan', dur: 0.9 });

    /* ---- b15 : vérification 288 + 312 = 600 ---- */
    C.montre('#l4e', '@b15+0.2');
    C.vole('#v-xs', '#i1', '@b15+0.8', { couleur: '--cyan', ...V });
    C.vole('#v-xa', '#i2', '@b15+1.9', { couleur: '--cyan', ...V });
    C.tombe('#x600', '@b15~"bien".fin', { hauteur: 160, couleur: '--ambre' });
    C.eclat('#x600', '@b15~"bien".fin+0.5', { n: 20, force: 170 });
    C.pulse('#v-xx', '@b15~"bien".fin+0.6', { scale: 1.25 });
    C.encadre('#tab', '@b15~"juste"-0.9', { couleur: '--vert', jusque: '@b16+1.2' });

    /* ---- b16 → b17 : question 2, probabilités sans condition ---- */
    C.cache(['#st1', '#st2', '#st3', '#st4'], '@b16');
    C.remplace('#q1', '#q2', '@b16+0.1');
    C.cache(['#l4a', '#l4b', '#l4c', '#l4d', '#l4e'], '@b16+0.3');
    C.allume('#tab-l3c3', '@b16~"effectif"', { couleur: '--ambre', jusque: '@b17.fin' });
    C.montre('#lq1', '@b16~"condition"');
    C.montre('#lq2', '@b16~"600"-0.2');
    // P(C) = 240 / 600
    C.allume('#tab-l1c3', '@b17~"240"-0.9', { couleur: '--violet', jusque: '@b17~"soit"' });
    C.vole('#v-ct', '#p1', '@b17~"240"-0.8', { couleur: '--violet', ...V });
    C.vole('#v-xx', '#p2', '@b17~"240"+0.1', { couleur: '--ambre', ...V });
    C.montre('#eq1', '@b17~"soit"-0.3');
    C.tombe('#rq1', '@b17~"soit"+0.1', { hauteur: 160, couleur: '--vert' });
    C.eclat('#rq1', '@b17~"soit"+0.55');
    // P(S) = 288 / 600
    C.allume('#tab-l3c1', '@b17~"288"-0.9', { couleur: '--cyan', jusque: '@b17~"soit"2' });
    C.vole('#v-xs', '#p3', '@b17~"288"-0.8', { couleur: '--cyan', ...V });
    C.vole('#v-xx', '#p4', '@b17~"288"+0.2', { couleur: '--ambre', ...V });
    C.montre('#eq2', '@b17~"soit"2-0.3');
    C.tombe('#rq2', '@b17~"soit"2+0.1', { hauteur: 160, couleur: '--vert' });
    C.eclat('#rq2', '@b17~"soit"2+0.55');

    /* ---- b18 → b20 : question 3, P_C(S), la LIGNE « avec carte » ---- */
    C.remplace('#q2', '#q3', '@b18');
    C.montre('#lq3', '@b18~"sachant"');
    C.allume(ligC, '@b18~"restreindre"-0.1', { couleur: '--violet', jusque: '@b19.fin' });
    C.pointe('#v-ct', '@b18~"240"-0.1');
    C.pointe('#v-cs', '@b18~"180"-0.1');
    C.pointe(null, '@b18.fin');
    C.vole('#v-cs', '#p5', '@b19~"180"-0.9', { couleur: '--ambre', ...V });
    C.vole('#v-ct', '#p6', '@b19~"sur"-0.3', { couleur: '--violet', ...V });
    C.montre('#eq3', '@b19~"dire"-0.5');
    C.tombe('#rq3', '@b19~"dire"', { hauteur: 160, couleur: '--vert' });
    C.eclat('#rq3', '@b19~"dire"+0.5');
    // b20 : on retrouve les 75 % de l'énoncé
    C.allume('#rc2', '@b20~"75"-0.1', { couleur: '--vert', jusque: '@b20~"donnée"' });
    C.pulse('#rq3', '@b20~"75"', { scale: 1.2 });
    C.fleche('#rq3', '#rc2', '@b20~"75"+0.1', { couleur: '--vert', courbure: 0.3, jusque: '@b20~"donnée"+0.3' });
    C.allume(ligC, '@b20~"chez"-0.1', { couleur: '--violet', jusque: '@b20~"porteurs".fin+0.8' });
    C.encadre('#tab', '@b20~"confirme"', { couleur: '--vert', jusque: '@b21+0.4' });

    /* ---- b21 → b22 : question 4, P_S(C), la COLONNE « samedi » ---- */
    C.remplace('#q3', '#q4', '@b21');
    C.montre('#lq4', '@b21+1.4');
    C.allume(colS, '@b21~"restreint"-0.1', { couleur: '--cyan', jusque: '@b22.fin' });
    C.pointe('#v-xs', '@b21~"288"-0.1');
    C.pointe('#v-cs', '@b21~"180"-0.1');
    C.pointe(null, '@b21.fin');
    C.vole('#v-cs', '#p7', '@b22~"180"-0.9', { couleur: '--ambre', ...V });
    C.vole('#v-xs', '#p8', '@b22~"sur"-0.3', { couleur: '--cyan', ...V });
    C.montre('#eq4', '@b22~"soit"-0.3');
    C.tombe('#rq4', '@b22~"soit"+0.1', { hauteur: 160, couleur: '--vert' });
    C.eclat('#rq4', '@b22~"soit"+0.5');

    /* ---- b23 : même case, pas le même dénominateur ---- */
    C.allume(ligC, '@b23~"regardez"', { couleur: '--violet', jusque: '@b23~"mais"-0.1' });
    C.allume(colS, '@b23~"regardez"+0.3', { couleur: '--cyan', jusque: '@b23~"mais"-0.1' });
    C.allume('#tab-l1c1', '@b23~"case"-0.1', { couleur: '--ambre', marge: 12, jusque: '@b23~"mais"-0.1' });
    C.pulse('#v-cs', '@b23~"case"', { scale: 1.35 });
    C.entoure('#tab-l1c1', '@b23~"case"+0.3', { couleur: '--ambre', jusque: '@b23~"mais"' });
    C.allume(['#p5', '#p7'], '@b23~"case"+0.4', { couleur: '--ambre', chacun: true, jusque: '@b23~"mais"-0.1' });
    C.pulse(['#p5', '#p7'], '@b23~"case"+0.5', { scale: 1.25 });
    C.allume(['#p6', '#p8'], '@b23~"mais"+0.1', { couleur: '--corail', chacun: true, jusque: '@b24~"240"-0.3' });
    C.pulse(['#p6', '#p8'], '@b23~"mais"+0.2', { scale: 1.25 });

    /* ---- b24 : c'est le « sachant » qui donne le dénominateur ---- */
    C.allume(ligC, '@b24~"240"-0.2', { couleur: '--violet', jusque: '@b24~"288"-0.2' });
    C.pulse('#p6', '@b24~"240"', { scale: 1.3 });
    C.allume(colS, '@b24~"288"-0.2', { couleur: '--cyan', jusque: '@b24~"retenez"' });
    C.pulse('#p8', '@b24~"288"', { scale: 1.3 });
    C.cache(['#rc1', '#rc2', '#rc3'], '@b24~"retenez"-0.2');
    C.montre('#fin', '@b24~"retenez".fin');
    C.surligne('#f-mot', '@b24~"sachant"3-0.1', { couleur: '--ambre' });
    C.encadre('#fin', '@b24~"dénominateur"-0.1', { couleur: '--ambre' });
    C.eclat('#fin', '@b24~"dénominateur"', { n: 30, force: 260 });
    C.pulse(['#rq3', '#rq4'], '@b24~"dénominateur".fin', { scale: 1.15 });
  },
});
