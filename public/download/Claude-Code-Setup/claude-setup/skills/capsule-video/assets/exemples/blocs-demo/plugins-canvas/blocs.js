/* =====================================================================
   Plugin « blocs » du moteur canvas : code qui s'écrit, terminal, compilation
   ---------------------------------------------------------------------
   Module CHARGÉ À CÔTÉ du moteur (aucune retouche de moteur-canvas/) : il
   s'enregistre dans les tables ouvertes du moteur (CV.CLES, CV.TYPES,
   CV.GABARITS) et enveloppe CV.creerGestes pour ajouter les gestes
   C.compile et C.badgeVoix. Il est chargé par une ligne en tête de spec.js
   (voir references/bloc-code.md), donc dans la page, l'aperçu et les workers.

   Éléments :
     { code: '…', fichier: 'cours.typ', langage: 'typst', frappe: […], surlignage: […], regard: […] }
     { terminal: [ { cmd, de, a }, { sortie, t }, { ok, t } ], invite: '$' }
   Gestes :
     C.compile('#editeur', '@b08~"compile"', { rendu: '#rendu1', zoom: { a: 1.6, fx: .5, fy: .3 } })
     C.badgeVoix({ voix: 'tom', texte: 'Voix de synthèse' })

   Tout est fonction du temps t (aucune horloge, aucun hasard non déterministe).
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});
  if (CV.BLOCS) return;
  CV.BLOCS = { version: 1 };
  const BASE = racine.PLUG_BASE || '/plugins-canvas/';
  const MONO = 'JBMono';
  const AV = 0.6;   // chasse de JetBrains Mono : 600/1000 em

  /* ---------- police à chasse fixe (page et workers) ---------- */
  const chargerMono = async () => {
    const ens = racine.document ? racine.document.fonts : racine.fonts;
    await Promise.all([['400', 'jetbrains-mono-latin-400-normal'], ['700', 'jetbrains-mono-latin-700-normal']].map(async ([w, f]) => {
      const ff = new FontFace(MONO, `url("${BASE}fonts/${f}.woff2")`, { weight: w, style: 'normal' });
      await ff.load();
      ens.add(ff);
    }));
  };
  const polices0 = CV.chargerPolices;
  CV.chargerPolices = async function (...a) { await polices0.apply(this, a); await chargerMono(); };

  /* ---------- palettes (VS Code Dark+ / Light+) ---------- */
  const PAL = {
    sombre: {
      fond: '#1e1e1e', barre: '#323233', ongletOff: '#2d2d2d', texte: '#d4d4d4', doux: '#9da0a6', num: '#6e7681', numActif: '#d0d0d0',
      ligneActive: 'rgba(255,255,255,0.045)', statut: '#007acc', statutTexte: '#ffffff', bord: 'rgba(255,255,255,0.12)',
      surligne: 'rgba(255,208,70,0.17)', curseur: '#d4d4d4', ok: '#23d18b', erreur: '#f14c4c', sortie: '#cccccc',
      cls: { texte: '#d4d4d4', motcle: '#c586c0', fonction: '#dcdcaa', chaine: '#ce9178', commentaire: '#6a9955', nombre: '#b5cea8',
        maths: '#4ec9b0', mathsDelim: '#569cd6', titre: '#569cd6', param: '#9cdcfe', constante: '#569cd6', etiquette: '#4fc1ff',
        operateur: '#d7ba7d', gras: '#ffffff', puce: '#6796e6', crochet0: '#ffd700', crochet1: '#da70d6', crochet2: '#179fff' },
    },
    clair: {
      fond: '#ffffff', barre: '#e8e8e8', ongletOff: '#ececec', texte: '#1f1f1f', doux: '#616161', num: '#8a8a8a', numActif: '#222222',
      ligneActive: 'rgba(0,0,0,0.045)', statut: '#007acc', statutTexte: '#ffffff', bord: 'rgba(0,0,0,0.14)',
      surligne: 'rgba(255,200,0,0.28)', curseur: '#1f1f1f', ok: '#16825d', erreur: '#cd3131', sortie: '#333333',
      cls: { texte: '#1f1f1f', motcle: '#af00db', fonction: '#795e26', chaine: '#a31515', commentaire: '#008000', nombre: '#098658',
        maths: '#267f99', mathsDelim: '#0000ff', titre: '#0451a5', param: '#001080', constante: '#0000ff', etiquette: '#0070c1',
        operateur: '#795e26', gras: '#000000', puce: '#0451a5', crochet0: '#0431fa', crochet1: '#319331', crochet2: '#7b3814' },
    },
  };
  const GRAS = new Set(['titre', 'gras', 'motcle']);

  /* ---------- coloration syntaxique : une classe par caractère ---------- */
  const MOTS_CLES = new Set(['set', 'show', 'let', 'import', 'include', 'if', 'else', 'for', 'while', 'in', 'return', 'break',
    'continue', 'context', 'as', 'not', 'and', 'or']);
  const CONSTANTES = new Set(['true', 'false', 'none', 'auto']);
  const FERME = { '(': ')', '[': ']', '{': '}' };

  function colorerTypst(src) {
    const n = src.length, cl = new Array(n).fill('texte');
    const peindre = (a, b, c) => { for (let i = a; i < b; i++) cl[i] = c; };
    const pile = [];                        // { mode, ferme }
    let maths = false, codeLigne = false, enTitre = false, apres = false, i = 0;
    const mode = () => (pile.length ? pile[pile.length - 1].mode : (codeLigne ? 'code' : 'markup'));
    while (i < n) {
      const c = src[i], d = src[i + 1];
      const etaitAppel = apres; apres = false;
      const debutLigne = i === 0 || src[i - 1] === '\n';
      if (c === '\n') { enTitre = false; if (!pile.length) codeLigne = false; i++; continue; }
      if (c === '/' && d === '/') { let j = src.indexOf('\n', i); if (j < 0) j = n; peindre(i, j, 'commentaire'); i = j; continue; }
      if (c === '/' && d === '*') { let j = src.indexOf('*/', i + 2); j = j < 0 ? n : j + 2; peindre(i, j, 'commentaire'); i = j; continue; }
      if (c === '"') {
        let j = i + 1;
        while (j < n && src[j] !== '"') { if (src[j] === '\\') j++; j++; }
        j = Math.min(n, j + 1); peindre(i, j, 'chaine'); i = j; continue;
      }
      if (c === '$') { cl[i] = 'mathsDelim'; maths = !maths; i++; continue; }
      if (maths) {
        let m;
        const reste = src.slice(i, i + 40);
        if ((m = /^[A-Za-z][A-Za-z0-9.]*/.exec(reste))) {
          peindre(i, i + m[0].length, src[i + m[0].length] === '(' ? 'fonction' : 'maths'); i += m[0].length; continue;
        }
        if ((m = /^\d+([.,]\d+)?/.exec(reste))) { peindre(i, i + m[0].length, 'nombre'); i += m[0].length; continue; }
        if ('^_/=<>+-*|'.includes(c)) cl[i] = 'operateur';
        else if (c !== ' ') cl[i] = 'maths';
        i++; continue;
      }
      if (c === '#') {
        const m = /^#([A-Za-z_][\w-]*)/.exec(src.slice(i, i + 60));
        if (m) {
          const motCle = MOTS_CLES.has(m[1]);
          peindre(i, i + m[0].length, motCle ? 'motcle' : 'fonction');
          if (motCle) codeLigne = true;
          i += m[0].length; apres = true; continue;
        }
      }
      if ('([{'.includes(c)) {
        const m0 = mode();
        if (m0 === 'code' || etaitAppel) {
          cl[i] = 'crochet' + (pile.length % 3);
          pile.push({ mode: c === '[' ? 'markup' : 'code', ferme: FERME[c] });
        } else cl[i] = 'texte';
        i++; continue;
      }
      if (')]}'.includes(c)) {
        const top = pile[pile.length - 1];
        if (top && top.ferme === c) { pile.pop(); cl[i] = 'crochet' + (pile.length % 3); apres = true; } else cl[i] = 'texte';
        i++; continue;
      }
      if (mode() === 'code') {
        let m;
        const reste = src.slice(i, i + 60);
        if ((m = /^[A-Za-z_][\w-]*/.exec(reste))) {
          const mot = m[0], suite = src.slice(i + mot.length).match(/^\s*(.)/);
          let cls = 'param';
          if (suite && suite[1] === ':' && src[i + mot.length + 1] !== ':') cls = 'param';
          else if (MOTS_CLES.has(mot)) cls = 'motcle';
          else if (CONSTANTES.has(mot)) cls = 'constante';
          else if (suite && suite[1] === '(') cls = 'fonction';
          peindre(i, i + mot.length, cls); i += mot.length; continue;
        }
        if ((m = /^\d+(\.\d+)?(pt|cm|mm|em|%|fr|deg|rad|in)?/.exec(reste))) { peindre(i, i + m[0].length, 'nombre'); i += m[0].length; continue; }
        if ('=+-*/<>!'.includes(c)) cl[i] = 'operateur';
        i++; continue;
      }
      // texte courant (markup)
      if (debutLigne) {
        let m;
        const reste = src.slice(i, i + 12);
        if ((m = /^=+(?=\s)/.exec(reste))) { peindre(i, i + m[0].length, 'titre'); enTitre = true; i += m[0].length; continue; }
        if ((m = /^\s*([-+]|\d+\.)(?=\s)/.exec(reste))) { peindre(i + m[0].length - m[1].length, i + m[0].length, 'puce'); i += m[0].length; continue; }
      }
      if (c === '*' && d && d !== ' ') {
        const j = src.indexOf('*', i + 1), fin = src.indexOf('\n', i);
        if (j > 0 && (fin < 0 || j < fin)) { peindre(i, j + 1, 'gras'); i = j + 1; continue; }
      }
      let m2;
      if ((m2 = /^(<[\w:-]+>|@[\w:-]+)/.exec(src.slice(i, i + 40)))) { peindre(i, i + m2[0].length, 'etiquette'); i += m2[0].length; continue; }
      cl[i] = enTitre ? 'titre' : 'texte';
      i++;
    }
    return cl;
  }

  function colorerLatex(src) {
    const n = src.length, cl = new Array(n).fill('texte');
    const peindre = (a, b, c) => { for (let i = a; i < b; i++) cl[i] = c; };
    let maths = false, prof = 0, i = 0;
    while (i < n) {
      const c = src[i];
      if (c === '%') { let j = src.indexOf('\n', i); if (j < 0) j = n; peindre(i, j, 'commentaire'); i = j; continue; }
      if (c === '$') { cl[i] = 'mathsDelim'; maths = !maths; i++; continue; }
      if (c === '\\') {
        const m = /^\\([A-Za-z@]+|.)/.exec(src.slice(i, i + 40));
        const nom = m ? m[1] : '';
        peindre(i, i + (m ? m[0].length : 1), ['begin', 'end', 'usepackage', 'documentclass', 'newcommand'].includes(nom) ? 'motcle' : 'fonction');
        i += m ? m[0].length : 1; continue;
      }
      if (c === '{') { cl[i] = 'crochet' + (prof % 3); prof++; i++; continue; }
      if (c === '}') { prof = Math.max(0, prof - 1); cl[i] = 'crochet' + (prof % 3); i++; continue; }
      if (c === '[' || c === ']') { cl[i] = 'crochet2'; i++; continue; }
      if (maths) cl[i] = /\d/.test(c) ? 'nombre' : '^_=+-'.includes(c) ? 'operateur' : 'maths';
      i++;
    }
    return cl;
  }

  function colorerBash(src) {
    const n = src.length, cl = new Array(n).fill('texte');
    const peindre = (a, b, c) => { for (let i = a; i < b; i++) cl[i] = c; };
    const re = /"[^"]*"|'[^']*'|#.*$|\S+/g;
    let m, premier = true;
    while ((m = re.exec(src))) {
      const s = m[0], a = m.index;
      if (s[0] === '"' || s[0] === "'") peindre(a, a + s.length, 'chaine');
      else if (s[0] === '#') peindre(a, a + s.length, 'commentaire');
      else if (premier) { peindre(a, a + s.length, 'fonction'); premier = false; }
      else if (s[0] === '-') peindre(a, a + s.length, 'param');
      else if (/^[\d.]+$/.test(s)) peindre(a, a + s.length, 'nombre');
    }
    return cl;
  }
  const COLORIEURS = { typst: colorerTypst, latex: colorerLatex, tex: colorerLatex, bash: colorerBash, shell: colorerBash };

  /* découpe en lignes + exécutions (runs) de même classe */
  function analyser(src, langage) {
    const col = (COLORIEURS[langage] || (s => new Array(s.length).fill('texte')))(src);
    const lignes = [];
    let debut = 0;
    const brut = src.split('\n');
    for (const texte of brut) {
      const runs = [];
      let i = 0;
      while (i < texte.length) {
        const c = col[debut + i];
        let j = i + 1;
        while (j < texte.length && col[debut + j] === c) j++;
        runs.push({ i0: i, s: texte.slice(i, j), c });
        i = j;
      }
      lignes.push({ texte, runs });
      debut += texte.length + 1;
    }
    return lignes;
  }

  /* source d'un littéral entre apostrophes inversées : première ligne vide et indentation commune retirées */
  function nettoyerSource(s) {
    let l = Array.isArray(s) ? s.join('\n') : String(s);
    l = l.replace(/\t/g, '  ').replace(/\r/g, '');
    const lignes = l.split('\n');
    if (lignes.length && lignes[0].trim() === '') lignes.shift();
    while (lignes.length && lignes[lignes.length - 1].trim() === '') lignes.pop();
    const ind = Math.min(...lignes.filter(x => x.trim()).map(x => x.match(/^ */)[0].length), 1e9);
    return lignes.map(x => x.slice(ind === 1e9 ? 0 : ind)).join('\n');
  }

  /* ---------- frappe : poids par caractère (rythme humain, déterministe) ---------- */
  function mulberry(a) {
    return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let x = Math.imul(a ^ (a >>> 15), 1 | a); x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x; return ((x ^ (x >>> 14)) >>> 0) / 4294967296; };
  }
  function poidsFrappe(texte, graine) {
    const r = mulberry(graine * 7919 + 13), cum = new Float64Array(texte.length + 1);
    let s = 0, indent = true;
    for (let i = 0; i < texte.length; i++) {
      const c = texte[i];
      let w = 0.7 + 0.7 * r();
      if (c === '\n') { w = 2.6; indent = true; }
      else if (c === ' ' && indent) w = 0.12;
      else { indent = false; if (c === ' ') w *= 1.25; else if ('()[]{}$"#='.includes(c)) w *= 1.4; else if (c >= 'A' && c <= 'Z') w *= 1.3; }
      s += w; cum[i + 1] = s;
    }
    for (let i = 0; i <= texte.length; i++) cum[i] = s ? cum[i] / s : 1;
    return cum;
  }
  /* nombre de caractères tapés à l'instant t (0 avant le début, tot après la fin) */
  function tapes(seg, t) {
    if (t < seg.t0) return -1;
    const p = (t - seg.t0) / Math.max(1e-6, seg.t1 - seg.t0);
    if (p >= 1) return seg.tot;
    let lo = 0, hi = seg.tot;
    while (lo < hi) { const m = (lo + hi + 1) >> 1; if (seg.cum[m] <= p) lo = m; else hi = m - 1; }
    return lo;
  }
  const borner = (x, a, b) => Math.max(a, Math.min(b, x));
  const doux = x => { x = borner(x, 0, 1); return x * x * (3 - 2 * x); };

  /* ---------- outils de dessin ---------- */
  function coche(ctx, cx, cy, r, p, couleur, lw) {
    const P = [[-0.5, 0.05], [-0.12, 0.42], [0.52, -0.36]];
    const L1 = Math.hypot(P[1][0] - P[0][0], P[1][1] - P[0][1]), L2 = Math.hypot(P[2][0] - P[1][0], P[2][1] - P[1][1]);
    const d = borner(p, 0, 1) * (L1 + L2);
    ctx.save();
    ctx.strokeStyle = couleur; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(cx + P[0][0] * r, cy + P[0][1] * r);
    if (d <= L1) { const f = d / L1; ctx.lineTo(cx + (P[0][0] + (P[1][0] - P[0][0]) * f) * r, cy + (P[0][1] + (P[1][1] - P[0][1]) * f) * r); }
    else {
      ctx.lineTo(cx + P[1][0] * r, cy + P[1][1] * r);
      const f = (d - L1) / L2;
      ctx.lineTo(cx + (P[1][0] + (P[2][0] - P[1][0]) * f) * r, cy + (P[1][1] + (P[2][1] - P[1][1]) * f) * r);
    }
    ctx.stroke(); ctx.restore();
  }
  function croix(ctx, cx, cy, r, couleur, lw) {
    ctx.save(); ctx.strokeStyle = couleur; ctx.lineWidth = lw; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(cx - r * 0.45, cy - r * 0.45); ctx.lineTo(cx + r * 0.45, cy + r * 0.45);
    ctx.moveTo(cx + r * 0.45, cy - r * 0.45); ctx.lineTo(cx - r * 0.45, cy + r * 0.45); ctx.stroke(); ctx.restore();
  }
  /* fenêtre arrondie avec ombre, puis clip sur la fenêtre (à fermer avec ctx.restore()) */
  function fenetre(ctx, b, z, E, P, rayon) {
    ctx.save();
    ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 44 * z * E.k; ctx.shadowOffsetY = 16 * z * E.k;
    ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, rayon); ctx.fillStyle = P.fond; ctx.fill();
    ctx.restore();
    ctx.save();
    ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, rayon); ctx.clip();
  }
  const TEXTE_UI = z => `400 ${22 * z}px Atkinson, sans-serif`;

  /* défilement : cible en lignes, lissée sur 0,4 s (fonction pure du temps) */
  function lisse(fCible, t) {
    let s = 0;
    for (let j = 0; j < 7; j++) s += fCible(t - j * 0.065);
    return s / 7;
  }

  /* =====================================================================
     Élément « code »
     ===================================================================== */
  CV.CLES.push('code', 'terminal');

  CV.TYPES.code = {
    tailleLibre: true, dynamique: true,
    creer(n, E) {
      const sp = n.spec;
      n.E = E;
      n.src = nettoyerSource(sp.code);
      n.langage = (sp.langage || 'typst').toLowerCase();
      n.lignes = analyser(n.src, n.langage);
      n.pal = PAL[sp.clair ? 'clair' : 'sombre'];
      n.compiles = [];
      n.segs = []; n.surl = []; n.regards = []; n.cov = [];
      n.resoudre = tt => {
        const N = n.lignes.length;
        n.cov = new Array(N).fill(null);
        n.segs = (sp.frappe || []).map((f, idx) => {
          const [a, b] = Array.isArray(f.lignes) ? f.lignes : [f.lignes, f.lignes];
          if (!(a >= 1 && b >= a && b <= N)) { E.erreur(`code ${n.id || ''} : frappe sur les lignes ${a}–${b}, mais le code a ${N} lignes`); return null; }
          const morceaux = n.lignes.slice(a - 1, b).map(L => L.texte);
          const texte = morceaux.join('\n');
          const t0 = tt(f.de);
          let t1 = f.a !== undefined ? tt(f.a) : t0 + texte.length / (f.vitesse || 14);
          if (t1 < t0 + 0.2) t1 = t0 + 0.2;
          const offs = []; let o = 0;
          morceaux.forEach(m => { offs.push(o); o += m.length + 1; });
          const seg = { l0: a - 1, l1: b - 1, t0, t1, offs, tot: texte.length, cum: poidsFrappe(texte, idx + 1) };
          for (let k = a - 1; k < b; k++) n.cov[k] = { s: idx, off: offs[k - a + 1] };
          return seg;
        }).filter(Boolean);
        // indices de segments à jour après filtrage
        n.cov = new Array(N).fill(null);
        n.segs.forEach((seg, idx) => { for (let k = seg.l0; k <= seg.l1; k++) n.cov[k] = { s: idx, off: seg.offs[k - seg.l0] }; });
        n.surl = (sp.surlignage || []).map(h => {
          const [a, b] = Array.isArray(h.lignes) ? h.lignes : [h.lignes, h.lignes];
          if (!(a >= 1 && b >= a && b <= N)) E.erreur(`code ${n.id || ''} : surlignage des lignes ${a}–${b} hors du code (${N} lignes)`);
          return { a: a - 1, b: b - 1, t0: tt(h.de), t1: h.jusque !== undefined ? tt(h.jusque) : Infinity, couleur: h.couleur || null };
        });
        n.regards = (sp.regard || []).map(r => ({ t: tt(r.t), ligne: r.ligne - 1 })).sort((x, y) => x.t - y.t);
      };
    },
    mesurer(n, W) {
      const sp = n.spec, N = n.lignes.length;
      const lw = Math.min(sp.l || W, W);
      const maxCols = Math.max(8, ...n.lignes.map(L => L.texte.length));
      const chiffres = Math.max(2, String(N).length);
      let taille = sp.taille || 32;
      taille = Math.max(18, Math.min(taille, (lw - 92) / (AV * (maxCols + chiffres + 1))));
      const lh = Math.round(taille * 1.55), titreH = 54, statutH = 44, pad = 14;
      const naturelle = titreH + statutH + 2 * pad + N * lh;
      const h = sp.h || Math.min(Math.max(naturelle, 240), 720);
      const cap = Math.max(3, Math.floor((h - titreH - statutH - 2 * pad) / lh));
      n.cfg = { taille, lh, titreH, statutH, pad, chiffres, cap, gut: chiffres * AV * taille + 40, ecritMin: false };
      n.lw = lw; n.lh = h;
    },
    peindre(ctx, n, E, opts, t) { peindreCode(ctx, n, E, t); },
  };

  /* état du code à l'instant t : lignes présentes, caractères visibles, curseur, rangées */
  function etatCode(n, t) {
    const N = n.lignes.length, present = new Uint8Array(N), vis = new Int32Array(N), rang = new Int32Array(N);
    const ty = n.segs.map(s => tapes(s, t));
    for (let k = 0; k < N; k++) {
      const c = n.cov[k], len = n.lignes[k].texte.length;
      if (!c) { present[k] = 1; vis[k] = len; continue; }
      const x = ty[c.s];
      if (x >= c.off && x >= 0) { present[k] = 1; vis[k] = borner(x - c.off, 0, len); }
    }
    let r = 0;
    for (let k = 0; k < N; k++) { rang[k] = r; if (present[k]) r++; }
    let cur = null, segCur = -1;
    n.segs.forEach((s, i) => { if (t >= s.t0 && (segCur < 0 || s.t0 >= n.segs[segCur].t0)) segCur = i; });
    if (segCur >= 0) {
      const s = n.segs[segCur];
      let k = s.l0;
      for (let j = s.l0; j <= s.l1; j++) if (present[j]) k = j;
      const clair = t > s.t1 + 0.4;
      cur = { k, col: vis[k], seg: s, repos: clair };
    }
    return { present, vis, rang, cur, lignes: r };
  }
  function scrollCode(n, t) {
    const cap = n.cfg.cap;
    const cible = tt => {
      const e = etatCode(n, tt);
      const maxS = Math.max(0, e.lignes - cap);
      let reg = null;
      for (const r of n.regards) if (r.t <= tt) reg = r;
      if (reg) return borner(e.rang[reg.ligne] - 1, 0, maxS);
      if (!e.cur) return 0;
      return borner(e.rang[e.cur.k] + 2 - cap, 0, maxS);
    };
    return lisse(cible, t);
  }

  function peindreCode(ctx, n, E, t) {
    const P = n.pal, z = n.z, b = n.b, c = n.cfg;
    const S = c.taille * z, LH = c.lh * z, CW = AV * S, TH = c.titreH * z, SH = c.statutH * z, PAD = c.pad * z;
    const e = etatCode(n, t), scroll = scrollCode(n, t);
    fenetre(ctx, b, z, E, P, 18 * z);
    const y0 = b.y + TH, y1 = b.y + b.h - SH, xNum = b.x + c.chiffres * CW + 22 * z, xTexte = b.x + c.gut * z + 22 * z;

    /* barre de titre : pastilles, onglet du fichier */
    ctx.fillStyle = P.barre; ctx.fillRect(b.x, b.y, b.w, TH);
    ['#ff5f57', '#febc2e', '#28c840'].forEach((col, i) => { ctx.beginPath(); ctx.arc(b.x + (26 + i * 26) * z, b.y + TH / 2, 7.5 * z, 0, 6.2832); ctx.fillStyle = col; ctx.fill(); });
    const nom = n.spec.fichier || 'cours.typ';
    ctx.font = `400 ${24 * z}px Atkinson, sans-serif`;
    const wNom = ctx.measureText(nom).width, xo = b.x + 120 * z, wo = wNom + 74 * z;
    ctx.fillStyle = P.fond; ctx.fillRect(xo, b.y + 6 * z, wo, TH - 6 * z);
    ctx.fillStyle = P.statut; ctx.fillRect(xo, b.y + 6 * z, wo, 2.5 * z);
    ctx.beginPath(); ctx.roundRect(xo + 16 * z, b.y + TH / 2 - 10 * z, 20 * z, 20 * z, 4 * z); ctx.fillStyle = '#239dad'; ctx.fill();
    ctx.fillStyle = '#ffffff'; ctx.font = `700 ${14 * z}px Atkinson, sans-serif`; ctx.textAlign = 'center'; ctx.fillText(n.langage === 'typst' ? 'T' : n.langage === 'latex' ? 'L' : '#', xo + 26 * z, b.y + TH / 2 + 5 * z);
    ctx.textAlign = 'left'; ctx.font = `400 ${24 * z}px Atkinson, sans-serif`; ctx.fillStyle = P.texte;
    ctx.fillText(nom, xo + 50 * z, b.y + TH / 2 + 8 * z);

    /* zone d'édition */
    ctx.save();
    ctx.beginPath(); ctx.rect(b.x, y0, b.w, y1 - y0); ctx.clip();
    const haut = k => y0 + PAD + (e.rang[k] - scroll) * LH;
    const base = k => haut(k) + LH / 2 + 0.36 * S;
    if (e.cur && e.present[e.cur.k] && !n.spec.sansLigneActive) { ctx.fillStyle = P.ligneActive; ctx.fillRect(b.x, haut(e.cur.k), b.w, LH); }
    for (const h of n.surl) {
      const a = Math.min(doux((t - h.t0) / 0.28), 1 - doux((t - h.t1) / 0.35));
      if (a <= 0.003) continue;
      for (let k = h.a; k <= h.b; k++) {
        if (!e.present[k]) continue;
        ctx.globalAlpha = a * (n.s.o < 1 ? 1 : 1);
        ctx.fillStyle = h.couleur || P.surligne; ctx.fillRect(b.x, haut(k), b.w, LH);
        ctx.fillStyle = h.couleur ? h.couleur : '#ffd046'; ctx.fillRect(b.x, haut(k), 4 * z, LH);
      }
      ctx.globalAlpha = 1;
    }
    ctx.letterSpacing = '0.01px';   // coupe les ligatures : le texte tapé ne change pas de forme en cours de frappe
    n.lignes.forEach((L, k) => {
      if (!e.present[k]) return;
      const yt = haut(k);
      if (yt > y1 || yt + LH < y0) return;
      if (n.spec.numeros !== false) {
        ctx.font = `400 ${S}px ${MONO}`; ctx.textAlign = 'right';
        ctx.fillStyle = e.cur && e.cur.k === k ? P.numActif : P.num;
        ctx.fillText(String(k + 1), xNum, base(k)); ctx.textAlign = 'left';
      }
      for (const r of L.runs) {
        if (r.i0 >= e.vis[k]) break;
        const s = r.s.slice(0, e.vis[k] - r.i0);
        ctx.font = `${GRAS.has(r.c) ? 700 : 400} ${S}px ${MONO}`;
        ctx.fillStyle = P.cls[r.c] || P.texte;
        ctx.fillText(s, xTexte + r.i0 * CW, base(k));
      }
    });
    ctx.letterSpacing = '0px';
    if (e.cur && n.spec.curseur !== false) {
      const visible = !e.cur.repos || Math.floor((t - e.cur.seg.t1) * 2) % 2 === 0;
      if (visible && e.present[e.cur.k]) { ctx.fillStyle = P.curseur; ctx.fillRect(xTexte + e.cur.col * CW, haut(e.cur.k) + LH * 0.14, Math.max(2, 2.6 * z), LH * 0.72); }
    }
    ctx.restore();

    /* compilation : dernier appel passé */
    let dtC = Infinity;
    for (const tc of n.compiles) if (t >= tc) dtC = Math.min(dtC, t - tc);
    if (dtC < 0.6) {
      ctx.fillStyle = CV.alpha(P.ok, 0.26 * Math.pow(1 - dtC / 0.6, 2)); ctx.fillRect(b.x, y0, b.w, y1 - y0);
    }
    if (dtC < 2.2) {
      const cx = b.x + b.w - 74 * z, cy = y0 + 74 * z, r = 38 * z;
      const ap = doux((dtC - 0.2) / 0.25), sortie = 1 - doux((dtC - 1.7) / 0.5);
      if (ap > 0 && sortie > 0) {
        ctx.save(); ctx.globalAlpha = ap * sortie;
        ctx.beginPath(); ctx.arc(cx, cy, r * (0.8 + 0.2 * ap), 0, 6.2832); ctx.fillStyle = P.ok; ctx.fill();
        coche(ctx, cx, cy, r * 0.85, doux((dtC - 0.3) / 0.3), '#ffffff', 7 * z);
        ctx.restore();
      }
    }

    /* barre d'état */
    ctx.fillStyle = P.statut; ctx.fillRect(b.x, y1, b.w, SH);
    ctx.font = TEXTE_UI(z); ctx.fillStyle = P.statutTexte; ctx.textAlign = 'left';
    ctx.fillText(n.spec.branche || 'main', b.x + 22 * z, y1 + SH / 2 + 7.5 * z);
    const xChip = b.x + 130 * z;
    if (dtC < Infinity || n.spec.statutInitial) {
      const comp = dtC < 0.45, texte = dtC === Infinity ? n.spec.statutInitial : comp ? 'Compilation…' : 'Compilé';
      const w = ctx.measureText(texte).width + 56 * z;
      ctx.beginPath(); ctx.roundRect(xChip, y1 + 7 * z, w, SH - 14 * z, 6 * z); ctx.fillStyle = dtC === Infinity ? 'rgba(255,255,255,0.18)' : comp ? 'rgba(255,255,255,0.22)' : '#16825d'; ctx.fill();
      ctx.fillStyle = '#ffffff'; ctx.fillText(texte, xChip + 40 * z, y1 + SH / 2 + 7.5 * z);
      if (dtC !== Infinity && !comp) coche(ctx, xChip + 20 * z, y1 + SH / 2, 9 * z, 1, '#ffffff', 3 * z);
      else if (comp) { ctx.save(); ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3 * z; ctx.lineCap = 'round'; ctx.beginPath(); const a0 = t * 9; ctx.arc(xChip + 20 * z, y1 + SH / 2, 8 * z, a0, a0 + 4.2); ctx.stroke(); ctx.restore(); }
    }
    ctx.textAlign = 'right';
    const pos = e.cur ? `Ln ${e.cur.k + 1}, Col ${e.cur.col + 1}` : 'Ln 1, Col 1';
    ctx.fillText(`${pos}     UTF-8     ${n.spec.statut || (n.langage === 'typst' ? 'Typst' : n.langage === 'latex' ? 'LaTeX' : n.langage)}`, b.x + b.w - 22 * z, y1 + SH / 2 + 7.5 * z);
    ctx.textAlign = 'left';
    ctx.restore();
    ctx.save();
    ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, 18 * z); ctx.lineWidth = 1.5 * z; ctx.strokeStyle = P.bord; ctx.stroke();
    ctx.restore();
  }

  /* =====================================================================
     Élément « terminal »
     ===================================================================== */
  CV.TYPES.terminal = {
    tailleLibre: true, dynamique: true,
    creer(n, E) {
      const sp = n.spec;
      n.E = E;
      n.pal = PAL[sp.clair ? 'clair' : 'sombre'];
      n.rows = [];
      n.resoudre = tt => {
        const rows = [];
        const inv = sp.invite || '$';
        (sp.terminal || []).forEach((it, idx) => {
          if (it.cmd !== undefined) {
            const texte = String(it.cmd), t0 = tt(it.de !== undefined ? it.de : it.t);
            let t1 = it.a !== undefined ? tt(it.a) : t0 + texte.length / (it.vitesse || 16);
            if (t1 < t0 + 0.2) t1 = t0 + 0.2;
            rows.push({ k: 'cmd', texte, t0, t1, tot: texte.length, cum: poidsFrappe(texte, idx + 11), invite: it.invite || inv, runs: analyser(texte, 'bash')[0].runs });
          } else {
            for (const kind of ['sortie', 'ok', 'erreur']) {
              if (it[kind] === undefined) continue;
              const t0 = tt(it.t !== undefined ? it.t : it.de), cad = it.cadence ?? 0.12;
              String(it[kind]).split('\n').forEach((s, i) => rows.push({ k: kind, texte: s, t0: t0 + i * cad }));
            }
          }
        });
        n.rows = rows;
      };
    },
    mesurer(n, W) {
      const sp = n.spec, lw = Math.min(sp.l || W, W);
      const cols = Math.max(12, ...(sp.terminal || []).flatMap(it => {
        const s = it.cmd !== undefined ? '$ ' + it.cmd : String(it.sortie ?? it.ok ?? it.erreur ?? '');
        return s.split('\n').map(x => x.length + 4);
      }));
      let taille = sp.taille || 28;
      taille = Math.max(16, Math.min(taille, (lw - 64) / (AV * cols)));
      const lh = Math.round(taille * 1.5), titreH = 46, pad = 14;
      const nb = (sp.terminal || []).reduce((a, it) => a + (it.cmd !== undefined ? 1 : String(it.sortie ?? it.ok ?? it.erreur ?? '').split('\n').length), 0);
      const h = sp.h || Math.min(Math.max(titreH + 2 * pad + nb * lh, 160), 420);
      n.cfg = { taille, lh, titreH, pad, cap: Math.max(2, Math.floor((h - titreH - 2 * pad) / lh)) };
      n.lw = lw; n.lh = h;
    },
    peindre(ctx, n, E, opts, t) { peindreTerminal(ctx, n, E, t); },
  };

  function peindreTerminal(ctx, n, E, t) {
    const P = n.pal, z = n.z, b = n.b, c = n.cfg;
    const S = c.taille * z, LH = c.lh * z, CW = AV * S, TH = c.titreH * z, PAD = c.pad * z;
    const rows = n.rows.filter(r => t >= (r.k === 'cmd' ? r.t0 : r.t0));
    const cap = c.cap;
    const maxS = Math.max(0, rows.length - cap);
    const defile = lisse(tt => Math.min(maxS, Math.max(0, n.rows.filter(r => tt >= r.t0).length - cap)), t);
    fenetre(ctx, b, z, E, P, 16 * z);
    ctx.fillStyle = P.fond; ctx.fillRect(b.x, b.y, b.w, b.h);
    ctx.fillStyle = P.barre; ctx.fillRect(b.x, b.y, b.w, TH);
    ctx.font = `400 ${20 * z}px Atkinson, sans-serif`; ctx.textAlign = 'left';
    const onglets = ['PROBLÈMES', 'SORTIE', 'TERMINAL'];
    let x = b.x + 24 * z;
    for (const o of onglets) {
      const actif = o === 'TERMINAL', w = ctx.measureText(o).width;
      ctx.fillStyle = actif ? P.texte : P.doux; ctx.fillText(o, x, b.y + TH / 2 + 7 * z);
      if (actif) { ctx.fillStyle = P.statut; ctx.fillRect(x, b.y + TH - 3 * z, w, 3 * z); }
      x += w + 34 * z;
    }
    ctx.save();
    ctx.beginPath(); ctx.rect(b.x, b.y + TH, b.w, b.h - TH); ctx.clip();
    ctx.letterSpacing = '0.01px';
    const xt = b.x + 26 * z;
    let derniere = rows.length - 1;
    rows.forEach((r, i) => {
      const yb = b.y + TH + PAD + (i - defile) * LH + LH / 2 + 0.36 * S;
      if (yb < b.y + TH - LH || yb > b.y + b.h + LH) return;
      ctx.font = `400 ${S}px ${MONO}`;
      if (r.k === 'cmd') {
        const ty = tapes(r, t), vis = borner(ty, 0, r.tot);
        ctx.fillStyle = P.ok; ctx.fillText(r.invite + ' ', xt, yb);
        const x0 = xt + (r.invite.length + 1) * CW;
        for (const run of r.runs) {
          if (run.i0 >= vis) break;
          ctx.fillStyle = P.cls[run.c] || P.texte;
          ctx.fillText(run.s.slice(0, vis - run.i0), x0 + run.i0 * CW, yb);
        }
        if (i === derniere) {
          const encore = t < r.t1 + 0.3, clig = Math.floor((t - r.t1) * 2) % 2 === 0;
          if (encore || clig) { ctx.fillStyle = P.curseur; ctx.fillRect(x0 + vis * CW, yb - 0.75 * S, Math.max(2, 2.6 * z), 0.95 * S); }
        }
      } else if (r.k === 'sortie') {
        ctx.fillStyle = P.sortie; ctx.fillText(r.texte, xt, yb);
      } else {
        const col = r.k === 'ok' ? P.ok : P.erreur;
        if (r.k === 'ok') coche(ctx, xt + 0.45 * S, yb - 0.3 * S, 0.5 * S, doux((t - r.t0) / 0.25), col, Math.max(2, 3 * z));
        else croix(ctx, xt + 0.45 * S, yb - 0.3 * S, 0.5 * S, col, Math.max(2, 3 * z));
        ctx.fillStyle = col; ctx.fillText(r.texte, xt + 1.8 * CW, yb);
      }
    });
    ctx.letterSpacing = '0px';
    ctx.restore();
    ctx.restore();
    ctx.save();
    ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, 16 * z); ctx.lineWidth = 1.5 * z; ctx.strokeStyle = P.bord; ctx.stroke();
    ctx.restore();
  }

  /* =====================================================================
     Gabarits de mise en page « tutoriel logiciel »
     ===================================================================== */
  CV.GABARITS['code-rendu'] = {
    bandeau: { x: 60, y: 34, l: 1800, h: 80 },
    code: { x: 40, y: 134, l: 1060, h: 896 },
    rendu: { x: 1130, y: 134, l: 750, h: 896 },
  };
  CV.GABARITS['code-terminal-rendu'] = {
    bandeau: { x: 60, y: 34, l: 1800, h: 80 },
    code: { x: 40, y: 134, l: 1060, h: 590 },
    terminal: { x: 40, y: 748, l: 1060, h: 282 },
    rendu: { x: 1130, y: 134, l: 750, h: 896 },
  };

  /* =====================================================================
     Branchement dans le moteur sans le modifier : ancres et gestes
     ===================================================================== */
  const ancres0 = CV.ancres;
  CV.ancres = function (T, TF, erreur) {
    const A = ancres0.call(this, T, TF, erreur);
    A._TF = TF || [];
    return A;
  };

  const gestes0 = CV.creerGestes;
  CV.creerGestes = function (E, tl, A) {
    const C = gestes0.call(this, E, tl, A);
    for (const n of E.noeuds) if (n.resoudre && (n.type === 'code' || n.type === 'terminal')) n.resoudre(A.temps);

    /* C.compile(cible, t, { rendu, remplace, zoom, delai }) : flash, coche, puis le rendu apparaît (et zoome) */
    C.compile = (cible, t, o = {}) => {
      const n = C.un(cible);
      if (!n || n.type !== 'code') { E.erreur('compile : élément « code » introuvable : ' + cible); return; }
      const t0 = A.temps(t), d = o.delai ?? 0.5;
      n.compiles.push(t0);
      if (o.remplace) C.cache(o.remplace, t0 + d - 0.1, { y: 0, scale: 0.98 });
      if (o.rendu) {
        C.montre(o.rendu, t0 + d, { y: 0, scale: 0.96, dur: 0.7, ease: 'power2.out' });
        if (o.zoom) C.zoom(o.rendu, t0 + d + (o.zoom.apres ?? 1.0), Object.assign({ dur: 2.5 }, o.zoom));
      }
    };

    /* C.badgeVoix({ voix: 'tom', texte: 'Voix de synthèse' }) : étiquette visible seulement pendant les temps forts de cette voix */
    C.badgeVoix = (o = {}) => {
      const voix = o.voix || 'tom', texte = o.texte || 'Voix de synthèse', tm = o.taille || 26;
      const plages = (A._TF || []).filter(b => b.voix === voix).map(b => [b.debut, b.fin]);
      if (!plages.length) E.erreur(`badgeVoix : aucun temps fort de voix « ${voix} » (data/temps-forts.js, champ voix)`);
      // plages voisines (moins de 0,6 s) fusionnées : pas de clignotement entre deux phrases d'une même voix
      const fus = [];
      plages.sort((a, b) => a[0] - b[0]).forEach(p => { const d = fus[fus.length - 1]; if (d && p[0] - d[1] < 0.6) d[1] = Math.max(d[1], p[1]); else fus.push(p.slice()); });
      const it = C.ajouter((ctx, EE, s, tt) => {
        let a = 0;
        for (const [d, f] of fus) a = Math.max(a, Math.min(doux((tt - d + 0.12) / 0.3), 1 - doux((tt - f - 0.1) / 0.35)));
        if (a <= 0.003) return;
        const th = EE.theme;
        ctx.save(); ctx.globalAlpha *= a;
        ctx.font = `400 ${tm}px Atkinson, sans-serif`;
        const w = ctx.measureText(texte).width + 2 * 18 + 50, h = tm + 22, x = 1920 - 34 - w, y = 1080 - 20 - h;
        ctx.beginPath(); ctx.roundRect(x, y, w, h, h / 2); ctx.fillStyle = 'rgba(5,8,20,0.66)'; ctx.fill();
        ctx.lineWidth = 1.5; ctx.strokeStyle = th.trait; ctx.stroke();
        // trois barres d'onde, animées par le temps
        for (let i = 0; i < 3; i++) {
          const hh = 6 + 9 * (0.5 + 0.5 * Math.sin(tt * 9 + i * 1.7));
          ctx.fillStyle = th.cyan; ctx.beginPath(); ctx.roundRect(x + 20 + i * 8, y + h / 2 - hh / 2, 4.5, hh, 2); ctx.fill();
        }
        ctx.fillStyle = th.texte; ctx.textBaseline = 'alphabetic';
        ctx.fillText(texte, x + 18 + 40, y + h / 2 + tm * 0.34);
        ctx.restore();
      });
      it.dessus = true;
    };
    return C;
  };
})(typeof self !== 'undefined' ? self : this);
