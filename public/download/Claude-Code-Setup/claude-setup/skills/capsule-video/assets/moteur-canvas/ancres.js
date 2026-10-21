/* =====================================================================
   Ancres de temps — module commun (page, aperçu et workers)
   ---------------------------------------------------------------------
   Code de résolution repris TEL QUEL de assets/gabarit/moteur/capsule.js
   (C.hasard, C.W, C.cherche, C.tempsFort, C.temps) : mêmes écritures,
   mêmes sens, mêmes messages d'erreur. Seule l'enveloppe change : une
   fabrique qui reçoit le transcript, les temps forts et la fonction
   d'erreur, pour fonctionner aussi dans un worker (sans window).
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});

  CV.ancres = function (T, TF, erreur) {
    const C = {};
    T = T || { mots: [], segments: [], duree: 10 };
    TF = TF || [];

    /* ---------- hasard déterministe ---------- */
    C.hasard = (graine = 1) => {
      let a = graine >>> 0;
      return () => {
        a |= 0; a = (a + 0x6d2b79f5) | 0;
        let x = Math.imul(a ^ (a >>> 15), 1 | a);
        x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
        return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
      };
    };

    /* ---------- ancrage sur les mots ---------- */
    const norm = s => String(s).toLowerCase().normalize('NFD')
      .replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9,]/g, '').replace(/^,+|,+$/g, '');

    C.W = (i, cote = 'debut') => {
      const m = T.mots[i];
      if (!m) { erreur('Mot #' + i + ' inexistant (' + T.mots.length + ' mots)'); return 0; }
      return cote === 'fin' ? m.fin : m.debut;
    };

    /* occurrence n° occ (1, 2…) de la suite de mots « texte » entre les instants apres et avant */
    C.cherche = (texte, apres = 0, cote = 'debut', avant = Infinity, occ = 1) => {
      const cible = String(texte).split(/\s+/).map(norm).filter(Boolean);
      const mots = T.mots;
      let vu = 0;
      for (let k = 0; k < mots.length; k++) {
        if (mots[k].debut < apres - 0.05) continue;
        if (mots[k].debut > avant + 0.05) break;
        let ok = true;
        for (let j = 0; j < cible.length; j++) {
          if (!mots[k + j] || norm(mots[k + j].mot) !== cible[j]) { ok = false; break; }
        }
        if (ok && ++vu === occ) return cote === 'fin' ? mots[k + cible.length - 1].fin : mots[k].debut;
      }
      erreur('Mot introuvable : « ' + texte + ' » entre ' + apres + ' et ' + avant + ' s');
      return apres;
    };

    /* Temps forts d'un script synthétisé (voix.py → data/temps-forts.js) */
    C.tempsFort = id => {
      const b = TF.find(x => x.id === id);
      if (!b) erreur('Temps fort inconnu : ' + id + (TF.length ? '' : ' (data/temps-forts.js absent)'));
      return b || { debut: 0, fin: 0 };
    };

    /* Spécification de temps :
       12.5 | '#147' | '#147+0.3' | '#147.fin' | '#147.fin-0.2' | '"150"@60'
       '@b10' (début du temps fort b10) | '@b10.fin' | '@b10~"fait"' (mot « fait » dans b10)
       '@b10~"fait"2' (2e occurrence) | '@b10~"ça fait".fin+0.1' */
    C.temps = spec => {
      if (typeof spec === 'number') return spec;
      const s = String(spec).trim();
      let m = s.match(/^@([\w-]+)(?:~"([^"]+)"(\d+)?)?(\.fin)?([+-][\d.]+)?$/);
      if (m) {
        const b = C.tempsFort(m[1]);
        const dec = m[5] ? parseFloat(m[5]) : 0;
        if (!m[2]) return (m[4] ? b.fin : b.debut) + dec;
        const occ = m[3] ? +m[3] : 1, cote = m[4] ? 'fin' : 'debut';
        // 1) mots EXACTS du script, horodatés par alignement (aligner.py) ; 2) repli : transcription brute
        if (b.mots && b.mots.length) {
          const cible = m[2].split(/[\s'’]+/).map(norm).filter(Boolean);
          let vu = 0;
          for (let k = 0; k + cible.length <= b.mots.length; k++) {
            if (cible.every((c, j) => norm(b.mots[k + j].mot) === c) && ++vu === occ)
              return (cote === 'fin' ? b.mots[k + cible.length - 1].fin : b.mots[k].debut) + dec;
          }
        }
        return C.cherche(m[2], b.debut, cote, b.fin, occ) + dec;
      }
      m = s.match(/^#(\d+)(\.fin)?([+-][\d.]+)?$/);
      if (m) return C.W(+m[1], m[2] ? 'fin' : 'debut') + (m[3] ? parseFloat(m[3]) : 0);
      m = s.match(/^"(.+)"(?:@([\d.]+))?([+-][\d.]+)?$/);
      if (m) return C.cherche(m[1], m[2] ? +m[2] : 0) + (m[3] ? parseFloat(m[3]) : 0);
      const n = parseFloat(s);
      if (!isNaN(n)) return n;
      erreur('Spécification de temps illisible : ' + s);
      return 0;
    };

    return C;
  };
})(typeof self !== 'undefined' ? self : this);
