#!/usr/bin/env python3
"""
Générateur de visualiseur H5P Branching Scenario standalone.

Crée un fichier HTML autonome qui peut être partagé avec des collègues pour
relecture et annotation. Le JSON preplan est embarqué dans le HTML.

Usage:
  # Générer le template du visualiseur
  python build_standalone.py --generate-template --output visualiseur.html

  # Construire un fichier standalone avec données embarquées
  python build_standalone.py --input preplan.json --template visualiseur.html --output standalone.html
"""
import json
import sys
import argparse
from pathlib import Path
from typing import Dict


# ============================================================================
# TEMPLATE DU VISUALISEUR
# ============================================================================

VISUALISEUR_TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualiseur H5P Branching Scenario</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
            transition: background-color 0.3s, color 0.3s;
        }

        body.dark-mode {
            background: #1e1e1e;
            color: #e0e0e0;
        }

        .container {
            display: flex;
            height: 100vh;
            gap: 0;
        }

        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: #2c3e50;
            color: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }

        .header h1 {
            font-size: 18px;
            flex: 1;
        }

        .theme-toggle {
            background: #34495e;
            border: none;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }

        .theme-toggle:hover {
            background: #455a64;
        }

        .main-content {
            display: flex;
            margin-top: 60px;
            height: calc(100vh - 60px);
            gap: 0;
        }

        .sidebar-left {
            width: 25%;
            background: white;
            border-right: 1px solid #ddd;
            overflow-y: auto;
            padding: 20px;
        }

        body.dark-mode .sidebar-left {
            background: #2a2a2a;
            border-right-color: #444;
        }

        .tree-view {
            margin: 0;
            padding: 0;
            list-style: none;
        }

        .tree-item {
            margin: 5px 0;
        }

        .tree-item button {
            background: none;
            border: none;
            padding: 10px;
            width: 100%;
            text-align: left;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 0.2s;
            color: inherit;
            font-size: 14px;
        }

        .tree-item button:hover {
            background: #f0f0f0;
        }

        body.dark-mode .tree-item button:hover {
            background: #3a3a3a;
        }

        .tree-item button.active {
            background: #3498db;
            color: white;
            font-weight: bold;
        }

        .tree-item button.active:hover {
            background: #2980b9;
        }

        .type-badge {
            display: inline-block;
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 3px;
            margin-left: 5px;
            font-weight: bold;
        }

        .type-text { background: #e3f2fd; color: #1565c0; }
        .type-branching { background: #f3e5f5; color: #6a1b9a; }
        .type-course { background: #e8f5e9; color: #2e7d32; }
        .type-video { background: #fff3e0; color: #e65100; }
        .type-image { background: #fce4ec; color: #c2185b; }

        body.dark-mode .type-text { background: #1a237e; }
        body.dark-mode .type-branching { background: #4a148c; }
        body.dark-mode .type-course { background: #1b5e20; }
        body.dark-mode .type-video { background: #e65100; }
        body.dark-mode .type-image { background: #880e4f; }

        .center {
            flex: 1;
            background: white;
            border-right: 1px solid #ddd;
            overflow-y: auto;
            padding: 30px;
        }

        body.dark-mode .center {
            background: #1e1e1e;
            border-right-color: #444;
        }

        .content-preview {
            max-width: 800px;
        }

        .preview-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }

        body.dark-mode .preview-title {
            color: #e0e0e0;
        }

        .preview-meta {
            font-size: 12px;
            color: #999;
            margin-bottom: 20px;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 4px;
        }

        body.dark-mode .preview-meta {
            background: #2a2a2a;
            color: #999;
        }

        .preview-content {
            line-height: 1.6;
            margin: 20px 0;
        }

        .preview-content h3 {
            margin-top: 15px;
            margin-bottom: 10px;
        }

        .alternative {
            background: #f5f5f5;
            padding: 12px;
            margin: 10px 0;
            border-left: 3px solid #3498db;
            border-radius: 4px;
        }

        body.dark-mode .alternative {
            background: #2a2a2a;
            border-left-color: #64b5f6;
        }

        .alternative-text {
            font-weight: 500;
        }

        .sidebar-right {
            width: 25%;
            background: white;
            border-left: 1px solid #ddd;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }

        body.dark-mode .sidebar-right {
            background: #2a2a2a;
            border-left-color: #444;
        }

        .remarks-section h3 {
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 16px;
        }

        .remark-item {
            background: #fff9e6;
            border-left: 3px solid #ffc107;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
            font-size: 13px;
        }

        body.dark-mode .remark-item {
            background: #332701;
            border-left-color: #ffa500;
        }

        .add-remark {
            margin: 15px 0;
        }

        .add-remark textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            font-size: 12px;
            resize: vertical;
            min-height: 60px;
        }

        body.dark-mode .add-remark textarea {
            background: #2a2a2a;
            border-color: #444;
            color: #e0e0e0;
        }

        .btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            margin: 5px 0;
        }

        .btn:hover {
            background: #2980b9;
        }

        .btn-primary {
            background: #27ae60;
            width: 100%;
        }

        .btn-primary:hover {
            background: #229954;
        }

        .file-input-wrapper {
            margin: 15px 0;
        }

        .file-input-wrapper input[type="file"] {
            width: 100%;
            padding: 8px;
            border: 1px dashed #ddd;
            border-radius: 4px;
            cursor: pointer;
        }

        body.dark-mode .file-input-wrapper input[type="file"] {
            border-color: #444;
            background: #2a2a2a;
            color: #e0e0e0;
        }

        .info-card {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
            font-size: 13px;
            line-height: 1.5;
        }

        body.dark-mode .info-card {
            background: #1a237e;
            border-left-color: #64b5f6;
        }

        .empty-state {
            text-align: center;
            color: #999;
            padding: 40px 20px;
        }

        body.dark-mode .empty-state {
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Visualiseur H5P Branching Scenario</h1>
        <button class="theme-toggle" onclick="toggleTheme()">Thème sombre</button>
    </div>

    <div class="main-content">
        <!-- Panneau gauche : arborescence -->
        <div class="sidebar-left">
            <h3>Arborescence</h3>
            <ul id="tree" class="tree-view"></ul>
            <div class="file-input-wrapper" id="file-input-section">
                <label>Charger un preplan:</label>
                <input type="file" id="file-input" accept=".json" onchange="loadFile(event)">
            </div>
        </div>

        <!-- Panneau central : aperçu du contenu -->
        <div class="center">
            <div id="content-area" class="content-preview">
                <div class="empty-state">
                    <p>Chargez un fichier preplan JSON pour commencer.</p>
                    <p style="font-size: 12px; margin-top: 10px;">Utilisez le formulaire ci-dessous ou déposez un fichier sur le panneau gauche.</p>
                </div>
            </div>
        </div>

        <!-- Panneau droit : remarques -->
        <div class="sidebar-right">
            <div class="remarks-section">
                <h3>Remarques</h3>
                <div id="remarks-list"></div>
                <div class="add-remark">
                    <textarea id="remark-input" placeholder="Ajouter une remarque pour ce nœud..."></textarea>
                    <button class="btn btn-primary" onclick="addRemark()">+ Ajouter remarque</button>
                </div>
                <button class="btn" onclick="downloadRemarks()">Télécharger remarques</button>
                <button class="btn" onclick="clearAllRemarks()">Effacer tout</button>
            </div>

            <div class="info-card">
                <strong>Guide:</strong>
                <ul style="margin-left: 15px; margin-top: 10px;">
                    <li>Cliquez sur un nœud pour l'aperçu</li>
                    <li>Ajoutez des remarques par nœud</li>
                    <li>Téléchargez les remarques en JSON</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        let preplan = null;
        let currentNode = null;
        let remarks = {};

        // Placeholder pour les données embarquées
        var __EMBEDDED_PREPLAN__ = null;

        function toggleTheme() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        }

        function loadThemePreference() {
            if (localStorage.getItem('theme') === 'dark') {
                document.body.classList.add('dark-mode');
                document.querySelector('.theme-toggle').textContent = 'Thème clair';
            }
        }

        function loadFile(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    preplan = JSON.parse(e.target.result);
                    renderTree();
                    showEmptyState();
                } catch (err) {
                    alert('Erreur JSON: ' + err.message);
                }
            };
            reader.readAsText(file);
        }

        function renderTree() {
            const tree = document.getElementById('tree');
            tree.innerHTML = '';

            if (!preplan || !preplan.nodes) return;

            const title = document.createElement('li');
            title.className = 'tree-item';
            const btn = document.createElement('button');
            btn.textContent = `📄 ${preplan.title || 'Sans titre'}`;
            btn.className = 'active';
            btn.onclick = () => showNodePreview(-1);
            title.appendChild(btn);
            tree.appendChild(title);

            preplan.nodes.forEach((node, idx) => {
                const li = document.createElement('li');
                li.className = 'tree-item';
                const btn = document.createElement('button');

                const typeEmoji = {
                    'text': '📝',
                    'branching_question': '❓',
                    'course_presentation': '📊',
                    'interactive_video': '🎥',
                    'image': '🖼️',
                    'video': '▶️'
                }[node.type] || '📌';

                const typeBadge = `<span class="type-badge type-${(node.type || 'text').split('_')[0]}">${node.type || 'text'}</span>`;
                btn.innerHTML = `${typeEmoji} ${node.title || `Nœud ${idx}`} ${typeBadge}`;
                btn.onclick = () => showNodePreview(idx);
                li.appendChild(btn);
                tree.appendChild(li);
            });
        }

        function showNodePreview(idx) {
            currentNode = idx;
            const content = document.getElementById('content-area');
            document.querySelectorAll('.tree-item button').forEach((btn, i) => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            if (idx === -1) {
                content.innerHTML = `
                    <div class="content-preview">
                        <div class="preview-title">${preplan.title || 'Parcours'}</div>
                        <div class="preview-meta">
                            <strong>Configuration globale</strong>
                        </div>
                        <div class="preview-content">
                            <p><strong>Pattern:</strong> ${preplan._meta?.pattern || 'custom'}</p>
                            <p><strong>Scoring:</strong> ${preplan.scoring || 'no-score'}</p>
                            <p><strong>Nœuds:</strong> ${preplan.nodes?.length || 0}</p>
                            <p><strong>Écrans de fin:</strong> ${preplan.endScreens?.length || 0}</p>
                            ${preplan.startScreen ? `
                                <h3>Écran de démarrage</h3>
                                <p><strong>${preplan.startScreen.title}</strong></p>
                                <p>${preplan.startScreen.subtitle || ''}</p>
                            ` : ''}
                        </div>
                    </div>
                `;
            } else {
                const node = preplan.nodes[idx];
                let html = `
                    <div class="content-preview">
                        <div class="preview-title">[${idx}] ${node.title || 'Sans titre'}</div>
                        <div class="preview-meta">
                            Type: <strong>${node.type || 'text'}</strong> |
                            Suivant: <strong>${node.nextContentId !== undefined ? node.nextContentId : '-'}</strong>
                        </div>
                        <div class="preview-content">
                `;

                if (node.type === 'branching_question') {
                    html += `<h3>Question</h3><p>${node.question || node.content || ''}</p>`;
                    html += `<h3>Alternatives (${node.alternatives?.length || 0})</h3>`;
                    (node.alternatives || []).forEach((alt, i) => {
                        html += `
                            <div class="alternative">
                                <div class="alternative-text">${alt.text}</div>
                                <small>→ Nœud ${alt.nextContentId}</small>
                                ${alt.feedback ? `<small><br/>Score: ${alt.feedback.score || 0}</small>` : ''}
                            </div>
                        `;
                    });
                } else if (node.type === 'course_presentation') {
                    html += `<h3>Diapositives (${node.slides?.length || 0})</h3>`;
                    (node.slides || []).forEach((slide, i) => {
                        html += `<p><strong>Slide ${i+1}:</strong> ${slide.content?.substring(0, 100) || '(vide)'}...</p>`;
                    });
                } else {
                    html += `<h3>Contenu</h3><p>${node.content || '(vide)'}</p>`;
                }

                if (node.feedback) {
                    html += `
                        <h3>Retour</h3>
                        <p><strong>${node.feedback.title}</strong></p>
                        <p>${node.feedback.subtitle}</p>
                        <p>Score: <strong>${node.feedback.score || 0}</strong></p>
                    `;
                }

                html += `</div></div>`;
                content.innerHTML = html;
            }

            displayRemarks();
        }

        function showEmptyState() {
            const content = document.getElementById('content-area');
            content.innerHTML = `
                <div class="empty-state">
                    <p>Preplan chargé: ${preplan.title}</p>
                    <p>Cliquez sur un nœud pour voir les détails.</p>
                </div>
            `;
        }

        function addRemark() {
            if (currentNode === null) {
                alert('Sélectionnez un nœud d\'abord');
                return;
            }

            const text = document.getElementById('remark-input').value.trim();
            if (!text) return;

            const key = `node_${currentNode}`;
            if (!remarks[key]) remarks[key] = [];
            remarks[key].push({
                timestamp: new Date().toISOString(),
                text: text
            });

            document.getElementById('remark-input').value = '';
            displayRemarks();
        }

        function displayRemarks() {
            const key = `node_${currentNode}`;
            const list = document.getElementById('remarks-list');
            list.innerHTML = '';

            if (!remarks[key]) return;

            remarks[key].forEach((r, i) => {
                const div = document.createElement('div');
                div.className = 'remark-item';
                div.innerHTML = `
                    <div>${r.text}</div>
                    <small>${new Date(r.timestamp).toLocaleString('fr-FR')}</small>
                    <button class="btn" style="width: auto; font-size: 11px; padding: 4px 8px;" onclick="deleteRemark('${key}', ${i})">Supprimer</button>
                `;
                list.appendChild(div);
            });
        }

        function deleteRemark(key, idx) {
            if (remarks[key]) {
                remarks[key].splice(idx, 1);
                if (remarks[key].length === 0) delete remarks[key];
                displayRemarks();
            }
        }

        function downloadRemarks() {
            const data = {
                preplan_title: preplan?.title,
                generated: new Date().toISOString(),
                remarks: remarks
            };

            const json = JSON.stringify(data, null, 2);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `remarques-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function clearAllRemarks() {
            if (confirm('Êtes-vous sûr ?')) {
                remarks = {};
                displayRemarks();
            }
        }

        // Charger le thème au démarrage
        loadThemePreference();

        // Si un preplan est embarqué, l'afficher
        if (__EMBEDDED_PREPLAN__) {
            preplan = __EMBEDDED_PREPLAN__;
            document.getElementById('file-input-section').style.display = 'none';
            renderTree();
            showEmptyState();
        }
    </script>
</body>
</html>
'''


# ============================================================================
# GENERATION DU TEMPLATE
# ============================================================================

def generate_template(output_path: Path):
    """Génère le fichier template du visualiseur."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(VISUALISEUR_TEMPLATE)
    print(f"OK Template généré : {output_path}")
    return 0


# ============================================================================
# CONSTRUCTION DU FICHIER STANDALONE
# ============================================================================

def build_standalone(preplan_path: Path, template_path: Path, output_path: Path):
    """Construit le fichier standalone en embarquant le preplan dans le template."""
    # Lire le preplan
    try:
        with open(preplan_path, 'r', encoding='utf-8') as f:
            preplan = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERREUR: JSON invalide dans {preplan_path}: {e}")
        return 1

    # Lire le template
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f"ERREUR: template non trouvé : {template_path}")
        return 1

    # Embarquer le preplan
    preplan_json = json.dumps(preplan, ensure_ascii=False)
    html = html.replace(
        'var __EMBEDDED_PREPLAN__ = null;',
        f'var __EMBEDDED_PREPLAN__ = {preplan_json};'
    )

    # Sauvegarder
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"OK Fichier standalone généré : {output_path}")
    return 0


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Génère un visualiseur HTML standalone pour H5P Branching Scenario'
    )
    parser.add_argument('--generate-template', action='store_true',
                        help='Générer le template du visualiseur')
    parser.add_argument('--input', '-i', help='Fichier JSON du preplan')
    parser.add_argument('--template', '-t', help='Fichier HTML du template')
    parser.add_argument('--output', '-o', required=True, help='Fichier HTML de sortie')

    args = parser.parse_args()

    if args.generate_template:
        return generate_template(Path(args.output))

    if not args.input or not args.template:
        print("ERREUR: --input et --template requis (sauf en mode --generate-template)")
        return 1

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERREUR: fichier introuvable : {args.input}")
        return 1

    template_path = Path(args.template)
    if not template_path.exists():
        print(f"ERREUR: template non trouvé : {args.template}")
        print(f"  Générez-le avec: python build_standalone.py --generate-template --output {args.template}")
        return 1

    return build_standalone(input_path, template_path, Path(args.output))


if __name__ == '__main__':
    sys.exit(main())
