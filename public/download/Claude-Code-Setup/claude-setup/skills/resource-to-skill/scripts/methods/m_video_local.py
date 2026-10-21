# -*- coding: utf-8 -*-
"""Methode: fichier video local (.mp4, .mkv, .mov, .webm, .avi)."""

from __future__ import annotations

from pathlib import Path

from base import Workspace
from video_common import (
    build_contact_sheets,
    fmt_time,
    frames_section,
    parse_vtt,
    probe_duration,
    sample_frames,
    transcribe_locally,
)

NAME = "video_local"
VERSION = "1.1"
MATURITY = "full"
GAPS = [
    "Sans piste de sous-titres a cote du fichier, la transcription depend de faster-whisper "
    "(indisponible sur un Python 32 bits).",
    "Sur les videos faites de texte anime, une capture peut attraper un texte en cours "
    "d'ecriture: le rejet des ecrans uniformes limite le phenomene sans l'eliminer.",
]

SIDECAR_SUFFIXES = (".srt", ".vtt")


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    video = Path(source)
    visual = opts.get("visual", "auto")
    duration = probe_duration(video)

    # Un .srt/.vtt depose a cote du fichier est toujours meilleur qu'une
    # transcription automatique: on le privilegie systematiquement.
    transcript, words, origin = "", 0, "aucune"
    for suffix in SIDECAR_SUFFIXES:
        sidecar = video.with_suffix(suffix)
        if sidecar.exists():
            text = sidecar.read_text(encoding="utf-8", errors="replace")
            transcript, words = parse_vtt(text)
            origin = f"sous-titres fournis ({sidecar.name})"
            ws.add_raw(sidecar.name, text)
            break

    if not transcript:
        transcript = transcribe_locally(video, ws, language=opts.get("lang"))
        words = len(transcript.split())
        origin = "whisper (local)" if transcript else "aucune"

    frames = sample_frames(video, ws, visual) if visual != "off" else []
    sheets = build_contact_sheets(frames, ws)

    parts = [
        f"# {video.stem}",
        "",
        f"- **Fichier** : `{video}`",
        f"- **Duree** : {fmt_time(duration)}",
        f"- **Piste texte** : {origin}",
        "",
        "## Transcription",
        "",
        transcript or "_Non disponible._",
        "",
        frames_section(frames, sheets),
    ]
    ws.write_content("\n".join(parts))

    if frames:
        ws.suggest("Lire les planches contact avant d'ouvrir les frames une a une.")
    if not transcript:
        ws.suggest("Contenu parle non capte: l'extraction repose entierement sur les images.")

    return {
        "title": video.stem,
        "coverage": {
            "text": "ok" if words > 200 else ("partial" if words else "missing"),
            "visual": "sampled" if frames else ("n/a" if visual == "off" else "missing"),
            "structure": "partial",
        },
        "stats": {"duration_s": round(duration), "transcript_words": words, "frames": len(frames)},
        "extra": {"transcript_origin": origin},
    }
