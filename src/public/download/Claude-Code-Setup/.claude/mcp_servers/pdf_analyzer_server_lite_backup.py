#!/usr/bin/env python3
"""
Serveur MCP pour l'analyse de fichiers PDF (version lite sans pikepdf).

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

import mcp.server
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

# Bibliothèques PDF
import PyPDF2
import fitz  # PyMuPDF pour extraction d'images
import pdfplumber  # Pour extraction de tableaux
from PIL import Image

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_analyzer_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PDFAnalyzerServer:
    """Serveur MCP pour l'analyse de fichiers PDF."""
    
    def __init__(self):
        self.server = Server("pdf-analyzer-server")
        logger.info("Initialisation du serveur PDF Analyzer (version lite)")
        
        # Configuration des chemins
        self.workspace_path = Path(r"C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours")
        self.temp_dir = Path(os.environ.get('TEMP', '/tmp')) / 'pdf_analyzer'
        self.temp_dir.mkdir(exist_ok=True)
        
        # Enregistrement des outils
        self._register_tools()
        
    def _register_tools(self):
        """Enregistre tous les outils disponibles."""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="analyze_pdf",
                    description="""
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
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pdf_path": {
                                "type": "string",
                                "description": "Chemin du fichier PDF"
                            },
                            "extract_images": {
                                "type": "boolean",
                                "description": "Extraire les images",
                                "default": True
                            },
                            "extract_text": {
                                "type": "boolean",
                                "description": "Extraire le texte",
                                "default": True
                            },
                            "extract_metadata": {
                                "type": "boolean",
                                "description": "Extraire les métadonnées",
                                "default": True
                            },
                            "extract_structure": {
                                "type": "boolean",
                                "description": "Extraire la structure",
                                "default": True
                            },
                            "page_range": {
                                "type": "string",
                                "description": "Pages à analyser (ex: '1-5,7,10')",
                                "default": ""
                            }
                        },
                        "required": ["pdf_path"]
                    }
                ),
                
                Tool(
                    name="extract_pdf_text",
                    description="""
                    Extrait uniquement le texte d'un PDF.
                    
                    Args:
                        pdf_path: Chemin du fichier PDF
                        page_numbers: Liste des numéros de pages (défaut: toutes)
                        preserve_layout: Préserver la mise en page (défaut: false)
                    
                    Returns:
                        JSON avec le texte extrait par page
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pdf_path": {
                                "type": "string",
                                "description": "Chemin du fichier PDF"
                            },
                            "page_numbers": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Numéros de pages à extraire",
                                "default": []
                            },
                            "preserve_layout": {
                                "type": "boolean",
                                "description": "Préserver la mise en page",
                                "default": False
                            }
                        },
                        "required": ["pdf_path"]
                    }
                ),
                
                Tool(
                    name="extract_pdf_images",
                    description="""
                    Extrait toutes les images d'un PDF.
                    
                    Args:
                        pdf_path: Chemin du fichier PDF
                        output_format: Format de sortie (base64, path) (défaut: base64)
                        image_format: Format des images (png, jpg) (défaut: png)
                        min_width: Largeur minimale des images (défaut: 50)
                        min_height: Hauteur minimale des images (défaut: 50)
                    
                    Returns:
                        JSON avec les images extraites et leurs métadonnées
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pdf_path": {
                                "type": "string",
                                "description": "Chemin du fichier PDF"
                            },
                            "output_format": {
                                "type": "string",
                                "enum": ["base64", "path"],
                                "description": "Format de sortie des images",
                                "default": "base64"
                            },
                            "image_format": {
                                "type": "string",
                                "enum": ["png", "jpg"],
                                "description": "Format des images extraites",
                                "default": "png"
                            },
                            "min_width": {
                                "type": "integer",
                                "description": "Largeur minimale des images",
                                "default": 50
                            },
                            "min_height": {
                                "type": "integer",
                                "description": "Hauteur minimale des images",
                                "default": 50
                            }
                        },
                        "required": ["pdf_path"]
                    }
                ),
                
                Tool(
                    name="extract_pdf_tables",
                    description="""
                    Extrait les tableaux d'un PDF.
                    
                    Args:
                        pdf_path: Chemin du fichier PDF
                        page_numbers: Pages à analyser (défaut: toutes)
                        output_format: Format de sortie (json, csv) (défaut: json)
                    
                    Returns:
                        JSON avec les tableaux extraits
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pdf_path": {
                                "type": "string",
                                "description": "Chemin du fichier PDF"
                            },
                            "page_numbers": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Pages à analyser",
                                "default": []
                            },
                            "output_format": {
                                "type": "string",
                                "enum": ["json", "csv"],
                                "description": "Format de sortie",
                                "default": "json"
                            }
                        },
                        "required": ["pdf_path"]
                    }
                ),
                
                Tool(
                    name="get_pdf_metadata",
                    description="""
                    Récupère les métadonnées d'un PDF.
                    
                    Args:
                        pdf_path: Chemin du fichier PDF
                    
                    Returns:
                        JSON avec les métadonnées
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pdf_path": {
                                "type": "string",
                                "description": "Chemin du fichier PDF"
                            }
                        },
                        "required": ["pdf_path"]
                    }
                ),
                
                Tool(
                    name="search_in_pdf",
                    description="""
                    Recherche du texte dans un PDF.
                    
                    Args:
                        pdf_path: Chemin du fichier PDF
                        search_text: Texte à rechercher
                        case_sensitive: Recherche sensible à la casse (défaut: false)
                        whole_words: Mots entiers uniquement (défaut: false)
                    
                    Returns:
                        JSON avec les occurrences trouvées et leur contexte
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pdf_path": {
                                "type": "string",
                                "description": "Chemin du fichier PDF"
                            },
                            "search_text": {
                                "type": "string",
                                "description": "Texte à rechercher"
                            },
                            "case_sensitive": {
                                "type": "boolean",
                                "description": "Sensible à la casse",
                                "default": False
                            },
                            "whole_words": {
                                "type": "boolean",
                                "description": "Mots entiers uniquement",
                                "default": False
                            }
                        },
                        "required": ["pdf_path", "search_text"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            try:
                logger.info(f"Appel de l'outil: {name} avec arguments: {arguments}")
                
                if name == "analyze_pdf":
                    result = await self._analyze_pdf(**arguments)
                elif name == "extract_pdf_text":
                    result = await self._extract_pdf_text(**arguments)
                elif name == "extract_pdf_images":
                    result = await self._extract_pdf_images(**arguments)
                elif name == "extract_pdf_tables":
                    result = await self._extract_pdf_tables(**arguments)
                elif name == "get_pdf_metadata":
                    result = await self._get_pdf_metadata(**arguments)
                elif name == "search_in_pdf":
                    result = await self._search_in_pdf(**arguments)
                else:
                    result = {"error": f"Outil non reconnu: {name}"}
                
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
                
            except Exception as e:
                logger.error(f"Erreur lors de l'exécution de {name}: {str(e)}")
                return [TextContent(
                    type="text", 
                    text=json.dumps({"error": str(e)}, ensure_ascii=False)
                )]
    
    async def _analyze_pdf(self, pdf_path: str, extract_images: bool = True, 
                          extract_text: bool = True, extract_metadata: bool = True,
                          extract_structure: bool = True, page_range: str = "") -> Dict[str, Any]:
        """Analyse complète d'un fichier PDF."""
        
        pdf_path = self._resolve_path(pdf_path)
        if not pdf_path.exists():
            return {"error": f"Fichier PDF non trouvé: {pdf_path}"}
        
        result = {
            "file_path": str(pdf_path),
            "file_size": pdf_path.stat().st_size,
            "analysis_date": datetime.now().isoformat()
        }
        
        # Extraction selon les options
        if extract_metadata:
            result["metadata"] = await self._get_pdf_metadata(str(pdf_path))
        
        if extract_structure:
            result["structure"] = self._get_pdf_structure(pdf_path)
        
        if extract_text:
            result["text"] = await self._extract_pdf_text(str(pdf_path))
        
        if extract_images:
            result["images"] = await self._extract_pdf_images(str(pdf_path), output_format="base64")
        
        # Statistiques
        result["statistics"] = self._calculate_statistics(result)
        
        return result
    
    async def _extract_pdf_text(self, pdf_path: str, page_numbers: List[int] = None,
                               preserve_layout: bool = False) -> Dict[str, Any]:
        """Extrait le texte d'un PDF."""
        
        pdf_path = self._resolve_path(pdf_path)
        result = {"pages": {}, "total_text": ""}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_extract = page_numbers if page_numbers else range(1, total_pages + 1)
                
                all_text = []
                
                for page_num in pages_to_extract:
                    if 1 <= page_num <= total_pages:
                        page = pdf.pages[page_num - 1]
                        
                        if preserve_layout:
                            text = page.extract_text(layout=True)
                        else:
                            text = page.extract_text()
                        
                        if text:
                            result["pages"][str(page_num)] = {
                                "text": text,
                                "char_count": len(text),
                                "word_count": len(text.split())
                            }
                            all_text.append(text)
                
                result["total_text"] = "\n\n".join(all_text)
                result["total_pages"] = total_pages
                result["extracted_pages"] = len(result["pages"])
                
        except Exception as e:
            logger.error(f"Erreur extraction texte: {str(e)}")
            result["error"] = str(e)
        
        return result
    
    async def _extract_pdf_images(self, pdf_path: str, output_format: str = "base64",
                                 image_format: str = "png", min_width: int = 50,
                                 min_height: int = 50) -> Dict[str, Any]:
        """Extrait toutes les images d'un PDF."""
        
        pdf_path = self._resolve_path(pdf_path)
        result = {"images": [], "total_count": 0}
        
        try:
            pdf_document = fitz.open(str(pdf_path))
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    try:
                        # Extraction de l'image
                        xref = img[0]
                        pix = fitz.Pixmap(pdf_document, xref)
                        
                        # Conversion si nécessaire
                        if pix.n - pix.alpha > 3:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        
                        # Vérification des dimensions
                        if pix.width >= min_width and pix.height >= min_height:
                            img_data = {
                                "page": page_num + 1,
                                "index": img_index,
                                "width": pix.width,
                                "height": pix.height,
                                "format": image_format
                            }
                            
                            if output_format == "base64":
                                # Conversion en PIL Image
                                img_buffer = pix.pil_tobytes(format=image_format.upper())
                                img_data["data"] = base64.b64encode(img_buffer).decode('utf-8')
                            else:  # path
                                # Sauvegarde sur disque
                                img_path = self.temp_dir / f"pdf_img_{page_num}_{img_index}.{image_format}"
                                pix.save(str(img_path))
                                img_data["path"] = str(img_path)
                            
                            result["images"].append(img_data)
                        
                        pix = None  # Libération mémoire
                        
                    except Exception as e:
                        logger.error(f"Erreur extraction image {img_index} page {page_num}: {str(e)}")
            
            pdf_document.close()
            result["total_count"] = len(result["images"])
            
        except Exception as e:
            logger.error(f"Erreur extraction images: {str(e)}")
            result["error"] = str(e)
        
        return result
    
    async def _extract_pdf_tables(self, pdf_path: str, page_numbers: List[int] = None,
                                 output_format: str = "json") -> Dict[str, Any]:
        """Extrait les tableaux d'un PDF."""
        
        pdf_path = self._resolve_path(pdf_path)
        result = {"tables": [], "total_count": 0}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pages_to_check = page_numbers if page_numbers else range(1, len(pdf.pages) + 1)
                
                for page_num in pages_to_check:
                    if 1 <= page_num <= len(pdf.pages):
                        page = pdf.pages[page_num - 1]
                        tables = page.extract_tables()
                        
                        for table_index, table in enumerate(tables):
                            if table and len(table) > 0:
                                table_data = {
                                    "page": page_num,
                                    "index": table_index,
                                    "rows": len(table),
                                    "columns": len(table[0]) if table[0] else 0
                                }
                                
                                if output_format == "json":
                                    table_data["data"] = table
                                else:  # csv
                                    import csv
                                    import io
                                    output = io.StringIO()
                                    writer = csv.writer(output)
                                    writer.writerows(table)
                                    table_data["csv"] = output.getvalue()
                                
                                result["tables"].append(table_data)
                
                result["total_count"] = len(result["tables"])
                
        except Exception as e:
            logger.error(f"Erreur extraction tableaux: {str(e)}")
            result["error"] = str(e)
        
        return result
    
    async def _get_pdf_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """Récupère les métadonnées d'un PDF."""
        
        pdf_path = self._resolve_path(pdf_path)
        result = {}
        
        try:
            # Métadonnées basiques avec PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Info du document
                if reader.metadata:
                    result["document_info"] = {
                        "title": reader.metadata.get('/Title', ''),
                        "author": reader.metadata.get('/Author', ''),
                        "subject": reader.metadata.get('/Subject', ''),
                        "creator": reader.metadata.get('/Creator', ''),
                        "producer": reader.metadata.get('/Producer', ''),
                        "creation_date": str(reader.metadata.get('/CreationDate', '')),
                        "modification_date": str(reader.metadata.get('/ModDate', '')),
                        "keywords": reader.metadata.get('/Keywords', '')
                    }
                
                # Infos structurelles
                result["structure"] = {
                    "pages": len(reader.pages),
                    "encrypted": reader.is_encrypted,
                    "pdf_version": reader.pdf_header if hasattr(reader, 'pdf_header') else 'Unknown'
                }
                
        except Exception as e:
            logger.error(f"Erreur extraction métadonnées: {str(e)}")
            result["error"] = str(e)
        
        return result
    
    async def _search_in_pdf(self, pdf_path: str, search_text: str, 
                           case_sensitive: bool = False, whole_words: bool = False) -> Dict[str, Any]:
        """Recherche du texte dans un PDF."""
        
        pdf_path = self._resolve_path(pdf_path)
        result = {"matches": [], "total_matches": 0}
        
        try:
            import re
            
            # Préparation du pattern de recherche
            if whole_words:
                pattern = r'\b' + re.escape(search_text) + r'\b'
            else:
                pattern = re.escape(search_text)
            
            flags = 0 if case_sensitive else re.IGNORECASE
            regex = re.compile(pattern, flags)
            
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        # Recherche des occurrences
                        for match in regex.finditer(text):
                            # Contexte autour du match
                            start = max(0, match.start() - 50)
                            end = min(len(text), match.end() + 50)
                            context = text[start:end]
                            
                            result["matches"].append({
                                "page": page_num,
                                "position": match.start(),
                                "matched_text": match.group(),
                                "context": context
                            })
                
                result["total_matches"] = len(result["matches"])
                result["search_query"] = {
                    "text": search_text,
                    "case_sensitive": case_sensitive,
                    "whole_words": whole_words
                }
                
        except Exception as e:
            logger.error(f"Erreur recherche dans PDF: {str(e)}")
            result["error"] = str(e)
        
        return result
    
    def _get_pdf_structure(self, pdf_path: Path) -> Dict[str, Any]:
        """Récupère la structure d'un PDF."""
        structure = {}
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Signets (bookmarks)
                structure["bookmarks"] = self._extract_bookmarks(reader)
                
                # Liens
                structure["links"] = []
                for page_num, page in enumerate(reader.pages, 1):
                    if '/Annots' in page:
                        annots = page['/Annots']
                        for annot_ref in annots:
                            annot = annot_ref.get_object()
                            if annot.get('/Subtype') == '/Link':
                                link_info = {
                                    "page": page_num,
                                    "type": "link"
                                }
                                if '/A' in annot and '/URI' in annot['/A']:
                                    link_info["uri"] = annot['/A']['/URI']
                                structure["links"].append(link_info)
                
                # Formulaires
                if reader.trailer and '/Root' in reader.trailer:
                    root = reader.trailer['/Root']
                    if '/AcroForm' in root:
                        structure["has_forms"] = True
                        try:
                            structure["form_fields"] = len(reader.get_form_text_fields())
                        except:
                            structure["form_fields"] = "Unknown"
                    else:
                        structure["has_forms"] = False
                else:
                    structure["has_forms"] = False
                
        except Exception as e:
            logger.error(f"Erreur extraction structure: {str(e)}")
            structure["error"] = str(e)
        
        return structure
    
    def _extract_bookmarks(self, reader: PyPDF2.PdfReader, outline=None, level=0) -> List[Dict]:
        """Extrait récursivement les signets d'un PDF."""
        if outline is None:
            outline = reader.outline if hasattr(reader, 'outline') else []
        
        bookmarks = []
        for item in outline:
            if isinstance(item, list):
                bookmarks.extend(self._extract_bookmarks(reader, item, level + 1))
            else:
                bookmark = {
                    "title": str(item.title) if hasattr(item, 'title') else "Unknown",
                    "level": level
                }
                try:
                    if hasattr(item, 'page'):
                        bookmark["page"] = reader.get_destination_page_number(item) + 1
                except:
                    pass
                bookmarks.append(bookmark)
        
        return bookmarks
    
    def _calculate_statistics(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule des statistiques sur l'analyse."""
        stats = {}
        
        # Statistiques texte
        if "text" in analysis_result and "pages" in analysis_result["text"]:
            total_chars = sum(p["char_count"] for p in analysis_result["text"]["pages"].values())
            total_words = sum(p["word_count"] for p in analysis_result["text"]["pages"].values())
            stats["text"] = {
                "total_characters": total_chars,
                "total_words": total_words,
                "average_words_per_page": total_words / len(analysis_result["text"]["pages"]) if analysis_result["text"]["pages"] else 0
            }
        
        # Statistiques images
        if "images" in analysis_result:
            stats["images"] = {
                "total_count": analysis_result["images"].get("total_count", 0),
                "average_per_page": analysis_result["images"].get("total_count", 0) / analysis_result.get("metadata", {}).get("structure", {}).get("pages", 1)
            }
        
        return stats
    
    def _resolve_path(self, path: str) -> Path:
        """Résout un chemin relatif ou absolu."""
        path = Path(path)
        if not path.is_absolute():
            path = self.workspace_path / path
        return path
    
    async def run(self):
        """Lance le serveur MCP."""
        logger.info("Démarrage du serveur PDF Analyzer MCP (version lite)")
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

if __name__ == "__main__":
    import asyncio
    
    server = PDFAnalyzerServer()
    asyncio.run(server.run())