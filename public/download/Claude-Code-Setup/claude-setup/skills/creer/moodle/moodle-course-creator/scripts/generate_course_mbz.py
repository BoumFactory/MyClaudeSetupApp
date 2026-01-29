#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur de cours Moodle complets (.mbz)
Permet de creer un cours avec sections, fichiers PDF, quiz et activites.

Usage:
    python generate_course_mbz.py --config cours_config.json --output mon_cours.mbz
"""

import os
import sys
import json
import tarfile
import gzip
import shutil
import tempfile
import hashlib
from datetime import datetime
from pathlib import Path
import argparse
from typing import List, Dict, Optional
import mimetypes


class MoodleCourseGenerator:
    """Generateur de cours Moodle complets avec fichiers et quiz"""

    # Extensions a exclure automatiquement
    EXCLUDED_EXTENSIONS = {
        '.tex', '.aux', '.log', '.out', '.toc', '.synctex.gz', '.synctex',
        '.comp', '.voc', '.listing', '.bak', '.tmp', '.fls', '.fdb_latexmk',
        '.bbl', '.blg', '.nav', '.snm', '.vrb'
    }
    # Dossiers a exclure
    EXCLUDED_DIRS = {'Sources', 'source', 'src', 'backup', '__pycache__', '.git', 'Ressources', 'ressources'}

    def __init__(self, course_fullname: str, course_shortname: str, settings: Dict = None):
        self.course_fullname = course_fullname
        self.course_shortname = course_shortname
        self.timestamp = int(datetime.now().timestamp())
        self.settings = settings or {}

        # Compteurs pour les IDs
        self.section_counter = 0
        self.activity_counter = 0
        self.file_counter = 0
        self.question_counter = 0
        self.answer_counter = 0

        # Stockage des elements
        self.sections: List[Dict] = []
        self.files_index: List[Dict] = []  # Index des fichiers pour files.xml
        self.files_content: Dict[str, bytes] = {}  # hash -> contenu binaire

    @classmethod
    def is_valid_file(cls, filepath: str) -> bool:
        """Verifie si un fichier doit etre inclus (exclut les sources LaTeX, etc.)"""
        path = Path(filepath)
        # Verifier l'extension
        if path.suffix.lower() in cls.EXCLUDED_EXTENSIONS:
            return False
        # Verifier si dans un dossier exclu
        for part in path.parts:
            if part in cls.EXCLUDED_DIRS:
                return False
        return True

    def _escape_xml(self, text: str) -> str:
        """Echappe les caracteres speciaux XML"""
        if text is None:
            return ""
        return (str(text)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

    def _compute_file_hash(self, content: bytes) -> str:
        """Calcule le hash SHA1 d'un contenu"""
        return hashlib.sha1(content).hexdigest()

    def _add_file_to_index(self, filepath: str, content: bytes, component: str,
                           filearea: str, itemid: int, contextid: int) -> Dict:
        """Ajoute un fichier a l'index et retourne ses metadonnees"""
        contenthash = self._compute_file_hash(content)
        filename = os.path.basename(filepath)

        # Determiner le mimetype
        mimetype, _ = mimetypes.guess_type(filename)
        if mimetype is None:
            # Types speciaux non reconnus par mimetypes
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.h5p':
                mimetype = "application/zip"  # H5P est un format ZIP
            else:
                mimetype = "application/octet-stream"

        self.file_counter += 1
        file_info = {
            'id': self.file_counter,
            'contenthash': contenthash,
            'contextid': contextid,
            'component': component,
            'filearea': filearea,
            'itemid': itemid,
            'filepath': '/',
            'filename': filename,
            'filesize': len(content),
            'mimetype': mimetype,
            'timecreated': self.timestamp,
            'timemodified': self.timestamp,
        }

        self.files_index.append(file_info)
        self.files_content[contenthash] = content

        return file_info

    def add_section(self, name: str, summary: str = "", visible: bool = False) -> int:
        """
        Ajoute une section au cours

        Args:
            name: Nom de la section
            summary: Description HTML de la section
            visible: Si True, la section est visible (defaut: False = cache)

        Returns:
            ID de la section creee
        """
        self.section_counter += 1
        section = {
            'id': self.section_counter,
            'number': self.section_counter,
            'name': name,
            'summary': summary,
            'visible': 1 if visible else 0,
            'activities': []
        }
        self.sections.append(section)
        return self.section_counter

    def add_file_resource(self, section_id: int, name: str, filepath: str,
                          description: str = "", visible: bool = False) -> int:
        """
        Ajoute un fichier (PDF, etc.) a une section

        Args:
            section_id: ID de la section
            name: Nom affiche de la ressource
            filepath: Chemin vers le fichier local
            description: Description de la ressource
            visible: Visibilite (defaut: cache)

        Returns:
            ID de l'activite creee
        """
        # Lire le fichier
        with open(filepath, 'rb') as f:
            content = f.read()

        self.activity_counter += 1
        activity_id = self.activity_counter
        contextid = 1000 + activity_id  # Context unique pour chaque activite

        # Ajouter le fichier a l'index
        file_info = self._add_file_to_index(
            filepath, content,
            component='mod_resource',
            filearea='content',
            itemid=0,
            contextid=contextid
        )

        activity = {
            'id': activity_id,
            'type': 'resource',
            'name': name,
            'description': description,
            'visible': 1 if visible else 0,
            'contextid': contextid,
            'file_info': file_info,
            'section_id': section_id  # Reference a la section
        }

        # Trouver la section et ajouter l'activite
        for section in self.sections:
            if section['id'] == section_id:
                activity['section_number'] = section['number']
                section['activities'].append(activity)
                break

        return activity_id

    def add_page(self, section_id: int, name: str, content: str,
                 visible: bool = False) -> int:
        """
        Ajoute une page HTML a une section

        Args:
            section_id: ID de la section
            name: Titre de la page
            content: Contenu HTML de la page
            visible: Visibilite

        Returns:
            ID de l'activite creee
        """
        self.activity_counter += 1
        activity_id = self.activity_counter

        activity = {
            'id': activity_id,
            'type': 'page',
            'name': name,
            'content': content,
            'visible': 1 if visible else 0,
            'contextid': 1000 + activity_id,
            'section_id': section_id
        }

        for section in self.sections:
            if section['id'] == section_id:
                activity['section_number'] = section['number']
                section['activities'].append(activity)
                break

        return activity_id

    def add_quiz(self, section_id: int, name: str, intro: str,
                 questions: List[Dict], visible: bool = False) -> int:
        """
        Ajoute un quiz avec questions Cloze

        Args:
            section_id: ID de la section
            name: Nom du quiz
            intro: Introduction du quiz (HTML)
            questions: Liste de questions (format du generateur precedent)
            visible: Visibilite

        Returns:
            ID du quiz cree
        """
        self.activity_counter += 1
        quiz_id = self.activity_counter
        contextid = 1000 + quiz_id

        # Compteur pour question_bank_entry de CE quiz
        # Chaque quiz a ses propres entries commencant a 1
        quiz_entry_counter = 0

        # Traiter les questions
        processed_questions = []
        for q in questions:
            quiz_entry_counter += 1
            # L'ID d'entree dans la banque de questions - unique par quiz
            entry_id = quiz_id * 1000 + quiz_entry_counter
            self.question_counter += 1
            question_id = self.question_counter

            # Construire la syntaxe CLOZE
            if q.get('type') == 'multichoice':
                cloze_parts = []
                for i, opt in enumerate(q['options']):
                    prefix = "=" if i == q['correct_index'] else "~"
                    fb = q.get('feedbacks', [""] * len(q['options']))[i]
                    fb_str = f"#{fb}" if fb else ""
                    cloze_parts.append(f"{prefix}{opt}{fb_str}")
                cloze_text = "{1:MULTICHOICE:" + "~".join(cloze_parts) + "}"
            elif q.get('type') == 'numerical':
                tol = q.get('tolerance', 0)
                if tol > 0:
                    cloze_text = f"{{1:NUMERICAL:={q['correct_value']}:{tol}}}"
                else:
                    cloze_text = f"{{1:NUMERICAL:={q['correct_value']}}}"
            elif q.get('type') == 'shortanswer':
                answers = "~".join([f"={a}" for a in q['correct_answers']])
                cloze_text = "{1:SHORTANSWER:" + answers + "}"
            else:
                cloze_text = "{1:SHORTANSWER:=}"

            processed_questions.append({
                'entry_id': entry_id,  # ID dans question_bank_entries
                'question_id': question_id,  # ID de la question
                'name': q['name'],
                'text': q['text'],
                'general_feedback': q.get('general_feedback', ''),
                'cloze_text': cloze_text,
                'original': q
            })

        activity = {
            'id': quiz_id,
            'type': 'quiz',
            'name': name,
            'intro': intro,
            'visible': 1 if visible else 0,
            'contextid': contextid,
            'questions': processed_questions,
            'section_id': section_id
        }

        for section in self.sections:
            if section['id'] == section_id:
                activity['section_number'] = section['number']
                section['activities'].append(activity)
                break

        return quiz_id

    def add_h5p(self, section_id: int, name: str, intro: str = "",
                h5p_file_path: str = None, h5p_content: bytes = None,
                questions: List[Dict] = None, h5p_type: str = "questionset",
                visible: bool = False) -> int:
        """
        Ajoute une activite H5P

        Args:
            section_id: ID de la section
            name: Nom de l'activite
            intro: Introduction (HTML)
            h5p_file_path: Chemin vers un fichier .h5p existant
            h5p_content: Contenu binaire d'un fichier .h5p
            questions: Liste de questions (pour generation automatique)
            h5p_type: Type H5P a generer ("questionset" ou "singlechoiceset")
            visible: Visibilite

        Returns:
            ID de l'activite creee
        """
        self.activity_counter += 1
        activity_id = self.activity_counter
        contextid = 1000 + activity_id

        # Obtenir le contenu H5P
        if h5p_file_path and os.path.exists(h5p_file_path):
            with open(h5p_file_path, 'rb') as f:
                h5p_data = f.read()
            h5p_filename = os.path.basename(h5p_file_path)
        elif h5p_content:
            h5p_data = h5p_content
            h5p_filename = f"{name.replace(' ', '_')}.h5p"
        elif questions:
            # Generer H5P a partir des questions
            try:
                from h5p_generator import convert_quiz_to_h5p
                h5p_data = convert_quiz_to_h5p(questions, name, h5p_type)
            except ImportError:
                # Fallback: charger depuis le meme dossier
                import importlib.util
                script_dir = os.path.dirname(os.path.abspath(__file__))
                spec = importlib.util.spec_from_file_location("h5p_generator",
                    os.path.join(script_dir, "h5p_generator.py"))
                h5p_gen = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(h5p_gen)
                h5p_data = h5p_gen.convert_quiz_to_h5p(questions, name, h5p_type)
            h5p_filename = f"{name.replace(' ', '_')}.h5p"
        else:
            raise ValueError("Il faut fournir h5p_file_path, h5p_content, ou questions")

        # Ajouter le fichier H5P a l'index
        file_info = self._add_file_to_index(
            h5p_filename, h5p_data,
            'mod_h5pactivity', 'package', 0, contextid
        )

        activity = {
            'id': activity_id,
            'type': 'h5pactivity',
            'name': name,
            'intro': intro,
            'visible': 1 if visible else 0,
            'contextid': contextid,
            'h5p_file_info': file_info,
            'section_id': section_id
        }

        for section in self.sections:
            if section['id'] == section_id:
                activity['section_number'] = section['number']
                section['activities'].append(activity)
                break

        return activity_id

    def _generate_moodle_backup_xml(self) -> str:
        """Genere moodle_backup.xml"""
        # Lister toutes les activites
        activities_xml = ""
        for section in self.sections:
            for activity in section['activities']:
                activities_xml += f'''        <activity>
          <moduleid>{activity['id']}</moduleid>
          <sectionid>{section['id']}</sectionid>
          <modulename>{activity['type']}</modulename>
          <title>{self._escape_xml(activity['name'])}</title>
          <directory>activities/{activity['type']}_{activity['id']}</directory>
          <insubsection></insubsection>
        </activity>
'''

        # Lister les settings des activites
        activity_settings = ""
        for section in self.sections:
            for activity in section['activities']:
                activity_settings += f'''      <setting>
        <level>activity</level>
        <activity>{activity['type']}_{activity['id']}</activity>
        <name>{activity['type']}_{activity['id']}_included</name>
        <value>1</value>
      </setting>
      <setting>
        <level>activity</level>
        <activity>{activity['type']}_{activity['id']}</activity>
        <name>{activity['type']}_{activity['id']}_userinfo</name>
        <value>0</value>
      </setting>
'''

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<moodle_backup>
  <information>
    <name>{self._escape_xml(self.course_shortname)}.mbz</name>
    <moodle_version>2024100700</moodle_version>
    <moodle_release>4.5</moodle_release>
    <backup_version>2024100700</backup_version>
    <backup_release>4.5</backup_release>
    <backup_date>{self.timestamp}</backup_date>
    <mnet_remoteusers>0</mnet_remoteusers>
    <include_files>1</include_files>
    <include_file_references_to_external_content>0</include_file_references_to_external_content>
    <original_wwwroot>https://localhost</original_wwwroot>
    <original_site_identifier_hash>generated_course_backup</original_site_identifier_hash>
    <original_course_id>1</original_course_id>
    <original_course_format>topics</original_course_format>
    <original_course_fullname>{self._escape_xml(self.course_fullname)}</original_course_fullname>
    <original_course_shortname>{self._escape_xml(self.course_shortname)}</original_course_shortname>
    <original_course_startdate>{self.timestamp}</original_course_startdate>
    <original_course_enddate>0</original_course_enddate>
    <original_course_contextid>1</original_course_contextid>
    <original_system_contextid>1</original_system_contextid>
    <details>
      <detail backup_id="course_backup_001">
        <type>course</type>
        <format>moodle2</format>
        <interactive>1</interactive>
        <mode>10</mode>
        <execution>1</execution>
        <executiontime>0</executiontime>
      </detail>
    </details>
    <contents>
      <activities>
{activities_xml}      </activities>
      <sections>
{self._generate_sections_content_list()}      </sections>
      <course>
        <courseid>1</courseid>
        <title>{self._escape_xml(self.course_fullname)}</title>
        <directory>course</directory>
      </course>
    </contents>
    <settings>
      <setting><level>root</level><name>filename</name><value>{self._escape_xml(self.course_shortname)}.mbz</value></setting>
      <setting><level>root</level><name>users</name><value>0</value></setting>
      <setting><level>root</level><name>anonymize</name><value>0</value></setting>
      <setting><level>root</level><name>role_assignments</name><value>0</value></setting>
      <setting><level>root</level><name>activities</name><value>1</value></setting>
      <setting><level>root</level><name>blocks</name><value>0</value></setting>
      <setting><level>root</level><name>files</name><value>1</value></setting>
      <setting><level>root</level><name>filters</name><value>1</value></setting>
      <setting><level>root</level><name>comments</name><value>0</value></setting>
      <setting><level>root</level><name>badges</name><value>0</value></setting>
      <setting><level>root</level><name>calendarevents</name><value>0</value></setting>
      <setting><level>root</level><name>userscompletion</name><value>0</value></setting>
      <setting><level>root</level><name>logs</name><value>0</value></setting>
      <setting><level>root</level><name>grade_histories</name><value>0</value></setting>
      <setting><level>root</level><name>questionbank</name><value>1</value></setting>
      <setting><level>root</level><name>groups</name><value>0</value></setting>
      <setting><level>root</level><name>competencies</name><value>0</value></setting>
{activity_settings}    </settings>
  </information>
</moodle_backup>'''

    def _generate_sections_content_list(self) -> str:
        """Genere la liste des sections pour moodle_backup.xml"""
        sections_xml = ""
        for section in self.sections:
            sections_xml += f'''        <section>
          <sectionid>{section['id']}</sectionid>
          <title>{self._escape_xml(section['name'])}</title>
          <directory>sections/section_{section['id']}</directory>
        </section>
'''
        return sections_xml

    def _generate_files_xml(self) -> str:
        """Genere files.xml avec tous les fichiers"""
        files_xml = ""
        for f in self.files_index:
            files_xml += f'''  <file id="{f['id']}">
    <contenthash>{f['contenthash']}</contenthash>
    <contextid>{f['contextid']}</contextid>
    <component>{f['component']}</component>
    <filearea>{f['filearea']}</filearea>
    <itemid>{f['itemid']}</itemid>
    <filepath>{f['filepath']}</filepath>
    <filename>{self._escape_xml(f['filename'])}</filename>
    <userid>1</userid>
    <filesize>{f['filesize']}</filesize>
    <mimetype>{f['mimetype']}</mimetype>
    <status>0</status>
    <timecreated>{f['timecreated']}</timecreated>
    <timemodified>{f['timemodified']}</timemodified>
    <source>{self._escape_xml(f['filename'])}</source>
    <author>Enseignant</author>
    <license>allrightsreserved</license>
    <sortorder>0</sortorder>
    <repositorytype>$@NULL@$</repositorytype>
    <repositoryid>$@NULL@$</repositoryid>
    <reference>$@NULL@$</reference>
  </file>
'''
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<files>
{files_xml}</files>'''

    def _generate_course_xml(self) -> str:
        """Genere course/course.xml avec les settings configurables"""
        # Recuperer les parametres avec valeurs par defaut
        course_format = self.settings.get('format', 'topics')
        course_summary = self.settings.get('summary', '<p>Cours genere automatiquement</p>')
        course_visible = 1 if self.settings.get('visible', True) else 0
        category_name = self.settings.get('category', 'Mathematiques')
        enable_completion = 1 if self.settings.get('enable_completion', False) else 0
        show_grades = 1 if self.settings.get('show_grades', True) else 0

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<course id="1" contextid="1">
  <shortname>{self._escape_xml(self.course_shortname)}</shortname>
  <fullname>{self._escape_xml(self.course_fullname)}</fullname>
  <idnumber></idnumber>
  <summary>{self._escape_xml(course_summary)}</summary>
  <summaryformat>1</summaryformat>
  <format>{course_format}</format>
  <showgrades>{show_grades}</showgrades>
  <newsitems>5</newsitems>
  <startdate>{self.timestamp}</startdate>
  <enddate>0</enddate>
  <marker>0</marker>
  <maxbytes>0</maxbytes>
  <legacyfiles>0</legacyfiles>
  <showreports>0</showreports>
  <visible>{course_visible}</visible>
  <groupmode>0</groupmode>
  <groupmodeforce>0</groupmodeforce>
  <defaultgroupingid>0</defaultgroupingid>
  <lang></lang>
  <theme></theme>
  <timecreated>{self.timestamp}</timecreated>
  <timemodified>{self.timestamp}</timemodified>
  <requested>0</requested>
  <showactivitydates>1</showactivitydates>
  <showcompletionconditions>1</showcompletionconditions>
  <pdfexportfont></pdfexportfont>
  <enablecompletion>{enable_completion}</enablecompletion>
  <completionnotify>0</completionnotify>
  <downloadcontent>0</downloadcontent>
  <cacherev>0</cacherev>
  <originalcourseid>$@NULL@$</originalcourseid>
  <category id="1">
    <name>{self._escape_xml(category_name)}</name>
    <description></description>
  </category>
  <tags>
  </tags>
  <customfields>
  </customfields>
  <courseformatoptions>
  </courseformatoptions>
</course>'''

    def _generate_section_xml(self, section: Dict) -> str:
        """Genere le XML d'une section"""
        # Sequence des activites dans cette section
        sequence = ",".join([str(a['id']) for a in section['activities']])

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<section id="{section['id']}">
  <number>{section['number']}</number>
  <name>{self._escape_xml(section['name'])}</name>
  <summary>{self._escape_xml(section['summary'])}</summary>
  <summaryformat>1</summaryformat>
  <sequence>{sequence}</sequence>
  <visible>{section['visible']}</visible>
  <availabilityjson>$@NULL@$</availabilityjson>
  <timemodified>{self.timestamp}</timemodified>
</section>'''

    def _generate_resource_xml(self, activity: Dict) -> str:
        """Genere le XML d'une ressource fichier"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<activity id="{activity['id']}" moduleid="{activity['id']}" modulename="resource" contextid="{activity['contextid']}">
  <resource id="{activity['id']}">
    <name>{self._escape_xml(activity['name'])}</name>
    <intro>{self._escape_xml(activity.get('description', ''))}</intro>
    <introformat>1</introformat>
    <tobemigrated>0</tobemigrated>
    <legacyfiles>0</legacyfiles>
    <legacyfileslast>$@NULL@$</legacyfileslast>
    <display>0</display>
    <displayoptions>a:1:{{s:10:"printintro";i:1;}}</displayoptions>
    <filterfiles>0</filterfiles>
    <revision>1</revision>
    <timemodified>{self.timestamp}</timemodified>
  </resource>
</activity>'''

    def _generate_page_xml(self, activity: Dict) -> str:
        """Genere le XML d'une page"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<activity id="{activity['id']}" moduleid="{activity['id']}" modulename="page" contextid="{activity['contextid']}">
  <page id="{activity['id']}">
    <name>{self._escape_xml(activity['name'])}</name>
    <intro></intro>
    <introformat>1</introformat>
    <content>{self._escape_xml(activity['content'])}</content>
    <contentformat>1</contentformat>
    <legacyfiles>0</legacyfiles>
    <legacyfileslast>$@NULL@$</legacyfileslast>
    <display>5</display>
    <displayoptions>a:2:{{s:12:"printheading";s:1:"1";s:10:"printintro";s:1:"0";}}</displayoptions>
    <revision>1</revision>
    <timemodified>{self.timestamp}</timemodified>
  </page>
</activity>'''

    def _generate_quiz_xml(self, activity: Dict) -> str:
        """Genere le XML d'un quiz"""
        num_questions = len(activity['questions'])

        # Generer les question_instances
        instances_xml = ""
        for i, q in enumerate(activity['questions']):
            instance_id = activity['id'] * 100 + i + 1
            ref_id = activity['id'] * 100 + i + 1
            instances_xml += f'''      <question_instance id="{instance_id}">
        <quizid>{activity['id']}</quizid>
        <slot>{i+1}</slot>
        <page>1</page>
        <displaynumber>$@NULL@$</displaynumber>
        <requireprevious>0</requireprevious>
        <maxmark>1.0000000</maxmark>
        <quizgradeitemid>$@NULL@$</quizgradeitemid>
        <question_reference id="{ref_id}">
          <usingcontextid>{activity['contextid']}</usingcontextid>
          <component>mod_quiz</component>
          <questionarea>slot</questionarea>
          <questionbankentryid>{q['entry_id']}</questionbankentryid>
          <version>$@NULL@$</version>
        </question_reference>
      </question_instance>
'''

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<activity id="{activity['id']}" moduleid="{activity['id']}" modulename="quiz" contextid="{activity['contextid']}">
  <quiz id="{activity['id']}">
    <name>{self._escape_xml(activity['name'])}</name>
    <intro>{self._escape_xml(activity['intro'])}</intro>
    <introformat>1</introformat>
    <timeopen>0</timeopen>
    <timeclose>0</timeclose>
    <timelimit>0</timelimit>
    <overduehandling>autosubmit</overduehandling>
    <graceperiod>0</graceperiod>
    <preferredbehaviour>immediatefeedback</preferredbehaviour>
    <canredoquestions>0</canredoquestions>
    <attempts_number>0</attempts_number>
    <attemptonlast>0</attemptonlast>
    <grademethod>1</grademethod>
    <decimalpoints>2</decimalpoints>
    <questiondecimalpoints>-1</questiondecimalpoints>
    <reviewattempt>69888</reviewattempt>
    <reviewcorrectness>69888</reviewcorrectness>
    <reviewmaxmarks>69888</reviewmaxmarks>
    <reviewmarks>69888</reviewmarks>
    <reviewspecificfeedback>69888</reviewspecificfeedback>
    <reviewgeneralfeedback>69888</reviewgeneralfeedback>
    <reviewrightanswer>69888</reviewrightanswer>
    <reviewoverallfeedback>4352</reviewoverallfeedback>
    <questionsperpage>{num_questions}</questionsperpage>
    <navmethod>free</navmethod>
    <shuffleanswers>1</shuffleanswers>
    <sumgrades>{num_questions}.00000</sumgrades>
    <grade>20.00000</grade>
    <timecreated>{self.timestamp}</timecreated>
    <timemodified>{self.timestamp}</timemodified>
    <password></password>
    <subnet></subnet>
    <browsersecurity>-</browsersecurity>
    <delay1>0</delay1>
    <delay2>0</delay2>
    <showuserpicture>0</showuserpicture>
    <showblocks>0</showblocks>
    <completionattemptsexhausted>0</completionattemptsexhausted>
    <completionminattempts>0</completionminattempts>
    <allowofflineattempts>0</allowofflineattempts>
    <subplugin_quizaccess_seb_quiz>
    </subplugin_quizaccess_seb_quiz>
    <quiz_grade_items>
    </quiz_grade_items>
    <question_instances>
{instances_xml}    </question_instances>
    <sections>
      <section id="1">
        <firstslot>1</firstslot>
        <heading>{self._escape_xml(activity['name'])}</heading>
        <shufflequestions>0</shufflequestions>
      </section>
    </sections>
    <feedbacks>
      <feedback id="1">
        <feedbacktext>&lt;p&gt;Quiz termine !&lt;/p&gt;</feedbacktext>
        <feedbacktextformat>1</feedbacktextformat>
        <mingrade>0.00000</mingrade>
        <maxgrade>21.00000</maxgrade>
      </feedback>
    </feedbacks>
    <overrides>
    </overrides>
    <grades>
    </grades>
    <attempts>
    </attempts>
  </quiz>
</activity>'''

    def _generate_h5pactivity_xml(self, activity: Dict) -> str:
        """Genere le XML d'une activite H5P"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<activity id="{activity['id']}" moduleid="{activity['id']}" modulename="h5pactivity" contextid="{activity['contextid']}">
  <h5pactivity id="{activity['id']}">
    <name>{self._escape_xml(activity['name'])}</name>
    <timecreated>{self.timestamp}</timecreated>
    <timemodified>{self.timestamp}</timemodified>
    <intro>{self._escape_xml(activity.get('intro', ''))}</intro>
    <introformat>1</introformat>
    <grade>100</grade>
    <displayoptions>0</displayoptions>
    <enabletracking>1</enabletracking>
    <grademethod>1</grademethod>
    <reviewmode>1</reviewmode>
    <attempts>
    </attempts>
  </h5pactivity>
</activity>'''

    def _generate_questions_xml(self) -> str:
        """Genere questions.xml global avec toutes les questions des quiz"""
        # Collecter toutes les questions avec leur contexte (quiz)
        quiz_questions = []
        for section in self.sections:
            for activity in section['activities']:
                if activity['type'] == 'quiz':
                    for q in activity['questions']:
                        quiz_questions.append({
                            'question': q,
                            'quiz_contextid': activity['contextid'],
                            'quiz_id': activity['id'],
                            'quiz_name': activity['name']
                        })

        if not quiz_questions:
            return '''<?xml version="1.0" encoding="UTF-8"?>
<question_categories>
</question_categories>'''

        # Generer les question_bank_entries - utiliser entry_id de chaque question
        entries_xml = ""
        answer_id = 1

        for qdata in quiz_questions:
            q = qdata['question']
            entry_id = q['entry_id']  # Utiliser l'ID genere dans add_quiz
            question_id = q['question_id']
            original = q['original']

            # Question Cloze (multianswer) avec entry_id correspondant au quiz
            entries_xml += f'''      <question_bank_entry id="{entry_id}">
        <questioncategoryid>2</questioncategoryid>
        <idnumber>$@NULL@$</idnumber>
        <ownerid>1</ownerid>
        <question_version>
          <question_versions id="{entry_id}">
            <version>1</version>
            <status>ready</status>
            <questions>
              <question id="{question_id}">
                <parent>0</parent>
                <name>{self._escape_xml(q['name'])}</name>
                <questiontext>&lt;p&gt;{self._escape_xml(q['text'])}&lt;/p&gt;</questiontext>
                <questiontextformat>1</questiontextformat>
                <generalfeedback>&lt;p&gt;{self._escape_xml(q['general_feedback'])}&lt;/p&gt;</generalfeedback>
                <generalfeedbackformat>1</generalfeedbackformat>
                <defaultmark>1.0000000</defaultmark>
                <penalty>0.3333333</penalty>
                <qtype>multianswer</qtype>
                <length>1</length>
                <stamp>localhost+q{question_id}</stamp>
                <timecreated>{self.timestamp}</timecreated>
                <timemodified>{self.timestamp}</timemodified>
                <createdby>1</createdby>
                <modifiedby>1</modifiedby>
                <plugin_qtype_multianswer_question>
                  <answers></answers>
                  <multianswer id="{entry_id}">
                    <question>{question_id}</question>
                    <sequence>{question_id + 1000}</sequence>
                  </multianswer>
                </plugin_qtype_multianswer_question>
                <plugin_qbank_comment_question><comments></comments></plugin_qbank_comment_question>
                <plugin_qbank_customfields_question><customfields></customfields></plugin_qbank_customfields_question>
                <question_hints></question_hints>
                <tags></tags>
              </question>
            </questions>
          </question_versions>
        </question_version>
      </question_bank_entry>
'''
            # Sous-question selon le type
            qtype = original.get('type', 'multichoice')
            sub_question_id = question_id + 1000
            sub_entry_id = entry_id + 10000  # Entry ID distinct pour la sous-question

            if qtype == 'multichoice':
                answers_xml = ""
                for i, opt in enumerate(original['options']):
                    fraction = "1.0000000" if i == original['correct_index'] else "0.0000000"
                    fb = original.get('feedbacks', [""] * len(original['options']))[i]
                    answers_xml += f'''                    <answer id="{answer_id}">
                      <answertext>{self._escape_xml(opt)}</answertext>
                      <answerformat>1</answerformat>
                      <fraction>{fraction}</fraction>
                      <feedback>{self._escape_xml(fb)}</feedback>
                      <feedbackformat>1</feedbackformat>
                    </answer>
'''
                    answer_id += 1

                entries_xml += f'''      <question_bank_entry id="{sub_entry_id}">
        <questioncategoryid>2</questioncategoryid>
        <idnumber>$@NULL@$</idnumber>
        <ownerid>1</ownerid>
        <question_version>
          <question_versions id="{sub_entry_id}">
            <version>1</version>
            <status>ready</status>
            <questions>
              <question id="{sub_question_id}">
                <parent>{question_id}</parent>
                <name>{self._escape_xml(q['name'])}</name>
                <questiontext>{self._escape_xml(q['cloze_text'])}</questiontext>
                <questiontextformat>1</questiontextformat>
                <generalfeedback></generalfeedback>
                <generalfeedbackformat>1</generalfeedbackformat>
                <defaultmark>1.0000000</defaultmark>
                <penalty>0.0000000</penalty>
                <qtype>multichoice</qtype>
                <length>1</length>
                <stamp>localhost+q{sub_question_id}</stamp>
                <timecreated>{self.timestamp}</timecreated>
                <timemodified>{self.timestamp}</timemodified>
                <createdby>1</createdby>
                <modifiedby>1</modifiedby>
                <plugin_qtype_multichoice_question>
                  <answers>
{answers_xml}                  </answers>
                  <multichoice id="{sub_entry_id}">
                    <layout>0</layout>
                    <single>1</single>
                    <shuffleanswers>0</shuffleanswers>
                    <correctfeedback></correctfeedback>
                    <correctfeedbackformat>1</correctfeedbackformat>
                    <partiallycorrectfeedback></partiallycorrectfeedback>
                    <partiallycorrectfeedbackformat>1</partiallycorrectfeedbackformat>
                    <incorrectfeedback></incorrectfeedback>
                    <incorrectfeedbackformat>1</incorrectfeedbackformat>
                    <answernumbering>0</answernumbering>
                    <shownumcorrect>0</shownumcorrect>
                    <showstandardinstruction>0</showstandardinstruction>
                  </multichoice>
                </plugin_qtype_multichoice_question>
                <plugin_qbank_comment_question><comments></comments></plugin_qbank_comment_question>
                <plugin_qbank_customfields_question><customfields></customfields></plugin_qbank_customfields_question>
                <question_hints></question_hints>
                <tags></tags>
              </question>
            </questions>
          </question_versions>
        </question_version>
      </question_bank_entry>
'''
            elif qtype == 'numerical':
                entries_xml += f'''      <question_bank_entry id="{sub_entry_id}">
        <questioncategoryid>2</questioncategoryid>
        <idnumber>$@NULL@$</idnumber>
        <ownerid>1</ownerid>
        <question_version>
          <question_versions id="{sub_entry_id}">
            <version>1</version>
            <status>ready</status>
            <questions>
              <question id="{sub_question_id}">
                <parent>{question_id}</parent>
                <name>{self._escape_xml(q['name'])}</name>
                <questiontext>{self._escape_xml(q['cloze_text'])}</questiontext>
                <questiontextformat>1</questiontextformat>
                <generalfeedback></generalfeedback>
                <generalfeedbackformat>1</generalfeedbackformat>
                <defaultmark>1.0000000</defaultmark>
                <penalty>0.0000000</penalty>
                <qtype>numerical</qtype>
                <length>1</length>
                <stamp>localhost+q{sub_question_id}</stamp>
                <timecreated>{self.timestamp}</timecreated>
                <timemodified>{self.timestamp}</timemodified>
                <createdby>1</createdby>
                <modifiedby>1</modifiedby>
                <plugin_qtype_numerical_question>
                  <answers>
                    <answer id="{answer_id}">
                      <answertext>{original['correct_value']}</answertext>
                      <answerformat>0</answerformat>
                      <fraction>1.0000000</fraction>
                      <feedback></feedback>
                      <feedbackformat>1</feedbackformat>
                    </answer>
                  </answers>
                  <numerical_records>
                    <numerical_record id="{answer_id}">
                      <answer>{answer_id}</answer>
                      <tolerance>{original.get('tolerance', 0)}</tolerance>
                    </numerical_record>
                  </numerical_records>
                  <numerical_options id="{sub_entry_id}">
                    <showunits>3</showunits>
                    <unitsleft>0</unitsleft>
                    <unitgradingtype>0</unitgradingtype>
                    <unitpenalty>0.1000000</unitpenalty>
                  </numerical_options>
                  <numerical_units></numerical_units>
                </plugin_qtype_numerical_question>
                <plugin_qbank_comment_question><comments></comments></plugin_qbank_comment_question>
                <plugin_qbank_customfields_question><customfields></customfields></plugin_qbank_customfields_question>
                <question_hints></question_hints>
                <tags></tags>
              </question>
            </questions>
          </question_versions>
        </question_version>
      </question_bank_entry>
'''
                answer_id += 1
            elif qtype == 'shortanswer':
                answers_xml = ""
                for ans in original['correct_answers']:
                    answers_xml += f'''                    <answer id="{answer_id}">
                      <answertext>{self._escape_xml(ans)}</answertext>
                      <answerformat>0</answerformat>
                      <fraction>1.0000000</fraction>
                      <feedback></feedback>
                      <feedbackformat>1</feedbackformat>
                    </answer>
'''
                    answer_id += 1

                entries_xml += f'''      <question_bank_entry id="{sub_entry_id}">
        <questioncategoryid>2</questioncategoryid>
        <idnumber>$@NULL@$</idnumber>
        <ownerid>1</ownerid>
        <question_version>
          <question_versions id="{sub_entry_id}">
            <version>1</version>
            <status>ready</status>
            <questions>
              <question id="{sub_question_id}">
                <parent>{question_id}</parent>
                <name>{self._escape_xml(q['name'])}</name>
                <questiontext>{self._escape_xml(q['cloze_text'])}</questiontext>
                <questiontextformat>1</questiontextformat>
                <generalfeedback></generalfeedback>
                <generalfeedbackformat>1</generalfeedbackformat>
                <defaultmark>1.0000000</defaultmark>
                <penalty>0.0000000</penalty>
                <qtype>shortanswer</qtype>
                <length>1</length>
                <stamp>localhost+q{sub_question_id}</stamp>
                <timecreated>{self.timestamp}</timecreated>
                <timemodified>{self.timestamp}</timemodified>
                <createdby>1</createdby>
                <modifiedby>1</modifiedby>
                <plugin_qtype_shortanswer_question>
                  <answers>
{answers_xml}                  </answers>
                  <shortanswer id="{sub_entry_id}">
                    <usecase>0</usecase>
                  </shortanswer>
                </plugin_qtype_shortanswer_question>
                <plugin_qbank_comment_question><comments></comments></plugin_qbank_comment_question>
                <plugin_qbank_customfields_question><customfields></customfields></plugin_qbank_customfields_question>
                <question_hints></question_hints>
                <tags></tags>
              </question>
            </questions>
          </question_versions>
        </question_version>
      </question_bank_entry>
'''

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<question_categories>
  <question_category id="1">
    <name>top</name>
    <contextid>1</contextid>
    <contextlevel>50</contextlevel>
    <contextinstanceid>1</contextinstanceid>
    <info></info>
    <infoformat>0</infoformat>
    <stamp>localhost+top</stamp>
    <parent>0</parent>
    <sortorder>0</sortorder>
    <idnumber>$@NULL@$</idnumber>
    <question_bank_entries>
    </question_bank_entries>
  </question_category>
  <question_category id="2">
    <name>{self._escape_xml(self.course_fullname)}</name>
    <contextid>1</contextid>
    <contextlevel>50</contextlevel>
    <contextinstanceid>1</contextinstanceid>
    <info>Banque de questions du cours</info>
    <infoformat>0</infoformat>
    <stamp>localhost+category</stamp>
    <parent>1</parent>
    <sortorder>999</sortorder>
    <idnumber>$@NULL@$</idnumber>
    <question_bank_entries>
{entries_xml}    </question_bank_entries>
  </question_category>
</question_categories>'''

    def _generate_module_xml(self, activity: Dict) -> str:
        """Genere module.xml pour une activite"""
        section_id = activity.get('section_id', 1)
        section_number = activity.get('section_number', 1)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<module id="{activity['id']}" version="2024100700">
  <modulename>{activity['type']}</modulename>
  <sectionid>{section_id}</sectionid>
  <sectionnumber>{section_number}</sectionnumber>
  <idnumber></idnumber>
  <added>{self.timestamp}</added>
  <score>0</score>
  <indent>0</indent>
  <visible>{activity['visible']}</visible>
  <visibleoncoursepage>1</visibleoncoursepage>
  <visibleold>1</visibleold>
  <groupmode>0</groupmode>
  <groupingid>0</groupingid>
  <completion>0</completion>
  <completiongradeitemnumber>$@NULL@$</completiongradeitemnumber>
  <completionpassgrade>0</completionpassgrade>
  <completionview>0</completionview>
  <completionexpected>0</completionexpected>
  <availability>$@NULL@$</availability>
  <showdescription>0</showdescription>
  <downloadcontent>1</downloadcontent>
  <lang></lang>
  <tags>
  </tags>
</module>'''

    def _generate_empty_xml(self, root_tag: str, content: str = "") -> str:
        """Genere un fichier XML minimal"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<{root_tag}>
{content}</{root_tag}>'''

    def generate_mbz(self, output_path: str) -> str:
        """
        Genere le fichier .mbz complet du cours

        Args:
            output_path: Chemin du fichier .mbz a creer

        Returns:
            Chemin absolu du fichier cree
        """
        if not self.sections:
            raise ValueError("Aucune section ajoutee. Utilisez add_section().")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Structure des dossiers
            course_dir = tmppath / "course"
            course_dir.mkdir()
            sections_dir = tmppath / "sections"
            sections_dir.mkdir()
            activities_dir = tmppath / "activities"
            activities_dir.mkdir()
            files_dir = tmppath / "files"
            files_dir.mkdir()

            # Fichiers racine
            (tmppath / "moodle_backup.xml").write_text(
                self._generate_moodle_backup_xml(), encoding='utf-8')
            (tmppath / "files.xml").write_text(
                self._generate_files_xml(), encoding='utf-8')
            (tmppath / "questions.xml").write_text(
                self._generate_questions_xml(), encoding='utf-8')

            # Fichiers vides necessaires
            (tmppath / "gradebook.xml").write_text(
                self._generate_empty_xml("gradebook",
                    "  <attributes></attributes>\n  <grade_categories></grade_categories>\n"
                    "  <grade_items></grade_items>\n  <grade_letters></grade_letters>\n"
                    "  <grade_settings></grade_settings>\n"), encoding='utf-8')
            (tmppath / "grade_history.xml").write_text(
                self._generate_empty_xml("grade_history", "  <grade_grades></grade_grades>\n"),
                encoding='utf-8')
            (tmppath / "groups.xml").write_text(
                self._generate_empty_xml("groups", "  <groupings></groupings>\n"),
                encoding='utf-8')
            (tmppath / "outcomes.xml").write_text(
                self._generate_empty_xml("outcomes_definition"), encoding='utf-8')
            (tmppath / "roles.xml").write_text(
                self._generate_empty_xml("roles_definition"), encoding='utf-8')
            (tmppath / "scales.xml").write_text(
                self._generate_empty_xml("scales_definition"), encoding='utf-8')
            (tmppath / "badges.xml").write_text(
                self._generate_empty_xml("badges"), encoding='utf-8')
            (tmppath / "completion.xml").write_text(
                self._generate_empty_xml("course_completion"), encoding='utf-8')

            # Dossier course
            (course_dir / "course.xml").write_text(
                self._generate_course_xml(), encoding='utf-8')
            (course_dir / "inforef.xml").write_text(
                self._generate_empty_xml("inforef"), encoding='utf-8')
            (course_dir / "roles.xml").write_text(
                self._generate_empty_xml("roles",
                    "  <role_overrides></role_overrides>\n  <role_assignments></role_assignments>\n"),
                encoding='utf-8')
            (course_dir / "enrolments.xml").write_text(
                self._generate_empty_xml("enrolments", "  <enrols></enrols>\n"),
                encoding='utf-8')
            (course_dir / "filters.xml").write_text(
                self._generate_empty_xml("filters",
                    "  <filter_actives></filter_actives>\n  <filter_configs></filter_configs>\n"),
                encoding='utf-8')
            (course_dir / "competencies.xml").write_text(
                self._generate_empty_xml("course_competencies",
                    "  <competencies></competencies>\n  <usercomps></usercomps>\n"),
                encoding='utf-8')
            (course_dir / "completiondefaults.xml").write_text(
                self._generate_empty_xml("course_completion_defaults",
                    "  <course_completion_defaults></course_completion_defaults>\n"),
                encoding='utf-8')
            (course_dir / "contentbank.xml").write_text(
                self._generate_empty_xml("contents"), encoding='utf-8')
            (course_dir / "calendar.xml").write_text(
                self._generate_empty_xml("events"), encoding='utf-8')

            # Sections
            for section in self.sections:
                section_path = sections_dir / f"section_{section['id']}"
                section_path.mkdir()
                (section_path / "section.xml").write_text(
                    self._generate_section_xml(section), encoding='utf-8')
                (section_path / "inforef.xml").write_text(
                    self._generate_empty_xml("inforef"), encoding='utf-8')

            # Activites
            for section in self.sections:
                for activity in section['activities']:
                    activity_path = activities_dir / f"{activity['type']}_{activity['id']}"
                    activity_path.mkdir()

                    # Generer le XML principal selon le type
                    if activity['type'] == 'resource':
                        (activity_path / "resource.xml").write_text(
                            self._generate_resource_xml(activity), encoding='utf-8')
                    elif activity['type'] == 'page':
                        (activity_path / "page.xml").write_text(
                            self._generate_page_xml(activity), encoding='utf-8')
                    elif activity['type'] == 'quiz':
                        (activity_path / "quiz.xml").write_text(
                            self._generate_quiz_xml(activity), encoding='utf-8')
                    elif activity['type'] == 'h5pactivity':
                        (activity_path / "h5pactivity.xml").write_text(
                            self._generate_h5pactivity_xml(activity), encoding='utf-8')

                    # Fichiers communs
                    (activity_path / "module.xml").write_text(
                        self._generate_module_xml(activity), encoding='utf-8')

                    # inforef avec reference aux fichiers si c'est une resource ou h5p
                    if activity['type'] == 'resource':
                        file_info = activity.get('file_info', {})
                        inforef_content = f'''  <fileref>
    <file>
      <id>{file_info.get('id', 1)}</id>
    </file>
  </fileref>
'''
                        (activity_path / "inforef.xml").write_text(
                            self._generate_empty_xml("inforef", inforef_content),
                            encoding='utf-8')
                    elif activity['type'] == 'h5pactivity':
                        file_info = activity.get('h5p_file_info', {})
                        inforef_content = f'''  <fileref>
    <file>
      <id>{file_info.get('id', 1)}</id>
    </file>
  </fileref>
'''
                        (activity_path / "inforef.xml").write_text(
                            self._generate_empty_xml("inforef", inforef_content),
                            encoding='utf-8')
                    else:
                        (activity_path / "inforef.xml").write_text(
                            self._generate_empty_xml("inforef"), encoding='utf-8')

                    (activity_path / "grades.xml").write_text(
                        self._generate_empty_xml("activity_gradebook",
                            "  <grade_items></grade_items>\n  <grade_letters></grade_letters>\n"),
                        encoding='utf-8')
                    (activity_path / "grade_history.xml").write_text(
                        self._generate_empty_xml("grade_history",
                            "  <grade_grades></grade_grades>\n"), encoding='utf-8')
                    (activity_path / "roles.xml").write_text(
                        self._generate_empty_xml("roles",
                            "  <role_overrides></role_overrides>\n  <role_assignments></role_assignments>\n"),
                        encoding='utf-8')
                    (activity_path / "filters.xml").write_text(
                        self._generate_empty_xml("filters",
                            "  <filter_actives></filter_actives>\n  <filter_configs></filter_configs>\n"),
                        encoding='utf-8')
                    (activity_path / "competencies.xml").write_text(
                        self._generate_empty_xml("course_module_competencies",
                            "  <competencies></competencies>\n"), encoding='utf-8')

            # Copier les fichiers dans files/
            for contenthash, content in self.files_content.items():
                # Structure: files/ab/contenthash (premiers 2 caracteres comme sous-dossier)
                subdir = files_dir / contenthash[:2]
                subdir.mkdir(exist_ok=True)
                (subdir / contenthash).write_bytes(content)

            # Creer l'archive tar
            tar_path = Path(output_path).with_suffix('.tar')
            with tarfile.open(tar_path, 'w') as tar:
                for file_path in tmppath.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(tmppath)
                        tar.add(file_path, arcname=arcname)

            # Compresser avec gzip
            with open(tar_path, 'rb') as f_in:
                with gzip.open(output_path, 'wb') as f_out:
                    f_out.writelines(f_in)

            # Supprimer le tar intermediaire
            tar_path.unlink()

        return str(Path(output_path).absolute())


def main():
    parser = argparse.ArgumentParser(description='Generateur de cours Moodle complets (.mbz)')
    parser.add_argument('--config', '-c', help='Fichier de configuration JSON')
    parser.add_argument('--output', '-o', help='Fichier .mbz de sortie')
    parser.add_argument('--scan-dir', '-s', help='Scanner un dossier pour les PDFs')

    args = parser.parse_args()

    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Passer les settings au generateur
        gen = MoodleCourseGenerator(
            config['course_fullname'],
            config['course_shortname'],
            config.get('settings', {})
        )

        skipped_files = []

        for sec in config.get('sections', []):
            section_id = gen.add_section(
                sec['name'],
                sec.get('summary', ''),
                sec.get('visible', False)
            )

            for act in sec.get('activities', []):
                if act['type'] == 'file':
                    # Verifier que le fichier est valide (pas une source)
                    if not MoodleCourseGenerator.is_valid_file(act['path']):
                        skipped_files.append(act['path'])
                        continue
                    # Verifier que le fichier existe
                    if not os.path.exists(act['path']):
                        print(f"Attention: Fichier introuvable: {act['path']}")
                        continue
                    gen.add_file_resource(
                        section_id, act['name'], act['path'],
                        act.get('description', ''),
                        act.get('visible', False)
                    )
                elif act['type'] == 'page':
                    gen.add_page(
                        section_id, act['name'], act['content'],
                        act.get('visible', False)
                    )
                elif act['type'] == 'quiz':
                    gen.add_quiz(
                        section_id, act['name'], act.get('intro', ''),
                        act['questions'],
                        act.get('visible', False)
                    )
                elif act['type'] == 'h5p':
                    gen.add_h5p(
                        section_id, act['name'], act.get('intro', ''),
                        h5p_file_path=act.get('h5p_file'),
                        questions=act.get('questions'),
                        h5p_type=act.get('h5p_type', 'questionset'),
                        visible=act.get('visible', False)
                    )

        if skipped_files:
            print(f"Fichiers sources exclus ({len(skipped_files)}):")
            for f in skipped_files[:5]:
                print(f"  - {f}")
            if len(skipped_files) > 5:
                print(f"  ... et {len(skipped_files) - 5} autres")

        output = args.output or config.get('output', 'cours.mbz')
        result = gen.generate_mbz(output)
        print(f"Cours genere : {result}")

    elif args.scan_dir:
        # Mode scan: lister les PDFs d'un dossier
        from pathlib import Path
        pdfs = list(Path(args.scan_dir).rglob('*.pdf'))
        valid_pdfs = [p for p in pdfs if MoodleCourseGenerator.is_valid_file(str(p))]
        print(f"PDFs trouves dans {args.scan_dir}:")
        for pdf in sorted(valid_pdfs):
            print(f"  {pdf}")
        print(f"\nTotal: {len(valid_pdfs)} fichiers valides (sur {len(pdfs)} trouves)")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
