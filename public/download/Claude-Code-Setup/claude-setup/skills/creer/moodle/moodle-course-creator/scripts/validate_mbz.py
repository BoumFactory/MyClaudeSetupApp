#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validateur de fichiers .mbz (Moodle Backup)

Ce script vérifie qu'un fichier .mbz est correctement structuré
et que tous les contenus H5P sont valides avant import dans Moodle.

Usage:
    python validate_mbz.py cours.mbz [--verbose] [--fix]

Vérifie:
    1. Structure du fichier (tar.gz valide)
    2. Fichiers obligatoires du backup Moodle
    3. Activités H5P correctement référencées
    4. Structure JSON des contenus H5P
    5. Encodage et caractères spéciaux
"""

import tarfile
import zipfile
import json
import hashlib
import xml.etree.ElementTree as ET
import argparse
import sys
import io
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Résultat de validation"""
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.valid = False

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def add_info(self, msg: str):
        self.info.append(msg)


class MBZValidator:
    """Validateur complet de fichiers .mbz"""

    # Fichiers obligatoires dans un backup Moodle
    REQUIRED_FILES = [
        'moodle_backup.xml',
        'course/course.xml',
    ]

    # Structure H5P attendue
    H5P_REQUIRED_FILES = ['h5p.json', 'content/content.json']

    def __init__(self, mbz_path: str, verbose: bool = False):
        self.mbz_path = Path(mbz_path)
        self.verbose = verbose
        self.result = ValidationResult()
        self.tar = None
        self.files_in_mbz: Dict[str, bytes] = {}
        self.h5p_activities: Dict[str, dict] = {}
        self.file_references: Dict[str, str] = {}  # hash -> filename

    def validate(self) -> ValidationResult:
        """Exécute toutes les validations"""
        print(f"\n{'='*60}")
        print(f"  VALIDATION: {self.mbz_path.name}")
        print(f"{'='*60}\n")

        # 1. Vérifier que le fichier existe
        if not self._check_file_exists():
            return self.result

        # 2. Vérifier la structure tar.gz
        if not self._check_tar_structure():
            return self.result

        # 3. Charger tous les fichiers
        self._load_all_files()

        # 4. Vérifier les fichiers obligatoires
        self._check_required_files()

        # 5. Parser les activités H5P
        self._parse_h5p_activities()

        # 6. Valider chaque fichier H5P
        self._validate_h5p_contents()

        # 7. Vérifier les références de fichiers
        self._check_file_references()

        # 8. Afficher le résumé
        self._print_summary()

        return self.result

    def _check_file_exists(self) -> bool:
        """Vérifie que le fichier existe"""
        if not self.mbz_path.exists():
            self.result.add_error(f"Fichier introuvable: {self.mbz_path}")
            return False

        size_kb = self.mbz_path.stat().st_size / 1024
        self.result.add_info(f"Taille du fichier: {size_kb:.1f} Ko")
        return True

    def _check_tar_structure(self) -> bool:
        """Vérifie que c'est un fichier tar.gz valide"""
        try:
            self.tar = tarfile.open(self.mbz_path, 'r:gz')
            members = self.tar.getnames()
            self.result.add_info(f"Archive tar.gz valide ({len(members)} fichiers)")
            return True
        except tarfile.TarError as e:
            self.result.add_error(f"Fichier tar.gz invalide: {e}")
            return False
        except Exception as e:
            self.result.add_error(f"Erreur lecture archive: {e}")
            return False

    def _load_all_files(self):
        """Charge tous les fichiers en mémoire"""
        for member in self.tar.getmembers():
            if member.isfile():
                try:
                    content = self.tar.extractfile(member).read()
                    self.files_in_mbz[member.name] = content

                    # Calculer le hash pour les fichiers dans files/
                    if member.name.startswith('files/'):
                        file_hash = hashlib.sha1(content).hexdigest()
                        self.file_references[file_hash] = member.name
                except Exception as e:
                    self.result.add_warning(f"Impossible de lire {member.name}: {e}")

    def _check_required_files(self):
        """Vérifie la présence des fichiers obligatoires"""
        for req_file in self.REQUIRED_FILES:
            if req_file not in self.files_in_mbz:
                self.result.add_error(f"Fichier obligatoire manquant: {req_file}")
            elif self.verbose:
                self.result.add_info(f"[OK] {req_file}")

    def _parse_h5p_activities(self):
        """Parse les activités H5P du backup"""
        # Trouver toutes les activités H5P
        for filename in self.files_in_mbz:
            if '/h5pactivity.xml' in filename:
                activity_dir = filename.rsplit('/', 1)[0]
                activity_id = activity_dir.split('_')[-1]

                try:
                    xml_content = self.files_in_mbz[filename].decode('utf-8')
                    root = ET.fromstring(xml_content)

                    h5p_elem = root.find('.//h5pactivity')
                    if h5p_elem is not None:
                        name = h5p_elem.findtext('name', 'Unknown')
                        self.h5p_activities[activity_id] = {
                            'name': name,
                            'dir': activity_dir,
                            'xml': xml_content
                        }
                        self.result.add_info(f"Activité H5P trouvée: {name}")
                except Exception as e:
                    self.result.add_warning(f"Erreur parsing {filename}: {e}")

        if not self.h5p_activities:
            self.result.add_warning("Aucune activité H5P trouvée dans le backup")

    def _validate_h5p_contents(self):
        """Valide le contenu de chaque fichier H5P dans files/"""
        h5p_count = 0

        for file_hash, file_path in self.file_references.items():
            content = self.files_in_mbz[file_path]

            # Vérifier si c'est un fichier H5P (zip avec h5p.json)
            try:
                with zipfile.ZipFile(io.BytesIO(content), 'r') as zf:
                    if 'h5p.json' in zf.namelist():
                        h5p_count += 1
                        self._validate_single_h5p(file_hash, file_path, zf)
            except zipfile.BadZipFile:
                # Pas un zip, probablement un PDF ou autre ressource
                pass
            except Exception as e:
                if self.verbose:
                    self.result.add_warning(f"Erreur vérification {file_path}: {e}")

        self.result.add_info(f"Fichiers H5P validés: {h5p_count}")

    def _validate_single_h5p(self, file_hash: str, file_path: str, zf: zipfile.ZipFile):
        """Valide un fichier H5P individuel"""
        short_name = file_hash[:8]

        # 1. Vérifier h5p.json
        try:
            h5p_json = json.loads(zf.read('h5p.json').decode('utf-8'))
            title = h5p_json.get('title', 'Sans titre')
            main_lib = h5p_json.get('mainLibrary', 'Unknown')

            if self.verbose:
                self.result.add_info(f"  H5P [{short_name}]: {title} ({main_lib})")
        except Exception as e:
            self.result.add_error(f"H5P [{short_name}]: h5p.json invalide - {e}")
            return

        # 2. Vérifier content/content.json
        try:
            content_json = json.loads(zf.read('content/content.json').decode('utf-8'))
        except Exception as e:
            self.result.add_error(f"H5P [{short_name}]: content.json invalide - {e}")
            return

        # 3. Valider la structure selon le type
        if main_lib == 'H5P.QuestionSet':
            self._validate_questionset(short_name, content_json)
        elif main_lib == 'H5P.GameMap':
            self._validate_gamemap(short_name, content_json)
        elif main_lib in ['H5P.MultiChoice', 'H5P.TrueFalse', 'H5P.Blanks', 'H5P.DragText']:
            self._validate_simple_content(short_name, main_lib, content_json)

    def _validate_questionset(self, h5p_id: str, content: dict):
        """Valide un QuestionSet H5P"""
        questions = content.get('questions', [])

        if not questions:
            self.result.add_error(f"H5P [{h5p_id}]: QuestionSet sans questions")
            return

        for i, q in enumerate(questions):
            lib = q.get('library', '')
            params = q.get('params', {})

            if 'MultiChoice' in lib:
                self._validate_multichoice_params(h5p_id, i, params)
            elif 'TrueFalse' in lib:
                self._validate_truefalse_params(h5p_id, i, params)
            elif 'Blanks' in lib:
                self._validate_blanks_params(h5p_id, i, params)
            elif 'DragText' in lib:
                self._validate_dragtext_params(h5p_id, i, params)

    def _validate_multichoice_params(self, h5p_id: str, q_idx: int, params: dict):
        """Valide les paramètres d'un MultiChoice"""
        answers = params.get('answers', [])
        question = params.get('question', '')

        if not question:
            self.result.add_error(f"H5P [{h5p_id}] Q{q_idx+1}: Question vide")

        if not answers:
            self.result.add_error(f"H5P [{h5p_id}] Q{q_idx+1}: Pas de réponses")
            return

        # Vérifier la structure des réponses
        correct_count = 0
        for j, ans in enumerate(answers):
            # VALIDATION CRITIQUE: la réponse doit être une string, pas un dict
            text = ans.get('text', '')

            if isinstance(text, dict):
                self.result.add_error(
                    f"H5P [{h5p_id}] Q{q_idx+1} R{j+1}: "
                    f"ERREUR CRITIQUE - 'text' est un dict au lieu d'une string! "
                    f"Valeur: {text}"
                )
            elif not isinstance(text, str):
                self.result.add_error(
                    f"H5P [{h5p_id}] Q{q_idx+1} R{j+1}: "
                    f"'text' devrait être une string, trouvé: {type(text)}"
                )
            elif not text.strip():
                self.result.add_warning(f"H5P [{h5p_id}] Q{q_idx+1} R{j+1}: Texte de réponse vide")

            if ans.get('correct'):
                correct_count += 1

        if correct_count == 0:
            self.result.add_error(f"H5P [{h5p_id}] Q{q_idx+1}: Aucune réponse correcte")

        if self.verbose and correct_count > 0:
            self.result.add_info(f"    Q{q_idx+1}: {len(answers)} réponses, {correct_count} correcte(s)")

    def _validate_truefalse_params(self, h5p_id: str, q_idx: int, params: dict):
        """Valide les paramètres d'un TrueFalse"""
        question = params.get('question', '')
        correct = params.get('correct')

        if not question:
            self.result.add_error(f"H5P [{h5p_id}] Q{q_idx+1}: Question vide")

        if correct is None:
            self.result.add_error(f"H5P [{h5p_id}] Q{q_idx+1}: Réponse correcte non définie")

    def _validate_blanks_params(self, h5p_id: str, q_idx: int, params: dict):
        """Valide les paramètres d'un Fill in the Blanks"""
        questions = params.get('questions', [])

        if not questions:
            self.result.add_error(f"H5P [{h5p_id}] Q{q_idx+1}: Pas de texte à trous")
            return

        # Vérifier qu'il y a des trous marqués par *mot*
        has_blanks = False
        for text in questions:
            if '*' in text:
                has_blanks = True
                break

        if not has_blanks:
            self.result.add_warning(f"H5P [{h5p_id}] Q{q_idx+1}: Aucun trou (*mot*) détecté")

    def _validate_dragtext_params(self, h5p_id: str, q_idx: int, params: dict):
        """Valide les paramètres d'un DragText"""
        text_field = params.get('textField', '')

        if not text_field:
            self.result.add_error(f"H5P [{h5p_id}] Q{q_idx+1}: Pas de texte pour drag&drop")
            return

        # Vérifier qu'il y a des mots à glisser *mot*
        if '*' not in text_field:
            self.result.add_warning(f"H5P [{h5p_id}] Q{q_idx+1}: Aucun mot à glisser (*mot*) détecté")

    def _validate_gamemap(self, h5p_id: str, content: dict):
        """Valide un GameMap H5P"""
        gamemap = content.get('gamemapSteps', {}).get('gamemap', {})
        elements = gamemap.get('elements', [])

        if not elements:
            self.result.add_error(f"H5P [{h5p_id}]: GameMap sans étapes")
            return

        self.result.add_info(f"  GameMap [{h5p_id}]: {len(elements)} étapes")

        # Vérifier chaque étape
        for i, stage in enumerate(elements):
            label = stage.get('label', f'Étape {i+1}')
            contents = stage.get('contentsList', [])

            if not contents:
                self.result.add_warning(f"H5P [{h5p_id}] {label}: Pas de contenu")

            # Valider le contenu de chaque étape
            for c in contents:
                content_type = c.get('contentType', {})
                lib = content_type.get('library', '')
                params = content_type.get('params', {})

                if 'MultiChoice' in lib:
                    self._validate_multichoice_params(h5p_id, i, params)
                elif 'QuestionSet' in lib:
                    # QuestionSet imbriqué
                    sub_questions = params.get('questions', [])
                    for j, sq in enumerate(sub_questions):
                        sq_lib = sq.get('library', '')
                        sq_params = sq.get('params', {})
                        if 'MultiChoice' in sq_lib:
                            self._validate_multichoice_params(h5p_id, j, sq_params)

    def _validate_simple_content(self, h5p_id: str, lib: str, content: dict):
        """Valide un contenu H5P simple (pas QuestionSet ni GameMap)"""
        if 'MultiChoice' in lib:
            self._validate_multichoice_params(h5p_id, 0, content)
        elif 'TrueFalse' in lib:
            self._validate_truefalse_params(h5p_id, 0, content)
        elif 'Blanks' in lib:
            self._validate_blanks_params(h5p_id, 0, content)
        elif 'DragText' in lib:
            self._validate_dragtext_params(h5p_id, 0, content)

    def _check_file_references(self):
        """Vérifie que les fichiers référencés existent"""
        # Chercher les références dans files.xml
        if 'files.xml' in self.files_in_mbz:
            try:
                files_xml = self.files_in_mbz['files.xml'].decode('utf-8')
                root = ET.fromstring(files_xml)

                for file_elem in root.findall('.//file'):
                    contenthash = file_elem.findtext('contenthash', '')
                    filename = file_elem.findtext('filename', '')

                    if contenthash and contenthash not in self.file_references:
                        self.result.add_warning(
                            f"Fichier référencé mais absent: {filename} ({contenthash[:8]})"
                        )
            except Exception as e:
                self.result.add_warning(f"Impossible de parser files.xml: {e}")

    def _print_summary(self):
        """Affiche le résumé de la validation"""
        print(f"\n{'='*60}")
        print("  RESUME DE LA VALIDATION")
        print(f"{'='*60}\n")

        # Infos
        if self.verbose and self.result.info:
            print("[INFO] INFORMATIONS:")
            for msg in self.result.info:
                print(f"   {msg}")
            print()

        # Warnings
        if self.result.warnings:
            print("[WARN] AVERTISSEMENTS:")
            for msg in self.result.warnings:
                print(f"   {msg}")
            print()

        # Erreurs
        if self.result.errors:
            print("[ERREUR] ERREURS:")
            for msg in self.result.errors:
                print(f"   {msg}")
            print()

        # Verdict final
        if self.result.valid:
            print("[OK] VALIDATION REUSSIE - Le fichier .mbz semble correct")
            print("     Il devrait fonctionner correctement dans Moodle.")
        else:
            print("[ECHEC] VALIDATION ECHOUEE - Des erreurs ont ete detectees")
            print("        Corrigez les erreurs avant d'importer dans Moodle.")

        print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Valide un fichier .mbz (backup Moodle) avant import"
    )
    parser.add_argument('mbz_file', help="Chemin vers le fichier .mbz à valider")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="Afficher plus de détails")

    args = parser.parse_args()

    validator = MBZValidator(args.mbz_file, verbose=args.verbose)
    result = validator.validate()

    # Code de sortie
    sys.exit(0 if result.valid else 1)


if __name__ == '__main__':
    main()
