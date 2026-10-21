/* Centre de loisirs — P(M), P(B), P(M∩B). Voie A : ancres = index de mots (data/transcript.txt).
   Portage canvas de tableau-croise (index.html + scenes.js) : mêmes contenus, même ordre, mêmes ancres. */
CAPSULE({
  titre: 'Centre de loisirs — probabilités',
  audio: 'audio.m4a', theme: 'nuit', ambiance: true,
  corrections: { 'tableau 6 contre': 'tableau croisé', 'P2M': 'P de M', '150 sur 200': '150 sur 250', 'donne 42': 'donne 0,42' },

  scenes: [
    /* ---- 1. Titre : le décor de l'exercice ---- */
    { id: 's-titre', gabarit: 'plein', debut: 0,
      zones: { centre: { x: 150, y: 0, l: 1620, h: 1080, valign: 'centre', ecart: 34 } },
      centre: [
        { surTitre: 'Correction · Probabilités', id: 't-sur' },
        { titre: 'Le centre de [loisirs]{.grad}', id: 't-titre' },
        { ligne: [
          { tex: '\\mathbf{250}', id: 't-n', taille: 190, gras: true, degrade: ['ambre', 'rose'] },
          { texte: 'jeunes inscrits', taille: 64, doux: true, nowrap: true },
        ], ecart: 26, valign: 'base', id: 't-compteur' },
        { ligne: [
          { puce: '🎵 Musique', couleur: 'violet', id: 'p-mus' },
          { puce: '🎭 Théâtre', couleur: 'rose', id: 'p-the' },
          { trait: 'vertical', h: 60, id: 'p-sep' },
          { puce: '🚌 Bus', couleur: 'cyan', id: 'p-bus' },
          { puce: '🚲 Autre moyen', couleur: 'ambre', id: 'p-aut' },
        ], ecart: 22 },
      ] },

    /* ---- 2. Scène principale : événements, tableau, calculs ---- */
    { id: 's-main', gabarit: 'plein', debut: '#35',
      zones: { bandeau: { x: 90, y: 36, l: 1740, h: 70 }, evts: { x: 90, y: 135, l: 1740, h: 110 },
        hasard: { x: 600, y: 520, l: 900, h: 140 }, tableau: { x: 90, y: 290, l: 960, h: 580 },
        bas: { x: 90, y: 890, l: 960, h: 160 }, panneau: { x: 1100, y: 290, l: 730, h: 760, ecart: 36 } },
      bandeau: { valign: 'centre', contenu: [{ ligne: [
        { texte: 'Centre de loisirs · **$\\mathbf{250}$ jeunes**', id: 'b-lieu', taille: 30, doux: true, nowrap: true },
        { pile: [{ puce: 'Question 1', couleur: 'cyan', id: 'q1' }, { puce: 'Question 2', couleur: 'rose', id: 'q2' }] },
      ], justifie: 'entre' }] },
      evts: [{ ligne: [
        { carte: { ligne: [{ lettre: 'M', couleur: 'violet', taille: 70, id: 'e-m-l' }, { texte: '« le jeune est inscrit en musique »', id: 'e-m-t', nowrap: true }], ecart: 22 },
          couleur: 'violet', id: 'e-m', marge: [18, 30], taille: 38, focus: true },
        { carte: { ligne: [{ lettre: 'B', couleur: 'cyan', taille: 70, id: 'e-b-l' }, { texte: '« le jeune vient en bus »', id: 'e-b-t', nowrap: true }], ecart: 22 },
          couleur: 'cyan', id: 'e-b', marge: [18, 30], taille: 38, focus: true },
      ], ecart: 26 }],
      hasard: [{ puce: '🎲 un jeune choisi au hasard', couleur: 'ambre', id: 'hasard', taille: 52, margeH: 44, margeV: 20 }],
      tableau: [{ id: 'tab', focus: true, hauteurCase: 140, taille: 64, tailleEntete: 38, totaux: true, tableau: [
        [{ texte: 'Effectifs', taille: 28 }, { texte: '🚌 Bus', couleur: 'cyan' }, 'Autre moyen', 'Total'],
        [{ texte: '🎵 Musique', couleur: 'violet' }, { n: 105, id: 'v-mb' }, { n: 45, id: 'v-ma' }, { n: 150, id: 'v-mt' }],
        ['🎭 Théâtre', { n: 20, id: 'v-tb' }, { n: 80, id: 'v-ta' }, { n: 100, id: 'v-tt' }],
        ['Total', { n: 125, id: 'v-xb' }, { n: 125, id: 'v-xa' }, { n: 250, id: 'v-xx', couleur: 'ambre' }],
      ] }],
      bas: [{ pile: [
        { carte: '$105$ = **$105$ jeunes** qui vérifient les deux', couleur: 'ambre', id: 'bulle', taille: 40, align: 'gauche' },
        { carte: { ligne: [
          'le mot-clé', { texte: '« et »', id: 'et-mot', taille: 54, gras: true, couleur: 'ambre', nowrap: true },
          { texte: '⟶', taille: 70 }, { tex: '\\cap', taille: 70 }, { texte: 'intersection', doux: true, nowrap: true },
        ], ecart: 26 }, id: 'et', taille: 42, align: 'gauche' },
      ] }],
      panneau: [
        { carte: { ligne: [{ tex: 'P(M)=' }, { tex: '\\dfrac{\\cssId{n1}{150}}{\\cssId{d1}{250}}' }, { tex: '=', id: 'eq1' },
          { resultat: '$\\mathbf{0{,}6}$', couleur: 'violet', id: 'r1' }], ecart: 20 }, id: 'l1', h: 176, justifie: 'centre', marge: [14, 28], tailleTex: 56, focus: true },
        { carte: { ligne: [{ tex: 'P(B)=' }, { tex: '\\dfrac{\\cssId{n2}{125}}{\\cssId{d2}{250}}' }, { tex: '=', id: 'eq2' },
          { resultat: '$\\mathbf{0{,}5}$', couleur: 'cyan', id: 'r2' }], ecart: 20 }, id: 'l2', h: 176, justifie: 'centre', marge: [14, 28], tailleTex: 56, focus: true },
        { carte: { ligne: [{ tex: 'P(M\\cap B)=' }, { tex: '\\dfrac{\\cssId{n3}{105}}{\\cssId{d3}{250}}', id: 'f3' }, { tex: '=', id: 'eq3' },
          { resultat: '$\\mathbf{0{,}42}$', couleur: 'ambre', id: 'r3' }], ecart: 20 }, id: 'l3', h: 176, justifie: 'centre', marge: [14, 28], tailleTex: 56, focus: true },
      ],
    },
  ],

  gestes(C) {
    const ligneM = ['#tab-l1c0', '#tab-l1c1', '#tab-l1c2', '#tab-l1c3'];
    const colB = ['#tab-l0c1', '#tab-l1c1', '#tab-l2c1', '#tab-l3c1'];

    /* ---- 1. Titre : le décor de l'exercice (0 → 12,9 s) ---- */
    C.montre('#t-sur', 0.2);
    C.ecrit('#t-titre', 0.5, { dur: 1.1 });
    C.montre('#t-compteur', '#13');
    C.compte('#t-n', '#13', { de: 0, a: 250, dur: 1.4 });
    C.eclat('#t-n', '#15', { n: 26 });
    C.tombe('#p-mus', '#21-0.15', { couleur: '--violet' });
    C.tombe('#p-the', '#25-0.15', { couleur: '--rose' });
    C.montre('#p-sep', '#27');
    C.tombe('#p-bus', '#29-0.15', { couleur: '--cyan' });
    C.tombe('#p-aut', '#33-0.15', { couleur: '--ambre' });

    /* ---- 2. Expérience aléatoire et événements (13 → 22 s) ---- */
    C.montre('#b-lieu', '#35+0.4');
    C.tombe('#hasard', '#38', { hauteur: 180 });
    C.montre('#e-m', '#45');
    C.ecrit('#e-m-t', '#47', { dur: 1.2 });
    C.pulse('#e-m-l', '#46', { scale: 1.3 });
    C.montre('#e-b', '#54');
    C.ecrit('#e-b-t', '#56', { dur: 1.2 });
    C.pulse('#e-b-l', '#55', { scale: 1.3 });
    C.cache('#hasard', '#61');

    /* ---- 3. Le tableau croisé : les nombres tombent à leur place (22 → 41 s) ---- */
    C.montre('#tab', '#62', { dur: 0.8 });
    C.tombe(['#v-mb', '#v-ma', '#v-tb', '#v-ta'], '#70', { stagger: 0.28, couleur: '--cyan' });
    C.tombe(['#v-mt', '#v-tt', '#v-xb', '#v-xa'], '#72', { stagger: 0.28, couleur: '--violet' });
    C.tombe('#v-xx', '#76', { hauteur: 340, couleur: '--ambre' });
    C.eclat('#v-xx', '#76+0.5', { n: 16, force: 150 });
    // « chaque fois qu'on voit un nombre, c'est un nombre de jeunes »
    C.pointe('#v-mb', '#84');
    C.allume('#tab-l1c1', '#85', { couleur: '--ambre', jusque: '#100' });
    C.montre('#bulle', '#91');
    C.fleche('#bulle', '#v-mb', '#92', { couleur: '--ambre', courbure: -0.3, jusque: '#100' });
    C.cache('#bulle', '#100');
    C.pointe(null, '#100');

    /* ---- 4. Question 1 : P(M) (42 → 81 s) ---- */
    C.montre('#q1', '#104');
    C.montre('#l1', '#110');
    C.focus(['#e-m', '#tab', '#l1'], '#110');
    C.allume('#e-m', '#127', { couleur: '--violet', jusque: '#142' });
    C.allume(ligneM, '#142', { couleur: '--violet', jusque: '#193' });
    C.pointe('#v-mt', '#152');
    C.vole('#v-mt', '#n1', '#153', { couleur: '--violet' });
    C.allume('#tab-l3c3', '#160', { couleur: '--ambre', jusque: '#193' });
    C.pointe('#v-xx', '#160');
    C.vole('#v-xx', '#d1', '#172-0.4', { couleur: '--ambre' });
    C.pointe(null, '#178');
    C.montre('#eq1', '#187');
    C.tombe('#r1', '#191', { hauteur: 160, couleur: '--violet' });
    C.eclat('#r1', '#191+0.5');

    /* ---- 5. Question 1 : P(B) (82 → 107 s) ---- */
    C.montre('#l2', '#194');
    C.focus(['#e-b', '#tab', '#l1', '#l2'], '#194');
    C.allume(colB, '#208', { couleur: '--cyan', jusque: '#252' });
    C.pointe('#v-xb', '#217');
    C.pulse('#v-xb', '#224', { scale: 1.3 });
    C.vole('#v-xb', '#n2', '#227', { couleur: '--cyan' });
    C.allume('#tab-l3c3', '#233', { couleur: '--ambre', jusque: '#252' });
    C.pointe('#v-xx', '#233');
    C.vole('#v-xx', '#d2', '#235-0.2', { couleur: '--ambre' });
    C.pointe(null, '#242');
    C.montre('#eq2', '#246');
    C.tombe('#r2', '#250', { hauteur: 160, couleur: '--cyan' });
    C.eclat('#r2', '#250+0.5');

    /* ---- 6. Question 2 : P(M∩B) (107 → 168 s) ---- */
    C.remplace('#q1', '#q2', '#252');
    C.montre('#l3', '#256');
    C.focus(['#e-m', '#e-b', '#tab', '#l1', '#l2', '#l3'], '#256');
    C.allume(ligneM, '#260', { couleur: '--violet', jusque: '#290' });
    C.allume(colB, '#261+0.2', { couleur: '--cyan', jusque: '#290' });
    C.allume('#tab-l1c1', '#262', { couleur: '--ambre', jusque: '#290' });
    C.pulse('#v-mb', '#262+0.2', { scale: 1.35 });
    // « musique ET bus » : le mot-clé
    C.surligne('#e-m-t', '#284', { couleur: '--violet' });
    C.surligne('#e-b-t', '#287', { couleur: '--cyan' });
    C.montre('#et', '#298');
    C.pulse('#et-mot', '#301', { scale: 1.3 });
    C.onde('#et-mot', '#301', { couleur: '--ambre' });
    // le nombre de jeunes « bus ET musique »
    C.focus(['#tab', '#et', '#l3', '#l1', '#l2'], '#322');
    C.pointe('#v-mb', '#327');
    C.entoure('#tab-l1c1', '#333', { couleur: '--ambre' });
    C.vole('#v-mb', '#n3', '#344', { couleur: '--ambre' });
    C.allume('#tab-l3c3', '#355', { couleur: '--ambre', jusque: '#380' });
    C.pointe('#v-xx', '#355');
    C.vole('#v-xx', '#d3', '#365-0.3', { couleur: '--ambre' });
    C.pointe(null, '#371');
    C.pulse('#f3', '#377', { scale: 1.12 });
    C.montre('#eq3', '#384');
    C.tombe('#r3', '#388-0.2', { hauteur: 200, couleur: '--ambre' });
    C.eclat('#r3', '#388+0.35', { n: 34, force: 280 });
    C.encadre('#l3', '#389.fin', { couleur: '--ambre' });

    /* ---- 7. Récapitulatif (168 → fin) ---- */
    C.defocus('#389.fin');
    C.pulse(['#r1', '#r2', '#r3'], '#389.fin+0.4', { scale: 1.15 });
  },
});
