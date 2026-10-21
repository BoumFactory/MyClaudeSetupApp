"""Lecture d'un script « voix mixtes » (partagée par nettoyer_audio.py et assembler_voix.py).

Format de script.md :

    ## b01 [prof] [pause 0.4]
    Texte que le professeur dit (et que son enregistrement doit contenir).
    > visuel : ce qui s'affiche (ligne ignorée)

    ## b02 [tom] [pause 0.5] [lent 1.1]
    Texte lu par la voix de synthèse Piper « tom ».

- étiquette de voix obligatoire : [prof] (voix enregistrée), [tom] / [siwis] / [upmc] (Piper, secours) ou une voix
  Pocket TTS : nom du catalogue ([estelle], [peter_yearsley]…) ou alias de voix clonée de config.json ([ma-voix]) ;
- [pause s] : silence après le bloc (défaut 0,5 s) ; [lent f] : ralentissement Piper (défaut 1.0) ;
- les lignes qui commencent par « > » (visuels, notes) et tout titre hors « ## id » sont ignorés.
"""
import pathlib
import re
import sys

VOIX_SYNTHESE = {"tom", "siwis", "upmc"}  # voix Piper ; toute autre étiquette (hors « prof ») est une voix Pocket TTS


def est_pocket(voix):
    return voix != "prof" and voix not in VOIX_SYNTHESE


def lire_script_mixte(chemin):
    blocs, cour = [], None
    for num, ligne in enumerate(pathlib.Path(chemin).read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^##\s+([A-Za-z]\d+[a-z]?)(\s.*)?$", ligne)
        if not m and ligne.startswith("#"):
            cour = None
            continue
        if m:
            options = m.group(2) or ""
            v = re.search(r"\[([A-Za-z_][\w-]*)\]", options)
            if not v:
                sys.exit(f"{chemin} ligne {num} : le bloc {m.group(1)} n'a pas d'étiquette de voix ([prof], [tom], [estelle]…).")
            pause = re.search(r"\[pause\s+([\d.]+)\]", options)
            lent = re.search(r"\[lent\s+([\d.]+)\]", options)
            cour = {"id": m.group(1), "voix": v.group(1), "pause": float(pause.group(1)) if pause else 0.5,
                    "lent": float(lent.group(1)) if lent else 1.0, "lignes": []}
            blocs.append(cour)
        elif cour is not None and ligne.strip() and not ligne.lstrip().startswith(">"):
            cour["lignes"].append(ligne.strip())
    res = [{"id": b["id"], "voix": b["voix"], "pause": b["pause"], "lent": b["lent"], "texte": " ".join(b["lignes"])}
           for b in blocs]
    vides = [b["id"] for b in res if not b["texte"]]
    if vides:
        sys.exit(f"Blocs sans texte : {', '.join(vides)}")
    ids = [b["id"] for b in res]
    doubles = sorted({i for i in ids if ids.count(i) > 1})
    if doubles:
        sys.exit(f"Identifiants de blocs en double : {', '.join(doubles)}")
    return res
