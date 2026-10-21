"""Relecture automatique de la rigueur d'un ou plusieurs script.md (voir references/rigueur.md).

Signale, par temps fort, les fautes de rédaction détectables par motif : enchaînements de calcul
sans « égale », liaisons piégeuses de la voix, objet calculé au lieu d'une grandeur, conclusions
elliptiques… Code de sortie 1 s'il reste une alerte (fournee_voix.py s'arrête alors, sauf --forcer).

Notations lues telles quelles ($, \\, ^, _, /, ≤, [AB], « triangle RIS »…) : la voix dirait « dollar » ou
épellerait mal. L'alerte « forme orale » PROPOSE la phrase réécrite (scripts/maths_parlees.py) ; Claude
corrige script.md lui-même, pour que les mots du script restent les mots dits (ancrage exact).

Usage :
    python relire_script.py <capsule ou dossier de fournée> [...] [--appliquer]

--appliquer : réécrit les phrases concernées de script.md avec la forme orale proposée, après sauvegarde
en script.avant-oral.md (pour qui préfère écrire le script en notations).
"""
import pathlib
import re
import shutil
import sys

from maths_parlees import a_relire, vers_oral

# (motif, règle de references/rigueur.md, conseil)
REGLES = [
    (r"\bsoit\s+(moins\s+)?\d", 1, "enchaînement « soit » : dire « égale »"),
    (r"(?i)\bça fait\b", 1, "« ça fait » : dire « égale »"),
    (r"(?i)\bc'est\s+(moins\s+)?\d", 1, "« c'est <nombre> » : dire « égale »"),
    (r"(?i)\bdonne\s+(bien\s+)?(moins\s+)?\d", 1, "« donne <nombre> » dans un calcul : dire « égale »"),
    # opération binaire (chiffre puis moins / plus / fois), division ou carré, puis « : nombre »
    (r"(?:\d\s+(?:moins|plus|fois)\s+|divisé par \d|au carré)[^.:;]*:\s*(moins\s+)?\d", 1,
     "résultat jeté après deux-points : écrire « … Égale <résultat>. »"),
    # « a moins (moins b) » doit passer par « a plus b » avant le résultat
    (r"entre parenthèses, moins [\d,]+[.,;]\s+[ÉEé]gale (?:moins )?\d+(?:,\d+)?(?![\d,]| plus| moins)", 4,
     "soustraction d'un négatif : dire d'abord « Égale a plus b », puis le résultat"),
    (r"(?i)\bcas\s+[a-h]\b", 18, "liaison « cas a » → « saza » : dire « Premier cas »"),
    (r"(?i)\bcalcul\w*\s+(?:\w+\s+){0,2}(?:le|la|les|un|une|deux|trois)\s+(?:vecteur|point|triangle|droite|segment|cercle|quadrilatère|parallélogramme)s?\b",
     8, "on calcule une grandeur (coordonnées, norme, longueur…), pas l'objet"),
    (r"(?i)\b(prouver|démontrer|montrer|justifier)\s+(un|une)\s+(parallélogramme|carré|losange|rectangle|triangle|milieu)",
     9, "on prouve qu'un objet EST … : « prouver qu'un quadrilatère est un parallélogramme »"),
    (r"(?i)\bpour\s+(un|une)\s+(carré|losange|rectangle|parallélogramme|triangle rectangle)\s*,", 9,
     "« pour un carré, … » : « pour démontrer qu'un quadrilatère est un carré, … »"),
    (r"(?:^|[.!?]\s+)(Égaux|Égales|Opposés|Mêmes coordonnées)\s*:", 10, "conclusion elliptique : nommer les objets"),
    (r"(?i)racine carrée de\s*:\s*le carré", 19, "« de le carré » : « la racine carrée de : moins 5, entre parenthèses, au carré »"),
    (r"(?i)\bd'un carré\b(?!\s*de\s+côté)", 13, "« d'un carré » pour un déplacement : « d'un côté de carré » ?"),
]


def blocs(chemin):
    cour = None
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+([A-Za-z]\d+[a-z]?)(\s.*)?$", ligne)
        if m:
            cour = m.group(1)
        elif ligne.startswith("#"):
            cour = None
        elif cour and ligne.strip():
            yield cour, ligne.strip()


def relire(script):
    alertes = []
    for bloc, texte in blocs(script):
        if texte.startswith("<!--"):
            continue
        for motif, regle, conseil in REGLES:
            for m in re.finditer(motif, texte):
                debut = max(0, m.start() - 30)
                alertes.append((bloc, regle, conseil, texte[debut:m.end() + 20]))
        if not texte.startswith(">") and a_relire(texte):   # « > visuel : … » n'est pas lu (voix_pocket.py)
            oral = vers_oral(texte)
            if oral != texte:
                alertes.append((bloc, None, "notation lue telle quelle : écrire la forme orale",
                                f"{texte}\n    → proposé : {oral}"))
    return alertes


def appliquer(script):
    """Réécrit les phrases à notations des temps forts avec leur forme orale (sauvegarde d'abord)."""
    brut = script.read_bytes().decode("utf-8")
    fin = "\r\n" if "\r\n" in brut else "\n"   # fins de ligne d'origine conservées
    lignes, cour, n = brut.splitlines(), None, 0
    for i, ligne in enumerate(lignes):
        if re.match(r"^##\s+([A-Za-z]\d+[a-z]?)(\s.*)?$", ligne):
            cour = True
        elif ligne.startswith("#"):
            cour = None
        elif cour and ligne.strip() and not ligne.lstrip().startswith(("<!--", ">")) and a_relire(ligne):
            oral = vers_oral(ligne.strip())
            if oral != ligne.strip():
                lignes[i], n = oral, n + 1
    if n:
        sauvegarde = script.with_name("script.avant-oral.md")
        k = 2
        while sauvegarde.exists():
            sauvegarde, k = script.with_name(f"script.avant-oral-{k}.md"), k + 1
        shutil.copy2(script, sauvegarde)
        script.write_bytes((fin.join(lignes) + fin).encode("utf-8"))
        print(f"{script.parent.name} : {n} phrase(s) réécrite(s) à l'oral (avant : {sauvegarde.name}).")


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if a != "--appliquer"]
    scripts = []
    for arg in args:
        p = pathlib.Path(arg)
        scripts += [p / "script.md"] if (p / "script.md").exists() else sorted(p.glob("*/script.md"))
    if "--appliquer" in sys.argv:
        for s in scripts:
            appliquer(s)
    total = 0
    for s in scripts:
        alertes = relire(s)
        total += len(alertes)
        for bloc, regle, conseil, extrait in alertes:
            etiquette = f"règle {regle}" if regle is not None else "forme orale"
            print(f"{s.parent.name} {bloc} [{etiquette}] {conseil}\n    … {extrait} …" if regle is not None
                  else f"{s.parent.name} {bloc} [{etiquette}] {conseil}\n    {extrait}")
    print(f"{len(scripts)} script(s) relu(s), {total} alerte(s).")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
