"""Reconstruit mécaniquement les automatismes 5e (Anti-régurgitation : texte verbatim issu d'un
script Python, jamais retapé par le LLM).

Source texte : Liste-des-automatismes-5e.pdf (doc officiel, texte propre, fractions
intactes, complet — contient les probabilités absentes de l'extraction cycle4).
Sous-domaines & pages source : alignés sur le BO cycle4.pdf (vérifiés visuellement
sur les screenshots des pages 7,8,12,13,16,18).

Sortie : data/_tmp/automatismes_5e_clean.json  (à fusionner ensuite dans 5E.json).
"""
from __future__ import annotations

import json
from pathlib import Path

import fitz  # PyMuPDF

LISTE_PDF = Path(__file__).resolve().parents[2] / "data" / "annexes" / "Liste-des-automatismes-5e.pdf"
OUT = Path(__file__).resolve().parents[1] / "data" / "_tmp" / "automatismes_5e_clean.json"

TRIGGER = "Les automatismes mentionnés dans le programme pour la classe de cinquième"
BULLET = "−"   # −
SUBBUL = "•"   # •

# Sous-domaine -> grand domaine BO (libellés exacts, validés par l'utilisateur)
SOUS_TO_MACRO = {
    "Opérations": "Nombres et calculs",
    "Nombres relatifs": "Nombres et calculs",
    "Nombres rationnels": "Nombres et calculs",
    "Puissances": "Nombres et calculs",
    "Calcul littéral et algébrique": "Nombres et calculs",
    "Repérage sur une droite et dans le plan": "Espace et géométrie",
    "Représentation de l’espace": "Espace et géométrie",
    "Transformations": "Espace et géométrie",
    "Angles": "Espace et géométrie",
    "Triangles": "Espace et géométrie",
    "Parallélogrammes": "Espace et géométrie",
    "Statistiques": "Organisation et gestion de données et probabilités",
    "Probabilités": "Organisation et gestion de données et probabilités",
    "Proportionnalité": "Proportionnalité, fonctions",
    "Fonctions": "Proportionnalité, fonctions",
    "La pensée informatique": "Pensée informatique",
}

# Sous-domaine -> code domaine v2 (inchangé pour stabilité des codes)
SOUS_TO_DOMAINE = {
    "Opérations": "NB", "Nombres relatifs": "NB", "Nombres rationnels": "NB",
    "Puissances": "NB", "Calcul littéral et algébrique": "AL",
    "Repérage sur une droite et dans le plan": "GEO", "Représentation de l’espace": "GEO",
    "Transformations": "GEO", "Angles": "GEO", "Triangles": "GEO",
    "Parallélogrammes": "GEO", "Statistiques": "STA", "Probabilités": "PR",
    "Proportionnalité": "AL",
}

# Sous-domaine -> page du BO cycle4.pdf (vérifié visuellement sur les PNG)
SOUS_TO_PAGE = {
    "Opérations": 7, "Nombres relatifs": 7, "Nombres rationnels": 8, "Puissances": 8,
    "Calcul littéral et algébrique": 8, "Repérage sur une droite et dans le plan": 12,
    "Représentation de l’espace": 12, "Transformations": 12, "Angles": 13,
    "Triangles": 13, "Parallélogrammes": 13, "Probabilités": 16, "Proportionnalité": 18,
}


def parse_liste() -> list[dict]:
    doc = fitz.open(LISTE_PDF)
    lines: list[tuple[bool, str]] = []  # (is_bold, text)
    for pno in range(doc.page_count):
        d = doc[pno].get_text("dict")
        for block in d["blocks"]:
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                txt = "".join(s["text"] for s in spans).strip()
                if not txt:
                    continue
                s0 = spans[0]
                is_bold = bool(s0["flags"] & 16) or "Bold" in s0["font"]
                if s0["size"] > 12:  # titre principal
                    continue
                lines.append((is_bold, txt))
    doc.close()

    autos: list[dict] = []
    started = False
    sous = None
    nr_count = 0  # compteur d'occurrences "Nombres rationnels" (2e -> Puissances)
    for is_bold, txt in lines:
        if not started:
            if txt.startswith(TRIGGER):
                started = True
            continue
        if is_bold:
            # En-tête de section
            for sep in (" – ", " - ", " — "):
                if sep in txt:
                    sous = txt.split(sep, 1)[1].strip()
                    break
            else:
                sous = txt.strip()
            if sous == "Nombres rationnels":
                nr_count += 1
                if nr_count == 2:
                    sous = "Puissances"  # override BO cycle4 (vérifié p.8)
            continue
        # Ligne de contenu
        stripped = txt.lstrip()
        if stripped.startswith(BULLET):
            autos.append({"sous_domaine": sous,
                          "text": stripped[len(BULLET):].strip()})
        elif stripped.startswith(SUBBUL):
            # sous-puce -> repliée dans l'automatisme courant
            if autos:
                autos[-1]["text"] += " " + stripped[len(SUBBUL):].strip()
        else:
            # continuation (wrap-text) -> repliée
            if autos:
                autos[-1]["text"] += " " + stripped
    return autos


def main() -> int:
    autos = parse_liste()
    detailed = []
    for a in autos:
        sd = a["sous_domaine"]
        detailed.append({
            "text": a["text"],
            "sous_domaine": sd,
            "domaine": SOUS_TO_DOMAINE.get(sd, "NB"),
            "grand_domaine": SOUS_TO_MACRO.get(sd, ""),
            "source": {
                "pdf": "cycle4.pdf",
                "page": SOUS_TO_PAGE.get(sd, 0),
                "bo_reference": "BO n°10 du 5 mars 2026",
                "bo_url": "https://www.education.gouv.fr/bo/2026/Hebdo10",
                "page_image": f"../pages/cycle4/page_{SOUS_TO_PAGE.get(sd, 0):03d}.png",
            },
            "extraction_method": "mechanical_from_liste_pdf_xref_cycle4",
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(detailed, ensure_ascii=False, indent=2), encoding="utf-8")

    # Résumé
    from collections import Counter
    by_sd = Counter(a["sous_domaine"] for a in detailed)
    print(f"[OK] {len(detailed)} automatismes -> {OUT}")
    for sd, n in by_sd.items():
        print(f"  {n:>2}  {SOUS_TO_MACRO.get(sd,''):<45} | {sd}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
