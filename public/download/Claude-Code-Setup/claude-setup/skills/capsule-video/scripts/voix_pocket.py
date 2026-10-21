"""Voix de synthèse Pocket TTS (Kyutai) : moteur par défaut du skill, clonage de voix possible.

Mêmes entrées et sorties que voix.py (Piper, voix de secours). Une voix PAR TEMPS FORT.

Usage :
    python voix_pocket.py <dossier_capsule>                       # tout générer (voix par défaut de config.json)
    python voix_pocket.py <dossier_capsule> --seulement b07,b12   # régénérer deux temps forts
    python voix_pocket.py <dossier_capsule> --modifies            # ne refaire que ce qui a changé (ou reprendre après un arrêt)
    python voix_pocket.py <dossier_capsule> --modele french       # modèle 2 fois plus rapide, un peu moins bon

Entrée : <dossier>/script.md, sections « ## id [voix] [pause s] » suivies du texte à dire.
    ## b01 [pause 0.6]            voix par défaut (config.json : voix_pocket_defaut, ou --voix)
    ## b07 [estelle] [pause 0.5]  voix du catalogue Pocket (estelle, peter_yearsley, cosette, marius, javert…)
    ## b09 [ma-voix]               alias d'une voix clonée, déclaré dans config.json (« voix_clonees »)
    [lent f] est ignoré : Pocket n'a pas de réglage de débit (le débit est celui de la voix ou de l'échantillon cloné).
Sortie : <dossier>/audio.wav (voix assemblée, silences compris, PCM 16 bits, 44,1 kHz mono)
         <dossier>/voix/<id>.wav (un fichier par temps fort, nivelé)
         <dossier>/data/temps-forts.json|js  {id, texte, texte_dit, lent, voix, debut, fin}
         <dossier>/data/fidelite-voix.json   bilan du contrôle de fidélité (essais, écarts) : à lire avant de rendre
         <dossier>/voix-brut/                candidats de chaque essai et état (reprise) : supprimable une fois la capsule validée

Contrôle de fidélité À LA DEMANDE : désactivé par défaut (un seul essai par temps fort) ; actif avec --controle ou
si config.json contient "controle_fidelite_auto": true. Quand il est actif, chaque temps fort est généré phrase par
phrase, puis réécouté SANS indice de texte (controle_fidelite.py) : Parakeet
ONNX sur processeur par défaut (--controle, clé asr_fidelite), Whisper en arbitre des seuls temps forts signalés
(--arbitre, clé arbitre_fidelite). Les modèles de contrôle sont chargés UNE fois, dans un serveur qui sert toutes
les manches. Un mot sauté, ajouté ou changé relance un essai (3 au plus, --essais) ; le meilleur candidat est gardé.
Pocket est variable d'un essai à l'autre (mot avalé, mot ajouté) : le contrôle sert quand l'utilisateur signale un mot mal dit.
Le texte dit réutilise pour_l_oreille de voix.py (nombres, pourcentages, décimaux en mots) SANS les rustines de Piper ;
les corrections de mots sont dans <capsule>/prononciation.json {"écrit": "dit"}.
Aucun étirement de l'audio (jugé robotique). Voix nivelées à -16 LUFS, une voix après l'autre.

Si Pocket TTS manque dans l'interpréteur courant, le script se relance avec "python_pocket" de config.json (-X utf8).
Mode --brut-seulement : utilisé par assembler_voix.py (voix mixtes prof + Pocket), sans assemblage.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import wave

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from commun import CONF  # noqa: E402  (HF_HOME = cache des modèles sur le lecteur choisi)

VOIX_PIPER = {"tom", "siwis", "upmc"}
HORS_POCKET = VOIX_PIPER | {"prof"}  # étiquettes des voix mixtes : jamais synthétisées par Pocket


def relancer_si_besoin():
    try:
        __import__("pocket_tts")
        return
    except ImportError:
        pass
    py = CONF.get("python_pocket")
    if not py or not os.path.exists(py) or os.path.abspath(py) == os.path.abspath(sys.executable):
        sys.exit("pocket_tts introuvable : installer Pocket TTS (installation/LISEZMOI.md), puis renseigner son Python "
                 "dans config.json (clé python_pocket). Voix de secours : voix.py (Piper).")
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    sys.exit(subprocess.call([py, "-X", "utf8", str(pathlib.Path(__file__).resolve())] + sys.argv[1:], env=env))


def lire_script(chemin, defaut):
    """Sections « ## id [voix] [pause s] [lent f] ». Lignes « > » (notes, visuels) ignorées."""
    blocs, cour = [], None
    for num, ligne in enumerate(pathlib.Path(chemin).read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^##\s+([A-Za-z]\d+[a-z]?)(\s.*)?$", ligne)
        if not m and ligne.startswith("#"):
            cour = None  # titre ou section hors temps forts (« Choix didactiques ») : jamais dit
            continue
        if m:
            options = m.group(2) or ""
            pause = re.search(r"\[pause\s+([\d.]+)\]", options)
            lent = re.search(r"\[lent\s+([\d.]+)\]", options)
            etiquettes = re.findall(r"\[([A-Za-z_][\w-]*)\]", options)
            if len(etiquettes) > 1:
                sys.exit(f"{chemin} ligne {num} : le temps fort {m.group(1)} a plusieurs étiquettes de voix {etiquettes}.")
            voix = etiquettes[0] if etiquettes else defaut
            cour = {"id": m.group(1), "voix": voix, "pause": float(pause.group(1)) if pause else 0.5,
                    "lent": float(lent.group(1)) if lent else 1.0, "lignes": []}
            blocs.append(cour)
        elif cour is not None and ligne.strip() and not ligne.lstrip().startswith(">"):
            cour["lignes"].append(ligne.strip())
    res = [{"id": b["id"], "voix": b["voix"], "pause": b["pause"], "lent": b["lent"], "texte": " ".join(b["lignes"])}
           for b in blocs]
    vides = [b["id"] for b in res if not b["texte"]]
    if vides:
        sys.exit(f"Temps forts sans texte : {', '.join(vides)}")
    ids = [b["id"] for b in res]
    doubles = sorted({i for i in ids if ids.count(i) > 1})
    if doubles:
        sys.exit(f"Identifiants de temps forts en double : {', '.join(doubles)}")
    return res


def resoudre_voix(etiquette):
    """Étiquette → (référence donnée à Pocket, empreinte pour détecter un changement).
    Alias de voix clonée (config.json « voix_clonees ») → fichier ; sinon nom du catalogue Pocket."""
    clones = CONF.get("voix_clonees") or {}
    if etiquette in clones:
        ech = clones[etiquette].get("echantillon", "")
        if not ech or not os.path.exists(ech):
            sys.exit(f"Voix clonée « {etiquette} » : échantillon introuvable ({ech or 'non renseigné'}). "
                     f"Voir references/cloner-sa-voix.md ; en attendant, utiliser une voix du catalogue.")
        return ech, f"{etiquette}|{ech}|{int(os.path.getmtime(ech))}"
    from pocket_tts.utils.utils import _ORIGINS_OF_PREDEFINED_VOICES
    if etiquette not in _ORIGINS_OF_PREDEFINED_VOICES:
        sys.exit(f"Voix « {etiquette} » inconnue. Catalogue Pocket : {', '.join(sorted(_ORIGINS_OF_PREDEFINED_VOICES))}. "
                 f"Voix clonées déclarées : {', '.join(sorted(clones)) or 'aucune'}.")
    return etiquette, etiquette


def duree_wav(chemin):
    with wave.open(str(chemin), "rb") as w:
        return w.getnframes() / w.getframerate()


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def sonie(fichiers):
    """Sonie intégrée (LUFS) de la mise bout à bout de fichiers mono 44,1 kHz."""
    entrees = []
    for f in fichiers:
        entrees += ["-i", str(f)]
    chaine = "".join(f"[{k}:a]" for k in range(len(fichiers))) + f"concat=n={len(fichiers)}:v=0:a=1,ebur128=framelog=quiet"
    r = subprocess.run(["ffmpeg", "-v", "info", *entrees, "-filter_complex", chaine, "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    t = re.findall(r"I:\s+(-?[\d.]+)\s+LUFS", r.stderr)
    return float(t[-1]) if t else None


def generer(tts, etat_voix, texte, sortie, silence_phrase, graine):
    """Phrase par phrase, silence entre elles, blancs de tête et de queue rognés (reproductible par la graine)."""
    import numpy as np
    import scipy.io.wavfile
    import torch
    torch.manual_seed(graine)
    phrases = [p for p in re.split(r"(?<=[.!?])\s+", texte) if p.strip()]
    sr = tts.sample_rate
    morceaux = []
    for k, p in enumerate(phrases):
        a = tts.generate_audio(etat_voix, p).numpy().astype("float32")
        idx = np.where(np.abs(a) > 0.01)[0]
        if len(idx):
            marge = int(0.06 * sr)
            a = a[max(0, idx[0] - marge): idx[-1] + marge]
        if k:
            morceaux.append(np.zeros(int(silence_phrase * sr), dtype="float32"))
        morceaux.append(a)
    audio = np.concatenate(morceaux)
    scipy.io.wavfile.write(str(sortie), sr, (np.clip(audio, -1, 1) * 32767).astype("int16"))


def controler(controleur, candidats, etat, etat_f):
    """Contrôle de fidélité de {cle: {fichier, texte_dit}} par le serveur persistant (Parakeet par défaut, arbitre
    Whisper facultatif : voir controle_fidelite.py) ; range les résultats dans etat."""
    try:
        res = controleur.controler(candidats)
    except RuntimeError as e:
        sys.exit(f"Contrôle de fidélité impossible : {e} (--sans-controle pour passer outre, sans garantie de fidélité).")
    for cle, v in res.items():
        bid, n = cle.split("|")
        for e in etat[bid]["essais"]:
            if e["n"] == int(n):
                e.update({k: v[k] for k in ("transcrit", "erreurs", "flous", "details", "moteur")})
                if "autre" in v:
                    e["autre"] = v["autre"]
        print(f"  {cle}: {v['erreurs']} erreur(s), {v['flous']} flou(s) [{v['moteur']}]", flush=True)
    etat_f.write_text(json.dumps(etat, ensure_ascii=False, indent=1), encoding="utf-8")


def meilleur(entree):
    """Candidat retenu : le moins d'erreurs, puis le moins d'écarts flous, puis le plus ancien. Sans contrôle : le dernier."""
    controles = [e for e in entree["essais"] if "erreurs" in e]
    if not controles:
        return entree["essais"][-1]
    return min(controles, key=lambda e: (e["erreurs"], e["flous"], e["n"]))


def niveler(blocs, d, etat, cible):
    """Chaque voix est amenée à la même sonie (une voix après l'autre : estelle et un clone ne sortent pas au même niveau)."""
    dv, tmp = d / "voix", d / "voix-brut"
    dv.mkdir(exist_ok=True)
    for b in blocs:
        e = meilleur(etat[b["id"]])
        b["essai"] = e["n"]
        ffmpeg("-i", str(d / e["fichier"]), "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(tmp / f"{b['id']}-44k.wav"))
    gains = {}
    for v in sorted({b["voix"] for b in blocs}):
        i = sonie([tmp / f"{b['id']}-44k.wav" for b in blocs if b["voix"] == v])
        gains[v] = (cible - i) if i is not None else 0.0
        if i is not None:
            print(f"Sonie {v} : {i:.1f} LUFS -> gain {gains[v]:+.1f} dB (cible {cible} LUFS)")
    for b in blocs:
        f44 = tmp / f"{b['id']}-44k.wav"
        dur = duree_wav(f44)
        fd = min(0.006, dur / 4)
        filtre = (f"volume={gains[b['voix']]:.2f}dB,alimiter=limit=0.89:level=disabled,afade=t=in:st=0:d={fd:.4f},"
                  f"afade=t=out:st={max(0.0, dur - fd):.4f}:d={fd:.4f}")
        ffmpeg("-i", str(f44), "-af", filtre, "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(dv / f"{b['id']}.wav"))


def assembler(blocs, d):
    """Phrases + silences -> audio.wav ; renvoie la durée totale. Bornes exactes de chaque temps fort."""
    dv = d / "voix"
    sil = lambda s: b"\x00" * (int(round(s * 44100)) * 2)  # noqa: E731
    morceaux, t = [sil(0.25)], 0.25
    for b in blocs:
        with wave.open(str(dv / f"{b['id']}.wav"), "rb") as w:
            morceaux.append(w.readframes(w.getnframes()))
            b["debut"] = round(t, 3)
            t += w.getnframes() / w.getframerate()
            b["fin"] = round(t, 3)
        morceaux.append(sil(b["pause"]))
        t += b["pause"]
    with wave.open(str(d / "audio.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes(b"".join(morceaux))
    return t


def ecrire_bilan(blocs, d, etat, modele, controle=None):
    lignes = {}
    for b in blocs:
        e = meilleur(etat[b["id"]])
        lignes[b["id"]] = {"voix": b["voix"], "essais": len(etat[b["id"]]["essais"]), "retenu": e["n"],
                           "duree_s": e["duree_brute"], "erreurs": e.get("erreurs"), "flous": e.get("flous"),
                           "transcrit": e.get("transcrit"), "moteur": e.get("moteur", "whisper" if "erreurs" in e else None),
                           "ecarts": e.get("details", [])}
        if e.get("autre"):
            lignes[b["id"]]["autre_moteur"] = e["autre"]
    controles = [v for v in lignes.values() if v["erreurs"] is not None]
    # « controle_whisper » : nom historique de la clé, vrai dès qu'un contrôle (Parakeet ou Whisper) a eu lieu
    bilan = {"modele": modele, "controle_whisper": bool(controles), "controle": controle,
             "genere_le": time.strftime("%Y-%m-%d %H:%M"),
             "temps_forts": len(lignes), "sans_erreur": sum(v["erreurs"] == 0 for v in controles),
             "a_ecouter": [k for k, v in lignes.items() if v["erreurs"]],
             "essais_total": sum(v["essais"] for v in lignes.values()),
             "note": "La reconnaissance vérifie les mots, pas la qualité d'écoute : un « flou » est souvent un homophone ou "
                     "un nom propre ; Parakeet signale aussi quelques fausses alertes (l'arbitre Whisper en lève une partie). "
                     "Le jugement final se fait à l'oreille.", "blocs": lignes}
    (d / "data").mkdir(exist_ok=True)
    (d / "data" / "fidelite-voix.json").write_text(json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")
    return bilan


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossier")
    ap.add_argument("--script", default="script.md")
    ap.add_argument("--voix", default=None, help="voix des temps forts sans étiquette (défaut : voix_pocket_defaut de config.json)")
    ap.add_argument("--modele", default=CONF.get("modele_pocket", "french_24l"),
                    help="french_24l (meilleur, ~temps réel sur processeur) | french (2 fois plus rapide, moins bon)")
    ap.add_argument("--essais", type=int, default=3, help="essais maximum par temps fort (contrôle de fidélité entre chaque manche)")
    ap.add_argument("--controle", nargs="?", const="auto", choices=("auto", "parakeet", "whisper"), default=None,
                    help="force le contrôle de fidélité ; moteur facultatif (défaut : asr_fidelite de config.json, parakeet). "
                         "Sans cette option, le contrôle n'a lieu que si controle_fidelite_auto vaut true dans config.json")
    ap.add_argument("--arbitre", default=None,
                    help="whisper | aucun : réécoute des seuls temps forts signalés (défaut : arbitre_fidelite de config.json)")
    ap.add_argument("--seulement", default="", help="ids à régénérer, séparés par des virgules")
    ap.add_argument("--modifies", action="store_true",
                    help="ne refaire que les temps forts dont le texte dit, la voix ou le modèle a changé (reprend aussi après un arrêt)")
    ap.add_argument("--sans-controle", action="store_true", help="un seul essai, sans contrôle de fidélité (déconseillé)")
    ap.add_argument("--silence-phrase", type=float, default=0.4, help="silence entre deux phrases d'un temps fort (s)")
    ap.add_argument("--pause-en-plus", type=float, default=0.2, help="ajouté à chaque [pause] entre temps forts (s)")
    ap.add_argument("--cible", type=float, default=-16.0, help="sonie visée de chaque voix (LUFS) : la voix brute sort à -33")
    ap.add_argument("--assembler-seulement", action="store_true", help="ne rien générer : renivelle et réassemble les meilleurs essais")
    ap.add_argument("--brut-seulement", action="store_true",
                    help="voix mixtes (assembler_voix.py) : génère les blocs Pocket, ni nivellement ni assemblage")
    a = ap.parse_args()
    relancer_si_besoin()

    d = pathlib.Path(a.dossier)
    brut = d / "voix-brut"
    brut.mkdir(parents=True, exist_ok=True)
    defaut = None if a.brut_seulement else (a.voix or CONF.get("voix_pocket_defaut") or "estelle")
    blocs = lire_script(d / a.script, defaut)
    if a.brut_seulement:
        pris = []
        for b in blocs:
            if b["voix"] is None:
                sys.exit(f"Temps fort {b['id']} sans étiquette de voix (obligatoire dans un script mixte).")
            if b["voix"] not in HORS_POCKET:
                pris.append(b)
        blocs = pris
        if not blocs:
            print("Aucun bloc Pocket dans ce script.")
            return
    dico_f = d / "prononciation.json"
    dico = json.loads(dico_f.read_text(encoding="utf-8")) if dico_f.exists() else {}

    import voix as voix_skill  # noqa: PLC0415  (voix.py : pour_l_oreille ; Piper n'est pas chargé)
    refs = {}
    for b in blocs:
        b["texte_dit"] = voix_skill.pour_l_oreille(b["texte"], dico, piper=False)
        if b["voix"] not in refs:
            refs[b["voix"]] = resoudre_voix(b["voix"])
        b["empreinte"] = f"{refs[b['voix']][1]}|{a.modele}"
        b["pause"] = round(b["pause"] + a.pause_en_plus, 3)

    etat_f = brut / "essais-pocket.json"
    etat = json.loads(etat_f.read_text(encoding="utf-8")) if etat_f.exists() else {}
    explicites = set(filter(None, a.seulement.split(",")))
    inconnus = explicites - {b["id"] for b in blocs}
    if inconnus:
        sys.exit(f"--seulement : temps forts inconnus {', '.join(sorted(inconnus))}")
    # Par défaut tout est régénéré ; --modifies, --seulement et --brut-seulement reprennent l'état existant
    # (un temps fort dont le texte dit, la voix ou le modèle a changé est toujours refait).
    tout_refaire = not (a.modifies or a.assembler_seulement or a.brut_seulement or explicites)
    for b in blocs:
        ancien = etat.get(b["id"])
        garder = ancien and ancien["texte_dit"] == b["texte_dit"] and ancien["voix"] == b["empreinte"]
        if not garder or tout_refaire or b["id"] in explicites:
            etat[b["id"]] = {"texte_dit": b["texte_dit"], "voix": b["empreinte"], "essais": []}
    # à produire : temps forts sans essai, puis (reprise après un arrêt) essais jamais contrôlés
    actifs = {b["id"] for b in blocs if not etat[b["id"]]["essais"] or any("erreurs" not in e for e in etat[b["id"]]["essais"])}
    if a.assembler_seulement:
        actifs = set()
    elif a.modifies or explicites:
        print(f"Temps forts à produire : {', '.join(sorted(actifs)) or 'aucun'}")

    t0 = time.time()
    maxi = 1 if (a.sans_controle or not (a.controle is not None or CONF.get("controle_fidelite_auto", False))) else a.essais
    pocket = {}  # modèle et états de voix, chargés au premier besoin (un état par voix, calculé une seule fois)

    def charger():
        if "tts" not in pocket:
            print(f"Chargement de Pocket TTS {a.modele} (1 à 5 min la première fois : poids à télécharger)…", flush=True)
            from pocket_tts import TTSModel
            pocket["tts"] = TTSModel.load_model(language=a.modele)
            pocket["voix"] = {}
            print(f"Modèle chargé en {time.time() - t0:.0f} s", flush=True)
        return pocket["tts"], pocket["voix"]

    # Contrôle : UN serveur par moteur pour toute la génération (modèle chargé une fois, pendant la synthèse)
    controleur = None
    controle_voulu = a.controle is not None or bool(CONF.get("controle_fidelite_auto", False))
    if not controle_voulu and not a.sans_controle:
        print("Contrôle de fidélité : désactivé (--controle pour le lancer, ou controle_fidelite_auto dans config.json)", flush=True)
    if controle_voulu and not a.sans_controle and actifs:
        from controle_fidelite import Controleur  # noqa: PLC0415
        try:
            controleur = Controleur(None if a.controle in (None, "auto") else a.controle, a.arbitre)
        except RuntimeError as e:
            sys.exit(f"Contrôle de fidélité impossible : {e} (--sans-controle pour passer outre).")
        controleur.demarrer()
        print(f"Contrôle de fidélité : {controleur.moteur}"
              + (f", arbitre {controleur.arbitre} sur les seuls temps forts signalés" if controleur.arbitre else ""), flush=True)
    try:
        boucle(a, d, blocs, etat, etat_f, actifs, refs, charger, maxi, controleur)
    finally:
        if controleur:
            controleur.fermer()

    manquants = [b["id"] for b in blocs if not etat[b["id"]]["essais"]]
    if manquants:
        sys.exit(f"Temps forts sans essai : {', '.join(manquants)}")
    nom_controle = None if not controleur else controleur.moteur + (f"+{controleur.arbitre}" if controleur.arbitre else "")
    finir(a, d, blocs, etat, brut, t0, nom_controle)


def boucle(a, d, blocs, etat, etat_f, actifs, refs, charger, maxi, controleur):
    # essais d'une exécution interrompue avant leur contrôle : les contrôler d'abord
    if controleur:
        en_attente = {f"{b['id']}|{e['n']}": {"fichier": str(d / e["fichier"]), "texte_dit": b["texte_dit"]}
                      for b in blocs if b["id"] in actifs for e in etat[b["id"]]["essais"] if "erreurs" not in e}
        if en_attente:
            controler(controleur, en_attente, etat, etat_f)
    while actifs:
        manche = [b for b in blocs if b["id"] in actifs and len(etat[b["id"]]["essais"]) < maxi
                  and not any(e.get("erreurs") == 0 for e in etat[b["id"]]["essais"])]
        if not manche:
            break
        tts, etats_voix = charger()
        cands = {}
        for b in manche:
            if b["voix"] not in etats_voix:  # l'état de chaque voix (clone compris) n'est calculé qu'une fois
                t1 = time.time()
                etats_voix[b["voix"]] = tts.get_state_for_audio_prompt(refs[b["voix"]][0])
                print(f"Voix {b['voix']} prête en {time.time() - t1:.0f} s", flush=True)
            n = len(etat[b["id"]]["essais"]) + 1
            rel = f"voix-brut/{b['id']}_e{n}.wav"
            t1 = time.time()
            graine = 1000 * n + int(re.sub(r"\D", "", b["id"]) or 0)
            generer(tts, etats_voix[b["voix"]], b["texte_dit"], d / rel, a.silence_phrase, graine)
            dur = duree_wav(d / rel)
            etat[b["id"]]["essais"].append({"n": n, "fichier": rel, "duree_brute": round(dur, 2)})
            cands[f"{b['id']}|{n}"] = {"fichier": str(d / rel), "texte_dit": b["texte_dit"]}
            print(f"  {b['id']} [{b['voix']}] essai {n} : {dur:5.1f} s audio en {time.time() - t1:4.0f} s", flush=True)
            etat_f.write_text(json.dumps(etat, ensure_ascii=False, indent=1), encoding="utf-8")
        if not controleur:
            break
        controler(controleur, cands, etat, etat_f)
        print("Bilan de la manche (erreurs de mots) :",
              {k: etat[k.split("|")[0]]["essais"][-1].get("erreurs") for k in cands}, flush=True)


def finir(a, d, blocs, etat, brut, t0, nom_controle):
    bilan = ecrire_bilan(blocs, d, etat, a.modele, nom_controle)
    if a.brut_seulement:
        sortie = {b["id"]: {"fichier": str(d / meilleur(etat[b["id"]])["fichier"]), "texte_dit": b["texte_dit"], "voix": b["voix"]}
                  for b in blocs}
        (brut / "pocket-bruts.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"OK {len(blocs)} blocs Pocket, bilan : data/fidelite-voix.json")
        return

    niveler(blocs, d, etat, a.cible)
    total = assembler(blocs, d)
    tf = [{k: b[k] for k in ("id", "texte", "texte_dit", "lent", "voix", "debut", "fin")} for b in blocs]
    (d / "data").mkdir(exist_ok=True)
    (d / "data" / "temps-forts.json").write_text(json.dumps(tf, ensure_ascii=False, indent=1), encoding="utf-8")
    # chargeable en file:// par la page : ancres '@b10', '@b10~"fait"' (aligner.py y ajoute les mots)
    (d / "data" / "temps-forts.js").write_text("window.TEMPS_FORTS = " + json.dumps(tf, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"\nOK audio.wav : {total:.1f} s, {len(blocs)} temps forts, {bilan['essais_total']} essais, "
          f"{time.time() - t0:.0f} s au total")
    if bilan["controle_whisper"]:
        print(f"Fidélité ({nom_controle or 'contrôle antérieur'}) : {bilan['sans_erreur']}/{len(blocs)} temps forts "
              f"sans mot sauté, ajouté ou changé")
    if bilan["a_ecouter"]:
        print("À ÉCOUTER (écart restant après les essais) : " + ", ".join(bilan["a_ecouter"])
              + " ; détail dans data/fidelite-voix.json. Corriger par prononciation.json ou reformuler, puis --seulement.")
    print("Puis TOUJOURS transcrire.py : les bornes changent à chaque synthèse.")


if __name__ == "__main__":
    main()
