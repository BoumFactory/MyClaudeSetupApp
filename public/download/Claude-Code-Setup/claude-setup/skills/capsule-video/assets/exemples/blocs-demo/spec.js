/* Plugin blocs (code, terminal, compile) : chargé à côté du moteur, voir references/bloc-code.md */
(function(){var b;try{b=document.currentScript.src.replace(/[^\/]*$/,'')+'plugins-canvas/';}catch(e){b='/plugins-canvas/';}self.PLUG_BASE=b;if(typeof importScripts==='function'){importScripts(b+'blocs.js');}else{document.write('<script src="'+b+'blocs.js"><\/script>');}})();
/* Démonstration des blocs « tutoriel logiciel » : code qui s'écrit, terminal, compilation, voix mixtes.
   Le professeur (voix enregistrée, ici simulée) et Claude (Piper tom) écrivent un cours Typst à tour de rôle.
   Référence : references/bloc-code.md et references/voix-mixtes.md. */
CAPSULE({
  titre: 'Démo blocs code',
  audio: 'audio.wav', theme: 'nuit', ambiance: true,   // pas de `mention` : le badge n'apparaît que pendant les passages de Claude

  scenes: [
    { id: 's-titre', gabarit: 'titre', debut: 0,
      haut: [
        { surTitre: 'Tutoriel logiciel', id: 't-sur', montre: 0.2 },
        { titre: 'Écrire un cours en [Typst]{.grad}', id: 't-titre', ecrit: '@b01+0.2' },
      ],
      centre: [
        { carte: 'Le professeur parle, **Claude** tape le code : deux voix, un seul fichier.', couleur: 'cyan',
          id: 't-carte', taille: 50, montre: '@b01~"cours"' },
      ] },

    { id: 's-main', gabarit: 'code-terminal-rendu', debut: '@b02-0.3',
      bandeau: [{ puce: 'Écrire · compiler · voir', couleur: 'cyan', id: 'bd', taille: 36, montre: '@b02-0.1' }],
      code: [{
        id: 'ed', fichier: 'cours.typ', langage: 'typst', h: 590, taille: 36, montre: '@b02-0.2',
        code: `
          #set page(width: 10cm, height: 6cm)
          #set text(lang: "fr", size: 16pt)

          = Fonctions affines

          $ f(x) = 2 x + 1 $
        `,
        // frappe calée sur les mots : chaque segment s'écrit entre deux ancres
        frappe: [
          { lignes: [1, 2], de: '@b02+0.2', a: '@b02~"langue".fin+0.1' },
          { lignes: [3, 4], de: '@b03~"signe"', a: '@b03.fin' },
          { lignes: [5, 6], de: '@b04~"dollars".fin', a: '@b04~"un".fin' },
        ],
        surlignage: [
          { lignes: 2, de: '@b02~"langue"-0.1', jusque: '@b02.fin' },
          { lignes: 4, de: '@b03~"titre"', jusque: '@b04-0.2' },
          { lignes: 6, de: '@b04~"formule"', jusque: '@b05' },
        ],
      }],
      terminal: [{
        id: 'term', montre: '@b05-0.6', h: 282, taille: 30,
        terminal: [
          { cmd: 'typst compile cours.typ', de: '@b05~"je"', a: '@b06~"terminal".fin' },
          { sortie: 'Compilation de cours.typ…', t: '@b06~"confirme"' },
          { ok: 'cours.pdf prêt en 0,4 s', t: '@b06~"fichier"' },
        ],
      }],
      zones: {},
      rendu: { valign: 'centre', contenu: [{ pile: [
        { carte: { texte: 'Le rendu du PDF apparaîtra ici', doux: true, taille: 40 }, couleur: 'violet', id: 'attente',
          alignEnfants: 'centre', justifie: 'centre', h: 500, montre: '@b02+0.4' },
        { image: 'rendu-cours.png', id: 'rendu', cadre: true, ajuste: 'contenir', l: 750 },
      ] }] },
    },
  ],

  gestes(C) {
    C.badgeVoix({ voix: 'tom', texte: 'Voix de synthèse' });
    // flash vert, coche, puis le rendu remplace l'attente et zoome sur la formule
    C.compile('#ed', '@b06~"fichier"', { rendu: '#rendu', remplace: '#attente', zoom: { a: 1.3, fx: 0.3, fy: 0.5, dur: 2.2 } });
  },
});
