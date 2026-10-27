"""Utilitaires partagés : palette de couleurs / emojis par domaine, slugs, etc.

La palette est cohérente pour tous les niveaux du skill `programmes-officiels`.
"""

from __future__ import annotations

import colorsys
import json
import re
import unicodedata

# Couleur "base" + emoji représentatif pour chaque code domaine du skill.
# La couleur sert pour le bandeau du domaine ; les sous-domaines sont
# dégradés automatiquement via `shade_color`.
DOMAINE_INFO: dict[str, dict[str, str]] = {
    "NB":   {"label": "Nombres et calculs",                "color": "#a30f33", "emoji": "🔢"},
    "AL":   {"label": "Algèbre",                            "color": "#5d3d70", "emoji": "❎"},
    "AN":   {"label": "Analyse",                            "color": "#1e5b9c", "emoji": "∫"},
    "GEO":  {"label": "Géométrie",                          "color": "#57117a", "emoji": "🔷"},
    "GM":   {"label": "Grandeurs et mesures",               "color": "#c75c04", "emoji": "📏"},
    "STA":  {"label": "Statistiques",                       "color": "#2a6a48", "emoji": "📊"},
    "PR":   {"label": "Probabilités",                       "color": "#6da43e", "emoji": "🎲"},
    "OGD":  {"label": "Organisation et gestion de données", "color": "#007a8c", "emoji": "📋"},
    "ALGO": {"label": "Algorithmique et programmation",     "color": "#404040", "emoji": "💻"},
    "TRG":  {"label": "Trigonométrie",                      "color": "#006eb5", "emoji": "📐"},
    "LOG":  {"label": "Vocabulaire ensembliste et logique", "color": "#6e4b2f", "emoji": "🔀"},
}

AUTOMATISMES_INFO = {"label": "Automatismes", "color": "#444444", "emoji": "🛠"}


# ---------------------------------------------------------------------------
#  Grands domaines BO du collège (cycle 3 + cycle 4)
# ---------------------------------------------------------------------------
# Au collège, le BO n'organise PAS le programme avec la taxonomie fine du lycée
# (NB/AL/AN/GEO/STA/PR…). Les en-têtes de section réels du BO cycle 4 (vérifiés
# sur les pages source) sont les « grands domaines » ci-dessous. La fiche
# collège regroupe les objectifs sous ces intitulés exacts ; le lycée garde la
# taxonomie fine (DOMAINE_INFO).
COLLEGE_NIVEAUX = {"CM1", "CM2", "6E", "5E", "4E", "3E"}

# Ordre d'affichage + emoji + code couleur (réutilise une couleur DOMAINE_INFO
# existante pour rester compatible avec CONFIG.colors).
MACRO_INFO: dict[str, dict[str, str]] = {
    "Nombres et calculs":                                   {"emoji": "🔢", "color_code": "NB"},
    "Grandeurs et mesures":                                 {"emoji": "📏", "color_code": "GM"},
    "Espace et géométrie":                                  {"emoji": "🔷", "color_code": "GEO"},
    "Organisation et gestion de données et probabilités":   {"emoji": "📊", "color_code": "STA"},
    "Proportionnalité, fonctions":                          {"emoji": "📈", "color_code": "AN"},
    "Pensée informatique":                                  {"emoji": "💻", "color_code": "ALGO"},
}

# Cycle 3 (CM1/CM2/6E) et cycle 4 (5E/4E/3E) n'ont PAS les mêmes grands domaines :
# le cycle 3 a « Grandeurs et mesures » comme domaine propre (longueurs/aires/
# volumes/durées) et n'a ni « Proportionnalité, fonctions » (la proportionnalité
# y est sous Nombres et calculs). Ordre d'affichage par cycle :
MACRO_ORDER = [  # cycle 4
    "Nombres et calculs", "Espace et géométrie",
    "Organisation et gestion de données et probabilités",
    "Proportionnalité, fonctions", "Pensée informatique",
]
MACRO_ORDER_C3 = [  # cycle 3
    "Nombres et calculs", "Grandeurs et mesures", "Espace et géométrie",
    "Organisation et gestion de données et probabilités", "Pensée informatique",
]
CYCLE3_NIVEAUX = {"CM1", "CM2", "6E"}

# code domaine v2 -> grand domaine BO, CYCLE 4
CODE_TO_MACRO_C4: dict[str, str] = {
    "NB": "Nombres et calculs", "AL": "Nombres et calculs",
    "GEO": "Espace et géométrie", "GM": "Espace et géométrie", "TRG": "Espace et géométrie",
    "STA": "Organisation et gestion de données et probabilités",
    "PR": "Organisation et gestion de données et probabilités",
    "OGD": "Organisation et gestion de données et probabilités",
    "AN": "Proportionnalité, fonctions",
    "ALGO": "Pensée informatique", "LOG": "Pensée informatique",
}
# code domaine v2 -> grand domaine BO, CYCLE 3 (GM = domaine propre)
CODE_TO_MACRO_C3: dict[str, str] = {
    "NB": "Nombres et calculs", "AL": "Nombres et calculs",
    "GM": "Grandeurs et mesures",
    "GEO": "Espace et géométrie", "TRG": "Espace et géométrie",
    "STA": "Organisation et gestion de données et probabilités",
    "PR": "Organisation et gestion de données et probabilités",
    "OGD": "Organisation et gestion de données et probabilités",
    "ALGO": "Pensée informatique", "LOG": "Pensée informatique",
}
# Surcharge par sous-domaine (cycle 4 uniquement) : la proportionnalité est codée
# AL mais relève du grand domaine « Proportionnalité, fonctions ».
SOUS_OVERRIDE_C4: dict[str, str] = {"Proportionnalité": "Proportionnalité, fonctions"}


def macro_order_for(niveau: str) -> list[str]:
    return MACRO_ORDER_C3 if niveau in CYCLE3_NIVEAUX else MACRO_ORDER


def macro_for_college(domaine_code: str, sous_domaine: str, niveau: str) -> str:
    """Renvoie le grand domaine BO pour un (code, sous-domaine) selon le cycle."""
    if niveau in CYCLE3_NIVEAUX:
        return CODE_TO_MACRO_C3.get(domaine_code, "Nombres et calculs")
    if sous_domaine in SOUS_OVERRIDE_C4:
        return SOUS_OVERRIDE_C4[sous_domaine]
    return CODE_TO_MACRO_C4.get(domaine_code, "Nombres et calculs")


NIVEAU_LABEL: dict[str, str] = {
    "CM1": "CM1",
    "CM2": "CM2",
    "6E":  "Sixième",
    "5E":  "Cinquième",
    "4E":  "Quatrième",
    "3E":  "Troisième",
    "2GT": "Seconde générale et technologique",
    "1SPE": "Première spécialité maths",
    "1ENS": "Première — maths dans l'enseignement scientifique",
    "1TEC": "Première — voie technologique",
    "TSPE": "Terminale spécialité maths",
    "TCOMP": "Terminale maths complémentaires",
    "TTEC": "Terminale — voie technologique",
}


def hex_to_hsl(hex_color: str) -> tuple[float, float, float]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0
    hue, light, sat = colorsys.rgb_to_hls(r, g, b)
    return hue, sat, light


def hsl_to_hex(hue: float, sat: float, light: float) -> str:
    r, g, b = colorsys.hls_to_rgb(hue, light, sat)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def shade_color(base_hex: str, step: int) -> str:
    """Éclaircit progressivement la couleur de base.

    step=0 → couleur de base, step=1, 2, … → plus claire à chaque pas.
    """
    hue, sat, light = hex_to_hsl(base_hex)
    new_light = min(0.85, light + 0.08 * step)
    return hsl_to_hex(hue, sat, new_light)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "x"


def html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


# ---------------------------------------------------------------------------
#  Lecture du référentiel embarqué dans une fiche HTML (gabarit v2)
# ---------------------------------------------------------------------------
#
# Le gabarit v2 ne contient aucun objectif statique : la colonne gauche est
# construite en JS au chargement à partir de l'objet `DATA`, écrit par
# generate_vierge.py entre les marqueurs `/* __DATA_START__ */` et
# `/* __DATA_END__ */` sous la forme `let DATA = {...json...};`.
# Si la fiche a été réenregistrée depuis le navigateur (bouton « Enregistrer »),
# le snapshot embarqué peut contenir son propre `data` (référentiel importé),
# qui prime alors sur le DATA du code.

DATA_START = "/* __DATA_START__ */"
DATA_END = "/* __DATA_END__ */"
SNAPSHOT_RE = re.compile(
    r'(<!--\s*__SNAPSHOT_START__\s*-->\s*'
    r'<script type="application/json" id="__snapshot__">)'
    r'(?P<json>[\s\S]*?)'
    r'(</script>\s*<!--\s*__SNAPSHOT_END__\s*-->)'
)


def read_snapshot(html_text: str) -> dict | None:
    """Renvoie le snapshot embarqué (dict) ou None s'il est vide/absent."""
    m = SNAPSHOT_RE.search(html_text)
    if not m or not m.group("json").strip():
        return None
    return json.loads(m.group("json"))


def read_data(html_text: str) -> dict:
    """Renvoie le référentiel DATA de la fiche (snapshot prioritaire)."""
    snap = read_snapshot(html_text)
    if snap and isinstance(snap.get("data"), dict):
        return snap["data"]
    ds = html_text.find(DATA_START)
    de = html_text.find(DATA_END)
    if ds == -1 or de == -1:
        raise ValueError("Marqueurs __DATA_START__/__DATA_END__ introuvables : "
                         "ce n'est pas une fiche générée par generate_vierge.py.")
    block = html_text[ds + len(DATA_START):de].strip()
    block = re.sub(r"^let\s+DATA\s*=\s*", "", block).rstrip().rstrip(";")
    return json.loads(block)


def iter_data_items(data: dict):
    """Itère (thème, sous-thème, item) sur toutes les compétences de DATA."""
    for theme_name, theme_val in data.items():
        for sub_name, sub in (theme_val.get("themes") or {}).items():
            items = sub if isinstance(sub, list) else (sub.get("items") or [])
            for item in items:
                yield theme_name, sub_name, item


def codes_from_data(data: dict) -> set[str]:
    return {item["code"] for _, _, item in iter_data_items(data) if item.get("code")}
