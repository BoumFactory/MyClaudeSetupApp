"""Compile un document bfcours-typst comme l'extension VS Code au Ctrl+Maj+B : version professeur, version élève
et extraits LaTeX (`#latex[…]`), puis, si demandé, une image PNG par page pour contrôler le rendu.

    python compiler.py doc.typ                     # doc-prof.pdf et doc-eleve.pdf à côté de doc.typ
    python compiler.py doc.typ --png               # + images dans <dossier>/.apercu/doc-prof/, doc-eleve/
    python compiler.py doc.typ --png --ppi 110     # images plus fines (défaut 80)
    python compiler.py doc.typ --version prof      # une seule version (prof ou eleve)
    python compiler.py chapitre1.typ               # fragment inclus : le document maître est retrouvé
    python compiler.py doc.typ --nettoyer          # supprime <dossier>/.apercu/ (fin de travail)
    python compiler.py doc.typ --sans-service      # ne pas passer par le service de VS Code

Moteur : `bfwatch.py` de la suite (retrouvé par localiser.py), donc exactement les PDF que l'utilisateur
obtient au Ctrl+Maj+B, extraits LaTeX compris (rendus mis en cache dans `rendus-tex/` à côté du document).

- Si le service bfwatch partagé de VS Code tourne (extension bfcours-typst, une fenêtre au moins), la
  requête lui est confiée et réutilise ses compilateurs chauds et son cache (moins d'une seconde sur un
  document déjà vu). compiler.py ne s'y inscrit pas : il ne prolonge pas la vie du service, qui s'arrête
  30 s après la fermeture de la dernière fenêtre VS Code.
- Sinon, bfwatch est chargé ici et compile les deux versions en parallèle (deux compilateurs, deux threads).
- Sans bfwatch (installation partielle), les deux versions sont compilées directement par le module typst,
  sans les extraits LaTeX, et le script le dit.

Les PDF s'écrivent à côté du document (règle du skill : on travaille dans le dossier de l'utilisateur).
En cas d'erreur, le diagnostic complet de Typst est affiché (fichier:ligne:colonne, extrait, indices).
Code de sortie : 0 si toutes les versions compilent, 1 sinon.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import localiser  # noqa: E402

VERSIONS = {
    "prof": {"libelle": "prof", "suffixe": "-prof", "entrees": {"correction": "true", "prof": "true"}},
    "eleve": {"libelle": "élève", "suffixe": "-eleve", "entrees": {"correction": "false", "prof": "false"}},
}
APERCU = ".apercu"


def _charger_bfwatch():
    chemin = localiser.bfwatch()
    if not chemin:
        return None
    spec = importlib.util.spec_from_file_location("bfwatch_skill", str(chemin))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    rendus = localiser.rendus_tex()
    if rendus:
        module.SCRIPT_RENDUS_TEX = rendus
    return module


def _diagnostic(erreur) -> str:
    d = str(getattr(erreur, "diagnostic", None) or str(erreur))
    return str(d).replace("\\\\?\\", "").replace("\\?\\", "")


def _polices():
    p = localiser.polices()
    return [str(p)] if p else []


def diagnostic_complet(document: Path, racine: Path, entrees) -> str:
    """Recompile une version pour obtenir le diagnostic détaillé (repli si bfwatch ne l'a pas transmis)."""
    import typst
    from tex2typ.reparation import assurer_index_rendus
    assurer_index_rendus(document)
    try:
        typst.compile(str(document), root=str(racine), font_paths=_polices(), sys_inputs=dict(entrees),
                     **localiser.options_paquets())
        return ""
    except typst.TypstError as e:
        return _diagnostic(e)


def _pannes_passageres(document: Path) -> bool:
    import json
    index = document.parent / "rendus-tex" / "index.json"
    try:
        extraits = json.loads(index.read_text(encoding="utf-8")).get("extraits", {})
    except (OSError, ValueError):
        return False
    return any("passagère" in (e.get("erreur") or "") or "Fatal error" in (e.get("erreur") or "")
               for e in extraits.values())


def compiler_direct(document: Path, versions) -> bool:
    """Repli sans bfwatch : les versions en parallèle par le module typst, sans extraits LaTeX."""
    import typst
    from tex2typ.reparation import assurer_index_rendus
    assurer_index_rendus(document)
    lignes = {}

    def une(v):
        sortie = document.with_name(document.stem + v["suffixe"] + ".pdf")
        try:
            _, avert = typst.compile_with_warnings(str(document), output=str(sortie), root=str(document.parent),
                                                   font_paths=_polices(), sys_inputs=v["entrees"],
                                                   **localiser.options_paquets())
            texte = [f"[ok]     {document.name} {v['libelle']:6} → {sortie.name}"]
            texte += ["  avertissement : " + _diagnostic(a).splitlines()[0] for a in avert]
            lignes[v["libelle"]] = (True, "\n".join(texte))
        except typst.TypstError as e:
            lignes[v["libelle"]] = (False, f"[ÉCHEC]  {document.name} {v['libelle']}\n{_diagnostic(e)}")

    fils = [threading.Thread(target=une, args=(v,)) for v in versions]
    for f in fils:
        f.start()
    for f in fils:
        f.join()
    for v in versions:
        print(lignes[v["libelle"]][1])
    return all(lignes[v["libelle"]][0] for v in versions)


def images(document: Path, versions, ppi: float) -> None:
    try:
        import fitz
    except ImportError:
        print("PyMuPDF absent (pip install pymupdf) : pas d'images de contrôle.")
        return
    for v in versions:
        pdf = document.with_name(document.stem + v["suffixe"] + ".pdf")
        if not pdf.exists():
            continue
        dossier = document.parent / APERCU / (document.stem + v["suffixe"])
        dossier.mkdir(parents=True, exist_ok=True)
        for ancien in dossier.glob("page-*.png"):
            ancien.unlink()
        with fitz.open(pdf) as doc:
            for i, page in enumerate(doc, 1):
                page.get_pixmap(dpi=int(ppi)).save(str(dossier / f"page-{i:02d}.png"))
            print(f"images : {dossier}  ({doc.page_count} page(s))")


# ---------------------------------------------------------------------------
# Production : par le service de VS Code, ou par bfwatch chargé ici
# ---------------------------------------------------------------------------

def par_service(client, document: Path, plafond: Path, choix: str):
    """Confie la compilation au serveur bfwatch de VS Code. Rend sa réponse, ou None s'il faut se rabattre."""
    requete = {"fichier": str(document), "espace": str(plafond), "une_version_sous": False}
    if choix != "les-deux":
        requete["versions"] = [choix]
    try:
        reponse = client.requete(requete, sur_etat=lambda texte: print(f"          {texte}"))
    except (OSError, ValueError) as erreur:
        print(f"service bfwatch indisponible ({erreur}) : compilation ici.")
        return None
    if reponse.get("arret"):
        print("service bfwatch en cours d'arrêt : compilation ici.")
        return None
    for d in reponse.get("documents", []):
        if d.get("ignore"):
            print(f"[info]   {Path(d.get('maitre') or document).name} : {d['ignore']}")
        latex = d.get("latex") or {}
        if latex.get("extraits"):
            print(f"[latex]  {latex['extraits']} extrait(s), {latex.get('compiles', 0)} compilé(s), "
                  f"{latex.get('erreurs', 0)} erreur(s)")
        if latex.get("avertissement"):
            print(f"[latex]  {latex['avertissement']}")
        for v in d.get("versions", []):
            etiquette = f"{Path(d['maitre']).name:36} {v['libelle']:8} {v.get('duree', 0):6.2f} s"
            if v.get("ok"):
                print(f"[ok]     {etiquette}  → {Path(v['sortie']).name} ({v.get('pages', 0)} page(s))")
            else:
                print(f"[ÉCHEC]  {etiquette}  {v.get('message', '')}")
            if v.get("polices_manquantes"):
                print("  police introuvable : " + ", ".join(v["polices_manquantes"]))
    if reponse.get("erreur"):
        print(f"[ÉCHEC]  {reponse['erreur']}")
    return reponse


def par_bfwatch_local(bfwatch, document: Path, plafond: Path, versions):
    """bfwatch chargé dans ce processus : versions compilées en parallèle, journal affiché au fil de l'eau."""
    config, _ = bfwatch.charger_config(None, creer=False)  # allègement, parallélisme : réglages de l'utilisateur
    config.update(dossier_polices=str(localiser.polices() or ""), une_version_sous=[], versions=versions)
    moteur = bfwatch.Moteur(config, bfwatch.Journal(couleur=False))
    moteur._rapport = []
    ok = moteur.traiter(document, plafond=plafond)
    documents, moteur._rapport = moteur._rapport, None
    return {"ok": ok, "documents": documents, "moteur": moteur}


def main() -> int:
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Compile un document bfcours-typst en versions prof et élève.")
    p.add_argument("document")
    p.add_argument("--version", choices=("prof", "eleve", "les-deux"), default="les-deux")
    p.add_argument("--png", action="store_true", help="une image par page dans <dossier>/.apercu/")
    p.add_argument("--ppi", type=float, default=80)
    p.add_argument("--espace", help="plafond de la recherche du document maître (défaut : dossier du fichier)")
    p.add_argument("--nettoyer", action="store_true", help="supprime le dossier .apercu/ du document et sort")
    p.add_argument("--sans-service", action="store_true",
                   help="compiler ici, sans passer par le service bfwatch de VS Code même s'il tourne")
    a = p.parse_args()

    document = Path(a.document).resolve()
    if a.nettoyer:  # seulement les images de contrôle, fichier par fichier
        cible = document.parent / APERCU
        if cible.is_dir():
            for sous in [d for d in cible.iterdir() if d.is_dir()]:
                for png in sous.glob("page-*.png"):
                    png.unlink()
                if not any(sous.iterdir()):
                    sous.rmdir()
            if not any(cible.iterdir()):
                cible.rmdir()
            print(f"nettoyé : {cible}")
        return 0
    if not document.exists():
        print(f"Fichier introuvable : {document}")
        return 1
    localiser.verifier_ou_quitter()
    if not localiser.polices():
        print("info : dossier des polices introuvable ; compilation avec les polices intégrées de Typst "
              "(rendu Erewhon absent, voir localiser.py).")
    versions = [VERSIONS[k] for k in (("prof", "eleve") if a.version == "les-deux" else (a.version,))]
    depart = time.perf_counter()

    bfwatch = _charger_bfwatch()
    if bfwatch is None:
        print("bfwatch introuvable : compilation directe, extraits LaTeX NON rendus.")
        ok = compiler_direct(document, versions)
        maitres = [document]
    else:
        plafond = Path(a.espace).resolve() if a.espace else document.parent
        client = None if a.sans_service else bfwatch.trouver_service(str(localiser.polices() or ""))
        if client is not None:
            print(f"service bfwatch de VS Code (port {client.annonce.get('port')}) : compilateurs réutilisés.")

        def produire():
            if client is not None:
                reponse = par_service(client, document, plafond, a.version)
                if reponse is not None:
                    return reponse
            return par_bfwatch_local(bfwatch, document, plafond, versions)

        try:
            reponse = produire()
            maitres = [Path(d["maitre"]) for d in reponse["documents"] if d.get("maitre")] or [document]
            # panne passagère de LuaLaTeX (cache des polices disputé par des compilations simultanées) :
            # une nouvelle passe, qui ne recompile que les extraits en échec
            for _ in range(2):
                if not any(_pannes_passageres(m) for m in maitres):
                    break
                print("nouvelle passe : extraits LaTeX en panne passagère")
                reponse = produire()
        finally:
            if client is not None:
                client.fermer()
        ok = bool(reponse.get("ok"))
        if not ok:
            for d in reponse.get("documents", []):
                echecs = [v for v in d.get("versions", []) if not v.get("ok")]
                if not echecs:
                    continue
                diag = echecs[0].get("diagnostic") or ""
                if not diag and d.get("racine"):
                    v = next((x for x in versions if x["libelle"] == echecs[0]["libelle"]), versions[0])
                    diag = diagnostic_complet(Path(d["maitre"]), Path(d["racine"]), v["entrees"])
                if diag:
                    print(f"\nDiagnostic ({Path(d['maitre']).name}, {echecs[0]['libelle']}) :\n{diag}")
    print(f"durée totale : {time.perf_counter() - depart:.1f} s")
    if a.png and ok:
        for maitre in maitres:
            images(maitre, versions, a.ppi)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
