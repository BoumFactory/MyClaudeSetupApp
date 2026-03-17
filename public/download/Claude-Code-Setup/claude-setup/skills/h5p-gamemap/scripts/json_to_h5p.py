#!/usr/bin/env python3
"""
Convertit un préplan JSON en fichier H5P Game Map.

Usage:
  python json_to_h5p.py --input preplan.json --output parcours.h5p [--background carte.png]
  python json_to_h5p.py --input preplan.json --validate

Le JSON doit suivre le schéma défini dans prompt.md.
"""
import json
import re
import sys
import argparse
from pathlib import Path

# Import du générateur existant (même dossier)
try:
    from generate_gamemap import generate_h5p
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from generate_gamemap import generate_h5p

VALID_TYPES = {'multichoice', 'truefalse', 'dragtext', 'blanks', 'singlechoiceset', 'questionset'}
VALID_STYLES = {'aventure', 'revision', 'evaluation', 'decouverte'}


def validate_preplan_json(data):
    """Valide un préplan JSON. Retourne (erreurs, avertissements)."""
    errors = []
    warnings = []

    if not isinstance(data, dict):
        errors.append("Le JSON doit être un objet (pas une liste)")
        return errors, warnings

    # Champs requis
    if not data.get('title'):
        errors.append("Champ 'title' requis")

    etapes = data.get('etapes', [])
    if not etapes:
        errors.append("Au moins une étape requise dans 'etapes'")
        return errors, warnings

    # Style
    style = data.get('style', 'aventure')
    if style not in VALID_STYLES:
        warnings.append(f"Style '{style}' inconnu, défaut 'aventure' appliqué")

    # Config
    config = data.get('config', {})
    lives = config.get('lives')
    if lives is not None and not isinstance(lives, int):
        warnings.append(f"config.lives devrait être un entier ou null, reçu: {type(lives).__name__}")

    # Validation par étape
    prev_type = None
    type_counts = {}

    for i, etape in enumerate(etapes):
        tag = f"Étape {i+1} ({etape.get('title', 'sans titre')})"

        # Type
        etype = etape.get('type', 'multichoice')
        if etype not in VALID_TYPES:
            errors.append(f"{tag}: type '{etype}' invalide. Valides: {', '.join(sorted(VALID_TYPES))}")
            continue

        type_counts[etype] = type_counts.get(etype, 0) + 1

        # Types consécutifs
        if etype == prev_type:
            warnings.append(f"{tag}: même type que l'étape précédente ('{etype}')")
        prev_type = etype

        # Position
        x = etape.get('x', 50)
        y = etape.get('y', 50)
        if not (0 <= x <= 100 and 0 <= y <= 100):
            errors.append(f"{tag}: position hors limites (x={x}, y={y}), doit être 0-100")

        # Contenu
        content = etape.get('content', {})
        if not content:
            errors.append(f"{tag}: 'content' vide")
            continue

        # Validation spécifique au type
        if etype == 'multichoice':
            _validate_multichoice(tag, content, errors)
        elif etype == 'truefalse':
            _validate_truefalse(tag, content, errors)
        elif etype in ('dragtext', 'blanks'):
            _validate_text_interactive(tag, etype, content, errors, warnings)
        elif etype == 'singlechoiceset':
            _validate_singlechoiceset(tag, content, errors, warnings)
        elif etype == 'questionset':
            _validate_questionset(tag, content, errors, warnings)

    # Checks globaux
    total = len(etapes)
    mc = type_counts.get('multichoice', 0)
    if total >= 4 and mc / total > 0.5:
        warnings.append(f"Trop de multichoice simples ({mc}/{total}), diversifier")
    if total >= 4 and len(type_counts) < 2:
        warnings.append("Un seul type utilisé — diversifier")

    # Vérifier qu'il y a un start
    has_start = any(e.get('isStart', False) for e in etapes)
    if not has_start:
        warnings.append("Aucune étape marquée isStart=true, la première sera utilisée")

    return errors, warnings


def _validate_multichoice(tag, content, errors):
    if not content.get('question'):
        errors.append(f"{tag}: 'question' manquante")
    answers = content.get('answers', [])
    if len(answers) < 2:
        errors.append(f"{tag}: minimum 2 réponses pour multichoice")
    if answers and not any(a.get('correct') for a in answers):
        errors.append(f"{tag}: aucune réponse marquée correct=true")
    for j, a in enumerate(answers):
        if not a.get('feedback'):
            pass  # feedback optionnel mais recommandé


def _validate_truefalse(tag, content, errors):
    if not content.get('question'):
        errors.append(f"{tag}: 'question' manquante")
    if 'correct' not in content:
        errors.append(f"{tag}: champ 'correct' (true/false) requis")


def _validate_text_interactive(tag, etype, content, errors, warnings):
    text = content.get('text', '')
    if not text:
        errors.append(f"{tag}: 'text' manquant")
        return

    # Détecter les trous
    trous = re.findall(r'\*([^*]+)\*', text)
    if not trous:
        warnings.append(f"{tag}: aucun trou (*mot*) détecté dans le texte")

    # LaTeX interdit dans les trous
    for trou in trous:
        if '\\(' in trou or '\\)' in trou or '$' in trou or '\\frac' in trou or '\\mathbb' in trou:
            errors.append(f"{tag}: LaTeX interdit dans les trous — trouvé '*{trou}*'")

    # DragText : dernière ligne sans trou
    if etype == 'dragtext' and trous:
        lines = [l for l in text.strip().split('\n') if l.strip()]
        if lines:
            last_line = lines[-1]
            if '*' in last_line:
                warnings.append(f"{tag}: dragtext — dernière ligne contient un trou (bug H5P connu)")


def _validate_singlechoiceset(tag, content, errors, warnings):
    questions = content.get('questions', [])
    if len(questions) < 2:
        warnings.append(f"{tag}: singlechoiceset devrait avoir 2+ questions")
    for j, q in enumerate(questions):
        qtag = f"{tag} Q{j+1}"
        if not q.get('question'):
            errors.append(f"{qtag}: question manquante")
        answers = q.get('answers', [])
        if len(answers) < 2:
            errors.append(f"{qtag}: minimum 2 réponses")
        if answers and not any(a.get('correct') for a in answers):
            errors.append(f"{qtag}: aucune bonne réponse")


def _validate_questionset(tag, content, errors, warnings):
    questions = content.get('questions', [])
    if len(questions) < 2:
        warnings.append(f"{tag}: questionset devrait avoir 2+ questions")
    for j, q in enumerate(questions):
        qtag = f"{tag} Q{j+1}"
        qtype = q.get('type', 'multichoice')
        if qtype not in ('multichoice', 'truefalse'):
            errors.append(f"{qtag}: type '{qtype}' non supporté dans questionset (multichoice ou truefalse)")
        if qtype == 'multichoice':
            answers = q.get('answers', [])
            if answers and not any(a.get('correct') for a in answers):
                errors.append(f"{qtag}: aucune bonne réponse")
        elif qtype == 'truefalse':
            if 'correct' not in q:
                errors.append(f"{qtag}: champ 'correct' requis")


def main():
    parser = argparse.ArgumentParser(
        description='Convertit un préplan JSON en fichier H5P Game Map',
        epilog='Le JSON doit suivre le schéma défini dans prompt.md.'
    )
    parser.add_argument('--input', '-i', required=True, help='Fichier JSON du préplan')
    parser.add_argument('--output', '-o', help='Fichier H5P de sortie (défaut: auto)')
    parser.add_argument('--background', '-b', help='Image de fond PNG (1920x1080 recommandé)')
    parser.add_argument('--validate', action='store_true', help='Valider uniquement sans générer')

    args = parser.parse_args()

    # Charger le JSON
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERREUR: fichier introuvable : {args.input}")
        return 1

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERREUR: JSON invalide ligne {e.lineno}: {e.msg}")
        return 1

    # Valider
    errors, warnings = validate_preplan_json(data)

    if warnings:
        print("Avertissements:")
        for w in warnings:
            print(f"  ! {w}")
        print()

    if errors:
        print("Erreurs bloquantes:")
        for e in errors:
            print(f"  X {e}")
        return 1

    nb_etapes = len(data.get('etapes', []))
    types_used = set(e.get('type', '?') for e in data.get('etapes', []))
    print(f"OK JSON valide — {nb_etapes} étapes, types: {', '.join(sorted(types_used))}")

    if args.validate:
        return 0

    # Générer le H5P
    if not args.output:
        slug = re.sub(r'[^a-z0-9]+', '_', data.get('theme', 'parcours').lower()).strip('_')
        args.output = str(input_path.parent / f"parcours_{slug}.h5p")

    generate_h5p(data, args.output, args.background)

    print(f"OK H5P généré : {args.output}")
    print()
    print(f"  Titre   : {data.get('title', '?')}")
    print(f"  Style   : {data.get('style', 'aventure')}")
    print(f"  Étapes  : {nb_etapes}")
    print()
    for i, e in enumerate(data.get('etapes', [])):
        marker = ">" if e.get('isStart') else " "
        print(f"  {marker} {i+1}. {e.get('title', '?')} [{e.get('type', '?')}]")
    print()
    print("Import Moodle : Cours > Mode édition > Ajouter H5P > Téléverser le .h5p")

    return 0


if __name__ == '__main__':
    sys.exit(main())
