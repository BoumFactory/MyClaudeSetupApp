/* =====================================================================
   Aperçu d'une capsule spec.js : canvas à l'écran, audio synchronisé,
   barre de lecture, relecture horodatée (commenter, « Copier pour Claude »).
   Repris de assets/gabarit/moteur/apercu.js. Ouvrir index.html tel quel
   (file://) : tout tourne dans la page, sans worker.
   Raccourcis : Espace lecture/pause · ←/→ ±2 s · ,/. image par image · C commenter
   ===================================================================== */
(() => {
  const BARRE = 132;
  const fmt = t => { const m = Math.floor(t / 60), s = t - 60 * m; return String(m).padStart(2, '0') + ':' + s.toFixed(1).padStart(4, '0'); };
  const cle = 'capsule-retours:' + location.pathname;
  const base = (document.currentScript && document.currentScript.src || '').replace(/apercu\.js.*$/, '');

  async function demarrer() {
    const T = window.TRANSCRIPT || { mots: [], segments: [], duree: 10 };
    const toile = document.getElementById('cv-toile');
    const ctx = toile.getContext('2d', { alpha: false });
    const bandeau = document.getElementById('cv-erreurs');
    const montrerErreurs = l => { if (l.length) { bandeau.hidden = false; bandeau.textContent = l.join('\n'); } };
    await MathJax.startup.promise;
    try { await CV.chargerPolices(base + 'vendor/fonts/'); } catch (e) { montrerErreurs(['Polices : ' + e]); }
    const theme = CV.THEMES[(CV.spec.theme || (CV.spec.config || {}).theme) || 'nuit'] || CV.THEMES.nuit;
    const prep = new CV.PrepDOM(theme, CV.spec.macros);
    const images = await CV.chargerImages(CV.spec, '');
    let m = null, k = 0, audio = null;
    let enLecture = false, tFixe = 0;
    const temps = () => (enLecture && audio ? audio.currentTime : tFixe);

    // le moteur est reconstruit à la résolution de l'écran (les sprites sont peints à cette résolution)
    function construire() {
      const kk = Math.min(innerWidth / 1920, (innerHeight - BARRE) / 1080) * (devicePixelRatio || 1);
      if (m && Math.abs(kk - k) < 0.01) return;
      k = kk;
      toile.width = Math.round(1920 * k); toile.height = Math.round(1080 * k);
      toile.style.width = (toile.width / (devicePixelRatio || 1)) + 'px';
      toile.style.height = (toile.height / (devicePixelRatio || 1)) + 'px';
      m = new CV.Moteur({ spec: CV.spec, transcript: T, tempsForts: window.TEMPS_FORTS || [], prep, k, images });
      // pré-roulage jusqu'à l'instant courant (mêmes valeurs qu'en lecture continue)
      for (let t = 0; t < tFixe; t += 1 / 30) m.seek(t);
      montrerErreurs(m.E.erreurs);
      if (m.rapport.length) console.info('[capsule] mise en page :\n' + m.rapport.join('\n'));
      dessiner(temps());
    }
    function dessiner(t) { m.seek(t); m.dessiner(ctx, t); }

    const ui = document.getElementById('cv-ui');
    ui.innerHTML = `
      <style>
        #cv-ui{position:fixed;left:0;right:0;bottom:0;height:${BARRE}px;background:#10142a;color:#e6e9f5;
          font:15px/1.35 "Segoe UI",system-ui,sans-serif;display:grid;grid-template-columns:auto 1fr 340px;gap:14px;
          padding:10px 16px;box-sizing:border-box;border-top:1px solid #2a3060;z-index:900}
        #cv-ui button{background:#252b55;color:#fff;border:1px solid #3b4380;border-radius:8px;padding:6px 12px;cursor:pointer;font:inherit}
        #cv-ui button:hover{background:#323a72}
        #cv-ui .gauche{display:flex;flex-direction:column;gap:8px;justify-content:center}
        #cv-ui .milieu{display:flex;flex-direction:column;gap:6px;justify-content:center;min-width:0}
        #cv-ui input[type=range]{width:100%}
        #cv-ui .phrase{color:#9fb0e8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
        #cv-ui .retours{overflow:auto;font-size:13px;border-left:1px solid #2a3060;padding-left:10px}
        #cv-ui .retours div{cursor:pointer;padding:2px 0} #cv-ui .retours div:hover{color:#fbbf24}
        #cv-saisie{display:none;gap:6px} #cv-saisie input{flex:1;background:#0b0e20;color:#fff;border:1px solid #3b4380;border-radius:6px;padding:6px}
      </style>
      <div class="gauche">
        <div><button id="cv-lecture">▶ Lecture</button> <span id="cv-temps">00:00.0</span></div>
        <div><button id="cv-commenter">💬 Commenter (C)</button>
          <select id="cv-vitesse"><option>0.75</option><option selected>1</option><option>1.25</option><option>1.5</option></select></div>
      </div>
      <div class="milieu">
        <input type="range" id="cv-curseur" min="0" max="1" step="0.01" value="0">
        <div class="phrase" id="cv-phrase"></div>
        <div id="cv-saisie"><input id="cv-texte" placeholder="Ce qui ne va pas à cet instant… (Entrée pour valider, Échap pour annuler)"><button id="cv-ok">OK</button></div>
      </div>
      <div class="retours"><b>Retours</b> <button id="cv-copier">Copier pour Claude</button> <button id="cv-vider">Vider</button><div id="cv-liste"></div></div>`;
    const $ = id => document.getElementById(id);
    construire();
    $('cv-curseur').max = m.duree;
    audio = new Audio(m.config.audio);
    let retours = [];
    try { retours = JSON.parse(localStorage.getItem(cle) || '[]'); } catch (e) { retours = []; }

    const motA = t => { let i = -1; T.mots.forEach((x, j) => { if (x.debut <= t) i = j; }); return i; };
    const phraseA = t => (T.segments.find(s => t >= s.debut - 0.05 && t <= s.fin + 0.4) || {}).texte || '';

    function aller(t) {
      const avant = tFixe;
      tFixe = Math.max(0, Math.min(m.duree, t));
      audio.currentTime = Math.min(tFixe, audio.duration || tFixe);
      // en avançant, on passe par chaque image (valeurs de départ des tweens identiques au rendu)
      if (tFixe > avant && tFixe - avant < 20) for (let x = avant; x < tFixe; x += 1 / 30) m.seek(x);
      dessiner(tFixe); maj(tFixe);
    }
    function maj(t) {
      $('cv-temps').textContent = fmt(t) + ' / ' + fmt(m.duree);
      $('cv-curseur').value = t;
      const i = motA(t);
      $('cv-phrase').textContent = (i >= 0 ? '#' + i + ' « ' + T.mots[i].mot + ' » — ' : '') + phraseA(t);
    }
    function boucle() {
      if (enLecture) {
        const t = audio.currentTime;
        dessiner(t); maj(t);
        if (audio.ended || t >= m.duree) basculer();
      }
      requestAnimationFrame(boucle);
    }
    function basculer() {
      enLecture = !enLecture;
      if (enLecture) { audio.currentTime = tFixe; audio.play(); } else { tFixe = audio.currentTime; audio.pause(); }
      $('cv-lecture').textContent = enLecture ? '⏸ Pause' : '▶ Lecture';
    }
    function afficherRetours() {
      $('cv-liste').innerHTML = retours.map((r, i) => `<div data-i="${i}">[${fmt(r.t)}] ${r.texte.replace(/</g, '&lt;')}</div>`).join('');
      $('cv-liste').querySelectorAll('div').forEach(d => { d.onclick = () => aller(retours[+d.dataset.i].t); });
      try { localStorage.setItem(cle, JSON.stringify(retours)); } catch (e) { /* stockage indisponible */ }
    }
    function ouvrirSaisie() {
      if (enLecture) basculer();
      $('cv-saisie').style.display = 'flex'; $('cv-texte').value = ''; $('cv-texte').focus();
    }
    function valider() {
      const x = $('cv-texte').value.trim();
      if (x) {
        const t = temps(), i = motA(t);
        retours.push({ t, mot: i, phrase: phraseA(t), texte: x });
        retours.sort((a, b) => a.t - b.t); afficherRetours();
      }
      $('cv-saisie').style.display = 'none';
    }
    $('cv-lecture').onclick = basculer;
    $('cv-commenter').onclick = ouvrirSaisie;
    $('cv-ok').onclick = valider;
    $('cv-vitesse').onchange = e => { audio.playbackRate = +e.target.value; };
    $('cv-curseur').oninput = e => aller(+e.target.value);
    $('cv-vider').onclick = () => { retours = []; afficherRetours(); };
    $('cv-copier').onclick = () => {
      const txt = 'Retours de relecture — ' + m.config.titre + '\n' + retours.map(r =>
        `[${fmt(r.t)}] (mot #${r.mot}, « ${r.phrase} ») → ${r.texte}`).join('\n');
      navigator.clipboard.writeText(txt).then(() => { $('cv-copier').textContent = 'Copié ✓'; setTimeout(() => { $('cv-copier').textContent = 'Copier pour Claude'; }, 1500); });
    };
    $('cv-texte').onkeydown = e => { if (e.key === 'Enter') valider(); if (e.key === 'Escape') $('cv-saisie').style.display = 'none'; e.stopPropagation(); };
    addEventListener('keydown', e => {
      if (e.target.tagName === 'INPUT' && e.target.type !== 'range') return;
      if (e.code === 'Space') { e.preventDefault(); basculer(); }
      else if (e.key === 'ArrowRight') aller(temps() + 2);
      else if (e.key === 'ArrowLeft') aller(temps() - 2);
      else if (e.key === '.') aller(temps() + 1 / 30);
      else if (e.key === ',') aller(temps() - 1 / 30);
      else if (e.key === 'c' || e.key === 'C') ouvrirSaisie();
    });
    let minuterie = null;
    addEventListener('resize', () => { clearTimeout(minuterie); minuterie = setTimeout(construire, 250); });
    afficherRetours(); maj(0); boucle();
    const h = new URLSearchParams(location.search).get('t');
    if (h) aller(parseFloat(h));
    window.capsuleApercu = { aller, moteur: () => m };
    document.dispatchEvent(new Event('capsule-prete'));
  }
  addEventListener('load', () => demarrer().catch(e => {
    const b = document.getElementById('cv-erreurs'); b.hidden = false; b.textContent = String(e && e.stack || e);
  }));
})();
