"""Construit le kit de depart .exoslombards (gabarits generiques + copie bfcours).

Usage : python construire_kit.py <dossier_destination>
Le dossier <destination>/.exoslombards est (re)cree.
"""
import json
import re
import shutil
import sys
from pathlib import Path

SRC = Path("D:/Applications/Exos_lombards/.exoslombards")
DEST = Path(sys.argv[1]) / ".exoslombards"

FNV_BASE = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3
MASK = (1 << 64) - 1


def fnv1a(data: bytes, h: int) -> int:
    for o in data:
        h ^= o
        h = (h * FNV_PRIME) & MASK
    return h


def empreinte_octets(b: bytes) -> str:
    return format(fnv1a(b, FNV_BASE), "016x")


def empreinte_globale(fichiers) -> str:
    h = FNV_BASE
    for f in fichiers:
        h = fnv1a(f["chemin"].encode("utf-8"), h)
        h = fnv1a(b"\0", h)
        h = fnv1a(f["empreinte"].encode("utf-8"), h)
        h = fnv1a(b"\n", h)
    return format(h, "016x")


# (fichier relatif a .exoslombards, ancien texte, nouveau texte) : chaque ancien
# texte doit etre present, sinon le script s'arrete.
PDFAUTHOR = ("pdfauthor={R.Deschamps},", "pdfauthor={},")
LUAMATHS = (
    '% chemin complet du fichier : "C:\\Users\\Utilisateur\\AppData\\Roaming\\MiKTeX\\tex\\latex\\luamaths\\luamaths.sty"',
    "% chemin complet du fichier : <racine MiKTeX>/tex/latex/luamaths/luamaths.sty",
)
IMGPATH = (
    "\\providecommand{\\bfcoursimgpath}{C:/Users/Utilisateur/Documents/Professionnel/bfcours-images}",
    "\\providecommand{\\bfcoursimgpath}{}",
)
ICONES = "C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2023 - 2024/1. Cours/366_fonctionnement/365_Icones"
B = "texmf/tex/latex/BFcours/"
PATCHS = [
    ("templates/fiche_exercices.tex",) + PDFAUTHOR,
    ("templates/devoir.tex",) + PDFAUTHOR,
    ("templates/bac.tex",) + PDFAUTHOR,
    (B + "bfcours.sty",) + LUAMATHS,
    (B + "bfcours.sty",) + IMGPATH,
    (B + "bfcours-enum.sty",) + LUAMATHS,
    (B + "bfcours-enum.sty",) + IMGPATH,
    (B + "bfcours-lourd.sty",) + LUAMATHS,
    (B + "bfcours-lourd.sty",) + IMGPATH,
    (B + "bfcoursQF.sty",) + LUAMATHS,
    (B + "bfcoursQF.sty",) + IMGPATH,
    (B + "bfcours-iconsInsert.sty", "\\newcommand{\\dbiconpath}{" + ICONES + "}", "\\newcommand{\\dbiconpath}{}"),
    (B + "bfcours-iconsInsert.sty", "\\newcommand{\\coverAnime}{" + ICONES + "/Fun/covers_manga}", "\\newcommand{\\coverAnime}{}"),
    (B + "bfcours-iconsInsert.sty", "\\newcommand{\\imdbPath}{" + ICONES + "}", "\\newcommand{\\imdbPath}{}"),
    (B + "bfcours-tectonic.sty",
     "    {C:/Users/Utilisateur/Documents/Professionnel/localtexmf/tex/latex/BFcours/}%\n"
     "    {C:/Users/Utilisateur/Documents/Professionnel/localtexmf/tex/latex/ProfDeleuze/}%\n"
     "    {C:/Users/Utilisateur/AppData/Roaming/MiKTeX/tex/latex/bclogo/}%\n",
     ""),
    (B + "bfcours-tectonic.sty",
     "\\newcommand{\\bfcoursimgpath}{C:/Users/Utilisateur/Documents/Professionnel/bfcours-images}",
     "\\providecommand{\\bfcoursimgpath}{}"),
    (B + "bfcours-exolombards-skin.sty", "\\newcommand{\\bfexol@auteur}{L. M\\'erat}", "\\newcommand{\\bfexol@auteur}{}"),
    (B + "bfcours-exolombards-skin.sty", "\\newcommand{\\bfexol@etablissement}{Lyc\\'ee Les Lombards}", "\\newcommand{\\bfexol@etablissement}{}"),
    (B + "bfcours-exolombards-skin.sty", "(L. Mérat)", "(vide)"),
    (B + "bfcours-exolombards-skin.sty", "(Lycée Les Lombards)", "(vide)"),
    (B + "bfcours-exolombards-skin.sty", " (lycée Les Lombards)", ""),
]

# Motifs interdits dans tout le kit (chemins personnels, etablissement, contacts).
INTERDITS = [r"Utilisateur", r"\b[A-Z]:[/\\](?!chemin/sans/espaces)", r"Users[/\\]", r"Professionnel", r"Reims 20",
             r"[Ll]yc[ée]e Les Lombards", r"Lyc\\'ee", r"@gmail", r"@ac-", r"R\.Deschamps"]


def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    # 1. Gabarits et preambule
    for rel in ["templates/fiche_exercices.tex", "templates/devoir.tex", "templates/bac.tex",
                "templates/apercu.tex", "preambules/lombards-macros.tex"]:
        (DEST / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / rel, DEST / rel)

    # 1 bis. Base principale vide (l'index exige sources/exercices) : meme
    # contenu que bases::SECTIONS_VIDES de l'application.
    (DEST / "sources/exercices").mkdir(parents=True, exist_ok=True)
    (DEST / "sources/sections.json").write_bytes(
        b'{\n  "parties": [],\n  "sections": [],\n  "orphelins": [],\n  "manquants": []\n}\n')

    # 2. Copie bfcours : exactement les fichiers du manifeste
    man = json.loads((SRC / "texmf/MANIFESTE.json").read_text(encoding="utf-8"))
    assert empreinte_globale(man["fichiers"]) == man["empreinte"], "algorithme d'empreinte faux"
    for f in man["fichiers"]:
        src = SRC / "texmf" / f["chemin"]
        octets = src.read_bytes()
        assert empreinte_octets(octets) == f["empreinte"], "copie d'origine non conforme : " + f["chemin"]
        dst = DEST / "texmf" / f["chemin"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(octets)

    # 3. Retouches
    for rel, avant, apres in PATCHS:
        p = DEST / rel
        t = p.read_bytes().decode("utf-8")
        n = t.count(avant)
        assert n >= 1, "motif absent dans " + rel + " : " + avant[:60]
        p.write_bytes(t.replace(avant, apres).encode("utf-8"))
        print("retouche", rel, "x" + str(n))

    # 4. Manifeste recalcule
    total = 0
    for f in man["fichiers"]:
        octets = (DEST / "texmf" / f["chemin"]).read_bytes()
        f["taille"] = len(octets)
        f["empreinte"] = empreinte_octets(octets)
        total += len(octets)
    man["source"] = ""
    man["source_images"] = ""
    man["taille"] = total
    man["empreinte"] = empreinte_globale(man["fichiers"])
    (DEST / "texmf/MANIFESTE.json").write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")

    # 5. Controle
    fautes = 0
    nb = 0
    for p in sorted(DEST.rglob("*")):
        if not p.is_file():
            continue
        nb += 1
        if p.suffix.lower() in (".pdf", ".png"):
            continue
        t = p.read_bytes().decode("utf-8", errors="replace")
        for motif in INTERDITS:
            for m in re.finditer(motif, t):
                ligne = t.count("\n", 0, m.start()) + 1
                print("INTERDIT", p.relative_to(DEST), "l." + str(ligne), motif)
                fautes += 1
    print("fichiers :", nb, "— fautes :", fautes)
    sys.exit(1 if fautes else 0)


if __name__ == "__main__":
    main()
