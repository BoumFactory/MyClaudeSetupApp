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
ENCODAGES_COURANTS = [
    'utf-8',
    'utf-8-sig',  # UTF-8 avec BOM
    'latin-1',
    'iso-8859-1',
    'cp1252',  # Windows Western European
    'cp850',   # DOS Western European
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
    """Essaie de lire le fichier avec différents encodages"""
    # D'abord, lecture en mode binaire pour analyse
    try:
        with open(file_path, 'rb') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"[ERREUR] Impossible de lire le fichier en mode binaire: {e}")
        return None, None, None

    # Essayer de décoder avec différents encodages
    for encoding in ENCODAGES_COURANTS:
        try:
            content = raw_content.decode(encoding)

            # Vérifier que le contenu est cohérent
            # Moins de 1% de caractères de remplacement invalides
            if content.count('�') < len(content) * 0.01:
                return content, encoding, raw_content
        except (UnicodeDecodeError, UnicodeError):
            continue

    return None, None, None

def clean_problematic_characters(content):
    """Nettoie les caractères problématiques pour LaTeX et HTML"""
    cleaned = content
    changes = []

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

    # Détecter les caractères invalides ou de remplacement
    if '�' in cleaned:
        count = cleaned.count('�')
        changes.append(f"  - ATTENTION: {count}x caractère de remplacement � détecté")

    # Vérifier qu'il n'y a pas de caractères de contrôle (sauf \n, \r, \t)
    control_chars = []
    for i, char in enumerate(cleaned):
        if unicodedata.category(char).startswith('C') and char not in '\n\r\t':
            control_chars.append((i, char, ord(char)))

    if control_chars:
        changes.append(f"  - ATTENTION: {len(control_chars)} caractères de contrôle détectés")
        for i, char, code in control_chars[:5]:  # Montrer les 5 premiers
            changes.append(f"    Position {i}: U+{code:04X}")

    return cleaned, changes

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

def fix_encoding_simple(input_file, output_file=None):
    """Corrige l'encodage d'un fichier en préservant sa syntaxe (.tex, .md, .py, .html, .js, .json)"""
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"[ERREUR] Fichier introuvable: {input_file}")
        return False

    print(f"[INFO] Analyse de: {input_path.name}")

    # Tentative de lecture
    content, detected_encoding, raw_content = try_read_file(input_path)

    if content is None:
        print("[ERREUR] Impossible de detecter l'encodage")
        return False

    print(f"[OK] Encodage detecte: {detected_encoding}")

    # Nettoyer les caractères problématiques (TOUJOURS, même si déjà UTF-8)
    print("[INFO] Nettoyage des caracteres problematiques...")
    cleaned_content, changes = clean_problematic_characters(content)

    if changes:
        print("[INFO] Modifications effectuees:")
        for change in changes:
            print(change)
    else:
        print("[INFO] Aucun caractere problematique detecte")

    # Si le fichier est déjà UTF-8 et qu'aucun nettoyage n'a été fait, ne rien faire
    if detected_encoding.startswith('utf-8') and not changes:
        print("[INFO] Le fichier est deja en UTF-8 propre, aucune correction necessaire")
        return True

    # Utiliser le contenu nettoyé
    content = cleaned_content

    # Déterminer le fichier de sortie
    if output_file is None:
        # Créer backup et écraser l'original
        backup_path = input_path.with_suffix(input_path.suffix + '.backup')
        if backup_path.exists():
            print(f"[WARN] Backup existe deja: {backup_path.name}")
        else:
            try:
                # Copier le fichier original en backup
                with open(backup_path, 'wb') as f_out:
                    f_out.write(raw_content)
                print(f"[INFO] Backup cree: {backup_path.name}")
            except Exception as e:
                print(f"[WARN] Impossible de creer le backup: {e}")
        output_path = input_path
    else:
        output_path = Path(output_file)

    # Écriture en UTF-8 (mode binaire pour contrôle total)
    try:
        # Encoder le contenu en UTF-8
        utf8_content = content.encode('utf-8')

        # Écrire en mode binaire pour éviter toute interprétation
        with open(output_path, 'wb') as f:
            f.write(utf8_content)

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
    if len(sys.argv) < 2:
        print("="*50)
        print("   Correction automatique d'encodage")
        print("   (Preserve la syntaxe du fichier)")
        print("   + Nettoyage caracteres problematiques")
        print("="*50)
        print("\nTypes de fichiers supportes:")
        print("  .tex, .md, .py, .html, .js, .json")
        print("\nUsage:")
        print("  python fix_encoding_simple.py <fichier>")
        print("  python fix_encoding_simple.py <source> <sortie>")
        print("\nExemples:")
        print("  python fix_encoding_simple.py cours.tex")
        print("  python fix_encoding_simple.py README.md")
        print("  python fix_encoding_simple.py script.py")
        print("  python fix_encoding_simple.py config.json")
        print("\nLe script:")
        print("  - Detecte et corrige l'encodage vers UTF-8")
        print("  - Nettoie les caracteres problematiques (espaces insecables, apostrophes, etc.)")
        print("  - Preserve la syntaxe selon le type de fichier")
        print("  - Valide la structure JSON pour les fichiers .json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    print("="*50)
    success = fix_encoding_simple(input_file, output_file)
    print("="*50)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
