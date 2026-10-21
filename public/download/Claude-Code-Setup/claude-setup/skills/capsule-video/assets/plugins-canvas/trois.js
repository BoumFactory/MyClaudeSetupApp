/* =====================================================================
   Plugin « trois » du moteur canvas : scènes 3D three.js (r159, MIT)
   ---------------------------------------------------------------------
   Module CHARGÉ À CÔTÉ du moteur (aucune retouche de moteur-canvas/), après
   three.min.js, par la ligne de chargement placée en tête de spec.js
   (scripts/installer_trois.py ; voir references/trois-d.md).

   Deux usages :
     1) fond plein écran, sous les cartes 2D  : dans gestes(C),
          C.trois({ scene3d: (THREE, scene, camera, o) => (t) => { …positionner tout… } });
     2) élément dans une zone de mise en page :
          { scene3d: (THREE, scene, camera, o) => (t) => {…}, l: 800, h: 600, id: 'vue' }

   La fonction `scene3d` est appelée UNE fois (à la première image dessinée) ;
   elle construit la scène et renvoie `maj(t)`, qui place tout en fonction
   de t SEULEMENT (aucune horloge, pas de Math.random : o.hasard(graine)).
   Chaque worker de rendu recrée la scène lui-même : mêmes images partout.

   Principe : un OffscreenCanvas WebGL dédié par vue, à la taille réelle du
   rendu (540p, 720p, 1080p), recopié par ctx.drawImage dans la toile 2D.
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});
  if (CV.TROIS) return;
  if (racine.__warn3) { console.warn = racine.__warn3; racine.__warn3 = null; }   // rend la parole à console.warn (neutralisé par le chargeur le temps de l'avertissement de three.min.js)
  const TR = (CV.TROIS = { version: 1, fonds: [], dessus: [], C: null, stats: { images: 0, ms: 0, vues: 0 } });
  const EN_WORKER = typeof importScripts === 'function';
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));

  /* ---------- outils d'animation (fonctions pures) ---------- */
  const ease = {
    borne: clamp,
    /* avancement 0..1 de t entre t0 et t1 */
    etape: (t, t0, t1) => clamp((t - t0) / Math.max(1e-6, t1 - t0), 0, 1),
    lisse: x => { x = clamp(x, 0, 1); return x * x * x * (x * (x * 6 - 15) + 10); },          // smootherstep
    entree: x => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); },                            // smoothstep
    sortie: x => { x = clamp(x, 0, 1); return 1 - Math.pow(1 - x, 3); },                         // cubic out
    rebond: x => { x = clamp(x, 0, 1); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },   // back out
    lerp: (a, b, x) => a + (b - a) * x,
  };

  /* ---------- une vue = un OffscreenCanvas WebGL + une scène ---------- */
  function creerVue(sp, L, H, k, C, nom) {
    const v = { sp, L, H, k, nom: nom || 'vue', pret: false, mort: false };
    v.px = Math.max(2, Math.round(L * k)); v.py = Math.max(2, Math.round(H * k));
    v.init = () => {
      const THREE = racine.THREE;
      if (!THREE) throw new Error('three.js non chargé : la ligne du plugin trois manque en tête de spec.js (installer_trois.py)');
      v.canvas = new OffscreenCanvas(v.px, v.py);
      const r = (v.renderer = new THREE.WebGLRenderer({ canvas: v.canvas, antialias: sp.antialias !== false, alpha: true,
        premultipliedAlpha: true, powerPreference: 'high-performance', preserveDrawingBuffer: false }));
      if (r.getContext().isContextLost()) throw new Error('contexte WebGL perdu dès la création (' + v.nom + ')');
      r.setPixelRatio(1); r.setSize(v.px, v.py, false); r.setClearColor(0x000000, 0);
      v.scene = new THREE.Scene();
      v.camera = new THREE.PerspectiveCamera(sp.fov || 45, L / H, 0.1, sp.loin || 2000);
      const E = C && C._E;
      const theme = E ? E.theme : CV.THEMES.nuit;
      const o = {
        THREE, renderer: r, L, H, k, theme, ease, C, vue: v,
        hasard: g => (C ? C.hasard(g) : CV.ancres({}, [], () => {}).hasard(g)),
        couleur: n => CV.couleur(theme, n),
        col: n => new THREE.Color(CV.couleur(theme, n)),
        a: C ? C.a : null,
      };
      Object.assign(o, aide(THREE, o));
      v.o = o;
      const maj = sp.scene3d(THREE, v.scene, v.camera, o);
      if (typeof maj !== 'function') throw new Error('scene3d doit renvoyer la fonction maj(t) (vue ' + v.nom + ')');
      v.maj = maj; v.pret = true;
      TR.stats.vues++;
    };
    /* dessine la vue à l'instant t dans ctx (coordonnées de scène 1920×1080), dans le rectangle x, y, w, h */
    v.peindre = (ctx, t, x, y, w, h) => {
      if (v.mort) return;
      const a = performance.now();   // mesure seulement : n'influence jamais l'image
      try {
        if (!v.pret) v.init();
        v.maj(t);
        v.renderer.render(v.scene, v.camera);
        if (v.renderer.getContext().isContextLost()) throw new Error('contexte WebGL perdu (' + v.nom + ')');
        ctx.drawImage(v.canvas, x, y, w, h);
      } catch (e) {
        v.mort = true;
        TR.erreur = e;
        console.error('[trois] ' + v.nom + ' : ' + (e && e.stack || e));
        if (EN_WORKER) throw e;   // un rendu sans 3D doit échouer bruyamment, jamais produire des images noires
      }
      TR.stats.images++; TR.stats.ms += performance.now() - a;
    };
    return v;
  }

  /* ---------- aides de construction (texte, lueur, matériaux) ---------- */
  function aide(THREE, o) {
    const A = {};
    /* plan portant un texte (texture canvas) : hauteur en unités du monde ; le plan fait face à +z */
    A.texte = (chaine, opt = {}) => {
      const taille = opt.taille || 128, gras = opt.gras !== false;
      const police = `${gras ? '700 ' : ''}${taille}px ${opt.police || "Atkinson, 'Segoe UI', 'Times New Roman', sans-serif"}`;
      const mes = new OffscreenCanvas(8, 8).getContext('2d');
      mes.font = police;
      const w = Math.ceil(mes.measureText(chaine).width + taille * 0.5), h = Math.ceil(taille * 1.4);
      const c = new OffscreenCanvas(w, h), x = c.getContext('2d');
      x.font = police; x.textAlign = 'center'; x.textBaseline = 'middle';
      if (opt.lueur !== 0) { x.shadowColor = opt.couleur || '#fff'; x.shadowBlur = taille * (opt.lueur ?? 0.12); }
      if (opt.fond) { x.fillStyle = opt.fond; x.beginPath(); x.roundRect(2, 2, w - 4, h - 4, taille * 0.25); x.fill(); x.shadowBlur = 0; }
      x.fillStyle = opt.couleur || '#ffffff';
      x.fillText(chaine, w / 2, h / 2 + taille * 0.04);
      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
      const hu = opt.hauteur || 1;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(hu * w / h, hu),
        new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, side: THREE.DoubleSide, fog: false }));
      m.userData.ratio = w / h;
      return m;
    };
    /* halo additif (sprite) : taille en unités du monde */
    A.lueur = (couleur, taille = 4, opacite = 0.8) => {
      const c = new OffscreenCanvas(128, 128), x = c.getContext('2d');
      const g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
      g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.25, 'rgba(255,255,255,0.45)'); g.addColorStop(1, 'rgba(255,255,255,0)');
      x.fillStyle = g; x.fillRect(0, 0, 128, 128);
      const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
      const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, color: new THREE.Color(couleur), transparent: true,
        opacity: opacite, blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
      s.scale.set(taille, taille, 1);
      return s;
    };
    /* matériau « lumineux » : couleur + émission (reste lisible sur fond sombre) */
    A.mat = (couleur, opt = {}) => new THREE.MeshStandardMaterial(Object.assign({
      color: new THREE.Color(couleur), emissive: new THREE.Color(couleur), emissiveIntensity: 0.35, roughness: 0.4, metalness: 0.15 }, opt));
    A.verre = (couleur, opacite = 0.18) => new THREE.MeshBasicMaterial({ color: new THREE.Color(couleur), transparent: true,
      opacity: opacite, depthWrite: false, side: THREE.DoubleSide });
    A.eclairer = (scene, intensite = 1) => {
      scene.add(new THREE.AmbientLight(0xffffff, 0.9 * intensite));
      const d1 = new THREE.DirectionalLight(0xffffff, 2.2 * intensite); d1.position.set(5, 8, 6); scene.add(d1);
      const d2 = new THREE.DirectionalLight(0x88aaff, 1.0 * intensite); d2.position.set(-6, -2, -4); scene.add(d2);
    };
    return A;
  }
  TR.ease = ease;

  /* ---------- démarrage : le fond 3D se dessine juste après le fond 2D, donc sous les scènes ---------- */
  const Fond0 = CV.Fond;
  CV.Fond = function (theme, k, ambiance) {
    Fond0.call(this, theme, k, ambiance);
    const d0 = this.dessiner;
    this.dessiner = (ctx, t) => {
      d0(ctx, t);
      for (const v of TR.fonds) {
        const al = v.sp.opacite ? v.sp.opacite(t) : 1;
        if (al <= 0.003) continue;
        ctx.save(); ctx.globalAlpha *= al;
        v.peindre(ctx, t, 0, 0, 1920, 1080);
        ctx.restore();
      }
    };
  };

  /* ---------- geste C.trois : enregistre un fond (ou un calque au-dessus des scènes) ---------- */
  const gestes0 = CV.creerGestes;
  CV.creerGestes = function (E, tl, A) {
    TR.fonds = []; TR.dessus = [];
    const C = gestes0.call(this, E, tl, A);
    C._E = E; TR.C = C;
    C.trois = (opt) => {
      if (!opt || typeof opt.scene3d !== 'function') { E.erreur('C.trois : scene3d(THREE, scene, camera, o) => maj(t) attendu'); return; }
      const v = creerVue(opt, 1920, 1080, E.k, C, 'fond3d');
      if (opt.dessus) {   // au-dessus des scènes (calque)
        C.ajouter((ctx, EE, s, t) => { const al = opt.opacite ? opt.opacite(t) : 1; if (al <= 0.003) return; ctx.save(); ctx.globalAlpha *= al; v.peindre(ctx, t, 0, 0, 1920, 1080); ctx.restore(); });
      } else TR.fonds.push(v);
      return v;
    };
    return C;
  };

  /* ---------- élément typé { scene3d, l, h } dans la mise en page ---------- */
  CV.CLES.push('scene3d');
  CV.TYPES.scene3d = {
    dynamique: true, marge: 0,
    creer(n, E) { n.E = E; n.vue = null; },
    mesurer(n, W) { n.lw = Math.min(n.spec.l || W, W); n.lh = n.spec.h || Math.round(n.lw * 9 / 16); },
    peindre(ctx, n, E, opts, t) {
      if (!n.vue) n.vue = creerVue(n.spec, n.b.w, n.b.h, E.k, TR.C, n.id || 'scene3d');
      const b = n.b;
      ctx.save();
      if (n.spec.rayon) { ctx.beginPath(); ctx.roundRect(b.x, b.y, b.w, b.h, n.spec.rayon); ctx.clip(); }
      n.vue.peindre(ctx, t, b.x, b.y, b.w, b.h);
      ctx.restore();
    },
  };
})(typeof self !== 'undefined' ? self : this);
