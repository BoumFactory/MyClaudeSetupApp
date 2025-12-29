#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test exhaustif pour la détection d'encodage
Crée des fichiers de test avec différents encodages et vérifie la détection
"""

import os
import sys
import tempfile
import shutil

# Textes de test avec caractères français typiques
TEST_TEXTS = {
    "simple": "Bonjour, ceci est un test d'encodage.",
    "accents": "Les élèves étudient les mathématiques à l'école.",
    "mixed": "Problème : résoudre l'équation avec précision et créativité.",
    "special": "« Voici des guillemets français », œuvre d'art, c'est ça !",
    "complex": """Introduction

Les intelligences artificielles (IA) comme ChatGPT, Claude ou Gemini sont aujourd'hui capables de résoudre de nombreux problèmes complexes. Cependant, elles ont aussi des limites surprenantes et peuvent commettre des erreurs sur des questions simples.

Objectif de cette activité : Apprendre à développer votre esprit critique face aux réponses d'une IA."""
}

ENCODINGS_TO_TEST = [
    'utf-8',
    'cp1252',      # Windows-1252
    'latin-1',     # ISO-8859-1
    'utf-16',
]

def create_test_file(content, encoding, temp_dir):
    """Crée un fichier de test avec l'encodage spécifié"""
    filename = os.path.join(temp_dir, f"test_{encoding.replace('-', '_')}.tex")
    try:
        with open(filename, 'w', encoding=encoding) as f:
            f.write(content)
        return filename
    except Exception as e:
        print(f"[!] Erreur creation fichier {encoding}: {e}")
        return None

def detect_encoding_simple(file_path):
    """
    Version simplifiée de détection d'encodage
    Essaie plusieurs encodages et retourne le premier qui fonctionne
    """
    encodings = ['utf-8', 'cp1252', 'latin-1', 'utf-16']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            # Vérifie que le contenu n'a pas de caractères de remplacement
            if '\ufffd' not in content:  # \ufffd = caractère de remplacement Unicode
                return encoding, content
        except (UnicodeDecodeError, UnicodeError):
            continue

    return None, None

def test_encoding_detection():
    """Teste la détection d'encodage sur différents cas"""
    print("=" * 70)
    print("TEST DE DETECTION D'ENCODAGE")
    print("=" * 70)
    print()

    temp_dir = tempfile.mkdtemp()
    results = []

    try:
        for test_name, test_text in TEST_TEXTS.items():
            print(f"\n[Test: {test_name.upper()}]")
            print("-" * 70)

            for encoding in ENCODINGS_TO_TEST:
                # Créer le fichier de test
                test_file = create_test_file(test_text, encoding, temp_dir)
                if not test_file:
                    continue

                # Tester la détection
                detected_encoding, content = detect_encoding_simple(test_file)

                # Vérifier le résultat
                success = detected_encoding is not None
                match = detected_encoding == encoding if success else False

                # Afficher le résultat
                status = "[OK]" if success else "[FAIL]"
                match_status = "[EXACT]" if match else "[DIFF]" if success else ""

                print(f"{status} {match_status:8} Source: {encoding:12} | Detecte: {detected_encoding or 'ECHEC':12}")

                results.append({
                    'test': test_name,
                    'encoding': encoding,
                    'detected': detected_encoding,
                    'success': success,
                    'match': match
                })

                # Nettoyer
                os.remove(test_file)

        # Statistiques finales
        print("\n" + "=" * 70)
        print("STATISTIQUES")
        print("=" * 70)

        total = len(results)
        successes = sum(1 for r in results if r['success'])
        matches = sum(1 for r in results if r['match'])

        print(f"Total de tests: {total}")
        print(f"Détections réussies: {successes}/{total} ({100*successes/total:.1f}%)")
        print(f"Encodages correctement identifiés: {matches}/{total} ({100*matches/total:.1f}%)")
        print()

        # Afficher les échecs
        failures = [r for r in results if not r['success']]
        if failures:
            print("[!] ECHECS:")
            for fail in failures:
                print(f"   - {fail['test']} avec {fail['encoding']}")
        else:
            print("[OK] Tous les tests ont reussi!")

        # Afficher les détections incorrectes mais qui ont fonctionné
        mismatches = [r for r in results if r['success'] and not r['match']]
        if mismatches:
            print("\n[!] DETECTIONS DIFFERENTES (mais fonctionnelles):")
            for mm in mismatches:
                print(f"   - {mm['test']}: {mm['encoding']} detecte comme {mm['detected']}")

        print("\n" + "=" * 70)

    finally:
        # Nettoyer le répertoire temporaire
        shutil.rmtree(temp_dir)

def test_conversion():
    """Teste la conversion d'encodage"""
    print("\n" + "=" * 70)
    print("TEST DE CONVERSION D'ENCODAGE")
    print("=" * 70)
    print()

    temp_dir = tempfile.mkdtemp()

    try:
        # Créer un fichier en cp1252
        test_text = TEST_TEXTS['complex']
        test_file = create_test_file(test_text, 'cp1252', temp_dir)

        if not test_file:
            print("[!] Impossible de creer le fichier de test")
            return

        print(f"[+] Fichier cree: {os.path.basename(test_file)}")

        # Détecter l'encodage
        detected, content = detect_encoding_simple(test_file)
        print(f"[?] Encodage detecte: {detected}")

        # Convertir en UTF-8
        if detected and detected != 'utf-8':
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Conversion {detected} -> utf-8 reussie")

            # Vérifier la conversion
            new_detected, new_content = detect_encoding_simple(test_file)
            print(f"[?] Nouvel encodage: {new_detected}")

            if new_detected == 'utf-8' and new_content == content:
                print("[OK] Conversion validee: contenu identique")
            else:
                print("[!] Probleme de conversion: contenu different")
        else:
            print(f"[i] Fichier deja en UTF-8, pas de conversion necessaire")

        print()

    finally:
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    print()
    test_encoding_detection()
    test_conversion()
    print()
