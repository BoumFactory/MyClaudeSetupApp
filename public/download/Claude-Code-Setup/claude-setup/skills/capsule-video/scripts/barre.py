"""Affichage de la progression d'un rendu : grand pourcentage en chiffres géants, barre, vitesse, temps restant.

Dans une vraie console (TTY) : bloc redessiné sur place (séquences ANSI) et titre de la fenêtre mis à jour
(« 47 % — Rendu … »). Sinon (sortie redirigée, journal) : une ligne de texte simple toutes les 5 s.
"""
import os
import sys
import time

CHIFFRES = {
    "0": ["█████", "█   █", "█   █", "█   █", "█████"],
    "1": ["  ██ ", " ███ ", "  ██ ", "  ██ ", " ████"],
    "2": ["█████", "    █", "█████", "█    ", "█████"],
    "3": ["█████", "    █", " ████", "    █", "█████"],
    "4": ["█   █", "█   █", "█████", "    █", "    █"],
    "5": ["█████", "█    ", "█████", "    █", "█████"],
    "6": ["█████", "█    ", "█████", "█   █", "█████"],
    "7": ["█████", "    █", "   █ ", "  █  ", "  █  "],
    "8": ["█████", "█   █", "█████", "█   █", "█████"],
    "9": ["█████", "█   █", "█████", "    █", "█████"],
    ",": ["     ", "     ", "     ", "  ██ ", " ██  "],
    "%": ["██  █", "██ █ ", "  █  ", " █ ██", "█  ██"],
    " ": ["   ", "   ", "   ", "   ", "   "],
}
VIOLET, VERT, GRIS, GRAS, RAZ = "\x1b[38;5;135m", "\x1b[38;5;42m", "\x1b[38;5;245m", "\x1b[1m", "\x1b[0m"


def duree_lisible(s):
    s = int(max(0, s))
    return f"{s // 60} min {s % 60:02d} s" if s >= 60 else f"{s} s"


class Barre:
    def __init__(self, titre, total, unite="images"):
        self.titre, self.total, self.unite = titre, max(1, total), unite
        self.tty = sys.stdout.isatty()
        self.t0 = time.time()
        self.hauteur = 0
        self.dernier_texte = 0.0
        if self.tty and sys.platform == "win32":
            os.system("")  # active les séquences ANSI de la console Windows

    def maj(self, fait, detail=""):
        pct = 100 * min(fait, self.total) / self.total
        el = time.time() - self.t0
        vitesse = fait / el if el > 0 else 0
        reste = (self.total - fait) / vitesse if vitesse > 0 else 0
        infos = f"{fait}/{self.total} {self.unite} · {vitesse:.1f}/s · écoulé {duree_lisible(el)} · reste ≈ {duree_lisible(reste)}"
        if detail:
            infos += f" · {detail}"
        if not self.tty:
            if time.time() - self.dernier_texte >= 5 or fait >= self.total:
                print(f"  {pct:5.1f} %  {infos}", flush=True)
                self.dernier_texte = time.time()
            return
        texte = f"{pct:.1f}".replace(".", ",") + " %"
        lignes = [" ".join(CHIFFRES[c][r] for c in texte) for r in range(5)]
        largeur = 60
        plein = int(largeur * pct / 100)
        couleur = VERT if fait >= self.total else VIOLET
        bloc = [f"{GRAS}{self.titre}{RAZ}", ""]
        bloc += [f"   {couleur}{l}{RAZ}" for l in lignes]
        bloc += ["", f"   {couleur}{'█' * plein}{GRIS}{'░' * (largeur - plein)}{RAZ}", f"   {GRIS}{infos}{RAZ}", ""]
        sortie = f"\x1b]0;{pct:.0f} % — {self.titre}\x07"
        if self.hauteur:
            sortie += f"\x1b[{self.hauteur}F\x1b[J"
        sortie += "\n".join(bloc) + "\n"
        sys.stdout.write(sortie)
        sys.stdout.flush()
        self.hauteur = len(bloc)

    def message(self, texte):
        """Ligne fixe au-dessus de la barre suivante (la barre courante reste affichée)."""
        self.hauteur = 0
        print(texte, flush=True)
