#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare l'audit d'accessibilité d'une évaluation.

Entrée : un .pdf, un .tex (maître ou fragment), un .docx / .odt / .pptx.
Sortie, dans un dossier d'audit daté placé à côté de l'évaluation :
  - eval.pdf               copie du PDF analysé
  - pages/page-NN.png      rendu de chaque page (à regarder avant d'analyser)
  - mise_en_page.json      blocs de texte numérotés (p1-b3...) avec leur bbox,
                           pour localiser les zones des constats
  - mesures.json           police, corps, interligne, justification, zones côte
                           à côte, images : les faits objectifs de la mise en forme

Usage :
  python preparer_eval.py --source "chemin/eval.tex" [--compiler] [--sortie DOSSIER]
Affiche en dernière ligne le JSON {"dossier_audit": ..., ...}.
"""
import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF manquant : pip install pymupdf")

SKILL_DIR = Path(__file__).resolve().parent.parent
QUICK_COMPILE = SKILL_DIR.parent / "tex-compiling-skill" / "scripts" / "quick_compile.py"
SOFFICE_CANDIDATS = [
    "soffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
]


def trouver_maitre_tex(tex: Path) -> Path:
    """Un fragment (sans \\documentclass) est compilé via le maître qui l'inclut."""
    contenu = tex.read_text(encoding="utf-8", errors="replace")
    if "\\documentclass" in contenu:
        return tex
    motif = re.compile(r"\\(input|include|subfile)\{\s*(\./)?" + re.escape(tex.stem) + r"(\.tex)?\s*\}")
    for autre in sorted(tex.parent.glob("*.tex")):
        if autre == tex:
            continue
        txt = autre.read_text(encoding="utf-8", errors="replace")
        if "\\documentclass" in txt and motif.search(txt):
            return autre
    return tex


def pdf_depuis_tex(tex: Path, compiler: bool) -> Path:
    maitre = trouver_maitre_tex(tex)
    pdf = maitre.with_suffix(".pdf")
    sources = [tex, maitre] + list(maitre.parent.glob("*.tex"))
    plus_recent = max(p.stat().st_mtime for p in sources if p.exists())
    perime = (not pdf.exists()) or pdf.stat().st_mtime < plus_recent
    if perime and compiler:
        print(f"Compilation de {maitre.name}...")
        subprocess.run([sys.executable, str(QUICK_COMPILE), "--file", str(maitre), "--passes", "2"],
                       timeout=600, check=False)
    if not pdf.exists():
        sys.exit(f"Aucun PDF pour {maitre} : relancer avec --compiler.")
    if pdf.stat().st_mtime < plus_recent:
        print(f"ATTENTION : {pdf.name} est plus ancien que les sources .tex "
              f"(relancer avec --compiler pour analyser la version à jour).")
    return pdf


def pdf_depuis_bureautique(doc: Path, tmp: Path) -> Path:
    soffice = next((c for c in SOFFICE_CANDIDATS if shutil.which(c) or Path(c).exists()), None)
    if not soffice:
        sys.exit("LibreOffice introuvable : exporter le document en PDF puis relancer sur le PDF.")
    tmp.mkdir(parents=True, exist_ok=True)
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(doc)],
                   timeout=180, check=False)
    pdf = tmp / (doc.stem + ".pdf")
    if not pdf.exists():
        sys.exit("La conversion LibreOffice a échoué.")
    return pdf


def nom_police(font: str) -> str:
    """'ABCDEF+LMSans10-Regular' -> 'LMSans10-Regular'."""
    return font.split("+", 1)[1] if "+" in font[:8] else font


def analyser_page(page, num):
    d = page.get_text("dict")
    blocs, lignes_pas, tailles = [], [], {}
    polices = {}
    justif_lignes = justif_total = 0
    for b in d["blocks"]:
        if b.get("type") != 0:
            continue
        lignes = b.get("lines", [])
        texte = ["".join(s["text"] for s in ln["spans"]) for ln in lignes]
        contenu = " ".join(t.strip() for t in texte if t.strip())
        if not contenu:
            continue
        # texte « ombré » (même texte répété à quelques dixièmes de point) : un seul bloc
        if any(abs(o["bbox"][0] - b["bbox"][0]) < 3 and abs(o["bbox"][1] - b["bbox"][1]) < 3
               and (o["texte"] in contenu or contenu in o["texte"]) for o in blocs):
            continue
        spans_tailles = []
        for ln in lignes:
            for s in ln["spans"]:
                n = len(s["text"].strip())
                if not n:
                    continue
                tz = round(s["size"], 1)
                tailles[tz] = tailles.get(tz, 0) + n
                p = nom_police(s["font"])
                polices[p] = polices.get(p, 0) + n
                spans_tailles.append(s["size"])
        # interligne : écart entre lignes successives d'un même bloc / corps
        for a, c in zip(lignes, lignes[1:]):
            if not a["spans"] or not c["spans"]:
                continue
            corps = max(s["size"] for s in a["spans"])
            ecart = c["bbox"][1] - a["bbox"][1]
            if corps > 4 and 0.8 * corps < ecart < 3 * corps and abs(c["bbox"][0] - a["bbox"][0]) < 40:
                lignes_pas.append(ecart / corps)
        # justification : lignes non finales qui butent toutes sur le bord droit du bloc
        if len(lignes) >= 3:
            x1max = max(l["bbox"][2] for l in lignes)
            for l in lignes[:-1]:
                justif_total += 1
                if x1max - l["bbox"][2] < 1.5:
                    justif_lignes += 1
        blocs.append({
            "id": f"p{num}-b{len(blocs) + 1}",
            "bbox": [round(v, 1) for v in b["bbox"]],
            "corps": round(statistics.median(spans_tailles), 1) if spans_tailles else None,
            "texte": contenu[:400],
        })
    # zones côte à côte : blocs qui se recouvrent verticalement mais pas horizontalement
    cote = []
    for ia, a in enumerate(blocs):
        for c in blocs[ia + 1:]:
            ay0, ay1 = a["bbox"][1], a["bbox"][3]
            cy0, cy1 = c["bbox"][1], c["bbox"][3]
            recouvre = min(ay1, cy1) - max(ay0, cy0)
            if recouvre > 12 and (a["bbox"][2] < c["bbox"][0] - 8 or c["bbox"][2] < a["bbox"][0] - 8):
                cote.append([a["id"], c["id"]])
    images = len(page.get_images(full=True))
    dessins = len(page.get_drawings())
    return blocs, lignes_pas, tailles, polices, (justif_lignes, justif_total), cote, images, dessins


def main():
    ap = argparse.ArgumentParser(description="Préparer l'audit d'accessibilité d'une évaluation")
    ap.add_argument("--source", required=True, help="Évaluation : .pdf, .tex, .docx, .odt, .pptx")
    ap.add_argument("--compiler", action="store_true", help="Compiler le .tex si le PDF manque ou est périmé")
    ap.add_argument("--sortie", help="Dossier d'audit (défaut : <dossier de l'éval>/audit_accessibilite/<date>)")
    ap.add_argument("--dpi", type=int, default=110, help="Résolution des aperçus de pages (défaut 110)")
    ap.add_argument("--pages", help="Pages de l'énoncé, ex. '1-2' ou '1,3' (défaut : avant le corrigé)")
    args = ap.parse_args()

    src = Path(args.source).resolve()
    if not src.exists():
        sys.exit(f"Introuvable : {src}")
    horodatage = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    sortie = Path(args.sortie).resolve() if args.sortie else src.parent / "audit_accessibilite" / horodatage
    sortie.mkdir(parents=True, exist_ok=True)

    ext = src.suffix.lower()
    if ext == ".pdf":
        pdf = src
    elif ext == ".tex":
        pdf = pdf_depuis_tex(src, args.compiler)
    elif ext in (".docx", ".doc", ".odt", ".pptx", ".ppt", ".odp", ".rtf"):
        pdf = pdf_depuis_bureautique(src, sortie / "_conversion")
    else:
        sys.exit(f"Format non pris en charge : {ext}")

    shutil.copy2(pdf, sortie / "eval.pdf")
    doc = fitz.open(sortie / "eval.pdf")
    (sortie / "pages").mkdir(exist_ok=True)

    # pages de l'énoncé : --pages, sinon tout ce qui précède la première page de corrigé
    if args.pages:
        enonce = set()
        for morceau in args.pages.split(","):
            if "-" in morceau:
                x, y = morceau.split("-")
                enonce.update(range(int(x), int(y) + 1))
            else:
                enonce.add(int(morceau))
    else:
        enonce, dans_corrige = set(), False
        motif_corrige = re.compile(r"\b(Solutions?|Corrigé|Correction|Éléments de correction)\b", re.I)
        for i, page in enumerate(doc, start=1):
            if motif_corrige.search(page.get_text()[:400]):
                dans_corrige = True
            if not dans_corrige:
                enonce.add(i)
        if not enonce:
            enonce = set(range(1, len(doc) + 1))

    pages_info, tous_pas, toutes_tailles, toutes_polices = [], [], {}, {}
    jl = jt = 0
    for i, page in enumerate(doc, start=1):
        page.get_pixmap(dpi=args.dpi).save(str(sortie / "pages" / f"page-{i:02d}.png"))
        blocs, pas, tailles, polices, (a, b), cote, imgs, dess = analyser_page(page, i)
        pages_info.append({
            "page": i,
            "role": "enonce" if i in enonce else "corrige",
            "largeur_pt": round(page.rect.width, 1),
            "hauteur_pt": round(page.rect.height, 1),
            "image": f"pages/page-{i:02d}.png",
            "blocs": blocs,
            "zones_cote_a_cote": cote,
            "images_raster": imgs,
            "traces_vectoriels": dess,
            "debut_texte": " ".join(bl["texte"] for bl in blocs)[:300],
        })
        if i not in enonce:
            continue  # les mesures ne portent que sur ce que lit l'élève
        tous_pas += pas
        jl += a
        jt += b
        for k, v in tailles.items():
            toutes_tailles[k] = toutes_tailles.get(k, 0) + v
        for k, v in polices.items():
            toutes_polices[k] = toutes_polices.get(k, 0) + v

    total = sum(toutes_tailles.values()) or 1
    corps_dominant = max(toutes_tailles, key=toutes_tailles.get) if toutes_tailles else None
    petits = sum(v for k, v in toutes_tailles.items() if k < 10) / total
    police_dom = max(toutes_polices, key=toutes_polices.get) if toutes_polices else None
    interligne = round(statistics.median(tous_pas), 2) if tous_pas else None
    mesures = {
        "fichier_source": str(src),
        "fichier_pdf": str(pdf),
        "nb_pages": len(doc),
        "pages_enonce": sorted(enonce),
        "pages_corrige": [p for p in range(1, len(doc) + 1) if p not in enonce],
        "police_dominante": police_dom,
        "polices": dict(sorted(toutes_polices.items(), key=lambda kv: -kv[1])[:6]),
        "corps_dominant_pt": corps_dominant,
        "part_texte_corps_inferieur_10pt": round(petits, 3),
        "repartition_corps_pt": dict(sorted(toutes_tailles.items())),
        "interligne_median": interligne,
        "part_lignes_justifiees": round(jl / jt, 2) if jt else None,
        "recommandation_grille": "Police Arial (sans empattement), corps 12 ou 14, interligne 1,3 à 1,5 [GRILLE]",
        "remarque_interligne": ("Rapport entre l'écart de deux lignes successives et le corps : "
                                "LaTeX standard ≈ 1,2 ; Word interligne simple ≈ 1,15-1,2."),
        "zones_cote_a_cote_par_page": {str(p["page"]): len(p["zones_cote_a_cote"])
                                       for p in pages_info if p["role"] == "enonce"},
    }
    (sortie / "mise_en_page.json").write_text(
        json.dumps({"pages": pages_info}, ensure_ascii=False, indent=1), encoding="utf-8")
    (sortie / "mesures.json").write_text(json.dumps(mesures, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{len(doc)} page(s) rendue(s) dans {sortie / 'pages'}")
    print(f"Police dominante : {police_dom} · corps {corps_dominant} pt · interligne médian {interligne}")
    print(f"Pages d'énoncé (mesurées) : {sorted(enonce)} — corriger avec --pages si la détection se trompe")
    for p in pages_info:
        print(f"  page {p['page']} [{p['role']}] : {p['debut_texte'][:100]}")
    print(json.dumps({"dossier_audit": str(sortie), "pdf": str(pdf), "nb_pages": len(doc)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
