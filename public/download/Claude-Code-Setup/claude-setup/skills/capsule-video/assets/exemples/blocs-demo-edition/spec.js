/* Plugin blocs (code, terminal, compile) : chargé à côté du moteur, voir references/bloc-code.md */
(function(){var b;try{b=document.currentScript.src.replace(/[^\/]*$/,'')+'plugins-canvas/';}catch(e){b='/plugins-canvas/';}self.PLUG_BASE=b;if(typeof importScripts==='function'){importScripts(b+'blocs.js');}else{document.write('<script src="'+b+'blocs.js"><\/script>');}})();
/* Démonstration de l'ÉDITION du code sur place : remplace, efface, insere, et compile qui change l'image de rendu.
   Cas du tutoriel Typst : dans #setbfsocle(correction-color: "prop"), prop → monrose → red → prop, chaque fois calé sur un mot,
   suivi d'une compilation dont le rendu (3 PNG différents) se fond dans le précédent.
   Référence : references/bloc-code.md (section « Éditer le code »). */
CAPSULE({
  titre: 'Démo édition de code',
  audio: 'audio.wav', theme: 'nuit', ambiance: true, mention: 'Voix de synthèse',

  scenes: [
    { id: 's-main', gabarit: 'code-rendu', debut: 0,
      bandeau: [{ puce: 'Modifier le code sur place', couleur: 'cyan', id: 'bd', taille: 36, montre: 0.1 }],
      code: [{
        id: 'ed', fichier: 'cours.typ', langage: 'typst', h: 520, taille: 36, montre: 0.1,
        code: `
          #import "@local/bfcours-typst:0.1.0": *
          // à régler
          #setbfsocle(correction-color: "prop")

          = Fonctions affines
        `,
        // texte attendu à la fin des gestes : le rendu s'arrête avec un message si l'affichage diffère
        attendu: `
          #import "@local/bfcours-typst:0.1.0": *
          #setbfsocle(correction-color: "prop")
          #set text(lang: "fr")

          = Fonctions affines
        `,
      }],
      zones: {},
      rendu: { valign: 'centre', contenu: [{ pile: [
        { image: 'rendu-prop.png', id: 'r0', cadre: true, ajuste: 'contenir', l: 750, montre: 0.3 },
        { image: 'rendu-monrose.png', id: 'r1', cadre: true, ajuste: 'contenir', l: 750 },
        { image: 'rendu-red.png', id: 'r2', cadre: true, ajuste: 'contenir', l: 750 },
        { image: 'rendu-prop.png', id: 'r3', cadre: true, ajuste: 'contenir', l: 750 },
      ] }] },
    },
  ],

  gestes(C) {
    // une ligne s'ouvre au milieu du code (lignes suivantes décalées) : après la ligne 3
    C.insere('#ed', 0.35, { apres: 3, code: '#set text(lang: "fr")' });

    // prop → monrose : effacement lettre à lettre au curseur, puis frappe ; compilation, rendu rose en fondu
    C.remplace('#ed', '@b01~"abord"', { ligne: 3, ancien: 'prop', par: 'monrose', a: '@b01~"rose".fin' });
    C.compile('#ed', '@b01.fin+0.05', { rendu: '#r1', remplace: '#r0', fondu: true });

    // monrose → red : sélection bleue visible, puis frappe
    C.remplace('#ed', '@b02~"ensuite"', { ligne: 3, ancien: 'monrose', par: 'red', mode: 'selection', a: '@b02~"rouge".fin-0.1' });
    C.compile('#ed', '@b02.fin+0.05', { rendu: '#r2', remplace: '#r1', fondu: true });

    // la ligne de commentaire (ligne 2) se replie : la ligne à régler devient la ligne 2 AFFICHÉE
    C.efface('#ed', '@b03~"on"', { lignes: 2 });
    C.remplace('#ed', '@b03~"revient"', { ligne: 2, ancien: 'red', par: 'prop', a: '@b03~"valeur".fin' });
    C.compile('#ed', '@b03~"départ"', { rendu: '#r3', remplace: '#r2', fondu: true });

    // contrôle : à la fin, le texte affiché est exactement celui-ci
    C.verifieCode('#ed', 8.2, `
      #import "@local/bfcours-typst:0.1.0": *
      #setbfsocle(correction-color: "prop")
      #set text(lang: "fr")

      = Fonctions affines
    `);
  },
});
