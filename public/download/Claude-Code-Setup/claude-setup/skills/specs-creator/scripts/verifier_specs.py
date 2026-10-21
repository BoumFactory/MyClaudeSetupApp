"""Vérifie la cohérence mécanique d'un dossier de specs produit par specs-creator.

Usage :
    python verifier_specs.py <dossier-specs>

Contrôles :
- un index (CLAUDE.md, sinon README.md) existe ;
- chaque fichier .md cité par l'index existe, et chaque .md du dossier est cité ;
- les décisions D-xx sont uniques, ont un statut, et toute décision citée existe ;
- les critères CA-xx cités existent dans le fichier des critères ;
- aucun marqueur de trou (TODO, TBD, à définir, ???, gabarit <…> resté tel quel)
  ne traîne hors du journal des décisions.

Code de sortie : 0 si tout va bien, 1 s'il reste des erreurs.
"""

import re
import sys
from pathlib import Path

RE_LIEN = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)|`([^`\s]+\.md)`")
RE_DECISION_TITRE = re.compile(r"^#{2,3}\s+(D-\d+)\b", re.MULTILINE)
RE_DECISION_CITEE = re.compile(r"\bD-\d+\b")
RE_CRITERE_DEF = re.compile(r"^\|\s*(CA-\d+)\s*\|", re.MULTILINE)
RE_CRITERE_DEF_TITRE = re.compile(r"^#{2,4}\s+(CA-\d+)\b", re.MULTILINE)
RE_CRITERE_CITE = re.compile(r"\bCA-\d+\b")
RE_TROU = re.compile(
    # « à compléter » est exclu : c'est le vocabulaire normal d'une fiche à trous.
    r"\bTODO\b|\bTBD\b|\bFIXME\b|à définir|à préciser|\?\?\?",
    re.IGNORECASE,
)
# Phrase de gabarit restée telle quelle : <Majuscule suivie de mots…>
RE_GABARIT = re.compile(r"<[A-ZÀ-Ý][a-zà-ÿ]+[ ,'][^<>\n]{3,}>")
RE_STATUT = re.compile(r"\*\*Statut\*\*\s*:\s*(.+)", re.IGNORECASE)


def sans_blocs_code(texte):
    """Retire les blocs ``` ``` pour ne pas signaler les exemples."""
    return re.sub(r"```.*?```", "", texte, flags=re.DOTALL)


def lire(chemin):
    return chemin.read_text(encoding="utf-8")


def numero_ligne(texte, position):
    return texte.count("\n", 0, position) + 1


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    dossier = Path(sys.argv[1])
    if not dossier.is_dir():
        print(f"ERREUR : dossier introuvable : {dossier}")
        return 1

    erreurs = []
    alertes = []

    fichiers = sorted(p for p in dossier.glob("*.md"))
    noms = {p.name for p in fichiers}

    # 1. Index
    index = None
    for candidat in ("CLAUDE.md", "README.md"):
        if candidat in noms:
            index = dossier / candidat
            break
    if index is None:
        erreurs.append("Aucun index : ni CLAUDE.md ni README.md à la racine du dossier.")
    else:
        texte_index = lire(index)
        cites = set()
        for m in RE_LIEN.finditer(texte_index):
            cible = m.group(1) or m.group(2)
            cites.add(cible)
            if not (dossier / cible).exists():
                erreurs.append(f"{index.name} cite « {cible} », qui n'existe pas.")
        cites_noms = {Path(c).name for c in cites}
        for p in fichiers:
            if p == index or p.name in ("CLAUDE.md", "README.md"):
                continue
            if p.name not in cites_noms:
                erreurs.append(f"{p.name} n'est pas cité par {index.name}.")

    # 2. Décisions
    fichier_decisions = next((p for p in fichiers if "decision" in p.name.lower()), None)
    decisions = set()
    statuts = {"tranché": 0, "par défaut": 0, "ouvert": 0, "autre": 0}
    if fichier_decisions is None:
        erreurs.append("Aucun journal des décisions (fichier *decisions*.md).")
    else:
        texte_dec = lire(fichier_decisions)
        titres = list(RE_DECISION_TITRE.finditer(texte_dec))
        if not titres:
            alertes.append(f"{fichier_decisions.name} ne contient aucune décision « ## D-xx ».")
        for i, m in enumerate(titres):
            ident = m.group(1)
            if ident in decisions:
                erreurs.append(f"Décision {ident} définie deux fois.")
            decisions.add(ident)
            fin = titres[i + 1].start() if i + 1 < len(titres) else len(texte_dec)
            bloc = texte_dec[m.end():fin]
            s = RE_STATUT.search(bloc)
            if not s:
                erreurs.append(f"Décision {ident} sans ligne « **Statut** : … ».")
                continue
            valeur = s.group(1).lower()
            if valeur.startswith("tranch"):
                statuts["tranché"] += 1
            elif "défaut" in valeur or "defaut" in valeur:
                statuts["par défaut"] += 1
            elif valeur.startswith("ouvert"):
                statuts["ouvert"] += 1
                if len(valeur.split()) < 3:
                    alertes.append(f"Décision {ident} ouverte sans raison donnée.")
            else:
                statuts["autre"] += 1
                alertes.append(f"Décision {ident} : statut inconnu « {s.group(1).strip()} ».")

    # 3. Critères
    fichier_criteres = next((p for p in fichiers if "critere" in p.name.lower()), None)
    criteres = set()
    if fichier_criteres is None:
        alertes.append("Aucun fichier de critères d'acceptation (*criteres*.md).")
    else:
        texte_ca = lire(fichier_criteres)
        criteres = set(RE_CRITERE_DEF.findall(texte_ca)) | set(RE_CRITERE_DEF_TITRE.findall(texte_ca))

    # 4. Références croisées et trous, fichier par fichier
    for p in fichiers:
        texte = sans_blocs_code(lire(p))
        for ident in sorted(set(RE_DECISION_CITEE.findall(texte))):
            if decisions and ident not in decisions:
                erreurs.append(f"{p.name} cite {ident}, absente du journal.")
        if criteres:
            for ident in sorted(set(RE_CRITERE_CITE.findall(texte))):
                if ident not in criteres:
                    erreurs.append(f"{p.name} cite {ident}, absent des critères.")
        if p == fichier_decisions:
            continue
        for m in RE_TROU.finditer(texte):
            erreurs.append(f"{p.name}, ligne ~{numero_ligne(texte, m.start())} : trou « {m.group(0)} » hors du journal.")
        for m in RE_GABARIT.finditer(texte):
            alertes.append(f"{p.name}, ligne ~{numero_ligne(texte, m.start())} : phrase de gabarit ? « {m.group(0)[:60]} »")

    # Bilan
    print(f"Dossier : {dossier}")
    print(f"Fichiers : {len(fichiers)} · décisions : {len(decisions)} "
          f"(tranchées {statuts['tranché']}, par défaut {statuts['par défaut']}, "
          f"ouvertes {statuts['ouvert']}) · critères : {len(criteres)}")
    if statuts["tranché"] and statuts["tranché"] > 20:
        alertes.append("Plus de 20 décisions tranchées par l'utilisateur : certaines étaient-elles secondaires ?")
    if decisions and statuts["tranché"] < 3:
        alertes.append("Moins de 3 décisions tranchées par l'utilisateur : un choix structurant a-t-il été pris par défaut ?")
    for a in alertes:
        print(f"ALERTE : {a}")
    for e in erreurs:
        print(f"ERREUR : {e}")
    if not erreurs:
        print("OK : aucune erreur." + (" (voir les alertes)" if alertes else ""))
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
