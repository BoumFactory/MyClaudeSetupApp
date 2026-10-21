/* =====================================================================
   Figures géométriques en primitives (moteur canvas)
   ---------------------------------------------------------------------
   { id: 'fig', l: 960, h: 500, figure: {
       vue: [0, -25, 960, 500],                 // repère de la figure (comme un viewBox SVG)
       points: { A: [455, 70], B: [230, 395] },
       objets: [
         { id: 'ab', segment: ['A', 'B'], couleur: 'vert', epaisseur: 7, t: [0, 1.2], main: [4, -3] },
         { id: 'd1', droite: ['A', 'I'], couleur: 'rose' },       // tracée d'un bord à l'autre de la vue
         { demi: ['A', 'B'] },                                    // demi-droite [AB)
         { angle: ['C', 'A', 'I'], r: 118, couleur: 'violet' },   // arc de C vers I autour de A (sens horaire à l'écran)
         { secteur: ['C', 'A', 'I'], r: 118, remplir: 'violet', opacite: 0.16 },
         { droit: ['C', 'A', 'B'], r: 34 },                       // codage d'angle droit
         { egal: ['A', 'B'], n: 2 },                              // codage de segments égaux
         { bande: [['A', 'I'], ['B', 'C']], remplir: 'rose', opacite: 0.13 },
         { polygone: ['A', 'B', 'C'], remplir: 'cyan', opacite: 0.2 },
         { cercle: 'A', r: 50 }, { point: 'A' },
         { chemin: 'M20 160 A130 130 0 0 1 280 160 Z', couleur: 'doux', remplir: 'rgba(255,255,255,.07)' },
         { id: 'lA', etiquette: 'A', en: [424, 40] },             // étiquette TeX centrée en (424 ; 40)
       ] } }
   Options de style : couleur (trait), epaisseur (5), remplir, opacite, pointilles: [a, b], taille (étiquette, 46).
   Chaque objet est un nœud : trace, apparait, clignote, allume, pointe… le visent par son id.
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});
  const f1 = v => (Math.round(v * 10) / 10).toFixed(1);
  const pt = p => f1(p[0]) + ' ' + f1(p[1]);
  const rad = d => d * Math.PI / 180, deg = r => r * 180 / Math.PI;
  const ang = (p, q) => deg(Math.atan2(q[1] - p[1], q[0] - p[0]));
  const pol = (p, a, r) => [p[0] + r * Math.cos(rad(a)), p[1] + r * Math.sin(rad(a))];

  /* intersection de la droite (P, u) avec le rectangle de la vue → [t0, t1] */
  function couperVue(P, u, v) {
    let t0 = -Infinity, t1 = Infinity;
    const lim = [[v[0], v[0] + v[2]], [v[1], v[1] + v[3]]];
    for (let k = 0; k < 2; k++) {
      if (Math.abs(u[k]) < 1e-9) { if (P[k] < lim[k][0] || P[k] > lim[k][1]) return null; continue; }
      let a = (lim[k][0] - P[k]) / u[k], b = (lim[k][1] - P[k]) / u[k];
      if (a > b) [a, b] = [b, a];
      t0 = Math.max(t0, a); t1 = Math.min(t1, b);
    }
    return t0 <= t1 ? [t0, t1] : null;
  }

  /* objet de figure → { d, trait, plein } en unités de la figure */
  function geometrie(o, P, vue, E) {
    const p = x => (Array.isArray(x) ? x : P[x] || (E.erreur('Point inconnu dans la figure : ' + x), [0, 0]));
    if (o.segment) {
      const [A, B] = o.segment.map(p), [t0, t1] = o.t || [0, 1];
      const a = [A[0] + (B[0] - A[0]) * t0, A[1] + (B[1] - A[1]) * t0], b = [A[0] + (B[0] - A[0]) * t1, A[1] + (B[1] - A[1]) * t1];
      if (o.main) {   // tracé à main levée : cubique décalée selon la normale
        const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L, [o1, o2] = o.main;
        return { d: 'M' + pt(a) + ' C' + pt([a[0] + dx / 3 + nx * o1, a[1] + dy / 3 + ny * o1]) + ' ' +
          pt([a[0] + 2 * dx / 3 + nx * o2, a[1] + 2 * dy / 3 + ny * o2]) + ' ' + pt(b), trait: true };
      }
      return { d: 'M' + pt(a) + ' L' + pt(b), trait: true };
    }
    if (o.droite || o.demi) {
      const [A, B] = (o.droite || o.demi).map(p);
      let u = [B[0] - A[0], B[1] - A[1]];
      const c = couperVue(A, u, vue);
      if (!c) return { d: 'M0 0', trait: true };
      let [t0, t1] = c;
      if (o.demi) t0 = 0;
      let a = [A[0] + u[0] * t0, A[1] + u[1] * t0], b = [A[0] + u[0] * t1, A[1] + u[1] * t1];
      if (o.droite && (a[0] > b[0] + 1e-6 || (Math.abs(a[0] - b[0]) < 1e-6 && a[1] > b[1]))) [a, b] = [b, a];
      if (o.sens === -1) [a, b] = [b, a];
      return { d: 'M' + pt(a) + ' L' + pt(b), trait: true };
    }
    if (o.angle || o.secteur) {
      const [A, O, B] = (o.angle || o.secteur).map(p), r = o.r || 40;
      const a1 = ang(O, A), a2 = ang(O, B);
      let balayage = ((a2 - a1) % 360 + 360) % 360;
      const grand = balayage > 180 ? 1 : 0;
      const arc = 'A' + r + ' ' + r + ' 0 ' + grand + ' 1 ' + pt(pol(O, a2, r));
      if (o.secteur) return { d: 'M' + pt(O) + ' L' + pt(pol(O, a1, r)) + ' ' + arc + ' Z', plein: true };
      return { d: 'M' + pt(pol(O, a1, r)) + ' ' + arc, trait: true };
    }
    if (o.droit) {
      const [A, O, B] = o.droit.map(p), r = o.r || 30;
      const p1 = pol(O, ang(O, A), r), p2 = pol(O, ang(O, B), r);
      return { d: 'M' + pt(p1) + ' L' + pt([p1[0] + p2[0] - O[0], p1[1] + p2[1] - O[1]]) + ' L' + pt(p2), trait: true };
    }
    if (o.egal) {
      const [A, B] = o.egal.map(p), n = o.n || 1, M = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2];
      const L = Math.hypot(B[0] - A[0], B[1] - A[1]), u = [(B[0] - A[0]) / L, (B[1] - A[1]) / L], nn = [-u[1], u[0]];
      const h = o.r || 14, e = 9;
      let d = '';
      for (let i = 0; i < n; i++) {
        const c = [M[0] + u[0] * e * (i - (n - 1) / 2), M[1] + u[1] * e * (i - (n - 1) / 2)];
        d += 'M' + pt([c[0] - nn[0] * h + u[0] * 3, c[1] - nn[1] * h + u[1] * 3]) + ' L' + pt([c[0] + nn[0] * h - u[0] * 3, c[1] + nn[1] * h - u[1] * 3]) + ' ';
      }
      return { d: d.trim(), trait: true };
    }
    if (o.bande) {
      const [[A, B], [C, D]] = o.bande.map(x => x.map(p));
      const y = (P1, P2, x) => P1[1] + (x - P1[0]) * (P2[1] - P1[1]) / (P2[0] - P1[0]);
      const x0 = vue[0], x1 = vue[0] + vue[2];
      return { d: 'M' + pt([x0, y(A, B, x0)]) + ' L' + pt([x1, y(A, B, x1)]) + ' L' + pt([x1, y(C, D, x1)]) + ' L' + pt([x0, y(C, D, x0)]) + ' Z', plein: true };
    }
    if (o.polygone) return { d: 'M' + o.polygone.map(x => pt(p(x))).join(' L') + ' Z', plein: !!o.remplir, trait: !!o.couleur || !o.remplir };
    if (o.cercle) {
      const O = p(o.cercle), r = o.r || 40;
      return { d: 'M' + pt([O[0] + r, O[1]]) + ' A' + r + ' ' + r + ' 0 1 1 ' + pt([O[0] - r, O[1]]) + ' A' + r + ' ' + r + ' 0 1 1 ' + pt([O[0] + r, O[1]]),
        plein: !!o.remplir, trait: !!o.couleur || !o.remplir };
    }
    if (o.point) {
      const O = p(o.point), r = o.r || 6;
      return { d: 'M' + pt([O[0] + r, O[1]]) + ' A' + r + ' ' + r + ' 0 1 1 ' + pt([O[0] - r, O[1]]) + ' A' + r + ' ' + r + ' 0 1 1 ' + pt([O[0] + r, O[1]]), plein: true, couleurPlein: true };
    }
    if (o.chemin) return { d: o.chemin, plein: !!o.remplir, trait: o.couleur !== undefined || !o.remplir };
    E.erreur('Objet de figure inconnu : ' + JSON.stringify(o).slice(0, 80));
    return { d: 'M0 0' };
  }

  CV.TYPES.figure = {
    tailleLibre: true,
    creer(n, E) {
      const F = n.spec.figure;
      n.vue = F.vue || [0, 0, n.spec.l || 400, n.spec.h || 300];
      const P = F.points || {};
      n.objets = [];
      for (const o of F.objets || []) {
        if (o.etiquette !== undefined) {
          // l'étiquette est déjà du TeX : un « $ » s'afficherait tel quel à l'écran
          if (/(^|[^\\])\$/.test(String(o.etiquette))) E.erreur('Étiquette de figure « ' + o.etiquette + ' » : retirer les $ (l\'étiquette est déjà du TeX)');
          const spec = { tex: String(o.etiquette), taille: o.taille || 46, id: o.id, couleur: o.couleur };
          for (const g of CV.RACCOURCIS) if (o[g] !== undefined) spec[g] = o[g];
          const e = CV.creerNoeud(spec, n, E);
          e.en = o.en || [0, 0];
          e.tailleBase = o.taille || 46;
          if (o.rotation !== undefined) e.s.rotation = o.rotation;   // degrés : étiquette posée le long d'un segment
          n.enfants.push(e);
          continue;
        }
        const m = new CV.Noeud('fobj', o, n, E);
        m.geo = geometrie(o, P, n.vue, E);
        m.chemin = E.prep.chemin(m.geo.d);
        m.fig = n;
        n.enfants.push(m);
        n.objets.push(m);
      }
    },
    mesurer(n, W, E) {
      const L = n.spec.l || n.vue[2], H = n.spec.h || n.vue[3];
      const sc = Math.min(1, W / L);
      n.lw = L * sc; n.lh = H * sc;
      n.u = (L / n.vue[2]) * sc;           // px locaux par unité de figure
      for (const e of n.enfants) if (e.type === 'tex') { e.spec.taille = e.tailleBase * sc; CV.mesurer(e, 4000, E); }
    },
    disposer(n, E) {
      for (const e of n.enfants) {
        if (e.type === 'tex') {
          const cx = (e.en[0] - n.vue[0]) * n.u, cy = (e.en[1] - n.vue[1]) * n.u;
          e.lx = cx - e.lw / 2; e.ly = cy - e.lh / 2;
          CV.disposer(e, E);
        } else { e.lx = 0; e.ly = 0; e.lw = 0; e.lh = 0; }
      }
    },
    apresPlacer(n) {
      const k = n.u * n.z;
      for (const m of n.objets) {
        const c = m.chemin, e = (m.spec.epaisseur || 5) / 2;
        m.b = { x: n.b.x + (c.x - e - n.vue[0]) * k, y: n.b.y + (c.y - e - n.vue[1]) * k, w: (c.w + 2 * e) * k, h: (c.h + 2 * e) * k };
        m.z = n.z;
      }
    },
  };

  CV.TYPES.fobj = {
    creer() {}, mesurer() {}, dynamique: true,
    peindre(ctx, m, E) {
      const n = m.fig, o = m.spec, s = m.s, g = m.geo;
      if (!m.p2d) m.p2d = new Path2D(g.d);
      ctx.save();
      ctx.translate(n.b.x, n.b.y);
      ctx.scale(n.u * n.z, n.u * n.z);
      ctx.translate(-n.vue[0], -n.vue[1]);
      if (g.plein && o.remplir !== undefined || g.couleurPlein) {
        const c = CV.couleur(E.theme, g.couleurPlein ? (o.remplir || o.couleur || 'texte') : o.remplir);
        const a0 = ctx.globalAlpha;
        ctx.globalAlpha = a0 * (o.opacite ?? 1);
        ctx.fillStyle = c;
        ctx.fill(m.p2d);
        ctx.globalAlpha = a0;
      }
      if (g.trait && !g.couleurPlein && s.trace > 0.001) {
        ctx.strokeStyle = CV.couleur(E.theme, o.couleur, 'texte');
        ctx.lineWidth = o.epaisseur || 5;
        ctx.lineCap = o.bout || 'round'; ctx.lineJoin = 'round';
        const L = m.chemin.l;
        if (s.trace < 0.999) ctx.setLineDash([L * s.trace, L + 10]);
        else if (o.pointilles) ctx.setLineDash(o.pointilles);
        ctx.stroke(m.p2d);
      }
      ctx.restore();
    },
  };
})(typeof self !== 'undefined' ? self : this);
