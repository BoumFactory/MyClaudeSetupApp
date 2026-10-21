"""Musique de fond générée localement (synthèse procédurale, aucun échantillon externe) et mixage sous la voix.

Usage :
    python musique.py <dossier_capsule> [--bpm 104] [--niveau -21] [--graine 3] [--sans-mix]

Entrées : <dossier>/audio.wav (voix), <dossier>/data/temps-forts.json (facultatif).
Sorties : <dossier>/musique.wav (musique seule, 44,1 kHz stéréo)
          <dossier>/audio-mix.wav (voix + musique, MÊME minutage que audio.wav)
Puis mettre `audio: 'audio-mix.wav'` dans spec.js (aperçu et rendu l'utilisent).

Ce que fait la musique :
  - suite d'accords la mineur → fa → do → sol (vi-IV-I-V), tonique et motivante ;
  - nappe filtrée, arpège pincé (croches, puis doubles croches pour relancer), basse douce,
    grosse caisse et charleston discrets ; intro et outro sans batterie, avec un motif de cloche ;
  - « respiration » : la musique remonte dans les silences et s'efface sous la voix (ducking) ;
  - compte à rebours : chaque silence de 4 s ou plus (défi « à toi de jouer ») coupe la batterie
    et place un tic par seconde.
Tout est déterministe (graine), donc deux exécutions donnent le même fichier.
"""
import argparse
import json
import pathlib
import sys
import wave
from fractions import Fraction

import numpy as np
from scipy.signal import butter, resample_poly, sawtooth, sosfilt

SR = 44100
ACCORDS = [  # (basse, nappe, arpège) en numéros MIDI
    (45, [57, 60, 64], [69, 72, 76, 81]),   # la mineur
    (41, [53, 57, 60], [65, 69, 72, 77]),   # fa
    (48, [55, 60, 64], [67, 72, 76, 79]),   # do
    (43, [55, 59, 62], [67, 71, 74, 79]),   # sol
]
ACCORDS_B = [ACCORDS[2], ACCORDS[3], ACCORDS[0], ACCORDS[1]]  # do sol la fa : variation de la seconde moitié


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def filtre(x, f, type_="low", ordre=2):
    return sosfilt(butter(ordre, f, btype=type_, fs=SR, output="sos"), x)


def enveloppe(n, att, rel):
    e = np.ones(n)
    a, r = int(att * SR), int(rel * SR)
    if a:
        e[:a] = np.linspace(0, 1, a)
    if r:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def pose(piste, debut, son, gain=1.0, pan=0.0):
    i = int(debut * SR)
    if i >= piste.shape[1]:
        return
    son = son[: piste.shape[1] - i]
    g = gain * np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)]) * np.sqrt(2)
    piste[:, i:i + len(son)] += g[:, None] * son


def pince(f, dur=0.55):
    t = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * k * f * t) / k ** 1.6 * np.exp(-t * (4 + 2.2 * k)) for k in range(1, 7))
    return s * enveloppe(len(t), 0.004, 0.05)


def cloche(f, dur=1.6):
    t = np.arange(int(dur * SR)) / SR
    s = np.sin(2 * np.pi * f * t + 1.2 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 3))
    return s * np.exp(-t * 2.2) * enveloppe(len(t), 0.003, 0.1)


def grosse_caisse():
    t = np.arange(int(0.32 * SR)) / SR
    f = 46 + 75 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)


def charleston(rng, dur=0.05):
    n = int(dur * SR)
    return filtre(rng.standard_normal(n), 7000, "high") * np.exp(-np.arange(n) / SR * 70)


def tic():
    t = np.arange(int(0.09 * SR)) / SR
    return (np.sin(2 * np.pi * 1760 * t) + 0.5 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t * 60)


def nappe(notes, dur):
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t)
    for m in notes:
        for d in (-0.0018, 0.0018):
            s += sawtooth(2 * np.pi * hz(m) * (1 + d) * t, 0.5)  # triangle : doux
    return s * enveloppe(len(t), 0.45, 0.6)


def lire_voix(chemin):
    with wave.open(str(chemin), "rb") as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        r = Fraction(SR, sr)
        x = resample_poly(x, r.numerator, r.denominator)
    return x


def silences_longs(d, seuil=4.0):
    f = d / "data" / "temps-forts.json"
    if not f.exists():
        return []
    tf = json.loads(f.read_text(encoding="utf-8"))
    zones = []
    for a, b in zip(tf, tf[1:] + [None]):
        fin_suivant = b["debut"] if b else None
        if fin_suivant and fin_suivant - a["fin"] >= seuil:
            zones.append((a["fin"], fin_suivant))
    return zones


def composer(duree, bpm, graine, comptes):
    rng = np.random.default_rng(graine)
    temps = 60 / bpm
    mesure = 4 * temps
    nb = int(np.ceil(duree / mesure)) + 1
    musique = {k: np.zeros((2, int((nb + 2) * mesure * SR))) for k in ("nappe", "arp", "basse", "batt", "deco")}

    def dans_compte(t):
        return any(a - 0.3 <= t <= b for a, b in comptes)

    for m in range(nb):
        t0 = m * mesure
        prog = ACCORDS if t0 < duree / 2 else ACCORDS_B
        basse, notes, arp = prog[m % 4]
        intro, outro = m < 4, t0 > duree - 4 * mesure
        section = (m - 4) % 16
        drop = (m - 4) % 32 in (30, 31)
        pose(musique["nappe"], t0, nappe(notes, mesure + 0.6), 0.10)
        # arpège : croches, doubles croches dans la 2e moitié de chaque section de 16 mesures
        pas = temps / 2 if (intro or outro or section < 8) else temps / 4
        motifs = [[0, 1, 2, 1], [0, 2, 1, 3], [1, 2, 3, 2], [0, 1, 3, 2]]
        motif = motifs[(m // 8) % 4]
        for k in range(int(round(mesure / pas))):
            t = t0 + k * pas
            accent = 1.0 if k % 4 == 0 else 0.7
            pose(musique["arp"], t, pince(hz(arp[motif[k % 4]])), 0.11 * accent, pan=0.35 * (1 if k % 2 else -1))
        # basse : temps 1, « et » du 2, temps 3
        for b, l in ((0, 1.2), (1.5, 0.45), (2, 1.0)):
            t = t0 + b * temps
            n = int(l * temps * SR)
            tt = np.arange(n) / SR
            s = np.sin(2 * np.pi * hz(basse) * tt) + 0.25 * np.sin(2 * np.pi * 2 * hz(basse) * tt)
            pose(musique["basse"], t, s * enveloppe(n, 0.01, 0.08), 0.20)
        # batterie
        if not (intro or outro or drop):
            for b in range(4):
                t = t0 + b * temps
                if not dans_compte(t):
                    pose(musique["batt"], t, grosse_caisse(), 0.30)
                    pose(musique["batt"], t + temps / 2, charleston(rng), 0.09, pan=0.3)
                    if pas < temps / 2:  # shaker léger en doubles croches quand l'arpège accélère
                        pose(musique["batt"], t + temps / 4, charleston(rng, 0.03), 0.035, pan=-0.3)
                        pose(musique["batt"], t + 3 * temps / 4, charleston(rng, 0.03), 0.035, pan=-0.3)
        if drop and (m - 4) % 32 == 30:  # montée de bruit filtré vers la section suivante
            n = int(2 * mesure * SR)
            sw = filtre(rng.standard_normal(n), 3000, "high") * np.linspace(0, 1, n) ** 2
            pose(musique["deco"], t0, sw, 0.035)
        if intro or outro:  # motif de cloche, quand la voix ne parle pas encore ou plus
            for k, i in enumerate([0, 2, 1, 3] if m % 2 == 0 else [2, 3, 1]):
                pose(musique["deco"], t0 + k * temps, cloche(hz(arp[i] + 12)), 0.06, pan=-0.2)
    for a, b in comptes:  # un tic par seconde du compte à rebours
        for k in range(int(b - a + 0.5)):
            pose(musique["deco"], a + k, tic(), 0.10)
    piste = sum(musique.values())
    piste = filtre(piste, 30, "high")
    n = int(duree * SR)
    piste = piste[:, :n]
    piste *= enveloppe(n, 1.5, 3.0)[None, :]
    return piste


def ducking(voix, n, plancher=0.42):
    """Gain de la musique : 1 dans les silences, `plancher` sous la voix (attaque 40 ms, relâche 600 ms)."""
    v = np.zeros(n)
    v[: min(n, len(voix))] = np.abs(voix[:n])
    fen = int(0.03 * SR)
    rms = np.sqrt(np.convolve(v ** 2, np.ones(fen) / fen, mode="same"))
    actif = (rms > 0.02).astype(float)
    g = np.empty(n)
    att, rel = np.exp(-1 / (0.04 * SR)), np.exp(-1 / (0.6 * SR))
    y = 0.0
    for i in range(0, n, 64):  # par blocs de 64 échantillons : assez fin, beaucoup plus rapide
        cible = actif[i]
        c = att if cible > y else rel
        y = cible + (y - cible) * c ** 64
        g[i:i + 64] = y
    return 1 - (1 - plancher) * g


def ecrire(chemin, st):
    st = np.clip(st, -1, 1)
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st.T * 32767).astype(np.int16).tobytes())


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("dossier")
    ap.add_argument("--bpm", type=float, default=104)
    ap.add_argument("--niveau", type=float, default=-21, help="dB de la musique sous la voix, quand la voix parle")
    ap.add_argument("--graine", type=int, default=3)
    ap.add_argument("--marge", type=float, default=1.2, help="secondes ajoutées après la voix (config.marge)")
    ap.add_argument("--sans-mix", action="store_true")
    a = ap.parse_args()

    d = pathlib.Path(a.dossier)
    voix = lire_voix(d / "audio.wav")
    duree = len(voix) / SR + a.marge
    n = int(duree * SR)
    comptes = silences_longs(d)
    musique = composer(duree, a.bpm, a.graine, comptes)

    # niveau : RMS de la musique (sous la voix) = RMS de la voix parlée + niveau dB
    parle = voix[np.abs(voix) > 0.02]
    rms_voix = np.sqrt(np.mean(parle ** 2)) if len(parle) else 0.1
    plancher = 0.42
    rms_mus = np.sqrt(np.mean(musique ** 2)) + 1e-9
    musique *= rms_voix * 10 ** (a.niveau / 20) / (rms_mus * plancher)
    ecrire(d / "musique.wav", musique / max(1.0, np.abs(musique).max() / 0.9))
    if a.sans_mix:
        print(f"OK musique.wav ({duree:.1f} s)")
        return
    g = ducking(voix, n, plancher)
    v = np.zeros(n)
    v[: len(voix)] = voix
    mix = musique * g[None, :] + v[None, :]
    pic = np.abs(mix).max()
    if pic > 0.97:
        mix *= 0.97 / pic
    ecrire(d / "audio-mix.wav", mix)
    print(f"OK musique.wav + audio-mix.wav : {duree:.1f} s, {len(comptes)} compte(s) à rebours, "
          f"musique {a.niveau:+.0f} dB sous la voix, remonte de {-20 * np.log10(plancher):.1f} dB dans les silences")


if __name__ == "__main__":
    main()
