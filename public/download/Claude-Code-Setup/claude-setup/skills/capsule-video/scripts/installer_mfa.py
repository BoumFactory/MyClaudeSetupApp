"""Installation automatisée et isolée de Montreal Forced Aligner (MFA 3), sans Anaconda.

Usage :
    python installer_mfa.py [--racine DOSSIER] [--config chemin/config.json] [--sans-modeles] [--cuda] [--maj-config]

--maj-config : à la fin, écrit la clé « mfa » ({micromamba, env, modeles, root}) dans le config.json du skill
(ou celui de --config), sans toucher aux autres clés. Appelé ainsi par installation/installer.ps1.
Python : n'importe lequel (bibliothèque standard). Durée ≈ 7 min 20, 2,5 Go (variante processeur, mesuré le
20/10/2026).

Ce que fait le script (relançable : chaque étape saute ce qui existe déjà) :
  1. télécharge micromamba (exécutable seul) dans <racine>/outils/
  2. crée l'environnement <racine>/env-mfa (conda-forge, montreal-forced-aligner)
  3. télécharge les modèles français (acoustique, dictionnaire, g2p) dans <racine>/mfa-modeles/

Isolation : MAMBA_ROOT_PREFIX, MFA_ROOT_DIR, les caches de paquets et TEMP restent sous <racine>.
Rien n'est écrit dans le PATH, le registre, le profil du terminal, ni dans une installation
Anaconda existante (--no-rc : aucun .condarc n'est lu ; pas de « shell init »).

<racine> : --racine, sinon le dossier parent de "cache_modeles" dans le config.json du skill,
sinon ~/capsule-video.
"""
import argparse
import json
import os
import shutil
import ssl
import subprocess
import sys
import time
import urllib.request

WINDOWS = sys.platform == "win32"


def _plateforme_micromamba():
    """Nom de l'exécutable micromamba officiel pour ce système (win-64, linux-64, linux-aarch64, osx-64, osx-arm64)."""
    import platform
    m = platform.machine().lower()
    if WINDOWS:
        return "win-64.exe"
    if sys.platform == "darwin":
        return "osx-arm64" if m in ("arm64", "aarch64") else "osx-64"
    return "linux-aarch64" if m in ("aarch64", "arm64") else "linux-64"


URLS_MICROMAMBA = [
    "https://github.com/mamba-org/micromamba-releases/releases/latest/download/micromamba-" + _plateforme_micromamba(),
]
SOUS_BIN = "Scripts" if WINDOWS else "bin"
NOM_MFA = "mfa.exe" if WINDOWS else "mfa"
ICI = os.path.dirname(os.path.abspath(__file__))
CONFIG_SKILL = os.path.join(ICI, "..", "config.json")


sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def dire(msg):
    print(msg, flush=True)


def racine_par_defaut(config):
    for c in [config, os.path.join(ICI, "..", "config.json"), CONFIG_SKILL]:
        if c and os.path.exists(c):
            try:
                cm = json.load(open(c, encoding="utf-8")).get("cache_modeles")
                if cm:
                    return os.path.dirname(os.path.abspath(cm))
            except Exception:
                pass
    return os.path.join(os.path.expanduser("~"), "capsule-video")


def oublier_enregistrement(env):
    """micromamba inscrit l'environnement dans ~/.conda/environments.txt (liste partagée avec Anaconda,
    non désactivable par variable). On retire notre seule ligne pour que `conda env list` d'un Anaconda
    existant ne voie rien de nouveau."""
    f = os.path.join(os.path.expanduser("~"), ".conda", "environments.txt")
    if not os.path.exists(f):
        return
    cible = os.path.normcase(os.path.normpath(env))
    with open(f, encoding="utf-8", errors="replace", newline="") as fh:
        lignes = fh.read().splitlines(keepends=True)
    gardees = [l for l in lignes if os.path.normcase(os.path.normpath(l.strip())) != cible]
    if len(gardees) != len(lignes):
        with open(f, "w", encoding="utf-8", newline="") as fh:
            fh.write("".join(gardees))


def poids(chemin):
    total = 0
    if os.path.isfile(chemin):
        return os.path.getsize(chemin)
    for r, _, fs in os.walk(chemin):
        for f in fs:
            try:
                total += os.path.getsize(os.path.join(r, f))
            except OSError:
                pass
    return total


def go(n):
    return f"{n / 1e9:.2f} Go" if n >= 1e8 else f"{n / 1e6:.0f} Mo"


def telecharger(url, dest):
    """Téléchargement avec repli SSL : certificats système, puis certifi, puis PowerShell, puis curl."""
    tmp = dest + ".part"
    essais = []
    essais.append(("Python (certificats système)", lambda: _urllib(url, tmp, ssl.create_default_context())))
    try:
        import certifi
        essais.append(("Python (certifi)", lambda: _urllib(url, tmp, ssl.create_default_context(cafile=certifi.where()))))
    except ImportError:
        pass
    if WINDOWS:
        essais.append(("PowerShell (magasin Windows)", lambda: subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -UseBasicParsing -Uri '{url}' -OutFile '{tmp}'"],
            check=True, timeout=900)))
        essais.append(("curl (schannel)", lambda: subprocess.run(
            ["curl", "-L", "--ssl-no-revoke", "-o", tmp, url], check=True, timeout=900)))
    else:
        essais.append(("curl", lambda: subprocess.run(["curl", "-fL", "-o", tmp, url], check=True, timeout=900)))
    for nom, f in essais:
        try:
            f()
            if os.path.getsize(tmp) > 1e6:
                os.replace(tmp, dest)
                dire(f"  téléchargé via {nom}")
                return True
        except Exception as e:
            dire(f"  échec via {nom} : {str(e)[:120]}")
    return False


def _urllib(url, tmp, ctx):
    req = urllib.request.Request(url, headers={"User-Agent": "capsule-video-installer"})
    with urllib.request.urlopen(req, context=ctx, timeout=120) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", help="dossier racine de l'installation (défaut : parent de cache_modeles)")
    ap.add_argument("--config", help="config.json du skill capsule-video")
    ap.add_argument("--sans-modeles", action="store_true")
    ap.add_argument("--cuda", action="store_true", help="variante Kaldi CUDA (+4 Go, inutile pour l alignement)")
    ap.add_argument("--maj-config", action="store_true", help="écrit la clé « mfa » dans config.json à la fin")
    a = ap.parse_args()

    racine = os.path.abspath(a.racine or racine_par_defaut(a.config)).replace("\\", "/")
    if "anaconda" in racine.lower():
        sys.exit("La racine ne doit pas être dans Anaconda.")
    outils = f"{racine}/outils"
    env = f"{racine}/env-mfa"
    mamba_root = f"{racine}/mamba-root"
    mfa_root = f"{racine}/mfa-modeles"
    tmp = f"{racine}/tmp-mfa"
    for d in (outils, mamba_root, mfa_root, tmp):
        os.makedirs(d, exist_ok=True)
    exe = f"{outils}/micromamba" + (".exe" if WINDOWS else "")
    t0 = time.time()
    dire(f"Racine d'installation : {racine}")

    # Environnement du processus fils : tout reste sous la racine
    e = dict(os.environ, PYTHONIOENCODING="utf-8", MAMBA_ROOT_PREFIX=mamba_root, MFA_ROOT_DIR=mfa_root,
             CONDA_PKGS_DIRS=f"{mamba_root}/pkgs", TEMP=tmp, TMP=tmp, TMPDIR=tmp, MAMBA_NO_BANNER="1", MAMBA_REGISTER_ENVS="false")
    for k in ("CONDA_PREFIX", "CONDA_DEFAULT_ENV", "PYTHONHOME", "PYTHONPATH"):
        e.pop(k, None)
    # retire Anaconda du PATH du seul processus fils (le PATH du poste n'est pas modifié)
    e["PATH"] = os.pathsep.join(p for p in e["PATH"].split(os.pathsep) if "anaconda" not in p.lower()
                                and "miniconda" not in p.lower())

    # 1. micromamba
    t = time.time()
    if os.path.exists(exe):
        dire("[1/3] micromamba déjà présent, étape sautée.")
    else:
        dire("[1/3] Téléchargement de micromamba (exécutable seul, ~15 Mo)...")
        if not telecharger(URLS_MICROMAMBA[0], exe):
            sys.exit("Impossible de télécharger micromamba (voir les messages ci-dessus).")
        if not WINDOWS:
            os.chmod(exe, 0o755)
    dire(f"      micromamba : {subprocess.run([exe, '--version'], capture_output=True, text=True, env=e).stdout.strip()}"
         f"  ({time.time() - t:.0f} s)")

    # 2. environnement MFA
    t = time.time()
    mfa = f"{env}/{SOUS_BIN}/{NOM_MFA}"
    if os.path.exists(mfa):
        dire("[2/3] Environnement MFA déjà créé, étape sautée.")
    else:
        dire("[2/3] Création de l'environnement MFA (conda-forge, variante processeur, ~1 Go)...")
        cmd = [exe, "--no-rc", "create", "-p", env, "-c", "conda-forge", "--override-channels",
               "montreal-forced-aligner"] + ([] if a.cuda or sys.platform == "darwin" else ["kaldi=*=cpu*"]) + ["-y"]
        r = subprocess.run(cmd, env=e)
        if r.returncode != 0:
            dire("      Échec. Nouvel essai avec --ssl-no-revoke (pare-feu / antivirus qui coupe la vérification de révocation)...")
            r = subprocess.run(cmd[:2] + ["--ssl-no-revoke"] + cmd[2:], env=e)
        if r.returncode != 0:
            sys.exit("Création de l'environnement impossible. Si l'erreur parle de SSL : "
                     "définir MAMBA_SSL_VERIFY=<chemin du certificat de l'établissement> puis relancer.")
        shutil.rmtree(f"{mamba_root}/pkgs", ignore_errors=True)  # le cache de paquets n'est plus utile
    dire(f"      env-mfa prêt ({time.time() - t:.0f} s)")

    oublier_enregistrement(env)

    # 3. modèles
    t = time.time()
    pm = f"{mfa_root}/pretrained_models"
    deja = all(os.path.exists(f"{pm}/{k}/french_mfa.{x}") for k, x in (("acoustic", "zip"), ("dictionary", "dict"), ("g2p", "zip")))
    if a.sans_modeles:
        dire("[3/3] Modèles sautés (--sans-modeles).")
    elif deja:
        dire("[3/3] Modèles français déjà présents, étape sautée.")
    else:
        dire("[3/3] Modèles français (acoustique, dictionnaire, g2p)...")
        chemins = [env, f"{env}/Scripts", f"{env}/Library/bin"] if WINDOWS else [f"{env}/bin"]
        e2 = dict(e, PATH=os.pathsep.join(chemins + [e["PATH"]]))
        for kind in ("acoustic", "dictionary", "g2p"):
            r = subprocess.run([mfa, "model", "download", kind, "french_mfa"], env=e2,
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            sortie = (r.stdout + r.stderr).strip().splitlines()
            dire(f"      {kind} : {'OK' if r.returncode == 0 else 'ECHEC'} {sortie[-1][:140] if sortie else ''}")
    dire(f"      modèles ({time.time() - t:.0f} s)")

    dire("\nRésumé")
    tot = 0
    for nom, ch in (("outils (micromamba)", outils), ("environnement env-mfa", env),
                    ("modèles MFA", mfa_root), ("cache mamba", mamba_root)):
        p = poids(ch)
        tot += p
        dire(f"  {nom:24s} {go(p)}")
    shutil.rmtree(tmp, ignore_errors=True)
    dire(f"  {'TOTAL':24s} {go(tot)}")
    dire(f"Durée totale : {time.time() - t0:.0f} s")
    dire(f"Commande MFA : {mfa}  (variable MFA_ROOT_DIR={mfa_root})")
    if a.maj_config:
        chemin = a.config or CONFIG_SKILL
        conf = json.load(open(chemin, encoding="utf-8")) if os.path.exists(chemin) else {}
        conf["mfa"] = {"micromamba": exe, "env": env, "modeles": mfa_root, "root": mamba_root}
        conf.setdefault("horodatage", "mfa")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(conf, f, ensure_ascii=False, indent=2)
            f.write("\n")
        dire(f"config.json mis à jour (clé « mfa ») : {os.path.abspath(chemin)}")


if __name__ == "__main__":
    main()
