#!/usr/bin/env python
"""Installe les bibliothèques H5P du skill (h5p_libs/ et h5p_libs_logiquiz/).

Les bibliothèques ne sont pas fournies avec la configuration : elles pèsent
plusieurs dizaines de Mo et sont figées sur des VERSIONS PRÉCISES (Moodle
académiques pour h5p_libs/, lecteur Logiquiz pour h5p_libs_logiquiz/). Le Hub
H5P officiel ne convient donc pas : il fournit les dernières versions.

Le script lit un manifeste (nom, sha256, taille de chaque archive), télécharge
chaque jeu manquant, vérifie son empreinte puis l'extrait dans le dossier du
skill, à côté de scripts/. Un jeu déjà présent n'est jamais écrasé sans --forcer.

Usage (depuis n'importe quel dossier) :
    python scripts/installer_libs.py                    # installe les jeux manquants
    python scripts/installer_libs.py --jeu moodle       # seulement h5p_libs/
    python scripts/installer_libs.py --forcer           # réinstalle même si présent
    python scripts/installer_libs.py --source D:/zips   # dossier local ou autre URL

Bibliothèque standard uniquement (urllib, zipfile, hashlib). En cas d'erreur
SSL (postes Windows sans certificats à jour), nouvel essai avec curl s'il est
installé ; sinon, le message donne l'URL à télécharger à la main.
"""
import argparse
import hashlib
import json
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

SOURCE_DEFAUT = 'https://bfcours.dev/download/ressources-skills/h5p-branching-scenario/'
NOM_MANIFESTE = 'manifeste.json'
DOSSIER_SKILL = Path(__file__).resolve().parent.parent
JEUX = {'moodle': 'h5p_libs', 'logiquiz': 'h5p_libs_logiquiz'}
DELAI = 60  # secondes, par requête


class ErreurInstallation(Exception):
    """Erreur expliquée à l'utilisateur, sans trace Python."""


# ---------------------------------------------------------------------------
# Accès à la source (dossier local ou URL)
# ---------------------------------------------------------------------------

def est_url(source: str) -> bool:
    return source.startswith(('http://', 'https://'))


def joindre(source: str, nom: str) -> str:
    if est_url(source):
        return source.rstrip('/') + '/' + nom
    return str(Path(source) / nom)


def _est_erreur_ssl(exc: BaseException) -> bool:
    if isinstance(exc, ssl.SSLError):
        return True
    raison = getattr(exc, 'reason', None)
    return isinstance(raison, ssl.SSLError) or 'CERTIFICATE_VERIFY_FAILED' in str(exc)


def _telecharger_curl(url: str, cible: Path) -> None:
    curl = shutil.which('curl')
    if not curl:
        raise ErreurInstallation(
            "Erreur SSL lors du téléchargement, et curl est introuvable pour réessayer.\n"
            f"  Télécharge le fichier à la main : {url}\n"
            "  puis relance avec --source <dossier contenant le zip et manifeste.json>."
        )
    print("  i Erreur SSL avec Python : nouvel essai avec curl.")
    try:
        res = subprocess.run([curl, '-fsSL', '--retry', '2', '-o', str(cible), url],
                             capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        raise ErreurInstallation(f"curl n'a pas terminé en 10 minutes : {url}")
    if res.returncode != 0:
        raise ErreurInstallation(
            f"Échec de curl (code {res.returncode}) : {res.stderr.strip()}\n"
            f"  Télécharge le fichier à la main : {url}"
        )


def recuperer(emplacement: str, cible: Path) -> None:
    """Copie (dossier local) ou télécharge (URL) emplacement vers cible."""
    if not est_url(emplacement):
        src = Path(emplacement)
        if not src.is_file():
            raise ErreurInstallation(f"Fichier introuvable : {src}")
        shutil.copyfile(src, cible)
        return
    try:
        requete = urllib.request.Request(emplacement,
                                         headers={'User-Agent': 'installer_libs.py'})
        with urllib.request.urlopen(requete, timeout=DELAI) as rep, open(cible, 'wb') as f:
            total = int(rep.headers.get('Content-Length') or 0)
            recu, palier = 0, 0
            while True:
                bloc = rep.read(1 << 16)
                if not bloc:
                    break
                f.write(bloc)
                recu += len(bloc)
                if total and recu * 10 // total > palier:
                    palier = recu * 10 // total
                    print(f"    {palier * 10} %", end='\r', flush=True)
        if total:
            print(' ' * 12, end='\r')
    except urllib.error.HTTPError as exc:
        raise ErreurInstallation(
            f"Le serveur a répondu {exc.code} pour {emplacement}\n"
            "  (fichier non encore publié, ou adresse modifiée)."
        )
    except (urllib.error.URLError, ssl.SSLError, OSError) as exc:
        if _est_erreur_ssl(exc):
            _telecharger_curl(emplacement, cible)
            return
        raise ErreurInstallation(
            f"Téléchargement impossible : {emplacement}\n  Cause : {exc}\n"
            "  Vérifie la connexion, ou télécharge le fichier à la main puis "
            "relance avec --source <dossier>."
        )


def lire_manifeste(source: str, travail: Path) -> dict:
    cible = travail / NOM_MANIFESTE
    recuperer(joindre(source, NOM_MANIFESTE), cible)
    try:
        manifeste = json.loads(cible.read_text(encoding='utf-8'))
        manifeste['jeux']
    except (json.JSONDecodeError, KeyError, TypeError):
        raise ErreurInstallation(f"Manifeste illisible : {joindre(source, NOM_MANIFESTE)}")
    return manifeste


# ---------------------------------------------------------------------------
# Vérification et extraction
# ---------------------------------------------------------------------------

def sha256_fichier(chemin: Path) -> str:
    h = hashlib.sha256()
    with open(chemin, 'rb') as f:
        for bloc in iter(lambda: f.read(1 << 20), b''):
            h.update(bloc)
    return h.hexdigest()


def extraire(archive: Path, dossier: str, destination: Path) -> int:
    """Extrait archive (racine = dossier/) dans destination/dossier.

    L'extraction se fait d'abord dans un dossier temporaire voisin, puis le
    dossier final est mis en place d'un coup : une coupure en cours de route ne
    laisse jamais un jeu à moitié installé."""
    with zipfile.ZipFile(archive) as zf:
        noms = zf.namelist()
        for nom in noms:
            if nom.startswith('/') or '..' in Path(nom).parts or ':' in nom:
                raise ErreurInstallation(f"Archive refusée : chemin suspect « {nom} ».")
            if nom.split('/', 1)[0] != dossier:
                raise ErreurInstallation(
                    f"Archive refusée : « {nom} » n'est pas dans {dossier}/.")
        temporaire = Path(tempfile.mkdtemp(prefix=f'.{dossier}-', dir=destination))
        try:
            zf.extractall(temporaire)
            final = destination / dossier
            ancien = None
            if final.exists():
                ancien = destination / f'.{dossier}-ancien'
                if ancien.exists():
                    shutil.rmtree(ancien)
                final.rename(ancien)
            (temporaire / dossier).rename(final)
            if ancien is not None:
                shutil.rmtree(ancien, ignore_errors=True)
        finally:
            shutil.rmtree(temporaire, ignore_errors=True)
    return sum(1 for n in noms if not n.endswith('/'))


def installer_jeu(cle: str, entree: dict, source: str, travail: Path) -> None:
    dossier = entree.get('dossier', JEUX[cle])
    nom = entree['nom']
    emplacement = joindre(source, nom)
    taille_mo = entree.get('taille', 0) / 1e6
    print(f"-> {dossier}/ : {nom} ({taille_mo:.1f} Mo)")
    archive = travail / nom
    recuperer(emplacement, archive)

    taille = archive.stat().st_size
    if entree.get('taille') and taille != entree['taille']:
        raise ErreurInstallation(
            f"Taille inattendue pour {nom} : {taille} octets au lieu de {entree['taille']}.\n"
            "  Téléchargement incomplet ou fichier modifié : rien n'a été installé.")
    empreinte = sha256_fichier(archive)
    if empreinte != entree['sha256']:
        raise ErreurInstallation(
            f"Empreinte sha256 incorrecte pour {nom} :\n"
            f"  attendue : {entree['sha256']}\n  obtenue  : {empreinte}\n"
            "  Fichier corrompu ou modifié : rien n'a été installé.")
    print("  OK empreinte sha256 vérifiée")

    n = extraire(archive, dossier, DOSSIER_SKILL)
    nb_libs = entree.get('nb_bibliotheques', '?')
    print(f"  OK {dossier}/ installé : {nb_libs} bibliothèques, {n} fichiers")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Télécharge et installe les bibliothèques H5P du skill "
                    "(h5p_libs/ pour Moodle, h5p_libs_logiquiz/ pour Logiquiz).")
    ap.add_argument('--jeu', choices=['moodle', 'logiquiz', 'tous'], default='tous',
                    help='Jeu à installer (défaut : tous)')
    ap.add_argument('--source', default=SOURCE_DEFAUT,
                    help='Dossier local ou URL contenant manifeste.json et les zips '
                         f'(défaut : {SOURCE_DEFAUT})')
    ap.add_argument('--forcer', action='store_true',
                    help="Réinstaller un jeu même s'il est déjà présent")
    args = ap.parse_args()

    cles = list(JEUX) if args.jeu == 'tous' else [args.jeu]
    a_faire = []
    for cle in cles:
        if (DOSSIER_SKILL / JEUX[cle]).is_dir() and not args.forcer:
            print(f"i {JEUX[cle]}/ déjà présent : rien à faire (--forcer pour réinstaller).")
        else:
            a_faire.append(cle)
    if not a_faire:
        return 0

    with tempfile.TemporaryDirectory(prefix='h5p-libs-') as tmp:
        travail = Path(tmp)
        try:
            print(f"Manifeste : {joindre(args.source, NOM_MANIFESTE)}")
            manifeste = lire_manifeste(args.source, travail)
            print(f"  Jeux publiés le {manifeste.get('date', '?')}")
            for cle in a_faire:
                entree = manifeste['jeux'].get(cle)
                if not entree:
                    raise ErreurInstallation(f"Le manifeste ne décrit pas le jeu « {cle} ».")
                installer_jeu(cle, entree, args.source, travail)
        except ErreurInstallation as exc:
            print(f"ERREUR : {exc}")
            return 1
    print("Terminé : le skill peut générer des .h5p.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
