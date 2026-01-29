/**
 * Script de build pour Tauri
 * Usage: node build.js
 */
const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, 'src');
const DIST_DIR = path.join(__dirname, 'dist');
const DATA_DIR = path.join(__dirname, 'data');

const CSS_FILES = ['css/main.css'];
const JS_FILES = ['js/exercises.js', 'js/import.js', 'js/editor.js', 'js/app.js'];

function readFile(filePath) {
    try {
        return fs.readFileSync(path.join(SRC_DIR, filePath), 'utf-8');
    } catch (e) {
        console.error(`Erreur lecture ${filePath}:`, e.message);
        return '';
    }
}

function build() {
    console.log('Build Tauri en cours...');

    const allCSS = CSS_FILES.map(readFile).join('\n');
    const allJS = JS_FILES.map(readFile).join('\n\n');

    // Module Database pour Tauri (utilise invoke)
    const databaseJS = `
/**
 * Module Database - Gestion via Tauri
 */
const Database = (function() {
    'use strict';

    let data = null;
    let listeners = [];
    let isReady = false;
    let dbPath = '';

    const { invoke } = window.__TAURI__.tauri;

    async function init() {
        try {
            dbPath = await invoke('get_database_path');
            const content = await invoke('load_database');
            data = JSON.parse(content);
            isReady = true;
            console.log('[DB] Chargé depuis:', dbPath);
            notifyListeners('init');
            return data;
        } catch (e) {
            console.error('[DB] Erreur:', e);
            data = { subjects: [], questions: [] };
            isReady = true;
            return data;
        }
    }

    async function save() {
        if (!data) return false;
        try {
            await invoke('save_database', { content: JSON.stringify(data, null, 2) });
            return true;
        } catch (e) {
            console.error('[DB] Erreur sauvegarde:', e);
            return false;
        }
    }

    function getStatus() { return { ready: isReady, path: dbPath }; }
    function exportJSON() { return JSON.stringify(data, null, 2); }
    function downloadJSON(filename = 'questions.json') {
        const blob = new Blob([exportJSON()], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = filename; a.click();
        URL.revokeObjectURL(url);
    }

    function getSubjects(enabledOnly = false) {
        const subjects = data?.subjects || [];
        return enabledOnly ? subjects.filter(s => s.enabled) : subjects;
    }
    function getSubject(id) { return data?.subjects.find(s => s.id === id) || null; }

    function addSubject(subject) {
        if (!data || !subject.id || !subject.name) return false;
        if (data.subjects.some(s => s.id === subject.id)) return false;
        data.subjects.push({ id: subject.id, name: subject.name, icon: subject.icon || '📚', enabled: subject.enabled !== false });
        save(); notifyListeners('subject-add', subject); return true;
    }

    function updateSubject(id, updates) {
        const subject = getSubject(id);
        if (!subject) return false;
        Object.assign(subject, updates);
        save(); notifyListeners('subject-update', subject); return true;
    }

    function toggleSubject(id, enabled) { return updateSubject(id, { enabled }); }

    function deleteSubject(id) {
        if (!data) return false;
        const index = data.subjects.findIndex(s => s.id === id);
        if (index === -1) return false;
        data.subjects.splice(index, 1);
        save(); notifyListeners('subject-delete', id); return true;
    }

    function getAllQuestions() { return data?.questions || []; }
    function getQuestion(id) { return data?.questions.find(q => q.id === id) || null; }

    function getQuestionsByFilter({ subject, theme, difficulty } = {}) {
        let questions = getAllQuestions();
        const enabledSubjects = getSubjects(true).map(s => s.id);
        questions = questions.filter(q => enabledSubjects.includes(q.subject));
        if (subject) questions = questions.filter(q => q.subject === subject);
        if (theme) questions = questions.filter(q => q.theme === theme);
        if (difficulty) questions = questions.filter(q => q.difficulty === difficulty);
        return questions;
    }

    function getThemes(subjectId = null) {
        let questions = getAllQuestions();
        if (subjectId) questions = questions.filter(q => q.subject === subjectId);
        return [...new Set(questions.map(q => q.theme).filter(Boolean))].sort();
    }

    function generateId() { return 'q' + Date.now().toString(36) + Math.random().toString(36).substr(2, 5); }

    function validateQuestion(q) {
        if (!q.type || !['qcm', 'input'].includes(q.type)) return { valid: false, error: 'Type invalide' };
        if (!q.question) return { valid: false, error: 'Question manquante' };
        if (!q.subject) return { valid: false, error: 'Matière manquante' };
        if (q.type === 'qcm') {
            if (!Array.isArray(q.choices) || q.choices.length < 2) return { valid: false, error: 'QCM: 2+ choix' };
            if (!Array.isArray(q.correctAnswers) || !q.correctAnswers.length) return { valid: false, error: 'QCM: correctAnswers' };
        }
        if (q.type === 'input' && (!Array.isArray(q.fields) || !q.fields.length)) return { valid: false, error: 'Input: champs' };
        return { valid: true };
    }

    function addQuestions(questions) {
        if (!data) return { added: [], errors: [] };
        const toAdd = Array.isArray(questions) ? questions : [questions];
        const results = { added: [], errors: [] };
        for (const q of toAdd) {
            const v = validateQuestion(q);
            if (!v.valid) { results.errors.push({ question: q, error: v.error }); continue; }
            if (!q.id) q.id = generateId();
            if (data.questions.some(e => e.id === q.id)) q.id = generateId();
            if (!q.stats) q.stats = { accessCount: 0, correctCount: 0, lastAccessed: null };
            if (!getSubject(q.subject)) addSubject({ id: q.subject, name: q.subject, enabled: true });
            data.questions.push(q); results.added.push(q);
        }
        if (results.added.length > 0) { save(); notifyListeners('add', results.added); }
        return results;
    }

    function updateQuestion(id, updates) {
        const index = data?.questions.findIndex(q => q.id === id);
        if (index === -1) return { success: false, error: 'Non trouvée' };
        const updated = { ...data.questions[index], ...updates, id };
        const v = validateQuestion(updated);
        if (!v.valid) return { success: false, error: v.error };
        data.questions[index] = updated;
        save(); notifyListeners('update', updated);
        return { success: true, question: updated };
    }

    function deleteQuestion(id) {
        const index = data?.questions.findIndex(q => q.id === id);
        if (index === -1) return { success: false, error: 'Non trouvée' };
        const deleted = data.questions.splice(index, 1)[0];
        save(); notifyListeners('delete', deleted);
        return { success: true, question: deleted };
    }

    function importFromJSON(jsonString) {
        try {
            const imported = JSON.parse(jsonString);
            if (Array.isArray(imported)) return addQuestions(imported);
            if (imported.questions && Array.isArray(imported.questions)) {
                if (imported.subjects) { for (const s of imported.subjects) { if (!getSubject(s.id)) addSubject(s); } }
                return addQuestions(imported.questions);
            }
            if (imported.question || imported.type) return addQuestions([imported]);
            return { added: [], errors: [{ error: 'Format non reconnu' }] };
        } catch (e) { return { added: [], errors: [{ error: 'JSON invalide' }] }; }
    }

    function recordAccess(questionId, isCorrect = null) {
        const question = getQuestion(questionId);
        if (!question) return false;
        question.stats = question.stats || { accessCount: 0, correctCount: 0, lastAccessed: null };
        question.stats.accessCount++;
        question.stats.lastAccessed = new Date().toISOString();
        if (isCorrect) question.stats.correctCount++;
        save(); return true;
    }

    function resetStats(questionId = null) {
        if (questionId) { const q = getQuestion(questionId); if (q) q.stats = { accessCount: 0, correctCount: 0, lastAccessed: null }; }
        else { data.questions.forEach(q => { q.stats = { accessCount: 0, correctCount: 0, lastAccessed: null }; }); }
        save(); notifyListeners('stats-reset', questionId); return true;
    }

    function getQuestionsForRevision(count = 10, filter = {}) {
        let questions = getQuestionsByFilter(filter);
        questions.sort((a, b) => {
            const aCount = a.stats?.accessCount || 0, bCount = b.stats?.accessCount || 0;
            if (aCount !== bCount) return aCount - bCount;
            const aDate = a.stats?.lastAccessed ? new Date(a.stats.lastAccessed) : new Date(0);
            const bDate = b.stats?.lastAccessed ? new Date(b.stats.lastAccessed) : new Date(0);
            return aDate - bDate;
        });
        return questions.slice(0, count);
    }

    function addListener(cb) { listeners.push(cb); return () => { listeners = listeners.filter(l => l !== cb); }; }
    function notifyListeners(event, payload) { listeners.forEach(l => { try { l(event, payload); } catch (e) {} }); }

    return {
        init, save, getStatus, exportJSON, downloadJSON,
        getSubjects, getSubject, addSubject, updateSubject, toggleSubject, deleteSubject,
        getAllQuestions, getQuestion, getQuestionsByFilter, getThemes,
        addQuestions, updateQuestion, deleteQuestion, importFromJSON,
        recordAccess, resetStats, getQuestionsForRevision, addListener
    };
})();
`;

    const html = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application de Révisions</title>
    <script>
        MathJax = {
            tex: { inlineMath: [['$', '$']], displayMath: [['$$', '$$']], processEscapes: true },
            options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'] },
            loader: { load: ['[tex]/mhchem'] },
            tex: { packages: {'[+]': ['mhchem']} }
        };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
    <style>
${allCSS}
    </style>
</head>
<body>
    <nav id="main-nav" class="main-nav"></nav>
    <main id="main-content" class="main-content"></main>
    <script src="https://unpkg.com/@tauri-apps/api@1/dist/tauri.min.js"></script>
    <script>
${databaseJS}

${allJS}
    </script>
</body>
</html>`;

    if (!fs.existsSync(DIST_DIR)) {
        fs.mkdirSync(DIST_DIR, { recursive: true });
    }

    // index.html pour Tauri
    fs.writeFileSync(path.join(DIST_DIR, 'index.html'), html, 'utf-8');
    console.log('✅ Créé: dist/index.html');

    // Copier questions.json
    const dataSource = path.join(DATA_DIR, 'questions.json');
    if (fs.existsSync(dataSource)) {
        fs.copyFileSync(dataSource, path.join(DIST_DIR, 'questions.json'));
        console.log('✅ Copié: dist/questions.json');
    }

    console.log('\n📦 Build Tauri terminé !');
    console.log('\nPour lancer en dev: cd src-tauri && cargo tauri dev');
    console.log('Pour builder: cd src-tauri && cargo tauri build');
}

build();
