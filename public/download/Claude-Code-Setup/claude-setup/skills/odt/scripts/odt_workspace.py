#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
ODT WORKSPACE - Manipulation de fichiers ODT avec workflow iteratif
=============================================================================

Ce script permet de:
1. Dezipper un ODT vers un dossier workspace
2. Analyser la structure du document (paragraphes, styles, formules)
3. Modifier le content.xml via des commandes simples
4. Re-pack le dossier en ODT
5. Convertir en PDF pour feedback visuel

Usage comme module:
    from odt_workspace import ODTWorkspace

    ws = ODTWorkspace("mon_doc.odt")
    ws.unpack()                          # Dezippe vers mon_doc_workspace/
    ws.analyze()                         # Affiche la structure
    ws.replace_text("ancien", "nouveau") # Modifie le texte
    ws.pack()                            # Recree l'ODT
    ws.to_pdf()                          # Convertit en PDF

Usage en ligne de commande:
    python odt_workspace.py unpack mon_doc.odt
    python odt_workspace.py analyze mon_doc.odt
    python odt_workspace.py pack mon_doc_workspace mon_doc_modifie.odt
    python odt_workspace.py topdf mon_doc.odt
"""

import os
import sys
import re
import shutil
import zipfile
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Optional, List, Dict, Tuple

# Namespace ODF
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'meta': 'urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
    'svg': 'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0',
}

# Chemin LibreOffice Windows
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"


class ODTWorkspace:
    """
    Gere un espace de travail pour modifier un fichier ODT.
    """

    def __init__(self, odt_path: str, workspace_dir: Optional[str] = None):
        """
        Initialise le workspace.

        Args:
            odt_path: Chemin vers le fichier ODT
            workspace_dir: Dossier de travail (defaut: {odt_name}_workspace)
        """
        self.odt_path = Path(odt_path).resolve()
        self.workspace_dir = Path(workspace_dir) if workspace_dir else \
            self.odt_path.parent / f"{self.odt_path.stem}_workspace"

        self.content_xml: Optional[ET.Element] = None
        self.styles_xml: Optional[ET.Element] = None
        self._modified = False

        # Enregistrer les namespaces pour eviter les prefixes ns0, ns1, etc.
        for prefix, uri in NS.items():
            ET.register_namespace(prefix, uri)

    def unpack(self) -> str:
        """
        Extrait le contenu de l'ODT vers le dossier workspace.

        Returns:
            Chemin du dossier workspace
        """
        if not self.odt_path.exists():
            raise FileNotFoundError(f"Fichier non trouve: {self.odt_path}")

        # Nettoyer le workspace existant
        if self.workspace_dir.exists():
            shutil.rmtree(self.workspace_dir)

        self.workspace_dir.mkdir(parents=True)

        with zipfile.ZipFile(self.odt_path, 'r') as z:
            z.extractall(self.workspace_dir)

        # Charger les fichiers XML
        self._load_xml()

        print(f"[UNPACK] Extrait vers: {self.workspace_dir}")
        return str(self.workspace_dir)

    def _load_xml(self):
        """Charge les fichiers XML en memoire."""
        content_path = self.workspace_dir / "content.xml"
        styles_path = self.workspace_dir / "styles.xml"

        if content_path.exists():
            self.content_xml = ET.parse(content_path).getroot()
        if styles_path.exists():
            self.styles_xml = ET.parse(styles_path).getroot()

    def _save_xml(self):
        """Sauvegarde les fichiers XML modifies."""
        if self.content_xml is not None:
            content_path = self.workspace_dir / "content.xml"
            tree = ET.ElementTree(self.content_xml)
            tree.write(content_path, encoding='utf-8', xml_declaration=True)

        if self.styles_xml is not None:
            styles_path = self.workspace_dir / "styles.xml"
            tree = ET.ElementTree(self.styles_xml)
            tree.write(styles_path, encoding='utf-8', xml_declaration=True)

    def analyze(self, verbose: bool = True) -> Dict:
        """
        Analyse la structure du document et retourne un resume.

        Returns:
            Dict avec la structure du document
        """
        if self.content_xml is None:
            if self.workspace_dir.exists():
                self._load_xml()
            else:
                self.unpack()

        result = {
            'paragraphs': [],
            'headings': [],
            'tables': [],
            'formulas': [],
            'styles_used': set(),
        }

        # Trouver le body
        body = self.content_xml.find('.//office:body/office:text', NS)
        if body is None:
            print("[ANALYZE] Pas de contenu trouve")
            return result

        idx = 0
        for elem in body:
            tag = elem.tag.split('}')[-1]  # Enlever le namespace

            if tag == 'p':
                style = elem.get(f'{{{NS["text"]}}}style-name', 'default')
                text = self._get_text(elem)
                result['paragraphs'].append({
                    'idx': idx,
                    'style': style,
                    'text': text[:100] + ('...' if len(text) > 100 else ''),
                    'full_text': text
                })
                result['styles_used'].add(style)
                idx += 1

            elif tag == 'h':
                level = elem.get(f'{{{NS["text"]}}}outline-level', '1')
                text = self._get_text(elem)
                result['headings'].append({
                    'idx': idx,
                    'level': level,
                    'text': text
                })
                idx += 1

            elif tag == 'table':
                name = elem.get(f'{{{NS["table"]}}}name', 'Table')
                rows = len(elem.findall('.//table:table-row', NS))
                result['tables'].append({
                    'idx': idx,
                    'name': name,
                    'rows': rows
                })
                idx += 1

            elif tag == 'section':
                # Section (souvent utilisee pour les environnements)
                name = elem.get(f'{{{NS["text"]}}}name', 'Section')
                idx += 1

        # Compter les formules (objets OLE)
        formulas = self.content_xml.findall('.//draw:object', NS)
        result['formulas'] = len(formulas)

        result['styles_used'] = list(result['styles_used'])

        if verbose:
            self._print_analysis(result)

        return result

    def _get_text(self, elem) -> str:
        """Extrait le texte d'un element, y compris les sous-elements."""
        texts = []
        if elem.text:
            texts.append(elem.text)
        for child in elem:
            texts.append(self._get_text(child))
            if child.tail:
                texts.append(child.tail)
        return ''.join(texts)

    def _print_analysis(self, result: Dict):
        """Affiche l'analyse de maniere lisible."""
        print("\n" + "="*60)
        print("ANALYSE DU DOCUMENT ODT")
        print("="*60)

        print(f"\n[STATISTIQUES]")
        print(f"  Paragraphes: {len(result['paragraphs'])}")
        print(f"  Titres: {len(result['headings'])}")
        print(f"  Tableaux: {len(result['tables'])}")
        print(f"  Formules: {result['formulas']}")
        print(f"  Styles utilises: {len(result['styles_used'])}")

        print(f"\n[STRUCTURE]")
        for h in result['headings']:
            indent = "  " * int(h['level'])
            print(f"  {indent}H{h['level']}: {h['text']}")

        print(f"\n[PARAGRAPHES] (premiers 20)")
        for p in result['paragraphs'][:20]:
            style = p['style'][:20].ljust(20)
            text = p['text'][:50]
            print(f"  [{p['idx']:3d}] {style} | {text}")

        if len(result['paragraphs']) > 20:
            print(f"  ... et {len(result['paragraphs']) - 20} autres paragraphes")

        print("\n" + "="*60)

    def get_paragraph(self, idx: int) -> Optional[Dict]:
        """
        Recupere un paragraphe par son index.

        Args:
            idx: Index du paragraphe

        Returns:
            Dict avec style et texte complet
        """
        result = self.analyze(verbose=False)
        for p in result['paragraphs']:
            if p['idx'] == idx:
                return p
        return None

    def replace_text(self, old_text: str, new_text: str,
                     first_only: bool = False) -> int:
        """
        Remplace du texte dans le document.

        Args:
            old_text: Texte a remplacer
            new_text: Nouveau texte
            first_only: Si True, ne remplace que la premiere occurrence

        Returns:
            Nombre de remplacements effectues
        """
        if self.content_xml is None:
            self._load_xml()

        count = 0
        for elem in self.content_xml.iter():
            if elem.text and old_text in elem.text:
                if first_only and count > 0:
                    break
                elem.text = elem.text.replace(old_text, new_text)
                count += 1
            if elem.tail and old_text in elem.tail:
                if first_only and count > 0:
                    break
                elem.tail = elem.tail.replace(old_text, new_text)
                count += 1

        if count > 0:
            self._modified = True
            self._save_xml()
            print(f"[REPLACE] {count} remplacement(s): '{old_text}' -> '{new_text}'")

        return count

    def add_paragraph(self, text: str, style: str = "Standard",
                      after_idx: Optional[int] = None) -> bool:
        """
        Ajoute un paragraphe au document.

        Args:
            text: Texte du paragraphe
            style: Nom du style a appliquer
            after_idx: Inserer apres cet index (None = a la fin)

        Returns:
            True si succes
        """
        if self.content_xml is None:
            self._load_xml()

        body = self.content_xml.find('.//office:body/office:text', NS)
        if body is None:
            print("[ERROR] Pas de body trouve")
            return False

        # Creer le nouveau paragraphe
        new_p = ET.Element(f'{{{NS["text"]}}}p')
        new_p.set(f'{{{NS["text"]}}}style-name', style)
        new_p.text = text

        if after_idx is not None:
            # Trouver la position
            children = list(body)
            insert_pos = min(after_idx + 1, len(children))
            body.insert(insert_pos, new_p)
        else:
            body.append(new_p)

        self._modified = True
        self._save_xml()
        print(f"[ADD] Paragraphe ajoute: '{text[:50]}...' (style: {style})")
        return True

    def delete_paragraph(self, idx: int) -> bool:
        """
        Supprime un paragraphe par son index.

        Args:
            idx: Index du paragraphe a supprimer

        Returns:
            True si succes
        """
        if self.content_xml is None:
            self._load_xml()

        body = self.content_xml.find('.//office:body/office:text', NS)
        if body is None:
            return False

        children = list(body)
        if 0 <= idx < len(children):
            body.remove(children[idx])
            self._modified = True
            self._save_xml()
            print(f"[DELETE] Paragraphe {idx} supprime")
            return True

        print(f"[ERROR] Index {idx} hors limites")
        return False

    def set_paragraph_text(self, idx: int, new_text: str) -> bool:
        """
        Modifie le texte d'un paragraphe.

        Args:
            idx: Index du paragraphe
            new_text: Nouveau texte

        Returns:
            True si succes
        """
        if self.content_xml is None:
            self._load_xml()

        body = self.content_xml.find('.//office:body/office:text', NS)
        if body is None:
            return False

        children = list(body)
        if 0 <= idx < len(children):
            elem = children[idx]
            # Supprimer les enfants (garder le style)
            for child in list(elem):
                elem.remove(child)
            elem.text = new_text
            self._modified = True
            self._save_xml()
            print(f"[SET] Paragraphe {idx}: '{new_text[:50]}...'")
            return True

        return False

    def pack(self, output_path: Optional[str] = None) -> str:
        """
        Recree le fichier ODT depuis le workspace.

        Args:
            output_path: Chemin de sortie (defaut: meme que l'original)

        Returns:
            Chemin du fichier cree
        """
        if not self.workspace_dir.exists():
            raise FileNotFoundError(f"Workspace non trouve: {self.workspace_dir}")

        output = Path(output_path) if output_path else self.odt_path

        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
            # Le mimetype DOIT etre non compresse et en premier
            mimetype_path = self.workspace_dir / 'mimetype'
            if mimetype_path.exists():
                z.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
            else:
                z.writestr('mimetype', 'application/vnd.oasis.opendocument.text',
                          compress_type=zipfile.ZIP_STORED)

            # Ajouter tous les autres fichiers
            for root, dirs, files in os.walk(self.workspace_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.')]

                for file in files:
                    if file == 'mimetype' or file.startswith('.'):
                        continue

                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.workspace_dir)
                    z.write(file_path, arcname)

        size = output.stat().st_size
        print(f"[PACK] Cree: {output} ({size} octets)")
        return str(output)

    def to_pdf(self, output_path: Optional[str] = None) -> str:
        """
        Convertit l'ODT en PDF via LibreOffice.

        Args:
            output_path: Chemin de sortie (defaut: meme nom avec .pdf)

        Returns:
            Chemin du fichier PDF
        """
        if not self.odt_path.exists():
            raise FileNotFoundError(f"Fichier ODT non trouve: {self.odt_path}")

        if not Path(SOFFICE_PATH).exists():
            raise FileNotFoundError(f"LibreOffice non trouve: {SOFFICE_PATH}")

        output_dir = self.odt_path.parent if output_path is None else Path(output_path).parent

        # Commande LibreOffice
        cmd = [
            SOFFICE_PATH,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', str(output_dir),
            str(self.odt_path)
        ]

        print(f"[PDF] Conversion en cours...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}")
            raise RuntimeError(f"Erreur conversion: {result.stderr}")

        pdf_path = output_dir / f"{self.odt_path.stem}.pdf"
        print(f"[PDF] Cree: {pdf_path}")
        return str(pdf_path)

    def cleanup(self):
        """Supprime le dossier workspace."""
        if self.workspace_dir.exists():
            shutil.rmtree(self.workspace_dir)
            print(f"[CLEANUP] Supprime: {self.workspace_dir}")


def print_help():
    """Affiche l'aide."""
    print("""
ODT WORKSPACE - Manipulation de fichiers ODT

Commandes:
  unpack <fichier.odt>              Extrait l'ODT vers un dossier workspace
  analyze <fichier.odt>             Affiche la structure du document
  pack <dossier> <fichier.odt>      Cree un ODT depuis un dossier
  topdf <fichier.odt>               Convertit en PDF
  replace <fichier.odt> <ancien> <nouveau>  Remplace du texte

Exemples:
  python odt_workspace.py unpack mon_doc.odt
  python odt_workspace.py analyze mon_doc.odt
  python odt_workspace.py topdf mon_doc.odt
  python odt_workspace.py replace mon_doc.odt "ancien texte" "nouveau texte"
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == 'unpack' and len(sys.argv) >= 3:
        ws = ODTWorkspace(sys.argv[2])
        ws.unpack()
        ws.analyze()

    elif cmd == 'analyze' and len(sys.argv) >= 3:
        ws = ODTWorkspace(sys.argv[2])
        if not ws.workspace_dir.exists():
            ws.unpack()
        ws.analyze()

    elif cmd == 'pack' and len(sys.argv) >= 4:
        ws = ODTWorkspace(sys.argv[3], workspace_dir=sys.argv[2])
        ws.pack(sys.argv[3])

    elif cmd == 'topdf' and len(sys.argv) >= 3:
        ws = ODTWorkspace(sys.argv[2])
        ws.to_pdf()

    elif cmd == 'replace' and len(sys.argv) >= 5:
        ws = ODTWorkspace(sys.argv[2])
        if not ws.workspace_dir.exists():
            ws.unpack()
        ws.replace_text(sys.argv[3], sys.argv[4])
        ws.pack()

    else:
        print_help()
        sys.exit(1)
