# -*- coding: utf-8 -*-
"""Rapport HTML de relecture: ce qui a ete extrait, ce qui a ete ecrit.

Le skill s'execute en une passe, sans validation intermediaire. Le rapport est
donc le moment ou l'utilisateur reprend la main: il doit pouvoir verifier en
quelques minutes que la matiere a bien ete captee (transcription, images) et que
le skill produit dit ce qu'il faut.

    python make_report.py --skill <dir-du-skill> --extraction <workspace> [--extraction …]
                          [--notes notes.md] [--out rapport.html] [--no-open]

Fichier autonome: images integrees en base64, aucun CDN, theme clair, images
agrandies au clic (second clic = taille reelle).
"""

from __future__ import annotations

import argparse
import base64
import html
import io
import json
import re
import webbrowser
from pathlib import Path

MAX_IMG_WIDTH = 1400
PREVIEW_CHARS = 6000


# --------------------------------------------------------------------------
# Markdown minimal (assez pour un SKILL.md et un content.md)
# --------------------------------------------------------------------------

def md_to_html(md: str) -> str:
    out: list[str] = []
    in_code = False
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    for raw in md.splitlines():
        line = raw.rstrip()
        fence = re.match(r"^\s*(`{3,4})(\w*)\s*$", line)
        if fence:
            close_lists()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append(f'<pre class="code"><code data-lang="{html.escape(fence.group(2))}">')
                in_code = True
            continue
        if in_code:
            out.append(html.escape(raw))
            continue

        if not line.strip():
            close_lists()
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", line)
        if h:
            close_lists()
            level = min(len(h.group(1)) + 1, 6)
            out.append(f"<h{level}>{inline(h.group(2))}</h{level}>")
            continue
        if re.match(r"^\s*[-*]{3,}\s*$", line):
            close_lists()
            out.append("<hr>")
            continue
        li = re.match(r"^(\s*)[-*+]\s+(.*)$", line)
        if li:
            if not in_ul:
                close_lists()
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(li.group(2))}</li>")
            continue
        ol = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", line)
        if ol:
            if not in_ol:
                close_lists()
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline(ol.group(3))}</li>")
            continue
        if line.startswith(">"):
            close_lists()
            out.append(f"<blockquote>{inline(line.lstrip('> '))}</blockquote>")
            continue
        close_lists()
        out.append(f"<p>{inline(line)}</p>")

    if in_code:
        out.append("</code></pre>")
    close_lists()
    return "\n".join(out)


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


# --------------------------------------------------------------------------
# Images
# --------------------------------------------------------------------------

def img_data_uri(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    try:
        from PIL import Image  # type: ignore

        with Image.open(io.BytesIO(raw)) as im:
            im = im.convert("RGB")
            if im.width > MAX_IMG_WIDTH:
                im = im.resize((MAX_IMG_WIDTH, round(im.height * MAX_IMG_WIDTH / im.width)))
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=82)
            raw = buf.getvalue()
        mime = "image/jpeg"
    except Exception:
        mime = {"png": "image/png", "gif": "image/gif", "webp": "image/webp"}.get(
            path.suffix.lstrip(".").lower(), "image/jpeg"
        )
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


# --------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------

COVERAGE_STYLE = {
    "ok": ("ok", "capte"),
    "sampled": ("warn", "echantillonne"),
    "partial": ("warn", "partiel"),
    "missing": ("bad", "absent"),
    "n/a": ("na", "sans objet"),
}


def extraction_section(ws_dir: Path, idx: int) -> str:
    manifest_path = ws_dir / "manifest.json"
    if not manifest_path.exists():
        return f'<section><h2>Extraction {idx}</h2><p class="bad">manifest.json introuvable dans {html.escape(str(ws_dir))}</p></section>'
    m = json.loads(manifest_path.read_text(encoding="utf-8"))

    badges = "".join(
        f'<span class="badge {COVERAGE_STYLE.get(v, ("na", v))[0]}">{html.escape(k)} : '
        f'{html.escape(COVERAGE_STYLE.get(v, ("na", v))[1])}</span>'
        for k, v in (m.get("coverage") or {}).items()
    )
    stats = " · ".join(f"{k} : {v}" for k, v in (m.get("stats") or {}).items())

    warns = "".join(f"<li>{html.escape(w)}</li>" for w in m.get("warnings", []))
    warns_html = f'<div class="callout warn-box"><strong>Signale par l\'extraction</strong><ul>{warns}</ul></div>' if warns else ""

    gallery = ""
    assets = [a for a in (m.get("artifacts", {}).get("assets") or [])]
    sheets = [a for a in assets if "contact-sheet" in a]
    others = [a for a in assets if "contact-sheet" not in a]
    tiles = []
    for rel in sheets + others[:24]:
        p = ws_dir / rel
        uri = img_data_uri(p)
        if uri:
            cls = "sheet" if "contact-sheet" in rel else "thumb"
            tiles.append(f'<figure class="{cls}"><img src="{uri}" alt="{html.escape(rel)}"><figcaption>{html.escape(Path(rel).name)}</figcaption></figure>')
    if tiles:
        extra = f"<p class='muted'>{len(others) - 24} image(s) supplementaire(s) dans <code>{html.escape(str(ws_dir / 'assets'))}</code>.</p>" if len(others) > 24 else ""
        gallery = f'<h3>Ce qui a ete vu</h3><div class="gallery">{"".join(tiles)}</div>{extra}'

    content_path = ws_dir / "content.md"
    preview = ""
    if content_path.exists():
        text = content_path.read_text(encoding="utf-8", errors="replace")
        head = text[:PREVIEW_CHARS]
        more = f"\n\n_… {len(text) - PREVIEW_CHARS} caracteres supplementaires dans content.md._" if len(text) > PREVIEW_CHARS else ""
        preview = (
            f'<details><summary>Extrait de la matiere brute ({len(text):,} caracteres)</summary>'
            f'<div class="md">{md_to_html(head + more)}</div></details>'.replace(",", " ")
        )

    return f"""<section id="extraction-{idx}">
  <h2>Matiere extraite — {html.escape(m.get('title') or ws_dir.name)}</h2>
  <p class="meta">Source : <code>{html.escape(str(m.get('source', '?')))}</code><br>
     Methode : <strong>{html.escape(m.get('method', {}).get('name', '?'))}</strong>
     (maturite {html.escape(str(m.get('method', {}).get('maturity', '?')))}) —
     workspace <code>{html.escape(str(ws_dir))}</code></p>
  <div class="badges">{badges}</div>
  <p class="muted">{html.escape(stats)}</p>
  {warns_html}
  {gallery}
  {preview}
</section>"""


def skill_section(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    body = skill_md.read_text(encoding="utf-8", errors="replace") if skill_md.exists() else "_SKILL.md introuvable._"

    fm = re.match(r"^---\n(.*?)\n---\n(.*)$", body, flags=re.S)
    front, rest = (fm.group(1), fm.group(2)) if fm else ("", body)
    desc = ""
    dm = re.search(r"^description:\s*(.+)$", front, flags=re.M)
    if dm:
        desc = dm.group(1).strip()

    files = []
    for p in sorted(skill_dir.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            rel = p.relative_to(skill_dir)
            files.append((rel, p))

    tree = "".join(
        f"<li><code>{html.escape(str(rel).replace(chr(92), '/'))}</code> "
        f'<span class="muted">{p.stat().st_size:,} o</span></li>'.replace(",", " ")
        for rel, p in files
    )

    extras = []
    for rel, p in files:
        if rel.name == "SKILL.md":
            continue
        if p.suffix.lower() in (".md", ".json", ".txt"):
            text = p.read_text(encoding="utf-8", errors="replace")
            preview_text = text[:PREVIEW_CHARS]
            rendered = md_to_html(preview_text) if p.suffix.lower() == ".md" else f'<pre class="code"><code>{html.escape(preview_text)}</code></pre>'
            extras.append(
                f'<details><summary><code>{html.escape(str(rel).replace(chr(92), "/"))}</code> — {len(text):,} caracteres</summary>'
                f'<div class="md">{rendered}</div></details>'.replace(",", " ")
            )

    return f"""<section id="skill">
  <h2>Skill produit — <code>{html.escape(skill_dir.name)}</code></h2>
  <div class="callout"><strong>Description (c'est elle qui declenche le skill)</strong>
    <p>{html.escape(desc) or '<em>absente</em>'}</p></div>
  <h3>Fichiers</h3>
  <ul class="tree">{tree}</ul>
  <h3>SKILL.md</h3>
  <div class="md skillmd">{md_to_html(rest)}</div>
  {'<h3>Ressources jointes</h3>' + ''.join(extras) if extras else ''}
</section>"""


def checklist_section(extractions: list[Path]) -> str:
    items: list[str] = []
    for ws_dir in extractions:
        mp = ws_dir / "manifest.json"
        if not mp.exists():
            continue
        m = json.loads(mp.read_text(encoding="utf-8"))
        for dim, val in (m.get("coverage") or {}).items():
            if val in ("partial", "missing"):
                items.append(f"Dimension <strong>{html.escape(dim)}</strong> {html.escape(val)} sur « {html.escape(m.get('title', ws_dir.name))} » : verifier que le skill ne s'appuie pas sur ce qui manque.")
        for w in m.get("warnings", []):
            items.append(html.escape(w))
    items.append("Le skill se declenchera-t-il sur les formulations que vous employez vraiment ? Relire la description.")
    items.append("Le skill contient-il des affirmations que la ressource ne dit pas ? Signaler pour correction.")
    items.append("Manque-t-il un exemple concret tire de la ressource ?")
    lis = "".join(f'<li><label><input type="checkbox"> {i}</label></li>' for i in items)
    return f'<section id="verifier"><h2>A verifier</h2><ul class="check">{lis}</ul></section>'


CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#16202c;--muted:#5c6b7f;--line:#dde3ec;--accent:#2563eb;
--ok:#16794a;--okbg:#e4f5ec;--warn:#8a5a00;--warnbg:#fdf3dc;--bad:#a02128;--badbg:#fdeaea;--nabg:#eef1f6;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 "Segoe UI",system-ui,-apple-system,sans-serif}
header.top{background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;padding:36px 28px}
header.top h1{margin:0 0 6px;font-size:1.7rem}
header.top p{margin:0;opacity:.9}
nav{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.95);border-bottom:1px solid var(--line);
padding:10px 28px;display:flex;gap:18px;flex-wrap:wrap;backdrop-filter:blur(6px)}
nav a{color:var(--accent);text-decoration:none;font-weight:600;font-size:.9rem}
nav a:hover{text-decoration:underline}
main{max-width:1080px;margin:0 auto;padding:28px}
section{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px 28px;margin-bottom:26px;
box-shadow:0 1px 3px rgba(20,30,50,.05)}
h2{margin-top:0;font-size:1.35rem;border-bottom:2px solid var(--line);padding-bottom:10px}
h3{margin-top:26px;font-size:1.08rem;color:#1e3a8a}
p.meta{color:var(--muted);font-size:.92rem}
.muted{color:var(--muted);font-size:.9rem}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
.badge{padding:4px 12px;border-radius:999px;font-size:.82rem;font-weight:600;background:var(--nabg)}
.badge.ok{background:var(--okbg);color:var(--ok)}
.badge.warn{background:var(--warnbg);color:var(--warn)}
.badge.bad{background:var(--badbg);color:var(--bad)}
.callout{background:#f0f5ff;border-left:4px solid var(--accent);padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0}
.callout.warn-box{background:var(--warnbg);border-left-color:#c98a00}
.callout ul{margin:8px 0 0;padding-left:20px}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin:14px 0}
.gallery figure{margin:0;background:#fbfcfe;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.gallery figure.sheet{grid-column:1/-1}
.gallery img{width:100%;display:block;cursor:zoom-in}
.gallery figcaption{font-size:.78rem;color:var(--muted);padding:6px 8px;word-break:break-all}
details{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:12px 0;background:#fbfcfe}
summary{cursor:pointer;font-weight:600;color:#1e3a8a}
details[open] summary{margin-bottom:10px}
.md{font-size:.95rem}
.md h2,.md h3,.md h4{color:#1e3a8a}
.md pre.code{background:#0f172a;color:#e2e8f0;padding:14px 16px;border-radius:8px;overflow-x:auto;font-size:.85rem;line-height:1.5}
.md code{background:#eef2f8;padding:1px 5px;border-radius:4px;font-size:.88em;font-family:Consolas,monospace}
.md pre.code code{background:none;padding:0;color:inherit}
.md blockquote{border-left:3px solid var(--line);margin:10px 0;padding-left:14px;color:var(--muted)}
.skillmd{max-height:640px;overflow-y:auto;border:1px solid var(--line);border-radius:10px;padding:16px 20px;background:#fbfcfe}
ul.tree{columns:2;font-size:.9rem;list-style:none;padding-left:0}
ul.tree li{break-inside:avoid;padding:2px 0}
ul.check{list-style:none;padding-left:0}
ul.check li{padding:6px 0;border-bottom:1px dashed var(--line)}
ul.check input{margin-right:10px;transform:scale(1.15)}
table{border-collapse:collapse;width:100%}
#lb{position:fixed;inset:0;background:rgba(10,16,28,.92);display:none;z-index:100;overflow:auto;cursor:zoom-in}
#lb.on{display:block}
#lb img{display:block;margin:auto;max-width:98vw;max-height:96vh;cursor:zoom-in}
#lb.full{cursor:zoom-out}
#lb.full img{max-width:none;max-height:none;cursor:zoom-out}
#lb .hint{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);color:#cbd5e1;font-size:.82rem;
background:rgba(15,23,42,.85);padding:6px 14px;border-radius:999px}
@media(max-width:720px){ul.tree{columns:1}main{padding:16px}section{padding:18px}}
"""

JS = """
const lb=document.getElementById('lb'), lbi=lb.querySelector('img');
document.querySelectorAll('.gallery img').forEach(img=>{
  img.addEventListener('click',()=>{lbi.src=img.src;lb.classList.add('on');lb.classList.remove('full');
    document.body.style.overflow='hidden';});
});
lb.addEventListener('click',e=>{
  if(e.target===lbi){ lb.classList.toggle('full'); lb.scrollTop=0; return; }
  lb.classList.remove('on','full'); document.body.style.overflow='';
});
document.addEventListener('keydown',e=>{ if(e.key==='Escape'){lb.classList.remove('on','full');document.body.style.overflow='';}});
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True, help="dossier du skill genere")
    ap.add_argument("--extraction", action="append", default=[], help="workspace d'extraction (repetable)")
    ap.add_argument("--notes", help="fichier markdown expliquant les choix de conception")
    ap.add_argument("--out", help="fichier HTML de sortie")
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    skill_dir = Path(args.skill).resolve()
    extractions = [Path(e).resolve() for e in args.extraction]
    out = Path(args.out).resolve() if args.out else skill_dir.parent / f"rapport-{skill_dir.name}.html"

    notes_html = ""
    if args.notes and Path(args.notes).exists():
        notes_html = f'<section id="choix"><h2>Choix de conception</h2><div class="md">{md_to_html(Path(args.notes).read_text(encoding="utf-8"))}</div></section>'

    sections = [skill_section(skill_dir)]
    sections += [extraction_section(ws, i + 1) for i, ws in enumerate(extractions)]
    if notes_html:
        sections.append(notes_html)
    sections.append(checklist_section(extractions))

    nav = ['<a href="#skill">Skill produit</a>']
    nav += [f'<a href="#extraction-{i + 1}">Matiere {i + 1}</a>' for i in range(len(extractions))]
    if notes_html:
        nav.append('<a href="#choix">Choix</a>')
    nav.append('<a href="#verifier">A verifier</a>')

    sources = ", ".join(
        json.loads((ws / "manifest.json").read_text(encoding="utf-8")).get("source", str(ws))
        for ws in extractions if (ws / "manifest.json").exists()
    )

    doc = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rapport — {html.escape(skill_dir.name)}</title>
<style>{CSS}</style></head>
<body>
<header class="top">
  <h1>Rapport de relecture — {html.escape(skill_dir.name)}</h1>
  <p>Ressource(s) : {html.escape(sources) or '—'}</p>
</header>
<nav>{''.join(nav)}</nav>
<main>{''.join(sections)}</main>
<div id="lb"><img alt=""><div class="hint">Clic sur l'image : taille reelle · Clic autour ou Echap : fermer</div></div>
<script>{JS}</script>
</body></html>"""

    out.write_text(doc, encoding="utf-8")
    print(json.dumps({"status": "ok", "report": str(out), "size_kb": round(out.stat().st_size / 1024)}, ensure_ascii=False))
    if not args.no_open:
        webbrowser.open(out.as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
