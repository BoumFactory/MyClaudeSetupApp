#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple de correction d'encodage (sans dépendances)
Version améliorée pour préserver la syntaxe et nettoyer les caractères problématiques
Supporte: .tex, .md, .py, .html, .js, .json
Usage: python fix_encoding_simple.py <fichier> [sortie]
"""

import sys
import codecs
import re
import unicodedata
import json
from pathlib import Path

# Encodages courants à essayer (par ordre de probabilité)
# UTF-8 EN PREMIER pour détecter les fichiers déjà corrects !
ENCODAGES_COURANTS = [
    'utf-8',   # TOUJOURS tester UTF-8 d'abord
    'cp850',   # DOS Western European
    'cp1252',  # Windows Western European
    'latin-1',
    'iso-8859-1',
]

# Patterns de vérification par type de fichier
LATEX_COMMANDS_CHECK = [
    r'\\tableofcontents',
    r'\\input\{',
    r'\\include\{',
    r'\\documentclass',
    r'\\usepackage',
    r'\\begin\{',
    r'\\end\{',
    r'\\section',
    r'\\subsection',
    r'\\textbf',
    r'\\textit',
    r'\\item',
    r'\\num\{',  # siunitx - commençant par \n
]

MARKDOWN_PATTERNS_CHECK = [
    r'^#{1,6}\s',  # Headers
    r'\[.*?\]\(.*?\)',  # Liens
    r'!\[.*?\]\(.*?\)',  # Images
    r'```',  # Code blocks
    r'\*\*.*?\*\*',  # Bold
    r'\*.*?\*',  # Italic
]

PYTHON_PATTERNS_CHECK = [
    r'^import\s',
    r'^from\s.*?\simport\s',
    r'^def\s',
    r'^class\s',
    r'^if\s',
    r'^for\s',
    r'^while\s',
]

HTML_PATTERNS_CHECK = [
    r'<html[^>]*>',
    r'<head[^>]*>',
    r'<body[^>]*>',
    r'<div[^>]*>',
    r'<p[^>]*>',
    r'<script[^>]*>',
    r'<style[^>]*>',
]

JAVASCRIPT_PATTERNS_CHECK = [
    r'\bfunction\s',
    r'\bconst\s',
    r'\blet\s',
    r'\bvar\s',
    r'\bif\s*\(',
    r'\bfor\s*\(',
    r'\bclass\s',
]

def try_read_file(file_path):
    """Essaie de lire le fichier avec différents encodages (optimisé)"""
    # Lecture en mode binaire
    try:
        with open(file_path, 'rb') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"[ERREUR] Impossible de lire le fichier en mode binaire: {e}")
        return None, None, None

    # Pour l'analyse, utiliser un échantillon (premiers 8KB ou tout si plus petit)
    # Cela évite de traiter tout le fichier pour la détection
    sample_size = min(len(raw_content), 8192)
    raw_sample = raw_content[:sample_size]

    # Essayer de décoder avec différents encodages
    # On garde tous les candidats valides pour choisir le meilleur
    candidates = []

    for encoding in ENCODAGES_COURANTS:
        try:
            # Décodage de l'échantillon seulement
            sample_content = raw_sample.decode(encoding)

            # Vérifier que le contenu est cohérent
            # Moins de 1% de caractères de remplacement invalides
            if sample_content.count('�') < len(sample_content) * 0.01:
                # Calculer un score de confiance basé sur :
                # 1. Nombre de caractères accentués français valides
                # 2. Absence de séquences suspectes
                french_accents = sum(1 for c in sample_content if c in 'éèêëàâäôöùûüçîïÉÈÊËÀÂÄÔÖÙÛÜÇÎÏœ')

                # Patterns suspects de double encodage UTF-8->CP1252
                # é devient Ã©, è devient Ã¨, etc.
                suspicious_patterns = (
                    sample_content.count('Ã©') + sample_content.count('Ã¨') +
                    sample_content.count('Ãª') + sample_content.count('Ã ') +
                    sample_content.count('Ã§') + sample_content.count('Ã´') +
                    sample_content.count('Ã»') + sample_content.count('Ã®') +
                    sample_content.count('Ã¯') + sample_content.count('Ã‰') +
                    sample_content.count('Ã€')
                )

                # Pénaliser les séquences "Ã" (pattern typique double encodage)
                suspicious_a_tilde = sample_content.count('Ã')

                # Score: favoriser encodages avec plus d'accents français et moins de patterns suspects
                score = french_accents - (suspicious_patterns * 100) - (suspicious_a_tilde * 5)

                candidates.append((encoding, score))
        except (UnicodeDecodeError, UnicodeError):
            continue

    if not candidates:
        return None, None, None

    # Trier les candidats par score décroissant
    candidates.sort(key=lambda x: x[1], reverse=True)

    # PRIORITÉ ABSOLUE À UTF-8 : Si UTF-8 décode sans erreur, l'utiliser TOUJOURS
    utf8_candidate = next((enc for enc, score in candidates if enc.lower().startswith('utf')), None)
    if utf8_candidate:
        best_encoding = utf8_candidate
        best_score = max(score for enc, score in candidates if enc == utf8_candidate)
        print(f"[INFO] UTF-8 detecte et selectionne (priorite)")
    else:
        # Prendre le meilleur candidat
        best_encoding, best_score = candidates[0]

    # Maintenant décoder TOUT le fichier avec le meilleur encodage
    try:
        best_content = raw_content.decode(best_encoding)
        return best_content, best_encoding, raw_content
    except (UnicodeDecodeError, UnicodeError) as e:
        print(f"[ERREUR] Echec decodage complet avec {best_encoding}: {e}")
        return None, None, None

def load_latex_character_mapping():
    """Charge la table de mapping des caractères LaTeX depuis le fichier JSON"""
    script_dir = Path(__file__).parent
    mapping_file = script_dir / 'latex_character_mapping.json'

    # Valeurs par défaut si le fichier n'existe pas
    default_mapping = {
        'forbidden_unicode_symbols': {},
        'math_symbol_replacements': {},
        'ligature_replacements': {
            'œ': r'\oe ',
            'Œ': r'\OE ',
        }
    }

    if not mapping_file.exists():
        print(f"[WARN] Fichier de mapping introuvable: {mapping_file}")
        return default_mapping

    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        return mapping
    except Exception as e:
        print(f"[WARN] Erreur lecture mapping: {e}")
        return default_mapping

def clean_latex_specific_characters(content):
    """Nettoie les caractères spécifiques problématiques pour LaTeX"""
    cleaned = content
    changes = []

    # Charger la table de mapping depuis le fichier JSON
    mapping = load_latex_character_mapping()

    forbidden_unicode_symbols = mapping.get('forbidden_unicode_symbols', {})
    math_symbols = mapping.get('math_symbol_replacements', {})
    latex_replacements = mapping.get('ligature_replacements', {})
    typography_fixes = mapping.get('typography_fixes', {})

    # Appliquer tous les remplacements : symboles interdits + symboles math + ligatures + typographie
    all_replacements = {**forbidden_unicode_symbols, **math_symbols, **latex_replacements, **typography_fixes}

    for symbol, replacement in all_replacements.items():
        if symbol in cleaned:
            count = cleaned.count(symbol)
            cleaned = cleaned.replace(symbol, replacement)
            if replacement:
                changes.append(f"  - [LATEX] {count}x '{symbol}' -> '{replacement}'")
            else:
                changes.append(f"  - [LATEX] {count}x '{symbol}' SUPPRIMÉ (symbole Unicode interdit)")

    return cleaned, changes

def clean_problematic_characters(content):
    """Nettoie les caractères problématiques pour LaTeX et HTML

    Returns:
        tuple: (cleaned_content, changes_list, warnings_list)
    """
    cleaned = content
    changes = []
    warnings = []

    # Normaliser en forme NFC (composition canonique)
    cleaned = unicodedata.normalize('NFC', cleaned)

    # Détecter et remplacer les caractères problématiques courants
    problematic_chars = {
        '\u00a0': ' ',  # Espace insécable -> espace normal (LaTeX utilise ~)
        '\u2019': "'",  # Apostrophe typographique -> apostrophe simple
        '\u2018': "'",  # Guillemet simple gauche -> apostrophe simple
        '\u201c': '"',  # Guillemet double gauche -> guillemet double
        '\u201d': '"',  # Guillemet double droit -> guillemet double
        '\u2013': '--', # Tiret demi-cadratin -> double tiret LaTeX
        '\u2014': '---',# Tiret cadratin -> triple tiret LaTeX
        '\u2026': '...',# Points de suspension -> trois points
        '\ufeff': '',   # BOM -> supprimer
        '\u200b': '',   # Zero-width space -> supprimer
        '\u200c': '',   # Zero-width non-joiner -> supprimer
        '\u200d': '',   # Zero-width joiner -> supprimer
    }

    for old_char, new_char in problematic_chars.items():
        if old_char in cleaned:
            count = cleaned.count(old_char)
            cleaned = cleaned.replace(old_char, new_char)
            if new_char:
                changes.append(f"  - {count}x U+{ord(old_char):04X} -> '{new_char}'")
            else:
                changes.append(f"  - {count}x U+{ord(old_char):04X} supprimé")

    # Détecter les caractères invalides ou de remplacement (WARNING, pas un changement)
    if '�' in cleaned:
        count = cleaned.count('�')
        warnings.append(f"  - ATTENTION: {count}x caractère de remplacement U+FFFD détecté")
        warnings.append(f"    -> Le fichier est déjà corrompu, impossible de restaurer automatiquement")

    # Vérifier qu'il n'y a pas de caractères de contrôle (sauf \n, \r, \t)
    control_chars = []
    for i, char in enumerate(cleaned):
        if unicodedata.category(char).startswith('C') and char not in '\n\r\t':
            control_chars.append((i, char, ord(char)))

    if control_chars:
        warnings.append(f"  - ATTENTION: {len(control_chars)} caractères de contrôle détectés")
        for i, char, code in control_chars[:5]:  # Montrer les 5 premiers
            warnings.append(f"    Position {i}: U+{code:04X}")

    return cleaned, changes, warnings

def get_patterns_for_file(file_path):
    """Détermine les patterns de vérification selon l'extension du fichier"""
    ext = Path(file_path).suffix.lower()

    patterns_map = {
        '.tex': LATEX_COMMANDS_CHECK,
        '.md': MARKDOWN_PATTERNS_CHECK,
        '.py': PYTHON_PATTERNS_CHECK,
        '.html': HTML_PATTERNS_CHECK,
        '.js': JAVASCRIPT_PATTERNS_CHECK,
        '.json': [],  # JSON sera vérifié différemment
    }

    return patterns_map.get(ext, []), ext

def verify_syntax_preservation(original_content, new_content, file_path):
    """Vérifie que la syntaxe du fichier est préservée selon son type"""
    patterns, ext = get_patterns_for_file(file_path)
    issues = []

    # Vérification spéciale pour JSON
    if ext == '.json':
        try:
            json.loads(original_content)
            json.loads(new_content)
        except json.JSONDecodeError as e:
            issues.append(f"JSON invalide après conversion: {e}")
        return issues

    # Vérification par patterns pour les autres types
    flags = re.MULTILINE if ext in ['.md', '.py'] else 0

    for pattern in patterns:
        original_matches = len(re.findall(pattern, original_content, flags))
        new_matches = len(re.findall(pattern, new_content, flags))

        if original_matches != new_matches:
            issues.append(f"Pattern {pattern} : {original_matches} -> {new_matches}")

    return issues

def fix_encoding_simple(input_file, output_file=None, dry_run=False, create_backup=True):
    """Corrige l'encodage d'un fichier en préservant sa syntaxe (.tex, .md, .py, .html, .js, .json)

    Args:
        input_file: Fichier à traiter
        output_file: Fichier de sortie (None = écraser l'original)
        dry_run: Si True, simule sans modifier les fichiers
        create_backup: Si True, crée un backup avant modification
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"[ERREUR] Fichier introuvable: {input_file}")
        return False

    print(f"[INFO] Analyse de: {input_path.name}")
    if dry_run:
        print("[INFO] Mode DRY-RUN: aucun fichier ne sera modifie")

    # Tentative de lecture
    content, detected_encoding, raw_content = try_read_file(input_path)

    if content is None:
        print("[ERREUR] Impossible de detecter l'encodage")
        return False

    print(f"[OK] Encodage detecte: {detected_encoding}")

    # Nettoyer les caractères problématiques (TOUJOURS, même si déjà UTF-8)
    print("[INFO] Nettoyage des caracteres problematiques...")
    cleaned_content, changes, warnings = clean_problematic_characters(content)

    # Nettoyage spécifique LaTeX pour les fichiers .tex
    latex_changes = []
    if input_path.suffix.lower() == '.tex':
        print("[INFO] Nettoyage specifique LaTeX...")
        cleaned_content, latex_changes = clean_latex_specific_characters(cleaned_content)

    # Combiner tous les changements
    all_changes = changes + latex_changes

    # Afficher les changements effectués
    if all_changes:
        print("[INFO] Modifications a effectuer:")
        for change in all_changes:
            try:
                print(change)
            except UnicodeEncodeError:
                safe_change = change.encode('ascii', 'backslashreplace').decode('ascii')
                print(safe_change)
    else:
        print("[INFO] Aucune modification necessaire")

    # Afficher les warnings séparément
    if warnings:
        print("[WARN] Problemes detectes (non corrigeables automatiquement):")
        for warning in warnings:
            try:
                print(warning)
            except UnicodeEncodeError:
                safe_warning = warning.encode('ascii', 'backslashreplace').decode('ascii')
                print(safe_warning)

    # Si le fichier est déjà UTF-8 et qu'aucun nettoyage n'a été fait, ne rien faire
    if detected_encoding.startswith('utf-8') and not all_changes:
        print("[INFO] Le fichier est deja en UTF-8 propre, aucune correction necessaire")
        if warnings:
            print("[INFO] Des warnings ont ete detectes mais aucune modification n'est possible")
        return True

    # Utiliser le contenu nettoyé
    content = cleaned_content

    # Si mode dry-run, s'arrêter ici
    if dry_run:
        print("[INFO] Mode DRY-RUN: simulation terminee, aucun fichier modifie")
        return True

    # Déterminer le fichier de sortie
    if output_file is None:
        output_path = input_path
    else:
        output_path = Path(output_file)

    # Créer un backup si demandé et qu'on écrase l'original
    if create_backup and output_path == input_path:
        backup_path = input_path.with_suffix(input_path.suffix + '.backup')
        try:
            import shutil
            shutil.copy2(input_path, backup_path)
            print(f"[INFO] Backup cree: {backup_path.name}")
        except Exception as e:
            print(f"[WARN] Impossible de creer le backup: {e}")
            print("[WARN] Continuer sans backup ? (Ctrl+C pour annuler)")
            import time
            time.sleep(2)

    # Écriture en UTF-8 (mode binaire pour contrôle total)
    try:
        # Encoder le contenu en UTF-8
        utf8_content = content.encode('utf-8')

        # Écrire en mode binaire pour éviter toute interprétation
        with open(output_path, 'wb') as f:
            f.write(utf8_content)

        # Message adapté selon le cas
        if detected_encoding.lower().startswith('utf'):
            if all_changes:
                print(f"[OK] Fichier nettoye: {output_path.name}")
                print(f"     Encodage UTF-8 preserve, {len(all_changes)} modifications appliquees")
            else:
                print(f"[OK] Fichier verifie: {output_path.name}")
                print(f"     Deja en UTF-8, aucune modification necessaire")
        else:
            print(f"[OK] Fichier converti: {output_path.name}")
            print(f"     {detected_encoding} -> UTF-8")

        # Vérification complète
        with open(output_path, 'rb') as f:
            test_raw = f.read()

        test_content = test_raw.decode('utf-8')
        print(f"[OK] Verification UTF-8: OK ({len(test_content)} caracteres)")

        # Vérifier que la syntaxe du fichier est préservée
        issues = verify_syntax_preservation(content, test_content, input_path)

        if issues:
            print("[WARN] Problemes detectes dans la syntaxe:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            file_type = input_path.suffix.upper()
            print(f"[OK] Syntaxe {file_type} preservee")

        # Vérification finale : le contenu doit être identique
        if content != test_content:
            print("[ERREUR] Le contenu a ete modifie lors de la conversion!")
            print(f"  Longueur originale: {len(content)}")
            print(f"  Longueur finale: {len(test_content)}")

            # Afficher les différences
            diff_count = 0
            for i, (c1, c2) in enumerate(zip(content, test_content)):
                if c1 != c2:
                    diff_count += 1
                    if diff_count <= 5:  # Afficher les 5 premières différences
                        print(f"  Position {i}: '{c1}' (U+{ord(c1):04X}) -> '{c2}' (U+{ord(c2):04X})")

            if diff_count > 5:
                print(f"  ... et {diff_count - 5} autres differences")

            return False

        print("[OK] Contenu identique apres conversion")
        return True

    except Exception as e:
        print(f"[ERREUR] Erreur ecriture: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Correction automatique d\'encodage pour fichiers texte',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemples:
  python fix_encoding_simple.py cours.tex
  python fix_encoding_simple.py --dry-run cours.tex
  python fix_encoding_simple.py --no-backup script.py
  python fix_encoding_simple.py cours.tex cours_fixed.tex

Types de fichiers supportés:
  .tex, .md, .py, .html, .js, .json

Le script:
  - Detecte et corrige l'encodage vers UTF-8
  - Nettoie les caracteres problematiques (espaces insecables, apostrophes, etc.)
  - Preserve la syntaxe selon le type de fichier
  - Cree un backup automatique avant modification (sauf --no-backup)
        '''
    )

    parser.add_argument('input_file', help='Fichier a traiter')
    parser.add_argument('output_file', nargs='?', default=None,
                        help='Fichier de sortie (par defaut: ecrase l\'original)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Simule sans modifier les fichiers')
    parser.add_argument('--no-backup', action='store_true',
                        help='Ne pas creer de backup avant modification')

    args = parser.parse_args()

    print("="*50)
    success = fix_encoding_simple(
        args.input_file,
        args.output_file,
        dry_run=args.dry_run,
        create_backup=not args.no_backup
    )
    print("="*50)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
