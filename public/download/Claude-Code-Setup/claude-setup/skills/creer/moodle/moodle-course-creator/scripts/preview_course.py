#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prévisualisateur de cours Moodle
Génère une page HTML interactive pour vérifier le cours avant import.

Usage:
    python preview_course.py --config cours_config.json
    python preview_course.py --config cours_config.json --output preview.html
"""

import json
import os
import re
import argparse
from pathlib import Path
from datetime import datetime


def escape_html(text: str) -> str:
    """Échappe les caractères HTML sauf les balises LaTeX"""
    if not text:
        return ""
    # Préserver les $ pour LaTeX
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


def convert_math_delimiters(text: str) -> str:
    """Convertit les délimiteurs LaTeX pour KaTeX"""
    if not text:
        return ""
    # Convertir \[ \] en $$ $$
    text = re.sub(r'\\\[', '$$', text)
    text = re.sub(r'\\\]', '$$', text)
    # Convertir \( \) en $ $
    text = re.sub(r'\\\(', '$', text)
    text = re.sub(r'\\\)', '$', text)
    # Garder les _ pour les indices (u_n, etc.)
    return text


def generate_preview_html(config: dict, output_path: str = None) -> str:
    """
    Génère une page HTML de prévisualisation du cours.

    Args:
        config: Configuration JSON du cours
        output_path: Chemin de sortie (optionnel)

    Returns:
        Chemin du fichier HTML généré
    """

    course_name = config.get('course_fullname', 'Cours Moodle')
    course_short = config.get('course_shortname', 'COURS')
    sections = config.get('sections', [])

    # Construire le HTML des sections
    sections_html = ""
    stats = {'pdfs': 0, 'h5p': 0, 'pages': 0, 'questions': 0}

    for i, section in enumerate(sections):
        section_name = section.get('name', f'Section {i+1}')
        section_summary = section.get('summary', '')
        visible = section.get('visible', False)
        activities = section.get('activities', [])

        activities_html = ""
        for act in activities:
            act_type = act.get('type', '')
            act_name = act.get('name', 'Sans nom')

            if act_type == 'file':
                stats['pdfs'] += 1
                path = act.get('path', '')
                filename = os.path.basename(path) if path else 'fichier.pdf'
                exists = os.path.exists(path) if path else False
                status_class = 'file-ok' if exists else 'file-missing'
                status_icon = '✓' if exists else '✗'
                activities_html += f'''
                <div class="activity activity-file {status_class}">
                    <span class="activity-icon">📄</span>
                    <span class="activity-name">{escape_html(act_name)}</span>
                    <span class="file-status">{status_icon} {escape_html(filename)}</span>
                </div>'''

            elif act_type == 'page':
                stats['pages'] += 1
                content = act.get('content', '')
                activities_html += f'''
                <div class="activity activity-page">
                    <span class="activity-icon">📝</span>
                    <span class="activity-name">{escape_html(act_name)}</span>
                    <div class="page-preview">{content}</div>
                </div>'''

            elif act_type == 'h5p':
                stats['h5p'] += 1
                h5p_type = act.get('h5p_type', 'questionset')
                questions = act.get('questions', [])
                stats['questions'] += len(questions)

                questions_html = ""
                for q_idx, q in enumerate(questions):
                    q_text = convert_math_delimiters(q.get('text', ''))
                    q_name = q.get('name', f'Question {q_idx+1}')
                    options = q.get('options', [])
                    correct_idx = q.get('correct_index', 0)

                    options_html = ""
                    for o_idx, opt in enumerate(options):
                        opt_text = convert_math_delimiters(opt)
                        is_correct = o_idx == correct_idx
                        correct_class = 'option-correct' if is_correct else 'option-wrong'
                        correct_marker = ' ✓' if is_correct else ''
                        options_html += f'''
                        <div class="option {correct_class}" data-correct="{str(is_correct).lower()}">
                            <span class="option-letter">{chr(65+o_idx)}.</span>
                            <span class="option-text">{escape_html(opt_text)}</span>
                            <span class="correct-marker">{correct_marker}</span>
                        </div>'''

                    questions_html += f'''
                    <div class="question">
                        <div class="question-header">
                            <span class="question-number">Q{q_idx+1}</span>
                            <span class="question-title">{escape_html(q_name)}</span>
                        </div>
                        <div class="question-text">{escape_html(q_text)}</div>
                        <div class="options">{options_html}</div>
                    </div>'''

                h5p_type_label = "Quiz rapide" if h5p_type == "singlechoiceset" else "Quiz complet"
                activities_html += f'''
                <div class="activity activity-h5p">
                    <div class="h5p-header">
                        <span class="activity-icon">🎯</span>
                        <span class="activity-name">{escape_html(act_name)}</span>
                        <span class="h5p-type">{h5p_type_label} ({len(questions)} questions)</span>
                    </div>
                    <div class="h5p-questions">{questions_html}</div>
                </div>'''

            elif act_type == 'quiz':
                # Quiz Moodle natif (déprécié)
                activities_html += f'''
                <div class="activity activity-quiz-warning">
                    <span class="activity-icon">⚠️</span>
                    <span class="activity-name">{escape_html(act_name)}</span>
                    <span class="warning-text">Quiz Moodle natif - Risque de problème de banque de questions !</span>
                </div>'''

        visible_badge = '<span class="badge badge-hidden">Caché</span>' if not visible else '<span class="badge badge-visible">Visible</span>'

        sections_html += f'''
        <div class="section" data-section="{i}">
            <div class="section-header" onclick="toggleSection({i})">
                <span class="section-toggle">▶</span>
                <span class="section-name">{escape_html(section_name)}</span>
                {visible_badge}
                <span class="section-count">{len(activities)} activité(s)</span>
            </div>
            <div class="section-content" id="section-{i}">
                {f'<div class="section-summary">{section_summary}</div>' if section_summary else ''}
                <div class="activities">{activities_html}</div>
            </div>
        </div>'''

    # HTML complet
    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prévisualisation - {escape_html(course_name)}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    <style>
        :root {{
            --primary: #1976d2;
            --success: #4caf50;
            --warning: #ff9800;
            --danger: #f44336;
            --bg: #f5f5f5;
            --card-bg: #ffffff;
            --text: #333;
            --text-light: #666;
            --border: #e0e0e0;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{ max-width: 1000px; margin: 0 auto; }}

        header {{
            background: var(--primary);
            color: white;
            padding: 20px 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}

        header h1 {{ font-size: 1.5rem; margin-bottom: 5px; }}
        header .subtitle {{ opacity: 0.9; font-size: 0.9rem; }}

        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}

        .stat {{
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
        }}

        .section {{
            background: var(--card-bg);
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .section-header {{
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid var(--border);
            transition: background 0.2s;
        }}

        .section-header:hover {{ background: var(--bg); }}

        .section-toggle {{
            transition: transform 0.2s;
            color: var(--text-light);
        }}

        .section.open .section-toggle {{ transform: rotate(90deg); }}

        .section-name {{ font-weight: 600; flex-grow: 1; }}

        .section-count {{ color: var(--text-light); font-size: 0.85rem; }}

        .badge {{
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 500;
        }}

        .badge-hidden {{ background: #ffecb3; color: #ff8f00; }}
        .badge-visible {{ background: #c8e6c9; color: #2e7d32; }}

        .section-content {{
            display: none;
            padding: 15px 20px;
        }}

        .section.open .section-content {{ display: block; }}

        .section-summary {{
            background: var(--bg);
            padding: 10px 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }}

        .activity {{
            padding: 12px 15px;
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .activity-icon {{ font-size: 1.2rem; }}
        .activity-name {{ font-weight: 500; flex-grow: 1; }}

        .activity-file.file-ok {{ border-color: var(--success); background: #f1f8e9; }}
        .activity-file.file-missing {{ border-color: var(--danger); background: #ffebee; }}

        .file-status {{ font-size: 0.85rem; color: var(--text-light); }}
        .file-ok .file-status {{ color: var(--success); }}
        .file-missing .file-status {{ color: var(--danger); }}

        .activity-h5p {{
            display: block;
            border-color: var(--primary);
            background: #e3f2fd;
        }}

        .h5p-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }}

        .h5p-type {{
            background: var(--primary);
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
        }}

        .h5p-questions {{ margin-top: 10px; }}

        .question {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 10px;
        }}

        .question-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}

        .question-number {{
            background: var(--primary);
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .question-title {{ font-weight: 500; color: var(--text-light); }}

        .question-text {{
            font-size: 1.1rem;
            margin-bottom: 15px;
            padding: 10px;
            background: var(--bg);
            border-radius: 4px;
        }}

        .options {{ display: flex; flex-direction: column; gap: 8px; }}

        .option {{
            padding: 10px 15px;
            border: 2px solid var(--border);
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .option:hover {{ border-color: var(--primary); background: #e3f2fd; }}

        .option-letter {{
            font-weight: 600;
            color: var(--text-light);
        }}

        .option-text {{ flex-grow: 1; }}

        .correct-marker {{
            color: var(--success);
            font-weight: bold;
            opacity: 0;
            transition: opacity 0.2s;
        }}

        .show-answers .option-correct {{
            border-color: var(--success);
            background: #e8f5e9;
        }}

        .show-answers .option-wrong {{
            border-color: var(--danger);
            background: #ffebee;
            opacity: 0.6;
        }}

        .show-answers .correct-marker {{ opacity: 1; }}

        .activity-quiz-warning {{
            border-color: var(--warning);
            background: #fff3e0;
        }}

        .warning-text {{
            color: var(--warning);
            font-size: 0.85rem;
        }}

        .page-preview {{
            width: 100%;
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-top: 10px;
            border: 1px solid var(--border);
        }}

        .controls {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
        }}

        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .btn-primary {{
            background: var(--primary);
            color: white;
        }}

        .btn-primary:hover {{ background: #1565c0; }}

        .btn-success {{
            background: var(--success);
            color: white;
        }}

        .btn-success:hover {{ background: #388e3c; }}

        footer {{
            text-align: center;
            padding: 20px;
            color: var(--text-light);
            font-size: 0.85rem;
        }}

        /* KaTeX overrides */
        .katex {{ font-size: 1.1em; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{escape_html(course_name)}</h1>
            <div class="subtitle">{escape_html(course_short)}</div>
            <div class="stats">
                <div class="stat">📁 {stats['pdfs']} fichiers PDF</div>
                <div class="stat">🎯 {stats['h5p']} activités H5P</div>
                <div class="stat">❓ {stats['questions']} questions</div>
                <div class="stat">📝 {stats['pages']} pages</div>
            </div>
        </header>

        <main>
            {sections_html}
        </main>

        <footer>
            Prévisualisation générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        </footer>
    </div>

    <div class="controls">
        <button class="btn btn-primary" onclick="toggleAllSections()">Tout déplier/replier</button>
        <button class="btn btn-success" onclick="toggleAnswers()">Afficher/Masquer réponses</button>
    </div>

    <script>
        // Rendu KaTeX
        document.addEventListener("DOMContentLoaded", function() {{
            renderMathInElement(document.body, {{
                delimiters: [
                    {{left: '$$', right: '$$', display: true}},
                    {{left: '$', right: '$', display: false}},
                    {{left: '\\\\[', right: '\\\\]', display: true}},
                    {{left: '\\\\(', right: '\\\\)', display: false}}
                ],
                throwOnError: false
            }});
        }});

        // Toggle section
        function toggleSection(idx) {{
            const section = document.querySelector(`[data-section="${{idx}}"]`);
            section.classList.toggle('open');
        }}

        // Toggle all sections
        let allOpen = false;
        function toggleAllSections() {{
            const sections = document.querySelectorAll('.section');
            allOpen = !allOpen;
            sections.forEach(s => {{
                if (allOpen) s.classList.add('open');
                else s.classList.remove('open');
            }});
        }}

        // Toggle answers
        let showAnswers = false;
        function toggleAnswers() {{
            showAnswers = !showAnswers;
            document.querySelectorAll('.h5p-questions').forEach(q => {{
                q.classList.toggle('show-answers', showAnswers);
            }});
        }}

        // Open first section by default
        document.querySelector('.section')?.classList.add('open');
    </script>
</body>
</html>'''

    # Déterminer le chemin de sortie
    if not output_path:
        config_path = Path(config.get('_config_path', 'cours_config.json'))
        output_path = config_path.parent / 'preview_cours.html'

    # Écrire le fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return str(Path(output_path).absolute())


def main():
    parser = argparse.ArgumentParser(description='Prévisualisateur de cours Moodle')
    parser.add_argument('--config', '-c', required=True, help='Fichier de configuration JSON')
    parser.add_argument('--output', '-o', help='Fichier HTML de sortie')
    parser.add_argument('--open', action='store_true', help='Ouvrir dans le navigateur')

    args = parser.parse_args()

    # Charger la config
    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)

    config['_config_path'] = args.config

    # Générer la preview
    output = generate_preview_html(config, args.output)
    print(f"Prévisualisation générée : {output}")

    # Ouvrir dans le navigateur si demandé
    if args.open:
        import webbrowser
        webbrowser.open(f'file://{output}')


if __name__ == "__main__":
    main()
