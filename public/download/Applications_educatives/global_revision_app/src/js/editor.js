/**
 * Module Editor - Interface CRUD pour gérer les questions
 */
const Editor = (function() {
    'use strict';

    let currentEditId = null;
    let filterSubject = null;

    function init(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="editor-container">
                <div class="editor-sidebar">
                    <h3>📚 Mes questions</h3>
                    <div class="editor-filters">
                        <select id="filter-subject" class="filter-select" onchange="Editor.filterBySubject(this.value)">
                            <option value="">Toutes les matières</option>
                        </select>
                    </div>
                    <div class="editor-stats"><span id="question-count">0 questions</span></div>
                    <div class="editor-actions-bar">
                        <button class="btn btn-primary btn-sm" onclick="Editor.showNewForm()">+ Nouvelle</button>
                        <button class="btn btn-secondary btn-sm" onclick="Editor.resetAllStats()">Reset stats</button>
                    </div>
                    <div class="question-list" id="question-list"></div>
                </div>
                <div class="editor-main">
                    <div id="editor-form-container">
                        <div class="editor-placeholder"><p>Sélectionnez ou créez une question</p></div>
                    </div>
                </div>
            </div>
        `;

        updateFilters();
        renderQuestionList();
        Database.addListener((event) => {
            if (['init', 'add', 'delete', 'update', 'stats-reset'].includes(event)) {
                updateFilters();
                renderQuestionList();
            }
        });
    }

    function updateFilters() {
        const select = document.getElementById('filter-subject');
        if (!select) return;
        const val = select.value;
        select.innerHTML = '<option value="">Toutes les matières</option>' +
            Database.getSubjects(true).map(s => `<option value="${s.id}">${s.icon} ${s.name}</option>`).join('');
        select.value = val;
    }

    function filterBySubject(id) {
        filterSubject = id || null;
        renderQuestionList();
    }

    function renderQuestionList() {
        const container = document.getElementById('question-list');
        const countEl = document.getElementById('question-count');
        if (!container) return;

        const filter = filterSubject ? { subject: filterSubject } : {};
        const questions = Database.getQuestionsByFilter(filter);

        if (countEl) countEl.textContent = `${questions.length} question(s)`;

        if (questions.length === 0) {
            container.innerHTML = '<p class="no-questions">Aucune question</p>';
            return;
        }

        container.innerHTML = questions.map(q => {
            const preview = q.question.replace(/\$[^$]+\$/g, '[math]').substring(0, 50);
            const stats = q.stats || {};
            return `
                <div class="question-item ${currentEditId === q.id ? 'active' : ''}" onclick="Editor.selectQuestion('${q.id}')">
                    <div class="question-item-header">
                        <span class="type-badge type-${q.type}">${q.type}</span>
                        <span class="difficulty-badge">★${q.difficulty || 1}</span>
                    </div>
                    <div class="question-item-preview">${preview}...</div>
                    <div class="question-item-meta">
                        <span>👁 ${stats.accessCount || 0}</span>
                        <button class="btn-icon btn-danger" onclick="event.stopPropagation(); Editor.deleteQuestion('${q.id}')">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');
    }

    function selectQuestion(id) {
        currentEditId = id;
        const question = Database.getQuestion(id);
        if (question) renderEditForm(question);
        renderQuestionList();
    }

    function showNewForm() {
        currentEditId = null;
        renderEditForm(null);
        renderQuestionList();
    }

    function renderEditForm(question) {
        const container = document.getElementById('editor-form-container');
        if (!container) return;

        const isNew = !question;
        const q = question || {
            type: 'qcm', subject: filterSubject || 'maths', theme: '', difficulty: 1,
            question: '', choices: [{ id: 'a', text: '' }, { id: 'b', text: '' }],
            correctAnswers: [], explanation: '', hint: ''
        };

        const subjects = Database.getSubjects();

        container.innerHTML = `
            <div class="edit-form">
                <h3>${isNew ? '+ Nouvelle question' : 'Modifier'}</h3>
                <form id="question-form" onsubmit="return false;">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Type</label>
                            <select id="edit-type" name="type" onchange="Editor.toggleTypeFields(this.value)">
                                <option value="qcm" ${q.type === 'qcm' ? 'selected' : ''}>QCM</option>
                                <option value="input" ${q.type === 'input' ? 'selected' : ''}>Réponse libre</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Difficulté</label>
                            <select id="edit-difficulty" name="difficulty">
                                <option value="1" ${q.difficulty === 1 ? 'selected' : ''}>★ Facile</option>
                                <option value="2" ${q.difficulty === 2 ? 'selected' : ''}>★★ Moyen</option>
                                <option value="3" ${q.difficulty === 3 ? 'selected' : ''}>★★★ Difficile</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Matière</label>
                            <select id="edit-subject" name="subject">
                                ${subjects.map(s => `<option value="${s.id}" ${s.id === q.subject ? 'selected' : ''}>${s.icon} ${s.name}</option>`).join('')}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Thème (label)</label>
                            <input type="text" id="edit-theme" name="theme" value="${q.theme || ''}" placeholder="Ex: Second degré">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Question (LaTeX: $...$)</label>
                        <textarea id="edit-question" name="question" rows="3" required>${q.question}</textarea>
                    </div>
                    <div id="qcm-fields" style="${q.type !== 'qcm' ? 'display:none' : ''}">
                        <label>Choix</label>
                        <div id="choices-container">${buildChoicesHTML(q.choices, q.correctAnswers)}</div>
                        <button type="button" class="btn btn-sm btn-secondary" onclick="Editor.addChoice()">+ Choix</button>
                    </div>
                    <div id="input-fields" style="${q.type !== 'input' ? 'display:none' : ''}">
                        <label>Champs</label>
                        <div id="fields-container">${buildFieldsHTML(q.fields)}</div>
                        <button type="button" class="btn btn-sm btn-secondary" onclick="Editor.addField()">+ Champ</button>
                    </div>
                    <div class="form-group">
                        <label>Explication</label>
                        <textarea id="edit-explanation" name="explanation" rows="2">${q.explanation || ''}</textarea>
                    </div>
                    <div class="form-group">
                        <label>Indice (optionnel)</label>
                        <input type="text" id="edit-hint" name="hint" value="${q.hint || ''}">
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" onclick="Editor.cancelEdit()">Annuler</button>
                        <button type="button" class="btn btn-primary" onclick="Editor.saveQuestion()">${isNew ? 'Créer' : 'Enregistrer'}</button>
                    </div>
                </form>
            </div>
        `;
    }

    function buildChoicesHTML(choices = [], correct = []) {
        if (!choices.length) choices = [{ id: 'a', text: '' }, { id: 'b', text: '' }];
        return choices.map(c => `
            <div class="choice-edit-row" data-choice-id="${c.id}">
                <input type="checkbox" name="correct[]" value="${c.id}" ${correct.includes(c.id) ? 'checked' : ''}>
                <span class="choice-letter">${c.id.toUpperCase()}</span>
                <input type="text" name="choice-text-${c.id}" value="${esc(c.text)}" placeholder="Texte..." class="choice-text-input">
                <button type="button" class="btn-icon btn-danger" onclick="Editor.removeChoice('${c.id}')">×</button>
            </div>
        `).join('');
    }

    function buildFieldsHTML(fields = []) {
        if (!fields || !fields.length) fields = [{ id: 'answer', label: '', type: 'text', answer: '' }];
        return fields.map((f, i) => `
            <div class="field-edit-row" data-field-index="${i}">
                <select name="field-type-${i}">
                    <option value="text" ${f.type === 'text' ? 'selected' : ''}>Texte</option>
                    <option value="number" ${f.type === 'number' ? 'selected' : ''}>Nombre</option>
                </select>
                <input type="text" name="field-label-${i}" value="${esc(f.label || '')}" placeholder="Label">
                <input type="text" name="field-answer-${i}" value="${esc(String(f.answer || ''))}" placeholder="Réponse">
                <input type="text" name="field-alts-${i}" value="${(f.alternatives || []).join(', ')}" placeholder="Alternatives (,)">
                <button type="button" class="btn-icon btn-danger" onclick="Editor.removeField(${i})">×</button>
            </div>
        `).join('');
    }

    function esc(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function toggleTypeFields(type) {
        document.getElementById('qcm-fields').style.display = type === 'qcm' ? '' : 'none';
        document.getElementById('input-fields').style.display = type === 'input' ? '' : 'none';
    }

    function addChoice() {
        const container = document.getElementById('choices-container');
        const letters = 'abcdefgh';
        const next = letters[container.querySelectorAll('.choice-edit-row').length] || 'x';
        container.insertAdjacentHTML('beforeend', buildChoicesHTML([{ id: next, text: '' }], []));
    }

    function removeChoice(id) {
        document.querySelector(`.choice-edit-row[data-choice-id="${id}"]`)?.remove();
    }

    function addField() {
        const container = document.getElementById('fields-container');
        const i = container.querySelectorAll('.field-edit-row').length;
        container.insertAdjacentHTML('beforeend', buildFieldsHTML([{ id: 'field' + i, type: 'text', answer: '' }])
            .replace(/field-(\w+)-0/g, `field-$1-${i}`));
    }

    function removeField(i) {
        document.querySelector(`.field-edit-row[data-field-index="${i}"]`)?.remove();
    }

    function saveQuestion() {
        const form = document.getElementById('question-form');
        const type = form.querySelector('[name="type"]').value;

        const question = {
            type,
            subject: form.querySelector('[name="subject"]').value,
            theme: form.querySelector('[name="theme"]').value,
            difficulty: parseInt(form.querySelector('[name="difficulty"]').value),
            question: form.querySelector('[name="question"]').value,
            explanation: form.querySelector('[name="explanation"]').value,
            hint: form.querySelector('[name="hint"]').value
        };

        if (type === 'qcm') {
            question.choices = [];
            question.correctAnswers = [];
            form.querySelectorAll('.choice-edit-row').forEach(row => {
                const id = row.dataset.choiceId;
                const text = row.querySelector('.choice-text-input').value;
                if (text.trim()) {
                    question.choices.push({ id, text });
                    if (row.querySelector('input[type="checkbox"]').checked) question.correctAnswers.push(id);
                }
            });
        } else {
            question.fields = [];
            form.querySelectorAll('.field-edit-row').forEach((row, i) => {
                const fieldType = row.querySelector(`[name="field-type-${i}"]`).value;
                const answer = row.querySelector(`[name="field-answer-${i}"]`).value;
                const alts = row.querySelector(`[name="field-alts-${i}"]`).value;
                question.fields.push({
                    id: 'field' + i,
                    type: fieldType,
                    label: row.querySelector(`[name="field-label-${i}"]`).value,
                    answer: fieldType === 'number' ? parseFloat(answer) : answer,
                    alternatives: alts ? alts.split(',').map(s => s.trim()).filter(Boolean) : []
                });
            });
        }

        if (!question.question.trim()) { alert('Question obligatoire'); return; }
        if (type === 'qcm' && question.choices.length < 2) { alert('Au moins 2 choix'); return; }
        if (type === 'qcm' && !question.correctAnswers.length) { alert('Cochez une réponse correcte'); return; }

        if (currentEditId) {
            Database.updateQuestion(currentEditId, question);
            App.showNotification('Question mise à jour', 'success');
        } else {
            const result = Database.addQuestions(question);
            if (result.added.length) {
                currentEditId = result.added[0].id;
                App.showNotification('Question créée', 'success');
            }
        }
        renderQuestionList();
    }

    function cancelEdit() {
        currentEditId = null;
        document.getElementById('editor-form-container').innerHTML =
            '<div class="editor-placeholder"><p>Sélectionnez ou créez une question</p></div>';
        renderQuestionList();
    }

    function deleteQuestion(id) {
        if (!confirm('Supprimer cette question ?')) return;
        Database.deleteQuestion(id);
        if (currentEditId === id) cancelEdit();
        App.showNotification('Question supprimée', 'info');
    }

    function resetAllStats() {
        if (!confirm('Réinitialiser toutes les statistiques ?')) return;
        Database.resetStats();
        App.showNotification('Stats réinitialisées', 'info');
    }

    return {
        init, filterBySubject, selectQuestion, showNewForm, toggleTypeFields,
        addChoice, removeChoice, addField, removeField, saveQuestion, cancelEdit,
        deleteQuestion, resetAllStats
    };
})();
