#!/usr/bin/env python3
"""
Extrait le contenu d'un fichier ODT vers un dossier.
Usage: python unpack.py <fichier.odt> <dossier_sortie>
"""
import zipfile
import os
import sys

def unpack_odt(odt_path: str, output_dir: str) -> None:
    """Extrait le contenu d'un fichier ODT vers un dossier."""
    if not os.path.exists(odt_path):
        print(f"Erreur: {odt_path} n'existe pas")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(odt_path, 'r') as z:
        z.extractall(output_dir)

    print(f"Extrait {odt_path} vers {output_dir}")
    print(f"Fichiers principaux:")
    for f in ['content.xml', 'styles.xml', 'meta.xml']:
        path = os.path.join(output_dir, f)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  - {f}: {size} octets")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python unpack.py <fichier.odt> <dossier_sortie>")
        sys.exit(1)

    unpack_odt(sys.argv[1], sys.argv[2])
