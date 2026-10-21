/* =====================================================================
   Page de rendu : préparation (MathJax, mise en page, table) puis
   répartition des images entre les workers (tranches contiguës, chacune
   commence par une image clé). Les workers dessinent, encodent en H.264
   (WebCodecs) et envoient les morceaux encodés au fil de l'eau à
   rendre_canvas.py (POST /flux). window.etat est lu par Python.
   ===================================================================== */
(async () => {
  const P = new URLSearchParams(location.search);
  const H = +(P.get('hauteur') || 540), W = Math.round(H * 16 / 9 / 2) * 2;
  const fps = +(P.get('fps') || 30), nbW = +(P.get('workers') || 2);
  const etat = (window.etat = { phase: 'préparation', faites: 0, total: 0, fini: false, erreurs: [], temps: {}, workers: [], rapport: [] });
  const t0 = performance.now();
  try {
    await MathJax.startup.promise;
    await CV.chargerPolices('vendor/fonts/');
    const tPolices = performance.now();
    const theme = CV.THEMES[(CV.spec && (CV.spec.theme || (CV.spec.config || {}).theme)) || 'nuit'] || CV.THEMES.nuit;
    const prep = new CV.PrepDOM(theme, CV.spec && CV.spec.macros);
    const images = await CV.chargerImages(CV.spec, '/');
    const m = new CV.Moteur({ spec: CV.spec, transcript: window.TRANSCRIPT, tempsForts: window.TEMPS_FORTS || [], prep, k: H / 1080, images });
    etat.rapport = m.rapport;
    etat.titre = m.config.titre; etat.audio = m.config.audio; etat.duree = m.duree;
    if (m.E.erreurs.length) { etat.erreurs = m.E.erreurs; etat.fini = true; return; }
    // mode « images fixes » (planche de contrôle) : PNG aux instants demandés, sans vidéo
    if (P.get('images')) {
      const ts = P.get('images').split(',').map(Number).sort((a, b) => a - b);
      const toile = new OffscreenCanvas(W, H), ctx = toile.getContext('2d', { alpha: false });
      let i = 0;
      for (const t of ts) {
        for (; i / fps < t; i++) m.seek(i / fps);   // pré-roulage image par image, comme un worker
        m.seek(t); m.dessiner(ctx, t);
        const png = await toile.convertToBlob({ type: 'image/png' });
        await fetch('/image?t=' + t, { method: 'POST', body: png });
        etat.faites++;
      }
      etat.fini = true;
      return;
    }
    const debut = +(P.get('debut') || 0), fin = Math.min(+(P.get('fin') || m.duree), m.duree);
    const N = Math.ceil((fin - debut) * fps);
    etat.total = N;
    etat.temps.prep_page = Math.round(performance.now() - t0);
    etat.temps.prep_mathjax_polices = Math.round(tPolices - t0);
    const table = prep.table;
    const taille = Math.ceil(N / nbW);
    etat.phase = 'rendu';
    const tRendu = performance.now();
    await Promise.all(Array.from({ length: nbW }, (_, i) => new Promise(res => {
      const i0 = i * taille, i1 = Math.min(N, i0 + taille);
      if (i0 >= i1) { res(); return; }
      const w = new Worker('travailleur.js');
      w.onmessage = e => {
        const d = e.data;
        if (d.type === 'progres') etat.faites += d.n;
        else if (d.type === 'fini') { etat.workers[i] = d; w.terminate(); res(); }
        else if (d.type === 'erreur') { etat.erreurs.push('worker ' + i + ' : ' + d.msg); w.terminate(); res(); }
      };
      w.onerror = e => { etat.erreurs.push('worker ' + i + ' : ' + e.message); res(); };
      w.postMessage({ tranche: i, i0, i1, debut, fps, W, H, k: H / 1080, table,
        transcript: window.TRANSCRIPT, tempsForts: window.TEMPS_FORTS || [],
        debit: +(P.get('debit') || 0), accel: P.get('accel') || 'prefer-hardware', gop: +(P.get('gop') || 10) * fps,
        // image clé juste après chaque changement de scène : l'image entière a changé, l'encodeur repart net
        clefs: (m.E.instantsScenes || []).map(t => Math.round((t - debut) * fps) + 1),
        codec: P.get('codec') || '' });
    })));
    etat.temps.rendu = Math.round(performance.now() - tRendu);
  } catch (e) {
    etat.erreurs.push(String(e && e.stack || e));
  }
  etat.fini = true;
})();
