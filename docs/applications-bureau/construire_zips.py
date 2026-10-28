"""Construit les zips statiques des applications de bureau du site.

Usage : python construire_zips.py <dossier applications-bureau du site> <dossier contenant .exoslombards>

Les exécutables ne sont plus rangés dans le dossier public : ils sont lus
depuis les sources, D:/Applications/<App>/src-tauri/target/release/<exe>.
Le kit .exoslombards est produit par construire_kit.py
(python construire_kit.py <dossier>, qui crée <dossier>/.exoslombards).

Chaque zip contient un dossier racine (nom sans espace) avec l'exe et son mode
d'emploi (lu dans le dossier public) ; celui d'Exos Lombards contient aussi le
kit .exoslombards, placé à côté de l'exe. Seuls les zips sont distribués.
"""
import sys
import zipfile
from pathlib import Path

SITE = Path(sys.argv[1])
KIT = Path(sys.argv[2]) / ".exoslombards"
SOURCES = Path("D:/Applications")

APPS = [
    # (slug, version, dossier racine dans le zip, exe, dossier source)
    ("activite-timer", "0.1.0", "Activite-Timer", "activite-timer.exe", "Activite-timer"),
    ("gestion-classes", "0.1.0", "Gestion-de-classes", "gestion-classes.exe", "gestion-classes"),
    ("exos-lombards", "0.1.0", "Exos-Lombards", "exos-lombards.exe", "Exos_lombards"),
]


def ajouter_arbre(z: zipfile.ZipFile, racine: Path, prefixe: str) -> int:
    """Ajoute racine/** sous prefixe/, dossiers vides compris."""
    n = 0
    for p in sorted(racine.rglob("*")):
        arc = prefixe + "/" + p.relative_to(racine).as_posix()
        if p.is_dir():
            if not any(p.iterdir()):
                z.writestr(arc + "/", "")
        else:
            z.write(p, arc)
            n += 1
    return n


def main():
    for slug, version, racine, exe, source in APPS:
        dossier = SITE / slug
        exe_p = SOURCES / source / "src-tauri" / "target" / "release" / exe
        html_p = dossier / (slug + "-mode-emploi.html")
        assert exe_p.is_file(), exe_p
        assert html_p.is_file(), html_p
        cible = dossier / (slug + "-" + version + ".zip")
        with zipfile.ZipFile(cible, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            z.write(exe_p, racine + "/" + exe)
            z.write(html_p, racine + "/" + html_p.name)
            n = 2
            if slug == "exos-lombards":
                assert KIT.is_dir(), KIT
                n += ajouter_arbre(z, KIT, racine + "/.exoslombards")
        print(cible.name, n, "fichiers", round(cible.stat().st_size / 1048576, 2), "Mo")

    # Controle : aucun nom de fichier hors de la liste attendue
    for zp in sorted(SITE.rglob("*.zip")):
        with zipfile.ZipFile(zp) as z:
            assert z.testzip() is None, zp
            noms = z.namelist()
            interdits = [x for x in noms if any(m in x for m in ("/classes/", "/fiches/", "/cache/", "/sources/exercices/", "config.json", "metadonnees", "tutoriel", "data/"))
                         and not x.endswith("sources/exercices/")]
            assert not interdits, (zp.name, interdits)
            print("ok", zp.name, len(noms), "entrees")


if __name__ == "__main__":
    main()
