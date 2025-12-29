"""
Utilitaires pour gérer l'encodage Windows et affichage console
"""

import sys
import io

def setup_console_encoding():
    """Configure l'encodage UTF-8 pour la console Windows"""
    if sys.platform == 'win32':
        # Forcer UTF-8 pour stdout et stderr
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def safe_print(text):
    """Affiche du texte en gérant les emojis sur Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Remplacer les emojis par des alternatives textuelles
        replacements = {
            '📚': '[LIVRES]',
            '📖': '[LIVRE]',
            '🔢': '[NOMBRES]',
            '🏷️': '[TAGS]',
            '🔗': '[LIEN]',
            '💾': '[DISQUE]',
            '📄': '[PDF]',
            '📝': '[DOC]',
            '✅': '[OK]',
            '❌': '[ERREUR]',
            '⚠️': '[ATTENTION]',
            '🔍': '[RECHERCHE]',
            '🌐': '[WEB]',
            '📦': '[PACKAGE]'
        }
        for emoji, replacement in replacements.items():
            text = text.replace(emoji, replacement)
        print(text)
