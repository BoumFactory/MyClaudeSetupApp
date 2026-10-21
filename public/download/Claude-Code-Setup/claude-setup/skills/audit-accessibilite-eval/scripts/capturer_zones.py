#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produit les captures d'écran des zones problématiques (PyMuPDF + Pillow).

Lit <dossier_audit>/constats.json et eval.pdf, puis écrit :
  - captures/<ID>-p<N>.png       extrait de page centré sur la zone, zone surlignée
  - captures/apercu-page-NN.png  page entière avec tous les constats numérotés
  - captures.json                correspondance constat -> fichiers, et erreurs

Chaque constat porte une liste « zones ». Une zone se localise de trois façons,
dans cet ordre de préférence :
  {"page": 1, "ancre": "Recopier et compléter le tableau"}
        texte cherché mot à mot (insensible à la casse, aux ligatures, à la
        ponctuation) ; « ancre_fin » étend la zone jusqu'à la fin d'un second
        texte ; « occurrence » (1 par défaut) choisit la n-ième apparition.
  {"page": 1, "bloc": "p1-b35"}  ou  {"page": 1, "bloc": ["p1-b35", "p1-b36"]}
        identifiants de blocs de mise_en_page.json
  {"page": 1, "bbox": [x0, y0, x1, y1]}
        rectangle en points PDF (origine en haut à gauche)
« marge » (points, défaut 4) élargit le surlignage ; « cadre »: true remplace le
surlignage ligne à ligne par un seul rectangle englobant (exercice entier, tableau).

Usage :
  python capturer_zones.py --dossier "<dossier_audit>"
Code de sortie 2 si une zone n'a pas été trouvée (corriger l'ancre et relancer).
"""
import argparse
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

COULEURS = {  # gravité -> (contour, remplissage RGBA)
    "bloquant": ((200, 30, 30), (220, 38, 38, 46)),
    "important": ((214, 110, 0), (234, 140, 20, 46)),
    "confort": ((30, 100, 200), (40, 120, 220, 40)),
}
ZOOM = 2.2          # ≈ 160 dpi pour les extraits
ZOOM_APERCU = 1.1   # aperçu de page entière
CONTEXTE_V = 26     # points de contexte au-dessus et au-dessous de la zone


def police(taille):
    for nom in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(nom, taille)
        except OSError:
            continue
    return ImageFont.load_default()


def norm(s):
    s = unicodedata.normalize("NFKC", s).casefold().replace("’", "'")
    return re.sub(r"[^\w']+", "", s)


def jetons(texte):
    return [t for t in (norm(m) for m in texte.split()) if t]


def chercher(mots, ancre, occurrence=1):
    """Renvoie (i_debut, i_fin) dans la liste des mots de la page, ou None."""
    cibles = jetons(ancre)
    if not cibles:
        return None
    toks = [norm(w[4]) for w in mots]
    idx = [i for i, t in enumerate(toks) if t]
    n = len(cibles)
    vus = 0
    for k in range(len(idx) - n + 1):
        fen = [toks[idx[k + j]] for j in range(n)]
        ok = all(
            (fen[j] == c) or (j == 0 and fen[j].endswith(c)) or (j == n - 1 and fen[j].startswith(c))
            or (n == 1 and c in fen[j])
            for j, c in enumerate(cibles)
        )
        if ok:
            vus += 1
            if vus == occurrence:
                return idx[k], idx[k + n - 1]
    return None


def rects_mots(mots, i0, i1):
    """Un rectangle par ligne : un surlignage qui épouse le texte."""
    lignes = {}
    for w in mots[i0:i1 + 1]:
        cle = (w[5], w[6])  # bloc, ligne
        r = fitz.Rect(w[:4])
        lignes[cle] = lignes[cle] | r if cle in lignes else r
    return list(lignes.values())


def localiser(zone, page, mots, blocs_par_id):
    if zone.get("bbox"):
        return [fitz.Rect(zone["bbox"])], None
    if zone.get("bloc"):
        ids = zone["bloc"] if isinstance(zone["bloc"], list) else [zone["bloc"]]
        manquants = [i for i in ids if i not in blocs_par_id]
        if manquants:
            return [], f"bloc(s) inconnu(s) : {manquants}"
        return [fitz.Rect(blocs_par_id[i]) for i in ids], None
    if zone.get("ancre"):
        trouve = chercher(mots, zone["ancre"], zone.get("occurrence", 1))
        if not trouve:
            return [], f"ancre introuvable : « {zone['ancre']} »"
        i0, i1 = trouve
        if zone.get("ancre_fin"):
            fin = chercher(mots[i0:], zone["ancre_fin"])
            if not fin:
                return [], f"ancre_fin introuvable après l'ancre : « {zone['ancre_fin']} »"
            i1 = i0 + fin[1]
        return rects_mots(mots, i0, i1), None
    return [], "zone sans ancre, bloc ni bbox"


def rendre(page, zoom):
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")


def chevauche(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def surligner(img, rects, zoom, gravite, etiquette=None, epaisseur=3, occupes=None):
    """occupes : liste partagée des étiquettes déjà posées sur l'image, pour les décaler."""
    contour, fond = COULEURS.get(gravite, COULEURS["important"])
    calque = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(calque)
    for r in rects:
        box = [r.x0 * zoom, r.y0 * zoom, r.x1 * zoom, r.y1 * zoom]
        dr.rounded_rectangle(box, radius=int(3 * zoom), fill=fond, outline=contour + (255,), width=epaisseur)
    if etiquette and rects:
        r0 = min(rects, key=lambda r: (r.y0, r.x0))
        taille = int(9 * zoom)
        f = police(taille)
        pad = int(2.5 * zoom)
        tw = dr.textlength(etiquette, font=f)
        h = taille + 2 * pad
        x, y = r0.x0 * zoom, r0.y0 * zoom - h - 2
        if y < 0:
            y = r0.y1 * zoom + 2
        if occupes is not None:
            w = tw + 2 * pad
            essais = 0
            while any(chevauche((x, y, x + w, y + h), o) for o in occupes) and essais < 30:
                x += w + 3
                if x + w > img.width:
                    x, y = r0.x0 * zoom, y - h - 2
                essais += 1
            occupes.append((x, y, x + w, y + h))
        dr.rounded_rectangle([x, y, x + tw + 2 * pad, y + h], radius=pad, fill=contour + (255,))
        dr.text((x + pad, y + pad * 0.6), etiquette, fill=(255, 255, 255, 255), font=f)
    return Image.alpha_composite(img, calque)


def main():
    ap = argparse.ArgumentParser(description="Captures des zones problématiques d'une évaluation")
    ap.add_argument("--dossier", required=True, help="Dossier d'audit (contient eval.pdf et constats.json)")
    args = ap.parse_args()

    dossier = Path(args.dossier)
    data = json.loads((dossier / "constats.json").read_text(encoding="utf-8"))
    doc = fitz.open(dossier / "eval.pdf")
    mep = json.loads((dossier / "mise_en_page.json").read_text(encoding="utf-8"))
    blocs_par_id = {b["id"]: b["bbox"] for p in mep["pages"] for b in p["blocs"]}
    cap = dossier / "captures"
    cap.mkdir(exist_ok=True)

    mots_cache, rendus = {}, {}
    sortie = {"constats": {}, "apercus": {}, "erreurs": []}
    par_page = {}  # page -> [(id, gravite, rects)]

    for c in data.get("constats", []):
        cid, grav = c["id"], c.get("gravite", "important")
        zones_par_page = {}
        for z in c.get("zones", []):
            num = int(z.get("page", 1))
            if not 1 <= num <= len(doc):
                sortie["erreurs"].append(f"{cid} : page {num} inexistante")
                continue
            page = doc[num - 1]
            if num not in mots_cache:
                mots_cache[num] = page.get_text("words")
            rects, err = localiser(z, page, mots_cache[num], blocs_par_id)
            if err:
                sortie["erreurs"].append(f"{cid} (page {num}) : {err}")
                continue
            if z.get("cadre") and len(rects) > 1:  # un seul rectangle englobant
                u = rects[0]
                for r in rects[1:]:
                    u |= r
                rects = [u]
            m = z.get("marge", 4)
            zones_par_page.setdefault(num, []).extend(fitz.Rect(r.x0 - m, r.y0 - m, r.x1 + m, r.y1 + m) for r in rects)
        fichiers = []
        for num, rects in sorted(zones_par_page.items()):
            page = doc[num - 1]
            par_page.setdefault(num, []).append((cid, grav, rects))
            if num not in rendus:
                rendus[num] = rendre(page, ZOOM)
            img = surligner(rendus[num], rects, ZOOM, grav, etiquette=cid)
            # cadrage : largeur du texte de la page, hauteur de la zone + contexte
            union = rects[0]
            for r in rects[1:]:
                union |= r
            blocs_page = [fitz.Rect(b["bbox"]) for p in mep["pages"] if p["page"] == num for b in p["blocs"]]
            x0 = min([b.x0 for b in blocs_page] + [union.x0]) - 10
            x1 = max([b.x1 for b in blocs_page] + [union.x1]) + 10
            y0 = union.y0 - CONTEXTE_V - 14
            y1 = union.y1 + CONTEXTE_V
            cadre = fitz.Rect(max(0, x0), max(0, y0), min(page.rect.x1, x1), min(page.rect.y1, y1))
            extrait = img.crop(tuple(int(v * ZOOM) for v in cadre)).convert("RGB")
            nom = f"{cid}-p{num}.png"
            extrait.save(cap / nom, optimize=True)
            fichiers.append({"page": num, "fichier": f"captures/{nom}",
                             "largeur": extrait.width, "hauteur": extrait.height})
        sortie["constats"][cid] = fichiers

    # deux constats sur la même zone : cadres superposés et étiquettes masquées
    alertes = []
    for num, items in par_page.items():
        for i, (ca, _, ra) in enumerate(items):
            for cb, _, rb in items[i + 1:]:
                for a in ra:
                    for b in rb:
                        inter = a & b
                        if inter.is_empty:
                            continue
                        union = a.get_area() + b.get_area() - inter.get_area() or 1
                        if inter.get_area() / union > 0.6:  # zones quasi identiques (pas une simple inclusion)
                            alertes.append(f"page {num} : {ca} et {cb} surlignent presque la même zone "
                                           "(cibler la phrase propre à chaque constat)")
                            break
                    else:
                        continue
                    break
    sortie["alertes"] = sorted(set(alertes))

    for num, items in sorted(par_page.items()):
        img = rendre(doc[num - 1], ZOOM_APERCU)
        occupes = []
        for cid, grav, rects in items:
            img = surligner(img, rects, ZOOM_APERCU, grav, etiquette=cid, epaisseur=2, occupes=occupes)
        nom = f"apercu-page-{num:02d}.png"
        img.convert("RGB").save(cap / nom, optimize=True)
        sortie["apercus"][str(num)] = f"captures/{nom}"

    (dossier / "captures.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(v) for v in sortie["constats"].values())
    print(f"{n} capture(s) et {len(sortie['apercus'])} aperçu(s) de page dans {cap}")
    sans = [k for k, v in sortie["constats"].items() if not v]
    if sans:
        print(f"Constats sans capture (normal s'ils portent sur tout le sujet) : {', '.join(sans)}")
    for a in sortie["alertes"]:
        print("alerte : " + a)
    if sortie["erreurs"]:
        print("ZONES NON TROUVÉES — corriger constats.json puis relancer :")
        for e in sortie["erreurs"]:
            print("  - " + e)
        sys.exit(2)


if __name__ == "__main__":
    main()
