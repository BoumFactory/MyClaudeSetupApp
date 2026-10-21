# -*- coding: utf-8 -*-
"""Methode: video en ligne (YouTube et tout site gere par yt-dlp)."""

from __future__ import annotations

import json
from pathlib import Path

from base import ExtractionError, Workspace, clip, require, run
from video_common import (
    build_contact_sheets,
    fmt_time,
    frames_section,
    parse_vtt,
    sample_frames,
    transcribe_locally,
)

NAME = "video_youtube"
VERSION = "1.1"
MATURITY = "full"
GAPS = [
    "Les videos privees ou soumises a un age gate necessitent des cookies (--cookies-from-browser).",
    "Les sous-titres automatiques ne ponctuent pas et deforment les termes techniques rares "
    "(les noms propres se verifient a l'image).",
    "Sur les videos faites de texte anime, une capture peut attraper un texte en cours "
    "d'ecriture: le rejet des ecrans uniformes limite le phenomene sans l'eliminer.",
]


def _pick_subtitle_lang(info: dict, wanted: str | None) -> tuple[str | None, bool]:
    """Choisit la meilleure piste: manuelle avant automatique, langue d'origine avant traduction.

    Une traduction automatique d'une traduction automatique degrade beaucoup le
    vocabulaire technique, d'ou la preference pour la langue reellement parlee.
    """
    manual = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}
    original = (info.get("language") or "").split("-")[0]
    order = [w for w in (wanted, original, "fr", "en") if w]

    for track, is_auto in ((manual, False), (auto, True)):
        keys = list(track.keys())
        for pref in order:
            for key in keys:
                if key == pref or key.startswith(f"{pref}-"):
                    return key, is_auto
        if keys and not is_auto:
            return keys[0], False
    return (list(auto.keys())[0], True) if auto else (None, False)


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    ytdlp = require("yt-dlp", "Installer avec: pip install -U yt-dlp")
    visual = opts.get("visual", "auto")
    wanted_lang = opts.get("lang")

    proc = run([ytdlp, "--dump-json", "--no-warnings", "--skip-download", source], timeout=300)
    info = json.loads(proc.stdout.strip().splitlines()[-1])
    ws.add_raw("metadata.json", json.dumps(info, ensure_ascii=False, indent=2)[:2_000_000])

    title = info.get("title") or "video"
    duration = info.get("duration") or 0
    lang, is_auto = _pick_subtitle_lang(info, wanted_lang)

    transcript, words = "", 0
    if lang:
        flag = "--write-auto-subs" if is_auto else "--write-subs"
        run(
            [
                ytdlp, "--skip-download", flag, "--sub-langs", lang,
                "--sub-format", "vtt/best", "--convert-subs", "vtt",
                "--no-warnings", "-o", str(ws.raw_dir / "subs.%(ext)s"), source,
            ],
            check=False,
            timeout=600,
        )
        vtt_files = sorted(ws.raw_dir.glob("subs*.vtt"))
        if vtt_files:
            ws.claim_raw(vtt_files[0].name)
            transcript, words = parse_vtt(vtt_files[0].read_text(encoding="utf-8", errors="replace"))
            if is_auto:
                ws.warn(
                    f"Sous-titres automatiques ({lang}): ponctuation absente et termes "
                    "techniques parfois mal transcrits. Croiser avec les images en cas de doute."
                )
        else:
            ws.warn(f"Piste de sous-titres `{lang}` annoncee mais non telechargeable.")

    need_audio = not transcript
    media = None
    if visual != "off" or need_audio:
        fmt = (
            "bv*[height<=720]+ba/b[height<=720]/b"
            if need_audio
            else "bv*[height<=720]/b[height<=720]/b"
        )
        run(
            [
                ytdlp, "-f", fmt, "--no-warnings", "--no-playlist",
                "-o", str(ws.raw_dir / "video.%(ext)s"), source,
            ],
            timeout=2400,
        )
        candidates = [p for p in ws.raw_dir.glob("video.*") if p.suffix != ".vtt"]
        if candidates:
            media = candidates[0]
            ws.claim_raw(media.name)

    if need_audio and media:
        transcript = transcribe_locally(media, ws, language=wanted_lang)
        words = len(transcript.split())
        if not transcript:
            ws.warn("Aucun sous-titre et aucune transcription possible: contenu parle non capte.")

    frames = sample_frames(media, ws, visual) if (media and visual != "off") else []
    sheets = build_contact_sheets(frames, ws)

    chapters = info.get("chapters") or []
    parts = [
        f"# {title}",
        "",
        f"- **Source** : {info.get('webpage_url', source)}",
        f"- **Chaine** : {info.get('channel') or info.get('uploader') or '?'}",
        f"- **Duree** : {fmt_time(duration)}",
        f"- **Piste texte** : {'sous-titres ' + ('automatiques' if is_auto else 'manuels') + f' ({lang})' if lang else 'whisper (local)' if transcript else 'aucune'}",
        "",
    ]
    if info.get("description"):
        parts += ["## Description de l'auteur", "", info["description"].strip(), ""]
    if chapters:
        parts += ["## Chapitres", ""]
        parts += [f"- **{fmt_time(c.get('start_time', 0))}** {c.get('title', '')}" for c in chapters]
        parts.append("")
    parts += ["## Transcription", "", transcript or "_Non disponible._", ""]
    parts.append(frames_section(frames, sheets))
    ws.write_content("\n".join(parts))

    if frames:
        ws.suggest(
            f"Regarder d'abord `assets/{sheets[0]}` si une planche existe, puis ouvrir seulement "
            "les frames qui montrent du code, un schema ou une interface."
        )
    if visual == "auto" and frames:
        ws.suggest("Si les diapos defilent vite et que des ecrans manquent, relancer avec --visual deep.")

    return {
        "title": title,
        "coverage": {
            "text": "ok" if words > 200 else ("partial" if words else "missing"),
            "visual": "sampled" if frames else ("n/a" if visual == "off" else "missing"),
            "structure": "ok" if chapters else "partial",
        },
        "stats": {
            "duration_s": duration,
            "transcript_words": words,
            "frames": len(frames),
            "contact_sheets": len(sheets),
        },
        "extra": {
            "channel": info.get("channel"),
            "upload_date": info.get("upload_date"),
            "subtitle_lang": lang,
            "subtitle_auto": is_auto,
            "description_excerpt": clip(info.get("description") or "", 300),
        },
    }
