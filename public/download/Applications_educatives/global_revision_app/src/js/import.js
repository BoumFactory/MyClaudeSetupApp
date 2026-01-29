/**
 * Module Import - Workflow guidé pour générer et importer des questions
 */
const Import = (function() {
    'use strict';

    // Prompts optimisés (courts pour économiser les tokens)
    const PROMPTS = {
        qcm: `Génère des QCM JSON. Format STRICT :
[{"subject":"ID_MATIERE","theme":"Thème","type":"qcm","difficulty":1,"question":"Question avec $LaTeX$ si maths","choices":[{"id":"a","text":"Choix A"},{"id":"b","text":"Choix B"},{"id":"c","text":"Choix C"}],"correctAnswers":["a"],"explanation":"Explication"}]

IDs matières: maths, physique, svt, nsi, francais, philosophie, histoire-geo, ses, anglais, allemand, espagnol, latin, grec, hggsp, hlp, si

Règles: difficulty 1-3, correctAnswers=tableau, LaTeX entre $...$

Génère 5 QCM sur : `,

        input: `Génère des questions à réponse libre JSON. Format STRICT :
[{"subject":"ID_MATIERE","theme":"Thème","type":"input","difficulty":2,"question":"Question","fields":[{"id":"rep","label":"Réponse :","type":"text","answer":"réponse","alternatives":["autre forme"]}],"explanation":"Explication"}]

IDs matières: maths, physique, svt, nsi, francais, philosophie, histoire-geo, ses, anglais, allemand, espagnol, latin, grec, hggsp, hlp, si

Types de champs: "text" ou "number" (avec "tolerance":0.1 si besoin)

Génère 5 questions sur : `,

        mixte: `Génère des questions de révision JSON (QCM et réponses libres mélangés). Format STRICT :

QCM: {"subject":"ID","theme":"Thème","type":"qcm","difficulty":1,"question":"...","choices":[{"id":"a","text":"..."}],"correctAnswers":["a"],"explanation":"..."}

Input: {"subject":"ID","theme":"Thème","type":"input","difficulty":2,"question":"...","fields":[{"id":"rep","type":"text","answer":"...","alternatives":["..."]}],"explanation":"..."}

IDs: maths, physique, svt, nsi, francais, philosophie, histoire-geo, ses, anglais, allemand, espagnol, hggsp, hlp, si

Génère 5 questions variées sur : `
    };

    let selectedType = 'mixte';

    function init(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="import-view">
                <!-- ÉTAPE 1 : Générer avec l'IA -->
                <div class="import-section">
                    <h3>1️⃣ Générer des questions avec l'IA</h3>
                    <p class="section-help">Choisis un format, copie le prompt, colle-le dans ChatGPT/Mistral/Claude et complète avec ton sujet.</p>

                    <div class="format-selector">
                        <button class="format-btn ${selectedType === 'qcm' ? 'active' : ''}" onclick="Import.selectFormat('qcm')">
                            <span class="format-icon">☑️</span>
                            <span class="format-name">QCM uniquement</span>
                        </button>
                        <button class="format-btn ${selectedType === 'input' ? 'active' : ''}" onclick="Import.selectFormat('input')">
                            <span class="format-icon">✍️</span>
                            <span class="format-name">Réponses libres</span>
                        </button>
                        <button class="format-btn ${selectedType === 'mixte' ? 'active' : ''}" onclick="Import.selectFormat('mixte')">
                            <span class="format-icon">🔀</span>
                            <span class="format-name">Mixte (recommandé)</span>
                        </button>
                    </div>

                    <div class="prompt-box">
                        <div class="prompt-header">
                            <span>Prompt à copier :</span>
                            <button class="btn btn-primary btn-sm" onclick="Import.copyPrompt()">📋 Copier le prompt</button>
                        </div>
                        <pre class="prompt-content" id="prompt-content">${PROMPTS[selectedType]}</pre>
                    </div>

                    <div class="prompt-tip">
                        <strong>💡 Astuce :</strong> Après avoir copié, complète la fin avec ton sujet. Ex: "le second degré niveau 1ère" ou "les verbes irréguliers anglais"
                    </div>
                </div>

                <!-- ÉTAPE 2 : Importer le résultat -->
                <div class="import-section">
                    <h3>2️⃣ Importer le résultat</h3>
                    <p class="section-help">Copie la réponse JSON de l'IA et colle-la ici (ou glisse un fichier .json)</p>

                    <div class="import-dropzone">
                        <textarea class="import-textarea" placeholder="Colle ici le JSON généré par l'IA..."></textarea>
                        <div class="dropzone-overlay">
                            <span class="dropzone-icon">📄</span>
                            <span>Dépose ton fichier .json</span>
                        </div>
                    </div>

                    <div class="import-actions">
                        <button class="btn btn-secondary" onclick="Import.clear()">Effacer</button>
                        <button class="btn btn-primary" onclick="Import.process()">✅ Importer</button>
                    </div>

                    <div class="import-result" id="import-result"></div>
                </div>
            </div>
        `;

        setupEvents(container);
    }

    function setupEvents(container) {
        const dropzone = container.querySelector('.import-dropzone');
        const textarea = container.querySelector('.import-textarea');

        dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
        dropzone.addEventListener('dragleave', e => { e.preventDefault(); dropzone.classList.remove('dragover'); });
        dropzone.addEventListener('drop', e => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            if (file && (file.type === 'application/json' || file.name.endsWith('.json'))) {
                const reader = new FileReader();
                reader.onload = ev => { textarea.value = ev.target.result; };
                reader.readAsText(file);
            }
        });

        textarea.addEventListener('paste', () => {
            setTimeout(() => {
                try {
                    const parsed = JSON.parse(textarea.value.trim());
                    textarea.value = JSON.stringify(parsed, null, 2);
                } catch (e) { /* pas du JSON */ }
            }, 10);
        });
    }

    function selectFormat(type) {
        selectedType = type;
        document.querySelectorAll('.format-btn').forEach(btn => {
            btn.classList.toggle('active', btn.textContent.toLowerCase().includes(type) ||
                (type === 'mixte' && btn.textContent.includes('Mixte')));
        });
        document.getElementById('prompt-content').textContent = PROMPTS[type];
    }

    function copyPrompt() {
        const prompt = PROMPTS[selectedType];
        navigator.clipboard.writeText(prompt).then(() => {
            App.showNotification('Prompt copié ! Colle-le dans ton IA.', 'success');
        }).catch(() => {
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = prompt;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            App.showNotification('Prompt copié !', 'success');
        });
    }

    function clear() {
        document.querySelector('.import-textarea').value = '';
        document.getElementById('import-result').innerHTML = '';
    }

    function process() {
        const content = document.querySelector('.import-textarea').value.trim();
        if (!content) {
            showResult('error', 'Colle le JSON généré par l\'IA');
            return;
        }

        const result = Database.importFromJSON(content);

        if (result.added.length > 0) {
            showResult('success', `✅ ${result.added.length} question(s) importée(s) !`);
            document.querySelector('.import-textarea').value = '';
            if (window.App) App.refreshUI();
        } else if (result.errors.length > 0) {
            showResult('error', '❌ Erreur : ' + result.errors.map(e => e.error).join(', '));
        }
    }

    function showResult(type, message) {
        const cls = { success: 'result-success', error: 'result-error' };
        document.getElementById('import-result').innerHTML = `<div class="import-message ${cls[type] || ''}">${message}</div>`;
    }

    return { init, selectFormat, copyPrompt, clear, process };
})();
