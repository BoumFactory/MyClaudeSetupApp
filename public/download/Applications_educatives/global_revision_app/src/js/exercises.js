/**
 * Module Exercises - Logique de révision et vérification des réponses
 */
const Exercises = (function() {
    'use strict';

    let currentQuestion = null;
    let sessionStats = { answered: 0, correct: 0, startTime: null };

    function renderQuestion(question, container) {
        if (!question || !container) return;
        currentQuestion = question;
        Database.recordAccess(question.id);

        container.innerHTML = buildQuestionHTML(question);
        renderMath(container);
        highlightCode(container);
    }

    function buildQuestionHTML(q) {
        const stars = '★'.repeat(q.difficulty || 1) + '☆'.repeat(3 - (q.difficulty || 1));
        const subject = Database.getSubject(q.subject);
        const subjectName = subject ? `${subject.icon} ${subject.name}` : q.subject;
        const accessCount = q.stats?.accessCount || 0;

        return `
            <div class="question-card" data-id="${q.id}" data-type="${q.type}">
                <div class="question-header">
                    <span class="question-meta">
                        <span class="subject-badge">${subjectName}</span>
                        ${q.theme ? `<span class="theme-badge">${q.theme}</span>` : ''}
                    </span>
                    <span class="question-info">
                        <span class="difficulty" title="Difficulté">${stars}</span>
                        <span class="access-count" title="Nombre de révisions">👁 ${accessCount}</span>
                    </span>
                </div>

                <div class="question-content">${q.question}</div>

                <form class="answer-form" onsubmit="return false;">
                    ${q.type === 'qcm' ? buildQCMFields(q) : buildInputFields(q)}
                    <div class="question-actions">
                        ${q.hint ? `<button type="button" class="btn btn-secondary btn-hint" onclick="Exercises.showHint()">💡 Indice</button>` : ''}
                        <button type="button" class="btn btn-primary btn-check" onclick="Exercises.checkAnswer()">Vérifier</button>
                    </div>
                </form>

                <div class="hint-container" style="display: none;">
                    <div class="hint-content">${q.hint || ''}</div>
                </div>

                <div class="feedback-container" style="display: none;"></div>
            </div>
        `;
    }

    function buildQCMFields(q) {
        const isMultiple = q.correctAnswers.length > 1;
        const inputType = isMultiple ? 'checkbox' : 'radio';

        return '<div class="choices-container">' +
            q.choices.map(c => `
                <label class="choice-label">
                    <input type="${inputType}" name="answer" value="${c.id}">
                    <span class="choice-text">${c.text}</span>
                </label>
            `).join('') + '</div>';
    }

    function buildInputFields(q) {
        return '<div class="fields-container">' +
            q.fields.map(f => `
                <div class="field-group">
                    <label for="field-${f.id}">${f.label || 'Réponse :'}</label>
                    ${f.options
                        ? `<select id="field-${f.id}" name="${f.id}" class="field-input">
                             <option value="">-- Choisir --</option>
                             ${f.options.map(o => `<option value="${o}">${o}</option>`).join('')}
                           </select>`
                        : `<input type="text" id="field-${f.id}" name="${f.id}" class="field-input" autocomplete="off">`
                    }
                </div>
            `).join('') + '</div>';
    }

    function showHint() {
        const hint = document.querySelector('.hint-container');
        if (hint) {
            hint.style.display = 'block';
            renderMath(hint);
        }
    }

    function checkAnswer() {
        if (!currentQuestion) return;
        const form = document.querySelector('.answer-form');
        if (!form) return;

        const results = currentQuestion.type === 'qcm' ? checkQCM(form) : checkInputs(form);

        sessionStats.answered++;
        if (results.correct) {
            sessionStats.correct++;
            Database.recordAccess(currentQuestion.id, true);
        }

        displayFeedback(results.correct, results);
        disableForm(form);

        return results;
    }

    function checkQCM(form) {
        const selected = Array.from(form.querySelectorAll('input[name="answer"]:checked')).map(i => i.value);
        const correct = currentQuestion.correctAnswers;

        const isCorrect = selected.length === correct.length &&
            selected.every(s => correct.includes(s)) &&
            correct.every(c => selected.includes(c));

        form.querySelectorAll('.choice-label').forEach(label => {
            const id = label.querySelector('input').value;
            if (correct.includes(id)) label.classList.add('correct');
            if (selected.includes(id) && !correct.includes(id)) label.classList.add('incorrect');
        });

        return { correct: isCorrect, selected, expected: correct };
    }

    function checkInputs(form) {
        const results = { correct: true, fields: {} };

        for (const field of currentQuestion.fields) {
            const input = form.querySelector(`[name="${field.id}"]`);
            if (!input) continue;

            const userAnswer = input.value.trim();
            const isFieldCorrect = checkFieldAnswer(userAnswer, field);

            results.fields[field.id] = { correct: isFieldCorrect, userAnswer, expected: field.answer };
            input.classList.add(isFieldCorrect ? 'correct' : 'incorrect');

            if (!isFieldCorrect) results.correct = false;
        }

        return results;
    }

    function checkFieldAnswer(userAnswer, field) {
        const normalize = s => s.toLowerCase().replace(/\s+/g, '').replace(/,/g, '.').replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
        const normalizedUser = normalize(userAnswer);
        const normalizedExpected = normalize(String(field.answer));

        if (normalizedUser === normalizedExpected) return true;

        if (field.type === 'number') {
            const tolerance = field.tolerance || 0;
            const userNum = parseFloat(normalizedUser);
            const expectedNum = parseFloat(field.answer);
            if (!isNaN(userNum) && !isNaN(expectedNum)) {
                return Math.abs(userNum - expectedNum) <= tolerance;
            }
        }

        if (field.alternatives) {
            for (const alt of field.alternatives) {
                if (normalizedUser === normalize(String(alt))) return true;
            }
        }

        return false;
    }

    function displayFeedback(isCorrect, results) {
        const container = document.querySelector('.feedback-container');
        if (!container) return;

        let html = `
            <div class="feedback ${isCorrect ? 'feedback-correct' : 'feedback-incorrect'}">
                <div class="feedback-header">${isCorrect ? '✅ Bravo !' : '❌ Pas tout à fait...'}</div>
        `;

        if (currentQuestion.explanation) {
            html += `<div class="feedback-explanation"><strong>Explication :</strong><div>${currentQuestion.explanation}</div></div>`;
        }

        if (!isCorrect && currentQuestion.type === 'input') {
            html += '<div class="expected-answers"><strong>Réponses attendues :</strong><ul>';
            for (const f of currentQuestion.fields) {
                html += `<li>${f.label || f.id} ${f.answer}</li>`;
            }
            html += '</ul></div>';
        }

        html += '</div>';
        container.innerHTML = html;
        container.style.display = 'block';
        renderMath(container);
    }

    function disableForm(form) {
        form.querySelectorAll('input, select, button').forEach(el => {
            if (el.classList.contains('btn-check')) el.style.display = 'none';
            else el.disabled = true;
        });
        const hint = form.querySelector('.btn-hint');
        if (hint) hint.style.display = 'none';
    }

    function renderMath(container) {
        if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise([container]).catch(e => console.warn('[MathJax]', e));
        }
    }

    function highlightCode(container) {
        if (window.hljs) {
            container.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
        }
    }

    function getSessionStats() { return { ...sessionStats }; }
    function resetSessionStats() { sessionStats = { answered: 0, correct: 0, startTime: Date.now() }; }

    return { renderQuestion, showHint, checkAnswer, getSessionStats, resetSessionStats };
})();
