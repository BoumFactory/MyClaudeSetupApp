#!/usr/bin/env python
"""Convertit une manche de questions Markdown en page HTML interactive.

Usage :
    python manche_html.py manche-01.md [--sortie fichier.html] [--pas-ouvrir]

Le format d'entrée est décrit dans references/format-manche.md.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

PORT = int(os.environ.get("GRILL_ME_PORT", "47821"))
DOSSIER_PAGES = Path(tempfile.gettempdir()) / "grill-me-pages"
SERVEUR = Path(__file__).resolve().parent / "serveur_pages.py"
RACINE_SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = RACINE_SKILL / "assets" / "template.html"
MARQUEUR = re.compile(r"/\*__DONNEES__\*/\s*\{\}")

TYPES = ("unique", "multiple", "libre")


class ErreurFormat(Exception):
    def __init__(self, message, ligne=None):
        self.ligne = ligne
        super().__init__(message)


def lire_front_matter(lignes):
    """Retourne (meta, indice de la première ligne après le front-matter)."""
    i = 0
    while i < len(lignes) and not lignes[i].strip():
        i += 1
    if i >= len(lignes) or lignes[i].strip() != "---":
        return {}, 0
    meta = {}
    j = i + 1
    while j < len(lignes) and lignes[j].strip() != "---":
        m = re.match(r"^\s*([A-Za-zÀ-ÿ_]+)\s*:\s*(.*)$", lignes[j])
        if m:
            meta[m.group(1).lower()] = m.group(2).strip()
        elif lignes[j].strip():
            raise ErreurFormat("ligne de front-matter invalide (attendu « clé: valeur »)", j + 1)
        j += 1
    if j >= len(lignes):
        raise ErreurFormat("front-matter non fermé (second « --- » manquant)", i + 1)
    return meta, j + 1


def nettoyer_titre(texte):
    return re.sub(r"^\s*Q?\d+\s*[—–:.\-]\s*", "", texte).strip()


def analyser_option(ligne, numero):
    texte = ligne[2:].strip()
    reco = False
    m = re.match(r"^\[reco\]\s*", texte, re.IGNORECASE)
    if m:
        reco = True
        texte = texte[m.end():]
    if not texte:
        raise ErreurFormat("option vide", numero)
    if " : " in texte:
        label, desc = texte.split(" : ", 1)
    else:
        label, desc = texte, ""
    return {"label": label.strip(), "desc": desc.strip(), "reco": reco}


def analyser_question(titre_brut, lignes, numeros, rang):
    """lignes : lignes du bloc (sans l'en-tête) ; numeros : numéros de ligne du fichier."""
    n_ligne_titre = numeros[0] - 1 if numeros else None
    titre = nettoyer_titre(titre_brut)
    if not titre:
        raise ErreurFormat(f"question {rang} sans titre", n_ligne_titre)

    type_ = None
    reco_txt = None
    reste = []  # couples (numero, texte)
    i = 0
    n = len(lignes)
    en_code = False
    while i < n:
        l, num = lignes[i], numeros[i]
        if l.strip().startswith("```"):
            en_code = not en_code
        if not en_code:
            m = re.match(r"^type\s*:\s*(\S+)\s*$", l, re.IGNORECASE)
            if m and type_ is None:
                type_ = m.group(1).lower()
                if type_ not in TYPES:
                    raise ErreurFormat(
                        f"type inconnu « {type_} » (attendu : unique, multiple ou libre)", num)
                i += 1
                continue
            m = re.match(r"^reco\s*:\s*(.*)$", l, re.IGNORECASE)
            if m and reco_txt is None:
                morceaux = [m.group(1).strip()]
                i += 1
                while i < n and lignes[i].strip() and not lignes[i].startswith("- "):
                    morceaux.append(lignes[i].strip())
                    i += 1
                reco_txt = " ".join(x for x in morceaux if x)
                continue
        reste.append((num, l))
        i += 1

    # Dernière liste à puces contiguë : options, si rien d'autre ne la suit.
    options = []
    corps_lignes = reste
    if type_ != "libre":
        fin = len(reste)
        while fin > 0 and not reste[fin - 1][1].strip():
            fin -= 1
        debut = fin
        while debut > 0 and reste[debut - 1][1].startswith("- "):
            debut -= 1
        if debut < fin:
            options = [analyser_option(l, num) for num, l in reste[debut:fin]]
            corps_lignes = reste[:debut]

    if type_ is None:
        type_ = "unique" if options else "libre"
    if type_ in ("unique", "multiple") and not options:
        raise ErreurFormat(
            f"question « {titre} » de type {type_} sans options "
            "(la dernière liste à puces du bloc doit contenir les options)", n_ligne_titre)
    if type_ == "libre" and options:
        raise ErreurFormat(f"question « {titre} » de type libre ne doit pas avoir d'options",
                           n_ligne_titre)
    nb_reco = sum(1 for o in options if o["reco"])
    if type_ == "unique" and nb_reco > 1:
        raise ErreurFormat(f"question « {titre} » : plusieurs [reco] pour un type unique",
                           n_ligne_titre)

    corps = "\n".join(l for _, l in corps_lignes).strip("\n").rstrip()
    return {
        "id": rang,
        "titre": titre,
        "type": type_,
        "corps": corps,
        "reco": reco_txt or "",
        "options": options,
    }


def analyser(texte, nom_defaut):
    lignes = texte.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lignes and lignes[0].startswith("\ufeff"):
        lignes[0] = lignes[0][1:]
    meta, debut = lire_front_matter(lignes)

    blocs = []  # (titre, lignes, numeros)
    courant = None
    en_code = False
    for idx in range(debut, len(lignes)):
        l = lignes[idx]
        if l.strip().startswith("```"):
            en_code = not en_code
        if not en_code and re.match(r"^##\s+\S", l):
            courant = (l[2:].strip(), [], [])
            blocs.append(courant)
        elif courant is not None:
            courant[1].append(l)
            courant[2].append(idx + 1)
        elif l.strip():
            raise ErreurFormat("contenu avant la première question (« ## Q1 — … » attendu)", idx + 1)

    if not blocs:
        raise ErreurFormat("aucune question trouvée (titres « ## Q1 — … » attendus)")

    questions = [analyser_question(t, ls, ns, k + 1) for k, (t, ls, ns) in enumerate(blocs)]
    return {
        "titre": meta.get("titre") or nom_defaut,
        "contexte": meta.get("contexte", ""),
        "questions": questions,
    }


def produire_html(donnees):
    if not TEMPLATE.exists():
        raise ErreurFormat(f"template introuvable : {TEMPLATE}")
    modele = TEMPLATE.read_text(encoding="utf-8")
    if not MARQUEUR.search(modele):
        raise ErreurFormat("marqueur /*__DONNEES__*/{} absent du template")
    js = json.dumps(donnees, ensure_ascii=False).replace("</", "<\\/")
    js = js.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    sortie = MARQUEUR.sub(lambda _m: js, modele, count=1)
    return sortie.replace("__TITRE__", html.escape(donnees["titre"]))


def serveur_actif():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/__ping", timeout=0.5) as r:
            return r.read(32).decode("utf-8", "replace").strip() == "grill-me"
    except Exception:
        return False


def lancer_serveur():
    """Lance serveur_pages.py détaché ; True s'il répond sous 3 s."""
    drapeaux = 0
    if sys.platform == "win32":
        drapeaux = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    try:
        subprocess.Popen([sys.executable, str(SERVEUR)], stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=drapeaux, close_fds=True)
    except OSError:
        return False
    fin = time.time() + 3
    while time.time() < fin:
        if serveur_actif():
            return True
        time.sleep(0.1)
    return False


def main():
    p = argparse.ArgumentParser(description="Manche Markdown -> page HTML interactive")
    p.add_argument("entree", help="fichier .md de la manche")
    p.add_argument("--sortie", help="chemin du HTML produit (défaut : à côté du .md)")
    p.add_argument("--pas-ouvrir", action="store_true", help="ne pas ouvrir le navigateur")
    p.add_argument("--fichier-local", action="store_true",
                   help="ouvrir en file:// au lieu du serveur local (micro redemandé à chaque fois)")
    a = p.parse_args()

    entree = Path(a.entree)
    try:
        texte = entree.read_text(encoding="utf-8")
    except OSError as e:
        print(f"Erreur : lecture impossible de {entree} ({e})", file=sys.stderr)
        return 1

    try:
        donnees = analyser(texte, entree.stem)
        page = produire_html(donnees)
    except ErreurFormat as e:
        loc = f" (ligne {e.ligne})" if e.ligne else ""
        print(f"Erreur de format{loc} : {e}", file=sys.stderr)
        return 1

    sortie = Path(a.sortie) if a.sortie else entree.with_suffix(".html")
    sortie.write_text(page, encoding="utf-8")
    sortie = sortie.resolve()
    print(sortie)

    url = None
    if not a.fichier_local:
        try:
            DOSSIER_PAGES.mkdir(parents=True, exist_ok=True)
            copie = DOSSIER_PAGES / (re.sub(r"[^\w.\-]", "_", sortie.stem) + ".html")
            copie.write_text(page, encoding="utf-8")
            print(f"Copie : {copie}")
            if a.pas_ouvrir:
                return 0
            if serveur_actif() or lancer_serveur():
                url = f"http://127.0.0.1:{PORT}/{urllib.parse.quote(copie.name)}"
            else:
                print(f"Avertissement : serveur local indisponible (port {PORT}), "
                      "repli sur file:// (le micro sera redemandé à chaque fois).", file=sys.stderr)
        except OSError as e:
            print(f"Avertissement : copie/serveur impossible ({e}), repli sur file://.", file=sys.stderr)

    if a.pas_ouvrir:
        return 0
    if url is None:
        url = sortie.as_uri()
    print(f"URL : {url}")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Ouverture automatique impossible : {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
