// Script pour la page des exercices

// Fonction pour s'assurer que AppUtils est chargé
function waitForAppUtils() {
    return new Promise((resolve) => {
        if (window.AppUtils) {
            resolve();
        } else {
            const checkInterval = setInterval(() => {
                if (window.AppUtils) {
                    clearInterval(checkInterval);
                    resolve();
                }
            }, 50);
        }
    });
}

// État global de l'application d'exercices
const appState = {
    currentExercise: 0,
    completedExercises: new Set(),
    correctExercises: new Set(),
    totalExercises: 0,
    totalPoints: 0,
    earnedPoints: 0,
    startTime: Date.now(),
    exerciseAttempts: {}
};

// Variable pour l'API client
let api;

/**
 * Initialisation de la page d'exercices
 */
document.addEventListener('DOMContentLoaded', async () => {
    // Attendre que AppUtils soit chargé
    await waitForAppUtils();

    // Initialiser l'API client
    api = new window.AppUtils.APIClient();

    window.AppUtils.log('Page d\'exercices initialisée');

    // Compter le nombre d'exercices
    const exerciseCards = document.querySelectorAll('.exercise-card');
    appState.totalExercises = exerciseCards.length;

    // Calculer le total de points
    exerciseCards.forEach(card => {
        const points = parseInt(card.dataset.points) || 0;
        appState.totalPoints += points;
    });

    // Charger la progression sauvegardée
    loadProgress();

    // Initialiser la progression
    updateGlobalProgress();

    // Gérer la touche Entrée pour soumettre
    document.querySelectorAll('.answer-input').forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const exerciseCard = input.closest('.exercise-card');
                const exerciseId = parseInt(exerciseCard.dataset.exerciseId);
                checkAnswer(exerciseId);
            }
        });
    });

    // Marquer les exercices en cours
    sessionStorage.setItem('exercisesInProgress', 'true');

    window.AppUtils.log(`${appState.totalExercises} exercices chargés (${appState.totalPoints} points)`, 'success');
});

/**
 * Afficher/masquer l'indice
 */
window.toggleHint = function(exerciseId) {
    const hintSection = document.getElementById(`hint-${exerciseId}`);
    if (!hintSection) return;

    hintSection.classList.toggle('collapsed');

    // Animation de l'apparition
    if (!hintSection.classList.contains('collapsed')) {
        hintSection.style.display = 'block';
        setTimeout(() => {
            hintSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }
};

/**
 * Vérifier une réponse
 */
window.checkAnswer = async function(exerciseId) {
    // Attendre que l'initialisation soit complète
    if (!api) {
        await waitForAppUtils();
        api = new window.AppUtils.APIClient();
    }

    window.AppUtils.log(`Vérification de l'exercice ${exerciseId}`);

    // Récupérer toutes les réponses de l'exercice
    const exerciseCard = document.querySelector(`[data-exercise-id="${exerciseId}"]`);
    const answerFields = exerciseCard.querySelectorAll('.answer-field');

    const answers = {};
    let allFilled = true;

    answerFields.forEach(field => {
        const fieldId = field.dataset.fieldId;
        const input = field.querySelector('.answer-input');
        const value = input.value.trim();

        if (!value) {
            allFilled = false;
        }

        answers[fieldId] = value;
    });

    // Vérifier que tous les champs sont remplis
    if (!allFilled) {
        window.AppUtils.window.AppUtils.showNotification('Veuillez remplir tous les champs', 'warning');
        return;
    }

    // Désactiver le bouton pendant la vérification
    const checkButton = exerciseCard.querySelector('.btn-check');
    const originalText = checkButton.textContent;
    checkButton.disabled = true;
    checkButton.textContent = 'Vérification...';

    try {
        // Appeler l'API de vérification
        const result = await api.post(`/api/check/${exerciseId}`, { answers });

        // Afficher le résultat
        displayFeedback(exerciseId, result);

        // Mettre à jour les statistiques
        appState.completedExercises.add(exerciseId);

        if (result.correct) {
            appState.correctExercises.add(exerciseId);
            const points = parseInt(exerciseCard.dataset.points) || 0;
            appState.earnedPoints += points;
            updateStatus(exerciseId, '✅');
            exerciseCard.classList.add('completed');
            exerciseCard.classList.remove('failed');
            window.AppUtils.window.AppUtils.showNotification('Bravo ! Réponse correcte', 'success');
        } else {
            updateStatus(exerciseId, '❌');
            exerciseCard.classList.add('failed');
            exerciseCard.classList.remove('completed');
            window.AppUtils.window.AppUtils.showNotification('Réponse incorrecte. Consultez la solution.', 'error');
        }

        // Mettre à jour la progression globale
        updateGlobalProgress();

        // Sauvegarder la progression
        saveProgress();

        // Vérifier si tous les exercices sont complétés
        if (appState.completedExercises.size === appState.totalExercises) {
            setTimeout(() => showSummary(), 1000);
        }

    } catch (error) {
        console.error('Erreur lors de la vérification:', error);
        window.AppUtils.showNotification('Erreur lors de la vérification. Veuillez réessayer.', 'error');
    } finally {
        checkButton.disabled = false;
        checkButton.textContent = originalText;
    }
}

/**
 * Afficher le feedback
 */
function displayFeedback(exerciseId, result) {
    const feedbackEl = document.getElementById(`feedback-${exerciseId}`);
    const exerciseCard = document.querySelector(`[data-exercise-id="${exerciseId}"]`);

    feedbackEl.className = `feedback show ${result.correct ? 'correct' : 'incorrect'}`;

    let html = '';

    // Afficher le résultat pour chaque champ
    if (result.results) {
        const answerFields = exerciseCard.querySelectorAll('.answer-field');

        answerFields.forEach(field => {
            const fieldId = field.dataset.fieldId;
            const input = field.querySelector('.answer-input');
            const statusEl = field.querySelector('.field-status');
            const isCorrect = result.results[fieldId];

            if (isCorrect) {
                input.classList.add('correct');
                input.classList.remove('incorrect');
                statusEl.textContent = '✓';
                statusEl.style.color = 'var(--success)';
            } else {
                input.classList.add('incorrect');
                input.classList.remove('correct');
                statusEl.textContent = '✗';
                statusEl.style.color = 'var(--danger)';
            }
        });
    }

    // Message principal
    if (result.correct) {
        html += '<p><strong>✅ Excellent !</strong> Votre réponse est correcte.</p>';
    } else {
        html += '<p><strong>❌ Réponse incorrecte.</strong> Révisez votre calcul ou consultez la solution ci-dessous.</p>';
    }

    // Afficher la solution si incorrecte
    if (!result.correct && result.solution) {
        html += `
            <details style="margin-top: 1rem;">
                <summary style="cursor: pointer; font-weight: 700; padding: 0.5rem; background: rgba(255, 255, 255, 0.5); border-radius: 4px;">
                    📖 Voir la solution détaillée
                </summary>
                <div style="margin-top: 1rem; padding: 1rem; background: white; border-radius: 8px; border-left: 4px solid var(--info);">
                    ${result.solution}
                </div>
            </details>
        `;
    }

    feedbackEl.innerHTML = html;

    // Re-render MathJax pour les formules dans le feedback
    if (window.MathJax && MathJax.typesetPromise) {
        MathJax.typesetPromise([feedbackEl]).catch(err => console.error('Erreur MathJax:', err));
    }

    // Scroller vers le feedback
    setTimeout(() => {
        feedbackEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

/**
 * Mettre à jour le statut d'un exercice
 */
function updateStatus(exerciseId, emoji) {
    const statusEl = document.getElementById(`status-${exerciseId}`);
    if (statusEl) {
        statusEl.textContent = emoji;
    }
}

/**
 * Mettre à jour la progression globale
 */
function updateGlobalProgress() {
    const progressBar = document.getElementById('globalProgressBar');
    const progressText = document.getElementById('progressText');
    const progressScore = document.getElementById('progressScore');

    if (!progressBar || !progressText || !progressScore) return;

    const completed = appState.completedExercises.size;
    const percentage = (completed / appState.totalExercises) * 100;
    const score = appState.totalPoints > 0 ? ((appState.earnedPoints / appState.totalPoints) * 100).toFixed(1) : 0;

    progressBar.style.width = `${percentage}%`;
    progressText.textContent = `${completed} / ${appState.totalExercises} exercices complétés`;
    progressScore.textContent = `Score : ${score}%`;
}

/**
 * Afficher le résumé final
 */
function showSummary() {
    const summarySection = document.getElementById('summarySection');
    const finalScore = document.getElementById('finalScore');
    const correctCount = document.getElementById('correctCount');
    const totalTime = document.getElementById('totalTime');

    if (!summarySection) return;

    const elapsedTime = Math.floor((Date.now() - appState.startTime) / 1000);
    const score = appState.totalPoints > 0 ? ((appState.earnedPoints / appState.totalPoints) * 100).toFixed(1) : 0;

    finalScore.textContent = `${score}%`;
    correctCount.textContent = `${appState.correctExercises.size} / ${appState.totalExercises}`;
    totalTime.textContent = window.AppUtils.formatTime(elapsedTime);

    summarySection.style.display = 'block';
    summarySection.scrollIntoView({ behavior: 'smooth' });

    // Retirer le flag d'exercices en cours
    sessionStorage.removeItem('exercisesInProgress');

    window.AppUtils.log('Tous les exercices complétés !', 'success');
    window.AppUtils.showNotification('Félicitations ! Tous les exercices sont terminés 🎉', 'success', 5000);
};

/**
 * Réinitialiser les exercices
 */
window.resetExercises = async function() {
    // Attendre que l'initialisation soit complète
    if (!api) {
        await waitForAppUtils();
        api = new window.AppUtils.APIClient();
    }
    if (!confirm('Voulez-vous vraiment recommencer tous les exercices ?')) {
        return;
    }

    // Réinitialiser l'état
    appState.completedExercises.clear();
    appState.correctExercises.clear();
    appState.earnedPoints = 0;
    appState.startTime = Date.now();
    appState.exerciseAttempts = {};

    // Réinitialiser l'UI
    document.querySelectorAll('.answer-input').forEach(input => {
        input.value = '';
        input.classList.remove('correct', 'incorrect');
    });

    document.querySelectorAll('.field-status').forEach(el => {
        el.textContent = '';
    });

    document.querySelectorAll('.feedback').forEach(el => {
        el.className = 'feedback';
    });

    document.querySelectorAll('.exercise-status').forEach(el => {
        el.textContent = '';
    });

    document.querySelectorAll('.exercise-card').forEach(card => {
        card.classList.remove('completed', 'failed');
    });

    document.querySelectorAll('.hint-section').forEach(hint => {
        hint.classList.add('collapsed');
    });

    document.getElementById('summarySection').style.display = 'none';

    // Mettre à jour la progression
    updateGlobalProgress();

    // Sauvegarder la réinitialisation
    saveProgress();

    // Scroller en haut
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Marquer les exercices comme en cours
    sessionStorage.setItem('exercisesInProgress', 'true');

    window.AppUtils.showNotification('Exercices réinitialisés', 'info');
    window.AppUtils.log('Exercices réinitialisés', 'info');
};

/**
 * Sauvegarder la progression
 */
function saveProgress() {
    const progress = {
        completedExercises: Array.from(appState.completedExercises),
        correctExercises: Array.from(appState.correctExercises),
        earnedPoints: appState.earnedPoints,
        startTime: appState.startTime,
        exerciseAttempts: appState.exerciseAttempts
    };

    window.AppUtils.saveToLocalStorage('exercisesProgress', progress);
    window.AppUtils.log('Progression sauvegardée', 'success');
}

/**
 * Charger la progression
 */
function loadProgress() {
    if (!loadFromLocalStorage) return;

    const progress = window.AppUtils.loadFromLocalStorage('exercisesProgress');

    if (progress) {
        appState.completedExercises = new Set(progress.completedExercises || []);
        appState.correctExercises = new Set(progress.correctExercises || []);
        appState.earnedPoints = progress.earnedPoints || 0;
        appState.startTime = progress.startTime || Date.now();
        appState.exerciseAttempts = progress.exerciseAttempts || {};

        // Restaurer l'état visuel
        appState.completedExercises.forEach(exerciseId => {
            const card = document.querySelector(`[data-exercise-id="${exerciseId}"]`);
            if (card) {
                if (appState.correctExercises.has(exerciseId)) {
                    updateStatus(exerciseId, '✅');
                    card.classList.add('completed');
                } else {
                    updateStatus(exerciseId, '❌');
                    card.classList.add('failed');
                }
            }
        });

        window.AppUtils.log('Progression chargée', 'info');
    }
}

// Les fonctions sont déjà accessibles globalement via window.checkAnswer, window.toggleHint et window.resetExercises
