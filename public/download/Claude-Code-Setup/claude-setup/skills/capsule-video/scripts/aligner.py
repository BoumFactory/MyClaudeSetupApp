"""Aligne les mots EXACTS du script sur les mots horodatés de data/transcript.json (mode voix de synthèse).

Usage : python aligner.py <dossier_capsule>
(appelé automatiquement par transcrire.py quand data/temps-forts.json existe)

Entrées : data/temps-forts.json (texte de chaque temps fort, bornes exactes)
          data/transcript.json (mots horodatés : texte dit aligné par MFA, ou mots reconnus par Whisper)
Sortie  : data/temps-forts.json et data/temps-forts.js enrichis de "mots" :
          [{"mot": "240", "debut": 71.32, "fin": 71.90, "source": "mfa" | "whisper" | "groupe" | "interpole"}]

Principe : dans la fenêtre de chaque temps fort, alignement de séquences (difflib) entre les mots du script
et les mots horodatés. Un mot apparié prend leur horodatage (« mfa » ou « whisper ») ; un passage écrit
autrement des deux côtés (« 240 » dit « deux cent quarante », « 540p ») prend la plage des mots
correspondants (« groupe ») ; un mot sans vis-à-vis (mot sauté par Whisper) est interpolé entre ses voisins.
Les ancres de spec.js portent ainsi sur le texte du script.
"""
import difflib
import json
import pathlib
import re
import sys
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9,]", "", s).strip(",")


def jetons(texte):
    """Mots du script, apostrophes séparées (l'exercice → l, exercice), ponctuation retirée."""
    brut = re.split(r"[\s'’]+", texte)
    return [(m, norm(m)) for m in brut if norm(m)]


def aligner(dossier):
    d = pathlib.Path(dossier) / "data"
    tf = json.loads((d / "temps-forts.json").read_text(encoding="utf-8"))
    tr = json.loads((d / "transcript.json").read_text(encoding="utf-8"))
    # mots reconnus, apostrophes séparées elles aussi
    reconnus = []
    for m in tr["mots"]:
        for morceau in re.split(r"['’]+", m["mot"]):
            if norm(morceau):
                reconnus.append({"n": norm(morceau), "debut": m["debut"], "fin": m["fin"]})
    source = "mfa" if tr.get("horodatage") == "mfa" else "whisper"
    total_apparies = total = groupes = 0
    for b in tf:
        fen = [r for r in reconnus if b["debut"] - 0.15 <= r["debut"] <= b["fin"] + 0.15]
        script = jetons(b["texte"])
        sm = difflib.SequenceMatcher(a=[n for _, n in script], b=[r["n"] for r in fen], autojunk=False)
        temps = [None] * len(script)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                for k in range(i2 - i1):
                    r = fen[j1 + k]
                    temps[i1 + k] = (r["debut"], r["fin"], source)
            elif op == "replace":
                # même passage écrit autrement (« 240 » dit « deux cent quarante », « 540p », « P de C » entendu
                # « P2C ») : les mots du script se partagent la plage des mots entendus, au prorata des lettres
                d0, f0 = fen[j1]["debut"], fen[j2 - 1]["fin"]
                poids = [len(nn) + 1 for _, nn in script[i1:i2]]
                tot, t = sum(poids), d0
                for k, p in enumerate(poids):
                    dt = max(f0 - d0, 0) * p / tot
                    temps[i1 + k] = (round(t, 3), round(t + dt, 3), "groupe")
                    t += dt
                groupes += i2 - i1
        # interpolation des mots non appariés entre voisins appariés (bornes du temps fort aux extrémités)
        reperes = [(-1, b["debut"], b["debut"])] + [(i, t[0], t[1]) for i, t in enumerate(temps) if t] \
            + [(len(script), b["fin"], b["fin"])]
        for (i0, _, f0), (i1, d1, _) in zip(reperes, reperes[1:]):
            trou = i1 - i0 - 1
            if trou <= 0:
                continue
            pas = max(d1 - f0, 0) / trou
            for k in range(trou):
                temps[i0 + 1 + k] = (round(f0 + k * pas, 3), round(f0 + (k + 1) * pas, 3), "interpole")
        b["mots"] = [{"mot": m, "debut": t[0], "fin": t[1], "source": t[2]} for (m, _), t in zip(script, temps)]
        total += len(script)
        total_apparies += sum(1 for t in temps if t[2] == source)
    (d / "temps-forts.json").write_text(json.dumps(tf, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "temps-forts.js").write_text("window.TEMPS_FORTS = " + json.dumps(tf, ensure_ascii=False) + ";\n",
                                      encoding="utf-8")
    interpoles = total - total_apparies - groupes
    print(f"Alignement script ↔ {source.upper() if source == 'mfa' else 'Whisper'} : {total_apparies}/{total} mots "
          f"appariés, {groupes} posés sur un passage écrit autrement (« groupe »), {interpoles} interpolés")
    return {"total": total, "apparies": total_apparies, "groupes": groupes, "interpoles": interpoles}


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    aligner(sys.argv[1])
