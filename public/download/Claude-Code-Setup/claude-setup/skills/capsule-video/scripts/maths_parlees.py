"""Forme orale des notations mathématiques : outil de RELECTURE du script, jamais de traduction silencieuse.

Le script d'une capsule s'écrit pour l'oreille (references/voix-synthese.md) : les mots du script sont les mots
dits, et l'ancrage des gestes (@b05~"mot") se résout sur eux. Ce module ne branche donc rien dans la chaîne
audio : relire_script.py l'appelle sur chaque temps fort et PROPOSE la forme orale quand le texte contient
des notations (« $R-I-S$ » → « R I S », « \\frac{0+2}{2} » → « 0 plus 2, le tout divisé par 2 »). Claude
corrige alors script.md lui-même (ou relire_script.py --appliquer réécrit le script après sauvegarde).

Règles reprises de l'outil d'un collègue (rd), corrigées (essais du 20/10/2026) :
- pas de « plusse » ni de « vinte » (rustines propres à Piper, déjà dans voix.py ; Pocket les lirait tels quels) ;
- les nombres restent en chiffres (voix.py et voix_pocket.py les disent) ; nombres=True les écrit en lettres,
  milliers « 3 200 » compris, « 12,5 % » → « douze virgule cinq pour cent » ;
- seuls les noms de points sont épelés (après un mot géométrique, entre crochets ou parenthèses, avant
  « au carré ») : IA, QCM, PGCD, OK, ET restent des mots ;
- « 3(x + 2) » → « 3 fois, entre parenthèses, x plus 2 » (et non « trois facteur de… »).

Usage :
    python maths_parlees.py "texte"          # forme orale proposée
    python maths_parlees.py --test           # auto-test
"""
import re
import sys

SEP = " "   # séparateur des lettres épelées : « vecteur A B » (convention des scripts existants)

MOTS_GEO = (r"(?:[Ss]egments?|[Tt]riangles?|[Qq]uadrilatères?|[Rr]ectangles?|[Cc]arrés?|[Ll]osanges?|"
            r"[Pp]arallélogrammes?|[Pp]olygones?|[Aa]ngles?|[Cc]ôtés?|[Dd]roites?|[Hh]ypoténuses?|[Ss]ommets?|"
            r"[Ll]ongueurs?|[Vv]ecteurs?|[Dd]emi-droites?|[Tt]rapèzes?|[Pp]entagones?|[Hh]exagones?)")

# caractères qui ne doivent jamais être lus tels quels
NOTATIONS = re.compile(r"[$\\^_/≤≥≠∈∉≈×÷±∞²³√∩∪]|\[[A-Z]{2,}\]")
GEO_COLLE = re.compile(rf"\b{MOTS_GEO}\s+[A-Z]{{2,5}}\b")


# ---------------------------------------------------------------- nombres (nombres=True seulement)
def _num2words(n):
    try:
        from num2words import num2words
        return num2words(int(n), lang="fr")
    except Exception:
        return str(n)


def decimal_en_mots(entier, frac):
    zeros = len(frac) - len(frac.lstrip("0"))
    reste = frac.lstrip("0")
    mots = _num2words(entier) + " virgule" + " zéro" * zeros
    return (mots + (" " + _num2words(reste) if reste else "")).strip()


def nombres_en_lettres(t):
    # milliers séparés par une espace (normale, insécable, fine) : un seul nombre
    t = re.sub(r"\b\d{1,3}(?:[ \u00a0\u202f]\d{3})+\b", lambda m: re.sub(r"\D", "", m.group(0)), t)
    t = re.sub(r"(\d)\s*%", r"\1 pour cent", t)
    t = re.sub(r"(\d+),(\d+)", lambda m: decimal_en_mots(m.group(1), m.group(2)), t)
    return re.sub(r"\b\d+\b", lambda m: _num2words(m.group(0)), t)


# ---------------------------------------------------------------- outils TeX
def _groupe(s, i):
    """s[i] == '{' : contenu du groupe équilibré et indice qui suit l'accolade fermante."""
    prof = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            prof += 1
        elif s[j] == "}":
            prof -= 1
            if prof == 0:
                return s[i + 1:j], j + 1
    return s[i + 1:], len(s)


def _commande(t, nom, nargs, f):
    """Remplace \\nom{a}{b}… (arguments équilibrés) par f(a, b, …)."""
    motif = re.compile(r"\\" + nom + r"(?![A-Za-z])\s*")
    while True:
        m = motif.search(t)
        if not m:
            return t
        i, args = m.end(), []
        for _ in range(nargs):
            while i < len(t) and t[i] == " ":
                i += 1
            if i < len(t) and t[i] == "{":
                a, i = _groupe(t, i)
            elif i < len(t):
                a, i = t[i], i + 1
            else:
                a = ""
            args.append(a)
        t = t[:m.start()] + f(*args) + t[i:]


def epeler(g):
    return SEP.join(g)


def est_compose(e):
    e = e.strip()
    if e.startswith("(") and e.endswith(")"):
        e = e[1:-1]
    return bool(re.search(r"[+\-±*/×÷]|\\(?:pm|times|div|cdot)\b|\b(?:plus|moins|fois)\b", e))


def fraction(num, den, **k):
    n, d = vers_oral(num, **k), vers_oral(den, **k)
    if est_compose(num) and est_compose(den):
        return f"{n}, le tout divisé par l'expression {d},"
    if est_compose(num):
        return f"{n}, le tout divisé par {d},"
    if est_compose(den):
        return f"{n} divisé par l'expression {d},"
    return f"{n} sur {d}"


def racine(r, **k):
    o = vers_oral(r, **k)
    return f"racine carrée de l'expression {o}," if est_compose(r) else f"racine carrée de {o}"


# ---------------------------------------------------------------- forme orale
def vers_oral(texte, nombres=False):
    """Forme orale proposée d'une phrase de script contenant des notations."""
    t = texte.replace("’", "'").replace("$", "")   # délimiteurs de formule : jamais lus
    k = {"nombres": False}

    # habillage TeX sans effet à l'oral
    for nom in ("text", "textbf", "mathbf", "mathrm", "boldsymbol", "mbox", "displaystyle"):
        t = _commande(t, nom, 1, lambda a: a)
    t = _commande(t, "cssId", 2, lambda _i, a: a)
    t = _commande(t, "textcolor", 2, lambda _c, a: a)
    t = _commande(t, "color", 1, lambda _c: "")
    t = re.sub(r"\\(?:left|right|,|;|!|quad|qquad)(?![A-Za-z])", " ", t)

    # objets géométriques
    t = _commande(t, "overrightarrow", 1, lambda a: "vecteur " + epeler(a.replace(" ", "")))
    t = _commande(t, "vec", 1, lambda a: "vecteur " + epeler(a.replace(" ", "")))
    t = _commande(t, "widehat", 1, lambda a: "angle " + epeler(a.replace(" ", "")))
    t = _commande(t, "overline", 1, lambda a: a + " barre")
    t = _commande(t, "bar", 1, lambda a: a + " barre")

    # probabilités
    t = re.sub(r"P_\{?([A-Za-z0-9]+)\}?\s*\(\s*([^()]+?)\s*\)", r"P de \2 sachant \1", t)
    t = re.sub(r"\\cap(?![A-Za-z])|∩", " inter ", t)
    t = re.sub(r"\\cup(?![A-Za-z])|∪", " union ", t)
    t = re.sub(r"\bP\s*\(\s*([^()]+?)\s*\)", r"P de \1", t)

    # fractions et racines (arguments équilibrés, traités de l'intérieur)
    for nom in ("dfrac", "tfrac", "frac"):
        t = _commande(t, nom, 2, lambda a, b: fraction(a, b, **k))
    t = _commande(t, "sqrt", 1, lambda a: racine(a, **k))
    t = re.sub(r"√\s*\(([^()]+)\)", lambda m: racine(m.group(1), **k), t)
    t = re.sub(r"√\s*(\w+)", lambda m: racine(m.group(1), **k), t)
    # fraction linéaire : (a+b)/c, (a+b)/(c+d), 3/4
    t = re.sub(r"\(([^()]+)\)\s*/\s*(\([^()]+\)|\w+)",
               lambda m: fraction(m.group(1), m.group(2).strip("()"), **k), t)
    t = re.sub(r"\b(\w+)\s*/\s*(\w+)\b", lambda m: fraction(m.group(1), m.group(2), **k), t)

    # puissances
    t = re.sub(r"\(([^()]+)\)\s*(?:\^\{?2\}?|²)", r"\1, le tout au carré,", t)
    t = re.sub(r"\(([^()]+)\)\s*(?:\^\{?3\}?|³)", r"\1, le tout au cube,", t)
    t = re.sub(r"\(([^()]+)\)\s*\^\{?([A-Za-z0-9+-]+)\}?", r"\1, le tout à la puissance \2,", t)
    t = re.sub(r"\b([A-Z]{2,5})\s*(?:\^\{?2\}?|²)", lambda m: epeler(m.group(1)) + " au carré", t)
    t = re.sub(r"\^\{?2\}?|²", " au carré", t)
    t = re.sub(r"\^\{?3\}?|³", " au cube", t)
    t = re.sub(r"\^\{([^{}]+)\}|\^(\w)", lambda m: " puissance " + (m.group(1) or m.group(2)), t)
    # indices : u_n → u n ; u_{n+1} → u indice n plus 1
    t = re.sub(r"_\{([^{}]+)\}", r" indice \1", t)
    t = re.sub(r"_(\w)", r" \1", t)

    # relations et opérateurs
    t = re.sub(r"\\(?:para|parallel)(?![A-Za-z])|//|∥", " est parallèle à ", t)
    t = re.sub(r"\\perp(?![A-Za-z])|⊥", " est perpendiculaire à ", t)
    t = re.sub(r"\\pm(?![A-Za-z])|±", " plus ou moins ", t)
    t = re.sub(r"\\(?:times|cdot)(?![A-Za-z])|×", " fois ", t)
    t = re.sub(r"\\div(?![A-Za-z])|÷", " divisé par ", t)
    t = re.sub(r"\\approx(?![A-Za-z])|≈", " environ égal à ", t)
    t = re.sub(r"\\neq?(?![A-Za-z])|≠", " différent de ", t)
    t = re.sub(r"\\leq?(?![A-Za-z])|<=|≤", " inférieur ou égal à ", t)
    t = re.sub(r"\\geq?(?![A-Za-z])|>=|≥", " supérieur ou égal à ", t)
    t = re.sub(r"\s<\s|\\lt(?![A-Za-z])", " inférieur à ", t)
    t = re.sub(r"\s>\s|\\gt(?![A-Za-z])", " supérieur à ", t)
    t = re.sub(r"\\notin(?![A-Za-z])|∉", " n'appartient pas à ", t)
    t = re.sub(r"\\in(?![A-Za-z])|∈", " appartient à ", t)
    t = re.sub(r"\\infty(?![A-Za-z])|∞", " l'infini ", t)

    # fonctions : f(x) → f de x ; produit : 3(x + 2) → 3 fois, entre parenthèses, x plus 2
    t = re.sub(r"\b([fghuvFGH])\s*\(([^()]+)\)", r"\1 de \2", t)
    t = re.sub(r"(\b\d+|\b[a-z])\s*\(([^()]*[+\-][^()]*)\)", r"\1 fois, entre parenthèses, \2,", t)

    # noms de points : [AB], (AB), triangle RIS, R-I-S
    t = re.sub(r"\[([A-Z]{2,})\]", lambda m: epeler(m.group(1)), t)
    t = re.sub(r"\(([A-Z]{2})\)", lambda m: epeler(m.group(1)), t)
    t = re.sub(rf"\b({MOTS_GEO})\s+([A-Z]{{2,5}})\b", lambda m: m.group(1) + " " + epeler(m.group(2)), t)
    t = re.sub(rf"(\b{MOTS_GEO}\s+[A-Z](?:{SEP}[A-Z])+\s+et\s+)([A-Z]{{2,5}})\b",
               lambda m: m.group(1) + epeler(m.group(2)), t)
    t = re.sub(r"\b([A-Z]{2,5})(?=\s+au\s+(?:carré|cube)\b)", lambda m: epeler(m.group(1)), t)
    t = re.sub(r"\b[A-Z](?:-[A-Z])+\b", lambda m: epeler(m.group(0).replace("-", "")), t)
    t = re.sub(r"\b(vecteur|angle)s?\s+\1\b", r"\1", t)

    # signes
    t = re.sub(r"\s*=\s*", " égale ", t)
    t = re.sub(r"\s*\+\s*", " plus ", t)
    t = re.sub(r"(?<=[\d)])\s*-\s*(?=[\w(])|(?<=\w)\s*-\s*(?=\d)|\s+-\s+", " moins ", t)
    t = re.sub(r"(?:(?<=^)|(?<=[\s(=]))-(?=\d|[a-z]\b)", "moins ", t)

    # restes de TeX : commandes inconnues, accolades
    t = re.sub(r"\\([A-Za-z]+)", r"\1", t)
    t = t.replace("{", "").replace("}", "")

    if nombres:
        t = nombres_en_lettres(t)

    # ponctuation et espaces
    t = re.sub(r",\s*(?=[,.;:!?]|$)", "", t)
    t = re.sub(r"\s+([,.])", r"\1", t)   # l'espace avant ; : ! ? (typographie française) est gardée
    t = re.sub(r";(?=\S)|,(?=[^\s\d])", lambda m: m.group(0) + " ", t)   # « 0,25 » reste un nombre
    t = re.sub(r"\s+", " ", t).strip()
    return t


def a_relire(texte):
    """Vrai si la phrase contient une notation qui ne doit pas être lue telle quelle."""
    return bool(NOTATIONS.search(texte) or GEO_COLLE.search(texte))


# ---------------------------------------------------------------- auto-test
CAS = [
    ("De plus, le triangle RIS est rectangle en I.", "De plus, le triangle R I S est rectangle en I."),
    ("Il y a plus de filles que de garçons.", "Il y a plus de filles que de garçons."),
    ("On répond au QCM puis on calcule le PGCD.", "On répond au QCM puis on calcule le PGCD."),
    ("L'IA ne remplace pas le professeur.", "L'IA ne remplace pas le professeur."),
    ("OK, ET maintenant, la droite d'équation y = 2x + 1.", "OK, ET maintenant, la droite d'équation y égale 2x plus 1."),
    ("On calcule IL au carré plus JL au carré.", "On calcule I L au carré plus J L au carré."),
    ("C'est-à-dire que x - 3 = 0, peut-être. Que vaut-il ? Où a-t-on 5-2 ?",
     "C'est-à-dire que x moins 3 égale 0, peut-être. Que vaut-il ? Où a-t-on 5 moins 2 ?"),
    ("Les vecteurs AB et CD sont-ils colinéaires ?", "Les vecteurs A B et C D sont-ils colinéaires ?"),
    ("Exemple : la règle trace le côté AB ; puis DC.", "Exemple : la règle trace le côté A B ; puis DC."),
    ("La droite (AB) est parallèle à (CD).", "La droite A B est parallèle à C D."),
    ("On a $(AB) \\para (CD)$.", "On a A B est parallèle à C D."),
    ("La probabilité P(A) vaut 0,25 et P_A(B) vaut 0,4.", "La probabilité P de A vaut 0,25 et P de B sachant A vaut 0,4."),
    ("On trouve 3 200 élèves, soit 12,5 % du total.", "On trouve 3 200 élèves, soit 12,5 % du total."),
    ("Le plus grand nombre est 21.", "Le plus grand nombre est 21."),
    ("f(x) = 2x + 3 pour tout x.", "f de x égale 2x plus 3 pour tout x."),
    ("On développe 3(x + 2) puis on réduit.", "On développe 3 fois, entre parenthèses, x plus 2, puis on réduit."),
    ("Le segment [AB] mesure 5 cm.", "Le segment A B mesure 5 cm."),
    ("Le volume en cm3 vaut 125.", "Le volume en cm3 vaut 125."),
    ("Le triangle $R-I-S$ est rectangle en $I$.", "Le triangle R I S est rectangle en I."),
    ("On calcule $\\frac{0+2}{2}$.", "On calcule 0 plus 2, le tout divisé par 2."),
    ("On a \\dfrac{1}{x+1} et \\frac{3}{4}.", "On a 1 divisé par l'expression x plus 1, et 3 sur 4."),
    ("On a \\sqrt{2+1} = 3/2.", "On a racine carrée de l'expression 2 plus 1, égale 3 sur 2."),
    ("L'expression (x+1)^2 est développée.", "L'expression x plus 1, le tout au carré, est développée."),
    ("$RS^2 = RI^2 + IS^2$", "R S au carré égale R I au carré plus I S au carré"),
    ("Le point $A$ a pour abscisse $-6$.", "Le point A a pour abscisse moins 6."),
    ("$P(\\overline{A} \\cap B)$", "P de A barre inter B"),
    ("$\\overrightarrow{AB}$ et le vecteur $\\vec{CD}$", "vecteur A B et le vecteur C D"),
    ("$x \\leq 3$ et $u_{n+1}$", "x inférieur ou égal à 3 et u indice n plus 1"),
]
CAS_NOMBRES = [
    ("On trouve 3 200 élèves, soit 12,5 % du total.",
     "On trouve trois mille deux cents élèves, soit douze virgule cinq pour cent du total."),
    ("Il en reste 0,05.", "Il en reste zéro virgule zéro cinq."),
]


def auto_test():
    ok = True
    try:
        import num2words  # noqa: F401  (nombres=True seulement)
        series = ((False, CAS), (True, CAS_NOMBRES))
    except ImportError:
        print("num2words absent : cas nombres=True sautés (les nombres restent en chiffres).")
        series = ((False, CAS),)
    for nombres, cas in series:
        for ecrit, attendu in cas:
            obtenu = vers_oral(ecrit, nombres=nombres)
            if obtenu != attendu:
                ok = False
                print(f"ÉCHEC : {ecrit}\n  obtenu  : {obtenu}\n  attendu : {attendu}")
    print("auto-test réussi" if ok else "auto-test en échec")
    return ok


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:] == ["--test"]:
        sys.exit(0 if auto_test() else 1)
    for a in sys.argv[1:]:
        print(vers_oral(a))
