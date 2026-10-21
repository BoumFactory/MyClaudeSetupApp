"""Voix de synthèse locale à partir d'un script découpé en temps forts.

Moteur Piper (voix de SECOURS depuis le 20/10/2026) : voix françaises natives (siwis, tom, upmc), gratuites et
locales, sur processeur, quasi instantanées. Voix par défaut : Pocket TTS, voix_pocket.py (mêmes entrées et sorties,
voix clonable).

Usage :
    python voix.py <dossier_capsule> [--voix-piper siwis]
    python voix.py <dossier_capsule> --seulement b07,b12        # régénérer deux phrases

Entrée : <dossier>/script.md, sections « ## id [pause s] » suivies du texte à dire.
Sortie : <dossier>/audio.wav (voix assemblée, silences compris, PCM 16 bits)
         <dossier>/voix/<id>.wav (une phrase par fichier)
         <dossier>/data/temps-forts.json|js  {id, texte, texte_dit, debut, fin}

Les nombres, pourcentages et décimaux sont dits en mots (num2words) ; le script garde les chiffres.
Si Piper manque dans l'interpréteur courant, le script se relance avec le Python
"python_voix" (à défaut "python_tts") de config.json.
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
from commun import CONF, conf_requise  # noqa: E402  (poids des modèles sur le lecteur choisi : HF_HOME)


def relancer_si_besoin():
    try:
        __import__("piper")
        return
    except ImportError:
        pass
    py = CONF.get("python_voix") or CONF.get("python_tts")
    if not py or not os.path.exists(py) or os.path.abspath(py) == os.path.abspath(sys.executable):
        sys.exit("piper introuvable : l'installer, ou renseigner son Python dans config.json")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    sys.exit(subprocess.call([py, str(pathlib.Path(__file__).resolve())] + sys.argv[1:], env=env))


def lire_script(chemin):
    """Sections « ## id [pause s] [lent f] » : pause après le temps fort, débit ralenti d'un facteur f (calculs)."""
    blocs, cour = [], None
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+([A-Za-z]\d+[a-z]?)(\s.*)?$", ligne)
        if not m and ligne.startswith("#"):
            cour = None  # titre ou section hors temps forts (« Choix didactiques ») : jamais dit
            continue
        if m:
            options = m.group(2) or ""
            pause = re.search(r"\[pause\s+([\d.]+)\]", options)
            lent = re.search(r"\[lent\s+([\d.]+)\]", options)
            cour = {"id": m.group(1), "pause": float(pause.group(1)) if pause else 0.5,
                    "lent": float(lent.group(1)) if lent else 1.0, "lignes": []}
            blocs.append(cour)
        elif cour is not None and ligne.strip():
            cour["lignes"].append(ligne.strip())
    return [{"id": b["id"], "pause": b["pause"], "lent": b["lent"], "texte": " ".join(b["lignes"])} for b in blocs]


# Prononciation des noms de points et de variables (mesuré sur la phonémisation de Piper fr, 03/10/2026) :
#   - « y » / « Y » isolés sont lus « i » (iʲ) → « i grec » ;
#   - « A » isolé suivi d'un mot n'est pas accentué (a au lieu de ˈa) et se fond avec la voyelle suivante
#     (« le point A a » → « a a », effet haché) → « ha », toujours accentué. « ha » (h aspiré) et non « ah » :
#     devant « ah », Piper fait la liaison (« les droites ah I » → « droites-z-ah », « sommet-t-ah ») ; devant
#     « ha », aucune liaison (mesuré le 09/10/2026) ;
#   - « I » isolé devant un mot à voyelle initiale devient une semi-voyelle (iʲ) qui s'enchaîne au mot suivant
#     (« les droites A I et B C » entendu « les droites assies et B C ») → virgule après « I » (ˈi, e), 09/10/2026.
#   Les autres lettres sont justes.
# Un dictionnaire propre à la capsule (prononciation.json : {"écrit": "dit"}) complète ces règles.
PRONOMS_Y = {"il", "elle", "on", "ils", "elles", "n'", "j'", "s'", "l'", "m'", "t'", "nous", "vous", "qu'"}
VERBES_Y = {"a", "avait", "aura", "aurait", "ait", "ont", "va", "vont", "allons", "allez", "aller", "est", "sont"}


def lettres_pour_l_oreille(t, dico=None, piper=True):
    for ecrit, dit in (dico or {}).items():
        t = re.sub(rf"(?<![\wÀ-ÿ'-]){re.escape(ecrit)}(?![\wÀ-ÿ'-])", dit, t)
    if not piper:
        return t  # les rustines ci-dessous corrigent la phonémisation de Piper, pas celle de Pocket TTS
    t = re.sub(r"(?<![\wÀ-ÿ'-])A(?![\wÀ-ÿ'-])", "ha", t)
    t = re.sub(r"(?<![\wÀ-ÿ'-])I(?=\s+[aeiouyàâéèêëîïôûAEIOUÉÈÊ])", "I,", t)
    t = re.sub(r"(?<![\wÀ-ÿ'-])Y(?![\wÀ-ÿ'-])", "i grec", t)

    def y_math(m):
        avant = re.findall(r"[\wÀ-ÿ']+'?$", t[:m.start()].rstrip())
        apres = re.match(r"\s*([\wÀ-ÿ]+)", t[m.end():])
        if (avant and avant[0].lower() in PRONOMS_Y) or t[:m.start()].endswith("'") \
                or (apres and apres.group(1).lower() in VERBES_Y):
            return m.group(0)  # pronom « y » : « il y a », « n'y va »
        return "i grec"
    return re.sub(r"(?<![\wÀ-ÿ'-])y(?![\wÀ-ÿ'-])", y_math, t)


def pour_l_oreille(texte, dico=None, piper=True):
    """Lettres puis chiffres → mots, en français (0,625 → zéro virgule six cent vingt-cinq ; 40 % → quarante pour cent).
    piper=False (voix_pocket.py) : sans les rustines propres à Piper (« ha », « i grec », « plusse », virgule après I)."""
    from num2words import num2words
    texte = lettres_pour_l_oreille(texte, dico, piper)

    def decimal(m):
        entier, frac = m.group(1), m.group(2)
        zeros = len(frac) - len(frac.lstrip("0"))
        reste = frac.lstrip("0")
        mots = num2words(int(entier), lang="fr") + " virgule " + " ".join(["zéro"] * zeros)
        return (mots + (" " + num2words(int(reste), lang="fr") if reste else "")).strip()

    t = texte.replace("«", "").replace("»", "").replace("×", " fois ")
    # milliers écrits avec une espace (« 3 200 », « 12 500 ») : un seul nombre, sinon « trois deux cents » (20/10/2026)
    t = re.sub(r"(?<![\d,])\d{1,3}(?:[   ]\d{3})+(?!\d)",
               lambda m: re.sub(r"[   ]", "", m.group(0)), t)
    t = re.sub(r"(\d+),(\d+)", decimal, t)
    t = re.sub(r"\s*%", " pour cent", t)
    # « 1 tuile » → « une tuile », « 21 unités » → « vingt et une » (num2words ne connaît que le masculin)
    t = re.sub(rf"\b(\d+)(?=\s+(?:{NOMS_FEMININS})s?\b)",
               lambda m: re.sub(r"\bun$", "une", num2words(int(m.group(1)), lang="fr")), t)
    t = re.sub(r"\d+", lambda m: num2words(int(m.group(0)), lang="fr"), t)
    if piper:
        t = plus_operateur(t)
    # Majuscule en début de phrase : un chiffre converti (« six unités ») commence par une minuscule, et Piper
    # ne coupe alors pas la phrase (« trop court. six unités » dit d'une traite, sans silence). 13/10/2026.
    t = re.sub(r"(^|[.!?]\s+)([a-zà-ÿ])", lambda m: m.group(1) + m.group(2).upper(), t)
    return re.sub(r"\s+", " ", t).strip()


# Noms féminins qui suivent souvent un nombre dans les capsules de maths (« 1 tuile », « 1 unité »).
NOMS_FEMININS = ("tuile|unité|paire|ligne|colonne|rangée|case|valeur|solution|équation|expression|"
                 "fraction|droite|minute|seconde|heure|part|face|pièce|carte|boule|question|étape|façon")
MOTS_NOMBRES = ("zéro|une?|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|"
                "quinze|seize|vingt|trente|quarante|cinquante|soixante|cent|mille|moins|x|i grec|l'opposé")


def plus_operateur(t):
    """« plus » opérateur se dit [plys] : Piper dit « ply » (« trois plus deux » → tʁwa ply dø) et lie
    devant voyelle (« plus un » → plyz œ̃). Mesuré le 13/10/2026. « plusse » est phonémisé plˈys.
    Opérateur = suivi d'un nombre, d'une lettre seule, de « moins », d'une parenthèse ; et « de plus » en fin."""
    # signe d'un relatif ou opérateur, y compris en début de phrase (« Plus deux plus plus trois »)
    # et devant « les » (« quatre tuiles, plus les trois du départ ») ; « la plus grande » reste [ply]
    t = re.sub(rf"\b([Pp])lus(?=\s+(?:(?:{MOTS_NOMBRES}|plus|Plus|les)\b|[a-zA-Z]\b|\())", r"\1lusse", t)
    return re.sub(r"\bde plus(?=\s*[.,;:!?]|\s*$)", "de plusse", t)


class Piper:
    def __init__(self, voix):
        from piper import PiperVoice
        dossier = conf_requise("voix_piper", "voix Piper de secours")
        self.v = PiperVoice.load(str(pathlib.Path(dossier) / f"fr_FR-{voix}-medium.onnx"))

    def dire(self, texte, sortie, a, lent=1.0):
        """Une phrase après l'autre, séparées par un silence : Piper les enchaîne sinon sans respirer
        (« 5 unités, c'est trop court. 6 unités, c'est trop long. » dit d'une traite)."""
        from piper import SynthesisConfig
        conf = SynthesisConfig(length_scale=lent * a.debit)
        with wave.open(str(sortie), "wb") as w:
            premier = True
            for ch in self.v.synthesize(texte, syn_config=conf):
                if premier:
                    w.setframerate(ch.sample_rate); w.setsampwidth(ch.sample_width); w.setnchannels(ch.sample_channels)
                else:
                    w.writeframes(b"\x00" * (int(a.silence_phrase * ch.sample_rate) * ch.sample_width * ch.sample_channels))
                w.writeframes(ch.audio_int16_bytes)
                premier = False


def assembler(d, dv, blocs):
    """Phrases + silences → audio.wav ; renvoie la durée totale. Bornes exactes de chaque temps fort."""
    params, morceaux, t = None, [], 0.0
    for b in blocs:
        with wave.open(str(dv / f"{b['id']}.wav"), "rb") as w:
            p = w.getparams()
            if params is None:
                params = p
                silence = lambda s: b"\x00" * (int(s * p.framerate) * p.sampwidth * p.nchannels)  # noqa: E731
                morceaux.append(silence(0.25))
                t = 0.25
            elif (p.framerate, p.sampwidth, p.nchannels) != (params.framerate, params.sampwidth, params.nchannels):
                sys.exit(f"{b['id']}.wav n'a pas le même format que les autres phrases : la régénérer")
            morceaux.append(w.readframes(p.nframes))
            b["debut"] = round(t, 3)
            t += p.nframes / p.framerate
            b["fin"] = round(t, 3)
        morceaux.append(silence(b["pause"]))
        t += b["pause"]
    with wave.open(str(d / "audio.wav"), "wb") as w:
        w.setparams(params)
        w.writeframes(b"".join(morceaux))
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dossier")
    ap.add_argument("--script", default="script.md")
    ap.add_argument("--voix-piper", default="siwis", help="siwis (femme) | tom | upmc (hommes)")
    ap.add_argument("--seulement", default="", help="ids à régénérer, séparés par des virgules")
    ap.add_argument("--modifies", action="store_true",
                    help="régénérer seulement les temps forts dont le texte dit, le débit ou la voix a changé")
    ap.add_argument("--dossier-voix", default="voix", help="sous-dossier des phrases (pour comparer des voix)")
    # Débit et respiration : réglages par défaut demandés le 13/10/2026 (« débit moins rapide, pauses un peu
    # plus marquées, sans que ça devienne chiant »). Changer ces valeurs impose de tout régénérer (pas --modifies).
    ap.add_argument("--debit", type=float, default=1.1, help="ralentissement global (length_scale), multiplie [lent]")
    ap.add_argument("--silence-phrase", type=float, default=0.45, help="silence entre deux phrases d'un temps fort (s)")
    ap.add_argument("--pause-en-plus", type=float, default=0.2, help="ajouté à chaque [pause] entre temps forts (s)")
    a = ap.parse_args()
    relancer_si_besoin()

    d = pathlib.Path(a.dossier)
    dv = d / a.dossier_voix
    dv.mkdir(parents=True, exist_ok=True)
    (d / "data").mkdir(exist_ok=True)
    blocs = lire_script(d / a.script)
    dico_f = d / "prononciation.json"
    dico = json.loads(dico_f.read_text(encoding="utf-8")) if dico_f.exists() else {}
    voix_id = a.voix_piper
    for b in blocs:
        b["texte_dit"] = pour_l_oreille(b["texte"], dico)
        b["voix"] = voix_id
        b["pause"] = round(b["pause"] + a.pause_en_plus, 3)
    if a.modifies:
        # ne régénérer que ce qui a changé depuis la dernière synthèse : texte dit, débit, voix, ou phrase absente
        ancien_f = d / "data" / "temps-forts.json"
        ancien = {x["id"]: x for x in json.loads(ancien_f.read_text(encoding="utf-8"))} if ancien_f.exists() else {}
        a_faire = {b["id"] for b in blocs if not (dv / f"{b['id']}.wav").exists() or b["id"] not in ancien
                   or any(ancien[b["id"]].get(k, {"lent": 1.0, "voix": voix_id}.get(k)) != b[k]
                          for k in ("texte_dit", "lent", "voix"))}
        print(f"Temps forts modifiés : {', '.join(sorted(a_faire)) or 'aucun'}")
    else:
        a_faire = set(filter(None, a.seulement.split(","))) or {b["id"] for b in blocs}

    t0 = time.time()
    moteur = Piper(a.voix_piper)
    print(f"Voix Piper {a.voix_piper} chargée en {time.time() - t0:.0f} s")

    for b in blocs:
        if b["id"] not in a_faire:
            continue
        sortie = dv / f"{b['id']}.wav"
        t1 = time.time()
        moteur.dire(b["texte_dit"], sortie, a, b["lent"])
        with wave.open(str(sortie), "rb") as w:
            duree = w.getnframes() / w.getframerate()
        print(f"  {b['id']}  {duree:5.1f} s audio en {time.time() - t1:4.1f} s  | {b['texte_dit'][:70]}")

    manquants = [b["id"] for b in blocs if not (dv / f"{b['id']}.wav").exists()]
    if manquants:
        print(f"Assemblage différé : phrases manquantes {', '.join(manquants)}")
        return

    total = assembler(d, dv, blocs)
    tf = [{k: b[k] for k in ("id", "texte", "texte_dit", "lent", "voix", "debut", "fin")} for b in blocs]
    (d / "data" / "temps-forts.json").write_text(json.dumps(tf, ensure_ascii=False, indent=1), encoding="utf-8")
    # chargeable en file:// par la page : ancres '@b10', '@b10~"fait"' (aligner.py y ajoute les mots)
    (d / "data" / "temps-forts.js").write_text(
        "window.TEMPS_FORTS = " + json.dumps(tf, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"OK audio.wav : {total:.1f} s, {len(blocs)} temps forts, synthèse en {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
