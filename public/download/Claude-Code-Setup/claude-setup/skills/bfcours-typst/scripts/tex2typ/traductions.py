"""Traductions dédiées : les commandes et environnements dont la forme Typst ne se déduit pas de la règle
générique (« même nom, options → clés, arguments → positionnels, corps en dernier »).

Une méthode `c_<nom>` traite la commande `\\<nom>`, `e_<nom>` l'environnement `<nom>`, `s_<nom>` un
environnement qui regroupe ses voisins (minipages côte à côte). Chaque méthode reçoit le nœud et renvoie
du Typst ; une méthode `c_` peut aussi renvoyer (texte, est_bloc, indice suivant) pour consommer les nœuds
qui suivent (\\tcbitempoint prend le texte de la question, \\def prend son nom et son corps).

Les noms de fonctions et les clés viennent de l'index : ce fichier ne fixe que la FORME des appels.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from . import maths, regles
from .analyse import Analyseur, Arg, Car, Cmd, Env, Groupe, Maths, Noeud, Par, Si, Texte
from .ecriture import (chaine, construire_appel, crochets, indenter, sans_marqueurs, texte_simple, virgule)

FIN_QUESTION = {"tcbitem", "item", "exocorrection", "tcblower", "par", "newpage", "clearpage", "pagebreak",
                "McqQuest", "vspace", "medskip", "bigskip", "smallskip", "section", "subsection"}
BLOCS = (Env, Si)


def _vide(n: Noeud) -> bool:
    return isinstance(n, Texte) and not n.s.strip()


class Traductions:
    # ================================================================== repères de fichiers
    def c_bfFichier(self, n, noeuds, i):
        a = n.arg("m")
        nom = a.brut if a else "?"
        return f"// ─── LaTeX : {nom} ───", True, i + 1

    # ================================================================== titres
    def _titre(self, n: Cmd, niveau: int):
        a = n.args[-1] if n.args else None
        titre = self.sequence(a.enfants).replace("\n", " ") if a and a.present else ""
        return "=" * niveau + " " + titre, True, None

    def c_section(self, n, noeuds, i):
        t, b, _ = self._titre(n, 1)
        return t, b, i + 1

    def c_subsection(self, n, noeuds, i):
        t, b, _ = self._titre(n, 2)
        return t, b, i + 1

    def c_subsubsection(self, n, noeuds, i):
        t, b, _ = self._titre(n, 3)
        return t, b, i + 1

    def c_paragraph(self, n, noeuds, i):
        t, b, _ = self._titre(n, 4)
        return t, b, i + 1

    c_chapter = c_section
    c_part = c_section

    # ================================================================== mise en forme
    def _envelopper(self, n: Cmd, avant: str, apres: str, fonction: Optional[str] = None) -> str:
        a = n.arg("m")
        if not a or not a.present:
            return ""
        t = self.sequence(a.enfants)
        if not t.strip():
            return ""
        nu = sans_marqueurs(t)
        simple = "\n" not in nu and not re.search(r"[*_\[\]]", nu) and nu == nu.strip()
        if simple and avant:
            return avant + t + apres
        return "#" + (fonction or "strong") + crochets(t)

    def c_textbf(self, n, noeuds, i):
        return self._lier(self._envelopper(n, "*", "*", "strong"), noeuds, i)

    def c_textit(self, n, noeuds, i):
        return self._lier(self._envelopper(n, "_", "_", "emph"), noeuds, i)

    c_emph = c_textit
    c_textsl = c_textit

    def _lier(self, t, noeuds, i):
        """`*mot*` collé à une lettre ne serait pas compris : on passe alors par la fonction."""
        if not t:
            return None, False, i + 1
        suivant = noeuds[i + 1] if i + 1 < len(noeuds) else None
        precedent = noeuds[i - 1] if i > 0 else None
        colle = (isinstance(suivant, Texte) and suivant.s[:1].isalnum()) or \
                (isinstance(precedent, Texte) and precedent.s[-1:].isalnum())
        if colle and t[:1] in "*_":
            f = "strong" if t[0] == "*" else "emph"
            t = "#" + f + "[" + t[1:-1] + "]"
        return t, False, i + 1

    def c_underline(self, n, noeuds, i):
        return "#underline" + self.contenu_arg(n.arg("m"))

    c_uline = c_underline

    def c_sout(self, n, noeuds, i):
        return "#strike" + self.contenu_arg(n.arg("m"))

    def c_textsc(self, n, noeuds, i):
        return "#smallcaps" + self.contenu_arg(n.arg("m"))

    def c_texttt(self, n, noeuds, i):
        a = n.arg("m")
        brut = texte_simple(a.brut) if a else ""
        if "`" not in brut and "\n" not in brut:
            return "`" + a.brut.replace("\\_", "_").replace("\\%", "%").replace("\\&", "&").replace("\\#", "#") + "`"
        return "#raw(" + chaine(brut) + ")"

    def c_textsf(self, n, noeuds, i):
        return self.sequence(n.arg("m").enfants) if n.arg("m") else None

    c_textrm = c_textsf
    c_textup = c_textsf
    c_textnormal = c_textsf
    c_mbox = c_textsf
    c_hbox = c_textsf

    def c_textsuperscript(self, n, noeuds, i):
        return "#super" + self.contenu_arg(n.arg("m"))

    c_up = c_textsuperscript
    c_exposant = c_textsuperscript

    def c_textsubscript(self, n, noeuds, i):
        return "#sub" + self.contenu_arg(n.arg("m"))

    def c_textcolor(self, n, noeuds, i):
        couleur = n.args[1].brut.strip() if len(n.args) > 1 else "black"
        corps = n.args[-1]
        return f"#textcolor({chaine(couleur)})" + self.contenu_arg(corps)

    def c_colorbox(self, n, noeuds, i):
        couleur = n.args[-2].brut.strip()
        return f"#box(fill: xcolor({chaine(couleur)}), inset: (x: 2pt, y: 1pt))" + self.contenu_arg(n.args[-1])

    def c_fcolorbox(self, n, noeuds, i):
        cadre, fond = n.args[-3].brut.strip(), n.args[-2].brut.strip()
        return (f"#box(stroke: 0.4pt + xcolor({chaine(cadre)}), fill: xcolor({chaine(fond)}), inset: 3pt)"
                + self.contenu_arg(n.args[-1]))

    def c_fbox(self, n, noeuds, i):
        return "#box(stroke: 0.4pt, inset: 3pt)" + self.contenu_arg(n.arg("m"))

    def c_framebox(self, n, noeuds, i):
        return self.c_fbox(n, noeuds, i)

    def c_makebox(self, n, noeuds, i):
        largeur = n.arg("o")
        tete = f"#box(width: {self._longueur(largeur.brut)})" if largeur else "#box"
        return tete + self.contenu_arg(n.arg("m"))

    def c_parbox(self, n, noeuds, i):
        m = [a for a in n.args if a.genre == "m" and a.present]
        if len(m) < 2:
            return None
        return f"#box(width: {self._longueur(m[0].brut)})" + self.contenu(m[1].enfants), "\n" in m[1].brut, i + 1

    def c_raisebox(self, n, noeuds, i):
        m = [a for a in n.args if a.genre == "m" and a.present]
        return f"#move(dy: -{self._longueur(m[0].brut).lstrip('-')})" + self.contenu(m[-1].enfants) if len(m) > 1 else None

    def c_scalebox(self, n, noeuds, i):
        m = [a for a in n.args if a.genre == "m" and a.present]
        f = self._nombre(m[0].brut) or "1"
        return f"#scale({float(f) * 100:g}%, reflow: true)" + self.contenu(m[-1].enfants)

    def c_resizebox(self, n, noeuds, i):
        m = [a for a in n.args if a.genre == "m" and a.present]
        largeur = m[0].brut.strip()
        if largeur in ("!", "*"):
            return self.contenu(m[-1].enfants)
        return f"#box(width: {self._longueur(largeur)})[#scale(x: 100%, reflow: true)" + self.contenu(m[-1].enfants) + "]"

    def c_rotatebox(self, n, noeuds, i):
        m = [a for a in n.args if a.genre == "m" and a.present]
        angle = self._nombre(m[0].brut) or "0"
        return f"#rotate(-{angle}deg, reflow: true)" + self.contenu(m[-1].enfants)

    def c_phantom(self, n, noeuds, i):
        return "#hide" + self.contenu_arg(n.arg("m"))

    c_hphantom = c_phantom

    def c_vphantom(self, n, noeuds, i):
        return None

    def c_today(self, n, noeuds, i):
        return '#datetime.today().display("[day]/[month]/[year]")'

    # accents de l'ancien LaTeX (\'e, \`a, \^o, \"i, \c{c})
    def _accent(self, n, noeuds, i, signe):
        from .conversion import ACCENTS_TEXTE
        a = n.arg("m")
        lettre = a.brut.strip() if a else ""
        j = i + 1
        if not lettre and j < len(noeuds) and isinstance(noeuds[j], Texte) and noeuds[j].s:
            lettre = noeuds[j].s[0]
            reste = noeuds[j].s[1:]
            noeuds[j] = Texte(noeuds[j].debut + 1, noeuds[j].fin, reste)
        return ACCENTS_TEXTE.get((signe, lettre), lettre), False, j

    def c_car_39(self, n, noeuds, i):
        return self._accent(n, noeuds, i, "'")

    def c_car_96(self, n, noeuds, i):
        return self._accent(n, noeuds, i, "`")

    def c_car_94(self, n, noeuds, i):
        return self._accent(n, noeuds, i, "^")

    def c_car_34(self, n, noeuds, i):
        return self._accent(n, noeuds, i, '"')

    def c_car_126(self, n, noeuds, i):
        return self._accent(n, noeuds, i, "~")

    def c_c(self, n, noeuds, i):
        return self._accent(n, noeuds, i, "c")

    def c_car_44(self, n, noeuds, i):  # \,
        return "#h(0.17em)"

    def c_car_32(self, n, noeuds, i):  # « \ »
        return " "

    # ================================================================== espaces, sauts
    def c_saut(self, n, noeuds, i):  # \\
        if self.niveau_tableau:
            return None, False, i + 1
        # un \\ en fin de contenu ne sert à rien en Typst
        reste = [x for x in noeuds[i + 1:] if not _vide(x)]
        if not reste:
            return None, False, i + 1
        espace = n.arg("o")
        if espace and espace.present and espace.brut.strip():
            l = self._longueur(espace.brut)
            if not l.startswith(("-", '"')):
                return f"\\\n#v({l})\n", False, i + 1
        return "\\\n", False, i + 1

    def c_newline(self, n, noeuds, i):
        return "\\\n"

    def c_par(self, n, noeuds, i):
        return "\n\n"

    def c_vspace(self, n, noeuds, i):
        a = n.arg("m")
        if not a:
            return None
        l = self._longueur(a.brut)
        if l.startswith("-") or l.startswith('"'):
            self.rapport.compter(self.rapport.ignorees, "\\vspace négatif")
            return None, False, i + 1
        if l in ("0pt", "0cm", "0mm", "0em"):
            return None, False, i + 1
        return f"#v({l})", True, i + 1

    def c_hspace(self, n, noeuds, i):
        a = n.arg("m")
        l = self._longueur(a.brut) if a else "1em"
        if l.startswith('"'):
            return None
        return f"#h({l})"

    def c_hfill(self, n, noeuds, i):
        return "#h(1fr)"

    c_dotfill = c_hfill

    def c_vfill(self, n, noeuds, i):
        return "#v(1fr)", True, i + 1

    def c_newpage(self, n, noeuds, i):
        if self.niveau > 0:
            self.rapport.compter(self.rapport.ignorees, "\\newpage dans un contenant")
            return None, False, i + 1
        reste = [x for x in noeuds[i + 1:] if not _vide(x) and not isinstance(x, Par)]
        if not reste:  # saut de page final : inutile
            return None, False, i + 1
        return "#pagebreak()", True, i + 1

    c_clearpage = c_newpage
    c_pagebreak = c_newpage

    def c_needspace(self, n, noeuds, i):
        a = n.arg("m")
        if not a:
            return None
        l = self._longueur(a.brut)
        if l.startswith('"'):
            return None
        conteneur = ", conteneur: true" if self.niveau > 0 else ""
        return f"#needspace({l}{conteneur})", True, i + 1

    c_Needspace = c_needspace

    def c_hline(self, n, noeuds, i):
        return "#line(length: 100%, stroke: 0.4pt)", True, i + 1

    def c_rule(self, n, noeuds, i):
        m = [a for a in n.args if a.genre == "m" and a.present]
        largeur = self._longueur(m[0].brut) if m else "100%"
        return f"#box(width: {largeur}, line(length: 100%))"

    # ================================================================== liens, notes, références
    def c_footnote(self, n, noeuds, i):
        return "#footnote" + self.contenu_arg(n.arg("m"))

    def c_href(self, n, noeuds, i):
        m = [a for a in n.args if a.present]
        return f"#link({chaine(m[0].brut.strip())})" + self.contenu(m[1].enfants)

    def c_url(self, n, noeuds, i):
        a = n.args[0] if n.args else None
        return f"#link({chaine(a.brut.strip())})" if a else None

    c_nolinkurl = c_url

    def c_ref(self, n, noeuds, i):
        a = n.arg("m")
        cible = re.sub(r"[^\w:.\-]", "-", a.brut.strip()) if a else ""
        return f"@{cible}" if re.fullmatch(r"[\w\-]+(?:[:.][\w\-]+)*", cible) else None

    c_eqref = c_ref
    c_autoref = c_ref
    c_cref = c_ref

    def c_pageref(self, n, noeuds, i):
        return None

    # ================================================================== images
    def c_includegraphics(self, n, noeuds, i):
        opts = n.arg("o")
        fichier = n.arg("m").brut.strip() if n.arg("m") else ""
        source = self._trouver_image(fichier)
        if source is None:
            return self.a_reprendre(self.texte[n.debut:n.fin], "image introuvable"), False, i + 1
        cible_rel = self._copier_image(source)
        cles = []
        if opts and opts.present:
            for k, v in self._options(opts.brut):
                if k in ("width", "height") and v:
                    cles.append(f"{k}: {self._longueur(v)}")
                elif k == "scale" and v:
                    self.rapport.a_reprendre.append(f"échelle d'image {v} : régler width à la main ({fichier})")
        args = [chaine(cible_rel)] + cles
        return "#image(" + ", ".join(args) + ")"

    def _trouver_image(self, nom: str) -> Optional[Path]:
        dossiers = [self.dossier_source] + [Path(f).parent for f in self.doc.fichiers]
        m = re.search(r"\\graphicspath\s*\{((?:\{[^}]*\})+)\}", self.doc.preambule)
        if m:
            for d in re.findall(r"\{([^}]*)\}", m.group(1)):
                dossiers.append((self.dossier_source / d).resolve())
        for d in dossiers:
            for ext in ("", ".pdf", ".png", ".jpg", ".jpeg", ".svg", ".PNG", ".JPG"):
                p = d / (nom + ext)
                if p.is_file():
                    return p
        return None

    def _copier_image(self, source: Path) -> str:
        """Copie l'image dans le dossier de sortie (sous-dossier images/), sauf si elle y est déjà."""
        try:
            rel = source.resolve().relative_to(self.sortie.resolve())
            return rel.as_posix()
        except ValueError:
            pass
        cible = self.sortie / "images" / source.name
        cible.parent.mkdir(parents=True, exist_ok=True)
        if not cible.exists() or cible.stat().st_size != source.stat().st_size:
            shutil.copy2(source, cible)
            self.rapport.images.append(f"{source} → images/{source.name}")
        # format réel (une image « .png » qui est un JPEG arrête Typst)
        tete = cible.read_bytes()[:8]
        if cible.suffix.lower() == ".png" and tete[:3] == b"\xff\xd8\xff":
            vrai = cible.with_suffix(".jpg")
            shutil.copy2(cible, vrai)
            cible.unlink()
            return "images/" + vrai.name
        return "images/" + cible.name

    # ================================================================== définitions dans le corps
    def c_def(self, n, noeuds, i):
        """\\def\\nom{corps} : \\def\\rdifficulty{n} devient #rdifficulty(n) ; les autres sont des macros."""
        j = i + 1
        if j < len(noeuds) and isinstance(noeuds[j], Cmd):
            nom = noeuds[j].nom
            corps_noeud = noeuds[j + 1] if j + 1 < len(noeuds) else None
            fin = j + 2 if isinstance(corps_noeud, Groupe) else j + 1
            if nom == "rdifficulty" and isinstance(corps_noeud, Groupe):
                v = self._nombre(self.texte[corps_noeud.debut + 1:corps_noeud.fin - 1]) or "1"
                return f"#rdifficulty({v})", True, fin
            # les arguments mangés par une signature connue de la macro sont rendus ici
            if noeuds[j].args:
                return None, False, j + 1
            if isinstance(corps_noeud, Groupe):
                corps = self.texte[corps_noeud.debut + 1:corps_noeud.fin - 1]
                self.macros[nom] = {"n": 0, "defaut": None, "corps": corps}
            return None, False, fin
        return None, False, j

    c_gdef = c_def
    c_edef = c_def
    c_xdef = c_def

    def c_newcommand(self, n, noeuds, i):
        return None, False, i + 1

    c_renewcommand = c_newcommand

    def c_displayitempointstrue(self, n, noeuds, i):
        return "#displayitempoints(true)", True, i + 1

    def c_displayitempointsfalse(self, n, noeuds, i):
        return "#displayitempoints(false)", True, i + 1

    # ================================================================== réglages bfcours
    def _setter(self, n: Cmd, nom: str):
        f = self.cat.fonction(nom)
        a = n.arg("m")
        cles = self.cles(f, a.brut, "\\" + nom) if a else []
        if not cles:
            return None
        return construire_appel(nom, [], cles)

    def c_setrdexo(self, n, noeuds, i):
        return self._setter(n, "setrdexo"), True, i + 1

    def c_setrdcrep(self, n, noeuds, i):
        return self._setter(n, "setrdcrep"), True, i + 1

    def c_setrdmcq(self, n, noeuds, i):
        return self._setter(n, "setrdmcq"), True, i + 1

    # ================================================================== bandeaux
    def _bandeau(self, n: Cmd, nom: str):
        args_m = [a for a in n.args if a.genre == "m"]
        opt = n.arg("o")
        valeurs = {}
        if opt is not None:
            valeurs["niveau"] = self._niveau(opt.brut)
        noms = regles.OBLIGATOIRES_NOMMES[nom]
        for cle, a in zip(noms, args_m):
            if a.present and a.brut.strip():
                valeurs[cle] = self.contenu(a.enfants)
        return valeurs

    def _niveau(self, brut: str) -> Optional[str]:
        """Niveau du bandeau : forme courte connue (« 2nde » → exposant posé par le paquet), sinon contenu
        (« 1ère\\\\techno » → `[1#super[ère] \\ techno]`)."""
        lignes = [texte_simple(l) for l in re.split(r"\\\\(?:\[[^\]]*\])?|\\newline", brut)]
        lignes = [l.replace(" ", "") if k == 0 else l for k, l in enumerate(lignes) if l.strip()]
        if not lignes:
            return None
        if len(lignes) == 1 and lignes[0] in regles.NIVEAUX:
            return chaine(regles.NIVEAUX[lignes[0]])
        tete = re.sub(r"^(\d+)(ère|ere|re|ème|eme|e|nde|de|nd)$", r"\1#super[\2]", lignes[0])
        return "[" + " \\ ".join([tete] + [self.texte_brut(l) for l in lignes[1:]]) + "]"

    def c_chapitre(self, n, noeuds, i):
        return self._chapitre(n, noeuds, i, "chapitre")

    def c_chapEval(self, n, noeuds, i):
        return self._chapitre(n, noeuds, i, "chap-eval")

    def _chapitre(self, n, noeuds, i, nom):
        v = self._bandeau(n, nom)
        type_brut = texte_simple(n.args[-1].brut) if n.args else ""
        libre = type_brut.rstrip(" :").strip().lower() not in ("", "évaluation", "evaluation")
        if self.premier_bandeau and self.niveau == 0 and nom == "chap-eval" and libre:
            # bandeau d'évaluation à libellé propre (« Devoir : ») : écrit tel quel, le modèle ne pose rien
            self.premier_bandeau = False
            nommes = [f"{k}: {x}" for k, x in v.items() if x and k != "type"] + [f"type: [{type_brut}]"]
            return construire_appel("chap-eval", [], nommes), True, i + 1
        if self.premier_bandeau and self.niveau == 0:
            self.premier_bandeau = False
            for cle in ("niveau", "theme", "cycle", "etablissement"):
                if v.get(cle):
                    self.modele[cle] = v[cle]
            cle_type = regles.TYPES_DOCUMENT.get(type_brut.rstrip(" :").strip().lower(), "")
            if nom == "chap-eval":
                self.modele["type-document"] = '"evaluation"'
                if v.get("apres"):  # contenu sous le bandeau (souvent \tableauEval)
                    return sans_marqueurs(v["apres"])[1:-1].strip(), True, i + 1
            elif cle_type and type_brut.rstrip().endswith(":"):
                # type connu suivi de « : » (« Cours : ») : le type court suffit, « : » est le séparateur par défaut
                self.modele["type-document"] = cle_type
            elif type_brut:  # libellé exact du LaTeX (« Fiche 1 : », « Cours » sans deux-points)
                self.modele["type-document"] = "[" + self.texte_brut(type_brut) + "]"
            elif cle_type:
                self.modele["type-document"] = cle_type
            if v.get("zone-droite") and nom == "chapitre":
                self.modele["zone-droite"] = v["zone-droite"]
            return None, False, i + 1
        # bandeau suivant : un saut de page le précède (le pied de page suit le dernier bandeau de la page)
        nommes = [f"{k}: {x}" for k, x in v.items() if x]
        if nom == "chapitre" and type_brut:
            nommes = [x for x in nommes if not x.startswith("type:")] + [f"type: [{type_brut}]"]
        return construire_appel(nom, [], nommes), True, i + 1

    # ================================================================== exercices
    def e_EXO(self, n: Env) -> str:
        return self._exo(n, "EXO")

    def e_EXOEVAL(self, n: Env) -> str:
        return self._exo(n, "EXOEVAL")

    def _exo(self, n: Env, nom: str) -> str:
        f = self.cat.fonction(nom)
        ancien, self.dans_exo = self.dans_exo, True
        try:
            return self.appel_env(f, n.args, n.enfants, {}, quoi=nom)
        finally:
            self.dans_exo = ancien

    def c_exocorrection(self, n, noeuds, i):
        return "#exocorrection", True, i + 1

    def c_tcblower(self, n, noeuds, i):
        return "#tcblower", True, i + 1

    def c_rdexocorrection(self, n, noeuds, i):
        a = n.arg("m")
        liste = a.brut.strip() if a else "0"
        valeur = liste if re.fullmatch(r"\d+", liste) else chaine(liste)
        opts = n.arg("o")
        cles = self.cles(self.cat.fonction("rdexocorrection"), opts.brut, "\\rdexocorrection") if opts else []
        t = construire_appel("rdexocorrection", [valeur], cles)
        if not self.dans_si:
            self.rapport.a_reprendre.append("\\rdexocorrection hors \\ifcorrection : enveloppé dans #ifcorrection "
                                            "(sinon les corrigés s'affichent chez l'élève)")
            t = "#ifcorrection[" + t + "]"
        return t, True, i + 1

    def c_itempoint(self, n, noeuds, i):
        """\\tcbitempoint{n}[dy][dx] Texte… → #itempoint(n)[Texte…] (le texte de la question qui suit)."""
        f = self.cat.fonction("itempoint")
        points = n.arg("m").brut.strip() if n.arg("m") else "1"
        points = self._nombre(points) or points
        nommes = []
        opts = [a for a in n.args if a.genre == "o" and a.present]
        for cle, a in zip(("dy", "dx"), opts):
            l = self._longueur(a.brut)
            if l not in ("0pt", "-0pt", "0cm", "0mm"):
                nommes.append(f"{cle}: {l}")
        if n.nom == "dystcbitempoint":
            nommes.append("dys: true")
        j = i + 1
        pris: List[Noeud] = []
        while j < len(noeuds):
            x = noeuds[j]
            if isinstance(x, Par) or isinstance(x, BLOCS) or (isinstance(x, Cmd) and x.nom in FIN_QUESTION):
                break
            if isinstance(x, Maths) and x.mode != "inline":
                break
            pris.append(x)
            j += 1
        texte = self.sequence(pris).strip()
        if not texte:
            return construire_appel("itempoint", [points], nommes), False, j
        del f
        return construire_appel("itempoint", [points, crochets(texte)], nommes), False, j

    c_tcbitempoint = c_itempoint
    c_dystcbitempoint = c_itempoint

    # ================================================================== listes à pastilles, colonnes
    def _items(self, noeuds: Sequence[Noeud], separateur: str = "tcbitem") -> List[Tuple[Optional[Arg], List[Noeud]]]:
        """Découpe un corps aux \\tcbitem : [(options, nœuds de la case)]."""
        items: List[Tuple[Optional[Arg], List[Noeud]]] = []
        courant: Optional[List[Noeud]] = None
        for x in noeuds:
            if isinstance(x, Cmd) and x.nom == separateur:
                courant = []
                items.append((x.arg("o"), courant))
            elif courant is not None:
                courant.append(x)
        return items

    def _cles_item(self, opts: Optional[Arg]) -> List[str]:
        """Clés Typst d'un `\\tcbitem[options]` (vide si l'item n'a pas d'options connues)."""
        if opts is not None and opts.present and opts.brut.strip():
            brut = ", ".join(k + ("=" + v if v is not None else "") for k, v in self._options(opts.brut)
                             if k not in ("blankest", "blank", "enhanced", "nobeforeafter"))
            return self.cles(self.cat.fonction("tcbitem"), brut, "\\tcbitem") if brut else []
        return []

    def _ligne_item(self, puce: str, t: str) -> str:
        """Un item : `+ texte` (ou `- texte`), les lignes suivantes indentées de 2 espaces."""
        premiere, *suite = t.split("\n") if t else [""]
        ligne = (puce + " " + premiere) if premiere.strip() else puce
        if suite:
            ligne += "\n" + indenter("\n".join(suite))
        return ligne

    def _item_regle(self, cles: List[str], t: str) -> str:
        """Item à options : `#tcbitem(clés)[…]` sur sa propre ligne (jamais `+ #tcbitem`)."""
        return construire_appel("tcbitem", [crochets(self.proteger(t))], cles)

    def _corps_items(self, items, puce: str) -> str:
        """[(options, nœuds)] → un item par ligne ; un item à options connues devient `#tcbitem(clés)[…]`."""
        lignes = []
        for opts, contenu in items:
            self.niveau += 1
            try:
                t = self.sequence(contenu).strip()
            finally:
                self.niveau -= 1
            cles = self._cles_item(opts)
            lignes.append(self._item_regle(cles, t) if cles else self._ligne_item(puce, t))
        return "\n".join(lignes)

    @staticmethod
    def _alias_colonnes(nommes: List[str]) -> List[str]:
        """`raster-columns: n` s'écrit par son alias `columns: n` dans `#begin(…)`."""
        return [re.sub(r"^raster-columns:", "columns:", c) for c in nommes]

    def e_tcbenumerate(self, n: Env) -> str:
        f = self.cat.fonction("tcbenumerate")
        nommes: List[str] = []
        noms = regles.OPTIONNELS_NOMMES["tcbenumerate"]
        for cle, a in zip(noms, [a for a in n.args if a.genre == "o"]):
            if not a.present or not a.brut.strip():
                continue
            if self._est_cles(a.brut, f):
                nommes += self.cles(f, a.brut, "tcbenumerate")
                continue
            brut = a.brut.strip()
            if cle == "format":
                conv = regles.VALEURS_OPTIONNELS[("tcbenumerate", "format")]
                v = conv.get(brut) or next((v for k, v in conv.items() if brut.startswith(k)), chaine(brut))
                nommes.append(f"format: {v}")
            else:
                v = self._nombre(brut)
                if v is not None and not (cle == "raster-columns" and v == "1") and not (cle == "depart" and v == "1"):
                    nommes.append(f"{cle}: {v}")
        corps = self._corps_items(self._items(n.enfants), "+")
        if not corps:
            return ""
        return self.begin_end("tcbenumerate", [], self._alias_colonnes(nommes), corps)

    def e_MultiColonnes(self, n: Env) -> str:
        m = n.arg("m")
        colonnes = self._nombre(m.brut) if m else None
        corps = self._corps_items(self._items(n.enfants), "-")
        if not corps:
            return ""
        return self.begin_end("multi-colonnes", [colonnes] if colonnes else [], [], corps)

    e_Colonnes = e_MultiColonnes

    def e_tcbraster(self, n: Env) -> str:
        """tcbraster[options] dont les cases sont des tcolorbox : `#begin(tcbraster, clés)` et une case par `-`."""
        f = self.cat.fonction("tcbraster")
        opts = n.arg("o")
        nommes = self.cles(f, opts.brut, "tcbraster") if opts and opts.present else []
        items = []
        for x in n.enfants:
            if isinstance(x, Env) and x.nom == "tcolorbox":
                items.append((x.arg("o"), x.enfants))
        if not items:
            items = self._items(n.enfants)
        corps = self._corps_items(items, "-")
        if not corps:
            return ""
        return self.begin_end("tcbraster", [], self._alias_colonnes(nommes), corps)

    e_tcbitemize = e_tcbraster

    def e_tcolorbox(self, n: Env) -> str:
        """tcolorbox isolée → `#begin(boite, clés)[Titre]` : les clés tcolorbox connues de boite passent, le reste est noté."""
        f = self.cat.fonction("boite")
        opts = n.arg("o")
        titre = None
        nommes: List[str] = []
        if opts is not None and opts.present:
            options = self._options(opts.brut)
            garde = []
            for k, v in options:
                if k == "title" and v:
                    titre = "[" + self.markup_depuis(v, True) + "]"
                elif k in ("blankest", "blank", "nobeforeafter", "enhanced", "auto outer arc"):
                    continue
                else:
                    garde.append((k, v))
            brut = ", ".join(k + ("=" + v if v is not None else "") for k, v in garde)
            nommes = self.cles(f, brut, "tcolorbox → boite") if brut else []
        return self.begin_end("boite", [titre] if titre else [], nommes, self.corps_env(n.enfants))

    # ================================================================== zones de réponse
    def e_crep(self, n: Env) -> str:
        f = self.cat.fonction("crep")
        opts = n.arg("o")
        nommes = self.cles(f, opts.brut, "crep") if opts and opts.present else []
        enfants = list(n.enfants)
        # \repline[k] à la fin de la crep : lignes vides en plus
        while enfants and _vide(enfants[-1]):
            enfants.pop()
        if enfants and isinstance(enfants[-1], Cmd) and enfants[-1].nom == "repline":
            o = enfants[-1].arg("o")
            k = self._nombre(o.brut) if o and o.present else "1"
            nommes.append(f"extra-lines: {k or 1}")
            enfants.pop()
        return self.begin_end("crep", [], nommes, self.corps_env(enfants))

    def c_repline(self, n, noeuds, i):
        o = n.arg("o")
        k = self._nombre(o.brut) if o and o.present else "1"
        return f"#crep(lines: {k or 1})[]", True, i + 1

    def c_tccrep(self, n, noeuds, i):
        f = self.cat.fonction("tccrep")
        opts = n.arg("o")
        nommes = self.cles(f, opts.brut, "tccrep") if opts and opts.present else []
        m = [a for a in n.args if a.genre == "m" and a.present]
        if n.nom == "tcautocrep" or len(m) < 2:
            largeur, corps = "auto", (m[-1] if m else None)
        else:
            largeur, corps = self._longueur(m[0].brut), m[1]
        if largeur.startswith('"'):
            largeur = "auto"
        return construire_appel("tccrep", [largeur, self.contenu_arg(corps)], nommes)

    c_tcautocrep = c_tccrep

    def c_repsim(self, n, noeuds, i):
        f = self.cat.fonction("repsim")
        opts = n.arg("o")
        nommes = []
        if opts and opts.present and opts.brut.strip():
            if self._est_cles(opts.brut, self.cat.fonction("tccrep")):
                nommes = self.cles(self.cat.fonction("tccrep"), opts.brut, "repsim")
            else:
                nommes = [f"largeur: {self._longueur(opts.brut)}"]
        del f
        return construire_appel("repsim", [self.contenu_arg(n.arg("m"))], nommes)

    def c_dotfills(self, n, noeuds, i):
        return "#tcfillcrep[]"

    # ================================================================== QCM, compétences
    def c_McqQuest(self, n, noeuds, i):
        f = self.cat.fonction("McqQuest")
        opts = n.arg("o")
        nommes = []
        if opts and opts.present:
            for k, v in self._options(opts.brut):
                if k == "br" and v is not None:
                    vals = [x.strip() for x in v.split(",") if x.strip()]
                    nommes.append("br: " + (vals[0] if len(vals) == 1 else "(" + ", ".join(vals) + ")"))
                else:
                    nommes += self.cles(f, k + ("=" + v if v is not None else ""), "McqQuest")
        m = [a for a in n.args if a.genre == "m" and a.present]
        question = self.contenu(m[0].enfants) if m else "[]"
        reponses = []
        if len(m) > 1:
            for morceau in _couper_virgules(m[1].brut):
                reponses.append("[" + self.markup_depuis(morceau.strip(), True) + "]")
        cases = [question] + reponses
        tete = "#mcq-quest" + ("(" + ", ".join(nommes) + ")" if nommes else "")
        if sum(len(sans_marqueurs(c)) for c in cases) < 90 and all("\n" not in sans_marqueurs(c) for c in cases):
            return tete + "".join(cases), True, i + 1
        # long : un argument par ligne, entre parenthèses (des crochets sur des lignes séparées ne seraient
        # plus rattachés à l'appel)
        return "#mcq-quest(\n" + ",\n".join(indenter(x) for x in nommes + cases) + ",\n)", True, i + 1

    def c_tableaucompetence(self, n, noeuds, i):
        a = n.arg("m")
        if not a:
            return None
        items = []
        for x in a.enfants:
            if isinstance(x, Cmd) and x.nom == "competence":
                code = x.arg("o")
                corps = x.arg("m")
                cle = [f"code: {chaine(texte_simple(code.brut))}"] if code and code.present and code.brut.strip() else []
                items.append(construire_appel("competence", [self.contenu_arg(corps)], cle, diese=False))
        if not items:
            return "#tableaucompetence()", True, i + 1
        return "#tableaucompetence(\n" + ",\n".join(indenter(x) for x in items) + ",\n)", True, i + 1

    c_tableaucompetenceEval = c_tableaucompetence

    # ================================================================== nombres, grandeurs, maths en texte
    def c_num(self, n, noeuds, i):
        a = n.arg("m")
        if not a:
            return None
        brut = a.brut.strip()
        v = self._nombre(brut.replace(" ", "").replace("\\,", "").replace("~", ""))
        return f"#num({v})" if v is not None else f"#num({chaine(brut)})"

    c_np = c_num
    c_nombre = c_num

    def c_SI(self, n, noeuds, i):
        m = [a for a in n.args if a.genre == "m" and a.present]
        if len(m) < 2:
            return None
        v = self._nombre(m[0].brut) or chaine(self.developper(m[0].brut).strip())
        unite = maths._unite(self.developper(m[1].brut))
        if not _unite_connue(unite):  # « minutes », « élèves » : du texte, pas une unité SI
            return f"#num({v})~{self.texte_brut(unite)}"
        return f"#qty({v}, {chaine(unite)})"

    c_qty = c_SI

    def c_si(self, n, noeuds, i):
        a = n.arg("m")
        return f"#unit({chaine(maths._unite(a.brut))})" if a else None

    c_unit = c_si

    def _maths_en_texte(self, n, noeuds, i):
        source = self.texte[n.debut:n.fin]
        r = maths.convertir(source, macros=self.macros_maths(), macros_utilisateur=self.macros)
        return "$" + r.texte + "$"

    c_Vecteur = _maths_en_texte
    c_Coordonnees = _maths_en_texte
    c_intervalle = _maths_en_texte
    c_CrochetG = _maths_en_texte
    c_CrochetD = _maths_en_texte
    c_vv = _maths_en_texte

    def c_ensuremath(self, n, noeuds, i):
        a = n.arg("m")
        return "$" + maths.convertir(a.brut, macros=self.macros_maths(), macros_utilisateur=self.macros).texte + "$"

    def c_tikzinclude(self, n, noeuds, i):
        a = n.arg("m")
        nom = a.brut.strip() if a else ""
        d = self.macros.get("tikzfig" + nom)
        if not d:
            return self.a_reprendre(self.texte[n.debut:n.fin], f"figure \\tikzfig{nom} introuvable"), False, i + 1
        return self.extrait(d["corps"], f"figure \\tikzinclude{{{nom}}}", "tikzpicture"), True, i + 1

    def c_textbullet(self, n, noeuds, i):
        """« \\textbullet Texte » en début de paragraphe : un élément de liste (`- Texte`)."""
        precedent = noeuds[i - 1] if i > 0 else None
        debut_ligne = precedent is None or isinstance(precedent, Par) or \
            (isinstance(precedent, Texte) and re.search(r"(^|\n)[ \t]*$", precedent.s)) or \
            (isinstance(precedent, Cmd) and precedent.nom in ("\\\\", "par", "tcbitem"))
        j = i + 1
        if j < len(noeuds) and isinstance(noeuds[j], Cmd) and noeuds[j].nom in (" ", "car_32") or \
                j < len(noeuds) and isinstance(noeuds[j], Groupe) and not noeuds[j].enfants:
            j += 1
        # « \textbullet{} texte » : l'espace qui suit est déjà dans le texte, ne pas la doubler
        espace = "" if j < len(noeuds) and isinstance(noeuds[j], Texte) and noeuds[j].s[:1] in (" ", "\t") else " "
        if debut_ligne:
            return "\n-" + espace, False, j
        return "•" + espace, False, j

    def c_item(self, n, noeuds, i):  # \item hors liste
        return "\n- ", False, i + 1

    def c_tcbitem(self, n, noeuds, i):  # \tcbitem hors disposition
        return None, False, i + 1

    def c_caption(self, n, noeuds, i):
        return None, False, i + 1

    # ================================================================== listes
    def e_itemize(self, n: Env) -> str:
        return self._liste(n, "-")

    def e_enumerate(self, n: Env) -> str:
        return self._liste(n, "+")

    def e_description(self, n: Env) -> str:
        return self._liste(n, "/")

    def _liste(self, n: Env, puce: str) -> str:
        items = self._items(n.enfants, "item")
        lignes = []
        for opt, contenu in items:
            self.niveau += 1
            try:
                t = self.sequence(contenu).strip()
            finally:
                self.niveau -= 1
            etiquette = self.markup_depuis(opt.brut, True) if opt is not None and opt.present else None
            if puce == "/":
                tete = f"/ {etiquette or ''}: "
            elif etiquette is not None:
                tete = f"{puce} {etiquette} "
                if puce == "-" and etiquette.strip() in ("", "•", "$bullet$"):
                    tete = "- "
            else:
                tete = puce + " "
            premiere, *suite = t.split("\n") if t else [""]
            ligne = tete + premiere
            if suite:
                ligne += "\n" + indenter("\n".join(suite))
            lignes.append(ligne)
        texte = "\n".join(lignes)
        opts = n.arg("o")
        motif = _numerotation(opts.brut) if puce == "+" and opts is not None and opts.present else None
        if puce == "/" or self.niveau_tableau > 0:
            # description, ou liste dans une cellule de tableau (élément opaque) : balisage natif
            if motif:
                return f"#[\n#set enum(numbering: {chaine(motif)})\n" + texte + "\n]"
            return texte
        nommes = [f"label: {chaine(motif)}"] if motif else []
        return self.begin_end("enumerate" if puce == "+" else "itemize", [], nommes, texte)

    # ================================================================== alignements, boîtes simples
    def e_center(self, n: Env) -> str:
        corps = self.sequence(n.enfants)
        nu = sans_marqueurs(corps).strip()
        if nu.startswith(("#latex", "#tabvar", "#image", "#ifcorrection[\n  #latex")) and "\n\n" not in nu:
            return corps  # extraits et tableaux sont déjà centrés
        return "#align(center)" + crochets(self.proteger(corps))

    def e_flushright(self, n: Env) -> str:
        return "#align(right)" + crochets(self.proteger(self.sequence(n.enfants)))

    def e_flushleft(self, n: Env) -> str:
        return self.sequence(n.enfants)

    def e_quote(self, n: Env) -> str:
        return "#quote(block: true)" + crochets(self.proteger(self.sequence(n.enfants)))

    e_quotation = e_quote

    def e_multicols(self, n: Env) -> str:
        m = n.arg("m")
        k = self._nombre(m.brut) if m else "2"
        return f"#columns({k or 2})" + crochets(self.proteger(self.sequence(n.enfants)))

    e_multicols_etoile = e_multicols

    def e_figure(self, n: Env) -> str:
        legende = next((x for x in n.enfants if isinstance(x, Cmd) and x.nom == "caption"), None)
        corps = self.sequence(n.enfants)
        if legende is not None:
            corps = self.proteger(corps)
        if legende is not None:
            return "#figure(" + crochets(corps) + ", caption: " + self.contenu_arg(legende.arg("m")) + ")"
        return corps

    e_table = e_figure

    def _taille_env(self, n: Env) -> str:
        return f"#text(size: {regles.TAILLES[n.nom]})" + crochets(self.sequence(n.enfants))

    e_tiny = e_scriptsize = e_footnotesize = e_small = e_large = e_Large = e_LARGE = e_huge = e_Huge = _taille_env

    def e_spacing(self, n: Env) -> str:
        return self.sequence(n.enfants)

    e_adjustbox = e_spacing

    # ================================================================== minipages côte à côte
    def s_minipage(self, noeuds: Sequence[Noeud], i: int):
        groupe: List[Env] = [noeuds[i]]
        j = i + 1
        while j < len(noeuds):
            x = noeuds[j]
            if _vide(x) or (isinstance(x, Cmd) and x.nom in ("hfill", "hspace", "quad", "qquad", "noindent")) \
                    or isinstance(x, Car) and x.c == "~":
                j += 1
                continue
            if isinstance(x, Env) and x.nom == "minipage":
                groupe.append(x)
                j += 1
                continue
            break
        while j - 1 > i and not isinstance(noeuds[j - 1], Env):
            j -= 1
        largeurs, contenus = [], []
        for mp in groupe:
            m = mp.arg("m")
            l = self._longueur(m.brut) if m else "100%"
            largeurs.append(l)
            self.niveau += 1
            try:
                contenus.append(self.sequence(mp.enfants).strip())
            finally:
                self.niveau -= 1
        if len(groupe) == 1:
            l = largeurs[0]
            if l == "100%":
                return contenus[0], j
            return f"#block(width: {l})" + crochets(self.proteger(contenus[0])), j
        proportions = _proportions(largeurs)
        nommes = [f"largeurs: ({', '.join(proportions)})"] if proportions else []
        corps = "\n".join(self._ligne_item("-", t) for t in contenus)
        return self.begin_end("multi-colonnes", [str(len(groupe))] if not nommes else [], nommes, corps), j

    # ================================================================== tableaux
    niveau_tableau = 0

    def _rangees(self, noeuds: Sequence[Noeud]):
        """Corps d'un tabular → [(filet_avant, [cellules (nœuds)])]."""
        rangees, cellules, courante = [], [], []
        filet = False
        for x in noeuds:
            if isinstance(x, Cmd) and x.nom == "\\\\":
                cellules.append(courante)
                rangees.append((filet, cellules))
                cellules, courante, filet = [], [], False
            elif isinstance(x, Car) and x.c == "&":
                cellules.append(courante)
                courante = []
            elif isinstance(x, Cmd) and x.nom in ("hline", "toprule", "midrule", "bottomrule"):
                filet = True
            elif isinstance(x, Cmd) and x.nom in ("cline", "arrayrulecolor", "noalign", "rowcolor" if False else ""):
                continue
            else:
                courante.append(x)
        if any(not _vide(c) for c in courante) or cellules:
            cellules.append(courante)
            rangees.append((filet, cellules))
        return [(f, c) for f, c in rangees if any(any(not _vide(y) for y in cel) for cel in c) or f]

    def _cellule(self, noeuds: List[Noeud], natif: bool) -> Tuple[str, int, int]:
        """Une cellule → (Typst, colonnes couvertes, rangées couvertes)."""
        noeuds = [x for x in noeuds]
        while noeuds and _vide(noeuds[0]):
            noeuds.pop(0)
        while noeuds and _vide(noeuds[-1]):
            noeuds.pop()
        colspan, rowspan, fond = 1, 1, None
        if noeuds and isinstance(noeuds[0], Cmd) and noeuds[0].nom == "multicolumn":
            mc = [a for a in noeuds[0].args if a.genre == "m"]
            colspan = int(self._nombre(mc[0].brut) or 1)
            noeuds = mc[2].enfants if len(mc) > 2 else []
        if noeuds and isinstance(noeuds[0], Cmd) and noeuds[0].nom == "multirow":
            mr = [a for a in noeuds[0].args if a.genre == "m"]
            rowspan = int(self._nombre(mr[0].brut) or 1)
            noeuds = mr[-1].enfants
        reste = []
        for x in noeuds:
            if isinstance(x, Cmd) and x.nom == "cellcolor":
                c = x.arg("m")
                fond = c.brut.strip() if c else None
            else:
                reste.append(x)
        self.niveau_tableau += 1
        self.niveau += 1
        try:
            t = self.proteger(self.sequence(reste).strip())
        finally:
            self.niveau_tableau -= 1
            self.niveau -= 1
        cles = []
        if colspan > 1:
            cles.append(f"colspan: {colspan}")
        if rowspan > 1:
            cles.append(f"rowspan: {rowspan}")
        if fond:
            cles.append(f"fill: xcolor({chaine(fond)})")
        if cles:
            return "table.cell(" + ", ".join(cles) + ")" + crochets(t), colspan, rowspan
        return crochets(t), colspan, rowspan

    def _cellules(self, noeuds: Sequence[Noeud], nb_colonnes: int, natif: bool) -> Tuple[List[str], bool]:
        lignes: List[str] = []
        a_filets = False
        occupees = {}  # colonne → rangées encore couvertes par un multirow
        for filet, cellules in self._rangees(noeuds):
            if filet:
                a_filets = True
            if filet and natif and lignes:
                lignes.append("table.hline(),")
            rangee, col = [], 0
            for cel in cellules:
                while occupees.get(col, 0) > 0:
                    occupees[col] -= 1
                    col += 1
                    if not any(not _vide(y) for y in cel):
                        cel = None
                        break
                if cel is None:
                    continue
                t, cs, rs = self._cellule(cel, natif)
                if rs > 1:
                    for k in range(cs):
                        occupees[col + k] = rs - 1
                rangee.append(t)
                col += cs
            lignes.append(", ".join(rangee) + ",")
        return lignes, a_filets

    def _tabular(self, n: Env, specification: str, largeur: Optional[str] = None) -> str:
        colonnes, alignements, verticaux = _colonnes(specification, self._longueur)
        lignes, filets = self._cellules(n.enfants, len(colonnes), True)
        tete = [f"columns: ({', '.join(colonnes)}{',' if len(colonnes) == 1 else ''})",
                f"align: ({', '.join(alignements)}{',' if len(alignements) == 1 else ''})"]
        if verticaux or filets:
            tete.append("stroke: 0.4pt")
        else:
            tete.append("stroke: none")
        corps = "\n".join(tete[i] + "," for i in range(len(tete))) + "\n" + "\n".join(lignes)
        t = "#table(\n" + indenter(corps) + "\n)"
        if largeur:
            t = f"#block(width: {largeur})[\n" + indenter(t) + "\n]"
        return t

    def e_tabular(self, n: Env) -> str:
        spec = next((a.brut for a in n.args if a.genre == "m" and a.present), "c")
        return self._tabular(n, spec)

    e_array = e_tabular

    def e_tabularx(self, n: Env) -> str:
        m = [a for a in n.args if a.genre == "m" and a.present]
        largeur = self._longueur(m[0].brut) if m else "100%"
        spec = m[1].brut if len(m) > 1 else "X"
        return self._tabular(n, spec, largeur)

    def e_tabular_etoile(self, n: Env) -> str:
        return self.e_tabularx(n)

    def e_tcbtab(self, n: Env) -> str:
        return self._tcbtab(n, n.nom)

    e_tcbtabc = e_tcbtab
    e_tcbtabx = e_tcbtab
    e_tcbtabcomp = e_tcbtab

    def _tcbtab(self, n: Env, nom: str) -> str:
        f, imposees = self.cat.pour_latex(nom)
        if f is None:
            f, imposees = self.cat.fonction("tcbtab"), {}
        opts = n.arg("o")
        spec_arg = next((a for a in n.args if a.genre == "m" and a.present), None)
        spec = spec_arg.brut.strip() if spec_arg else "c"
        nommes = [f"{k}: {v}" for k, v in imposees.items()]
        if opts is not None and opts.present and opts.brut.strip():
            if self._est_cles(opts.brut, f):
                nommes += self.cles(f, opts.brut, nom)
            else:  # \begin{tcbtab}[Titre]{spec}
                nommes.append("title: " + self.contenu(opts.enfants))
        lignes, _ = self._cellules(n.enfants, 0, False)
        # rangée d'en-tête colorée par \cellcolor{currentTableColbackTitleColor} → entete: true
        if lignes and "currentTableColbackTitleColor" in lignes[0]:
            lignes[0] = re.sub(r'table\.cell\(fill: xcolor\("currentTableColbackTitleColor"\)\)', "", lignes[0])
            lignes[0] = re.sub(r"\\textcolor\(\"currentTableColTitleColor\"\)", "", lignes[0])
            nommes.append("entete: true")
        tete = [chaine(spec)] + nommes
        return "#tcbtab(\n" + indenter(",\n".join(tete) + ",\n" + "\n".join(lignes)) + "\n)"

    # ================================================================== code
    def _code(self, n: Env, langage: str = "") -> str:
        code = n.brut_corps.strip("\n")
        clotures = "````" if "```" in code else "```"
        return f"{clotures}{langage}\n{code}\n{clotures}"

    def e_verbatim(self, n: Env) -> str:
        return self._code(n)

    def e_lstlisting(self, n: Env) -> str:
        o = re.search(r"language\s*=\s*\{?(\w+)", n.brut_corps[:0] + (self.texte[n.debut:n.corps_debut]))
        corps = re.sub(r"^\s*\[[^\]]*\]", "", n.brut_corps)
        n2 = Env(n.debut, n.fin, n.nom, n.args, [], corps)
        return self._code(n2, (o.group(1).lower() if o else ""))

    def e_minted(self, n: Env) -> str:
        m = re.match(r"\s*(?:\[[^\]]*\])?\s*\{(\w+)\}", n.brut_corps)
        corps = n.brut_corps[m.end():] if m else n.brut_corps
        return self._code(Env(n.debut, n.fin, n.nom, n.args, [], corps), m.group(1) if m else "")

    def _python(self, n: Env) -> str:
        corps = re.sub(r"^\s*\[[^\]]*\]", "", n.brut_corps)
        bloc = self._code(Env(n.debut, n.fin, n.nom, n.args, [], corps), "python")
        return self.begin_end("bf-code-python", [], [], bloc) if self.cat.fonction("BFCodePython") else bloc

    e_CodePython = e_CodePythonLst = e_BFCodePython = e_codePython = e_pythoncode = _python

    # ================================================================== figures
    def e_tikzpicture(self, n: Env) -> str:
        code = self.texte[n.debut:n.fin]
        if "\\tkzTabInit" in code:
            t = tkztab_vers_tabvar(code, self)
            if t:
                return t
        return self.extrait(code, "figure TikZ", "tikzpicture")


INDENT_RQ = "  "

_SYMBOLES_SI = {"m", "g", "s", "L", "l", "h", "min", "A", "V", "W", "J", "N", "Pa", "Hz", "K", "mol", "cd", "°C", "°",
                "€", "%", "t", "ha", "a", "bar", "Wh", "B", "o", "Ω", "lx", "dB"}
_PREFIXES_SI = ("k", "h", "da", "d", "c", "m", "µ", "n", "M", "G", "T")


def _unite_connue(u: str) -> bool:
    """Unité que `qty` sait lire : symboles SI (préfixés), puissances ² ³, produits ⋅ et quotients /."""
    for morceau in re.split(r"[/⋅·*]", u.replace(" ", "")):
        base = morceau.rstrip("²³")
        if not base:
            return False
        if base in _SYMBOLES_SI:
            continue
        if any(base.startswith(p) and base[len(p):] in _SYMBOLES_SI for p in _PREFIXES_SI):
            continue
        return False
    return True


def _couper_virgules(brut: str) -> List[str]:
    """Réponses d'un \\McqQuest : virgules de premier niveau, hors formules et groupes."""
    morceaux, prof, maths_ouvertes, cour = [], 0, False, ""
    i = 0
    while i < len(brut):
        c = brut[i]
        if c == "\\" and i + 1 < len(brut):
            cour += brut[i:i + 2]
            i += 2
            continue
        if c == "$":
            maths_ouvertes = not maths_ouvertes
        elif c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
        if c == "," and prof == 0 and not maths_ouvertes:
            morceaux.append(cour)
            cour = ""
        else:
            cour += c
        i += 1
    if cour.strip():
        morceaux.append(cour)
    return morceaux


def _numerotation(brut: str) -> Optional[str]:
    m = re.search(r"label\s*=\s*\{?(.*?)\}?\s*(?:,|$)", brut)
    motif = m.group(1) if m else brut
    for latex, typst in (("\\arabic*", "1"), ("\\alph*", "a"), ("\\Alph*", "A"), ("\\roman*", "i"),
                         ("\\Roman*", "I")):
        if latex in motif:
            return motif.replace(latex, typst).replace("{", "").replace("}", "").strip()
    if re.fullmatch(r"\s*[aAiI1][.)]\s*", motif):
        return motif.strip()
    return None


def _proportions(largeurs: List[str]) -> List[str]:
    """Largeurs de minipages → proportions entières pour `largeurs:` de MultiColonnes."""
    vals = []
    for l in largeurs:
        m = re.fullmatch(r"(-?[\d.]+)(%|cm|mm|pt|em)", l)
        if not m:
            return []
        v = float(m.group(1)) * {"%": 1, "cm": 10, "mm": 1, "pt": 0.35, "em": 4}[m.group(2)] * (1 if m.group(2) != "%" else 1)
        vals.append(v)
    if not vals or min(vals) <= 0:
        return []
    if max(vals) / min(vals) < 1.05:
        return []  # colonnes égales : le nombre suffit
    return [str(round(v)) for v in vals]


def _colonnes(spec: str, longueur):
    """Spécification de colonnes LaTeX → (largeurs, alignements, filets verticaux)."""
    s = re.sub(r"[@<>!]\{(?:[^{}]|\{[^{}]*\})*\}", "", spec)
    while True:
        m = re.search(r"\*\{(\d+)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", s)
        if not m:
            break
        s = s[: m.start()] + m.group(2) * int(m.group(1)) + s[m.end():]
    colonnes, alignements = [], []
    verticaux = "|" in s
    i = 0
    while i < len(s):
        c = s[i]
        if c in "lcr":
            colonnes.append("auto")
            alignements.append({"l": "left", "c": "center", "r": "right"}[c])
        elif c in "pmb" and s[i + 1: i + 2] == "{":
            fin = s.index("}", i)
            colonnes.append(longueur(s[i + 2: fin]))
            alignements.append("left" if c != "m" else "left + horizon")
            i = fin
        elif c == "X":
            colonnes.append("1fr")
            alignements.append("left")
        elif c in "SCLR":
            colonnes.append("auto")
            alignements.append("center")
        i += 1
    if not colonnes:
        colonnes, alignements = ["auto"], ["center"]
    return colonnes, alignements, verticaux


def tkztab_vers_tabvar(code: str, conv) -> Optional[str]:
    """Tableau tkz-tab (\\tkzTabInit, \\tkzTabLine, \\tkzTabVar) → #tabvar(…) ; None si inconvertible."""
    if re.search(r"\\tkzTab(Ima|Val|Slope|Tan|IniVar)", code):
        return None
    m = re.search(r"\\tkzTabInit\s*(?:\[([^\]]*)\])?\s*\{", code)
    if not m:
        return None
    from .ecriture import fin_groupe
    d1 = m.end() - 1
    f1 = fin_groupe(code, d1)
    lignes_init = code[d1 + 1: f1 - 1]
    m2 = re.match(r"\s*\{", code[f1:])
    if not m2:
        return None
    d2 = f1 + m2.end() - 1
    f2 = fin_groupe(code, d2)
    valeurs_x = code[d2 + 1: f2 - 1]

    def formule(t: str) -> str:
        t = t.strip()
        if t.startswith("$") and t.endswith("$"):
            t = t[1:-1]
        return maths.convertir(t, macros=conv.macros_maths(), macros_utilisateur=conv.macros).texte

    def contenu_nom(t: str) -> str:
        t = t.strip()
        if t.startswith("$") and t.endswith("$") and t.count("$") == 2:
            return "$" + formule(t) + "$"
        return "[" + conv.markup_depuis(t, True) + "]"

    noms = []
    for morceau in _couper_virgules(lignes_init):
        if "/" in morceau:
            nom, h = morceau.rsplit("/", 1)
        else:
            nom, h = morceau, "1"
        noms.append((contenu_nom(nom), conv._nombre(h) or "1"))
    xs = [chaine(formule(x)) for x in _couper_virgules(valeurs_x)]
    lignes = []
    rang = 1
    for mm in re.finditer(r"\\tkzTab(Line|Var)\s*(?:\[[^\]]*\])?\s*\{", code):
        d = mm.end() - 1
        f = fin_groupe(code, d)
        brut = code[d + 1: f - 1]
        if rang >= len(noms):
            return None
        nom, h = noms[rang]
        rang += 1
        if mm.group(1) == "Line":
            elements = []
            for e in brut.split(","):
                e = e.strip()
                if re.fullmatch(r"[+\-ztdh|]?", e):
                    elements.append(e)
                else:
                    elements.append(formule(e))
            spec = ",".join(elements)
            cle_h = f", h: {h}" if h not in ("1",) else ""
            lignes.append(f"tkz-tab-line({nom}, {chaine(spec)}{cle_h})")
        else:
            items = []
            for e in _couper_virgules(brut):
                e = e.strip()
                if not e:
                    continue
                parties = e.split("/")
                signe = parties[0].strip()
                if len(parties) == 1 or all(not p.strip() for p in parties[1:]):
                    items.append(chaine(signe))
                else:
                    vals = [chaine(formule(p)) for p in parties[1:] if p.strip() or True]
                    items.append("(" + ", ".join([chaine(signe)] + vals) + ")")
            cle_h = f", h: {h}" if h not in ("2",) else ""
            lignes.append(f"tkz-tab-var({nom}, {', '.join(items)}{cle_h})")
    if not lignes:
        return None
    nommes = []
    if m.group(1):
        for k, v in conv._options(m.group(1)):
            if k in ("lgt", "espcl") and v and conv._nombre(v):
                nommes.append(f"{k}: {conv._nombre(v)}cm")
    tete_x = "(" + ", ".join(xs) + ("," if len(xs) == 1 else "") + ")"
    args = [tete_x] + lignes + nommes
    nom_x = noms[0][0] if noms else None
    if nom_x and nom_x.replace(" ", "") not in ("$x$",):
        args.append(f"nom-x: {nom_x}")
    return "#tabvar(\n" + ",\n".join(indenter(a) for a in args) + ",\n)"
