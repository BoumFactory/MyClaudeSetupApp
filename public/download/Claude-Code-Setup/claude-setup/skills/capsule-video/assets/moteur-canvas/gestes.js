/* =====================================================================
   Gestes du moteur canvas — même catalogue que references/gestes.md
   ---------------------------------------------------------------------
   Tous de la forme C.geste(cible, t, options) ; cible = '#id', 'id',
   '.classe', nœud, ou tableau de ces écritures ; t résolu par C.temps
   (ancres.js, code repris tel quel de capsule.js). GSAP anime de simples
   objets JS (n.s = { x, y, scale, scaleX, scaleY, rotation, o, clip,
   trace, lum, sat, flou, pliage }) : il fonctionne dans un worker.
   Différence avec le moteur HTML : l'état initial « caché » est déduit
   tout seul (un élément dont le premier geste est une entrée — montre,
   tombe, ecrit, trace, apparait, cible de vole… — part invisible).
   ===================================================================== */
(function (racine) {
  const CV = (racine.CV = racine.CV || {});

  CV.creerGestes = function (E, tl, A) {
    const C = Object.assign({}, A);   // hasard, W, cherche, tempsFort, temps
    const tt = A.temps;
    C.tl = tl;
    C.erreur = E.erreur;
    const journal = [];               // { n, t, sens: 'entree' | 'sortie' }
    const hooks = [];
    E.hooks = hooks;
    E.calque = E.calque || [];
    const theme = E.theme;
    const couleur = c => CV.couleur(theme, c, 'ambre');
    const fr = (x, d) => Number(x).toFixed(d).replace('.', ',');

    /* ---------- sélection ---------- */
    const tous = c => {
      if (c === null || c === undefined) return [];
      if (Array.isArray(c)) return c.flatMap(tous);
      if (c instanceof CV.Noeud) return [c];
      if (c && c.s && c.dessiner) return [c];          // élément du calque (halo renvoyé par allume)
      if (typeof c === 'string') {
        return c.split(',').map(x => x.trim()).filter(Boolean).flatMap(x => {
          if (x[0] === '.') { const cl = x.slice(1); return E.noeuds.filter(n => n.classes.includes(cl)); }
          const id = x[0] === '#' ? x.slice(1) : x;
          const n = E.ids.get(id);
          if (!n) { E.erreur('Élément introuvable : ' + x); return []; }
          return [n];
        });
      }
      return [];
    };
    const un = c => { const l = tous(c); return l[0] || null; };
    const etats = c => tous(c).map(n => n.s);
    C.un = un; C.tous = tous;
    C.etat = c => { const l = etats(c); return l.length === 1 ? l[0] : l; };
    const noter = (c, t, sens) => tous(c).forEach(n => journal.push({ n, t, sens }));

    /* boîte (repère 1920×1080) d'un nœud ou de l'union de plusieurs */
    const boite = c => {
      if (c && typeof c === 'object' && !Array.isArray(c) && !(c instanceof CV.Noeud) && c.cx !== undefined) return c;   // boîte { cx, cy, w, h } donnée telle quelle
      const l = tous(c);
      if (!l.length) return { x: 0, y: 0, w: 0, h: 0, cx: 0, cy: 0 };
      const x = Math.min(...l.map(n => n.b.x)), y = Math.min(...l.map(n => n.b.y));
      const x2 = Math.max(...l.map(n => n.b.x + n.b.w)), y2 = Math.max(...l.map(n => n.b.y + n.b.h));
      return { x, y, w: x2 - x, h: y2 - y, cx: (x + x2) / 2, cy: (y + y2) / 2 };
    };
    C.boite = boite;

    /* élément du calque (au-dessus des scènes) */
    const item = (dessiner, s) => {
      const it = { s: Object.assign(CV.etatInitial(), s || {}), dessiner };
      E.calque.push(it);
      return it;
    };
    C.ajouter = (dessiner, s) => item(dessiner, s);   // échappatoire : élément dessiné à la main
    const transformer = (ctx, s, cx, cy) => {
      ctx.globalAlpha *= s.o;
      if (s.x || s.y || s.rotation || s.scale !== 1) {
        ctx.translate(cx + s.x, cy + s.y);
        if (s.rotation) ctx.rotate(s.rotation * Math.PI / 180);
        ctx.scale(s.scale, s.scale);
        ctx.translate(-cx, -cy);
      }
    };

    /* =====================================================================
       Apparitions et sorties
       ===================================================================== */
    C.montre = (c, t, o = {}) => {
      noter(c, tt(t), 'entree');
      return tl.fromTo(etats(c), { o: 0, y: o.y ?? 26, scale: o.scale ?? 0.94 },
        { o: 1, y: 0, scale: 1, duration: o.dur ?? 0.6, ease: o.ease ?? 'back.out(1.6)',
          stagger: o.stagger ?? 0, immediateRender: false }, tt(t));
    };
    C.cache = (c, t, o = {}) => {
      noter(c, tt(t), 'sortie');
      return tl.to(etats(c), { o: 0, y: o.y ?? -12, scale: o.scale ?? 0.97, duration: o.dur ?? 0.4,
        ease: 'power2.in', stagger: o.stagger ?? 0 }, tt(t));
    };
    C.tombe = (c, t, o = {}) => {
      const t0 = tt(t), d = o.dur ?? 0.75;
      noter(c, t0, 'entree');
      tl.fromTo(etats(c), { o: 0, y: -(o.hauteur ?? 260), rotation: o.rotation ?? -10, scale: 1.25 },
        { o: 1, y: 0, rotation: 0, scale: 1, duration: d, ease: 'bounce.out',
          stagger: o.stagger ?? 0, immediateRender: false }, t0);
      if (o.onde !== false) tous(c).forEach((n, k) => C.onde(n, t0 + d * 0.38 + k * (o.stagger ?? 0), { couleur: o.couleur }));
      return tl;
    };
    C.ecrit = (c, t, o = {}) => {
      const t0 = tt(t);
      noter(c, t0, 'entree');
      tl.set(etats(c), { o: 1 }, t0);
      return tl.fromTo(etats(c), { clip: 0 }, { clip: 1, duration: o.dur ?? 0.9, ease: o.ease ?? 'power1.inOut',
        stagger: o.stagger ?? 0, immediateRender: false }, t0);
    };
    C.pulse = (c, t, o = {}) => tl.fromTo(etats(c), { scale: 1 },
      { scale: o.scale ?? 1.18, duration: (o.dur ?? 0.5) / 2, yoyo: true, repeat: 1,
        ease: 'power2.out', immediateRender: false }, tt(t));
    C.secoue = (c, t, o = {}) => tl.fromTo(etats(c), { x: 0 },
      { keyframes: { x: [0, -14, 12, -8, 5, 0] }, duration: o.dur ?? 0.5, ease: 'none', immediateRender: false }, tt(t));

    /* Tracé progressif d'un objet de figure (ex-helper trace des scenes.js) : trace(c, t, dur) ou trace(c, t, { dur }) */
    C.trace = (c, t, o = {}) => {
      if (typeof o === 'number') o = { dur: o };
      const t0 = tt(t);
      noter(c, t0, 'entree');
      tl.set(etats(c), { o: 1 }, t0);
      return tl.fromTo(etats(c), { trace: 0 }, { trace: 1, duration: o.dur ?? 0.7, ease: o.ease ?? 'power1.inOut',
        stagger: o.stagger ?? 0, immediateRender: false }, t0);
    };
    /* Fondu vers une opacité (ex-helper fond) : apparait(c, t, dur, vers) ou apparait(c, t, { dur, vers }) */
    C.apparait = (c, t, o = {}, vers) => {
      if (typeof o === 'number') o = { dur: o, vers };
      const v = o.vers ?? 1;
      noter(c, tt(t), v > 0 ? 'entree' : 'sortie');
      return tl.to(etats(c), { o: v, duration: o.dur ?? 0.5, ease: o.ease ?? 'power1.out' }, tt(t));
    };
    C.fond = C.apparait;
    /* Clignotement (ex-helper blink) : clignote(c, t, n, bas) ou clignote(c, t, { n, bas }) */
    C.clignote = (c, t, o = {}, bas) => {
      if (typeof o === 'number') o = { n: o, bas };
      const t0 = tt(t), n = o.n ?? 3, b = o.bas ?? 0.2, s = etats(c);
      for (let i = 0; i < n; i++) {
        tl.to(s, { o: b, duration: 0.18, ease: 'power1.in' }, t0 + i * 0.5);
        tl.to(s, { o: 1, duration: 0.22, ease: 'power1.out' }, t0 + i * 0.5 + 0.2);
      }
      return tl;
    };

    /* Bascule dans une pile : a sort vers le haut, b entre au même endroit */
    C.remplace = (a, b, t, o = {}) => {
      const t0 = tt(t);
      noter(a, t0, 'sortie'); noter(b, t0 + 0.25, 'entree');
      tl.to(etats(a), { o: 0, y: -30, duration: 0.35, ease: 'power2.in' }, t0);
      tl.fromTo(etats(b), { o: 0, y: 30 }, { o: 1, y: 0, duration: 0.5, ease: 'back.out(1.7)', immediateRender: false }, t0 + 0.25);
      return tl;
    };

    /* Compteur animé (format français, chiffres de la police des formules) */
    C.compte = (c, t, o = {}) => {
      const d = o.decimales ?? 0, t0 = tt(t);
      noter(c, t0, 'entree');
      tous(c).forEach(n => {
        const obj = { v: o.de ?? 0 };
        n.compteur = () => fr(obj.v, d);
        n.dynamique = true;
        tl.set(n.s, { o: 1 }, t0);
        tl.fromTo(obj, { v: o.de ?? 0 }, { v: o.a, duration: o.dur ?? 1.0, ease: 'power2.out', immediateRender: false }, t0);
      });
      return tl;
    };

    /* Changement de scène plein écran (fondu flou) */
    let sceneCourante = null;
    C.scene = (c, t, o = {}) => {
      const t0 = tt(t);
      (E.instantsScenes = E.instantsScenes || []).push(t0 + (sceneCourante ? 0.3 : 0) + (o.dur ?? 0.7));   // fin du fondu
      if (sceneCourante) tl.to(etats(sceneCourante), { o: 0, scale: 0.96, flou: 8, duration: 0.5, ease: 'power2.in' }, t0);
      tl.fromTo(etats(c), { o: 0, scale: 1.04, flou: 8 },
        { o: 1, scale: 1, flou: 0, duration: o.dur ?? 0.7, ease: 'power2.out', immediateRender: false }, t0 + (sceneCourante ? 0.3 : 0));
      sceneCourante = c;
      return tl;
    };

    /* « Dérouler puis compacter » : les lignes détaillées se replient (leur hauteur va à 0, le contenu est rogné
       par le bas, comme height → 0 en CSS) ; tout ce qui suit dans le flux remonte, à TOUS les niveaux
       (colonne de la carte, puis colonne qui contient la carte…), et chaque carte traversée rétrécit. */
    C.compacte = (details, resume, t, o = {}) => {
      const t0 = tt(t), d = o.dur ?? 0.7, ease = 'power2.inOut';
      const ds = tous(details);
      noter(ds, t0, 'sortie');
      ds.forEach(n => tl.fromTo(n.s, { pliage: 1, o: 1 }, { pliage: 0, o: 0, duration: d, ease, immediateRender: false }, t0));
      const remonter = (e, v) => tl.to(e.s, { y: '-=' + v, duration: d, ease }, t0);
      const parParent = new Map();
      ds.forEach(n => { const p = n.parent; if (!parParent.has(p)) parParent.set(p, []); parParent.get(p).push(n); });
      for (const [p, liste] of parParent) {
        if (!p) continue;
        const ec = (p.spec.ecart ?? 26) * p.z;
        let cumul = 0;
        for (const e of p.enfants) {   // une ligne repliée fait remonter TOUT ce qui la suit, lignes repliées comprises
          if (cumul > 0) remonter(e, cumul);
          if (liste.includes(e)) cumul += e.b.h + ec;
        }
        // remontée en cascade jusqu'à la zone (ou l'étape de pile) qui contient tout
        let enfant = p;
        for (let q = p.parent; q && q.type !== 'zone' && !enfant.zoomPropre; enfant = q, q = q.parent) {
          if (q.type === 'carte') {
            q.reduction = q.reduction || { v: 0 };
            q.dynamique = true;
            tl.to(q.reduction, { v: '+=' + cumul, duration: d, ease }, t0);
          } else if (q.type === 'colonne') {
            const fr = q.enfants;
            for (const e of fr.slice(fr.indexOf(enfant) + 1)) remonter(e, cumul);
          } else break;   // ligne, pile, tableau… : la hauteur ne se propage pas
        }
      }
      if (o.depuis) C.vole(o.depuis, resume, t0, { couleur: o.couleur, dur: d + 0.2 });
      else C.montre(resume, t0 + d * 0.5);
      if (o.couleur !== null) C.onde(resume, t0 + d + 0.1, { couleur: o.couleur });
      return tl;
    };

    /* =====================================================================
       Désigner, relier, célébrer
       ===================================================================== */
    C.onde = (c, t, o = {}) => {
      const b = boite(c), r = Math.max(b.w, b.h) * (o.taille ?? 0.75);
      const col = couleur(o.couleur ?? '--ambre');
      const it = item((ctx, E2, s) => {
        if (s.o <= 0.002) return;
        ctx.save(); ctx.globalAlpha *= s.o;
        ctx.beginPath(); ctx.arc(b.cx, b.cy, Math.max(0.1, (r - 2.5) * s.scale), 0, Math.PI * 2);
        ctx.lineWidth = 5 * s.scale; ctx.strokeStyle = col; ctx.stroke();
        ctx.restore();
      }, { o: 0 });
      tl.fromTo(it.s, { o: 0.9, scale: 0.3 }, { o: 0, scale: 1.6, duration: o.dur ?? 0.8, ease: 'power2.out', immediateRender: false }, tt(t));
      return tl;
    };

    C.eclat = (c, t, o = {}) => {
      const b = boite(c), n = o.n ?? 22, rnd = C.hasard(o.graine ?? Math.round(b.cx + b.cy));
      const pal = (o.couleurs || ['--rose', '--cyan', '--ambre', '--violet', '--vert']).map(couleur);
      const t0 = tt(t);
      for (let k = 0; k < n; k++) {
        const taille = 8 + rnd() * 12, rond = rnd() < 0.5, col = pal[k % pal.length];
        const it = item((ctx, E2, s) => {
          if (s.o <= 0.002) return;
          ctx.save(); ctx.globalAlpha *= s.o;
          ctx.translate(b.cx + s.x, b.cy + s.y); ctx.rotate(s.rotation * Math.PI / 180); ctx.scale(s.scale, s.scale);
          ctx.fillStyle = col; ctx.beginPath();
          if (rond) ctx.arc(0, 0, taille / 2, 0, Math.PI * 2); else ctx.roundRect(-taille / 2, -taille / 2, taille, taille, 3);
          ctx.fill(); ctx.restore();
        }, { o: 0 });
        const a = (k / n) * Math.PI * 2 + rnd() * 0.4, v = (o.force ?? 220) * (0.6 + rnd() * 0.7);
        const dx = Math.cos(a) * v, dy = Math.sin(a) * v;
        tl.fromTo(it.s, { o: 1, x: 0, y: 0, rotation: 0, scale: 1 },
          { keyframes: { x: [0, dx * 0.7, dx], y: [0, dy * 0.7 - 30, dy + 120] },
            rotation: rnd() * 540 - 270, scale: 0.4, o: 0, duration: o.dur ?? 1.1,
            ease: 'power1.out', immediateRender: false }, t0);
      }
      return tl;
    };

    /* Le geste signature : un clone de la source VOLE vers la place de la cible */
    C.vole = (source, cible, t, o = {}) => {
      let s = un(source);
      const d = un(cible);
      if (!s || !d) return tl;
      const bs = boite(s), bd = boite(d);
      // html: '0,40' (texte) ou tex: '0{,}40' : le clone montre un autre contenu que la source (ex. « 40 % » → 0,40)
      if (o.html !== undefined || o.tex !== undefined) {
        const st0 = s.comp && s.comp.lignes[0] && s.comp.lignes[0].items.find(b => !b.esp && !b.f);
        const Pf = CV.formulesDe(s, E);
        const spec = o.tex !== undefined ? { tex: o.tex, taille: s.taille || (s.comp ? s.comp.taille * 1.1 : 60) }
          : { texte: String(o.html), nowrap: true, tab: true, taille: s.comp ? s.comp.taille : (s.taille || Pf.defaut) / 1.1, gras: st0 ? st0.a.st.gras : true,
            couleur: s.spec.couleur };
        const tmp = CV.creerNoeud(spec, s.parent, E);
        CV.mesurer(tmp, 4000, E); CV.disposer(tmp, E);
        CV.placer(tmp, bs.cx - tmp.lw * s.z / 2, bs.cy - tmp.lh * s.z / 2, s.z);
        tmp.invisible = true;   // nœud provisoire (enregistré dans E.noeuds) : seul son sprite vole, jamais peint en place
        const source0 = s;
        s = tmp;
        C.pulse(source0, tt(t), { scale: 1.22, dur: 0.35 });
        s.pulseFait = true;
      }
      const col = o.couleur ? couleur(o.couleur) : CV.couleurPrincipale(s, E);
      const lueur = 22 * s.z;
      let sp = null;
      const clone = item((ctx, E2, st) => {
        if (st.o <= 0.002) return;
        if (!sp) sp = CV.sprite(s, E, { cle: 'vol|' + (o.couleur || ''), sousArbre: true, couleur: o.couleur ? col : undefined, lueur, sur: 1.4 });
        ctx.save();
        transformer(ctx, st, bs.cx, bs.cy);
        ctx.shadowColor = 'transparent';
        ctx.drawImage(sp.c, sp.x0, sp.y0, sp.w, sp.h);
        ctx.restore();
      }, { o: 0 });
      void col;
      const t0 = tt(t), d0 = o.dur ?? 1.0;
      // échelle d'arrivée : le moteur HTML divise les hauteurs de boîte de texte, soit la zone de contenu de la police
      // (Atkinson ≈ 1,14 em ; boîte d'un morceau KaTeX ≈ 1,053 em du corps de la formule), et non les boîtes MathJax
      const hEm = n => (n.type === 'part' && n.formule.taille ? 1.053 * n.formule.taille
        : n.type === 'texte' && n.comp ? 1.14 * n.comp.taille : 0);
      const k = (hEm(d) && hEm(s) ? hEm(d) / hEm(s) : bd.h / bs.h) || 1;
      const dx = bd.cx - bs.cx, dy = bd.cy - bs.cy;
      const arc = o.arc ?? -Math.min(260, 90 + Math.hypot(dx, dy) * 0.25);
      noter(d, 0, 'entree');
      tl.set(d.s, { o: 0 }, 0);
      if (!s.pulseFait) C.pulse(s, t0, { scale: 1.22, dur: 0.35 });
      tl.set(clone.s, { o: 1 }, t0 + 0.12);
      tl.to(clone.s, { x: dx, duration: d0, ease: 'power2.inOut' }, t0 + 0.12);
      tl.to(clone.s, { keyframes: { y: [0, Math.min(0, dy) + arc, dy], easeEach: 'sine.inOut' },
        duration: d0, ease: 'none' }, t0 + 0.12);
      tl.to(clone.s, { keyframes: { scale: [1, 1.35, k], rotation: [0, o.rotation ?? 8, 0] },
        duration: d0, ease: 'none' }, t0 + 0.12);
      const arrivee = t0 + 0.12 + d0;
      tl.set(clone.s, { o: 0 }, arrivee);
      tl.set(d.s, { o: 1 }, arrivee);
      tl.fromTo(d.s, { scaleY: 0.7, scaleX: 1.2 }, { scaleY: 1, scaleX: 1, duration: 0.45,
        ease: 'elastic.out(1.2, 0.4)', immediateRender: false }, arrivee);
      if (o.onde !== false) C.onde(d, arrivee, { couleur: o.couleur ?? '--ambre' });
      return tl;
    };

    /* garde de `jusque` : une extinction qui précède (ou égale) l'allumage donnerait un halo jamais visible ou figé.
       Erreur visible (la planche refuse la capsule) plutôt qu'une correction silencieuse. */
    const jusqueValide = (geste, c, t0, jusque) => {
      const tj = tt(jusque);
      if (tj > t0 + 1e-6) return true;
      const nom = typeof c === 'string' ? c : (un(c) && un(c).id) || '';
      E.erreur(`${geste}${nom ? ' sur ' + nom : ''} : jusque ${JSON.stringify(jusque)} (${fr(tj, 2)} s) ne suit pas le début du geste (${fr(t0, 2)} s)`);
      return false;
    };

    /* Halo lumineux sur un ou plusieurs éléments (case, ligne, colonne) ; renvoie les halos */
    C.allume = (c, t, o = {}) => {
      const cibles = o.chacun ? tous(c).map(n => boite(n)) : [boite(c)];
      const col = couleur(o.couleur ?? '--ambre'), p = o.marge ?? 8;
      const halos = cibles.map(bb => {
        const r = { x: bb.x - p, y: bb.y - p, w: bb.w + 2 * p, h: bb.h + 2 * p };
        let sp = null;
        return item((ctx, E2, s) => {
          if (s.o <= 0.002) return;
          if (!sp) sp = CV.spriteHalo(r, col, E);
          ctx.save(); transformer(ctx, s, r.x + r.w / 2, r.y + r.h / 2);
          ctx.drawImage(sp.c, sp.x0, sp.y0, sp.w, sp.h); ctx.restore();
        }, { o: 0 });
      });
      const t0 = tt(t);
      tl.fromTo(halos.map(h => h.s), { o: 0, scale: 1.08 }, { o: 1, scale: 1, duration: o.dur ?? 0.45,
        ease: 'power2.out', immediateRender: false }, t0);
      if (o.jusque !== undefined && jusqueValide('allume', c, t0, o.jusque)) tl.to(halos.map(h => h.s), { o: 0, duration: 0.4 }, tt(o.jusque));
      return halos;
    };
    C.eteint = (halos, t) => tl.to(etats(halos), { o: 0, duration: 0.4 }, tt(t));

    /* Surligneur fluo derrière un texte */
    C.surligne = (c, t, o = {}) => {
      const col = CV.mix(couleur(o.couleur ?? '--ambre'), 0.45);
      tous(c).forEach(n => {
        const h = { s: { scaleX: 0 }, couleur: col };
        (n.surligneurs = n.surligneurs || []).push(h);
        tl.fromTo(h.s, { scaleX: 0 }, { scaleX: 1, duration: o.dur ?? 0.5, ease: 'power2.out', immediateRender: false }, tt(t));
      });
      return tl;
    };

    /* Tracé à la main dans le calque : entoure (ellipse), encadre (rectangle arrondi), fleche */
    function trait(d, t, o, tete, quoi) {
      const col = couleur(o.couleur ?? '--rose'), ep = o.epaisseur ?? 6;
      const L = E.prep.chemin(d).l || 1;
      const p2d = new Path2D(d), p2t = tete ? new Path2D(tete) : null;
      const st = { p: 0, tete: 0 };
      // Avant d'être tracé, un trait SVG à bout rond du moteur HTML laisse un point lumineux à son départ
      // (dasharray = dashoffset = longueur) : visible dès le début de la capsule jusqu'à l'extinction du tracé.
      // Parasite à l'écran : désactivé par défaut ; config pointsTraces: true pour le retrouver.
      const m0 = /^M\s*([-\d.]+)[\s,]+([-\d.]+)/.exec(d);
      const pointDepart = E.pointsTraces === true && m0 ? [+m0[1], +m0[2]] : null;
      const it = item((ctx, E2, s) => {
        if (s.o <= 0.002) return;
        if (st.p <= 0.001) {
          if (!pointDepart) return;
          ctx.save(); ctx.globalAlpha *= s.o;
          ctx.strokeStyle = col; ctx.lineWidth = ep; ctx.lineCap = 'round';
          ctx.shadowColor = col; ctx.shadowBlur = 10 * E.k;
          ctx.beginPath(); ctx.moveTo(pointDepart[0], pointDepart[1]); ctx.lineTo(pointDepart[0] + 0.01, pointDepart[1]); ctx.stroke();
          ctx.restore();
          return;
        }
        ctx.save(); ctx.globalAlpha *= s.o;
        ctx.strokeStyle = col; ctx.lineWidth = ep; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        ctx.shadowColor = col; ctx.shadowBlur = 10 * E.k;   // drop-shadow(0 0 10px currentColor)
        if (st.p < 0.999) ctx.setLineDash([L * st.p, L + 10]);
        ctx.stroke(p2d);
        if (p2t && st.tete > 0.002) { ctx.setLineDash([]); ctx.globalAlpha *= st.tete; ctx.stroke(p2t); }
        ctx.restore();
      });
      const t0 = tt(t);
      tl.fromTo(st, { p: 0 }, { p: 1, duration: o.dur ?? 0.7, ease: 'power2.inOut', immediateRender: false }, t0);
      if (tete) tl.to(st, { tete: 1, duration: 0.15 }, t0 + (o.dur ?? 0.7) - 0.1);
      if (o.jusque !== undefined && jusqueValide(quoi ? quoi[0] : 'tracé', quoi ? quoi[1] : null, t0, o.jusque)) tl.to(it.s, { o: 0, duration: 0.4 }, tt(o.jusque));
      return it;
    }
    C.entoure = (c, t, o = {}) => {
      const b = boite(c), m = o.marge ?? 18;
      const rx = b.w / 2 + m, ry = b.h / 2 + m * 0.8, cx = b.cx, cy = b.cy;
      const pts = [];
      for (let k = 0; k <= 64; k++) {
        const a = -2.2 + (k / 64) * (Math.PI * 2 + 0.5);
        const w = 1 + 0.035 * Math.sin(k * 0.9);
        pts.push((cx + Math.cos(a) * rx * w).toFixed(1) + ',' + (cy + Math.sin(a) * ry * w).toFixed(1));
      }
      return trait('M' + pts.join(' L'), t, o, null, ['entoure', c]);
    };
    C.encadre = (c, t, o = {}) => {
      const b = boite(c), m = o.marge ?? 14, r = 18;
      const x = +(b.x - m).toFixed(2), y = +(b.y - m).toFixed(2), w = +(b.w + 2 * m).toFixed(2), h = +(b.h + 2 * m).toFixed(2);
      const d = `M${x + r},${y} H${x + w - r} Q${x + w},${y} ${x + w},${y + r} V${y + h - r} Q${x + w},${y + h} ${x + w - r},${y + h} H${x + r} Q${x},${y + h} ${x},${y + h - r} V${y + r} Q${x},${y} ${x + r},${y + 2}`;
      return trait(d, t, Object.assign({ couleur: '--vert' }, o), null, ['encadre', c]);
    };
    C.fleche = (a, b, t, o = {}) => {
      const A = boite(a), B = boite(b);
      const bord = (P, Q) => {
        const dx = Q.cx - P.cx, dy = Q.cy - P.cy;
        const s = Math.min(Math.abs((P.w / 2 + 10) / (dx || 1e-6)), Math.abs((P.h / 2 + 10) / (dy || 1e-6)));
        return [P.cx + dx * s, P.cy + dy * s];
      };
      const f = v => v.toFixed(1);
      const [x1, y1] = bord(A, B), [x2, y2] = bord(B, A);
      const cb = o.courbure ?? 0.25;
      const mx = (x1 + x2) / 2 - (y2 - y1) * cb, my = (y1 + y2) / 2 + (x2 - x1) * cb;
      const ang = Math.atan2(y2 - my, x2 - mx), L2 = 26;
      const p1 = [x2 - L2 * Math.cos(ang - 0.45), y2 - L2 * Math.sin(ang - 0.45)];
      const p2 = [x2 - L2 * Math.cos(ang + 0.45), y2 - L2 * Math.sin(ang + 0.45)];
      return trait(`M${f(x1)},${f(y1)} Q${f(mx)},${f(my)} ${f(x2)},${f(y2)}`, t, Object.assign({ couleur: '--cyan' }, o),
        `M${f(p1[0])},${f(p1[1])} L${f(x2)},${f(y2)} L${f(p2[0])},${f(p2[1])}`, ['fleche', a]);
    };

    /* Pointeur lumineux (le « doigt » du professeur) */
    let pointeur = null, pointeurVisible = false;
    C.pointe = (c, t, o = {}) => {
      if (!pointeur) {
        let sp = null;
        pointeur = item((ctx, E2, s) => {
          if (s.o <= 0.002) return;
          if (!sp) sp = CV.spritePointeur(E);
          ctx.save(); ctx.globalAlpha *= s.o;
          ctx.translate(s.x, s.y); ctx.scale(s.scale, s.scale);
          ctx.drawImage(sp.c, sp.x0, sp.y0, sp.w, sp.h); ctx.restore();
        }, { o: 0, scale: 0.5 });
        pointeur.dessus = true;
      }
      const p = pointeur.s, t0 = tt(t);
      if (c === null) { tl.to(p, { o: 0, scale: 0.5, duration: 0.3 }, t0); pointeurVisible = false; return tl; }
      const b = boite(c);
      const x = b.x + b.w * (o.fx ?? 0.5), y = b.y + b.h * (o.fy ?? 0.5);
      if (!pointeurVisible) {
        tl.set(p, { x, y }, t0);
        tl.fromTo(p, { o: 0, scale: 0.3 }, { o: 1, scale: 1, duration: 0.35, ease: 'back.out(2)', immediateRender: false }, t0);
        pointeurVisible = true;
      } else tl.to(p, { x, y, duration: o.dur ?? 0.6, ease: 'power3.inOut' }, t0);
      return tl;
    };

    /* Mise au point : assombrit les éléments « focus » non ciblés (spec : focus: true ;
       à défaut, les éléments de premier niveau des zones de la scène) */
    const focusables = () => {
      const f = E.noeuds.filter(n => n.spec.focus || n.classes.includes('cv-focus'));
      return f.length ? f : E.premierNiveau || [];
    };
    C.focus = (c, t, o = {}) => {
      const garde = new Set(tous(c));
      const contient = (a, b) => { for (let p = b; p; p = p.parent) if (p === a) return true; return false; };
      const autres = focusables().filter(e => !garde.has(e) && ![...garde].some(g => contient(g, e) || contient(e, g)));
      tl.to(autres.map(n => n.s), { lum: 0.38, sat: 0.4, duration: o.dur ?? 0.5 }, tt(t));
      tl.to([...garde].map(n => n.s), { lum: 1, sat: 1, duration: o.dur ?? 0.5 }, tt(t));
      return tl;
    };
    C.defocus = (t, o = {}) => tl.to(focusables().map(n => n.s), { lum: 1, sat: 1, duration: o.dur ?? 0.5 }, tt(t));

    /* Zoom lent dans une image (« Ken Burns ») : zoom('#img', t, { a: 1.15, dur: 12, fx: 0.3, fy: 0.4 }) */
    C.zoom = (c, t, o = {}) => {
      const v = { kb: o.a ?? 1.15, duration: o.dur ?? 8, ease: o.ease ?? 'sine.inOut' };
      if (o.fx !== undefined) v.fx = o.fx;
      if (o.fy !== undefined) v.fy = o.fy;
      return tl.to(etats(c), v, tt(t));
    };

    /* =====================================================================
       Tuiles algébriques : deplace, retourne, annule, ajoutePaire
       (les gestes classiques montre, cache, tombe, allume, entoure, pulse, vole
       marchent sur une tuile ; ils se visent par id : 'a-1', 'p-l1c2', 'm-g-1'…)
       ===================================================================== */
    const tuilesDe = c => {
      const res = [];
      const voir = n => { if (n.type === 'tuile') res.push(n); else n.enfants.forEach(voir); };
      tous(c).forEach(voir);
      return res;
    };
    const decale = n => n.pf || { x: 0, y: 0 };                 // décalage programmé (deplace)
    const centreN = n => ({ x: n.b.x + n.b.w / 2 + decale(n).x, y: n.b.y + n.b.h / 2 + decale(n).y });
    const refTuile = ref => {                                   // centre et taille d'une cible
      const l = tous(ref);
      if (l.length === 1) { const c = centreN(l[0]); return { x: c.x, y: c.y, w: l[0].b.w, h: l[0].b.h }; }
      const b = boite(ref);
      return { x: b.cx, y: b.cy, w: b.w, h: b.h };
    };
    /* centre voulu pour le mobile m (taille mw × mh) face à la cible r, selon l'ancre */
    const placeAncre = (r, mw, mh, o) => {
      const g = o.ecart ?? 10, a = o.ancre || 'centre';
      let x = r.x, y = r.y;
      if (a === 'fin') x = r.x + r.w / 2 + g + mw / 2;
      else if (a === 'debut') x = r.x - r.w / 2 - g - mw / 2;
      else if (a === 'dessous') y = r.y + r.h / 2 + g + mh / 2;
      else if (a === 'dessus') y = r.y - r.h / 2 - g - mh / 2;
      else if (a === 'coin') { x = r.x - r.w / 2 + mw / 2; y = r.y - r.h / 2 + mh / 2; }
      return { x: x + (o.dx ?? 0), y: y + (o.dy ?? 0) };
    };
    /* retournement : la tuile se met de chant, change de polarité (couleur + étiquette) à mi-course, se rouvre */
    const retourneTuile = (n, t0, d, o = {}) => {
      if (!n.tu) return;
      const tu = n.tu;
      const vers = o.vers === 'positif' ? 0 : o.vers === 'negatif' ? 1 : (tu.suivant ? 0 : 1);
      tu.suivant = vers;
      tl.to(n.s, { scaleX: 0, duration: d / 2, ease: 'power2.in' }, t0);
      tl.set(tu, { neg: vers }, t0 + d / 2);
      tl.to(n.s, { scaleX: 1, duration: d / 2, ease: 'power2.out' }, t0 + d / 2);
      tl.to(n.s, { keyframes: { scale: [1, 1.12, 1], easeEach: 'sine.inOut' }, duration: d, ease: 'none' }, t0);
    };
    /* glisse n de son décalage actuel vers le centre voulu (soulevée au-dessus de la scène pendant le trajet) */
    const glisse = (n, vers, tk, d, o = {}) => {
      const de = decale(n), c0 = centreN(n);
      const to = { x: de.x + vers.x - c0.x, y: de.y + vers.y - c0.y };
      n.pf = to;
      tl.set(n.s, { lev: 1 }, tk);
      tl.fromTo(n.s, { x: de.x }, { x: to.x, duration: d, ease: o.ease ?? 'power2.inOut', immediateRender: false }, tk);
      if (o.arc) tl.fromTo(n.s, { y: de.y }, { keyframes: { y: [de.y, Math.min(de.y, to.y) - o.arc, to.y], easeEach: 'sine.inOut' }, duration: d, ease: 'none', immediateRender: false }, tk);
      else tl.fromTo(n.s, { y: de.y }, { y: to.y, duration: d, ease: o.ease ?? 'power2.inOut', immediateRender: false }, tk);
      if (o.retourne) retourneTuile(n, tk, d, o);
      else if (o.rebond !== false) tl.fromTo(n.s, { scaleX: 1.07, scaleY: 0.93 }, { scaleX: 1, scaleY: 1, duration: 0.4, ease: 'elastic.out(1.2, 0.45)', immediateRender: false }, tk + d);
      if (o.garde !== true) tl.set(n.s, { lev: 0 }, tk + d + 0.01);
    };

    C.deplace = (c, cible, t, o = {}) => {
      const t0 = tt(t), d = o.dur ?? 0.8;
      const decalage = cible && typeof cible === 'object' && !Array.isArray(cible) && !(cible instanceof CV.Noeud) && (cible.dx !== undefined || cible.dy !== undefined);
      tous(c).forEach((n, k) => {
        const tk = t0 + k * (o.stagger ?? 0), c0 = centreN(n);
        const vers = decalage ? { x: c0.x + (cible.dx ?? 0), y: c0.y + (cible.dy ?? 0) }
          : placeAncre(refTuile(Array.isArray(cible) ? cible[k] : cible), n.b.w, n.b.h, o);
        glisse(n, vers, tk, d, o);
      });
      return tl;
    };

    C.retourne = (c, t, o = {}) => {
      const t0 = tt(t);
      tuilesDe(c).forEach((n, k) => {
        retourneTuile(n, t0 + k * (o.stagger ?? 0), o.dur ?? 0.7, o);
        if (o.onde) C.onde({ cx: centreN(n).x, cy: centreN(n).y, w: n.b.w, h: n.b.h }, t0 + k * (o.stagger ?? 0) + (o.dur ?? 0.7), { couleur: o.couleur ?? '--violet' });
      });
      return tl;
    };

    /* pastille « 0 » (ou autre texte) qui apparaît puis s'efface */
    const etiquetteZero = (x, y, taille, t0, texte, tenue) => {
      const it = item((ctx, E2, s) => {
        if (s.o <= 0.002) return;
        ctx.save(); ctx.globalAlpha *= s.o; ctx.translate(x, y); ctx.scale(s.scale, s.scale);
        ctx.beginPath(); ctx.arc(0, 0, taille * 0.62, 0, Math.PI * 2);
        ctx.fillStyle = CV.mix(theme.texte, 0.1, theme.fond1); ctx.fill();
        ctx.lineWidth = 4; ctx.strokeStyle = theme.violet; ctx.stroke();
        if (texte === '0') {   // zéro sans barre (design.md) : un ovale
          ctx.beginPath(); ctx.ellipse(0, 0, taille * 0.17, taille * 0.27, 0, 0, Math.PI * 2);
          ctx.lineWidth = taille * 0.1; ctx.strokeStyle = theme.texte; ctx.stroke();
        } else {
          ctx.font = CV.police(taille * 0.8, { gras: true }); ctx.fillStyle = theme.texte;
          ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText(texte, 0, taille * 0.04);
        }
        ctx.restore();
      }, { o: 0 });
      tl.fromTo(it.s, { o: 0, scale: 0.4 }, { o: 1, scale: 1, duration: 0.4, ease: 'back.out(2.2)', immediateRender: false }, t0);
      tl.to(it.s, { o: 0, scale: 0.9, duration: 0.35, ease: 'power1.in' }, t0 + tenue);
    };

    /* paire nulle : b glisse sur a, éclat, les deux s'effacent ensemble ; zero: true affiche « 0 » à leur place */
    C.annule = (a, b, t, o = {}) => {
      const A = tuilesDe(a), B = tuilesDe(b);
      if (A.length !== B.length) { E.erreur('annule : ' + A.length + ' tuile(s) contre ' + B.length); return tl; }
      const t0 = tt(t), d = o.dur ?? 0.7, col = o.couleur ?? '--violet';
      A.forEach((na, k) => {
        const nb = B[k], tk = t0 + k * (o.stagger ?? 0.45);
        const ca = centreN(na), tc = tk + d, tf = tc + 0.18;
        glisse(nb, ca, tk, d, { rebond: false, garde: true, ease: 'power2.in', arc: o.arc });
        [na, nb].forEach(n => tl.fromTo(n.tu, { flash: 0 }, { keyframes: { flash: [0, 1, 0], easeEach: 'sine.inOut' }, duration: 0.45, ease: 'none', immediateRender: false }, tc));
        C.onde({ cx: ca.x, cy: ca.y, w: na.b.w, h: na.b.h }, tc, { couleur: col, taille: 0.95 });
        if (o.etincelles !== false) C.eclat({ cx: ca.x, cy: ca.y, w: na.b.w, h: na.b.h }, tc, { n: 9, force: 110, dur: 0.7, couleurs: [col, '--ambre', '--rose'], graine: 7 + k });
        noter([na, nb], tf, 'sortie');
        tl.to([na.s, nb.s], { o: 0, scale: 0.55, duration: 0.35, ease: 'power2.in' }, tf);
        tl.set(nb.s, { lev: 0 }, tf + 0.36);
        if (o.zero) etiquetteZero(ca.x, ca.y, Math.min(na.b.w, na.b.h) * 1.1 + 20, tf + 0.1, o.zero === true ? '0' : String(o.zero), o.tenue ?? 1.0);
      });
      return tl;
    };

    /* apparition d'une paire nulle (+1 et −1 déclarés dans la spec) ; vers: cible → les tuiles viennent se ranger à sa suite */
    C.ajoutePaire = (cible, t, o = {}) => {
      const T = tuilesDe(cible), t0 = tt(t);
      noter(T, t0, 'entree');
      T.forEach((n, k) => {
        tl.fromTo(n.s, { o: 0, scale: 0.3, y: -50 }, { o: 1, scale: 1, y: 0, duration: 0.6, ease: 'back.out(2.2)', immediateRender: false }, t0 + k * (o.stagger ?? 0.15));
        C.onde({ cx: centreN(n).x, cy: centreN(n).y, w: n.b.w, h: n.b.h }, t0 + 0.35 + k * (o.stagger ?? 0.15), { couleur: o.couleur ?? '--violet' });
      });
      if (o.zero && T.length) {
        const bb = boite(T);
        etiquetteZero(bb.cx, bb.y - 46, 64, t0 + 0.5, o.zero === true ? '0' : String(o.zero), o.tenue ?? 1.4);
      }
      if (o.vers) {
        const tv = t0 + (o.pause ?? 1.2);
        T.forEach((n, k) => {
          const ref = k === 0 ? o.vers : T[k - 1];
          const c0 = centreN(n);
          glisse(n, placeAncre(refTuile(ref), n.b.w, n.b.h, { ancre: o.ancre ?? 'fin', ecart: o.ecart ?? 8 }), tv + k * 0.15, o.dur ?? 0.7, {});
          void c0;
        });
      }
      return tl;
    };

    /* Accès libre */
    C.a = t => tt(t);
    C.surSeek = f => hooks.push(f);
    C.changement = () => {};

    C._journal = journal;
    return C;
  };

  /* couleur dominante d'un nœud (lueur du clone de `vole`) */
  CV.couleurPrincipale = (n, E) => {
    const f = n.type === 'part' ? n.formule.f : n.type === 'tex' ? n.f : null;
    if (f) {
      const op = f.ops.find(o => o.c && (n.type !== 'part' || o.ids.includes(n.id)));
      if (op) return op.c;
    }
    const c = n.spec && n.spec.couleur && !['carte', 'puce'].includes(n.type) ? n.spec.couleur : null;
    return c ? CV.couleur(E.theme, c) : E.theme.texte;
  };

  /* halo : bordure 4 px, fond 16 %, lueur externe 40 px à 60 %, lueur interne 26 px à 25 % (theme.css .cv-halo) */
  CV.spriteHalo = (r, col, E) => {
    const m = 70, k = E.k, x0 = r.x - m, y0 = r.y - m, w = r.w + 2 * m, h = r.h + 2 * m;
    const c = CV.toile(w * k, h * k), ctx = c.getContext('2d');
    ctx.setTransform(k, 0, 0, k, -x0 * k, -y0 * k);
    const rr = 20;
    const forme = new Path2D(); forme.roundRect(r.x, r.y, r.w, r.h, rr);
    // lueur externe (hors de la boîte seulement)
    ctx.save();
    const ext = new Path2D(); ext.rect(x0, y0, w, h); ext.addPath(forme);
    ctx.clip(ext, 'evenodd');
    ctx.shadowColor = CV.mix(col, 0.6); ctx.shadowBlur = 40 * k; ctx.fillStyle = '#000';
    ctx.shadowOffsetX = 10000 * k; ctx.translate(-10000, 0); ctx.fill(forme);
    ctx.restore();
    // fond
    ctx.fillStyle = CV.mix(col, 0.16); ctx.fill(forme);
    // lueur interne
    ctx.save(); ctx.clip(forme);
    const anneau = new Path2D(); anneau.rect(r.x - 200, r.y - 200, r.w + 400, r.h + 400); anneau.addPath(forme);
    ctx.shadowColor = CV.mix(col, 0.25); ctx.shadowBlur = 26 * k; ctx.fillStyle = '#000';
    ctx.shadowOffsetX = 10000 * k; ctx.translate(-10000, 0);
    ctx.fill(anneau, 'evenodd');
    ctx.restore();
    // bordure 4 px (intérieure)
    ctx.beginPath(); ctx.roundRect(r.x + 2, r.y + 2, r.w - 4, r.h - 4, rr - 2);
    ctx.lineWidth = 4; ctx.strokeStyle = col; ctx.stroke();
    return { c, x0, y0, w: c.width / k, h: c.height / k, k };
  };

  /* pointeur : radial-gradient(#fff 0 22 %, rose 40 %, transparent 72 %) + lueur 40 px étalée de 10 px */
  CV.spritePointeur = E => {
    const k = E.k, m = 80, w = 44 + 2 * m;
    const c = CV.toile(w * k, w * k), ctx = c.getContext('2d');
    ctx.setTransform(k, 0, 0, k, (w / 2) * k, (w / 2) * k);
    const rose = E.theme.rose;
    ctx.save();
    ctx.shadowColor = CV.mix(rose, 0.55); ctx.shadowBlur = 40 * k;
    ctx.shadowOffsetX = 10000 * k; ctx.translate(-10000, 0);
    ctx.beginPath(); ctx.arc(0, 0, 32, 0, Math.PI * 2); ctx.fillStyle = '#000'; ctx.fill();
    ctx.restore();
    const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 22 * Math.SQRT2);
    g.addColorStop(0, '#fff'); g.addColorStop(0.22, '#fff'); g.addColorStop(0.40, rose); g.addColorStop(0.72, CV.alpha(rose, 0));
    ctx.beginPath(); ctx.arc(0, 0, 22, 0, Math.PI * 2); ctx.fillStyle = g; ctx.fill();
    return { c, x0: -w / 2, y0: -w / 2, w, h: w, k };
  };
})(typeof self !== 'undefined' ? self : this);
