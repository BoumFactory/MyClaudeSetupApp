/* =====================================================================
   Texte riche du moteur canvas
   ---------------------------------------------------------------------
   Écriture d'un texte dans spec.js :
     'L\'angle $\\widehat{BAI}$ mesure $\\ambre{50^\\circ}$.'
     '**gras**'                       → gras
     '[alternes-internes]{#f1a .kw}'  → morceau visable par les gestes (id),
                                        classes : kw (mot-clé ambre gras), tt (gras, couleur de la carte),
                                        grad (dégradé du titre), gras, it, doux, ou un nom de couleur (violet…)
     decoupe: 'p' + 'Si deux | droites…' → morceaux p1, p2… (apparition morceau par morceau)
   Les espaces avant « : ; ! ? » et après « « » sont insécables.
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});

  /* ---------- analyse ---------- */
  let compteurSpan = 0;
  CV.analyserTexte = (src, decoupe) => {
    let s = String(src);
    if (decoupe) s = s.split(/\s*\|\s*/).map((x, i) => '[' + x + ']{#' + decoupe + (i + 1) + '}').join(' ');
    const atomes = [];
    const spans = [];   // { id, classes, parent }
    const lire = (s, style, pile) => {
      let mot = '';
      const finMot = () => { if (mot) { atomes.push({ k: 'mot', s: mot, st: style, spans: pile }); mot = ''; } };
      for (let i = 0; i < s.length; i++) {
        const c = s[i];
        if (c === '\\' && s[i + 1] === '$') { mot += '$'; i++; continue; }
        if (c === '$') {
          const j = s.indexOf('$', i + 1);
          if (j < 0) { mot += c; continue; }
          finMot();
          atomes.push({ k: 'tex', tex: s.slice(i + 1, j), st: style, spans: pile });
          i = j; continue;
        }
        if (c === '*' && s[i + 1] === '*') {
          const j = s.indexOf('**', i + 2);
          if (j < 0) { mot += c; continue; }
          finMot();
          lire(s.slice(i + 2, j), Object.assign({}, style, { gras: true }), pile);
          i = j + 1; continue;
        }
        if (c === '[') {
          // [contenu]{#id .classe} — crochets imbriqués permis
          let prof = 1, j = i + 1;
          for (; j < s.length && prof; j++) { if (s[j] === '[') prof++; else if (s[j] === ']') prof--; }
          const fin = j - 1;
          if (prof === 0 && s[j] === '{') {
            const k = s.indexOf('}', j);
            if (k > 0) {
              finMot();
              const attrs = s.slice(j + 1, k).trim().split(/\s+/).filter(Boolean);
              const id = (attrs.find(a => a[0] === '#') || '').slice(1) || null;
              const classes = attrs.filter(a => a[0] === '.').map(a => a.slice(1));
              const st = Object.assign({}, style);
              for (const cl of classes) {
                if (cl === 'kw') { st.gras = true; st.coul = 'ambre'; }
                else if (cl === 'tt') { st.gras = true; st.coul = 'accent-carte'; }
                else if (cl === 'acc') { st.gras = true; st.coul = '#ff1493'; }   // \acc{…} de bfcours
                else if (cl === 'gras') st.gras = true;
                else if (cl === 'it') st.it = true;
                else if (cl === 'doux') st.coul = 'doux';
                else if (cl === 'grad') st.grad = ++compteurSpan;
                else if (CV.NOMS_COULEURS.includes(cl)) st.coul = cl;
              }
              let p = pile;
              if (id) { spans.push({ id, classes, parent: pile.length ? pile[pile.length - 1] : null }); p = pile.concat(id); }
              lire(s.slice(i + 1, fin), st, p);
              i = k; continue;
            }
          }
          mot += c; continue;
        }
        if (c === '\n') {   // retour à la ligne forcé
          finMot();
          while (atomes.length && atomes[atomes.length - 1].k === 'esp') atomes.pop();
          atomes.push({ k: 'br', st: style, spans: pile });
          continue;
        }
        if (/\s/.test(c)) {
          finMot();
          if (atomes.length && atomes[atomes.length - 1].k === 'br') continue;
          if (atomes.length && atomes[atomes.length - 1].k !== 'esp') atomes.push({ k: 'esp', st: style, spans: pile });
          continue;
        }
        mot += c;
      }
      finMot();
    };
    lire(s, {}, []);
    while (atomes.length && atomes[0].k === 'esp') atomes.shift();
    while (atomes.length && atomes[atomes.length - 1].k === 'esp') atomes.pop();
    // espaces insécables (typographie française)
    for (let i = 1; i < atomes.length - 1; i++) {
      const a = atomes[i];
      if (a.k !== 'esp') continue;
      const suiv = atomes[i + 1], prec = atomes[i - 1];
      if ((suiv.k === 'mot' && /^[:;!?»]/.test(suiv.s)) || (prec.k === 'mot' && /«$/.test(prec.s))) a.insec = true;
    }
    return { atomes, spans, decoupe: decoupe || null };
  };

  /* ---------- police ---------- */
  // st.tab : chiffres tabulaires (font-variant-numeric: tabular-nums du moteur HTML : .cv-case, .cv-vol, compteurs),
  // famille AtkinsonT = même police avec la fonction « tnum » (voir chargerPolices)
  CV.police = (taille, st) => (st.it ? 'italic ' : '') + (st.gras ? '700 ' : '400 ') + taille.toFixed(2)
    + (st.tab ? 'px AtkinsonT, Atkinson, "Segoe UI", sans-serif' : 'px Atkinson, "Segoe UI", sans-serif');

  let ctxMesure = null;
  const mesureur = () => ctxMesure || (ctxMesure = new OffscreenCanvas(8, 8).getContext('2d'));
  const cacheLargeur = new Map();
  CV.largeurTexte = (s, police, espacement = 0) => {
    const cle = police + '|' + espacement + '|' + s;
    let w = cacheLargeur.get(cle);
    if (w === undefined) {
      const c = mesureur();
      c.font = police;
      c.letterSpacing = espacement + 'px';
      w = c.measureText(s).width;
      cacheLargeur.set(cle, w);
    }
    return w;
  };
  const cacheMetriques = new Map();
  CV.metriques = police => {
    let m = cacheMetriques.get(police);
    if (!m) {
      const c = mesureur();
      c.font = police; c.letterSpacing = '0px';
      const r = c.measureText('Hgéq');
      m = { asc: r.fontBoundingBoxAscent, desc: r.fontBoundingBoxDescent };
      cacheMetriques.set(police, m);
    }
    return m;
  };

  /* ---------- mise en lignes ----------
     o : { taille, interligne, tailleTex, nowrap, espacement, majuscules, formule(tex) → données MathJax }
     Renvoie { lignes: [{ y (ligne de base depuis le haut), w, items: [{ a, x, w }] }], w, h, deborde } */
  CV.composerTexte = (analyse, largeurMax, o) => {
    const taille = o.taille, lh = o.interligne || 1.3, tt = taille * (o.tailleTex || 1.1);
    const esp = o.espacement || 0;
    const boites = analyse.atomes.map(a => {
      if (a.k === 'tex') {
        const f = o.formule(a.tex);
        return { a, w: f.w * tt, asc: Math.max(f.asc, 0.7) * tt, desc: Math.max(f.desc, 0.2) * tt, f, tt };
      }
      if (a.k === 'br') return { a, w: 0, br: true };
      const police = CV.police(taille, a.st);
      if (a.k === 'esp') return { a, w: CV.largeurTexte(' ', police, esp), police, esp: true };
      const s = o.majuscules ? a.s.toUpperCase() : a.s;
      return { a, s, w: CV.largeurTexte(s, police, esp), police };
    });
    // morceaux de `decoupe` : insécables comme des inline-block, sauf s'ils sont plus larges que la ligne
    const colle = new Set();
    if (analyse.decoupe) {
      const larg = {};
      boites.forEach(b => { const id = b.a.spans[0]; if (id) larg[id] = (larg[id] || 0) + b.w; });
      boites.forEach((b, i) => {
        if (!b.esp) return;
        const p = boites[i - 1], s = boites[i + 1], id = p && p.a.spans[0];
        if (id && s && s.a.spans[0] === id && larg[id] <= largeurMax) colle.add(b);
      });
    }
    // mots insécables : un « mot » = suite d'atomes sans espace sécable
    const groupes = [];
    let g = [];
    for (const b of boites) {
      if (b.br) { if (g.length) groupes.push(g); groupes.push([b]); g = []; continue; }
      if (b.esp && !b.a.insec && !colle.has(b)) { if (g.length) groupes.push(g); groupes.push([b]); g = []; }
      else g.push(b);
    }
    if (g.length) groupes.push(g);
    const lignes = [];
    let cour = [], wc = 0, deborde = false;
    const pousser = () => {
      while (cour.length && cour[cour.length - 1].esp) { wc -= cour[cour.length - 1].w; cour.pop(); }
      lignes.push({ items: cour, w: wc });
      cour = []; wc = 0;
    };
    for (const gr of groupes) {
      const wg = gr.reduce((s, b) => s + b.w, 0);
      if (gr.length === 1 && gr[0].br) { pousser(); continue; }
      const estEsp = gr.length === 1 && gr[0].esp;
      if (estEsp) { if (cour.length) { cour.push(gr[0]); wc += wg; } continue; }
      if (!o.nowrap && cour.length && wc + wg > largeurMax + 0.01) pousser();
      for (const b of gr) { cour.push(b); wc += b.w; }
      if (wc > largeurMax + 0.5) deborde = true;
    }
    if (cour.length || !lignes.length) pousser();
    // hauteur de chaque ligne : modèle CSS (demi-interlignage autour du texte, formules en boîtes)
    let y = 0, wMax = 0;
    for (const L of lignes) {
      let haut = 0, bas = 0;
      const m = CV.metriques(CV.police(taille, {}));
      const demi = (taille * lh - (m.asc + m.desc)) / 2;
      haut = m.asc + demi; bas = m.desc + demi;
      let x = 0;
      for (const b of L.items) {
        if (b.f) { haut = Math.max(haut, b.asc); bas = Math.max(bas, b.desc); }
        b.x = x; x += b.w;
      }
      L.y = y + haut; L.haut = haut; L.bas = bas;
      y += haut + bas;
      wMax = Math.max(wMax, L.w);
    }
    return { lignes, w: wMax, h: y, deborde, taille, espacement: esp, majuscules: !!o.majuscules };
  };
})(typeof self !== 'undefined' ? self : this);
