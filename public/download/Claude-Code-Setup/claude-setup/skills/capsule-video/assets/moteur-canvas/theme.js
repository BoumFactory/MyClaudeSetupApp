/* =====================================================================
   Thèmes « nuit » / « jour » du moteur canvas
   ---------------------------------------------------------------------
   Mêmes valeurs que assets/gabarit/moteur/theme.css. Ce qui est coûteux
   et constant (dégradés du fond, taches floues, grain) est pré-rendu une
   fois en image ; à chaque image, on ne fait que déplacer ces images.
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});

  CV.THEMES = {
    nuit: {
      fond1: '#0b1026', fond2: '#1b1250', fond3: '#052a3f',
      texte: '#eef2ff', doux: '#a9b4d6', trait: 'rgba(255,255,255,0.14)',
      carte: 'rgba(255,255,255,0.065)', carteForte: 'rgba(255,255,255,0.11)',
      violet: '#a78bfa', rose: '#f472b6', cyan: '#22d3ee', ambre: '#fbbf24',
      vert: '#34d399', corail: '#fb7185', bleu: '#60a5fa',
      ombre: { y: 20, flou: 60, couleur: 'rgba(0,0,0,0.35)' },
      grain: 'rgba(255,255,255,0.07)', blob: 0.32, tag: '#05060d',
    },
    jour: {
      fond1: '#f6f7fb', fond2: '#e9e4ff', fond3: '#dff6fb',
      texte: '#141a33', doux: '#56607e', trait: 'rgba(20,26,51,0.12)',
      carte: 'rgba(255,255,255,0.75)', carteForte: '#ffffff',
      violet: '#7c3aed', rose: '#db2777', cyan: '#0891b2', ambre: '#d97706',
      vert: '#059669', corail: '#e11d48', bleu: '#2563eb',
      ombre: { y: 18, flou: 50, couleur: 'rgba(40,40,90,0.14)' },
      grain: 'rgba(20,26,51,0.07)', blob: 0.32, tag: '#141a33',
    },
  };
  CV.NOMS_COULEURS = ['violet', 'rose', 'cyan', 'ambre', 'vert', 'corail', 'bleu', 'texte', 'doux'];

  /* ---------- couleurs ---------- */
  /* '--violet', 'violet', '#a78bfa', 'rgba(…)' → chaîne CSS utilisable par le canvas */
  CV.couleur = (theme, nom, defaut) => {
    if (nom === undefined || nom === null || nom === '') nom = defaut;
    if (nom === undefined || nom === null) return theme.ambre;
    const n = String(nom).replace(/^--/, '');
    if (n === 'accent') return theme.ambre;
    if (n === 'texte-doux') return theme.doux;
    return theme[n] !== undefined && typeof theme[n] === 'string' ? theme[n] : String(nom);
  };

  /* chaîne CSS → [r, g, b, a] (a entre 0 et 1) ; hex court/long, rgb(), rgba() */
  const cacheRGBA = new Map();
  CV.rgba = css => {
    if (Array.isArray(css)) return css;
    if (cacheRGBA.has(css)) return cacheRGBA.get(css);
    let r = [255, 255, 255, 1];
    const s = String(css).trim();
    let m;
    if ((m = s.match(/^#([0-9a-f]{3,8})$/i))) {
      let h = m[1];
      if (h.length <= 4) h = h.split('').map(c => c + c).join('');
      r = [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16),
        h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1];
    } else if ((m = s.match(/^rgba?\(([^)]+)\)$/i))) {
      const p = m[1].split(/[\s,/]+/).filter(Boolean).map(parseFloat);
      r = [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
    } else if (s === 'transparent') r = [0, 0, 0, 0];
    cacheRGBA.set(css, r);
    return r;
  };
  CV.css = ([r, g, b, a]) => `rgba(${Math.round(r)},${Math.round(g)},${Math.round(b)},${+a.toFixed(4)})`;
  /* color-mix(in srgb, a p%, b) — mélange prémultiplié, comme le navigateur */
  CV.mix = (a, p, b = 'transparent') => {
    const A = CV.rgba(a), B = CV.rgba(b), q = 1 - p;
    const al = A[3] * p + B[3] * q;
    if (al <= 0) return 'rgba(0,0,0,0)';
    const c = i => (A[i] * A[3] * p + B[i] * B[3] * q) / al;
    return CV.css([c(0), c(1), c(2), al]);
  };
  CV.alpha = (a, f) => { const A = CV.rgba(a); return CV.css([A[0], A[1], A[2], A[3] * f]); };

  /* ---------- toile hors écran ---------- */
  CV.toile = (l, h) => new OffscreenCanvas(Math.max(1, Math.ceil(l)), Math.max(1, Math.ceil(h)));

  /* ---------- fond pré-rendu (dégradés + taches + grain) ----------
     k = pixels de sortie par pixel de scène (0,5 en 540p, 2/3 en 720p).
     Reprend .cv-blob / .cv-grain / #stage de theme.css. */
  CV.Fond = function (theme, k, ambiance) {
    const L = 1920, H = 1080;
    // 1) fond : deux dégradés radiaux elliptiques sur la couleur de base
    const base = CV.toile(L * k, H * k);
    {
      const x = base.getContext('2d');
      x.scale(k, k);
      x.fillStyle = theme.fond1; x.fillRect(0, 0, L, H);
      const ellipse = (cx, cy, rx, ry, couleur) => {
        x.save(); x.translate(cx, cy); x.scale(1, ry / rx);
        const g = x.createRadialGradient(0, 0, 0, 0, 0, rx);
        g.addColorStop(0, couleur); g.addColorStop(0.6, CV.alpha(couleur, 0));
        x.fillStyle = g; x.fillRect(-rx, -rx, 2 * rx, 2 * rx); x.restore();
      };
      // radial-gradient(1200px 800px at 15% 10%, fond-2, transparent 60%) puis (1000px 700px at 90% 95%, fond-3, …)
      ellipse(L * 0.90, H * 0.95, 1000, 700, theme.fond3);
      ellipse(L * 0.15, H * 0.10, 1200, 800, theme.fond2);
    }
    // 2) taches floues : 760 px, blur(110px) ; la 3e plus petite et plus pâle
    const tache = (diam, couleur) => {
      const flou = 110, m = flou * 4, cote = diam + 2 * m;   // 4 σ : à 3 σ, le bord de l'image se voyait sur le fond sombre
      const c = CV.toile(cote * k, cote * k), x = c.getContext('2d');
      x.filter = `blur(${flou * k}px)`;
      x.fillStyle = couleur;
      x.beginPath(); x.arc(c.width / 2, c.height / 2, (diam / 2) * k, 0, Math.PI * 2); x.fill();
      return { toile: c, cote };
    };
    const blobs = [
      { ...tache(760, theme.violet), cx: -180 + 380, cy: -220 + 380, o: theme.blob },
      { ...tache(760, theme.cyan), cx: L + 200 - 380, cy: H + 260 - 380, o: theme.blob },
      { ...tache(560, theme.rose), cx: L * 0.45 + 280, cy: H * 0.30 + 280, o: theme.blob / 2 },
    ];
    // 3) grain : points de 1,2 px tous les 34 px, opacité de calque 0,5
    const grain = CV.toile(L * k, H * k);
    {
      const x = grain.getContext('2d');
      x.scale(k, k); x.globalAlpha = 0.5;
      const motif = CV.toile(34 * k * 4, 34 * k * 4), y = motif.getContext('2d');
      y.scale(k, k);
      const g = theme.grain;
      for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
        const gr = y.createRadialGradient(17 + 34 * i, 17 + 34 * j, 0, 17 + 34 * i, 17 + 34 * j, 1.3);
        gr.addColorStop(0, g); gr.addColorStop(1.2 / 1.3, g); gr.addColorStop(1, CV.alpha(g, 0));
        y.fillStyle = gr; y.fillRect(34 * i + 15, 34 * j + 15, 4, 4);
      }
      x.setTransform(1, 0, 0, 1, 0, 0);
      x.fillStyle = x.createPattern(motif, 'repeat');
      x.fillRect(0, 0, grain.width, grain.height);
    }

    /* dessine le fond à l'instant t (contexte en coordonnées de scène) */
    this.dessiner = (ctx, t) => {
      ctx.save();
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.drawImage(base, 0, 0);
      ctx.restore();
      blobs.forEach((b, i) => {
        let dx = 0, dy = 0, s = 1;
        if (ambiance) {   // même mouvement que installerAmbiance() de capsule.js
          const f = 0.05 + i * 0.017, ph = i * 2.1;
          dx = Math.sin(t * f * 6.28 + ph) * 160; dy = Math.cos(t * f * 5.1 + ph) * 110;
          s = 1 + 0.12 * Math.sin(t * f * 3 + ph);
        }
        const c = b.cote * s;
        ctx.globalAlpha = b.o;
        ctx.drawImage(b.toile, b.cx + dx - c / 2, b.cy + dy - c / 2, c, c);
      });
      ctx.globalAlpha = 1;
      ctx.save();
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.drawImage(grain, 0, 0);
      ctx.restore();
    };
  };
})(typeof self !== 'undefined' ? self : this);
