#!/usr/bin/env python
"""Construit les archives des bibliothèques H5P du skill h5p-branching-scenario.

Les dossiers h5p_libs/ (cible Moodle) et h5p_libs_logiquiz/ (lecteur Logiquiz)
ne sont plus publiés dans la configuration : le skill les télécharge à la
demande avec scripts/installer_libs.py. Ce script produit, dans
public/download/ressources-skills/h5p-branching-scenario/ :

    h5p_libs-AAAA-MM-JJ.zip            (racine du zip = h5p_libs/)
    h5p_libs_logiquiz-AAAA-MM-JJ.zip   (racine du zip = h5p_libs_logiquiz/)
    manifeste.json                     (nom, URL, sha256, taille, date, nombre de bibliothèques)

Les archives sont reproductibles : entrées triées, horodatage fixe. Deux
constructions sur les mêmes dossiers donnent donc le même sha256.

Usage (depuis la racine du site) :
    python docs/ressources-skills/construire_libs_h5p.py --libs <dossier du skill contenant h5p_libs/>
    python docs/ressources-skills/construire_libs_h5p.py --libs <...> --date 2026-10-28

Par défaut, --libs vaut la copie publiée du skill. Les anciens zips du même jeu
sont laissés en place (supprimer à la main ceux qui ne sont plus référencés).
"""
import argparse
import datetime
import hashlib
import json
import sys
import zipfile
from pathlib import Path

RACINE_SITE = Path(__file__).resolve().parents[2]
SKILL_PUBLIE = (RACINE_SITE / 'public' / 'download' / 'Claude-Code-Setup'
                / 'claude-setup' / 'skills' / 'h5p-branching-scenario')
SORTIE = RACINE_SITE / 'public' / 'download' / 'ressources-skills' / 'h5p-branching-scenario'
URL_BASE = 'https://bfcours.dev/download/ressources-skills/h5p-branching-scenario/'

JEUX = {
    'moodle': {
        'dossier': 'h5p_libs',
        'description': 'Bibliothèques alignées sur les Moodle académiques (sortie principale).',
    },
    'logiquiz': {
        'dossier': 'h5p_libs_logiquiz',
        'description': 'Bibliothèques alignées sur le lecteur hors ligne Logiquiz (variante -logiquiz).',
    },
}

HORODATAGE_FIXE = (2026, 1, 1, 0, 0, 0)


def sha256_fichier(chemin: Path) -> str:
    h = hashlib.sha256()
    with open(chemin, 'rb') as f:
        for bloc in iter(lambda: f.read(1 << 20), b''):
            h.update(bloc)
    return h.hexdigest()


def construire_zip(dossier: Path, cible: Path) -> dict:
    """Zippe dossier/ (racine du zip = nom du dossier). Retourne les compteurs."""
    fichiers = sorted(p for p in dossier.rglob('*') if p.is_file())
    nb_libs = sum(1 for d in dossier.iterdir() if (d / 'library.json').is_file())
    tmp = cible.with_suffix('.zip.tmp')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in fichiers:
            nom = dossier.name + '/' + p.relative_to(dossier).as_posix()
            info = zipfile.ZipInfo(nom, date_time=HORODATAGE_FIXE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes(), compresslevel=9)
    tmp.replace(cible)
    return {'nb_fichiers': len(fichiers), 'nb_bibliotheques': nb_libs}


def main() -> int:
    ap = argparse.ArgumentParser(description='Construit les zips des bibliothèques H5P et le manifeste.')
    ap.add_argument('--libs', default=str(SKILL_PUBLIE),
                    help='Dossier du skill contenant h5p_libs/ et h5p_libs_logiquiz/')
    ap.add_argument('--date', default=datetime.date.today().isoformat(),
                    help='Date inscrite dans le nom des zips (AAAA-MM-JJ)')
    ap.add_argument('--sortie', default=str(SORTIE), help='Dossier de sortie')
    args = ap.parse_args()

    libs = Path(args.libs)
    sortie = Path(args.sortie)
    sortie.mkdir(parents=True, exist_ok=True)

    manifeste = {
        'skill': 'h5p-branching-scenario',
        'version_manifeste': 1,
        'date': args.date,
        'installation': 'python scripts/installer_libs.py (depuis le dossier du skill)',
        'jeux': {},
    }
    for cle, jeu in JEUX.items():
        dossier = libs / jeu['dossier']
        if not dossier.is_dir():
            print(f"ERREUR : dossier introuvable : {dossier}")
            return 1
        nom_zip = f"{jeu['dossier']}-{args.date}.zip"
        cible = sortie / nom_zip
        compteurs = construire_zip(dossier, cible)
        entree = {
            'nom': nom_zip,
            'dossier': jeu['dossier'],
            'description': jeu['description'],
            'url': URL_BASE + nom_zip,
            'sha256': sha256_fichier(cible),
            'taille': cible.stat().st_size,
            'date': args.date,
        }
        entree.update(compteurs)
        manifeste['jeux'][cle] = entree
        taille_mo = entree['taille'] / 1e6
        print(f"OK {nom_zip} : {entree['nb_bibliotheques']} bibliothèques, "
              f"{entree['nb_fichiers']} fichiers, {taille_mo:.1f} Mo")

    (sortie / 'manifeste.json').write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"OK manifeste : {sortie / 'manifeste.json'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
