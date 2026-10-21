/* Démonstration des tuiles algébriques (36 s, sans voix : gestes calés sur des secondes brutes).
   1. (−3) + (+2) : deux paires nulles s'annulent une à une   2. l'opposé : les tuiles se retournent
   3. rectangle produit 2 × (x + 3)                            4. tapis d'équation x + 2 = 5
   Référence : references/moteur-canvas.md § Tuiles algébriques et references/gestes.md § Tuiles.
   Pour une vraie capsule : remplacer les secondes par des ancres '@b03~"mot"' (voie B). */
CAPSULE({
  titre: 'Tuiles algébriques — démonstration',
  audio: 'audio.wav', theme: 'jour', ambiance: true,
  // couleurs et proportions des tuiles (facultatif ; valeurs par défaut : un jaune, x vert, x² bleu, négatif rouge, x/u = 3,2) :
  // tuiles: { couleurs: { un: '#ffd21f', x: '#d6249f', x2: '#2fb34a', negatif: '#e5322d' }, rapportX: 5.6 },

  scenes: [
    /* ===== 1. (−3) + (+2) ===== */
    { id: 'sc1', gabarit: 'colonne', debut: 0,
      zones: { centre: { x: 90, y: 150, l: 1740, h: 880 } },
      bandeau: [{ puce: '1 · Additionner des relatifs', couleur: 'cyan', id: 'b1', taille: 38 }],
      centre: { valign: 'centre', ecart: 70, align: 'centre', contenu: [
        { tex: '(-3)+(+2)=\\cssId{r1}{-1}', taille: 120, id: 'e1' },
        { tuiles: '-3 +2', id: 'a', taille: 140, ecart: 20 },
        { texte: 'Une tuile jaune et une tuile rouge forment une **paire nulle**.', taille: 44, id: 't1', align: 'centre' },
      ] } },

    /* ===== 2. L'opposé ===== */
    { id: 'sc2', gabarit: 'colonne', debut: 9.5,
      zones: { centre: { x: 90, y: 150, l: 1740, h: 880 } },
      bandeau: [{ puce: '2 · L’opposé', couleur: 'violet', id: 'b2', taille: 38 }],
      centre: { valign: 'centre', ecart: 70, align: 'centre', contenu: [
        { tex: '-(+2)=\\cssId{r2}{-2}', taille: 120, id: 'e2' },
        { tuiles: '2', id: 'o', taille: 170, ecart: 26 },
        { texte: 'Retourner une tuile, c’est prendre son **opposé**.', taille: 44, id: 't2', align: 'centre' },
      ] } },

    /* ===== 3. Rectangle produit ===== */
    { id: 'sc3', gabarit: 'colonne', debut: 17,
      zones: { centre: { x: 90, y: 150, l: 1740, h: 880 } },
      bandeau: [{ puce: '3 · Développer', couleur: 'rose', id: 'b3', taille: 38 }],
      centre: { valign: 'centre', ecart: 40, align: 'centre', contenu: [{ ligne: [
        { produit: { haut: 'x +3', gauche: '2' }, id: 'p', taille: 112 },
        { colonne: [
          { tex: '2(x+3)=\\cssId{s1}{2x}+\\cssId{s2}{6}', taille: 84, id: 'e3' },
          { texte: 'La largeur **2**, la longueur **x + 3**.', taille: 40, id: 't3' },
        ], ecart: 34, align: 'centre' },
      ], ecart: 110, valign: 'centre' }] } },

    /* ===== 4. Tapis d'équation ===== */
    { id: 'sc4', gabarit: 'colonne', debut: 27.5,
      zones: { centre: { x: 90, y: 150, l: 1740, h: 880 } },
      bandeau: [{ puce: '4 · Résoudre x + 2 = 5', couleur: 'vert', id: 'b4', taille: 38 }],
      centre: { valign: 'centre', ecart: 50, align: 'centre', contenu: [
        { tapis: { gauche: 'x +2', droite: '5' }, id: 'm', taille: 120, l: 1560, hMin: 380 },
        { resultat: '$x=3$', couleur: 'vert', id: 'rx', taille: 90 },
      ] } },
  ],

  gestes(C) {
    /* --- 1 --- */
    C.montre('#e1', 0.6); C.montre('#b1', 0.3);
    C.montre('.a-tuiles', 1.3, { stagger: 0.18 });
    C.montre('#t1', 2.8);
    C.annule('#a-1', '#a-4', 4.2, { zero: true });
    C.annule('#a-2', '#a-5', 5.9, { zero: true });
    C.allume('#a-3', 7.5, { couleur: '--rose', jusque: 9 });
    C.montre('#r1', 7.6); C.pulse('#a-3', 7.6);

    /* --- 2 --- */
    C.montre('#e2', 10.0);
    C.montre('.o-tuiles', 10.6, { stagger: 0.2 });
    C.montre('#t2', 11.4);
    C.retourne('.o-tuiles', 12.6, { stagger: 0.25, onde: true });
    C.montre('#r2', 14.2);

    /* --- 3 --- */
    C.montre('#e3', 17.6);
    C.montre('.p-haut', 18.2, { stagger: 0.2 });
    C.montre('.p-gauche', 19.2, { stagger: 0.2 });
    C.montre('#t3', 19.8);
    C.montre('.p-produits', 21.0, { stagger: 0.3 });
    C.allume(['#p-l1c1', '#p-l2c1'], 24.0, { couleur: '--vert', jusque: 25.6 });
    C.montre('#s1', 24.0);
    C.allume(['#p-l1c2', '#p-l1c3', '#p-l1c4', '#p-l2c2', '#p-l2c3', '#p-l2c4'], 25.6, { couleur: '--ambre', jusque: 27.2 });
    C.montre('#s2', 25.6);

    /* --- 4 --- */
    C.montre('#m', 28.0);
    C.montre('.m-g-tuiles', 28.8, { stagger: 0.15 });
    C.montre('.m-d-tuiles', 29.4, { stagger: 0.15 });
    C.deplace(['#m-g-2', '#m-g-3', '#m-d-1', '#m-d-2'], { dx: 0, dy: -330 }, 31.4, { stagger: 0.12, dur: 0.7, rebond: false });
    C.cache(['#m-g-2', '#m-g-3', '#m-d-1', '#m-d-2'], 32.3, { stagger: 0.12, dur: 0.3 });
    C.pulse('#m-g-1', 33.4);
    C.tombe('#rx', 33.6);
  },
});
