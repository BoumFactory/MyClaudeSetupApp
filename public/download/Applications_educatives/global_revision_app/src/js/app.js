/**
 * Application principale - Global Revision App (Tauri)
 * Lit/écrit directement dans questions.json à côté de l'exécutable
 */
const App = (function() {
    'use strict';

    let currentView = 'home';
    let revisionState = { questions: [], currentIndex: 0, filter: {} };

    /**
     * Point d'entrée : initialise la base et lance l'app
     */
    async function init() {
        console.log('[App] Initialisation...');

        try {
            await Database.init();
            renderNavigation();
            showView('home');
            Database.addListener(() => updateStats());
            updateStats();
            console.log('[App] Prêt !');
        } catch (e) {
            console.error('[App] Erreur init:', e);
            document.body.innerHTML = `
                <div style="padding: 2rem; text-align: center;">
                    <h1>Erreur de chargement</h1>
                    <p>${e.message}</p>
                </div>
            `;
        }
    }

    function renderNavigation() {
        const nav = document.getElementById('main-nav');
        if (!nav) return;

        const status = Database.getStatus();

        nav.innerHTML = `
            <div class="nav-brand">
                <span class="brand-icon">📚</span>
                <span class="brand-text">Révisions</span>
            </div>
            <div class="nav-links">
                <button class="nav-link active" data-view="home" onclick="App.showView('home')">🏠 Accueil</button>
                <button class="nav-link" data-view="revision" onclick="App.showView('revision')">📝 Réviser</button>
                <button class="nav-link" data-view="manage" onclick="App.showView('manage')">✏️ Gérer</button>
                <button class="nav-link" data-view="import" onclick="App.showView('import')">📥 Importer</button>
                <button class="nav-link" data-view="settings" onclick="App.showView('settings')">⚙️ Matières</button>
            </div>
            <div class="nav-actions">
                <button class="btn btn-sm btn-secondary" onclick="App.exportData()">💾 Exporter</button>
            </div>
        `;
    }

    function showView(viewName) {
        currentView = viewName;
        document.querySelectorAll('.nav-link').forEach(l => l.classList.toggle('active', l.dataset.view === viewName));

        const content = document.getElementById('main-content');
        if (!content) return;

        switch (viewName) {
            case 'home': renderHomeView(content); break;
            case 'revision': renderRevisionView(content); break;
            case 'manage': renderManageView(content); break;
            case 'import': renderImportView(content); break;
            case 'settings': renderSettingsView(content); break;
        }
    }

    function renderHomeView(container) {
        const subjects = Database.getSubjects(true);
        const questions = Database.getQuestionsByFilter({});
        const totalAccess = questions.reduce((sum, q) => sum + (q.stats?.accessCount || 0), 0);

        container.innerHTML = `
            <div class="home-view">
                <div class="hero-section">
                    <h1>🎓 Application de Révisions</h1>
                    <p>QCM et questions à réponse libre</p>
                </div>
                <div class="stats-cards">
                    <div class="stat-card"><div class="stat-value" id="stat-questions">${questions.length}</div><div class="stat-label">Questions</div></div>
                    <div class="stat-card"><div class="stat-value" id="stat-subjects">${subjects.length}</div><div class="stat-label">Matières</div></div>
                    <div class="stat-card"><div class="stat-value" id="stat-revisions">${totalAccess}</div><div class="stat-label">Révisions</div></div>
                </div>
                <div class="subject-grid">
                    <h2>📚 Matières</h2>
                    <div class="subjects-container">
                        ${subjects.map(s => {
                            const count = questions.filter(q => q.subject === s.id).length;
                            return `<div class="subject-card" onclick="App.startRevision('${s.id}')">
                                <div class="subject-icon">${s.icon}</div>
                                <div class="subject-name">${s.name}</div>
                                <div class="subject-count">${count} question(s)</div>
                            </div>`;
                        }).join('')}
                        ${subjects.length === 0 ? '<p class="no-data">Aucune matière active. Allez dans ⚙️ Matières.</p>' : ''}
                    </div>
                </div>
                <div class="quick-actions">
                    <h2>🚀 Actions rapides</h2>
                    <div class="actions-container">
                        <button class="action-card" onclick="App.startSmartRevision()">
                            <span class="action-icon">🧠</span>
                            <span class="action-text">Révision intelligente</span>
                            <span class="action-desc">Priorité aux moins révisées</span>
                        </button>
                        <button class="action-card" onclick="App.startRandomRevision()">
                            <span class="action-icon">🎲</span>
                            <span class="action-text">Mode aléatoire</span>
                            <span class="action-desc">Questions au hasard</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    function renderRevisionView(container) {
        const subjects = Database.getSubjects(true);
        container.innerHTML = `
            <div class="revision-view">
                <div class="revision-header">
                    <h2>📝 Révision</h2>
                    <div class="revision-controls">
                        <select id="revision-subject" onchange="App.updateRevisionThemes()">
                            <option value="">Toutes les matières</option>
                            ${subjects.map(s => `<option value="${s.id}">${s.icon} ${s.name}</option>`).join('')}
                        </select>
                        <select id="revision-theme"><option value="">Tous les thèmes</option></select>
                        <button class="btn btn-primary" onclick="App.startFilteredRevision()">Commencer</button>
                    </div>
                </div>
                <div class="revision-progress" id="revision-progress" style="display: none;">
                    <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
                    <span class="progress-text" id="progress-text">0 / 0</span>
                    <span class="progress-stats" id="progress-stats">✓ 0</span>
                </div>
                <div class="question-container" id="question-container">
                    <div class="revision-placeholder"><p>Sélectionnez une matière ou cliquez sur "Commencer"</p></div>
                </div>
                <div class="revision-nav" id="revision-nav" style="display: none;">
                    <button class="btn btn-secondary" onclick="App.previousQuestion()">← Précédent</button>
                    <button class="btn btn-primary" onclick="App.nextQuestion()">Suivant →</button>
                </div>
            </div>
        `;
    }

    function updateRevisionThemes() {
        const subjectId = document.getElementById('revision-subject').value;
        const themeSelect = document.getElementById('revision-theme');
        themeSelect.innerHTML = '<option value="">Tous les thèmes</option>';
        if (subjectId) {
            const themes = Database.getThemes(subjectId);
            themes.forEach(t => { themeSelect.innerHTML += `<option value="${t}">${t}</option>`; });
        }
    }

    function startFilteredRevision() {
        const subject = document.getElementById('revision-subject').value;
        const theme = document.getElementById('revision-theme').value;
        revisionState.filter = {};
        if (subject) revisionState.filter.subject = subject;
        if (theme) revisionState.filter.theme = theme;

        revisionState.questions = Database.getQuestionsByFilter(revisionState.filter);
        revisionState.currentIndex = 0;

        if (!revisionState.questions.length) { showNotification('Aucune question', 'warning'); return; }

        Exercises.resetSessionStats();
        showCurrentQuestion();
        showRevisionUI(true);
    }

    function startRevision(subjectId) {
        revisionState.filter = { subject: subjectId };
        revisionState.questions = Database.getQuestionsByFilter(revisionState.filter);
        revisionState.currentIndex = 0;

        if (!revisionState.questions.length) { showNotification('Aucune question', 'warning'); return; }

        showView('revision');
        setTimeout(() => {
            document.getElementById('revision-subject').value = subjectId;
            updateRevisionThemes();
            Exercises.resetSessionStats();
            showCurrentQuestion();
            showRevisionUI(true);
        }, 50);
    }

    function startSmartRevision() {
        revisionState.filter = {};
        revisionState.questions = Database.getQuestionsForRevision(20);
        revisionState.currentIndex = 0;
        if (!revisionState.questions.length) { showNotification('Aucune question', 'warning'); return; }
        showView('revision');
        setTimeout(() => { Exercises.resetSessionStats(); showCurrentQuestion(); showRevisionUI(true); }, 50);
    }

    function startRandomRevision() {
        revisionState.filter = {};
        revisionState.questions = shuffleArray([...Database.getQuestionsByFilter({})]).slice(0, 20);
        revisionState.currentIndex = 0;
        if (!revisionState.questions.length) { showNotification('Aucune question', 'warning'); return; }
        showView('revision');
        setTimeout(() => { Exercises.resetSessionStats(); showCurrentQuestion(); showRevisionUI(true); }, 50);
    }

    function shuffleArray(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    function showRevisionUI(show) {
        const progress = document.getElementById('revision-progress');
        const nav = document.getElementById('revision-nav');
        if (progress) progress.style.display = show ? 'flex' : 'none';
        if (nav) nav.style.display = show ? 'flex' : 'none';
        updateProgressUI();
    }

    function showCurrentQuestion() {
        if (revisionState.currentIndex >= revisionState.questions.length) { showRevisionSummary(); return; }
        const q = revisionState.questions[revisionState.currentIndex];
        Exercises.renderQuestion(q, document.getElementById('question-container'));
        updateProgressUI();
    }

    function updateProgressUI() {
        const fill = document.getElementById('progress-fill');
        const text = document.getElementById('progress-text');
        const stats = document.getElementById('progress-stats');
        if (!fill) return;
        const total = revisionState.questions.length;
        const current = revisionState.currentIndex + 1;
        const sessionStats = Exercises.getSessionStats();
        fill.style.width = (total > 0 ? (current / total) * 100 : 0) + '%';
        text.textContent = `${current} / ${total}`;
        stats.textContent = `✓ ${sessionStats.correct}`;
    }

    function nextQuestion() {
        if (revisionState.currentIndex < revisionState.questions.length - 1) {
            revisionState.currentIndex++;
            showCurrentQuestion();
        } else {
            showRevisionSummary();
        }
    }

    function previousQuestion() {
        if (revisionState.currentIndex > 0) {
            revisionState.currentIndex--;
            showCurrentQuestion();
        }
    }

    function showRevisionSummary() {
        const container = document.getElementById('question-container');
        const stats = Exercises.getSessionStats();
        const pct = stats.answered > 0 ? Math.round((stats.correct / stats.answered) * 100) : 0;
        container.innerHTML = `
            <div class="revision-summary">
                <div class="summary-icon">${pct >= 70 ? '🎉' : pct >= 50 ? '👍' : '💪'}</div>
                <h2>Session terminée !</h2>
                <div class="summary-stats">
                    <div class="summary-stat"><span class="stat-value">${stats.answered}</span><span class="stat-label">Questions</span></div>
                    <div class="summary-stat"><span class="stat-value">${stats.correct}</span><span class="stat-label">Correctes</span></div>
                    <div class="summary-stat"><span class="stat-value">${pct}%</span><span class="stat-label">Score</span></div>
                </div>
                <div class="summary-actions">
                    <button class="btn btn-secondary" onclick="App.showView('home')">Accueil</button>
                    <button class="btn btn-primary" onclick="App.restartRevision()">Recommencer</button>
                </div>
            </div>
        `;
        showRevisionUI(false);
    }

    function restartRevision() {
        revisionState.currentIndex = 0;
        revisionState.questions = shuffleArray(revisionState.questions);
        Exercises.resetSessionStats();
        showCurrentQuestion();
        showRevisionUI(true);
    }

    function renderManageView(container) {
        container.innerHTML = `<div id="editor-container"></div>`;
        Editor.init('editor-container');
    }

    function renderImportView(container) {
        container.innerHTML = `<div id="import-container"></div>`;
        Import.init('import-container');
    }

    // ==================== SETTINGS ====================

    function renderSettingsView(container) {
        const subjects = Database.getSubjects();
        container.innerHTML = `
            <div class="settings-view">
                <h2>⚙️ Configuration des matières</h2>
                <p class="settings-help">Activez/désactivez les matières selon vos besoins.</p>

                <div class="subjects-settings">
                    ${subjects.map(s => `
                        <div class="subject-setting-row">
                            <label class="subject-toggle">
                                <input type="checkbox" ${s.enabled ? 'checked' : ''} onchange="App.toggleSubject('${s.id}', this.checked)">
                                <span class="subject-info">${s.icon} ${s.name}</span>
                            </label>
                            <button class="btn-icon" onclick="App.editSubject('${s.id}')" title="Modifier">✏️</button>
                            <button class="btn-icon btn-danger" onclick="App.deleteSubject('${s.id}')" title="Supprimer">🗑️</button>
                        </div>
                    `).join('')}
                </div>

                <div class="add-subject-form">
                    <h3>➕ Ajouter une matière</h3>
                    <div class="form-row">
                        <input type="text" id="new-subject-icon" placeholder="Icône" maxlength="2" style="width: 60px;">
                        <input type="text" id="new-subject-name" placeholder="Nom de la matière">
                        <input type="text" id="new-subject-id" placeholder="ID (ex: bio)">
                        <button class="btn btn-primary" onclick="App.addSubject()">Ajouter</button>
                    </div>
                </div>

                <div class="settings-actions">
                    <button class="btn btn-secondary" onclick="App.exportData()">💾 Exporter la base</button>
                </div>
            </div>
        `;
    }

    function toggleSubject(id, enabled) {
        Database.toggleSubject(id, enabled);
        showNotification(enabled ? 'Matière activée' : 'Matière désactivée', 'info');
    }

    function editSubject(id) {
        const subject = Database.getSubject(id);
        if (!subject) return;

        const newName = prompt('Nom de la matière :', subject.name);
        if (newName && newName !== subject.name) {
            Database.updateSubject(id, { name: newName });
            renderSettingsView(document.getElementById('main-content'));
            showNotification('Matière modifiée', 'success');
        }

        const newIcon = prompt('Icône (emoji) :', subject.icon);
        if (newIcon && newIcon !== subject.icon) {
            Database.updateSubject(id, { icon: newIcon });
            renderSettingsView(document.getElementById('main-content'));
        }
    }

    function deleteSubject(id) {
        if (!confirm('Supprimer cette matière ?')) return;
        Database.deleteSubject(id);
        renderSettingsView(document.getElementById('main-content'));
        showNotification('Matière supprimée', 'info');
    }

    function addSubject() {
        const icon = document.getElementById('new-subject-icon').value.trim() || '📚';
        const name = document.getElementById('new-subject-name').value.trim();
        const id = document.getElementById('new-subject-id').value.trim().toLowerCase().replace(/\s+/g, '-');

        if (!name || !id) { showNotification('Nom et ID requis', 'error'); return; }

        if (Database.addSubject({ id, name, icon, enabled: true })) {
            renderSettingsView(document.getElementById('main-content'));
            showNotification('Matière ajoutée', 'success');
        } else {
            showNotification('Cette matière existe déjà', 'error');
        }
    }

    // ==================== UTILITAIRES ====================

    function updateStats() {
        const questions = Database.getQuestionsByFilter({});
        const subjects = Database.getSubjects(true);
        const el1 = document.getElementById('stat-questions');
        const el2 = document.getElementById('stat-subjects');
        if (el1) el1.textContent = questions.length;
        if (el2) el2.textContent = subjects.length;
    }

    function exportData() {
        Database.downloadJSON('mes-questions.json');
        showNotification('Base exportée !', 'success');
    }

    function refreshUI() {
        showView(currentView);
    }

    function showNotification(message, type = 'info') {
        const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `<span class="notification-icon">${icons[type] || 'ℹ️'}</span><span class="notification-message">${message}</span>`;

        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            document.body.appendChild(container);
        }
        container.appendChild(notification);
        setTimeout(() => notification.classList.add('show'), 10);
        setTimeout(() => { notification.classList.remove('show'); setTimeout(() => notification.remove(), 300); }, 3000);
    }

    return {
        init, showView, startRevision, startSmartRevision, startRandomRevision, startFilteredRevision,
        updateRevisionThemes, nextQuestion, previousQuestion, restartRevision,
        toggleSubject, editSubject, deleteSubject, addSubject,
        exportData, refreshUI, showNotification
    };
})();

document.addEventListener('DOMContentLoaded', App.init);
