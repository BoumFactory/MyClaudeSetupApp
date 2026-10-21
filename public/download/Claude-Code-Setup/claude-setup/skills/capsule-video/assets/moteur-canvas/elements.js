/* =====================================================================
   Éléments typés du moteur canvas : création, mise en page, peinture
   ---------------------------------------------------------------------
   Un élément de spec.js est un objet dont UNE clé donne le type :
     { texte }, { surTitre }, { titre }, { tex }, { carte }, { puce },
     { ligne }, { colonne }, { pile }, { figure }, { calcul }, { grille },
     { tableau }, { icone }, { espace }, { dessin }
   (une simple chaîne = { texte }). Clés communes : id, taille, couleur,
   align (dans une colonne : gauche | centre | droite | etire), l, h, et
   les raccourcis de gestes (montre, ecrit, tombe, cache, apparait, trace).

   Mise en page en trois temps, toujours au zoom 1 (repère 1920×1080) :
     mesurer(n, W)  taille naturelle sous une largeur maximale W
     disposer(n)    position des enfants une fois la largeur fixée (n.lw)
     placer(n, x, y, z)  boîtes absolues n.b après le zoom z de la zone
   Le zoom de chaque zone est cherché pour que TOUT tienne (texte réduit
   au besoin) : aucun débordement possible.
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});

  CV.etatInitial = () => ({ x: 0, y: 0, scale: 1, scaleX: 1, scaleY: 1, rotation: 0, o: 1,
    clip: 1, trace: 1, lum: 1, sat: 1, flou: 0, pliage: 1, lev: 0 });

  function Noeud(type, spec, parent, E) {
    this.type = type; this.spec = spec; this.parent = parent; this.enfants = [];
    this.id = spec.id || null;
    this.s = CV.etatInitial();
    this.b = { x: 0, y: 0, w: 0, h: 0 }; this.z = 1;
    this.lx = 0; this.ly = 0; this.lw = 0; this.lh = 0;
    this.classes = spec.classe ? String(spec.classe).split(/\s+/) : [];
    if (this.id) {
      if (E.ids.has(this.id)) E.erreur('id en double : ' + this.id);
      else E.ids.set(this.id, this);
    }
    E.noeuds.push(this);
  }
  CV.Noeud = Noeud;

  CV.TYPES = {};
  // les conteneurs d'abord : une carte peut avoir une clé « titre » (étiquette) ou « puce »
  // (composants.js ajoute ses types : methode, encadrer, resultat, lettre, image…)
  CV.CLES = ['carte', 'ligne', 'colonne', 'pile', 'figure', 'calcul', 'grille', 'tableau', 'puce',
    'surTitre', 'titre', 'texte', 'tex', 'icone', 'espace', 'dessin'];

  CV.creerNoeud = (spec, parent, E) => {
    if (typeof spec === 'string') spec = { texte: spec };
    else if (typeof spec === 'number') spec = { tex: String(spec) };
    let type = CV.CLES.find(t => spec[t] !== undefined);
    if (!type) { E.erreur('Élément sans type reconnu : ' + JSON.stringify(spec).slice(0, 90)); type = 'espace'; spec = { espace: 0 }; }
    const n = new Noeud(type, spec, parent, E);
    CV.TYPES[type].creer(n, E);
    return n;
  };
  const enfantsDe = (n, liste, E) => {
    (Array.isArray(liste) ? liste : [liste]).filter(x => x !== null && x !== undefined && x !== false)
      .forEach(c => n.enfants.push(CV.creerNoeud(c, n, E)));
  };

  /* propriété héritée des conteneurs (taille, gras…) */
  CV.herite = (n, cle) => {
    for (let p = n; p; p = p.parent) if (p.spec && p.spec[cle] !== undefined) return p.spec[cle];
    return undefined;
  };

  /* Préréglages de taille des formules (clé `formules` de la capsule, d'une scène ou d'un conteneur).
     ratio : formule sans taille dans un conteneur à `taille` t → ratio × t ; defaut : sans aucune taille héritée ;
     padV : respiration au-dessus et au-dessous de chaque formule (fraction de sa taille) ;
     ecartCarte / ecartGrille : écarts par défaut ; resultat : taille par défaut de la pilule resultat ;
     figurePanneau : retouches du gabarit figure-panneau. Clé absente = 'actuel' (comportement historique). */
  CV.PRESETS_FORMULES = {
    actuel: { ratio: 1.1, defaut: 66, padV: 0, ecartCarte: 12, ecartGrille: [12, 14], resultat: 62, figurePanneau: null },
    grandes: { ratio: 1.6, defaut: 66, padV: 0, ecartCarte: 12, ecartGrille: [12, 14], resultat: 62, figurePanneau: null },
    compactes: { ratio: 1.1, defaut: 44, padV: 0.12, ecartCarte: 16, ecartGrille: [14, 14], resultat: 46,
      figurePanneau: { figure: { x: 40, y: 136, l: 960, h: 480 }, 'sous-figure': { x: 40, y: 700, l: 960, h: 350, ecart: 14 } } },
  };
  const cacheFormules = new Map();
  CV.reglageFormules = (v, E) => {
    if (v === undefined || v === null) return Object.assign({ nom: 'actuel' }, CV.PRESETS_FORMULES.actuel);
    const cle = typeof v === 'string' ? v : JSON.stringify(v);
    if (cacheFormules.has(cle)) return cacheFormules.get(cle);
    const noms = Object.keys(CV.PRESETS_FORMULES);
    const base = typeof v === 'string' ? v : (v.base || 'actuel');
    let P = CV.PRESETS_FORMULES[base];
    if (!P) {
      if (E) E.erreur('formules : préréglage inconnu « ' + base + ' » (connus : ' + noms.join(', ') + ')');
      P = CV.PRESETS_FORMULES.actuel;
    }
    const r = Object.assign({ nom: P === CV.PRESETS_FORMULES[base] ? base : 'actuel' }, P, typeof v === 'object' ? v : {});
    delete r.base;
    cacheFormules.set(cle, r);
    return r;
  };
  /* réglage qui s'applique au nœud n : le plus proche conteneur (carte, scène…) qui porte `formules`, sinon la capsule */
  CV.formulesDe = (n, E) => {
    const v = n ? CV.herite(n, 'formules') : undefined;
    return v !== undefined ? CV.reglageFormules(v, E) : (E && E.formules) || CV.reglageFormules(undefined);
  };
  const accentCarte = (n, E) => {
    for (let p = n; p; p = p.parent) if ((p.type === 'carte' || p.type === 'puce') && p.spec.couleur) return CV.couleur(E.theme, p.spec.couleur);
    return E.theme.ambre;
  };
  const couleurTexte = (n, E) => {
    const c = n.spec.couleur !== undefined && !['carte', 'puce'].includes(n.type) ? n.spec.couleur
      : n.type === 'surTitre' ? 'cyan' : CV.herite(n, 'couleurTexte');
    return c ? CV.couleur(E.theme, c) : E.theme.texte;
  };

  /* ---------- mise en page générique ---------- */
  CV.mesurer = (n, W, E) => {
    const T = CV.TYPES[n.type];
    const libre = T.tailleLibre;
    const Wn = n.spec.l && !libre ? Math.min(n.spec.l, W) : W;
    n.deborde = false;
    T.mesurer(n, Wn, E);
    if (!libre) {
      if (n.spec.l) { if (n.lw > n.spec.l + 0.5 || n.spec.l > W + 0.5) n.deborde = true; n.lw = Math.min(n.spec.l, W); }
      if (n.spec.h) n.lh = Math.max(n.spec.h, n.lh);   // h = hauteur minimale (min-height) : le contenu ne déborde jamais
    }
    if (n.lw > W + 0.5) n.deborde = true;
    n.nw = n.lw;
    for (const c of n.enfants) if (c.deborde) n.deborde = true;
  };
  CV.disposer = (n, E) => {
    const T = CV.TYPES[n.type];
    if (T.disposer) T.disposer(n, E);
  };
  /* (x, y) = coin haut-gauche absolu de n ; z = zoom de son sous-arbre */
  CV.placer = (n, x, y, z) => {
    n.z = z;
    n.b = { x, y, w: n.lw * z, h: n.lh * z };
    for (const c of n.enfants) CV.placer(c, x + c.lx * z, y + c.ly * z, c.zoomPropre || z);
    const T = CV.TYPES[n.type];
    if (T.apresPlacer) T.apresPlacer(n);
  };
  /* raccourcis de gestes utilisables comme clés d'un élément : { texte: '…', montre: '@b03~"codage"' } */
  CV.RACCOURCIS = ['montre', 'ecrit', 'tombe', 'cache', 'apparait', 'trace', 'pulse', 'surligne', 'compte'];
  const etirable = c => {
    const a = c.spec.align;
    if (a) return a === 'etire';
    return !['puce', 'icone', 'tex', 'tuiles', 'produit', 'tapis'].includes(c.type);
  };
  CV.etirable = etirable;

  /* ---------- texte ---------- */
  function optionsTexte(n, E) {
    const sp = n.spec;
    const o = { taille: sp.taille ?? CV.herite(n, 'taille') ?? 40, interligne: sp.interligne ?? 1.3,
      tailleTex: sp.tailleTex ?? 1.1, nowrap: !!sp.nowrap, espacement: 0, majuscules: !!sp.majuscules,
      formule: tex => E.prep.formule(tex, false) };
    if (sp.espacementLettres) o.espacement = sp.espacementLettres * o.taille;   // en em, comme letter-spacing
    if (n.type === 'surTitre') { o.taille = sp.taille ?? 30; o.majuscules = true; o.espacement = 0.18 * o.taille; }
    if (n.type === 'titre') { o.taille = sp.taille ?? 92; o.interligne = sp.interligne ?? 1.05; o.espacement = -0.01 * o.taille; }
    if (n.type === 'puce') { o.taille = sp.taille ?? 32; o.nowrap = true; }
    if (n.type === 'icone') { o.taille = sp.taille ?? 80; o.nowrap = true; }
    return o;
  }
  function styleBase(n) {
    const sp = n.spec;
    const gras = sp.gras ?? CV.herite(n, 'gras') ?? (['surTitre', 'titre', 'puce'].includes(n.type));
    return { gras, it: !!(sp.it ?? CV.herite(n, 'it')), coul: sp.doux ? 'doux' : undefined, tab: !!(sp.tab ?? CV.herite(n, 'tab')) };
  }
  function creerTexte(n, E) {
    const src = n.spec[n.type];
    n.analyse = CV.analyserTexte(src, n.spec.decoupe);
    const base = styleBase(n);
    n.analyse.atomes.forEach(a => { a.st = Object.assign({}, base, a.st); if (!a.st.coul && base.coul) a.st.coul = base.coul; });
    // morceaux visables : un nœud par [..]{#id}, imbriqués comme dans le texte
    const parId = {};
    for (const sp of n.analyse.spans) {
      const parent = sp.parent ? parId[sp.parent] : n;
      const m = new Noeud('morceau', { id: sp.id }, parent, E);
      m.para = n; m.horsFlux = false;
      parent.enfants.push(m);
      parId[sp.id] = m;
    }
  }
  function mesurerTexte(n, W, E) {
    n.comp = CV.composerTexte(n.analyse, W, optionsTexte(n, E));
    n.lw = n.comp.w; n.lh = n.comp.h;
    n.base = n.comp.lignes.length ? n.comp.lignes[0].y : n.lh * 0.8;   // ligne de base (alignement « base » d'une ligne)
    if (n.comp.deborde) n.deborde = true;
  }
  /* remplissage d'un texte : dégradé de tout le paragraphe (degrade: ['ambre', 'rose'], à 120°) ou couleur */
  /* extrémités d'un linear-gradient(120deg) CSS sur une boîte : [x0, y0, x1, y1] */
  CV.extremitesDegrade = (b, deg = 120) => {
    const a = deg * Math.PI / 180, dx = Math.sin(a), dy = -Math.cos(a);
    const L = Math.abs(b.w * dx) + Math.abs(b.h * dy), cx = b.x + b.w / 2, cy = b.y + b.h / 2;
    return [cx - dx * L / 2, cy - dy * L / 2, cx + dx * L / 2, cy + dy * L / 2];
  };
  CV.remplissageTexte = (ctx, para, E, coul, boite) => {
    const d = para.spec.degrade;
    if (!d) return coul;
    const g = ctx.createLinearGradient(...CV.extremitesDegrade(boite || para.b));
    const cs = d.map(c => CV.couleur(E.theme, c));
    cs.forEach((c, i) => g.addColorStop(cs.length > 1 ? i / (cs.length - 1) : 0, c));
    return g;
  };
  /* lueur d'un texte (text-shadow 0 0 Xpx couleur 45 %) : lueur: true (30 px) ou nombre de px */
  CV.lueurTexte = (ctx, para, coul) => {
    const l = para.spec.lueur;
    if (!l) return;
    ctx.shadowColor = CV.mix(coul, para.spec.lueurForce ?? 0.45);
    ctx.shadowBlur = (l === true ? 30 : l) * para.z * (ctx.getTransform().a || 1);
  };
  function disposerTexte(n) {
    const al = n.spec.alignTexte || (n.spec.align === 'centre' ? 'centre' : n.spec.align === 'droite' ? 'droite' : 'gauche');
    n.items = [];
    const grad = {};
    for (const L of n.comp.lignes) {
      const dx = al === 'centre' ? (n.lw - L.w) / 2 : al === 'droite' ? n.lw - L.w : 0;
      for (const b of L.items) {
        if (b.esp) continue;
        const it = { b, x: dx + b.x, y: L.y, w: b.w, proprio: b.a.spans.length ? b.a.spans[b.a.spans.length - 1] : null };
        const m = b.f ? null : CV.metriques(b.police);
        it.haut = b.f ? b.asc : m.asc; it.bas = b.f ? b.desc : m.desc;
        n.items.push(it);
        if (b.a.st.grad) {
          const g = grad[b.a.st.grad] || (grad[b.a.st.grad] = { x0: Infinity, x1: -Infinity });
          g.x0 = Math.min(g.x0, it.x); g.x1 = Math.max(g.x1, it.x + it.w);
        }
      }
    }
    n.grad = grad;
    // boîtes des morceaux (repère du paragraphe), puis relatives à leur parent
    const boites = {};
    for (const it of n.items) for (const id of it.b.a.spans) {
      const bb = boites[id] || (boites[id] = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity });
      bb.x0 = Math.min(bb.x0, it.x); bb.x1 = Math.max(bb.x1, it.x + it.w);
      bb.y0 = Math.min(bb.y0, it.y - it.haut); bb.y1 = Math.max(bb.y1, it.y + it.bas);
    }
    const poser = (p, ox, oy) => {
      for (const m of p.enfants) {
        if (m.type !== 'morceau') continue;
        const bb = boites[m.id] || { x0: 0, y0: 0, x1: 0, y1: 0 };
        m.lx = bb.x0 - ox; m.ly = bb.y0 - oy; m.lw = bb.x1 - bb.x0; m.lh = bb.y1 - bb.y0;
        m.ax = bb.x0; m.ay = bb.y0;
        poser(m, bb.x0, bb.y0);
      }
    };
    poser(n, 0, 0);
  }
  /* peint les items d'un paragraphe appartenant à `proprio` (null = hors morceau) */
  function peindreItems(ctx, para, proprio, E, opts) {
    const z = para.z, ox = para.b.x, oy = para.b.y, base = couleurTexte(para, E);
    const taille = para.comp.taille;
    for (const it of para.items) {
      if (it.proprio !== proprio && !(opts && opts.tout && proprio === null)) continue;
      if (opts && opts.dans && !it.b.a.spans.includes(opts.dans)) continue;
      const st = it.b.a.st;
      let coul = st.coul === 'accent-carte' ? accentCarte(para, E) : st.coul ? CV.couleur(E.theme, st.coul) : base;
      if (opts && opts.couleur) coul = opts.couleur;
      const x = ox + it.x * z, y = oy + it.y * z;
      if (!(opts && opts.lueur)) CV.lueurTexte(ctx, para, coul);
      if (it.b.f) { CV.peindreFormule(ctx, it.b.f, x, y, it.b.tt * z, coul, null); continue; }
      ctx.font = CV.police(taille * z, st);
      ctx.letterSpacing = (para.comp.espacement * z) + 'px';
      if (st.grad && !(opts && opts.couleur)) {
        const g = para.grad[st.grad];
        const lg = ctx.createLinearGradient(ox + g.x0 * z, 0, ox + g.x1 * z, 0);
        lg.addColorStop(0, E.theme.ambre); lg.addColorStop(0.5, E.theme.rose); lg.addColorStop(1, E.theme.violet);
        ctx.fillStyle = lg;
      } else ctx.fillStyle = opts && opts.couleur ? coul : CV.remplissageTexte(ctx, para, E, coul);
      ctx.fillText(it.b.s, x, y);
    }
    ctx.letterSpacing = '0px';
    if (!(opts && opts.lueur)) { ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; }
  }
  CV.peindreItems = peindreItems;

  const typeTexte = {
    creer: creerTexte, mesurer: mesurerTexte, disposer: disposerTexte, sprite: true,
    marge: n => 14 + (n.spec.lueur ? (n.spec.lueur === true ? 30 : n.spec.lueur) * 1.6 : 0),
    peindre: (ctx, n, E, opts) => peindreItems(ctx, n, null, E, opts),
  };
  CV.TYPES.texte = typeTexte;
  CV.TYPES.surTitre = typeTexte;
  CV.TYPES.titre = typeTexte;
  CV.TYPES.morceau = {
    creer() {}, mesurer() {}, sprite: true, marge: 14,
    peindre: (ctx, n, E, opts) => peindreItems(ctx, n.para, n.id, E, opts),
    /* pour un clone (vole) : tout le contenu du morceau, morceaux imbriqués compris */
    peindreTout: (ctx, n, E, opts) => {
      const z = n.para.z;
      for (const it of n.para.items) if (it.b.a.spans.includes(n.id)) {
        const o = Object.assign({}, opts, { dans: n.id });
        peindreItems(ctx, n.para, it.proprio, E, o);
      }
      void z;
    },
  };

  /* ---------- formule (MathJax → chemins) ---------- */
  const DOM = typeof DOMMatrix !== 'undefined' ? DOMMatrix : null;
  CV.peindreFormule = (ctx, f, x, yBase, taille, couleur, filtre) => {
    ctx.save();
    ctx.translate(x, yBase);
    ctx.scale(taille, taille);
    const parCouleur = new Map();
    for (const op of f.ops) {
      if (filtre && !filtre(op)) continue;
      const c = op.c || couleur;
      if (op.t === 'p' || op.t === 'r') {
        let p = parCouleur.get(c);
        if (!p) { p = new Path2D(); parCouleur.set(c, p); }
        const m = new DOM(op.m);
        if (op.t === 'p') p.addPath(new Path2D(op.d), m);
        else { const r = new Path2D(); r.rect(op.x, op.y, op.w, op.h); p.addPath(r, m); }
      } else if (op.t === 'l') {
        ctx.save(); ctx.transform(...op.m); ctx.strokeStyle = c; ctx.lineWidth = op.e || 40;
        ctx.beginPath(); ctx.moveTo(op.x1, op.y1); ctx.lineTo(op.x2, op.y2); ctx.stroke(); ctx.restore();
      } else if (op.t === 'x') {
        ctx.save(); ctx.transform(...op.m); ctx.font = op.f; ctx.fillStyle = c; ctx.fillText(op.s, 0, 0); ctx.restore();
      }
    }
    for (const [c, p] of parCouleur) { ctx.fillStyle = c; ctx.fill(p); }
    ctx.restore();
  };
  const tailleTex = (n, E) => {
    if (n.spec.taille !== undefined) return n.spec.taille;
    const tt = CV.herite(n, 'tailleTex');
    if (tt !== undefined) return tt;
    const P = CV.formulesDe(n, E), t = CV.herite(n, 'taille');
    return t ? t * P.ratio : P.defaut;
  };
  CV.TYPES.tex = {
    creer(n, E) {
      n.f = E.prep.formule(String(n.spec.tex), !!n.spec.display);
      if (n.f.erreur) E.erreur('Formule « ' + n.spec.tex + ' » : ' + n.f.erreur);
      // sous-parties \cssId : un nœud par id, imbriqués selon l'ordre des ids des chemins
      const parents = {};
      for (const op of n.f.ops) {
        const ids = op.ids.filter(i => i[0] !== '.');
        op.proprio = ids.length ? ids[ids.length - 1] : null;
        ids.forEach((id, j) => { if (!(id in parents)) parents[id] = j ? ids[j - 1] : null; });
      }
      const noeuds = {};
      const creerPart = id => {
        if (noeuds[id]) return noeuds[id];
        const par = parents[id] ? creerPart(parents[id]) : n;
        const m = new Noeud('part', { id }, par, E);
        m.formule = n; par.enfants.push(m); noeuds[id] = m;
        return m;
      };
      Object.keys(parents).forEach(creerPart);
      n.parts = noeuds;
    },
    mesurer(n, W, E) {
      const t = tailleTex(n, E);
      n.taille = t;
      // respiration verticale (préréglage `formules`) ; jamais sur une étiquette de figure (placée par son centre)
      const padV = n.parent && n.parent.type === 'figure' ? 0 : Math.round(t * CV.formulesDe(n, E).padV);
      n.asc = Math.max(n.f.asc, 0.75) * t + padV; n.desc = Math.max(n.f.desc, 0.25) * t + padV;
      n.lw = n.f.w * t; n.lh = n.asc + n.desc;
    },
    disposer(n) {
      const poser = (p, ox, oy) => {
        for (const m of p.enfants) {
          const bb = n.f.parts[m.id] || { x: 0, y: 0, w: 0, h: 0 };
          const ax = bb.x * n.taille, ay = n.asc + bb.y * n.taille;
          m.lx = ax - ox; m.ly = ay - oy; m.lw = bb.w * n.taille; m.lh = bb.h * n.taille;
          poser(m, ax, ay);
        }
      };
      poser(n, 0, 0);
    },
    sprite: true, marge: n => 10 + (n.spec.lueur ? (n.spec.lueur === true ? 30 : n.spec.lueur) * 1.6 : 0),
    peindre: (ctx, n, E, opts) => {
      const coul = opts && opts.couleur || couleurTexte(n, E);
      ctx.save();
      if (!(opts && opts.lueur)) CV.lueurTexte(ctx, n, coul);
      CV.peindreFormule(ctx, n.f, n.b.x, n.b.y + n.asc * n.z, n.taille * n.z, coul, op => (opts && opts.tout) || op.proprio === null);
      ctx.restore();
    },
  };
  CV.TYPES.part = {
    creer() {}, mesurer() {}, sprite: true, marge: 10,
    peindre: (ctx, n, E, opts) => {
      const f = n.formule;
      CV.peindreFormule(ctx, f.f, f.b.x, f.b.y + f.asc * f.z, f.taille * f.z, opts && opts.couleur || couleurTexte(f, E),
        op => (opts && opts.tout) ? op.ids.includes(n.id) : op.proprio === n.id);
    },
  };

  /* ---------- conteneurs ---------- */
  function mesurerColonne(n, W, E, enfants, ecart) {
    let h = 0, w = 0;
    enfants.forEach((c, i) => {
      CV.mesurer(c, W, E);
      h += c.lh + (i ? ecart : 0);
      w = Math.max(w, c.lw);
    });
    return { w, h };
  }
  function disposerColonne(n, E, enfants, ecart, x0, y0, largeur) {
    let y = y0;
    const libre = n.spec.h ? n.lh - (y0 * 2) - enfants.reduce((s, c, i) => s + c.lh + (i ? ecart : 0), 0) : 0;
    const just = n.spec.justifie;
    if (libre > 0 && just === 'centre') y += libre / 2;
    if (libre > 0 && just === 'fin') y += libre;
    const entre = libre > 0 && just === 'entre' && enfants.length > 1 ? libre / (enfants.length - 1) : 0;
    for (const c of enfants) {
      const a = c.spec.align || n.spec.alignEnfants || (etirable(c) && !c.spec.l ? 'etire' : 'gauche');
      if (a === 'etire' && !c.spec.l) c.lw = Math.max(c.lw, largeur);
      c.lx = x0 + (a === 'centre' ? (largeur - c.lw) / 2 : a === 'droite' ? largeur - c.lw : 0);
      c.ly = y;
      y += c.lh + ecart + entre;
      CV.disposer(c, E);
    }
  }
  CV.TYPES.colonne = {
    creer(n, E) { enfantsDe(n, n.spec.colonne, E); },
    mesurer(n, W, E) {
      const r = mesurerColonne(n, W, E, n.enfants, n.spec.ecart ?? 26);
      n.lw = r.w; n.lh = r.h;
    },
    disposer(n, E) { disposerColonne(n, E, n.enfants, n.spec.ecart ?? 26, 0, 0, n.lw); },
  };
  CV.TYPES.ligne = {
    creer(n, E) { enfantsDe(n, n.spec.ligne, E); },
    mesurer(n, W, E) {
      const ec = n.spec.ecart ?? 24, nb = n.enfants.length;
      const dispo = W - ec * Math.max(0, nb - 1);
      if (n.spec.egal) {
        n.enfants.forEach(c => CV.mesurer(c, dispo / nb, E));
      } else {
        n.enfants.forEach(c => CV.mesurer(c, dispo, E));
        const somme = n.enfants.reduce((s, c) => s + c.lw, 0);
        if (somme > dispo + 0.5) {
          // on rétrécit les enfants souples (textes) : les autres gardent leur largeur
          const fixes = n.enfants.filter(c => !['texte', 'carte', 'colonne'].includes(c.type));
          const wFixe = fixes.reduce((s, c) => s + c.lw, 0);
          const souples = n.enfants.filter(c => !fixes.includes(c));
          const wSouple = souples.reduce((s, c) => s + c.lw, 0);
          const reste = Math.max(10, dispo - wFixe);
          souples.forEach(c => CV.mesurer(c, reste * c.lw / wSouple, E));
        }
      }
      n.lw = n.enfants.reduce((s, c) => s + c.lw, 0) + ec * Math.max(0, nb - 1);
      if (n.spec.egal) n.lw = W;
      n.lh = Math.max(0, ...n.enfants.map(c => c.lh));
      const tousTex = nb && n.enfants.every(c => c.type === 'tex');
      if ((tousTex && (n.spec.valign || 'base') === 'base') || n.spec.valign === 'base') {
        // alignement sur la ligne de base (formules : leur ligne de base ; textes : celle de leur 1re ligne)
        const base = c => (c.asc !== undefined ? c.asc : c.base !== undefined ? c.base : c.lh / 2);
        const asc = Math.max(...n.enfants.map(base)), desc = Math.max(...n.enfants.map(c => c.lh - base(c)));
        n.lh = asc + desc;
        if (tousTex) { n.asc = asc; n.desc = desc; } else { n.asc = undefined; n.desc = undefined; n.base = asc; }
      } else { n.asc = undefined; n.desc = undefined; }
      n.deborde = n.deborde || n.lw > W + 0.5;
    },
    disposer(n, E) {
      const ec = n.spec.ecart ?? 24, nb = n.enfants.length;
      if (n.spec.egal) n.enfants.forEach(c => { c.lw = (n.lw - ec * (nb - 1)) / nb; });
      const total = n.enfants.reduce((s, c) => s + c.lw, 0) + ec * Math.max(0, nb - 1);
      const libre = n.lw - total, j = n.spec.justifie;
      let x = j === 'centre' ? libre / 2 : j === 'fin' ? libre : 0;
      const entre = j === 'entre' && nb > 1 ? libre / (nb - 1) : 0;
      const tousTex = n.enfants.every(c => c.type === 'tex');
      const va = n.spec.valign || (tousTex ? 'base' : 'centre');
      const base = c => (c.asc !== undefined ? c.asc : c.base !== undefined ? c.base : c.lh / 2);
      const ascMax = Math.max(0, ...n.enfants.map(base));
      for (const c of n.enfants) {
        c.lx = x;
        c.ly = va === 'haut' ? 0 : va === 'bas' ? n.lh - c.lh : va === 'base' ? ascMax - base(c) : (n.lh - c.lh) / 2;
        x += c.lw + ec + entre;
        CV.disposer(c, E);
      }
    },
  };
  CV.TYPES.pile = {
    creer(n, E) { enfantsDe(n, n.spec.pile, E); },
    mesurer(n, W, E) {
      n.enfants.forEach(c => CV.mesurer(c, W, E));
      n.lw = Math.max(0, ...n.enfants.map(c => c.lw));
      n.lh = Math.max(0, ...n.enfants.map(c => c.lh));
    },
    disposer(n, E) {
      for (const c of n.enfants) {
        if (!c.zoomPropre) { c.lw = etirable(c) || c.type === 'puce' ? n.lw : c.lw; c.lx = 0; c.ly = 0; }
        CV.disposer(c, E);
      }
    },
  };
  CV.TYPES.espace = {
    creer() {}, mesurer(n) { n.lw = 0; n.lh = +n.spec.espace || 0; },
  };

  /* ---------- carte (verre) ---------- */
  const MARGE_CARTE = 130;
  CV.TYPES.carte = {
    creer(n, E) {
      const c = n.spec.carte;
      const liste = [];
      if (n.spec.puce) liste.push({ puce: n.spec.puce, couleur: n.spec.couleur, align: 'gauche' });
      (Array.isArray(c) ? c : [c]).forEach(x => liste.push(x));
      // alignEnfants de la carte → colonne interne (ex. 'centre' : textes centrés sous une icône)
      const col = CV.creerNoeud({ colonne: liste, ecart: n.spec.ecart ?? CV.formulesDe(n, E).ecartCarte, alignEnfants: n.spec.alignEnfants }, n, E);
      n.enfants.push(col);
      n.col = col;
      if (n.spec.titre) {
        n.tag = { comp: null, analyse: CV.analyserTexte(n.spec.titre) };
        n.tag.analyse.atomes.forEach(a => { a.st = Object.assign({ gras: true }, a.st); });
      }
    },
    mesurer(n, W, E) {
      const m = n.spec.marge ?? [28, 36];
      const [mv, mh] = Array.isArray(m) ? m : [m, m];
      n.pad = { h: mh, haut: n.spec.titre ? (n.spec.margeHaut ?? 64) : mv, bas: n.spec.margeBas ?? mv };
      if (n.tag) n.tag.comp = CV.composerTexte(n.tag.analyse, 2000, { taille: 34, interligne: 1.3, nowrap: true, formule: t => E.prep.formule(t, false) });
      CV.mesurer(n.col, W - 2 * mh, E);
      n.lw = n.col.lw + 2 * mh;
      if (n.tag) n.lw = Math.max(n.lw, n.tag.comp.w + 36 + 22 + 20);
      n.lh = n.col.lh + n.pad.haut + n.pad.bas;
    },
    disposer(n, E) {
      n.col.lx = n.pad.h; n.col.ly = n.pad.haut;
      n.col.lw = n.lw - 2 * n.pad.h;
      if (n.spec.h) {
        // carte de hauteur fixée : justifie = centre | fin | entre répartit le contenu (comme justify-content)
        const interieur = n.lh - n.pad.haut - n.pad.bas;
        if (interieur > n.col.lh && n.spec.justifie) {
          n.col.spec = Object.assign({}, n.col.spec, { h: interieur, justifie: n.spec.justifie });
          n.col.lh = interieur;
        }
      }
      CV.disposer(n.col, E);
    },
    sprite: true, marge: MARGE_CARTE,
    peindre(ctx, n, E) {
      const t = E.theme, z = n.z, r = (n.spec.rayon ?? 28) * z;
      const b = n.reduction ? Object.assign({}, n.b, { h: n.b.h - n.reduction.v }) : n.b;   // carte qui rétrécit (compacte)
      const acc = n.spec.couleur ? CV.couleur(t, n.spec.couleur) : null;
      const fond = acc ? CV.mix(acc, 0.12, n.spec.forte ? t.carteForte : t.carte) : (n.spec.forte ? t.carteForte : t.carte);
      const bord = acc ? CV.mix(acc, 0.55) : t.trait;
      CV.ombreCarte(ctx, b.x, b.y, b.w, b.h, r, t.ombre, z);
      ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, r);
      ctx.fillStyle = fond; ctx.fill();
      const e = 1.5 * z;
      ctx.beginPath(); ctx.roundRect(b.x + e / 2, b.y + e / 2, b.w - e, b.h - e, Math.max(0, r - e / 2));
      ctx.lineWidth = e; ctx.strokeStyle = bord; ctx.stroke();
      if (n.tag) {
        const c = n.tag.comp, tx = b.x + 22 * z, ty = b.y + 14 * z;
        const w = (c.w + 36) * z, h = (c.h + 4) * z;
        ctx.beginPath(); ctx.roundRect(tx, ty, w, h, 8 * z);
        ctx.fillStyle = t.tag; ctx.fill();
        ctx.lineWidth = 1.5 * z; ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.stroke();
        ctx.fillStyle = '#ffffff';
        CV.peindreComp(ctx, c, tx + 18 * z, ty + 2 * z, z, '#ffffff', E);
      }
    },
  };
  /* ombre portée « box-shadow » : visible seulement HORS de la boîte, comme en CSS */
  CV.ombreCarte = (ctx, x, y, w, h, r, ombre, z) => {
    ctx.save();
    const ext = new Path2D();
    const m = (ombre.flou + ombre.y) * 2 * z;
    ext.rect(x - m, y - m, w + 2 * m, h + 2 * m);
    const int = new Path2D(); int.roundRect(x, y, w, h, r);
    ext.addPath(int);
    ctx.clip(ext, 'evenodd');
    ctx.shadowColor = ombre.couleur; ctx.shadowBlur = ombre.flou * z * (ctx.getTransform().a || 1);
    ctx.shadowOffsetY = ombre.y * z * (ctx.getTransform().d || 1);
    ctx.fillStyle = '#000';
    ctx.fill(int);
    ctx.restore();
  };
  /* peint un texte composé (comp) dont le coin haut-gauche est (x, y) */
  CV.peindreComp = (ctx, comp, x, y, z, couleur, E) => {
    for (const L of comp.lignes) for (const b of L.items) {
      if (b.esp) continue;
      const px = x + b.x * z, py = y + L.y * z;
      const st = b.a.st;
      const c = st.coul ? CV.couleur(E.theme, st.coul) : couleur;
      if (b.f) { CV.peindreFormule(ctx, b.f, px, py, b.tt * z, c, null); continue; }
      ctx.font = CV.police(comp.taille * z, st); ctx.fillStyle = c;
      ctx.letterSpacing = (comp.espacement * z) + 'px';
      ctx.fillText(b.s, px, py);
    }
    ctx.letterSpacing = '0px';
  };

  /* ---------- puce (pilule) ---------- */
  CV.TYPES.puce = {
    creer(n) {
      n.analyse = CV.analyserTexte(n.spec.puce);
      const base = styleBase(n);
      n.analyse.atomes.forEach(a => { a.st = Object.assign({}, base, a.st); });
    },
    mesurer(n, W, E) {
      const o = optionsTexte(n, E);
      n.comp = CV.composerTexte(n.analyse, 4000, o);
      const ph = n.spec.margeH ?? 26, pv = n.spec.margeV ?? 10;
      n.pad = { h: ph, v: pv };
      // pilule numérotée (numero: 1) : pastille ronde avant le texte, comme les étapes « 1 Dresser »
      n.num = n.spec.numero !== undefined ? { d: n.spec.tailleNumero ?? 44, ecart: 12, g: n.spec.margeGauche ?? 12 } : null;
      const avant = n.num ? n.num.g + n.num.d + n.num.ecart : ph;
      n.lw = n.comp.w + avant + ph + 4;
      n.lh = Math.max(n.comp.h, n.num ? n.num.d : 0) + 2 * pv + 4;
    },
    sprite: true, marge: 8,
    peindre(ctx, n, E, opts) {
      const t = E.theme, b = n.b, z = n.z;
      const c = CV.couleur(t, n.spec.couleur, 'ambre');
      if (!(opts && opts.couleur)) {
        ctx.beginPath(); ctx.roundRect(b.x + z, b.y + z, b.w - 2 * z, b.h - 2 * z, b.h / 2);
        ctx.fillStyle = CV.mix(c, 0.18); ctx.fill();
        ctx.lineWidth = 2 * z; ctx.strokeStyle = CV.mix(c, 0.6); ctx.stroke();
      }
      let x = b.x + (n.pad.h + 2) * z;
      if (n.num) {
        const d = n.num.d * z, cx = b.x + (n.num.g + 2) * z + d / 2, cy = b.y + b.h / 2;
        ctx.beginPath(); ctx.arc(cx, cy, d / 2, 0, Math.PI * 2); ctx.fillStyle = c; ctx.fill();
        ctx.font = CV.police(d * 0.68, { gras: true }); ctx.fillStyle = '#0b1026';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(String(n.spec.numero), cx, cy + d * 0.03);
        ctx.textAlign = 'start'; ctx.textBaseline = 'alphabetic';
        x = cx + d / 2 + n.num.ecart * z;
      }
      CV.peindreComp(ctx, n.comp, x, b.y + (b.h - n.comp.h * z) / 2, z, opts && opts.couleur || t.texte, E);
    },
  };
  CV.TYPES.icone = {
    creer(n) { n.analyse = CV.analyserTexte(n.spec.icone); },
    mesurer(n, W, E) { n.comp = CV.composerTexte(n.analyse, 4000, optionsTexte(n, E)); n.lw = n.comp.w; n.lh = n.comp.h; },
    sprite: true, marge: 10,
    peindre(ctx, n, E) { CV.peindreComp(ctx, n.comp, n.b.x, n.b.y, n.z, E.theme.texte, E); },
  };

  /* ---------- calcul / grille : lignes alignées (ex. sur le signe =) ---------- */
  function creerGrille(n, E) {
    const lignes = n.spec.calcul || n.spec.grille;
    n.cases = lignes.map(l => l.map(c => {
      if (c === '' || c === null || c === undefined) return null;
      const spec = typeof c === 'string' ? (n.spec.calcul ? { tex: c } : { texte: c }) : c;
      const e = CV.creerNoeud(spec, n, E);
      n.enfants.push(e);
      return e;
    }));
  }
  CV.TYPES.calcul = CV.TYPES.grille = {
    creer: creerGrille,
    mesurer(n, W, E) {
      const nbc = Math.max(...n.cases.map(l => l.length));
      const [eL, eC] = n.spec.ecart ? (Array.isArray(n.spec.ecart) ? n.spec.ecart : [n.spec.ecart, n.spec.ecart]) : CV.formulesDe(n, E).ecartGrille;
      n.cases.forEach(l => l.forEach(c => c && CV.mesurer(c, W, E)));
      n.colW = []; for (let j = 0; j < nbc; j++) n.colW[j] = Math.max(0, ...n.cases.map(l => (l[j] ? l[j].lw : 0)));
      if (n.spec.colonnesL) n.spec.colonnesL.forEach((w, j) => { if (w) n.colW[j] = Math.max(n.colW[j], w); });
      n.ligH = n.cases.map(l => {
        const asc = Math.max(0, ...l.map(c => (c ? (c.asc ?? c.lh / 2) : 0)));
        const desc = Math.max(0, ...l.map(c => (c ? (c.desc ?? c.lh / 2) : 0)));
        return { asc, desc, h: Math.max(asc + desc, n.spec.hauteurLigne || 0) };
      });
      n.ec = [eL, eC];
      n.lw = n.colW.reduce((s, w) => s + w, 0) + eC * (nbc - 1);
      n.lh = n.ligH.reduce((s, l) => s + l.h, 0) + eL * (n.cases.length - 1);
    },
    disposer(n, E) {
      const al = n.spec.colonnes || (n.spec.calcul ? ['droite', 'centre', 'gauche'] : []);
      let y = 0;
      n.cases.forEach((l, i) => {
        const L = n.ligH[i];
        const yBase = y + (L.h - L.asc - L.desc) / 2 + L.asc;
        let x = 0;
        l.forEach((c, j) => {
          if (c) {
            const a = al[j] || 'gauche';
            c.lx = x + (a === 'droite' ? n.colW[j] - c.lw : a === 'centre' ? (n.colW[j] - c.lw) / 2 : 0);
            c.ly = yBase - (c.asc ?? c.lh / 2);
            CV.disposer(c, E);
          }
          x += n.colW[j] + n.ec[1];
        });
        y += L.h + n.ec[0];
      });
    },
  };

  /* ---------- dessin personnalisé (échappatoire) ----------
     { dessin: (ctx, boite, t, outils) => { … }, l: 300, h: 200 } — redessiné à chaque image */
  CV.TYPES.dessin = {
    creer() {}, mesurer(n) { n.lw = n.spec.l || 100; n.lh = n.spec.h || 100; },
    dynamique: true,
    peindre(ctx, n, E, opts, t) {
      try { n.spec.dessin(ctx, n.b, t, { theme: E.theme, couleur: c => CV.couleur(E.theme, c), z: n.z }); }
      catch (e) { if (!n.signale) { E.erreur('dessin ' + (n.id || '') + ' : ' + e.message); n.signale = true; } }
    },
  };

})(typeof self !== 'undefined' ? self : this);
