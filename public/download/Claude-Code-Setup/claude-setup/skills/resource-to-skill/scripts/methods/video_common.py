# -*- coding: utf-8 -*-
"""Briques partagees par les methodes video (YouTube et fichier local).

Trois problemes a resoudre pour qu'une video devienne exploitable:

1. Le texte dit -> sous-titres si disponibles (gratuit, instantane), sinon
   transcription locale par whisper.
2. Ce qui est montre -> echantillonnage d'images. Une video technique porte
   souvent l'essentiel a l'ecran (code, schema, interface) et la bande son n'y
   fait que des allusions ("comme vous le voyez ici").
3. Le lien entre les deux -> chaque image porte son timecode, ce qui permet de
   la relier a la ligne de transcription correspondante.

Les images sont regroupees en planches contact: Claude lit 1 ou 2 images au lieu
de 24, decide ce qui merite un zoom, et ne charge les frames pleine resolution
que pour les moments reellement utiles.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

from base import ExtractionError, Workspace, has_module, pip_install, require, run

# Reglages d'echantillonnage par mode visuel.
VISUAL_MODES = {
    "off": {"max_frames": 0, "scene": None},
    "auto": {"max_frames": 24, "scene": 0.30},
    "deep": {"max_frames": 48, "scene": 0.18},
}

TILE_COLS = 4


# --------------------------------------------------------------------------
# Sous-titres
# --------------------------------------------------------------------------

def parse_vtt(vtt_text: str, block_seconds: int = 30) -> tuple[str, int]:
    """Transforme un WebVTT en transcription lisible, groupee par blocs horodates.

    Les sous-titres automatiques YouTube defilent mot a mot: chaque cue reprend
    la fin de la precedente. Sans deduplication on obtient un texte trois fois
    trop long et illisible. On ne garde donc que le texte reellement nouveau.
    """
    cues: list[tuple[float, str]] = []
    time_re = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[.,](\d{3})"
    )
    current_start = None
    buffer: list[str] = []

    def flush():
        if current_start is not None and buffer:
            line = " ".join(buffer).strip()
            if line:
                cues.append((current_start, line))

    for raw_line in vtt_text.splitlines():
        line = raw_line.strip()
        m = time_re.search(line)
        if m:
            flush()
            buffer = []
            h, mi, s, ms = (int(x) for x in m.groups()[:4])
            current_start = h * 3600 + mi * 60 + s + ms / 1000.0
            continue
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE")):
            continue
        clean = re.sub(r"<[^>]+>", "", line)
        clean = re.sub(r"&nbsp;?", " ", clean).strip()
        if clean:
            buffer.append(clean)
    flush()

    # Deduplication: on ne conserve que le suffixe nouveau de chaque cue.
    seen_words: list[str] = []
    timeline: list[tuple[float, str]] = []
    for start, text in cues:
        words = text.split()
        overlap = 0
        max_overlap = min(len(words), len(seen_words), 40)
        for k in range(max_overlap, 0, -1):
            if seen_words[-k:] == words[:k]:
                overlap = k
                break
        new_words = words[overlap:]
        if new_words:
            timeline.append((start, " ".join(new_words)))
            seen_words.extend(new_words)
            seen_words = seen_words[-60:]

    if not timeline:
        return "", 0

    lines: list[str] = []
    block_start = timeline[0][0]
    chunk: list[str] = []
    for start, text in timeline:
        if start - block_start >= block_seconds and chunk:
            lines.append(f"**[{fmt_time(block_start)}]** " + " ".join(chunk))
            block_start = start
            chunk = []
        chunk.append(text)
    if chunk:
        lines.append(f"**[{fmt_time(block_start)}]** " + " ".join(chunk))

    words_total = sum(len(t.split()) for _, t in timeline)
    return "\n\n".join(lines), words_total


def fmt_time(seconds: float) -> str:
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"


# --------------------------------------------------------------------------
# Transcription locale (secours quand aucun sous-titre n'existe)
# --------------------------------------------------------------------------

def transcribe_locally(media: Path, ws: Workspace, language: str | None = None) -> str:
    """Transcrit avec faster-whisper, en l'installant si besoin.

    Renvoie une transcription horodatee, ou "" si aucun moteur n'est disponible.
    L'echec n'est pas fatal: une video peut rester exploitable par ses images.
    """
    if not has_module("faster_whisper"):
        ws.warn("faster-whisper absent, tentative d'installation…")
        if not pip_install("faster-whisper"):
            ws.warn(
                "Installation de faster-whisper impossible (Python 32 bits ou reseau). "
                "Aucune transcription audio: l'extraction repose sur les images."
            )
            ws.suggest(
                "Si la bande son est indispensable, fournir un fichier .srt/.vtt "
                "a cote de la video, ou transcrire sur une machine Python 64 bits."
            )
            return ""

    try:
        from faster_whisper import WhisperModel  # type: ignore
    except Exception as exc:  # pragma: no cover - depend de l'environnement
        ws.warn(f"faster-whisper inutilisable: {exc}")
        return ""

    ws.suggest("Transcription generee par whisper: quelques termes techniques peuvent etre approximatifs.")
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _info = model.transcribe(str(media), language=language, vad_filter=True)

    lines, chunk, block_start = [], [], None
    for seg in segments:
        if block_start is None:
            block_start = seg.start
        if seg.start - block_start >= 30 and chunk:
            lines.append(f"**[{fmt_time(block_start)}]** " + " ".join(chunk))
            block_start, chunk = seg.start, []
        chunk.append(seg.text.strip())
    if chunk:
        lines.append(f"**[{fmt_time(block_start or 0)}]** " + " ".join(chunk))
    return "\n\n".join(lines)


# --------------------------------------------------------------------------
# Echantillonnage visuel
# --------------------------------------------------------------------------

def detect_scene_times(video: Path, threshold: float, scan_fps: int = 4) -> list[float]:
    """Releve les instants de changement d'ecran, sans ecrire d'image.

    On analyse une version reduite et sous-echantillonnee: le but est de reperer
    *quand* l'ecran change, pas d'obtenir une image de qualite. Separer la
    detection de l'extraction permet ensuite de choisir librement quels instants
    retenir — notamment de couvrir toute la duree au lieu de s'arreter des que le
    plafond d'images est atteint, ce qui laissait la fin des videos aveugle.
    """
    ffmpeg = require("ffmpeg", "Installer ffmpeg (winget install Gyan.FFmpeg) puis relancer.")
    proc = run(
        [
            ffmpeg, "-hide_banner", "-nostdin", "-i", str(video),
            "-vf", f"fps={scan_fps},scale=320:-2,select='gt(scene,{threshold})',showinfo",
            "-f", "null", "-",
        ],
        check=False,
        timeout=2400,
    )
    return sorted(float(t) for t in re.findall(r"pts_time:([0-9.]+)", proc.stderr or ""))


def grab_frame(video: Path, t: float, dest: Path, width: int = 1024) -> bool:
    ffmpeg = require("ffmpeg", "Installer ffmpeg puis relancer.")
    run(
        [
            ffmpeg, "-hide_banner", "-nostdin", "-y", "-ss", f"{max(t, 0):.2f}",
            "-i", str(video), "-frames:v", "1", "-vf", f"scale={width}:-2",
            "-q:v", "4", str(dest),
        ],
        check=False,
        timeout=300,
    )
    return dest.exists() and dest.stat().st_size > 2000


def frame_is_blank(path: Path, threshold: float = 11.0) -> bool:
    """Une image quasi uniforme n'apprend rien et coute autant a lire qu'une autre.

    Beaucoup de videos enchainent les plans par un fondu au noir: la detection de
    scene se declenche pile pendant le fondu et capture un ecran vide. On mesure
    donc la dispersion des niveaux de gris pour ecarter ces images.
    """
    if not has_module("PIL"):
        return False
    try:
        from PIL import Image, ImageStat  # type: ignore

        with Image.open(path) as im:
            small = im.convert("L")
            small.thumbnail((160, 160))
            return ImageStat.Stat(small).stddev[0] < threshold
    except Exception:
        return False


def sample_frames(video: Path, ws: Workspace, mode: str = "auto") -> list[dict]:
    """Extrait des images representatives et renvoie [{file, time, label}].

    Trois exigences, souvent en tension:
      - viser les moments ou l'ecran change vraiment plutot qu'un tic-tac regulier;
      - couvrir toute la duree, y compris la fin, meme quand les changements se
        concentrent au debut;
      - ne pas ramener d'ecrans vides.

    On decoupe donc la video en autant de tranches que d'images voulues, et dans
    chaque tranche on prend le changement de scene le plus central (a defaut, le
    milieu de la tranche), en decalant l'instant tant que l'image obtenue est
    uniforme.
    """
    cfg = VISUAL_MODES.get(mode, VISUAL_MODES["auto"])
    if cfg["max_frames"] == 0:
        return []

    duration = probe_duration(video)
    if duration <= 0:
        ws.warn("Duree de la video indeterminee: echantillonnage visuel impossible.")
        return []

    n = max(1, min(cfg["max_frames"], int(duration // 4) or 1))
    scenes = detect_scene_times(video, cfg["scene"])
    slice_len = duration / n

    targets: list[float] = []
    for i in range(n):
        lo, hi = i * slice_len, (i + 1) * slice_len
        center = (lo + hi) / 2
        in_slice = [t for t in scenes if lo <= t < hi]
        # +1 s apres le changement: le temps que l'ecran se stabilise (fin de
        # fondu, texte qui finit de s'afficher).
        pick = min(in_slice, key=lambda t: abs(t - center)) + 1.0 if in_slice else center
        targets.append(min(pick, duration - 0.5))

    out_dir = ws.assets_dir
    frames: list[dict] = []
    blanks = 0
    for i, t in enumerate(targets):
        name = f"frame-{i + 1:03d}.jpg"
        dest = out_dir / name
        chosen = None
        for offset in (0.0, 1.8, 3.5, -1.2):
            t_try = min(max(t + offset, 0.0), max(duration - 0.5, 0.0))
            if grab_frame(video, t_try, dest) and not frame_is_blank(dest):
                chosen = t_try
                break
        if chosen is None:
            if dest.exists():
                blanks += 1
                dest.unlink(missing_ok=True)
            continue
        frames.append({"file": name, "time": chosen, "label": f"t = {fmt_time(chosen)}"})

    if blanks:
        ws.warn(
            f"{blanks} image(s) ecartee(s) car uniformes (fondu, ecran noir). "
            "La couverture visuelle est plus clairsemee que prevu."
        )
    if not frames:
        ws.warn("Aucune image exploitable: la video est peut-etre entierement noire ou audio seule.")

    for f in frames:
        ws.register_asset(f["file"])
    return frames


def probe_duration(video: Path) -> float:
    ffprobe = require("ffprobe", "ffprobe accompagne ffmpeg: verifier l'installation.")
    proc = run(
        [
            ffprobe, "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video),
        ],
        check=False,
        timeout=120,
    )
    try:
        return float((proc.stdout or "0").strip())
    except ValueError:
        return 0.0


def build_contact_sheets(frames: list[dict], ws: Workspace, per_sheet: int = 12) -> list[str]:
    """Assemble les frames en planches contact horodatees.

    Lire 24 images coute cher en contexte; lire 2 planches puis zoomer sur 3
    frames utiles coute peu et donne le meme resultat. Le timecode inscrit sur
    chaque vignette est ce qui permet de faire le lien avec la transcription.
    """
    if not frames:
        return []
    if not has_module("PIL") and not pip_install("pillow"):
        ws.warn("Pillow indisponible: pas de planche contact, les frames restent lisibles une a une.")
        return []

    from PIL import Image, ImageDraw  # type: ignore

    sheets: list[str] = []
    thumb_w, thumb_h = 512, 288
    band = 22
    for sheet_idx in range(math.ceil(len(frames) / per_sheet)):
        batch = frames[sheet_idx * per_sheet : (sheet_idx + 1) * per_sheet]
        rows = math.ceil(len(batch) / TILE_COLS)
        sheet = Image.new("RGB", (TILE_COLS * thumb_w, rows * (thumb_h + band)), "white")
        draw = ImageDraw.Draw(sheet)
        for i, fr in enumerate(batch):
            src = ws.assets_dir / fr["file"]
            if not src.exists():
                continue
            with Image.open(src) as im:
                im = im.convert("RGB")
                im.thumbnail((thumb_w, thumb_h))
                x = (i % TILE_COLS) * thumb_w
                y = (i // TILE_COLS) * (thumb_h + band)
                sheet.paste(im, (x, y))
                draw.rectangle([x, y + thumb_h, x + thumb_w, y + thumb_h + band], fill="#1f2937")
                draw.text((x + 6, y + thumb_h + 5), f"{fr['file']}  |  {fmt_time(fr['time'])}", fill="white")
        name = f"contact-sheet-{sheet_idx + 1}.jpg"
        sheet.save(ws.assets_dir / name, quality=88)
        ws.register_asset(name)
        sheets.append(name)
    return sheets


def frames_section(frames: list[dict], sheets: list[str]) -> str:
    if not frames:
        return "## Images\n\nAucune image extraite (mode visuel desactive).\n"
    lines = ["## Images extraites", ""]
    if sheets:
        lines.append("Planches contact (a lire en premier, chaque vignette porte son timecode) :")
        lines += [f"- `assets/{s}`" for s in sheets]
        lines.append("")
    lines.append("Frames pleine resolution :")
    lines += [f"- `assets/{f['file']}` — {fmt_time(f['time'])}" for f in frames]
    lines.append("")
    return "\n".join(lines)
