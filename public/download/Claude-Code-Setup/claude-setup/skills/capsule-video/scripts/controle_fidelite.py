"""Contrôle de fidélité des voix de synthèse : un moteur de reconnaissance (SANS indice de texte) réécoute
chaque candidat, et le texte entendu est comparé au texte dit.

Moteurs (clé « asr_fidelite » de config.json, option --moteur) :
  parakeet  Parakeet TDT 0.6B v3 ONNX int8 sur processeur (défaut) : ≈ 0,5 s par temps fort, chargé en 3,5 s,
            sans CUDA. Un peu plus bavard que Whisper (quelques fausses alertes), jamais d'invention.
  whisper   Whisper large-v3 (carte graphique si disponible, sinon medium sur processeur) : ≈ 4 s par temps fort
            sur RTX 3060, ≈ 18 s sur processeur.
Arbitre (clé « arbitre_fidelite », option --arbitre) : les SEULS temps forts signalés par le moteur principal
sont réécoutés par l'autre moteur ; on garde le verdict qui trouve le moins d'erreurs (une vraie erreur de
synthèse est entendue par les deux, une fausse alerte est propre à un moteur).

Chaque moteur tourne dans SON Python (python_parakeet, python_asr) et n'est chargé qu'UNE fois par génération :
voix_pocket.py ouvre un serveur de contrôle (--serveur) qui reçoit toutes les manches.

Usages :
  python controle_fidelite.py --capsule <dossier> [--moteur parakeet] [--arbitre whisper|aucun]
        contrôle les voix déjà produites (voix/<id>.wav contre texte_dit de data/temps-forts.json), sans
        resynthèse ; bilan dans data/controle-fidelite.json
  python controle_fidelite.py entree.json sortie.json [--moteur parakeet]
        entree.json : {"cle": {"fichier": "chemin.wav", "texte_dit": "..."}} ; sortie.json : {"cle": {"transcrit": "..."}}
  python controle_fidelite.py --serveur --moteur parakeet      (lancé par ServeurControle, protocole sur stdin/stdout)

Un écart « flou » (mots proches par les lettres : nom propre ou homophone écrit autrement) est compté à part ;
un écart « erreur » est un mot sauté, ajouté ou remplacé par un mot différent.
Pourquoi sans indice : avec le texte en indice (initial_prompt), Whisper hallucine par moments
« Sous-titrage Société Radio-Canada » à la place de la phrase, et le contrôle ne vérifie plus rien.
"""
import argparse
import difflib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import unicodedata

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import commun  # noqa: E402  (HF_HOME = cache des modèles ; DLL CUDA installées par pip)

MOTEURS = ("parakeet", "whisper")


# ------------------------------------------------------------------ comparaison
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


ROMAIN_OK = re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")
VAL_ROMAIN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def _romain(s):
    total = 0
    for k, c in enumerate(s):
        v = VAL_ROMAIN[c]
        total += -v if k + 1 < len(s) and VAL_ROMAIN[s[k + 1]] > v else v
    return total


def normaliser(texte):
    """Écritures que les moteurs produisent autrement que le texte dit : π, exposants, ordinaux (« XVIIIe »,
    « 18e », « 1er ») remis en mots. Appliqué aux deux côtés de la comparaison."""
    t = texte.replace("π", " pi ").replace("²", " au carré").replace("³", " au cube")
    try:
        from num2words import num2words
    except ImportError:
        return t

    def ordinal_romain(m):
        r = m.group(1)
        seul = len(r) == 1
        if not ROMAIN_OK.match(r) or (seul and not re.match(r"\s+si[eè]cle", t[m.end():])):
            return m.group(0)  # « Le », « Ce », « De » ou point nommé C : jamais des chiffres romains
        n = _romain(r)
        return "premier" if n == 1 else num2words(n, lang="fr", to="ordinal")
    t = re.sub(r"\b([IVXLCDM]+)(?:e|ème|eme)\b", ordinal_romain, t)
    t = re.sub(r"\b1(?:er|re|ère)\b", "premier", t)
    t = re.sub(r"\b(\d+)(?:e|ème|eme)\b", lambda m: num2words(int(m.group(1)), lang="fr", to="ordinal"), t)
    return t


def jetons(texte):
    texte = normaliser(texte)
    try:
        from num2words import num2words
        texte = re.sub(r"(?<=\d)[\s  ](?=\d{3})", "", texte)
        texte = re.sub(r"\d+", lambda m: num2words(int(m.group(0)), lang="fr"), texte)
    except ImportError:
        pass  # chiffres laissés tels quels : le texte dit n'en contient normalement plus
    mots = [n for n in (norm(m) for m in re.split(r"[\s'’\-]+", texte)) if n]
    # lettres de suite (« O I » dit, « OI » écrit par le moteur) : un seul jeton des deux côtés
    res = []
    for m in mots:
        if res and len(m) == 1 and len(res[-1]) == 1 and res[-1].isalpha() and m.isalpha():
            res[-1] += m
        else:
            res.append(m)
    return res


# homophones qu'un moteur écrit au hasard (accents déjà retirés : à/a, où/ou sont égaux) : écart « flou »
HOMOPHONES = {frozenset(p) for p in (("ses", "ces"), ("ce", "se"), ("son", "sont"), ("on", "ont"), ("et", "est"),
                                     ("peu", "peut"), ("mes", "mais"), ("quel", "quelle"), ("tout", "tous"),
                                     ("cent", "sans"), ("vers", "verre"), ("pair", "paire"), ("aire", "ere"))}


def comparer(attendu, recu):
    a, b = jetons(attendu), jetons(recu)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    erreurs = flous = 0
    details = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        da, db = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        lettres = len(da) == 1 and len(db) == 1  # une lettre prise pour une autre (« j » entendu « g ») : le moteur hésite
        homophone = frozenset((da, db)) in HOMOPHONES
        if op == "replace" and (lettres or homophone or difflib.SequenceMatcher(a=da.replace(" ", ""), b=db.replace(" ", "")).ratio() >= 0.7):
            flous += 1
            details.append({"type": "flou", "attendu": da, "entendu": db})
        else:
            erreurs += max(i2 - i1, j2 - j1)
            details.append({"type": {"delete": "saute", "insert": "ajoute", "replace": "change"}[op],
                            "attendu": da, "entendu": db})
    return erreurs, flous, details


def comparer_transcrit(texte_dit, transcrit):
    """Remet l'écriture du moteur (« 0,625 », « 62,5% », « 3² ») en mots comme le texte dit, puis compare.
    Demande num2words (Python de Pocket ou de Parakeet)."""
    import voix as voix_skill  # noqa: PLC0415  (pour_l_oreille ; Piper n'est pas chargé)
    recu = voix_skill.pour_l_oreille(normaliser(transcrit), None, piper=False)
    return comparer(texte_dit, recu)


# ------------------------------------------------------------------ moteurs (dans le Python du moteur)
class Transcripteur:
    def __init__(self, moteur):
        self.moteur = moteur
        t0 = time.time()
        if moteur == "parakeet":
            import asr_parakeet
            self.m = asr_parakeet.charger()
        else:
            import asr_whisper
            self.m, _ = asr_whisper.charger("large-v3")
        print(f"Moteur de contrôle {moteur} chargé en {time.time() - t0:.1f} s", file=sys.stderr, flush=True)

    def transcrire(self, chemin):
        if self.moteur == "parakeet":
            import asr_parakeet
            return asr_parakeet.texte(self.m, chemin)
        segs, _ = self.m.transcribe(str(chemin), language="fr", beam_size=5, vad_filter=False,
                                    condition_on_previous_text=False)
        return " ".join(s.text.strip() for s in segs)


def serveur(moteur):
    """Protocole : une ligne JSON {"fichiers": {cle: chemin}} sur stdin → une ligne « @@RESULTAT {cle: texte} »
    sur stdout. Fin de stdin = fin du processus. Les messages vont sur stderr."""
    sys.stdin.reconfigure(encoding="utf-8")
    tr = Transcripteur(moteur)
    print("@@PRET", flush=True)
    for ligne in sys.stdin:
        if not ligne.strip():
            continue
        req = json.loads(ligne)
        out = {}
        for cle, chemin in req["fichiers"].items():
            out[cle] = tr.transcrire(chemin)
        print("@@RESULTAT " + json.dumps(out, ensure_ascii=False), flush=True)


# ------------------------------------------------------------------ côté appelant
def moteur_disponible(moteur):
    return commun.module_present(commun.MODULE_DE[moteur]) or commun.python_de(moteur) is not None


class ServeurControle:
    """Processus de contrôle persistant : le modèle est chargé une fois (dès la création, en parallèle du reste)
    et sert à toutes les manches. fermer() à la fin."""

    def __init__(self, moteur):
        py = commun.python_de(moteur)
        if not py:
            if not commun.module_present(commun.MODULE_DE[moteur]):
                raise RuntimeError(f"moteur {moteur} introuvable (clé {commun.PYTHON_DE[moteur]} de config.json)")
            py = sys.executable
        self.moteur = moteur
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        self.p = subprocess.Popen([py, "-X", "utf8", str(ICI / "controle_fidelite.py"), "--serveur", "--moteur", moteur],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf-8", errors="replace",
                                  env=env)
        self.pret = False

    def _lire(self, prefixe):
        while True:
            ligne = self.p.stdout.readline()
            if not ligne:
                raise RuntimeError(f"le serveur de contrôle {self.moteur} s'est arrêté (code {self.p.poll()})")
            if ligne.startswith(prefixe):
                return ligne[len(prefixe):]
            print(ligne, end="", flush=True)  # messages des bibliothèques : relayés tels quels

    def transcrire(self, fichiers):
        """{cle: chemin} → {cle: texte entendu}."""
        if not fichiers:
            return {}
        if not self.pret:
            self._lire("@@PRET")
            self.pret = True
        self.p.stdin.write(json.dumps({"fichiers": {k: str(v) for k, v in fichiers.items()}}, ensure_ascii=False) + "\n")
        self.p.stdin.flush()
        return json.loads(self._lire("@@RESULTAT "))

    def fermer(self):
        try:
            self.p.stdin.close()
            self.p.wait(timeout=60)
        except Exception:  # noqa: BLE001
            self.p.kill()


class Controleur:
    """Moteur principal + arbitre facultatif, serveurs ouverts au premier besoin et gardés jusqu'à fermer()."""

    def __init__(self, moteur=None, arbitre=None):
        moteur = moteur or commun.CONF.get("asr_fidelite") or "parakeet"
        if not moteur_disponible(moteur):
            autre = [m for m in MOTEURS if m != moteur and moteur_disponible(m)]
            if not autre:
                raise RuntimeError("aucun moteur de contrôle installé (python_parakeet ou python_asr de config.json)")
            print(f"Contrôle : {moteur} absent, repli sur {autre[0]}", flush=True)
            moteur = autre[0]
        if arbitre is None:
            arbitre = commun.CONF.get("arbitre_fidelite")
        if arbitre in ("", "aucun", "null", moteur) or (arbitre and not moteur_disponible(arbitre)):
            arbitre = None
        self.moteur, self.arbitre = moteur, arbitre
        self.serveurs = {}

    def demarrer(self):
        """Lance le chargement du moteur principal sans attendre (il se fait pendant la synthèse)."""
        self._serveur(self.moteur)

    def _serveur(self, m):
        if m not in self.serveurs:
            self.serveurs[m] = ServeurControle(m)
        return self.serveurs[m]

    def controler(self, candidats):
        """{cle: {fichier, texte_dit}} → {cle: {transcrit, erreurs, flous, details, moteur, [autre]}}."""
        t0 = time.time()
        bruts = self._serveur(self.moteur).transcrire({k: v["fichier"] for k, v in candidats.items()})
        res = {}
        for cle, txt in bruts.items():
            e, f, d = comparer_transcrit(candidats[cle]["texte_dit"], txt)
            res[cle] = {"transcrit": txt, "erreurs": e, "flous": f, "details": d, "moteur": self.moteur}
        print(f"  contrôle {self.moteur} : {len(bruts)} fichier(s) en {time.time() - t0:.1f} s", flush=True)
        signales = [k for k, v in res.items() if v["erreurs"]]
        if self.arbitre and signales:
            t0 = time.time()
            arb = self._serveur(self.arbitre).transcrire({k: candidats[k]["fichier"] for k in signales})
            leves = 0
            for cle, txt in arb.items():
                e, f, d = comparer_transcrit(candidats[cle]["texte_dit"], txt)
                principal = res[cle]
                autre = {"moteur": self.arbitre, "transcrit": txt, "erreurs": e, "flous": f, "details": d}
                if e < principal["erreurs"]:
                    leves += 1
                    res[cle] = dict(autre, autre={k: principal[k] for k in ("moteur", "transcrit", "erreurs", "flous", "details")})
                else:
                    principal["autre"] = autre
            print(f"  arbitre {self.arbitre} : {len(signales)} signalé(s) réécouté(s) en {time.time() - t0:.1f} s, "
                  f"{leves} fausse(s) alerte(s) levée(s)", flush=True)
        return res

    def fermer(self):
        for s in self.serveurs.values():
            s.fermer()
        self.serveurs = {}


# ------------------------------------------------------------------ modes en ligne de commande
def controler_capsule(dossier, moteur, arbitre):
    d = pathlib.Path(dossier)
    tf = json.loads((d / "data" / "temps-forts.json").read_text(encoding="utf-8"))
    cands = {b["id"]: {"fichier": str(d / "voix" / f"{b['id']}.wav"), "texte_dit": b.get("texte_dit") or b["texte"]}
             for b in tf if b.get("voix") != "prof"}
    t0 = time.time()
    c = Controleur(moteur, arbitre)
    try:
        res = c.controler(cands)
    finally:
        c.fermer()
    duree = time.time() - t0
    bilan = {"moteur": c.moteur, "arbitre": c.arbitre, "duree_s": round(duree, 1), "genere_le": time.strftime("%Y-%m-%d %H:%M"),
             "temps_forts": len(res), "sans_erreur": sum(v["erreurs"] == 0 for v in res.values()),
             "a_ecouter": [k for k, v in res.items() if v["erreurs"]], "blocs": res}
    (d / "data" / "controle-fidelite.json").write_text(json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in res.items():
        if v["erreurs"] or v["flous"]:
            ecarts = "; ".join(f"{x['type']} « {x['attendu']} » → « {x['entendu']} »" for x in v["details"])
            print(f"  {k} [{v['moteur']}] {v['erreurs']} erreur(s), {v['flous']} flou(s) : {ecarts}")
    print(f"\nContrôle {c.moteur}" + (f" + arbitre {c.arbitre}" if c.arbitre else "") +
          f" : {bilan['sans_erreur']}/{len(res)} temps forts sans erreur, {duree:.1f} s de bout en bout "
          f"(chargement compris). À écouter : {', '.join(bilan['a_ecouter']) or 'aucun'} ; détail : data/controle-fidelite.json")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichiers", nargs="*", help="entree.json sortie.json (mode historique)")
    ap.add_argument("--moteur", choices=MOTEURS, default=None)
    ap.add_argument("--arbitre", default=None, help="whisper | parakeet | aucun (défaut : arbitre_fidelite de config.json)")
    ap.add_argument("--capsule", default=None)
    ap.add_argument("--serveur", action="store_true")
    a = ap.parse_args()
    if a.serveur:
        commun.relancer_pour(a.moteur, __file__, sys.argv[1:])
        serveur(a.moteur)
    elif a.capsule:
        if not commun.module_present("num2words"):  # la comparaison remet les nombres en mots
            py = commun.python_de("parakeet") or commun.python_de("pocket")
            if not py:
                sys.exit("num2words introuvable (Python de Parakeet ou de Pocket).")
            sys.exit(subprocess.call([py, "-X", "utf8", __file__] + sys.argv[1:],
                                     env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")))
        controler_capsule(a.capsule, a.moteur, a.arbitre)
    elif len(a.fichiers) == 2:
        moteur = a.moteur or commun.CONF.get("asr_fidelite") or "parakeet"
        commun.relancer_pour(moteur, __file__, sys.argv[1:])
        entree = json.loads(pathlib.Path(a.fichiers[0]).read_text(encoding="utf-8"))
        tr = Transcripteur(moteur)
        sortie = {}
        for cle, v in entree.items():
            sortie[cle] = {"transcrit": tr.transcrire(v["fichier"])}
            print(f"  {cle}: transcrit", flush=True)
        pathlib.Path(a.fichiers[1]).write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        ap.error("--capsule <dossier>, --serveur, ou entree.json sortie.json")


if __name__ == "__main__":
    main()
