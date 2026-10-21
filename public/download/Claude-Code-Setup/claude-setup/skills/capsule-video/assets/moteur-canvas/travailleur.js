/* =====================================================================
   Worker de rendu : reconstruit la capsule à partir de la spec et de la
   table de préparation, dessine sa tranche d'images sur un OffscreenCanvas,
   encode en H.264 (VideoEncoder, matériel de préférence, repli logiciel)
   et envoie les morceaux encodés au fil de l'eau (POST /flux).
   ===================================================================== */
importScripts('vendor/gsap.min.js', 'ancres.js', 'theme.js', 'prep.js', 'texte.js', 'elements.js', 'composants.js', 'figure.js',
  'dessin.js', 'gestes.js', 'moteur.js');

onmessage = async e => {
  try { await rendre(e.data); } catch (err) { postMessage({ type: 'erreur', msg: String(err && err.stack || err) }); }
};

async function rendre(P) {
  const tA = performance.now();
  importScripts('/spec.js');
  await CV.chargerPolices('vendor/fonts/');
  const erreurs = [];
  const prep = new CV.PrepTable(P.table, m => erreurs.push(m));
  const images = await CV.chargerImages(CV.spec, '/');
  const m = new CV.Moteur({ spec: CV.spec, transcript: P.transcript, tempsForts: P.tempsForts, prep, k: P.k, images });
  if (m.E.erreurs.length || erreurs.length) throw new Error(m.E.erreurs.concat(erreurs).join('\n'));
  // pré-roulage image par image jusqu'au début de la tranche : mêmes valeurs de départ des tweens
  // qu'une lecture continue (aucune différence visible à la jonction des tranches)
  for (let i = 0; i < P.i0; i++) m.seek(P.debut + i / P.fps);
  const tPrep = performance.now() - tA;

  const toile = new OffscreenCanvas(P.W, P.H);
  const ctx = toile.getContext('2d', { alpha: false });
  // débit par défaut : ≈ 0,3 bit par pixel et par seconde à 30 i/s (540p ≈ 160 kb/s)
  const debit = P.debit || Math.round(P.W * P.H * 0.31);
  let config = null, accel = P.accel;
  for (const a of [P.accel, P.accel === 'prefer-hardware' ? 'prefer-software' : 'prefer-hardware']) {
    for (const codec of P.codec ? [P.codec] : ['avc1.640028', 'avc1.4d0028', 'avc1.42e01f']) {
      const c = { codec, width: P.W, height: P.H, bitrate: debit, framerate: P.fps, hardwareAcceleration: a,
        avc: { format: 'annexb' }, latencyMode: 'quality', bitrateMode: 'variable' };
      const s = await VideoEncoder.isConfigSupported(c).catch(() => ({ supported: false }));
      if (s.supported) { config = c; accel = a; break; }
    }
    if (config) break;
  }
  if (!config) throw new Error('Aucune configuration H.264 acceptée par VideoEncoder');

  let morceaux = [], octets = 0, envoi = Promise.resolve(), nEnvois = 0, erreurEnc = null;
  const vider = () => {
    if (!morceaux.length) return;
    const corps = new Blob(morceaux);
    morceaux = [];
    const n = nEnvois++;
    envoi = envoi.then(() => fetch(`/flux?tranche=${P.tranche}&n=${n}`, { method: 'POST', body: corps }))
      .then(r => { if (!r.ok) throw new Error('POST /flux : ' + r.status); });
  };
  const enc = new VideoEncoder({
    output: chunk => {
      const b = new Uint8Array(chunk.byteLength);
      chunk.copyTo(b);
      morceaux.push(b); octets += b.length;
      if (morceaux.length >= 90) vider();
    },
    error: err => { erreurEnc = err; },
  });
  enc.configure(config);

  let tDessin = 0, tImage = 0, tAttente = 0;
  const clefs = new Set(P.clefs || []);
  const dt = Math.round(1e6 / P.fps);
  let rapporte = 0;
  for (let i = P.i0; i < P.i1; i++) {
    const t = P.debut + i / P.fps;
    const a = performance.now();
    m.seek(t);
    m.dessiner(ctx, t);
    const b = performance.now(); tDessin += b - a;
    const image = new VideoFrame(toile, { timestamp: (i - P.i0) * dt, duration: dt });
    enc.encode(image, { keyFrame: i === P.i0 || (i - P.i0) % P.gop === 0 || clefs.has(i) });
    image.close();
    const c = performance.now(); tImage += c - b;
    while (enc.encodeQueueSize > 6) await new Promise(r => enc.addEventListener('dequeue', r, { once: true }));
    tAttente += performance.now() - c;
    if (erreurEnc) throw erreurEnc;
    const faites = i + 1 - P.i0;
    if (faites - rapporte >= 15) { postMessage({ type: 'progres', n: faites - rapporte }); rapporte = faites; }
  }
  const tF = performance.now();
  await enc.flush();
  enc.close();
  vider();
  await envoi;
  postMessage({ type: 'progres', n: P.i1 - P.i0 - rapporte });
  postMessage({ type: 'fini', images: P.i1 - P.i0, octets, accel, codec: config.codec, debit,
    t_prep: Math.round(tPrep), t_dessin: Math.round(tDessin), t_image: Math.round(tImage),
    t_attente_encodeur: Math.round(tAttente), t_vidage: Math.round(performance.now() - tF) });
}
