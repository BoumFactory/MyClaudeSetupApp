/* =====================================================================
   Moteur canvas de capsule-video — construction et dessin d'une image
   ---------------------------------------------------------------------
   spec.js (données) → arbre d'éléments → mise en page par gabarits
   (texte réduit pour tenir) → gestes GSAP sur des objets JS → dessin.
   Le même code tourne dans l'aperçu (page), dans la page de rendu
   (préparation) et dans chaque worker (dessin + encodage) : même spec,
   même table de préparation → mêmes images (aucune horloge, aucun hasard).
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});

  /* spec.js commence par CAPSULE({ … }) */
  racine.CAPSULE = s => { CV.spec = s; };

  /* ---------- gabarits de mise en page (zones dans le repère 1920×1080) ----------
     Inspirés de references/design.md. Une scène peut redéfinir ou ajouter des zones :
     zones: { maZone: { x, y, l, h } }. Valeur d'une zone dans la scène : liste d'éléments,
     ou { contenu: [...], valign: 'haut' | 'centre' | 'bas', ecart: 26 }. */
  CV.GABARITS = {
    titre: {
      haut: { x: 90, y: 110, l: 1740, h: 230, ecart: 11 },
      centre: { x: 90, y: 360, l: 1740, h: 680, ecart: 60 },
    },
    'figure-panneau': {
      bandeau: { x: 60, y: 34, l: 900, h: 80 },
      figure: { x: 40, y: 150, l: 960, h: 500 },
      'sous-figure': { x: 40, y: 656, l: 960, h: 390, ecart: 12 },
      panneau: { x: 1060, y: 130, l: 800, h: 910 },
    },
    'tableau-calcul': {
      bandeau: { x: 60, y: 34, l: 1800, h: 80 },
      donnees: { x: 90, y: 130, l: 1740, h: 130 },
      tableau: { x: 60, y: 290, l: 960, h: 640 },
      calcul: { x: 1060, y: 290, l: 800, h: 640 },
      bas: { x: 90, y: 950, l: 1740, h: 100 },
    },
    colonne: {
      bandeau: { x: 60, y: 34, l: 1800, h: 80 },
      centre: { x: 260, y: 150, l: 1400, h: 880 },
    },
    plein: { centre: { x: 90, y: 70, l: 1740, h: 940 } },
  };

  CV.TYPES.scene = { creer() {}, mesurer() {} };
  CV.TYPES.zone = { creer() {}, mesurer() {} };

  /* cherche le plus grand zoom (≤ 1) pour que n tienne dans W×H */
  function ajuster(n, W, H, E) {
    const essai = z => { CV.mesurer(n, W / z, E); return !n.deborde && n.lh * z <= H + 0.5; };
    let z = 1;
    if (!essai(1)) {
      let lo = 0.3, hi = 1;
      for (let i = 0; i < 14; i++) { const m = (lo + hi) / 2; if (essai(m)) lo = m; else hi = m; }
      z = lo;
      if (!essai(z)) E.erreur('Contenu impossible à faire tenir : ' + (n.id || n.type));
    }
    if (n.lw < W / z && CV.etirable(n) && !n.spec.l) n.lw = W / z;
    CV.disposer(n, E);
    return z;
  }

  /* Compteur (geste compte). Sur un texte : dans le style du texte (police, couleur ou dégradé, lueur) ;
     sur une formule : glyphes MathJax posés côte à côte. */
  CV.peindreCompteur = (ctx, n, E) => {
    if (n.comp && n.comp.lignes.length) {
      const s = n.compteur(), L = n.comp.lignes[0], b0 = L.items.find(b => !b.esp && !b.f);
      const st = b0 ? b0.a.st : {};
      ctx.save();
      ctx.font = CV.police(n.comp.taille * n.z, Object.assign({}, st, { tab: true }));   // compteur : chiffres tabulaires comme .cv-vol
      ctx.letterSpacing = (n.comp.espacement * n.z) + 'px';
      const w = ctx.measureText(s).width, al = n.spec.align;
      const x = al === 'centre' ? n.b.x + (n.b.w - w) / 2 : al === 'droite' ? n.b.x + n.b.w - w : n.b.x;
      const coul = st.coul ? CV.couleur(E.theme, st.coul) : n.spec.couleur ? CV.couleur(E.theme, n.spec.couleur) : E.theme.texte;
      CV.lueurTexte(ctx, n, coul);
      ctx.fillStyle = CV.remplissageTexte(ctx, n, E, coul);
      ctx.fillText(s, x, n.b.y + L.y * n.z);
      ctx.restore();
      return;
    }
    const s = n.compteur(), taille = (n.taille || (n.comp ? n.comp.taille * 1.1 : CV.formulesDe(n, E).defaut)) * n.z;
    const glyphes = [...s].map(c => E.prep.formule(CV.texChiffre(c, n.spec.gras), false));
    const w = glyphes.reduce((a, f) => a + f.w * taille, 0);
    const al = n.spec.align;
    let x = al === 'centre' ? n.b.x + (n.b.w - w) / 2 : al === 'droite' ? n.b.x + n.b.w - w : n.b.x;
    const base = n.b.y + (n.asc ? n.asc * n.z : n.b.h * 0.72);
    const col = n.spec.couleur ? CV.couleur(E.theme, n.spec.couleur) : E.theme.texte;
    ctx.save();
    CV.lueurTexte(ctx, n, col);
    // dégradé : défini dans le repère de la scène, puis ramené dans le repère (translaté, mis à l'échelle) de chaque glyphe
    const P = n.spec.degrade ? CV.extremitesDegrade({ x, y: n.b.y, w, h: n.b.h }) : null;
    const cs = n.spec.degrade ? n.spec.degrade.map(c => CV.couleur(E.theme, c)) : null;
    for (const f of glyphes) {
      let remp = col;
      if (P) {
        remp = ctx.createLinearGradient((P[0] - x) / taille, (P[1] - base) / taille, (P[2] - x) / taille, (P[3] - base) / taille);
        cs.forEach((c, i) => remp.addColorStop(cs.length > 1 ? i / (cs.length - 1) : 0, c));
      }
      CV.peindreFormule(ctx, f, x, base, taille, remp, null);
      x += f.w * taille;
    }
    ctx.restore();
  };
  CV.texChiffre = (c, gras) => { const t = c === ',' ? '{,}' : c; return gras ? '\\mathbf{' + t + '}' : t; };

  CV.Moteur = function (o) {
    const spec = o.spec || CV.spec;
    if (!spec) throw new Error('spec.js absent ou sans CAPSULE({ … })');
    const cfg = Object.assign({ titre: 'Capsule', audio: 'audio.wav', theme: 'nuit', ambiance: true, marge: 1.2, mention: null },
      spec.config || {}, spec);
    const E = { theme: CV.THEMES[cfg.theme] || CV.THEMES.nuit, prep: o.prep, k: o.k, ids: new Map(), noeuds: [],
      erreurs: [], calque: [], premierNiveau: [], images: o.images || {}, pointsTraces: cfg.pointsTraces, cfgTuiles: cfg.tuiles || {} };
    E.erreur = msg => { if (!E.erreurs.includes(String(msg))) E.erreurs.push(String(msg)); };
    E.formules = CV.reglageFormules(cfg.formules, E);   // clé absente → 'actuel' (comportement historique)
    this.E = E;
    const T = o.transcript || { mots: [], segments: [], duree: 10 };
    const A = CV.ancres(T, o.tempsForts || [], E.erreur);
    const gsap = racine.gsap || (racine.window && racine.window.gsap);
    const tl = gsap.timeline({ paused: true });
    this.tl = tl;

    /* 1) arbre */
    const scenes = [];
    const rapport = [];
    for (const sc of spec.scenes || []) {
      const n = new CV.Noeud('scene', sc, null, E);
      n.s.o = 0;
      const gab = CV.GABARITS[sc.gabarit || 'plein'];
      if (!gab) E.erreur('Gabarit inconnu : ' + sc.gabarit + ' (connus : ' + Object.keys(CV.GABARITS).join(', ') + ')');
      const Pf = CV.formulesDe(n, E);   // préréglage formules de la scène (ou de la capsule)
      const retouche = sc.gabarit === 'figure-panneau' && Pf.figurePanneau ? Pf.figurePanneau : {};
      const zones = Object.assign({}, gab || {}, retouche, sc.zones || {});
      for (const nom of Object.keys(zones)) {
        let v = sc[nom];
        if (v === undefined) continue;
        if (!Array.isArray(v) && !(v && v.contenu)) v = [v];
        const opt = Array.isArray(v) ? {} : v;
        const contenu = Array.isArray(v) ? v : v.contenu;
        const rect = Object.assign({}, zones[nom], opt);
        const z = new CV.Noeud('zone', { id: sc.id ? sc.id + ':' + nom : null }, n, E);
        z.rect = rect; z.nom = nom;
        n.enfants.push(z);
        const seul = contenu.length === 1 && contenu[0] && contenu[0].pile !== undefined;
        const r = seul ? CV.creerNoeud(contenu[0], z, E)
          : CV.creerNoeud({ colonne: contenu, ecart: rect.ecart ?? 26, alignEnfants: rect.align }, z, E);
        z.enfants.push(r);
        z.racine = r; z.pileSeule = seul;
        E.premierNiveau.push(...(seul ? r.enfants : r.enfants));
      }
      scenes.push(n);
    }
    for (const k of Object.keys(spec)) {
      if (!['titre', 'audio', 'theme', 'ambiance', 'marge', 'mention', 'tailleMention', 'macros', 'scenes', 'gestes', 'config', 'sousTitres', 'corrections', 'pointsTraces', 'tuiles', 'formules'].includes(k))
        E.erreur('Clé inconnue dans spec.js : ' + k);
    }

    /* 2) mise en page : chaque zone (ou chaque morceau d'une pile seule) est réduite pour tenir */
    // préréglage « grandes » : une zone réduite de plus de 20 % redevient « compactes » en silence → avertir
    const alerteGrandes = (sc, nom, zz, n) => {
      if (zz >= 0.8 || CV.formulesDe(n, E).nom !== 'grandes') return;
      rapport.push(`AVERTISSEMENT ${sc.id || 'scène'} / ${nom} : formules réduites de ${Math.round((1 - zz) * 100)} % en préréglage « grandes » ; couper la scène en deux étapes`);
    };
    for (const sc of scenes) {
      sc.b = { x: 0, y: 0, w: 1920, h: 1080 }; sc.z = 1;
      for (const z of sc.enfants) {
        const R = z.rect, r = z.racine;
        z.b = { x: R.x, y: R.y, w: R.l, h: R.h }; z.z = 1;
        const caler = (n, zz) => {
          const h = n.lh * zz, va = R.valign || 'haut';
          return va === 'centre' ? (R.h - h) / 2 : va === 'bas' ? R.h - h : 0;
        };
        if (z.pileSeule) {
          r.lw = R.l; r.lh = R.h; r.lx = 0; r.ly = 0;
          for (const c of r.enfants) {
            const zz = ajuster(c, R.l, R.h, E);
            c.zoomPropre = zz; c.lx = 0; c.ly = caler(c, zz) + Math.min(c.spec.dy || 0, Math.max(0, R.h - c.lh * zz));
            if (zz < 0.999) rapport.push(`${sc.id || 'scène'} / ${z.nom} / ${c.id || c.type} : texte à ${Math.round(zz * 100)} %`);
            alerteGrandes(sc, z.nom + ' / ' + (c.id || c.type), zz, c);
          }
          // pile de pilules (bandeau) : toutes à la largeur de la plus longue, comme une grille CSS
          if (r.enfants.length && r.enfants.every(c => !CV.etirable(c))) {
            const wMax = Math.max(...r.enfants.map(c => c.lw));
            r.enfants.forEach(c => { c.lw = wMax; CV.disposer(c, E); });
          }
          CV.placer(r, R.x, R.y, 1);
        } else {
          const zz = ajuster(r, R.l, R.h, E);
          if (zz < 0.999) rapport.push(`${sc.id || 'scène'} / ${z.nom} : texte à ${Math.round(zz * 100)} %`);
          alerteGrandes(sc, z.nom, zz, r);
          CV.placer(r, R.x, R.y + caler(r, zz), zz);
        }
      }
    }
    this.rapport = rapport;

    /* 3) fond, ambiance */
    this.fond = new CV.Fond(E.theme, E.k, cfg.ambiance !== false);

    /* 4) gestes */
    const C = CV.creerGestes(E, tl, A);
    this.C = C;
    C.config = cfg;
    scenes.forEach(sc => { if (sc.spec.debut !== undefined) C.scene(sc, sc.spec.debut); });
    try {
      if (typeof spec.gestes === 'function') spec.gestes(C);
    } catch (e) { E.erreur('gestes : ' + e.message + (e.stack ? ' — ' + String(e.stack).split('\n')[1] : '')); }
    for (const n of E.noeuds.slice()) {
      for (const g of CV.RACCOURCIS) {
        const v = n.spec[g];
        if (v === undefined || (g === 'cache' && v === true)) continue;
        const [t, opts] = Array.isArray(v) ? v : [v, {}];
        try { C[g](n, t, opts); } catch (e) { E.erreur(g + ' sur ' + (n.id || n.type) + ' : ' + e.message); }
      }
      if (n.spec.visible === false || n.spec.cache === true) n.s.o = 0;
    }
    // glyphes des compteurs sur formule (préparés ici pour que la table des workers les contienne)
    for (const n of E.noeuds) if (n.compteur && !n.comp) for (const c of '0123456789-,') E.prep.formule(CV.texChiffre(c, n.spec.gras), false);

    /* 5) état initial : un élément dont le premier geste est une entrée part caché */
    const premier = new Map();
    for (const j of C._journal) {
      const p = premier.get(j.n);
      if (!p || j.t < p.t - 1e-9) premier.set(j.n, j);
    }
    for (const [n, j] of premier) if (j.sens === 'entree') n.s.o = 0;

    this.duree = (T.duree || 10) + cfg.marge;
    tl.set({}, {}, this.duree);
    this.config = cfg;
    this.scenes = scenes;

    const hooks = E.hooks;
    this.seek = t => { tl.seek(t, false); for (const f of hooks) f(t); };
    const mention = cfg.mention ? CV.analyserTexte(cfg.mention) : null;
    const tm = cfg.tailleMention ?? 26;
    /* sous-titres (sousTitres: true) : segments du transcript, table `corrections` appliquée (lapsus, erreurs de reconnaissance) */
    const corr = Object.entries(cfg.corrections || {});
    const segs = cfg.sousTitres ? (T.segments || []).map(s => {
      let x = s.texte;
      corr.forEach(([a, b]) => { x = x.split(a).join(b); });
      return { debut: s.debut, fin: s.fin, texte: x.trim(), comp: null };
    }) : [];
    const sousTitre = (ctx, t) => {
      const s = segs.find(z => t >= z.debut && t < z.fin + 0.3);
      if (!s || !s.texte) return;
      if (!s.comp) {   // texte brut : ni formule ni balisage
        const atomes = [];
        s.texte.split(/(\s+)/).filter(Boolean).forEach(m => atomes.push(/^\s+$/.test(m) ? { k: 'esp', st: {}, spans: [] } : { k: 'mot', s: m, st: {}, spans: [] }));
        s.comp = CV.composerTexte({ atomes, spans: [] }, 1448, { taille: 34, interligne: 1.3, formule: x => E.prep.formule(x, false) });
      }
      const c = s.comp, w = c.w + 52, h = c.h + 20, x = (1920 - w) / 2, y = 1080 - 46 - h;
      ctx.save();
      ctx.beginPath(); ctx.roundRect(x, y, w, h, 14); ctx.fillStyle = 'rgba(5,8,20,0.72)'; ctx.fill();
      for (const L of c.lignes) {   // lignes centrées
        const dx = (c.w - L.w) / 2;
        for (const b of L.items) if (!b.esp && !b.f) { ctx.font = CV.police(34, b.a.st); ctx.fillStyle = '#ffffff'; ctx.fillText(b.s, x + 26 + dx + b.x, y + 10 + L.y); }
      }
      ctx.restore();
    };
    this.dessiner = (ctx, t) => {
      ctx.setTransform(E.k, 0, 0, E.k, 0, 0);
      ctx.globalAlpha = 1; ctx.filter = 'none';
      this.fond.dessiner(ctx, t);
      for (const sc of scenes) { CV.dessinerNoeud(ctx, sc, E, t); CV.dessinerLevees(ctx, E, t); }
      for (const it of E.calque) if (!it.dessus) it.dessiner(ctx, E, it.s, t);
      if (mention) {   // #legal : bas droite, 26 px, texte doux, opacité 0,85
        const c = CV.composerTexte(mention, 2000, { taille: tm, nowrap: true, espacement: 0.02 * tm, formule: x => E.prep.formule(x, false) });
        ctx.save(); ctx.globalAlpha = 0.85;
        CV.peindreComp(ctx, c, 1920 - 34 - c.w, 1080 - 16 - c.h, 1, E.theme.doux, E);
        ctx.restore();
      }
      for (const it of E.calque) if (it.dessus) it.dessiner(ctx, E, it.s, t);
      if (segs.length) sousTitre(ctx, t);
    };
    this.info = () => ({ duree: this.duree, audio: cfg.audio, erreurs: E.erreurs, titre: cfg.titre, rapport });
  };

  /* Polices Atkinson (page ou worker) depuis le dossier vendor/fonts */
  CV.chargerPolices = async base => {
    const F = [['400', 'normal', 'atkinson-hyperlegible-latin-400-normal'], ['700', 'normal', 'atkinson-hyperlegible-latin-700-normal'],
      ['400', 'italic', 'atkinson-hyperlegible-latin-400-italic'], ['700', 'italic', 'atkinson-hyperlegible-latin-700-italic']];
    const ens = racine.document ? racine.document.fonts : racine.fonts;
    await Promise.all(F.flatMap(([w, s, f]) => [['Atkinson', {}], ['AtkinsonT', { featureSettings: '"tnum"' }]].map(async ([fam, extra]) => {
      const ff = new FontFace(fam, `url("${base}${f}.woff2")`, Object.assign({ weight: w, style: s }, extra));
      await ff.load();
      ens.add(ff);
    })));
  };
})(typeof self !== 'undefined' ? self : this);
