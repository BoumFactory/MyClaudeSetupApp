"""Applique un JSON de progression à une fiche HTML vierge.

Usage :
    python apply_progression.py --html progression_5E_vierge.html \
                                --progression my_progression.json \
                                --output progression_5E_remplie.html

Le JSON de progression décrit :
  - une liste de séquences (titre + objectifs codes + commentaires éventuels
    + séparateurs Exos/RdP/Auto)
  - des marqueurs "vacances" insérés entre certaines séquences
  - éventuellement une séquence d'intro à remplacer

Schéma complet : voir `references/format_progression_json.md`.

Effets sur le HTML :
  1. Remplace le contenu du <div id="sequencesContainer"> par les séquences
     décrites (les séquences d'intro restent éditables côté HTML).
  2. Pour chaque objectif déposé, marque l'élément correspondant dans le
     leftPanel comme `class="objectif grayed"` et `draggable="false"`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import html_escape  # noqa: E402


# ---------------------------------------------------------------------------
#  Lookup des couleurs / textes d'objectifs depuis le leftPanel
# ---------------------------------------------------------------------------

# data-code="..."  +  style="background:#xxxx; color:white;"  +  texte
OBJECTIF_PATTERN = re.compile(
    r'<div class="objectif(?P<grayed>[^"]*)" '
    r'(?P<draggable>draggable="(?:true|false)" )?'
    r'title="(?P<title>[^"]*)" '
    r'style="background:(?P<bg>[^;]+);[^"]*" '
    r'data-code="(?P<code>[^"]+)"'
    r'[^>]*>(?P<inner>.*?)</div>',
    flags=re.DOTALL,
)


def build_objectifs_index(html_text: str) -> dict[str, dict[str, str]]:
    """Construit un index code → {bg, text, theme, page, bo_ref, bo_url}.

    Depuis le patch métadonnées BO, chaque .objectif du leftPanel contient un
    span.objectif-text + un .objectif-meta. On extrait le texte du span pour ne
    pas charrier le pied de méta dans les .right-objectif générés.
    """
    start = html_text.find('<div id="leftPanel"')
    end = html_text.find('<div id="resizer"', start)
    if start == -1 or end == -1:
        raise ValueError("leftPanel boundaries not found")
    panel = html_text[start:end]

    # Regex large : on capture tout le bloc `<div class="objectif…"…>…</div>`
    # (la classe peut être "objectif", "objectif optionnel", "objectif grayed",
    # ou "objectif optionnel grayed"). Le contenu peut contenir un span
    # objectif-text + un div objectif-meta — tolérance via `[\s\S]*?`.
    pattern = re.compile(
        r'<div class="objectif(?P<extra>[^"]*)"\s+'
        r'(?:draggable="(?:true|false)"\s+)?'
        r'title="(?P<title>[^"]*)"\s+'
        r'style="background:(?P<bg>[^;]+);[^"]*"\s+'
        r'data-code="(?P<code>[^"]+)"'
        r'(?:[^>]*\sdata-theme="(?P<theme>[^"]*)")?'
        r'(?:[^>]*\sdata-type="(?P<ctype>[^"]*)")?'
        r'(?:[^>]*\sdata-page="(?P<page>[^"]*)")?'
        r'(?:[^>]*\sdata-bo-ref="(?P<boref>[^"]*)")?'
        r'(?:[^>]*\sdata-bo-url="(?P<bourl>[^"]*)")?'
        r'[^>]*>(?P<inner>[\s\S]*?)</div>',
        flags=re.DOTALL,
    )
    # Pour extraire le texte affiché : préférer le contenu du <span class="objectif-text">
    # si présent (cas post-patch), sinon le inner entier (cas legacy/sans patch).
    span_re = re.compile(
        r'<span class="objectif-text">([\s\S]*?)</span>'
    )
    index: dict[str, dict[str, str]] = {}
    for m in pattern.finditer(panel):
        code = m.group("code")
        bg = m.group("bg").strip()
        inner = m.group("inner")
        sm = span_re.search(inner)
        text = (sm.group(1) if sm else inner).strip() or m.group("title")
        theme = (m.group("theme") or "").strip()
        page = (m.group("page") or "").strip()
        bo_ref = (m.group("boref") or "").strip()
        bo_url = (m.group("bourl") or "").strip()
        ctype = (m.group("ctype") or "").strip()
        index[code] = {
            "bg": bg, "text": text, "theme": theme,
            "page": page, "bo_ref": bo_ref, "bo_url": bo_url,
            "type": ctype,
        }
    return index


def print_coverage_stats(objectifs_index: dict[str, dict[str, str]],
                          placed_codes: set[str]) -> None:
    """Affiche un récap placé / total par domaine après injection."""
    by_theme_total: dict[str, int] = {}
    by_theme_placed: dict[str, int] = {}
    for code, data in objectifs_index.items():
        theme = data.get("theme") or "—"
        by_theme_total[theme] = by_theme_total.get(theme, 0) + 1
        if code in placed_codes:
            by_theme_placed[theme] = by_theme_placed.get(theme, 0) + 1

    total = len(objectifs_index)
    placed = len(placed_codes & set(objectifs_index.keys()))
    pct = (placed / total * 100) if total else 0.0
    print(f"\nCouverture : {placed}/{total} compétences placées ({pct:.1f} %)")

    width = max((len(t) for t in by_theme_total), default=10)
    for theme in sorted(by_theme_total.keys()):
        t = by_theme_total[theme]
        p = by_theme_placed.get(theme, 0)
        bar_n = int(round((p / t) * 20)) if t else 0
        bar = "█" * bar_n + "·" * (20 - bar_n)
        print(f"  {theme:<{width}}  {p:>3}/{t:<3}  {bar}")

    missing_codes = sorted(set(objectifs_index.keys()) - placed_codes)
    if missing_codes:
        sample = ", ".join(missing_codes[:8])
        more = f" (+{len(missing_codes)-8} autres)" if len(missing_codes) > 8 else ""
        print(f"\n{len(missing_codes)} code(s) non placé(s). Exemples : {sample}{more}")


def grey_out_placed(html_text: str, codes: set[str]) -> str:
    """Pour chaque code placé, ajoute la classe 'grayed' et passe draggable="false"."""

    def replacer(m: re.Match) -> str:
        code = m.group("code")
        if code not in codes:
            return m.group(0)
        full = m.group(0)
        # Ajoute la classe grayed si absente
        if 'class="objectif"' in full:
            full = full.replace('class="objectif"', 'class="objectif grayed"', 1)
        elif 'class="objectif grayed"' in full:
            pass
        # Force draggable="false"
        full = re.sub(r'draggable="true"', 'draggable="false"', full)
        return full

    return OBJECTIF_PATTERN.sub(replacer, html_text)


# ---------------------------------------------------------------------------
#  Construction des séquences HTML depuis le JSON
# ---------------------------------------------------------------------------

def render_right_objectif(code: str, text: str, bg: str,
                           page: str = "", bo_ref: str = "", bo_url: str = "",
                           ctype: str = "") -> str:
    """Reproduit la structure produite par createRightObjectif() en JS.

    Ajoute le span .objectif-text et le .objectif-meta — visibles uniquement
    quand l'utilisateur double-clique pour étendre l'objectif. Si ctype vaut
    "approfondissement", on marque l'élément comme optionnel (classe et badge).
    """
    is_opt = (ctype == "approfondissement")
    classes = "right-objectif" + (" optionnel" if is_opt else "")
    opt_badge = (
        '<span class="opt-badge" title="Approfondissement optionnel — '
        'non exigible, à la discrétion de l\'enseignant">opt.</span>'
        if is_opt else ""
    )
    # Lien 📄 p.X cliquable via openPdfAtPage (JS injecté côté HTML vierge)
    meta_bits: list[str] = []
    if page:
        p_html = html_escape(page)
        meta_bits.append(
            f'<a href="#" onclick="openPdfAtPage({p_html}); '
            f'event.preventDefault(); event.stopPropagation(); return false;" '
            f'title="Ouvrir le PDF du programme à la page {p_html}">📄 p.{p_html}</a>'
        )
    if bo_ref:
        meta_bits.append(html_escape(bo_ref))
    if bo_url:
        meta_bits.append(
            f'<a href="{html_escape(bo_url)}" target="_blank" rel="noopener" '
            f'onclick="event.stopPropagation()">🔗 BO en ligne</a>'
        )
    meta_html = (
        '<div class="objectif-meta">' + " · ".join(meta_bits) + "</div>"
        if meta_bits else ""
    )
    return (
        f'<div class="{classes}" data-code="{html_escape(code)}" '
        f'title="{html_escape(text)}" '
        f'style="background-color: {html_escape(bg)};" draggable="true" '
        f'data-page="{html_escape(page)}" '
        f'data-bo-ref="{html_escape(bo_ref)}" '
        f'data-bo-url="{html_escape(bo_url)}" '
        f'data-type="{html_escape(ctype)}">'
        f'<span class="objectif-text">{html_escape(text)}{opt_badge}</span>'
        f'{meta_html}'
        f'<span class="close-btn delete-right-objectif" title="Supprimer cet objectif">×</span>'
        f'</div>'
    )


def render_commentaire(titre: str, texte: str) -> str:
    titre_html = html_escape(titre) if titre else "Commentaire / Ressource"
    texte_html = html_escape(texte) if texte else ""
    return (
        '<div class="commentaire-bloc open">'
        '<div class="commentaire-header">'
        '<span class="chevron" style="transform: rotate(90deg);">&#9656;</span>'
        f'<span class="commentaire-texte" contenteditable="true" oninput="updateExport()">{titre_html}</span>'
        '<button class="delete-commentaire" title="Supprimer ce commentaire">×</button>'
        '</div>'
        '<div class="commentaire-content">'
        f'<div class="commentaire-zone" contenteditable="true" oninput="scheduleSanitize(this)">{texte_html}</div>'
        '</div>'
        '</div>'
    )


def render_separator(label: str) -> str:
    label_html = html_escape(label) if label else "Exos / RdP / Auto🛠"
    return (
        '<div class="exercice-separator">'
        '<div class="separator-line">'
        f'<div class="separator-text" contenteditable="true" oninput="updateExport()">{label_html}</div>'
        '<button class="delete-separator" title="Supprimer">×</button>'
        '</div>'
        '</div>'
    )


def render_vacances(label: str) -> str:
    label_html = html_escape(label) if label else "Vacances"
    return (
        '<div class="vacances">'
        '<div class="ligne"></div>'
        f'<div class="texte" contenteditable="true" oninput="updateExport()">{label_html}</div>'
        '<div class="ligne"></div>'
        '<button class="delete-vacances" title="Supprimer cette ligne Vacances">✖</button>'
        '</div>'
    )


def render_sequence(seq: dict, objectifs_index: dict[str, dict[str, str]],
                    missing_codes: list[str]) -> str:
    titre = seq.get("titre", "Séquence <Titre>")
    contenu = seq.get("contenu", [])

    body_parts: list[str] = ['<div class="insertion-indicator"></div>']
    for item in contenu:
        kind = item.get("type", "objectif")
        if kind == "objectif":
            code = item.get("code", "")
            data = objectifs_index.get(code)
            if data is None:
                missing_codes.append(code)
                continue
            body_parts.append(render_right_objectif(
                code, data["text"], data["bg"],
                page=data.get("page", ""),
                bo_ref=data.get("bo_ref", ""),
                bo_url=data.get("bo_url", ""),
                ctype=data.get("type", ""),
            ))
        elif kind == "commentaire":
            body_parts.append(render_commentaire(item.get("titre", ""), item.get("texte", "")))
        elif kind == "separateur":
            body_parts.append(render_separator(item.get("label", "")))
        else:
            print(f"[WARN] Type d'item inconnu : {kind}", file=sys.stderr)

    return (
        '<div class="sequence open" draggable="true">'
        '<div class="sequence-header">'
        '<span class="chevron" onclick="this.closest(\'.sequence\').classList.toggle(\'open\')">&#9656;</span>'
        f'<div class="sequence-title" contenteditable="true" oninput="updateExport()">{html_escape(titre)}</div>'
        '<div class="sequence-buttons">'
        '<button onclick="ajouterSeparation(this)">🛠</button>'
        '<button onclick="ajouterCommentaire(this)">📝</button>'
        '<button onclick="event.stopPropagation(); moveSequence(this.closest(\'.sequence\'), -1)">🔼</button>'
        '<button onclick="event.stopPropagation(); moveSequence(this.closest(\'.sequence\'), 1)">🔽</button>'
        '<button class="delete-sequence" onclick="event.stopPropagation(); supprimerSequence(this)">×</button>'
        '</div>'
        '</div>'
        '<div class="sequence-content dropzone" ondrop="drop(event)" ondragover="allowDrop(event)">'
        + "".join(body_parts) +
        '</div>'
        '</div>'
    )


# ---------------------------------------------------------------------------
#  Découpage du HTML pour remplacer le sequencesContainer
# ---------------------------------------------------------------------------

def _find_div_close(html_text: str, open_pos: int) -> int:
    gt = html_text.find(">", open_pos)
    if gt == -1:
        raise ValueError("malformed opening div")
    depth = 1
    i = gt + 1
    while i < len(html_text) and depth > 0:
        next_open = html_text.find("<div", i)
        next_close = html_text.find("</div>", i)
        if next_close == -1:
            raise ValueError("unterminated div")
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            i = next_close + len("</div>")
            if depth == 0:
                return next_close
    raise ValueError("unmatched div")


def apply_progression(html_text: str, progression: dict,
                       show_stats: bool = True) -> str:
    objectifs_index = build_objectifs_index(html_text)

    pieces: list[str] = []
    placed_codes: set[str] = set()
    missing: list[str] = []

    # Séquence d'intro : on la conserve telle quelle (présente dans le HTML vierge)
    # SAUF si la progression la redéfinit explicitement via "intro": {...}.
    keep_intro = progression.get("conserver_intro", True)

    for entry in progression.get("elements", []):
        kind = entry.get("type")
        if kind == "sequence":
            pieces.append(render_sequence(entry, objectifs_index, missing))
            for item in entry.get("contenu", []):
                if item.get("type") == "objectif":
                    placed_codes.add(item.get("code", ""))
        elif kind == "vacances":
            pieces.append(render_vacances(entry.get("label", "Vacances")))
        else:
            print(f"[WARN] Type d'élément racine inconnu : {kind}", file=sys.stderr)

    # Localise le sequencesContainer
    open_token = '<div id="sequencesContainer"'
    open_pos = html_text.find(open_token)
    if open_pos == -1:
        raise ValueError("<div id=\"sequencesContainer\"> not found")
    close_pos = _find_div_close(html_text, open_pos)
    gt = html_text.find(">", open_pos)
    existing_inner = html_text[gt + 1:close_pos]

    new_inner_parts: list[str] = []
    if keep_intro:
        # L'intro est la première séquence pré-écrite (background:#868686).
        # On la repère par son tag d'ouverture puis on cherche le </div> qui lui
        # correspond via comptage d'imbrication (regex naïve ferait foirer sur les
        # divs imbriquées de la structure sequence-header / sequence-content).
        m = re.search(r'<div class="sequence open"[^>]*background:\s*#868686[^>]*>',
                       existing_inner)
        if m:
            intro_start = m.start()
            # Indice absolu dans html_text (existing_inner commence à gt+1).
            absolute_open = gt + 1 + intro_start
            intro_close_abs = _find_div_close(html_text, absolute_open)
            intro_end_rel = intro_close_abs - (gt + 1) + len("</div>")
            new_inner_parts.append(existing_inner[intro_start:intro_end_rel])
    new_inner_parts.extend(pieces)
    new_inner = "\n".join(new_inner_parts)

    html_text = html_text[: gt + 1] + "\n" + new_inner + "\n" + html_text[close_pos:]

    # Greys-out des objectifs placés dans le leftPanel.
    if placed_codes:
        html_text = grey_out_placed(html_text, placed_codes)

    if missing:
        print(
            f"[WARN] {len(missing)} code(s) absent(s) du leftPanel et donc non placé(s) : "
            + ", ".join(missing[:8]) + ("…" if len(missing) > 8 else ""),
            file=sys.stderr,
        )

    if show_stats:
        print_coverage_stats(objectifs_index, placed_codes)

    return html_text


# ---------------------------------------------------------------------------
#  CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Applique un JSON de progression à un HTML vierge.")
    parser.add_argument("--html", required=True, help="HTML vierge en entrée")
    parser.add_argument("--progression", required=True, help="JSON décrivant la progression")
    parser.add_argument("--output", required=True, help="HTML rempli en sortie")
    parser.add_argument("--no-stats", action="store_true",
                        help="N'affiche pas le récap de couverture par domaine.")
    args = parser.parse_args()

    html_text = Path(args.html).read_text(encoding="utf-8")
    progression = json.loads(Path(args.progression).read_text(encoding="utf-8"))

    out = apply_progression(html_text, progression, show_stats=not args.no_stats)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    print(f"[OK] Progression appliquée → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
