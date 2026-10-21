/* Capsule « moteur canvas » : tout le contenu est ici (données + gestes). Référence : references/moteur-canvas.md.
   Exemple complet : <dossier_capsules>/labomaths-edge-canvas/spec.js */
CAPSULE({
  titre: 'Titre de la capsule',
  audio: 'audio.wav', theme: 'nuit', ambiance: true, mention: 'Voix de synthèse',
  formules: 'grandes',   // 'grandes' | 'compactes' (préférence de l'utilisateur), surchargeable par scène ; ni tailleTex ni taille en dur
  macros: { AB: '\\violet{\\overrightarrow{AB}}' },   // \AB dans toutes les formules

  scenes: [
    { id: 's-titre', gabarit: 'titre', debut: 0,
      haut: [
        { surTitre: "Correction d'exercice", id: 't-sur', montre: 0.2 },
        { titre: 'Titre [de la capsule]{.grad}', id: 't-titre', ecrit: '@b01+0.3' },
      ],
      centre: [
        { carte: 'Objectif : …', couleur: 'vert', id: 't-obj', taille: 50, montre: '@b01.fin-0.5' },
      ] },

    { id: 's-main', gabarit: 'figure-panneau', debut: '@b02-0.3',
      bandeau: { valign: 'centre', contenu: [{ pile: [
        { puce: 'Question 1', couleur: 'rose', id: 'q1', taille: 38 },
      ] }] },
      figure: [{ id: 'fig', l: 960, h: 500, figure: { vue: [0, 0, 960, 500],
        points: { A: [200, 400], B: [760, 120] },
        objets: [
          { id: 'ab', segment: ['A', 'B'], couleur: 'violet', epaisseur: 6 },
          { id: 'lA', etiquette: 'A', en: [180, 440] }, { id: 'lB', etiquette: 'B', en: [790, 100] },
        ] } }],
      panneau: [
        { carte: 'Calculer les coordonnées du vecteur $\\AB$.', couleur: 'rose', id: 'enonce', taille: 46 },
        { carte: { calcul: [
          [{ tex: '\\AB', id: 'c1g' }, { tex: '=', id: 'c1e' }, '\\begin{pmatrix} \\cssId{x}{6} \\\\ \\cssId{y}{-4} \\end{pmatrix}'],
        ] }, couleur: 'ambre', id: 'calc' },
      ] },
  ],

  gestes(C) {
    C.montre('#q1', '@b02-0.1');
    C.trace('#ab', '@b02~"segment"', 0.8);
    C.montre(['#lA', '#lB'], '@b02~"segment"+0.6', { stagger: 0.2 });
    C.montre('#enonce', '@b03-0.2');
    C.montre(['#calc', '#c1g', '#c1e'], '@b04-0.2');
    C.tombe('#x', '@b04~"6"-0.15');
    C.tombe('#y', '@b04~"4"-0.15');
    C.encadre('#calc', '@b04.fin', { jusque: '@b05-0.4' });
  },
});
