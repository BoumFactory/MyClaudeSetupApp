/* =====================================================================
   Composants du moteur canvas (en plus d'elements.js)
   ---------------------------------------------------------------------
   { lettre: 'M', couleur: 'violet' }        lettre d'événement (.cv-lettre) ; taille: 74 (côté de la boîte)
   { pastille: 1, couleur: 'ambre' }         numéro d'étape dans un rond (taille: 56)
   { resultat: '0,6', couleur: 'violet' }    résultat dans une pilule lumineuse (.cv-resultat) ; '$…$' = formule
   { trait: 'vertical', h: 60 }              séparateur fin (ou 'horizontal', l)
   { image: 'exo-source.png', l, h }         image bitmap ; ajuste: 'contenir' | 'couvrir' ; cadre: true ;
                                             zoom lent par le geste C.zoom('#img', t, { a: 1.15, dur: 20 })
   { tableau: [[…], …], id: 'tab' }          tableau croisé (.cv-tableau) ; chaque CASE est visable : 'tab-l1c2'
   Composants façon bfcours (ex-plugin bfcours) :
   { methode: [...] ou 'texte', titre: 'Méthode' }   boîte méthode (\outilcours), bord gauche orange
   { encadrer: '$x = 3$' ou [...] }                  résultat encadré façon \encadrer[prop]{…}
   { etape: 'Dresser le tableau', n: 1 }             étape numérotée d'une méthode
   texte riche : [mot]{.acc}                         mot accentué façon \acc{…}
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});
  const BF = { prop: 'rgb(70,110,255)', meth: 'rgb(214,128,40)', defi: 'rgb(76,175,105)', rose: '#ff1493' };
  CV.BF = BF;
  // conteneurs avant les feuilles (une méthode peut avoir une clé « titre »)
  CV.CLES.splice(1, 0, 'methode', 'encadrer', 'resultat');
  CV.CLES.push('lettre', 'pastille', 'trait', 'image', 'etape');
  const enfants = (n, liste, E, defaut) => {
    const l = Array.isArray(liste) ? liste : [liste];
    return CV.creerNoeud({ colonne: l.map(x => (typeof x === 'string' && defaut ? defaut(x) : x)), ecart: n.spec.ecart ?? 10,
      alignEnfants: n.spec.alignEnfants }, n, E);
  };
  const texteOuFormule = (x, extra) => (typeof x === 'string' && /^\$[^$]+\$$/.test(x.trim()) ? Object.assign({ tex: x.trim().slice(1, -1) }, extra)
    : typeof x === 'string' ? Object.assign({ texte: x }, extra) : x);

  /* ---------- lettre / pastille ---------- */
  function badge(n, E, rond) {
    return {
      creer() {},
      mesurer(n2) { const d = n2.spec.taille ?? (rond ? 56 : 74); n2.lw = d; n2.lh = d; n2.base = d * 0.68; },
      sprite: true, marge: 40,
      peindre(ctx, n2, E2, opts) {
        const b = n2.b, z = n2.z, d = b.w;
        const c = CV.couleur(E2.theme, n2.spec.couleur, rond ? 'ambre' : 'violet');
        const r = rond ? d / 2 : d * 22 / 74;
        if (!rond) {   // box-shadow 0 0 30px c 55 %
          ctx.save(); ctx.shadowColor = CV.mix(c, 0.55); ctx.shadowBlur = (30 * d / 74) * (ctx.getTransform().a || 1);
          ctx.beginPath(); ctx.roundRect(b.x, b.y, d, d, r); ctx.fillStyle = c; ctx.fill(); ctx.restore();
        }
        const g = ctx.createLinearGradient(b.x, b.y, b.x + d, b.y + d);
        g.addColorStop(0, c); g.addColorStop(1, rond ? c : CV.mix(c, 0.6, '#ffffff'));
        ctx.beginPath(); ctx.roundRect(b.x, b.y, d, d, r); ctx.fillStyle = opts && opts.couleur ? opts.couleur : g; ctx.fill();
        ctx.font = CV.police(d * (rond ? 0.64 : 46 / 74), { gras: true });
        ctx.fillStyle = '#0b1026'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(String(n2.spec[rond ? 'pastille' : 'lettre']), b.x + d / 2, b.y + d / 2 + d * 0.03);
        ctx.textAlign = 'start'; ctx.textBaseline = 'alphabetic';
        void z; void n; void E;
      },
    };
  }
  CV.TYPES.lettre = badge(null, null, false);
  CV.TYPES.pastille = badge(null, null, true);

  /* ---------- résultat (pilule lumineuse) ---------- */
  CV.TYPES.resultat = {
    creer(n, E) {
      const v = n.spec.resultat;
      const tr = n.spec.taille ?? CV.formulesDe(n, E).resultat;   // 62 par défaut ; préréglage formules: 'compactes' → 46
      const spec = texteOuFormule(String(v), { gras: true, nowrap: true, taille: tr, couleur: n.spec.couleurTexte });
      if (spec.tex !== undefined) spec.taille = tr;
      n.c = CV.creerNoeud(spec, n, E);
      n.enfants.push(n.c);
    },
    mesurer(n, W, E) {
      const [pv, ph] = n.spec.marge ?? [6, 30];
      n.pad = { v: pv + 3, h: ph + 3 };
      CV.mesurer(n.c, W - 2 * n.pad.h, E);
      n.lw = n.c.lw + 2 * n.pad.h; n.lh = n.c.lh + 2 * n.pad.v;
      n.base = n.pad.v + (n.c.asc ?? n.c.base ?? n.c.lh * 0.75);
    },
    disposer(n, E) { n.c.lx = (n.lw - n.c.lw) / 2; n.c.ly = n.pad.v; CV.disposer(n.c, E); },
    sprite: true, marge: 60,
    peindre(ctx, n, E) {
      const b = n.b, z = n.z, c = CV.couleur(E.theme, n.spec.couleur, 'vert'), r = 22 * z;
      ctx.save();
      const ext = new Path2D(); ext.rect(b.x - 100 * z, b.y - 100 * z, b.w + 200 * z, b.h + 200 * z);
      const forme = new Path2D(); forme.roundRect(b.x, b.y, b.w, b.h, r); ext.addPath(forme);
      ctx.clip(ext, 'evenodd');
      ctx.shadowColor = CV.mix(c, 0.4); ctx.shadowBlur = 36 * z * (ctx.getTransform().a || 1);
      ctx.fillStyle = '#000'; ctx.fill(forme);
      ctx.restore();
      ctx.fillStyle = CV.mix(c, 0.16); ctx.fill(new Path2D(forme));
      ctx.beginPath(); ctx.roundRect(b.x + 1.5 * z, b.y + 1.5 * z, b.w - 3 * z, b.h - 3 * z, r - 1.5 * z);
      ctx.lineWidth = 3 * z; ctx.strokeStyle = c; ctx.stroke();
    },
  };

  /* ---------- trait (séparateur) ---------- */
  CV.TYPES.trait = {
    creer() {},
    mesurer(n) {
      const v = n.spec.trait !== 'horizontal';
      n.lw = v ? (n.spec.epaisseur ?? 2) : (n.spec.l ?? 100); n.lh = v ? (n.spec.h ?? 60) : (n.spec.epaisseur ?? 2);
    },
    sprite: true, marge: 4,
    peindre(ctx, n, E) { ctx.fillStyle = n.spec.couleur ? CV.couleur(E.theme, n.spec.couleur) : E.theme.trait; ctx.fillRect(n.b.x, n.b.y, n.b.w, n.b.h); },
  };

  /* ---------- image bitmap ---------- */
  CV.TYPES.image = {
    tailleLibre: true,
    creer(n, E) {
      n.bitmap = (E.images || {})[n.spec.image];
      if (!n.bitmap) E.erreur('Image introuvable ou illisible : ' + n.spec.image);
      n.s.kb = 1; n.s.fx = n.spec.fx ?? 0.5; n.s.fy = n.spec.fy ?? 0.5;
    },
    mesurer(n, W) {
      const iw = n.bitmap ? n.bitmap.width : 4, ih = n.bitmap ? n.bitmap.height : 3;
      let l = n.spec.l, h = n.spec.h;
      if (!l && !h) { l = Math.min(W, iw); h = l * ih / iw; } else if (!h) h = l * ih / iw; else if (!l) l = h * iw / ih;
      const sc = Math.min(1, W / l);
      n.lw = l * sc; n.lh = h * sc;
    },
    dynamique: true,
    peindre(ctx, n, E) {
      const b = n.b, z = n.z, bm = n.bitmap, r = (n.spec.rayon ?? (n.spec.cadre ? 20 : 0)) * z;
      if (n.spec.cadre) {
        CV.ombreCarte(ctx, b.x, b.y, b.w, b.h, r, E.theme.ombre, z);
        ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, r); ctx.fillStyle = n.spec.fond || '#ffffff'; ctx.fill();
      }
      if (!bm) return;
      ctx.save();
      ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, r); ctx.clip();
      const m = (n.spec.cadre ? 10 : 0) * z;
      const bx = b.x + m, by = b.y + m, bw = b.w - 2 * m, bh = b.h - 2 * m;
      const sc = n.spec.ajuste === 'couvrir' ? Math.max(bw / bm.width, bh / bm.height) : Math.min(bw / bm.width, bh / bm.height);
      let w = bm.width * sc, h = bm.height * sc, x = bx + (bw - w) / 2, y = by + (bh - h) / 2;
      const k = n.s.kb;   // zoom lent (« Ken Burns ») autour du point (fx, fy) de l'image
      if (k !== 1) { const px = x + w * n.s.fx, py = y + h * n.s.fy; x = px - (px - x) * k; y = py - (py - y) * k; w *= k; h *= k; }
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(bm, x, y, w, h);
      ctx.restore();
      if (n.spec.cadre) { ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, r); ctx.lineWidth = 1.5 * z; ctx.strokeStyle = E.theme.trait; ctx.stroke(); }
    },
  };
  /* liste des images d'une spec (à charger avant de construire le moteur) */
  CV.imagesDe = spec => {
    const res = new Set();
    const voir = o => {
      if (!o || typeof o !== 'object') return;
      if (Array.isArray(o)) { o.forEach(voir); return; }
      if (typeof o.image === 'string') res.add(o.image);
      Object.values(o).forEach(voir);
    };
    voir(spec.scenes);
    return [...res];
  };
  /* chargement : fetch (page servie, worker) ou <img> (aperçu en file://) */
  CV.chargerImages = async (spec, base = '') => {
    const out = {};
    await Promise.all(CV.imagesDe(spec).map(async src => {
      try {
        const r = await fetch(base + src);
        if (!r.ok) throw new Error(r.status);
        out[src] = await createImageBitmap(await r.blob());
      } catch (e) {
        if (racine.document) {
          try {
            const img = new Image(); img.src = base + src; await img.decode();
            out[src] = await createImageBitmap(img);
          } catch (e2) { /* signalé par l'élément image */ }
        }
      }
    }));
    return out;
  };

  /* ---------- boîte méthode (bfcours) ---------- */
  CV.TYPES.methode = {
    creer(n, E) {
      const titre = n.spec.titre ?? 'Méthode';
      const liste = (Array.isArray(n.spec.methode) ? n.spec.methode : [n.spec.methode]).map(x => texteOuFormule(x));
      if (titre) liste.unshift({ texte: titre, taille: 26, gras: true, majuscules: true, couleur: BF.meth, espacementLettres: 0.12 });
      n.col = CV.creerNoeud({ colonne: liste, ecart: n.spec.ecart ?? 6 }, n, E);
      n.enfants.push(n.col);
    },
    mesurer(n, W, E) {
      n.pad = { haut: 26, bas: 26, g: 40, d: 34 };
      CV.mesurer(n.col, W - n.pad.g - n.pad.d, E);
      n.lw = n.col.lw + n.pad.g + n.pad.d; n.lh = n.col.lh + n.pad.haut + n.pad.bas;
    },
    disposer(n, E) { n.col.lx = n.pad.g; n.col.ly = n.pad.haut; n.col.lw = n.lw - n.pad.g - n.pad.d; CV.disposer(n.col, E); },
    sprite: true, marge: 10,
    peindre(ctx, n, E) {
      const b = n.b, z = n.z, r = 18 * z;
      ctx.save();
      ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, r); ctx.clip();
      ctx.fillStyle = CV.mix(BF.meth, 0.14, E.theme.carte); ctx.fillRect(b.x, b.y, b.w, b.h);
      ctx.fillStyle = BF.meth; ctx.fillRect(b.x, b.y, 10 * z, b.h);
      ctx.restore();
    },
  };
  /* ---------- résultat encadré (\encadrer[prop]) ---------- */
  CV.TYPES.encadrer = {
    creer(n, E) {
      const v = n.spec.encadrer;
      n.c = Array.isArray(v) ? CV.creerNoeud({ colonne: v, ecart: 8 }, n, E) : CV.creerNoeud(texteOuFormule(v), n, E);
      n.enfants.push(n.c);
    },
    mesurer(n, W, E) {
      n.pad = { v: 4 + 3, h: 22 + 3 };
      CV.mesurer(n.c, W - 2 * n.pad.h, E);
      n.lw = n.c.lw + 2 * n.pad.h; n.lh = n.c.lh + 2 * n.pad.v;
      n.base = n.pad.v + (n.c.asc ?? n.c.base ?? n.c.lh * 0.75);
    },
    disposer(n, E) { n.c.lx = n.pad.h; n.c.ly = n.pad.v; CV.disposer(n.c, E); },
    sprite: true, marge: 6,
    peindre(ctx, n, E) {
      const b = n.b, z = n.z, c = n.spec.couleur ? CV.couleur(E.theme, n.spec.couleur) : BF.prop;
      ctx.beginPath(); ctx.roundRect(b.x + 1.5 * z, b.y + 1.5 * z, b.w - 3 * z, b.h - 3 * z, 10 * z);
      ctx.fillStyle = CV.mix(c, 0.12); ctx.fill(); ctx.lineWidth = 3 * z; ctx.strokeStyle = c; ctx.stroke();
    },
  };
  /* ---------- étape numérotée (bfcours) ---------- */
  CV.TYPES.etape = {
    creer(n, E) {
      const c = n.spec.couleur ?? BF.meth;
      n.l = CV.creerNoeud({ ligne: [{ pastille: n.spec.n ?? 1, couleur: c, taille: 52 },
        { texte: n.spec.etape, gras: true, couleur: c, taille: n.spec.taille ?? 36, nowrap: n.spec.nowrap }], ecart: 14 }, n, E);
      n.enfants.push(n.l);
    },
    mesurer(n, W, E) { CV.mesurer(n.l, W, E); n.lw = n.l.lw; n.lh = n.l.lh; },
    disposer(n, E) { n.l.lx = 0; n.l.ly = 0; CV.disposer(n.l, E); },
  };

  /* ---------- tableau croisé (.cv-tableau) ----------
     { tableau: lignes, id: 'tab', colonnes: [1.35, 1, 1, 1], hauteurCase: 108, taille: 50, tailleEntete: 34, totaux: true }
     Case : nombre (formule), chaîne (texte ; '$…$' = formule), élément, ou null. Sur l'élément d'une case :
     couleur, fond: 'total'. La 1re ligne et la 1re colonne sont des en-têtes (texte doux gras).
     Chaque case est un nœud visable : 'tab-l1c2' (ligne 1, colonne 2) ; le contenu garde son propre id. */
  CV.TYPES.tableau = {
    creer(n, E) {
      const tb = n.spec.tableau, nl = tb.length, nc = Math.max(...tb.map(l => l.length));
      n.cases = tb.map((l, i) => l.map((c, j) => {
        const entete = i === 0 || j === 0;
        const taille = entete ? (n.spec.tailleEntete ?? 34) : (n.spec.taille ?? 50);
        const total = n.spec.totaux && (i === nl - 1 || j === nc - 1) && !(i === 0 || j === 0);
        const k = new CV.Noeud('case', { id: (n.id || 'tableau') + '-l' + i + 'c' + j }, n, E);
        k.tab = n; k.i = i; k.j = j; k.total = total || (c && c.fond === 'total');
        n.enfants.push(k);
        if (c !== null && c !== undefined && c !== '') {
          let spec;
          // nombre (ou { n: 105, id: 'v-mb', couleur }) : Atkinson gras comme les .cv-case du moteur HTML ;
          // nombres: 'tex' → formule en gras (chiffres sans zéro barré, règle de design.md)
          const nombre = v => (n.spec.nombres === 'tex'
            ? { tex: '\\mathbf{' + String(v).replace('.', '{,}') + '}', taille }
            : { texte: String(v).replace('.', ','), taille, gras: true, nowrap: true, tab: true });
          if (typeof c === 'number') spec = nombre(c);
          else if (typeof c === 'string') spec = /^\$[^$]+\$$/.test(c) ? { tex: c.slice(1, -1), taille } : { texte: c, taille, gras: true, nowrap: !entete, doux: entete };
          else if (c.n !== undefined) { spec = Object.assign(nombre(c.n), c); delete spec.n; }
          else spec = Object.assign({ taille }, c);
          if (spec.texte !== undefined && spec.gras === undefined) spec.gras = true;
          if (entete && spec.texte !== undefined && !spec.couleur && spec.doux === undefined) spec.doux = true;
          if (spec.couleur && spec.doux) spec.doux = false;
          k.c = CV.creerNoeud(spec, k, E);
          k.enfants.push(k.c);
        }
        return k;
      }));
    },
    mesurer(n, W, E) {
      const nc = Math.max(...n.cases.map(l => l.length));
      const p = n.spec.colonnes || Array.from({ length: nc }, (_, j) => (j === 0 ? 1.35 : 1));
      const sp = p.reduce((s, x) => s + x, 0);
      n.colW = p.map(x => W * x / sp);
      n.cases.forEach(l => l.forEach((k, j) => { if (k.c) CV.mesurer(k.c, n.colW[j] - 36, E); }));
      n.ligH = n.cases.map((l, i) => Math.max((i === 0 && n.spec.hauteurEntete) || n.spec.hauteurCase || 108, ...l.map(k => (k.c ? k.c.lh + 24 : 0))));
      n.lw = W; n.lh = n.ligH.reduce((s, h) => s + h, 0);
    },
    disposer(n, E) {
      let y = 0;
      n.cases.forEach((l, i) => {
        let x = 0;
        l.forEach((k, j) => {
          k.lx = x; k.ly = y; k.lw = n.colW[j]; k.lh = n.ligH[i];
          if (k.c) { k.c.lx = (k.lw - k.c.lw) / 2; k.c.ly = (k.lh - k.c.lh) / 2; CV.disposer(k.c, E); }
          x += n.colW[j];
        });
        y += n.ligH[i];
      });
    },
    sprite: true, marge: 130,
    peindre(ctx, n, E) {
      const t = E.theme, b = n.b, z = n.z, r = 28 * z;
      CV.ombreCarte(ctx, b.x, b.y, b.w, b.h, r, t.ombre, z);
      ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, r); ctx.fillStyle = t.carte; ctx.fill();
      ctx.save(); ctx.clip();
      // fonds des totaux
      ctx.fillStyle = t === CV.THEMES.jour ? 'rgba(20,26,51,0.035)' : 'rgba(255,255,255,0.035)';
      n.cases.forEach(l => l.forEach(k => { if (k.total) ctx.fillRect(k.b.x, k.b.y, k.b.w, k.b.h); }));
      ctx.lineWidth = 1.5 * z; ctx.strokeStyle = t.trait;
      let y = b.y;
      n.ligH.forEach((h, i) => { y += h * z; if (i < n.ligH.length - 1) { ctx.beginPath(); ctx.moveTo(b.x, y); ctx.lineTo(b.x + b.w, y); ctx.stroke(); } });
      let x = b.x;
      n.colW.forEach((w, j) => { x += w * z; if (j < n.colW.length - 1) { ctx.beginPath(); ctx.moveTo(x, b.y); ctx.lineTo(x, b.y + b.h); ctx.stroke(); } });
      ctx.restore();
      ctx.beginPath(); ctx.roundRect(b.x + 0.75 * z, b.y + 0.75 * z, b.w - 1.5 * z, b.h - 1.5 * z, r);
      ctx.lineWidth = 1.5 * z; ctx.strokeStyle = t.trait; ctx.stroke();
    },
  };
  CV.TYPES.case = { creer() {}, mesurer() {} };

  /* =====================================================================
     TUILES ALGÉBRIQUES
     ---------------------------------------------------------------------
     { tuiles: '3x2 -2x +4', id: 'a' }     rangée de tuiles ; ids générés a-1, a-2… (classe .a-tuiles)
     { produit: { haut: 'x +3', gauche: '2' }, id: 'p' }   rectangle produit (cadre en L + intérieur)
     { tapis: { gauche: 'x +2', droite: '5' }, id: 'm' }    tapis d'équation (groupes m-g et m-d)
     Couleurs et proportions réglables pour toute la capsule : CAPSULE({ tuiles: { couleurs, rapportX } }).
     Détail : references/moteur-canvas.md § Tuiles algébriques.
     ===================================================================== */
  CV.CLES.splice(1, 0, 'tuiles', 'produit', 'tapis');
  const TU = (CV.TUILES = {});
  /* couleurs d'objet (identiques en thème nuit et jour) : f = fond, b = bordure, t = étiquette */
  TU.DEFAUT = {
    '1': { f: '#ffd21f', b: '#7a5c00', t: '#3d2e00' },
    x: { f: '#2fb34a', b: '#12552a', t: '#ffffff' },
    x2: { f: '#2f6fe8', b: '#16397f', t: '#ffffff' },
    y: { f: '#8e4fe0', b: '#45247f', t: '#ffffff' },
    y2: { f: '#e0479e', b: '#79204f', t: '#ffffff' },
    xy: { f: '#f28a1e', b: '#7f4205', t: '#2b1600' },
    neg: { f: '#e5322d', b: '#74100d', t: '#ffffff' },
  };
  const ALIAS = { un: '1', '1': '1', x: 'x', x2: 'x2', y: 'y', y2: 'y2', xy: 'xy', negatif: 'neg', neg: 'neg' };
  /* config de capsule : couleurs: { un, x, x2, y, y2, xy, negatif } ; chaque valeur = '#fond' ou { f, b, t } */
  TU.couleur = (E, k, neg) => {
    const cache = E.cacheTuiles = E.cacheTuiles || {};
    const cle = neg ? 'neg' : k;
    if (cache[cle]) return cache[cle];
    const base = TU.DEFAUT[cle];
    let res = Object.assign({}, base);
    const cfg = (E.cfgTuiles && E.cfgTuiles.couleurs) || {};
    for (const nom of Object.keys(cfg)) {
      if (ALIAS[nom] !== cle) continue;
      const v = cfg[nom];
      const f = typeof v === 'string' ? v : v.f;
      const lum = (() => { const c = CV.rgba(f); return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255; })();
      res = { f, b: (v && v.b) || CV.mix('#000000', 0.55, f), t: (v && v.t) || (lum > 0.6 ? '#2b1c00' : '#ffffff') };
    }
    cache[cle] = res;
    return res;
  };
  TU.proportions = (E, spec) => {
    const cfg = E.cfgTuiles || {};
    const u = spec.taille ?? cfg.taille ?? 80;
    const rx = spec.rapportX ?? cfg.rapportX ?? 3.2;
    const ry = spec.rapportY ?? cfg.rapportY ?? Math.max(1.5, rx * 0.7);
    return { u, X: Math.round(u * rx), Y: Math.round(u * ry) };
  };
  TU.dims = (k, vertical, P) => {
    let w, h;
    if (k === '1') { w = P.u; h = P.u; } else if (k === 'x') { w = P.X; h = P.u; } else if (k === 'x2') { w = P.X; h = P.X; }
    else if (k === 'y') { w = P.Y; h = P.u; } else if (k === 'y2') { w = P.Y; h = P.Y; } else { w = P.X; h = P.Y; }
    return vertical && w !== h ? { w: h, h: w } : { w, h };
  };
  /* analyse : chaîne ('3x2 -2x +4', 'x² x|') ou tableau de chaînes / { t, neg, vertical, vide, id } */
  const RE_TOKEN = /([+-]?)\s*(\d*)(x\^?2|x²|y\^?2|y²|xy|yx|x|y)?(\|)?/g;
  const NOM_K = s => ({ 'x2': 'x2', 'x²': 'x2', 'x^2': 'x2', 'y2': 'y2', 'y²': 'y2', 'y^2': 'y2', xy: 'xy', yx: 'xy', x: 'x', y: 'y' }[s]);
  TU.analyser = (src, opt, erreur) => {
    const out = [];
    const vert = !!opt.vertical;
    const liste = Array.isArray(src) ? src : [src];
    for (const it of liste) {
      if (it && typeof it === 'object') {
        out.push({ k: it.t || '1', neg: !!it.neg, vertical: it.vertical ?? vert, vide: it.vide ?? opt.vide, id: it.id });
        continue;
      }
      const s = String(it ?? '').trim();
      if (!s) continue;
      let m, vu = 0;
      RE_TOKEN.lastIndex = 0;
      while ((m = RE_TOKEN.exec(s)) !== null) {
        if (m[0] === '') { RE_TOKEN.lastIndex++; continue; }
        vu += m[0].length;
        if (m[2] === '' && !m[3]) continue;
        const k = m[3] ? NOM_K(m[3]) : '1', n = m[2] === '' ? 1 : parseInt(m[2], 10);
        for (let i = 0; i < n; i++) out.push({ k, neg: m[1] === '-', vertical: !!m[4] || (vert && k !== '1' && k !== 'x2' && k !== 'y2'), vide: opt.vide });
      }
      if (vu < s.length) erreur('Tuiles : « ' + s + ' » contient un jeton incompris');
    }
    return out;
  };

  /* ---------- une tuile ---------- */
  const fmesure = new Map();
  const mesureLabel = (police, s) => {
    const cle = police + '|' + s;
    let r = fmesure.get(cle);
    if (!r) {
      const c = new OffscreenCanvas(8, 8).getContext('2d');
      c.font = police;
      const m = c.measureText(s);
      r = { w: m.width, asc: m.actualBoundingBoxAscent, desc: m.actualBoundingBoxDescent };
      fmesure.set(cle, r);
    }
    return r;
  };
  const accrocher = (ctx, E) => {
    const M = ctx.getTransform(), ref = E.k;
    const ok = M.b === 0 && M.c === 0 && Math.abs(M.a) >= 0.5 * ref && Math.abs(M.d) >= 0.5 * ref;
    return {
      ok, a: Math.abs(M.a) || 1,
      x: v => (ok ? (Math.round(M.a * v + M.e) - M.e) / M.a : v),
      y: v => (ok ? (Math.round(M.d * v + M.f) - M.f) / M.d : v),
    };
  };
  CV.TYPES.tuile = {
    creer() {}, mesurer() {}, dynamique: true, sousArbreOK: true, marge: 16,
    peindre(ctx, n, E) {
      const tu = n.tu, b = n.b, th = E.theme, S = accrocher(ctx, E);
      const x0 = S.x(b.x), x1 = S.x(b.x + b.w), y0 = S.y(b.y), y1 = S.y(b.y + b.h);
      const w = x1 - x0, h = y1 - y0, r = Math.min(0.1 * tu.u * n.z, w / 4, h / 4);
      const bw = S.ok ? Math.max(1, Math.round(2.2 * S.a)) / S.a : 2 * n.z;
      if (tu.vide) {
        ctx.save();
        ctx.beginPath(); ctx.roundRect(x0 + bw, y0 + bw, w - 2 * bw, h - 2 * bw, r);
        ctx.fillStyle = CV.mix(th.texte, 0.05); ctx.fill();
        ctx.setLineDash([12 * n.z, 9 * n.z]); ctx.lineWidth = bw; ctx.strokeStyle = CV.mix(th.doux, 0.9); ctx.stroke();
        ctx.restore();
        return;
      }
      const neg = tu.neg > 0.5, col = TU.couleur(E, tu.k, neg);
      ctx.beginPath(); ctx.roundRect(x0, y0, w, h, r); ctx.fillStyle = col.b; ctx.fill();
      const ix = x0 + bw, iy = y0 + bw, iw = w - 2 * bw, ih = h - 2 * bw;
      ctx.beginPath(); ctx.roundRect(ix, iy, iw, ih, Math.max(0, r - bw));
      const g = ctx.createLinearGradient(0, iy, 0, iy + ih);
      g.addColorStop(0, CV.mix('#ffffff', 0.16, col.f)); g.addColorStop(0.5, col.f); g.addColorStop(1, col.f);
      ctx.fillStyle = g; ctx.fill();
      if (tu.flash > 0.002) { ctx.fillStyle = 'rgba(255,255,255,' + Math.min(1, tu.flash * 0.85).toFixed(3) + ')'; ctx.fill(); }
      // étiquette : signe moins typographique (U+2212), variables en italique, exposant 2 pour x² et y²
      const k = tu.k, variable = k !== '1';
      const fs = tu.u * n.z * (k === 'x2' ? 0.8 : k === 'y2' ? 0.7 : 0.52);
      const principal = (neg ? '−' : '') + (k === '1' ? '1' : k === 'xy' ? 'xy' : k[0]);
      const sup = k === 'x2' || k === 'y2' ? '2' : '';
      const pol = CV.police(fs, { gras: true, it: variable }), polSup = CV.police(fs * 0.62, { gras: true, it: false });
      const a = mesureLabel(pol, principal), bsup = sup ? mesureLabel(polSup, sup) : null;
      const dec = fs * 0.42;
      const total = a.w + (bsup ? bsup.w + fs * 0.03 : 0);
      const haut = Math.max(a.asc, bsup ? dec + bsup.asc : 0), bas = a.desc;
      const cx = ix + iw / 2, cy = iy + ih / 2, base = cy + (haut - bas) / 2;
      ctx.fillStyle = col.t; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
      ctx.font = pol; ctx.fillText(principal, cx - total / 2, base);
      if (sup) { ctx.font = polSup; ctx.fillText(sup, cx - total / 2 + a.w + fs * 0.03, base - dec); }
    },
  };
  let cptTu = 0;
  const creerTuile = (parent, E, id, d, P, dims) => {
    const k = new CV.Noeud('tuile', { id, classe: d.classe }, parent, E);
    const dm = dims || TU.dims(d.k, d.vertical, P);
    k.tu = { k: d.k, neg: d.neg ? 1 : 0, suivant: d.neg ? 1 : 0, flash: 0, vide: !!d.vide, w: dm.w, h: dm.h, u: P.u };
    k.lw = dm.w; k.lh = dm.h;
    parent.enfants.push(k);
    return k;
  };

  /* mise en rangées : place les tuiles `liste` dans la largeur W (retour à la ligne, ou n colonnes) */
  function fluxTuiles(liste, W, o) {
    const rangs = []; let rang = [], rw = 0;
    for (const k of liste) {
      const apres = rw + (rang.length ? o.ecart : 0) + k.lw;
      const plein = o.colonnes ? rang.length >= o.colonnes : (o.retour && rang.length && apres > W + 0.5);
      if (plein) { rangs.push(rang); rang = []; rw = 0; }
      rw += (rang.length ? o.ecart : 0) + k.lw; rang.push(k);
    }
    if (rang.length) rangs.push(rang);
    let y = 0, wMax = 0;
    for (const r of rangs) {
      const hr = Math.max(...r.map(k => k.lh));
      let x = 0;
      for (const k of r) {
        k.lx = x; x += k.lw + o.ecart;
        k.ly = y + (o.alignV === 'bas' ? hr - k.lh : o.alignV === 'haut' ? 0 : (hr - k.lh) / 2);
      }
      wMax = Math.max(wMax, x - o.ecart);
      y += hr + o.ecartV;
    }
    return { w: wMax, h: Math.max(0, y - o.ecartV) };
  }
  CV.TYPES.tuiles = {
    creer(n, E) {
      if (!n.spec.align) n.spec.align = 'centre';
      const pre = n.prefixe = n.id || 'tu' + (++cptTu);
      const P = n.P = TU.proportions(E, n.spec);
      const descs = TU.analyser(n.spec.tuiles, { vertical: n.spec.vertical, vide: n.spec.vide }, E.erreur);
      descs.forEach((d, i) => { d.classe = pre + '-tuiles'; creerTuile(n, E, d.id || pre + '-' + (i + 1), d, P); });
    },
    mesurer(n, W) {
      const ecart = n.spec.ecart ?? 8;
      const r = fluxTuiles(n.enfants, W, { ecart, ecartV: n.spec.ecartV ?? ecart, colonnes: n.spec.colonnes,
        retour: n.spec.retour !== false, alignV: n.spec.alignV });
      n.lw = r.w; n.lh = r.h;
    },
  };

  /* ---------- rectangle produit ---------- */
  const FACTEUR = { '1': 1, x: 1, y: 1 };
  const PRODUIT = { '11': '1', '1x': 'x', x1: 'x', '1y': 'y', y1: 'y', xx: 'x2', yy: 'y2', xy: 'xy', yx: 'xy' };
  CV.TYPES.produit = {
    creer(n, E) {
      if (!n.spec.align) n.spec.align = 'centre';
      const pre = n.prefixe = n.id || 'tu' + (++cptTu);
      const P = n.P = TU.proportions(E, n.spec);
      const s = n.spec.produit;
      const lire = (src, vertical) => TU.analyser(src, { vertical }, E.erreur).filter(d => {
        if (!FACTEUR[d.k]) { E.erreur('Produit : facteur « ' + d.k + ' » non permis (1, x ou y seulement)'); return false; }
        return true;
      });
      const haut = lire(s.haut, false), gauche = lire(s.gauche, true);
      n.hauts = haut.map((d, j) => creerTuile(n, E, pre + '-h' + (j + 1), Object.assign(d, { classe: pre + '-haut' }), P, TU.dims(d.k, false, P)));
      n.gauches = gauche.map((d, i) => creerTuile(n, E, pre + '-g' + (i + 1), Object.assign(d, { classe: pre + '-gauche' }), P, TU.dims(d.k, true, P)));
      n.cases = n.gauches.map((g, i) => n.hauts.map((h, j) => {
        const k = PRODUIT[h.tu.k + g.tu.k];
        const neg = (h.tu.neg > 0.5) !== (g.tu.neg > 0.5);
        return creerTuile(n, E, pre + '-l' + (i + 1) + 'c' + (j + 1), { k, neg, classe: pre + '-produits' }, P, { w: h.tu.w, h: g.tu.h });
      }));
    },
    mesurer(n) {
      const P = n.P, g = n.spec.cadre ?? 14, e = n.spec.ecart ?? 0, d = P.u + g;
      n.g = g;
      n.colX = []; n.rowY = [];
      let x = d, y = d;
      n.hauts.forEach(k => { n.colX.push(x); k.lx = x; k.ly = 0; x += k.lw + e; });
      n.gauches.forEach(k => { n.rowY.push(y); k.lx = 0; k.ly = y; y += k.lh + e; });
      n.cases.forEach((ligne, i) => ligne.forEach((k, j) => { k.lx = n.colX[j]; k.ly = n.rowY[i]; }));
      n.lw = Math.max(d, x - e); n.lh = Math.max(d, y - e);
    },
    dynamique: true, marge: 30,
    peindre(ctx, n, E) {
      const th = E.theme, b = n.b, z = n.z, P = n.P, S = accrocher(ctx, E), p = 10 * z;
      // cadre en L (bandeau haut + bandeau gauche, une seule surface)
      const cadre = new Path2D();
      cadre.roundRect(S.x(b.x - p), S.y(b.y - p), b.w + 2 * p, (P.u) * z + 2 * p, 16 * z);
      cadre.roundRect(S.x(b.x - p), S.y(b.y - p), (P.u) * z + 2 * p, b.h + 2 * p, 16 * z);
      ctx.fillStyle = CV.mix(th.texte, 0.07); ctx.fill(cadre);
      // emplacements de l'intérieur
      if (n.spec.guide !== false) {
        ctx.save(); ctx.setLineDash([10 * z, 8 * z]); ctx.lineWidth = Math.max(1, 2 * z); ctx.strokeStyle = CV.mix(th.doux, 0.55);
        n.cases.forEach(l => l.forEach(k => {
          const x0 = S.x(k.b.x), y0 = S.y(k.b.y);
          ctx.beginPath(); ctx.roundRect(x0, y0, S.x(k.b.x + k.b.w) - x0, S.y(k.b.y + k.b.h) - y0, 6 * z); ctx.stroke();
        }));
        ctx.restore();
      }
      if (n.spec.signe !== false) {   // « × » dans l'angle
        ctx.font = CV.police(P.u * z * 0.6, { gras: true }); ctx.fillStyle = CV.mix(th.doux, 0.9);
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('×', b.x + P.u * z / 2, b.y + P.u * z / 2 + P.u * z * 0.03);
        ctx.textAlign = 'start'; ctx.textBaseline = 'alphabetic';
      }
    },
  };

  /* ---------- tapis d'équation ---------- */
  CV.TYPES.tapis = {
    creer(n, E) {
      if (!n.spec.align) n.spec.align = 'centre';
      const pre = n.prefixe = n.id || 'tu' + (++cptTu);
      const s = n.spec.tapis;
      const opt = c => Object.assign({ tuiles: c ?? '', id: undefined }, ['taille', 'rapportX', 'rapportY', 'vertical', 'ecart', 'ecartV', 'alignV'].reduce((a, k) => {
        if (n.spec[k] !== undefined) a[k] = n.spec[k]; return a; }, {}));
      n.gg = CV.creerNoeud(Object.assign(opt(s.gauche), { id: pre + '-g', align: 'gauche' }), n, E);
      n.gd = CV.creerNoeud(Object.assign(opt(s.droite), { id: pre + '-d', align: 'gauche' }), n, E);
      n.enfants.push(n.gg, n.gd);
    },
    mesurer(n, W, E) {
      const pad = n.spec.marge ?? 36, signe = 70;
      const demi = (n.spec.l ? Math.min(n.spec.l, W) : W) / 2 - pad - signe / 2;
      CV.mesurer(n.gg, Math.max(60, demi), E); CV.mesurer(n.gd, Math.max(60, demi), E);
      n.pad = pad;
      const nat = 2 * (Math.max(n.gg.lw, n.gd.lw) + 2 * pad) + 0;
      n.lw = n.spec.l ? Math.min(n.spec.l, W) : Math.min(W, Math.max(nat, 900));
      n.lh = Math.max(n.gg.lh, n.gd.lh) + 2 * pad;
      n.lh = Math.max(n.lh, n.spec.hMin ?? 300);
    },
    disposer(n, E) {
      const demi = n.lw / 2;
      [[n.gg, 0], [n.gd, demi]].forEach(([g, x0]) => {
        g.lx = x0 + (demi - g.lw) / 2; g.ly = (n.lh - g.lh) / 2;
        CV.disposer(g, E);
      });
    },
    sprite: true, marge: 130,
    peindre(ctx, n, E) {
      const th = E.theme, b = n.b, z = n.z, r = 30 * z;
      CV.ombreCarte(ctx, b.x, b.y, b.w, b.h, r, th.ombre, z);
      ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, r);
      ctx.fillStyle = CV.mix(th.texte, 0.06, th.carteForte); ctx.fill();
      ctx.lineWidth = 2 * z; ctx.strokeStyle = th.trait; ctx.stroke();
      const cx = b.x + b.w / 2, cy = b.y + b.h / 2;
      ctx.lineWidth = 4 * z; ctx.lineCap = 'round'; ctx.strokeStyle = CV.mix(th.texte, 0.28);
      ctx.beginPath(); ctx.moveTo(cx, b.y + 28 * z); ctx.lineTo(cx, cy - 56 * z);
      ctx.moveTo(cx, cy + 56 * z); ctx.lineTo(cx, b.y + b.h - 28 * z); ctx.stroke();
      ctx.lineWidth = 9 * z; ctx.strokeStyle = th.texte;
      ctx.beginPath(); ctx.moveTo(cx - 26 * z, cy - 11 * z); ctx.lineTo(cx + 26 * z, cy - 11 * z);
      ctx.moveTo(cx - 26 * z, cy + 11 * z); ctx.lineTo(cx + 26 * z, cy + 11 * z); ctx.stroke();
      ctx.lineCap = 'butt';
    },
  };

})(typeof self !== 'undefined' ? self : this);
