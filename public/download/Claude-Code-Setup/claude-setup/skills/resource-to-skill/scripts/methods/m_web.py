# -*- coding: utf-8 -*-
"""Methode: page web / documentation en ligne."""

from __future__ import annotations

import re
import ssl
import urllib.error
import urllib.request

from base import ExtractionError, Workspace, has_module, pip_install

NAME = "web"
VERSION = "1.0"
MATURITY = "partial"
GAPS = [
    "Pages rendues par JavaScript: seul le HTML initial est recupere, souvent vide.",
    "Pas de suivi des liens: une documentation multi-pages doit etre passee page par page "
    "(ou reprise par l'outil WebFetch de Claude).",
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) resource-to-skill/1.0"


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr,en;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
    except (urllib.error.URLError, ssl.SSLError):
        # Certificat auto-signe dans la chaine TLS du poste: on retente sans verification.
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            raw = resp.read()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    html = _fetch(source)
    ws.add_raw("page.html", html)

    if not has_module("bs4") and not pip_install("beautifulsoup4"):
        raise ExtractionError("beautifulsoup4 requis: pip install beautifulsoup4")
    from bs4 import BeautifulSoup  # type: ignore

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "aside", "noscript"]):
        tag.decompose()

    title = (soup.title.get_text(strip=True) if soup.title else source)
    main = soup.find("main") or soup.find("article") or soup.body or soup

    lines: list[str] = []
    for el in main.find_all(["h1", "h2", "h3", "h4", "p", "li", "pre", "code", "table"]):
        text = el.get_text("\n" if el.name == "pre" else " ", strip=True)
        if not text:
            continue
        if el.name.startswith("h"):
            lines.append(f"\n{'#' * int(el.name[1])} {text}\n")
        elif el.name == "li":
            lines.append(f"- {text}")
        elif el.name == "pre":
            lines.append(f"\n```\n{text}\n```\n")
        elif el.name == "code" and el.parent.name != "pre":
            continue
        else:
            lines.append(text)

    body = "\n".join(lines).strip()
    if len(body) < 400:
        ws.warn(
            "Contenu textuel tres pauvre: la page est probablement rendue par JavaScript."
        )
        ws.suggest("Reprendre cette URL avec l'outil WebFetch de Claude, qui execute davantage la page.")

    headings = [h.get_text(strip=True) for h in main.find_all(["h1", "h2", "h3"])][:60]
    ws.write_content(
        "\n".join([f"# {title}", "", f"- **URL** : {source}", "", "## Contenu", "", body])
    )

    return {
        "title": title,
        "coverage": {
            "text": "ok" if len(body) > 1500 else ("partial" if body else "missing"),
            "visual": "n/a",
            "structure": "ok" if len(headings) > 2 else "partial",
        },
        "stats": {"chars": len(body), "headings": len(headings)},
        "extra": {"headings": headings[:20]},
    }
