"""Préconversion d'un document LaTeX bfcours en Typst bfcours-typst, lisible et indenté.

    python convertir.py chemin/cours.tex                         # → chemin/cours.typ (même dossier)
    python convertir.py chemin/cours.tex -o autre/dossier/       # → autre/dossier/cours.typ
    python convertir.py chemin/cours.tex -o autre/dossier/fiche.typ
    python convertir.py chemin/cours.tex --compiler              # puis PDF prof et élève + images de contrôle
    python convertir.py chemin/exercice.tex --fragment           # fichier sans préambule (un \\input)

Le fichier Typst est écrit DIRECTEMENT dans le dossier demandé (par défaut, celui du .tex) ; les images
citées y sont copiées (sous-dossier images/). Les fichiers LaTeX d'origine ne sont jamais modifiés.
Un .typ existant n'est remplacé qu'avec --remplacer (sinon : nom-converti.typ à côté).

Ce que fait le script (l'agent n'a plus qu'à relire et retoucher) :
- commandes bfcours → fonctions de même nom en kebab-case (`\\Definition` → `definition`, `kebab.py`), options → clés
  validées contre l'index de la suite ;
- formules → mode maths Typst lisible ; tkz-tab → tabvar ; minipages → multi-colonnes(largeurs: …) ;
- figures TikZ et constructions sans équivalent → extraits #latex[…] (rendus par LaTeX à la compilation) ;
- compilation des deux versions et réparation automatique de ce qui ne compile pas ;
- rapport final : ce qui reste à reprendre, à la main ou par un redessin (farfadet-geom, cetz).
Code de sortie : 0 si le document compile en version professeur et élève, 1 sinon.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))

import localiser  # noqa: E402
from tex2typ import signatures  # noqa: E402
from tex2typ.catalogue import Catalogue  # noqa: E402
from tex2typ.conversion import Conversion  # noqa: E402
from tex2typ.lecture import Document, lire_document, lire_texte, retirer_commentaires, deplier  # noqa: E402
from tex2typ.reparation import compiler_versions, lieux_erreur, region_fautive, retirer_marqueurs  # noqa: E402

TOURS_MAX = 60


def nom_sans_accents(nom: str) -> str:
    t = unicodedata.normalize("NFD", nom)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^\w.\-]+", "_", t)


def cible(source: Path, sortie: str | None, remplacer: bool) -> Path:
    if sortie:
        s = Path(sortie)
        if s.suffix.lower() == ".typ":
            chemin = s
        else:
            chemin = s / (nom_sans_accents(source.stem) + ".typ")
    else:
        chemin = source.with_name(nom_sans_accents(source.stem) + ".typ")
    chemin = chemin.resolve()
    if chemin.exists() and not remplacer:
        chemin = chemin.with_name(chemin.stem + "-converti.typ")
    return chemin


class Pilote:
    """Convertit, compile, replie le nœud fautif, recommence (au plus TOURS_MAX fois)."""

    def __init__(self, doc, cat, sortie: Path, polices):
        self.doc, self.cat, self.sortie, self.polices = doc, cat, sortie, polices
        self.essais = 0
        self.notes = []

    def ecrire(self, replis):
        conv = Conversion(self.doc, self.cat, signatures.charger(), self.sortie.parent, replis, nom=self.sortie.stem)
        texte, spans = retirer_marqueurs(conv.convertir())
        self.sortie.write_text(texte, encoding="utf-8")
        return conv, spans

    def erreur(self, replis):
        self.essais += 1
        conv, spans = self.ecrire(replis)
        return compiler_versions(self.sortie, self.polices, self.sortie.parent), conv, spans

    def reparer(self):
        replis = set()
        erreur, conv, spans = self.erreur(replis)
        for _ in range(TOURS_MAX):
            if erreur is None:
                break
            lieux = lieux_erreur(erreur, self.sortie)
            ident = region_fautive(lieux, spans, conv.regions, replis)
            cle = conv.regions[ident].cle if ident is not None else self.dichotomie(replis, conv, spans)
            if cle is None:
                break
            description = next((r.description for r in conv.regions.values() if r.cle == cle), "?")
            resume = (getattr(erreur, "message", "") or str(erreur)).splitlines()[0][:110]
            self.notes.append(f"{description} : {resume}")
            replis.add(cle)
            erreur, conv, spans = self.erreur(replis)
        if replis:
            conv.rapport.replis = [f"{len(replis)} nœud(s) replié(s) après refus de Typst "
                                   f"({self.essais} compilations)"] + self.notes
        return erreur, conv.rapport

    def dichotomie(self, replis, conv, spans):
        """Erreur sans position dans le document (levée pendant la mise en page) : on cherche la région
        fautive en repliant des moitiés de régions, du niveau du document vers l'intérieur."""
        par_cle = {conv.regions[k].cle: s for k, s in spans.items() if k in conv.regions}
        def dedans(a, b):  # span a dans span b
            return (a[0], a[1]) >= (b[0], b[1]) and (a[2], a[3]) <= (b[2], b[3]) and a != b

        def maximales(parent=None):
            cles = [c for c, s in par_cle.items() if c not in replis and (parent is None or dedans(s, par_cle[parent]))]
            return sorted([c for c in cles if not any(dedans(par_cle[c], par_cle[d]) for d in cles if d != c)],
                          key=lambda c: par_cle[c][:2])

        def fautive(candidats):
            if not candidats or self.erreur(replis | set(candidats))[0] is not None:
                return None
            reste = list(candidats)
            while len(reste) > 1:
                moitie = reste[: len(reste) // 2]
                reste = moitie if self.erreur(replis | set(moitie))[0] is None else reste[len(reste) // 2:]
            return reste[0]

        coupable = fautive(maximales())
        while coupable is not None:
            plus_fine = fautive(maximales(coupable))
            if plus_fine is None:
                break
            coupable = plus_fine
        return coupable


def main() -> int:
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Préconvertit un document LaTeX bfcours en Typst bfcours-typst.")
    p.add_argument("source", help="fichier .tex (le maître, ou un fragment avec --fragment)")
    p.add_argument("-o", "--sortie", help="dossier (ou fichier .typ) de destination ; défaut : dossier du .tex")
    p.add_argument("--remplacer", action="store_true", help="remplace un .typ existant du même nom")
    p.add_argument("--fragment", action="store_true", help="fichier sans \\documentclass (un exercice inclus)")
    p.add_argument("--maitre", help="avec --fragment : le maître qui l'inclut (réglages, macros)")
    p.add_argument("--sans-reparation", action="store_true", help="n'essaie pas de compiler ni de réparer")
    p.add_argument("--compiler", action="store_true", help="à la fin : PDF prof et élève + images (compiler.py)")
    a = p.parse_args()

    source = Path(a.source).resolve()
    if not source.is_file():
        print(f"Fichier introuvable : {source}")
        return 2
    localiser.verifier_ou_quitter(besoin_typst=not a.sans_reparation)
    sortie = cible(source, a.sortie, a.remplacer)
    sortie.parent.mkdir(parents=True, exist_ok=True)

    doc = lire_document(source)
    if a.fragment and a.maitre:  # préambule et macros du maître, corps du fragment
        maitre = lire_document(Path(a.maitre).resolve())
        doc.preambule = maitre.preambule
        doc.classe_options = maitre.classe_options
    cat = Catalogue()
    polices = [str(localiser.polices())] if localiser.polices() else []

    pilote = Pilote(doc, cat, sortie, polices)
    if a.sans_reparation:
        conv, _ = pilote.ecrire(set())
        erreur, rapport = None, conv.rapport
    else:
        erreur, rapport = pilote.reparer()
    afficher_rapport(source, sortie, rapport, erreur, doc)
    if a.compiler and erreur is None:
        import subprocess
        subprocess.run([sys.executable, str(ICI / "compiler.py"), str(sortie), "--png"], check=False)
    return 0 if erreur is None else 1


def afficher_rapport(source, sortie, r, erreur, doc: Document):
    print(f"Typst écrit : {sortie}")
    if erreur is None:
        print("Compilation : OK en version professeur et élève (extraits LaTeX non rendus à ce stade).")
    else:
        print("Compilation : ÉCHEC, à corriger à la main :")
        diagnostic = str(str(getattr(erreur, "diagnostic", "") or str(erreur)).replace("\\\\?\\", "").strip())
        print("  " + str(diagnostic).replace("\n", "\n  ")[:1500])
    if doc.introuvables:
        print("\nFichiers \\input introuvables : " + ", ".join(sorted(set(doc.introuvables))))
    if doc.illisibles:
        print("\nCaractères illisibles dans les sources (à corriger dans le .tex) : "
              + ", ".join(f"{Path(k).name} ({v})" for k, v in doc.illisibles.items()))
    if r is None:
        return
    if r.extraits:
        compte = {}
        for e in r.extraits:
            compte[e] = compte.get(e, 0) + 1
        print(f"\nExtraits LaTeX ({len(r.extraits)}) — fidèles, à redessiner seulement si utile "
              "(farfadet-geom pour la géométrie plane) :")
        for e, k in sorted(compte.items(), key=lambda x: -x[1]):
            print(f"  {k:3} × {e}")
    if r.replis:
        print("\nReplis automatiques :")
        for x in r.replis[:30]:
            print("  - " + x)
    if r.a_reprendre:
        print(f"\nÀ reprendre ({len(r.a_reprendre)}) — cherchez « a-reprendre » et les commentaires dans le .typ :")
        vus = set()
        for x in r.a_reprendre:
            if x in vus:
                continue
            vus.add(x)
            print("  - " + x)
            if len(vus) >= 40:
                print("  …")
                break
    if r.cles_ecartees:
        print("\nOptions LaTeX sans clé Typst (écartées) :")
        for x in sorted(set(r.cles_ecartees))[:30]:
            print("  - " + x)
    if r.inconnues:
        print("\nCommandes inconnues : " + ", ".join(f"{k} ×{v}" for k, v in sorted(r.inconnues.items(), key=lambda x: -x[1])[:30]))
    if r.ignorees:
        print("Ignorées (sans effet en Typst) : " + ", ".join(f"{k} ×{v}" for k, v in sorted(r.ignorees.items(), key=lambda x: -x[1])[:20]))
    if r.images:
        print(f"\nImages copiées : {len(r.images)}")


if __name__ == "__main__":
    sys.exit(main())
