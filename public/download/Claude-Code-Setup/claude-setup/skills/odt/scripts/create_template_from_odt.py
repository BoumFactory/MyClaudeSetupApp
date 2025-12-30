#!/usr/bin/env python3
"""
Cree un template ODT avec tous les styles d'un fichier source Sesamath.

Ce script copie les styles complets d'un ODT source vers un nouveau document vierge,
preservant ainsi tous les styles educatifs Sesamath.

Usage:
    python create_template_from_odt.py <source.odt> <output_template.odt>
"""

import os
import sys
import zipfile
import shutil
import tempfile

from odf.opendocument import OpenDocumentText
from odf.text import P, H


def create_template_with_styles(source_odt: str, output_path: str):
    """
    Copie tous les styles d'un ODT source vers un nouveau document vide.

    Args:
        source_odt: Chemin vers le fichier ODT source contenant les styles
        output_path: Chemin de sortie pour le template

    Cette methode preserve TOUS les styles en copiant directement styles.xml
    """
    temp_dir = tempfile.mkdtemp(prefix="odt_template_")

    try:
        # 1. Dezipper la source
        print(f"[1/4] Extraction de la source: {source_odt}")
        source_temp = os.path.join(temp_dir, "source")
        os.makedirs(source_temp)
        with zipfile.ZipFile(source_odt, 'r') as z:
            z.extractall(source_temp)

        # Verifier que styles.xml existe
        styles_xml_path = os.path.join(source_temp, "styles.xml")
        if not os.path.exists(styles_xml_path):
            raise FileNotFoundError("styles.xml non trouve dans le fichier source")

        styles_size = os.path.getsize(styles_xml_path)
        print(f"    styles.xml trouve: {styles_size:,} octets")

        # 2. Creer un document vide avec odfpy
        print("[2/4] Creation du document de base...")
        doc = OpenDocumentText()

        # Ajouter du contenu informatif
        h = H(outlinelevel=1, text="Template Sesamath - Styles Educatifs")
        doc.text.addElement(h)

        p = P(text="Ce document contient tous les styles educatifs Sesamath extraits des cahiers officiels.")
        doc.text.addElement(p)

        p = P(text="")
        doc.text.addElement(p)

        p = P(text="Pour utiliser ces styles dans LibreOffice Writer:")
        doc.text.addElement(p)

        p = P(text="1. Ouvrez le panneau Styles (F11)")
        doc.text.addElement(p)

        p = P(text="2. Les styles commencant par '_' sont les styles Sesamath")
        doc.text.addElement(p)

        p = P(text="3. Exemples: _Paragraphe_Definition, _Paragraphe_Propriete, etc.")
        doc.text.addElement(p)

        # Sauvegarder temporairement
        temp_odt = os.path.join(temp_dir, "base.odt")
        doc.save(temp_odt)
        print(f"    Document de base cree")

        # 3. Dezipper le document de base
        print("[3/4] Injection des styles...")
        new_temp = os.path.join(temp_dir, "new")
        os.makedirs(new_temp)
        with zipfile.ZipFile(temp_odt, 'r') as z:
            z.extractall(new_temp)

        # Remplacer styles.xml par celui de la source
        shutil.copy(styles_xml_path, os.path.join(new_temp, "styles.xml"))
        print(f"    styles.xml injecte")

        # 4. Rezipper correctement
        print("[4/4] Creation du template final...")

        # S'assurer que le dossier de sortie existe
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Creer l'archive ODT
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            # mimetype DOIT etre le premier fichier et non compresse
            mimetype_path = os.path.join(new_temp, "mimetype")
            if os.path.exists(mimetype_path):
                zout.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)

            # Ajouter tous les autres fichiers
            for root, dirs, files in os.walk(new_temp):
                for file in files:
                    if file == "mimetype":
                        continue  # Deja ajoute
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, new_temp)
                    zout.write(file_path, arcname)

        output_size = os.path.getsize(output_path)
        print(f"\n[OK] Template cree avec succes!")
        print(f"     Fichier: {output_path}")
        print(f"     Taille: {output_size:,} octets")

        return True

    except Exception as e:
        print(f"[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Nettoyer
        shutil.rmtree(temp_dir)


def main():
    if len(sys.argv) < 3:
        print("Usage: python create_template_from_odt.py <source.odt> <output.odt>")
        print()
        print("Exemple:")
        print("  python create_template_from_odt.py cahier_sesamath.odt template_sesamath.odt")
        sys.exit(1)

    source = sys.argv[1]
    output = sys.argv[2]

    if not os.path.exists(source):
        print(f"[ERREUR] Source non trouvee: {source}")
        sys.exit(1)

    if not source.lower().endswith('.odt'):
        print(f"[ERREUR] Le fichier source doit etre un .odt")
        sys.exit(1)

    success = create_template_with_styles(source, output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
