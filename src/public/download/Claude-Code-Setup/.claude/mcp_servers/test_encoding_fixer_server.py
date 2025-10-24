#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour le serveur MCP encoding-fixer.
Teste les fonctionnalités de détection et correction d'encodage.
"""

import sys
import json
import codecs
from pathlib import Path

# Ajouter le répertoire parent au path pour l'import
sys.path.insert(0, str(Path(__file__).parent))

try:
    import encoding_fixer_server
    print("✅ Import du module encoding_fixer_server réussi")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)


def test_get_encoding_stats():
    """Test de la fonction get_encoding_stats()"""
    print("\n" + "="*60)
    print("TEST 1: get_encoding_stats()")
    print("="*60)

    result_json = encoding_fixer_server.get_encoding_stats()
    result = json.loads(result_json)

    print("Résultat:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    assert "supported_encodings" in result
    assert "default_output" in result
    print("✅ Test get_encoding_stats() réussi")


def test_detect_file_encoding():
    """Test de la fonction detect_file_encoding()"""
    print("\n" + "="*60)
    print("TEST 2: detect_file_encoding()")
    print("="*60)

    # Utiliser le fichier de test minimal
    test_file = Path(__file__).parent / "test_encoding_minimal.tex"

    if not test_file.exists():
        print(f"⚠️  Fichier de test non trouvé: {test_file}")
        print("   Créez d'abord le fichier test_encoding_minimal.tex")
        return

    result_json = encoding_fixer_server.detect_file_encoding(str(test_file))
    result = json.loads(result_json)

    print("Résultat:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    assert result["success"] == True
    assert "detected_encoding" in result
    print(f"✅ Test detect_file_encoding() réussi - Encodage détecté: {result['detected_encoding']}")


def test_fix_file_encoding():
    """Test de la fonction fix_file_encoding()"""
    print("\n" + "="*60)
    print("TEST 3: fix_file_encoding()")
    print("="*60)

    # Utiliser le fichier de test minimal
    test_file = Path(__file__).parent / "test_encoding_minimal.tex"
    output_file = Path(__file__).parent / "test_encoding_minimal_utf8.tex"

    if not test_file.exists():
        print(f"⚠️  Fichier de test non trouvé: {test_file}")
        return

    # Nettoyer le fichier de sortie s'il existe déjà
    if output_file.exists():
        output_file.unlink()
        print(f"Fichier de sortie existant supprimé: {output_file.name}")

    result_json = encoding_fixer_server.fix_file_encoding(
        str(test_file),
        str(output_file),
        create_backup=False
    )
    result = json.loads(result_json)

    print("Résultat:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    assert result["success"] == True
    assert output_file.exists()

    # Vérifier que le fichier de sortie est bien en UTF-8
    with codecs.open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert len(content) > 0
        assert 'élève' in content or 'é' in content

    print("✅ Test fix_file_encoding() réussi")

    # Nettoyage
    if output_file.exists():
        output_file.unlink()
        print(f"Fichier de sortie nettoyé: {output_file.name}")


def test_fix_file_encoding_with_backup():
    """Test de fix_file_encoding() avec backup"""
    print("\n" + "="*60)
    print("TEST 4: fix_file_encoding() avec backup")
    print("="*60)

    # Créer une copie temporaire du fichier de test
    test_file = Path(__file__).parent / "test_encoding_minimal.tex"
    temp_file = Path(__file__).parent / "test_encoding_temp.tex"

    if not test_file.exists():
        print(f"⚠️  Fichier de test non trouvé: {test_file}")
        return

    # Copier le fichier de test
    with codecs.open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    with codecs.open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)

    result_json = encoding_fixer_server.fix_file_encoding(
        str(temp_file),
        output_path="",  # Écrase l'original
        create_backup=True
    )
    result = json.loads(result_json)

    print("Résultat:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    assert result["success"] == True

    # Vérifier que le backup a été créé
    backup_file = temp_file.with_suffix(temp_file.suffix + '.backup')
    assert backup_file.exists(), "Le backup n'a pas été créé"

    print("✅ Test fix_file_encoding() avec backup réussi")

    # Nettoyage
    if temp_file.exists():
        temp_file.unlink()
    if backup_file.exists():
        backup_file.unlink()
    print("Fichiers temporaires nettoyés")


def test_invalid_file():
    """Test avec un fichier inexistant"""
    print("\n" + "="*60)
    print("TEST 5: Fichier inexistant")
    print("="*60)

    result_json = encoding_fixer_server.detect_file_encoding("fichier_inexistant.tex")
    result = json.loads(result_json)

    print("Résultat:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    assert result["success"] == False
    assert "error" in result
    print("✅ Test fichier inexistant réussi (erreur gérée correctement)")


def main():
    """Fonction principale de test"""
    print("="*60)
    print("TESTS DU SERVEUR ENCODING-FIXER MCP")
    print("="*60)

    try:
        test_get_encoding_stats()
        test_detect_file_encoding()
        test_fix_file_encoding()
        test_fix_file_encoding_with_backup()
        test_invalid_file()

        print("\n" + "="*60)
        print("✅ TOUS LES TESTS SONT RÉUSSIS!")
        print("="*60)

    except AssertionError as e:
        print(f"\n❌ Test échoué: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
