/**
 * Module Database - Gestion de la base de données JSON via Tauri
 * Lecture/écriture directe dans le fichier JSON à côté de l'exécutable
 */
const Database = (function() {
    'use strict';

    let data = null;
    let listeners = [];
    let isReady = false;
    let dbPath = '';

    // API Tauri
    const { invoke } = window.__TAURI__.tauri;

    /**
     * Initialise la base de données en chargeant le JSON
     */
    async function init() {
        try {
            // Charger le chemin pour affichage
            dbPath = await invoke('get_database_path');

            // Charger les données
            const content = await invoke('load_database');
            data = JSON.parse(content);
            isReady = true;

            console.log('[DB] Chargé depuis:', dbPath);
            notifyListeners('init');
            return data;
        } catch (e) {
            console.error('[DB] Erreur chargement:', e);
            // Base vide par défaut
            data = createEmpty();
            isReady = true;
            return data;
        }
    }

    function createEmpty() {
        return {
            subjects: [
                { id: 'maths', name: 'Mathématiques', icon: '📐', enabled: true },
                { id: 'physique', name: 'Physique-Chimie', icon: '⚗️', enabled: true },
                { id: 'francais', name: 'Français', icon: '📖', enabled: true }
            ],
            questions: []
        };
    }

    /**
     * Sauvegarde les données dans le fichier JSON via Tauri
     */
    async function save() {
        if (!data) return false;

        try {
            const content = JSON.stringify(data, null, 2);
            await invoke('save_database', { content });
            console.log('[DB] Sauvegardé');
            return true;
        } catch (e) {
            console.error('[DB] Erreur sauvegarde:', e);
            return false;
        }
    }

    function getStatus() {
        return {
            ready: isReady,
            path: dbPath
        };
    }

    function exportJSON() {
        return JSON.stringify(data, null, 2);
    }

    function downloadJSON(filename = 'questions.json') {
        const blob = new Blob([exportJSON()], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    }

    // ==================== MATIÈRES ====================

    function getSubjects(enabledOnly = false) {
        const subjects = data?.subjects || [];
        return enabledOnly ? subjects.filter(s => s.enabled) : subjects;
    }

    function getSubject(id) {
        return data?.subjects.find(s => s.id === id) || null;
    }

    function addSubject(subject) {
        if (!data || !subject.id || !subject.name) return false;
        if (data.subjects.some(s => s.id === subject.id)) return false;

        data.subjects.push({
            id: subject.id,
            name: subject.name,
            icon: subject.icon || '📚',
            enabled: subject.enabled !== false
        });
        save();
        notifyListeners('subject-add', subject);
        return true;
    }

    function updateSubject(id, updates) {
        const subject = getSubject(id);
        if (!subject) return false;

        Object.assign(subject, updates);
        save();
        notifyListeners('subject-update', subject);
        return true;
    }

    function toggleSubject(id, enabled) {
        return updateSubject(id, { enabled });
    }

    function deleteSubject(id) {
        if (!data) return false;
        const index = data.subjects.findIndex(s => s.id === id);
        if (index === -1) return false;

        data.subjects.splice(index, 1);
        save();
        notifyListeners('subject-delete', id);
        return true;
    }

    // ==================== QUESTIONS ====================

    function getAllQuestions() {
        return data?.questions || [];
    }

    function getQuestion(id) {
        return data?.questions.find(q => q.id === id) || null;
    }

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

        const themes = [...new Set(questions.map(q => q.theme).filter(Boolean))];
        return themes.sort();
    }

    function addQuestions(questions) {
        if (!data) return { added: [], errors: [] };

        const toAdd = Array.isArray(questions) ? questions : [questions];
        const results = { added: [], errors: [] };

        for (const q of toAdd) {
            const validation = validateQuestion(q);
            if (!validation.valid) {
                results.errors.push({ question: q, error: validation.error });
                continue;
            }

            if (!q.id) q.id = generateId();
            if (data.questions.some(e => e.id === q.id)) q.id = generateId();

            if (!q.stats) {
                q.stats = { accessCount: 0, correctCount: 0, lastAccessed: null };
            }

            if (!getSubject(q.subject)) {
                addSubject({ id: q.subject, name: q.subject, enabled: true });
            }

            data.questions.push(q);
            results.added.push(q);
        }

        if (results.added.length > 0) {
            save();
            notifyListeners('add', results.added);
        }

        return results;
    }

    function updateQuestion(id, updates) {
        const index = data?.questions.findIndex(q => q.id === id);
        if (index === -1) return { success: false, error: 'Question non trouvée' };

        const updated = { ...data.questions[index], ...updates, id };
        const validation = validateQuestion(updated);
        if (!validation.valid) return { success: false, error: validation.error };

        data.questions[index] = updated;
        save();
        notifyListeners('update', updated);
        return { success: true, question: updated };
    }

    function deleteQuestion(id) {
        const index = data?.questions.findIndex(q => q.id === id);
        if (index === -1) return { success: false, error: 'Question non trouvée' };

        const deleted = data.questions.splice(index, 1)[0];
        save();
        notifyListeners('delete', deleted);
        return { success: true, question: deleted };
    }

    function importFromJSON(jsonString) {
        try {
            const imported = JSON.parse(jsonString);

            if (Array.isArray(imported)) {
                return addQuestions(imported);
            }

            if (imported.questions && Array.isArray(imported.questions)) {
                if (imported.subjects) {
                    for (const s of imported.subjects) {
                        if (!getSubject(s.id)) addSubject(s);
                    }
                }
                return addQuestions(imported.questions);
            }

            if (imported.question || imported.type) {
                return addQuestions([imported]);
            }

            return { added: [], errors: [{ error: 'Format JSON non reconnu' }] };
        } catch (e) {
            return { added: [], errors: [{ error: 'JSON invalide: ' + e.message }] };
        }
    }

    // ==================== STATS ====================

    function recordAccess(questionId, isCorrect = null) {
        const question = getQuestion(questionId);
        if (!question) return false;

        question.stats = question.stats || { accessCount: 0, correctCount: 0, lastAccessed: null };
        question.stats.accessCount++;
        question.stats.lastAccessed = new Date().toISOString();

        if (isCorrect) question.stats.correctCount++;

        save();
        return true;
    }

    function resetStats(questionId = null) {
        if (questionId) {
            const q = getQuestion(questionId);
            if (q) q.stats = { accessCount: 0, correctCount: 0, lastAccessed: null };
        } else {
            data.questions.forEach(q => {
                q.stats = { accessCount: 0, correctCount: 0, lastAccessed: null };
            });
        }
        save();
        notifyListeners('stats-reset', questionId);
        return true;
    }

    function getQuestionsForRevision(count = 10, filter = {}) {
        let questions = getQuestionsByFilter(filter);

        questions.sort((a, b) => {
            const aCount = a.stats?.accessCount || 0;
            const bCount = b.stats?.accessCount || 0;
            if (aCount !== bCount) return aCount - bCount;

            const aDate = a.stats?.lastAccessed ? new Date(a.stats.lastAccessed) : new Date(0);
            const bDate = b.stats?.lastAccessed ? new Date(b.stats.lastAccessed) : new Date(0);
            return aDate - bDate;
        });

        return questions.slice(0, count);
    }

    // ==================== UTILITAIRES ====================

    function generateId() {
        return 'q' + Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    }

    function validateQuestion(q) {
        if (!q.type || !['qcm', 'input'].includes(q.type)) {
            return { valid: false, error: 'Type invalide (qcm ou input)' };
        }
        if (!q.question) {
            return { valid: false, error: 'Question manquante' };
        }
        if (!q.subject) {
            return { valid: false, error: 'Matière (subject) manquante' };
        }

        if (q.type === 'qcm') {
            if (!Array.isArray(q.choices) || q.choices.length < 2) {
                return { valid: false, error: 'QCM: au moins 2 choix requis' };
            }
            if (!Array.isArray(q.correctAnswers) || q.correctAnswers.length === 0) {
                return { valid: false, error: 'QCM: correctAnswers requis' };
            }
        }

        if (q.type === 'input') {
            if (!Array.isArray(q.fields) || q.fields.length === 0) {
                return { valid: false, error: 'Input: au moins un champ requis' };
            }
        }

        return { valid: true };
    }

    function addListener(callback) {
        listeners.push(callback);
        return () => { listeners = listeners.filter(l => l !== callback); };
    }

    function notifyListeners(event, payload) {
        listeners.forEach(l => { try { l(event, payload); } catch (e) { console.error(e); } });
    }

    // API Publique
    return {
        init, save, getStatus, exportJSON, downloadJSON,
        getSubjects, getSubject, addSubject, updateSubject, toggleSubject, deleteSubject,
        getAllQuestions, getQuestion, getQuestionsByFilter, getThemes,
        addQuestions, updateQuestion, deleteQuestion, importFromJSON,
        recordAccess, resetStats, getQuestionsForRevision,
        addListener
    };
})();
