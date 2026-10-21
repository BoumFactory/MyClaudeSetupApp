/* =====================================================================
   Dessin du graphe de scène sur un canvas 2D (OffscreenCanvas ou écran)
   ---------------------------------------------------------------------
   Le contexte est en coordonnées de scène (1920×1080) multipliées par k.
   Chaque élément constant (carte avec son ombre, texte, formule, puce)
   est peint UNE fois dans une petite image (« sprite ») à la résolution
   de sortie, puis seulement déplacé : c'est ce qui rend le canvas rapide
   sans rien perdre du design. Transformations GSAP (x, y, échelle,
   rotation, opacité) et découpe d'écriture appliquées à l'image.
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});

  /* ---------- sprites ---------- */
  CV.sprite = (n, E, opts) => {
    const cle = opts && opts.cle ? opts.cle : 'base';
    n.sprites = n.sprites || {};
    if (n.sprites[cle]) return n.sprites[cle];
    const T = CV.TYPES[n.type];
    const mb = typeof T.marge === 'function' ? T.marge(n) : (T.marge ?? 10);
    const m = mb * n.z + (opts && opts.lueur ? opts.lueur * 2.2 : 0);
    const sur = opts && opts.sur ? opts.sur : 1;
    const k = E.k * sur;
    const x0 = n.b.x - m, y0 = n.b.y - m, w = n.b.w + 2 * m, h = n.b.h + 2 * m;
    const c = CV.toile(w * k, h * k);
    const ctx = c.getContext('2d');
    ctx.setTransform(k, 0, 0, k, -x0 * k, -y0 * k);
    if (opts && opts.lueur) {   // text-shadow 0 0 Xpx currentColor (clone qui vole)
      ctx.shadowColor = opts.couleur; ctx.shadowBlur = opts.lueur * k;
    }
    if (opts && opts.sousArbre) CV.peindreSousArbre(ctx, n, E, opts);
    else T.peindre(ctx, n, E, opts);
    const sp = { c, x0, y0, w: c.width / k, h: c.height / k, k };
    n.sprites[cle] = sp;
    return sp;
  };
  /* contenu statique de n et de ses descendants (pour les clones de `vole`) */
  /* contenu seulement, comme l'innerHTML cloné par le moteur HTML : le décor de la racine (carte, encadré,
     pilule de résultat, tableau) n'est pas recopié */
  const DECORS = ['carte', 'encadrer', 'resultat', 'methode', 'tableau'];
  CV.peindreSousArbre = (ctx, n, E, opts, racine = true) => {
    const T = CV.TYPES[n.type];
    if (T.peindre && (!T.dynamique || T.sousArbreOK) && !(racine && DECORS.includes(n.type))) T.peindre(ctx, n, E, opts);
    for (const c of n.enfants) CV.peindreSousArbre(ctx, c, E, opts, false);
  };

  /* dessine un sprite ; aligné sur les pixels quand la transformation est une simple translation */
  CV.poserSprite = (ctx, sp, clip) => {
    const m = ctx.getTransform();
    if (m.b === 0 && m.c === 0 && Math.abs(m.a - sp.k) < 1e-6 && Math.abs(m.d - sp.k) < 1e-6 && !clip) {
      const dx = Math.round(m.a * sp.x0 + m.e), dy = Math.round(m.d * sp.y0 + m.f);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.drawImage(sp.c, dx, dy);
      ctx.restore();
    } else ctx.drawImage(sp.c, sp.x0, sp.y0, sp.w, sp.h);
  };

  /* ---------- calques temporaires (flou de scène, mise au point) ---------- */
  function calque(E, prof) {
    E.calquesTemp = E.calquesTemp || [];
    let c = E.calquesTemp[prof];
    if (!c) { c = CV.toile(1920 * E.k, 1080 * E.k); E.calquesTemp[prof] = c; }
    const x = c.getContext('2d');
    x.setTransform(1, 0, 0, 1, 0, 0);
    x.clearRect(0, 0, c.width, c.height);
    x.setTransform(E.k, 0, 0, E.k, 0, 0);
    return c;
  }

  /* ---------- parcours ---------- */
  CV.dessinerNoeud = (ctx, n, E, t, prof = 0) => {
    const s = n.s;
    if (s.o <= 0.002 || n.invisible) return;
    if (s.lev > 0.5 && !E.passeLevee) { (E.levees = E.levees || []).push(n); return; }   // tuile soulevée : redessinée au-dessus de la scène
    if ((s.flou > 0.05 || s.lum < 0.999 || s.sat < 0.999) && !n.dansCalque) {
      const c = calque(E, prof);
      const x = c.getContext('2d');
      n.dansCalque = true;
      const o = s.o; s.o = 1;
      CV.dessinerNoeud(x, n, E, t, prof + 1);
      s.o = o; n.dansCalque = false;
      ctx.save();
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      const f = [];
      if (s.flou > 0.05) f.push(`blur(${(s.flou * E.k).toFixed(2)}px)`);
      if (s.lum < 0.999) f.push(`brightness(${s.lum.toFixed(3)})`);
      if (s.sat < 0.999) f.push(`saturate(${s.sat.toFixed(3)})`);
      ctx.filter = f.join(' ');
      ctx.globalAlpha *= o;
      ctx.drawImage(c, 0, 0);
      ctx.restore();
      return;
    }
    const b = n.b;
    ctx.save();
    if (s.o < 1) ctx.globalAlpha *= s.o;
    const sx = s.scale * s.scaleX, sy = s.scale * s.scaleY;
    if (s.pliage < 0.999) {   // compacte : la hauteur visible se replie vers le haut, le contenu est rogné (pas écrasé)
      if (s.pliage <= 0.002) { ctx.restore(); return; }
      ctx.beginPath(); ctx.rect(b.x - 200, b.y + s.y - 200, b.w + 400, 200 + b.h * s.pliage); ctx.clip();
    }
    if (s.x || s.y || s.rotation || sx !== 1 || sy !== 1) {
      const cx = b.x + b.w / 2, cy = b.y + b.h / 2;
      ctx.translate(cx + s.x, cy + s.y);
      if (s.rotation) ctx.rotate(s.rotation * Math.PI / 180);
      if (sx !== 1 || sy !== 1) ctx.scale(sx || 1e-4, sy || 1e-4);
      ctx.translate(-cx, -cy);
    }
    const clip = s.clip < 0.999;
    if (clip) {
      // ecrit : inset(-30% R -30% -3%) avec R de 101 % à -3 % (comme capsule.js)
      const droite = b.w * (-0.01 + 1.04 * Math.max(0, s.clip));
      ctx.beginPath(); ctx.rect(b.x - 0.03 * b.w, b.y - 0.3 * b.h, droite + 0.03 * b.w, b.h * 1.6); ctx.clip();
    }
    if (n.surligneurs) for (const h of n.surligneurs) CV.dessinerSurligneur(ctx, n, h, E);
    const T = CV.TYPES[n.type];
    if (n.compteur) CV.peindreCompteur(ctx, n, E);
    else if (T.peindre) {
      if (T.dynamique || n.dynamique) T.peindre(ctx, n, E, null, t);
      else if (T.sprite) CV.poserSprite(ctx, CV.sprite(n, E), clip);
    }
    for (const c of n.enfants) CV.dessinerNoeud(ctx, c, E, t, prof);
    ctx.restore();
  };

  /* tuiles soulevées (geste deplace, annule) : dessinées après la scène, par-dessus tout */
  CV.dessinerLevees = (ctx, E, t) => {
    const l = E.levees;
    if (!l || !l.length) return;
    E.levees = []; E.passeLevee = true;
    for (const n of l) {
      let a = 1;
      for (let p = n.parent; p; p = p.parent) a *= p.s.o;
      ctx.save(); ctx.globalAlpha *= a;
      CV.dessinerNoeud(ctx, n, E, t);
      ctx.restore();
    }
    E.passeLevee = false;
  };

  /* surligneur fluo : derrière le texte, de -6 px à +6 px, de 18 % à 96 % de la hauteur */
  CV.dessinerSurligneur = (ctx, n, h, E) => {
    if (h.s.scaleX <= 0.001) return;
    const b = n.b, z = n.z;
    const x = b.x - 6 * z, y = b.y + b.h * 0.18, w = (b.w + 12 * z) * h.s.scaleX, hh = b.h * 0.78;
    ctx.beginPath(); ctx.roundRect(x, y, w, hh, Math.min(8 * z, w / 2));
    ctx.fillStyle = h.couleur; ctx.fill();
  };
})(typeof self !== 'undefined' ? self : this);
