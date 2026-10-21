/* =====================================================================
   Préparation : formules MathJax (sortie SVG) et longueurs de tracés
   ---------------------------------------------------------------------
   Deux fournisseurs, même interface { formule(tex, display), chemin(d) } :
   - CV.PrepDOM (page principale ou aperçu : a un DOM et MathJax) calcule
     tout et remplit une TABLE sérialisable ;
   - CV.PrepTable (workers) relit cette table, sans DOM ni MathJax.
   Une formule devient une liste d'opérations de dessin (chemins Path2D,
   rectangles, textes) en unités em, ligne de base en y = 0, y vers le
   bas, plus la boîte de chaque sous-partie marquée \cssId{id}{…} ou
   \class{nom}{…} : `vole`, `allume`, `entoure` visent ainsi un nombre
   précis dans une formule.
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});

  /* Macros par défaut. Parallélisme : toujours « // » (règle fixe de references/rigueur.md) ;
     \para et \parallel donnent tous deux « // ». */
  CV.MACROS_PAR_DEFAUT = {
    para: '\\mathrel{/\\mkern-4mu/}',
    parallel: '\\mathrel{/\\mkern-4mu/}',
  };

  /* Macros de couleur du thème : \violet{x}, \textcolor{ambre}{x}, \color{cyan}
     + macros propres à la capsule (spec.macros : { BAC: '\\cyan{\\widehat{BAC}}' } → \BAC). */
  CV.pretraiterTex = (tex, theme, macros) => {
    let s = String(tex);
    const noms = Object.keys(macros || {}).sort((a, b) => b.length - a.length);
    for (let passe = 0; passe < 5 && noms.length; passe++) {
      let change = false;
      for (const n of noms) {
        const re = new RegExp('\\\\' + n + '(?![A-Za-z])', 'g');
        if (re.test(s)) { s = s.replace(re, () => '{' + macros[n] + '}'); change = true; }
      }
      if (!change) break;
    }
    // macros par défaut (non entourées d'accolades : la relation garde son espacement)
    for (const [n, v] of Object.entries(CV.MACROS_PAR_DEFAUT)) {
      if (macros && macros[n] !== undefined) continue;
      s = s.replace(new RegExp('\\\\' + n + '(?![A-Za-z])', 'g'), () => v);
    }
    for (const n of CV.NOMS_COULEURS) {
      const hex = theme[n];
      s = s.replace(new RegExp('\\\\' + n + '\\{', 'g'), '\\textcolor{' + hex + '}{');
      s = s.replace(new RegExp('\\\\(textcolor|color)\\{' + n + '\\}', 'g'), '\\$1{' + hex + '}');
    }
    return s;
  };

  CV.cleFormule = (tex, display) => (display ? 'D:' : 'I:') + tex;

  /* ---------- page principale : MathJax + SVG ---------- */
  CV.PrepDOM = function (theme, macros) {
    const table = { formules: {}, longueurs: {} };
    this.table = table;
    const NS = 'http://www.w3.org/2000/svg';
    const boite = document.createElement('div');
    boite.style.cssText = 'position:absolute;left:-10000px;top:0;visibility:hidden;font-size:100px';
    document.body.appendChild(boite);
    const svgL = document.createElementNS(NS, 'svg');
    boite.appendChild(svgL);
    const cheminL = document.createElementNS(NS, 'path');
    svgL.appendChild(cheminL);

    /* longueur et boîte d'un chemin SVG : { l, x, y, w, h } */
    this.chemin = d => {
      if (table.longueurs[d] !== undefined) return table.longueurs[d];
      cheminL.setAttribute('d', d);
      let r = { l: 0, x: 0, y: 0, w: 0, h: 0 };
      try {
        const bb = cheminL.getBBox();
        r = { l: +cheminL.getTotalLength().toFixed(3), x: +bb.x.toFixed(2), y: +bb.y.toFixed(2),
          w: +bb.width.toFixed(2), h: +bb.height.toFixed(2) };
      } catch (e) { /* chemin illisible : longueur nulle */ }
      table.longueurs[d] = r;
      return r;
    };

    const mult = (A, B) => [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1],
      A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3],
      A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]];
    const matriceDe = el => {
      const l = el.transform && el.transform.baseVal;
      if (!l || !l.numberOfItems) return null;
      const m = l.consolidate().matrix;
      return [m.a, m.b, m.c, m.d, m.e, m.f];
    };
    const applique = (M, x, y) => [M[0] * x + M[2] * y + M[4], M[1] * x + M[3] * y + M[5]];
    const r3 = v => Math.round(v * 1e5) / 1e5;

    this.formule = (tex, display = false) => {
      const cle = CV.cleFormule(tex, display);
      if (table.formules[cle]) return table.formules[cle];
      const src = CV.pretraiterTex(tex, theme, macros);
      let res;
      try {
        const conteneur = MathJax.tex2svg(src, { display });
        boite.appendChild(conteneur);
        const svg = conteneur.querySelector('svg');
        const err = svg.querySelector('[data-mjx-error]');
        const vb = svg.viewBox.baseVal;
        const ops = [], parts = {};
        const S = [0.001, 0, 0, 0.001, 0, 0];
        const ajouterBoite = (ids, M, bb) => {
          if (!ids.length || !bb) return;
          const coins = [applique(M, bb.x, bb.y), applique(M, bb.x + bb.width, bb.y),
            applique(M, bb.x, bb.y + bb.height), applique(M, bb.x + bb.width, bb.y + bb.height)];
          const xs = coins.map(c => c[0]), ys = coins.map(c => c[1]);
          for (const id of ids) {
            const p = parts[id] || (parts[id] = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity });
            p.x0 = Math.min(p.x0, ...xs); p.y0 = Math.min(p.y0, ...ys);
            p.x1 = Math.max(p.x1, ...xs); p.y1 = Math.max(p.y1, ...ys);
          }
        };
        const parcourir = (el, M, couleur, ids) => {
          const m = matriceDe(el);
          if (m) M = mult(M, m);
          const f = el.getAttribute && el.getAttribute('fill');
          if (f && f !== 'currentColor' && f !== 'none') couleur = f;
          if (el.id) ids = ids.concat(el.id);
          const cl = el.getAttribute && el.getAttribute('class');
          if (cl && el.tagName !== 'svg') ids = ids.concat(cl.split(/\s+/).filter(Boolean).map(c => '.' + c));
          const tag = el.tagName;
          if (tag === 'path') {
            const d = el.getAttribute('d');
            if (d) { ops.push({ t: 'p', d, m: M.map(r3), c: couleur, ids }); ajouterBoite(ids, M, el.getBBox()); }
          } else if (tag === 'rect') {
            const r = { x: +el.getAttribute('x') || 0, y: +el.getAttribute('y') || 0,
              w: +el.getAttribute('width') || 0, h: +el.getAttribute('height') || 0 };
            ops.push({ t: 'r', ...r, m: M.map(r3), c: couleur, ids });
            ajouterBoite(ids, M, { x: r.x, y: r.y, width: r.w, height: r.h });
          } else if (tag === 'line') {
            const l = { x1: +el.getAttribute('x1') || 0, y1: +el.getAttribute('y1') || 0,
              x2: +el.getAttribute('x2') || 0, y2: +el.getAttribute('y2') || 0,
              e: +(el.getAttribute('stroke-width') || 0) };
            ops.push({ t: 'l', ...l, m: M.map(r3), c: el.getAttribute('stroke') !== 'currentColor' && el.getAttribute('stroke') || couleur, ids });
          } else if (tag === 'text') {
            const s = el.textContent;
            if (s) {
              const st = getComputedStyle(el);
              ops.push({ t: 'x', s, m: M.map(r3), c: couleur, ids,
                f: (el.getAttribute('font-style') || (/italic/.test(el.getAttribute('data-variant') || '') ? 'italic' : '')) + ' ' +
                  (el.getAttribute('font-weight') || (/bold/.test(el.getAttribute('data-variant') || '') ? '700' : '400')) + ' ' +
                  (parseFloat(el.getAttribute('font-size')) || 1000) + 'px ' + (el.getAttribute('font-family') || st.fontFamily || 'serif') });
              ajouterBoite(ids, M, el.getBBox());
            }
            return;
          }
          for (const c of el.children) parcourir(c, M, couleur, ids);
        };
        for (const c of svg.children) parcourir(c, S, null, []);
        const P = {};
        for (const id in parts) {
          const p = parts[id];
          if (p.x0 < Infinity) P[id] = { x: r3(p.x0), y: r3(p.y0), w: r3(p.x1 - p.x0), h: r3(p.y1 - p.y0) };
        }
        res = { w: r3(vb.width / 1000), asc: r3(-vb.y / 1000), desc: r3((vb.height + vb.y) / 1000), ops, parts: P,
          erreur: err ? (err.getAttribute('data-mjx-error') || 'erreur TeX') : null };
        boite.removeChild(conteneur);
      } catch (e) {
        res = { w: 1, asc: 0.75, desc: 0.25, ops: [], parts: {}, erreur: String(e && e.message || e) };
      }
      table.formules[cle] = res;
      return res;
    };
  };

  /* ---------- workers : relecture de la table ---------- */
  CV.PrepTable = function (table, erreur) {
    this.table = table;
    this.formule = (tex, display = false) => {
      const r = table.formules[CV.cleFormule(tex, display)];
      if (!r) { erreur('Formule absente de la table de préparation : ' + tex); return { w: 1, asc: 0.75, desc: 0.25, ops: [], parts: {} }; }
      return r;
    };
    this.chemin = d => {
      const l = table.longueurs[d];
      if (l === undefined) { erreur('Tracé absent de la table de préparation : ' + d.slice(0, 40)); return { l: 1, x: 0, y: 0, w: 0, h: 0 }; }
      return l;
    };
  };

  /* Configuration MathJax à poser AVANT de charger vendor/tex-svg-full.js */
  CV.configMathJax = () => ({
    tex: { packages: { '[+]': ['color', 'html'] } },
    svg: { fontCache: 'none' },
    startup: { typeset: false },
  });
})(typeof self !== 'undefined' ? self : this);
