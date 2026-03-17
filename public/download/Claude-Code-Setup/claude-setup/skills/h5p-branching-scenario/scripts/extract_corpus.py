#!/usr/bin/env python3
"""
Extracteur de corpus PDF pour H5P.

Scinde des fichiers PDF en pages individuelles et extrait le texte.
Génère un index JSON avec métadonnées.

Usage:
  python extract_corpus.py --input corpus/ --output generated/reference/
"""
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any

try:
    import PyPDF2
except ImportError:
    print("ERREUR: PyPDF2 requis. Installez avec: pip install PyPDF2")
    sys.exit(1)


# ============================================================================
# EXTRACTION DES PAGES
# ============================================================================

def extract_pages_from_pdf(pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
    """Extrait les pages d'un PDF et retourne les métadonnées."""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            nb_pages = len(reader.pages)

        pages_info = []
        for page_num in range(nb_pages):
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                page = reader.pages[page_num]

                # Extraire le texte
                text = page.extract_text() or ""
                text_preview = text[:200].replace('\n', ' ')

                # Détecter les images (heuristique simple)
                has_images = '/Image' in page['/Resources'].keys() if '/Resources' in page else False

                # Sauvegarder la page PDF
                writer = PyPDF2.PdfWriter()
                writer.add_page(page)
                page_filename = f"page_{page_num+1:02d}.pdf"
                page_path = output_dir / page_filename
                with open(page_path, 'wb') as out_f:
                    writer.write(out_f)

                # Sauvegarder le texte
                txt_filename = f"page_{page_num+1:02d}.txt"
                txt_path = output_dir / txt_filename
                with open(txt_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(text)

                pages_info.append({
                    'page_num': page_num + 1,
                    'text_preview': text_preview,
                    'has_images': has_images,
                    'text_length': len(text)
                })

        return {
            'filename': pdf_path.name,
            'nb_pages': nb_pages,
            'pages': pages_info
        }

    except Exception as e:
        print(f"ERREUR lors du traitement {pdf_path}: {e}")
        return None


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Extrait les pages de fichiers PDF et génère un index JSON'
    )
    parser.add_argument('--input', '-i', required=True, help='Répertoire contenant les PDF')
    parser.add_argument('--output', '-o', required=True, help='Répertoire de sortie')

    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"ERREUR: répertoire introuvable : {args.input}")
        return 1

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Trouver tous les PDF
    pdf_files = list(input_dir.glob('*.pdf')) + list(input_dir.glob('**/*.pdf'))
    if not pdf_files:
        print(f"ERREUR: aucun fichier PDF trouvé dans {args.input}")
        return 1

    print(f"Traitement de {len(pdf_files)} fichier(s) PDF...")
    index = []
    total_pages = 0
    processed = 0

    for pdf_path in pdf_files:
        # Créer un sous-répertoire pour chaque PDF
        pdf_stem = pdf_path.stem
        pdf_output_dir = output_dir / pdf_stem
        pdf_output_dir.mkdir(parents=True, exist_ok=True)

        print(f"  Extraction : {pdf_path.name}...", end=" ")
        metadata = extract_pages_from_pdf(pdf_path, pdf_output_dir)

        if metadata:
            metadata['output_dir'] = str(pdf_output_dir.relative_to(output_dir))
            index.append(metadata)
            total_pages += metadata['nb_pages']
            processed += 1
            print(f"OK ({metadata['nb_pages']} pages)")
        else:
            print("ERREUR")

    # Sauvegarder l'index
    index_path = output_dir / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print()
    print(f"OK Extraction complète")
    print(f"  Fichiers traités : {processed}/{len(pdf_files)}")
    print(f"  Pages extraites  : {total_pages}")
    print(f"  Sortie           : {output_dir}")
    print(f"  Index            : {index_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
