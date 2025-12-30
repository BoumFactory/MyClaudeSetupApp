#!/usr/bin/env python3
"""
Cree un fichier ODT a partir d'un dossier extrait.
Usage: python pack.py <dossier_source> <fichier.odt>

IMPORTANT: Le fichier mimetype doit etre non compresse et en premier dans l'archive.
"""
import zipfile
import os
import sys

def pack_odt(input_dir: str, odt_path: str) -> None:
    """Cree un fichier ODT a partir d'un dossier."""
    if not os.path.isdir(input_dir):
        print(f"Erreur: {input_dir} n'est pas un dossier")
        sys.exit(1)

    with zipfile.ZipFile(odt_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # Le mimetype DOIT etre non compresse et en premier
        mimetype_path = os.path.join(input_dir, 'mimetype')
        if os.path.exists(mimetype_path):
            z.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
        else:
            # Creer le mimetype si absent
            z.writestr('mimetype', 'application/vnd.oasis.opendocument.text',
                      compress_type=zipfile.ZIP_STORED)

        # Ajouter tous les autres fichiers
        for root, dirs, files in os.walk(input_dir):
            # Exclure les dossiers caches
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file == 'mimetype':
                    continue
                if file.startswith('.'):
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, input_dir)
                z.write(file_path, arcname)

    size = os.path.getsize(odt_path)
    print(f"Cree {odt_path} ({size} octets)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pack.py <dossier_source> <fichier.odt>")
        sys.exit(1)

    pack_odt(sys.argv[1], sys.argv[2])
