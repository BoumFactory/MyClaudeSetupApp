#!/usr/bin/env python3
"""
Serveur MCP pour l'analyse de fichiers PDF (version FastMCP).

Ce serveur permet d'extraire :
- Texte complet et par page
- Images intégrées
- Métadonnées du document
- Structure du document
- Tableaux
- Recherche de texte

Author: Assistant Claude
Date: 2025
"""

import json
import logging
import os
import sys
import base64
import io
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime

# Configuration du logging pour écrire dans stderr seulement
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("pdf-analyzer-server")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    logger.error("Erreur: Le package 'mcp' n'est pas installé. Installez-le avec: pip install mcp")
    sys.exit(1)

# Créer l'instance du serveur MCP
mcp = FastMCP("pdf-analyzer-server")

# Bibliothèques PDF
try:
    import PyPDF2
    import fitz  # PyMuPDF pour extraction d'images
    import pdfplumber  # Pour extraction de tableaux
    from PIL import Image
except ImportError as e:
    logger.error(f"Erreur lors de l'import des dépendances PDF: {e}")
    logger.error("Installez les dépendances avec: pip install PyPDF2 pymupdf pdfplumber pillow")
    sys.exit(1)

# Configuration du workspace depuis mcp.json
def get_workspace_path() -> Path:
    """Charge le workspace path depuis mcp.json."""
    config_path = Path(__file__).parent / "mcp.json"
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                workspace_str = config.get('pdf_analyzer_server', {}).get('workspace_path', '')
                if workspace_str:
                    return Path(workspace_str)
    except Exception as e:
        logger.warning(f"Erreur lors du chargement de mcp.json: {e}")
    
    # Fallback vers chemin relatif
    return Path(__file__).parent.parent

WORKSPACE_PATH = get_workspace_path()
TEMP_DIR = Path(os.environ.get('TEMP', '/tmp')) / 'pdf_analyzer'
TEMP_DIR.mkdir(exist_ok=True)

def parse_page_range(page_range: str, total_pages: int) -> List[int]:
    """Parse une chaîne de pages (ex: "1-5,7,10-15") en liste de numéros."""
    if not page_range:
        return list(range(1, total_pages + 1))
    
    pages = []
    for part in page_range.split(','):
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    
    # Filtrer les pages invalides
    return [p for p in pages if 1 <= p <= total_pages]

def extract_text_pypdf2(pdf_path: Path, page_numbers: Optional[List[int]] = None) -> Dict[int, str]:
    """Extrait le texte d'un PDF avec PyPDF2."""
    text_by_page = {}
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            if page_numbers is None:
                page_numbers = list(range(1, total_pages + 1))
            
            for page_num in page_numbers:
                if 1 <= page_num <= total_pages:
                    page = pdf_reader.pages[page_num - 1]
                    text_by_page[page_num] = page.extract_text()
                    
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction du texte: {e}")
        
    return text_by_page

def extract_images_pymupdf(pdf_path: Path, output_format: str = "base64", 
                          image_format: str = "png", min_width: int = 50, 
                          min_height: int = 50) -> List[Dict[str, Any]]:
    """Extrait les images d'un PDF avec PyMuPDF."""
    images = []
    
    try:
        pdf_document = fitz.open(str(pdf_path))
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(pdf_document, xref)
                
                if pix.width >= min_width and pix.height >= min_height:
                    if pix.n < 5:  # GRAY or RGB
                        img_data = pix.tobytes(image_format)
                    else:  # CMYK
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                        img_data = pix.tobytes(image_format)
                    
                    if output_format == "base64":
                        img_base64 = base64.b64encode(img_data).decode('utf-8')
                        image_info = {
                            "page": page_num + 1,
                            "index": img_index,
                            "width": pix.width,
                            "height": pix.height,
                            "format": image_format,
                            "data": f"data:image/{image_format};base64,{img_base64}"
                        }
                    else:  # path
                        img_path = TEMP_DIR / f"page_{page_num + 1}_img_{img_index}.{image_format}"
                        with open(img_path, 'wb') as f:
                            f.write(img_data)
                        image_info = {
                            "page": page_num + 1,
                            "index": img_index,
                            "width": pix.width,
                            "height": pix.height,
                            "format": image_format,
                            "path": str(img_path)
                        }
                    
                    images.append(image_info)
                
                pix = None
        
        pdf_document.close()
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des images: {e}")
    
    return images

def extract_tables_pdfplumber(pdf_path: Path, page_numbers: Optional[List[int]] = None,
                            output_format: str = "json") -> List[Dict[str, Any]]:
    """Extrait les tableaux d'un PDF avec pdfplumber."""
    tables = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if page_numbers is None:
                page_numbers = list(range(1, len(pdf.pages) + 1))
            
            for page_num in page_numbers:
                if 1 <= page_num <= len(pdf.pages):
                    page = pdf.pages[page_num - 1]
                    page_tables = page.extract_tables()
                    
                    for table_index, table in enumerate(page_tables):
                        if table:  # Vérifier que le tableau n'est pas vide
                            if output_format == "json":
                                table_data = {
                                    "page": page_num,
                                    "index": table_index,
                                    "rows": len(table),
                                    "columns": len(table[0]) if table else 0,
                                    "data": table
                                }
                            else:  # csv
                                import csv
                                csv_buffer = io.StringIO()
                                writer = csv.writer(csv_buffer)
                                writer.writerows(table)
                                table_data = {
                                    "page": page_num,
                                    "index": table_index,
                                    "rows": len(table),
                                    "columns": len(table[0]) if table else 0,
                                    "csv": csv_buffer.getvalue()
                                }
                            
                            tables.append(table_data)
    
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des tableaux: {e}")
    
    return tables

def get_pdf_metadata_pypdf2(pdf_path: Path) -> Dict[str, Any]:
    """Récupère les métadonnées d'un PDF."""
    metadata = {}
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Informations de base
            metadata['pages'] = len(pdf_reader.pages)
            metadata['is_encrypted'] = pdf_reader.is_encrypted
            
            # Métadonnées du document
            if pdf_reader.metadata:
                doc_info = {}
                for key, value in pdf_reader.metadata.items():
                    # Nettoyer les clés (enlever le /)
                    clean_key = key[1:] if key.startswith('/') else key
                    doc_info[clean_key] = str(value) if value else None
                metadata['document_info'] = doc_info
            
            # Taille du fichier
            file_size = os.path.getsize(pdf_path)
            metadata['file_size'] = file_size
            metadata['file_size_mb'] = round(file_size / (1024 * 1024), 2)
            
            # Dates du fichier
            stat = os.stat(pdf_path)
            metadata['creation_date'] = datetime.fromtimestamp(stat.st_ctime).isoformat()
            metadata['modification_date'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des métadonnées: {e}")
        metadata['error'] = str(e)
    
    return metadata

def search_text_in_pdf(pdf_path: Path, search_text: str, 
                      case_sensitive: bool = False, 
                      whole_words: bool = False) -> List[Dict[str, Any]]:
    """Recherche du texte dans un PDF."""
    results = []
    search_lower = search_text if case_sensitive else search_text.lower()
    
    try:
        # Extraire tout le texte
        text_by_page = extract_text_pypdf2(pdf_path)
        
        for page_num, page_text in text_by_page.items():
            if not page_text:
                continue
                
            # Préparer le texte pour la recherche
            search_in = page_text if case_sensitive else page_text.lower()
            
            # Recherche basique
            if whole_words:
                import re
                pattern = r'\b' + re.escape(search_lower) + r'\b'
                matches = list(re.finditer(pattern, search_in))
            else:
                # Recherche simple
                pos = 0
                matches = []
                while True:
                    pos = search_in.find(search_lower, pos)
                    if pos == -1:
                        break
                    matches.append(type('Match', (), {'start': lambda: pos, 'end': lambda: pos + len(search_lower)})())
                    pos += 1
            
            # Pour chaque match trouvé
            for match in matches:
                # Extraire le contexte (50 caractères avant et après)
                start = max(0, match.start() - 50)
                end = min(len(page_text), match.end() + 50)
                context = page_text[start:end]
                
                # Nettoyer le contexte
                context = context.replace('\n', ' ').strip()
                
                results.append({
                    "page": page_num,
                    "position": match.start(),
                    "context": f"...{context}...",
                    "match": page_text[match.start():match.end()]
                })
    
    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {e}")
    
    return results

# Définition des outils FastMCP

@mcp.tool()
def analyze_pdf(
    pdf_path: str,
    extract_images: bool = True,
    extract_text: bool = True,
    extract_metadata: bool = True,
    extract_structure: bool = True,
    page_range: str = ""
) -> str:
    """
    Analyse complète d'un fichier PDF.
    
    Args:
        pdf_path: Chemin du fichier PDF à analyser
        extract_images: Extraire les images (défaut: true)
        extract_text: Extraire le texte (défaut: true)
        extract_metadata: Extraire les métadonnées (défaut: true)
        extract_structure: Extraire la structure (défaut: true)
        page_range: Pages à analyser (ex: "1-5,7,10-15") (défaut: toutes)
    
    Returns:
        JSON avec analyse complète du PDF
    """
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.is_absolute():
            pdf_file = WORKSPACE_PATH / pdf_file
        
        if not pdf_file.exists():
            return json.dumps({"error": f"Fichier non trouvé: {pdf_file}"})
        
        result = {
            "file": str(pdf_file),
            "analysis_date": datetime.now().isoformat()
        }
        
        # Métadonnées
        if extract_metadata:
            result["metadata"] = get_pdf_metadata_pypdf2(pdf_file)
            total_pages = result["metadata"].get("pages", 0)
        else:
            # Obtenir le nombre de pages même sans métadonnées complètes
            with open(pdf_file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                total_pages = len(reader.pages)
        
        # Parser la plage de pages
        pages_to_analyze = parse_page_range(page_range, total_pages)
        result["analyzed_pages"] = pages_to_analyze
        
        # Extraction du texte
        if extract_text:
            text_data = extract_text_pypdf2(pdf_file, pages_to_analyze)
            result["text"] = {
                "pages": text_data,
                "total_extracted": len(text_data)
            }
        
        # Extraction des images
        if extract_images:
            images = extract_images_pymupdf(pdf_file)
            # Filtrer par pages analysées
            if page_range:
                images = [img for img in images if img["page"] in pages_to_analyze]
            result["images"] = {
                "count": len(images),
                "images": images[:10]  # Limiter à 10 images pour éviter des réponses trop grandes
            }
        
        # Structure (table des matières simplifiée basée sur le texte)
        if extract_structure:
            structure = []
            if extract_text and "text" in result:
                for page_num, text in result["text"]["pages"].items():
                    # Recherche simple de titres (lignes courtes en majuscules)
                    lines = text.split('\n')
                    for line in lines[:10]:  # Vérifier les 10 premières lignes
                        line = line.strip()
                        if line and len(line) < 100 and line.isupper():
                            structure.append({
                                "page": page_num,
                                "title": line,
                                "level": 1
                            })
            result["structure"] = structure
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def extract_pdf_text(
    pdf_path: str,
    page_numbers: Optional[List[int]] = None,
    preserve_layout: bool = False
) -> str:
    """
    Extrait uniquement le texte d'un PDF.
    
    Args:
        pdf_path: Chemin du fichier PDF
        page_numbers: Liste des numéros de pages (défaut: toutes)
        preserve_layout: Préserver la mise en page (défaut: false)
    
    Returns:
        JSON avec le texte extrait par page
    """
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.is_absolute():
            pdf_file = WORKSPACE_PATH / pdf_file
        
        if not pdf_file.exists():
            return json.dumps({"error": f"Fichier non trouvé: {pdf_file}"})
        
        text_data = extract_text_pypdf2(pdf_file, page_numbers)
        
        result = {
            "file": str(pdf_file),
            "pages_extracted": len(text_data),
            "text_by_page": text_data
        }
        
        # Si preserve_layout, essayer avec pdfplumber qui préserve mieux la mise en page
        if preserve_layout:
            try:
                import pdfplumber
                with pdfplumber.open(pdf_file) as pdf:
                    for page_num in (page_numbers or range(1, len(pdf.pages) + 1)):
                        if 1 <= page_num <= len(pdf.pages):
                            page = pdf.pages[page_num - 1]
                            result["text_by_page"][page_num] = page.extract_text()
            except:
                pass  # Garder le résultat PyPDF2 si pdfplumber échoue
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction du texte: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def extract_pdf_images(
    pdf_path: str,
    output_format: str = "base64",
    image_format: str = "png",
    min_width: int = 50,
    min_height: int = 50
) -> str:
    """
    Extrait toutes les images d'un PDF.
    
    Args:
        pdf_path: Chemin du fichier PDF
        output_format: Format de sortie (base64, path) (défaut: base64)
        image_format: Format des images (png, jpg) (défaut: png)
        min_width: Largeur minimale des images (défaut: 50)
        min_height: Hauteur minimale des images (défaut: 50)
    
    Returns:
        JSON avec les images extraites et leurs métadonnées
    """
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.is_absolute():
            pdf_file = WORKSPACE_PATH / pdf_file
        
        if not pdf_file.exists():
            return json.dumps({"error": f"Fichier non trouvé: {pdf_file}"})
        
        images = extract_images_pymupdf(pdf_file, output_format, image_format, min_width, min_height)
        
        result = {
            "file": str(pdf_file),
            "images_found": len(images),
            "output_format": output_format,
            "image_format": image_format,
            "filters": {
                "min_width": min_width,
                "min_height": min_height
            },
            "images": images
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des images: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def extract_pdf_tables(
    pdf_path: str,
    page_numbers: Optional[List[int]] = None,
    output_format: str = "json"
) -> str:
    """
    Extrait les tableaux d'un PDF.
    
    Args:
        pdf_path: Chemin du fichier PDF
        page_numbers: Pages à analyser (défaut: toutes)
        output_format: Format de sortie (json, csv) (défaut: json)
    
    Returns:
        JSON avec les tableaux extraits
    """
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.is_absolute():
            pdf_file = WORKSPACE_PATH / pdf_file
        
        if not pdf_file.exists():
            return json.dumps({"error": f"Fichier non trouvé: {pdf_file}"})
        
        tables = extract_tables_pdfplumber(pdf_file, page_numbers, output_format)
        
        result = {
            "file": str(pdf_file),
            "tables_found": len(tables),
            "output_format": output_format,
            "tables": tables
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des tableaux: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_pdf_metadata(
    pdf_path: str
) -> str:
    """
    Récupère les métadonnées d'un PDF.
    
    Args:
        pdf_path: Chemin du fichier PDF
    
    Returns:
        JSON avec les métadonnées
    """
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.is_absolute():
            pdf_file = WORKSPACE_PATH / pdf_file
        
        if not pdf_file.exists():
            return json.dumps({"error": f"Fichier non trouvé: {pdf_file}"})
        
        metadata = get_pdf_metadata_pypdf2(pdf_file)
        
        result = {
            "file": str(pdf_file),
            "metadata": metadata
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des métadonnées: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def search_in_pdf(
    pdf_path: str,
    search_text: str,
    case_sensitive: bool = False,
    whole_words: bool = False
) -> str:
    """
    Recherche du texte dans un PDF.
    
    Args:
        pdf_path: Chemin du fichier PDF
        search_text: Texte à rechercher
        case_sensitive: Recherche sensible à la casse (défaut: false)
        whole_words: Mots entiers uniquement (défaut: false)
    
    Returns:
        JSON avec les occurrences trouvées et leur contexte
    """
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.is_absolute():
            pdf_file = WORKSPACE_PATH / pdf_file
        
        if not pdf_file.exists():
            return json.dumps({"error": f"Fichier non trouvé: {pdf_file}"})
        
        results = search_text_in_pdf(pdf_file, search_text, case_sensitive, whole_words)
        
        result = {
            "file": str(pdf_file),
            "search_text": search_text,
            "case_sensitive": case_sensitive,
            "whole_words": whole_words,
            "occurrences_found": len(results),
            "results": results
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {e}")
        return json.dumps({"error": str(e)})

# Point d'entrée principal
def main():
    """Lance le serveur MCP."""
    logger.info("Démarrage du serveur PDF Analyzer (FastMCP)...")
    logger.info(f"Workspace: {WORKSPACE_PATH}")
    logger.info(f"Répertoire temporaire: {TEMP_DIR}")
    
    # Vérifier que les dépendances sont installées
    try:
        import PyPDF2
        import fitz
        import pdfplumber
        from PIL import Image
        logger.info("Toutes les dépendances PDF sont disponibles")
    except ImportError as e:
        logger.error(f"Dépendances manquantes: {e}")
        logger.error("Installez avec: pip install PyPDF2 pymupdf pdfplumber pillow")
        sys.exit(1)
    
    # Lancer le serveur
    mcp.run()

if __name__ == "__main__":
    main()