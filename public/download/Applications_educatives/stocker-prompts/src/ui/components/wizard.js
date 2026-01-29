/**
 * Composant Wizard - Arbre décisionnel pour catégoriser un prompt
 * Structure: Action → Matière → Niveau → Thème
 */

import { ACTIONS, ACTION_CATEGORIES } from '../../config/actions.js';
import { DEFAULT_SUBJECTS, DEFAULT_LEVELS } from '../../config/subjects.js';
import { db } from '../../core/database.js';

class Wizard {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.currentStep = 0;
    this.steps = ['action', 'subject', 'level', 'theme'];
    this.selection = {
      action: null,
      subject: null,
      level: null,
      theme: ''
    };
    this.onComplete = null;
    this.onCancel = null;
  }

  /**
   * Démarre le wizard
   * @param {Object} options - Options du wizard
   * @param {Function} options.onComplete - Callback à la fin
   * @param {Function} options.onCancel - Callback annulation
   * @param {Object} options.prefill - Valeurs pré-remplies {level, subject, theme}
   */
  start(options = {}) {
    this.onComplete = options.onComplete || (() => {});
    this.onCancel = options.onCancel || (() => {});
    this.currentStep = 0;

    // Initialiser avec les valeurs pré-remplies
    const prefill = options.prefill || {};
    this.selection = {
      action: null,
      subject: prefill.subject || null,
      level: prefill.level || null,
      theme: prefill.theme || ''
    };

    this.render();
  }

  /**
   * Rendu principal
   */
  render() {
    const step = this.steps[this.currentStep];
    const settings = db.getSettings();

    // Vérifier si l'étape peut être sautée
    const canSkip = this.canSkipStep(step, settings);

    // Générer les boutons de navigation
    const navButtons = this.renderNavButtons(canSkip);

    let html = `
      <div class="wizard">
        <div class="wizard-progress">
          ${this.steps.map((s, i) => `
            <div class="wizard-step ${i === this.currentStep ? 'active' : ''} ${i < this.currentStep ? 'completed' : ''}">
              <span class="step-number">${i + 1}</span>
              <span class="step-label">${this.getStepLabel(s)}</span>
            </div>
          `).join('<div class="wizard-step-connector"></div>')}
        </div>

        <!-- Boutons en haut (sticky) -->
        <div class="wizard-actions wizard-actions-top">
          ${navButtons}
        </div>

        <div class="wizard-content">
    `;

    switch (step) {
      case 'action':
        html += this.renderActionStep(settings);
        break;
      case 'subject':
        html += this.renderSubjectStep(settings);
        break;
      case 'level':
        html += this.renderLevelStep(settings);
        break;
      case 'theme':
        html += this.renderThemeStep();
        break;
    }

    html += `
        </div>

        <!-- Boutons en bas -->
        <div class="wizard-actions wizard-actions-bottom">
          ${navButtons}
        </div>
      </div>
    `;

    this.container.innerHTML = html;
    this.bindEvents();
  }

  /**
   * Vérifie si l'étape peut être sautée
   */
  canSkipStep(step, settings) {
    switch (step) {
      case 'level':
        // On peut sauter si un niveau par défaut est défini ou déjà pré-rempli
        return !!(settings.defaultLevel || this.selection.level);
      case 'theme':
        // Le thème est toujours optionnel
        return true;
      case 'subject':
        // On peut sauter si déjà pré-rempli
        return !!this.selection.subject;
      default:
        return false;
    }
  }

  /**
   * Génère les boutons de navigation
   */
  renderNavButtons(canSkip) {
    const isLastStep = this.currentStep >= this.steps.length - 1;

    let buttons = '';

    // Bouton Retour/Annuler
    if (this.currentStep > 0) {
      buttons += '<button class="btn btn-secondary wizard-back">← Retour</button>';
    } else {
      buttons += '<button class="btn btn-secondary wizard-cancel">Annuler</button>';
    }

    // Bouton Passer (si disponible)
    if (canSkip && !isLastStep) {
      buttons += '<button class="btn btn-outline wizard-skip">Passer ⏭</button>';
    }

    // Bouton Suivant/Terminer
    if (!isLastStep) {
      buttons += '<button class="btn btn-primary wizard-next" disabled>Suivant →</button>';
    } else {
      buttons += '<button class="btn btn-success wizard-finish" disabled>Terminer ✓</button>';
    }

    return buttons;
  }

  getStepLabel(step) {
    const labels = {
      action: 'Action',
      subject: 'Matière',
      level: 'Niveau',
      theme: 'Thème'
    };
    return labels[step] || step;
  }

  renderActionStep(settings) {
    const enabledActions = settings.enabledActions || [];
    const actions = ACTIONS.filter(a => enabledActions.includes(a.id));

    // Grouper par catégorie
    const byCategory = {};
    actions.forEach(a => {
      if (!byCategory[a.category]) byCategory[a.category] = [];
      byCategory[a.category].push(a);
    });

    let html = '<h3>Que veux-tu faire ?</h3><div class="action-categories">';

    for (const [catId, catActions] of Object.entries(byCategory)) {
      const cat = ACTION_CATEGORIES[catId];
      html += `
        <div class="action-category">
          <h4 style="color: ${cat.color}">${cat.label}</h4>
          <div class="action-grid">
            ${catActions.map(a => `
              <button class="action-btn ${this.selection.action === a.id ? 'selected' : ''}"
                      data-action="${a.id}" title="${a.description}">
                <span class="action-emoji">${a.emoji}</span>
                <span class="action-label">${a.label}</span>
              </button>
            `).join('')}
          </div>
        </div>
      `;
    }

    html += '</div>';
    return html;
  }

  renderSubjectStep(settings) {
    const enabledSubjects = settings.enabledSubjects || [];
    const subjects = DEFAULT_SUBJECTS.filter(s => enabledSubjects.includes(s.id));

    return `
      <h3>Pour quelle matière ?</h3>
      <div class="subject-grid">
        ${subjects.map(s => `
          <button class="subject-btn ${this.selection.subject === s.id ? 'selected' : ''}"
                  data-subject="${s.id}">
            <span class="subject-emoji">${s.emoji}</span>
            <span class="subject-label">${s.label}</span>
          </button>
        `).join('')}
      </div>
    `;
  }

  renderLevelStep(settings) {
    const defaultLevel = settings.defaultLevel;
    const levels = DEFAULT_LEVELS.filter(l => l.enabled);

    // Si un niveau par défaut est défini, le présélectionner
    if (defaultLevel && !this.selection.level) {
      this.selection.level = defaultLevel;
    }

    return `
      <h3>Quel niveau ?</h3>
      ${defaultLevel ? `<p class="hint">Niveau par défaut : ${DEFAULT_LEVELS.find(l => l.id === defaultLevel)?.label || defaultLevel}</p>` : ''}
      <div class="level-grid">
        ${levels.map(l => `
          <button class="level-btn ${this.selection.level === l.id ? 'selected' : ''}"
                  data-level="${l.id}">
            ${l.label}
          </button>
        `).join('')}
      </div>
    `;
  }

  renderThemeStep() {
    return `
      <h3>Quel thème ou chapitre ?</h3>
      <p class="hint">Décris en quelques mots le sujet (optionnel mais recommandé)</p>
      <input type="text" id="theme-input" class="theme-input"
             placeholder="Ex: Théorème de Pythagore, La Révolution française..."
             value="${this.selection.theme}">
      <div class="theme-suggestions">
        <span class="suggestion-label">Suggestions :</span>
        <button class="suggestion-btn" data-theme="Équations">Équations</button>
        <button class="suggestion-btn" data-theme="Fonctions">Fonctions</button>
        <button class="suggestion-btn" data-theme="Géométrie">Géométrie</button>
        <button class="suggestion-btn" data-theme="Statistiques">Statistiques</button>
      </div>
    `;
  }

  bindEvents() {
    // Actions
    this.container.querySelectorAll('.action-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.selection.action = btn.dataset.action;
        this.container.querySelectorAll('.action-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        this.updateNextButton();
      });
    });

    // Subjects
    this.container.querySelectorAll('.subject-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.selection.subject = btn.dataset.subject;
        this.container.querySelectorAll('.subject-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        this.updateNextButton();
      });
    });

    // Levels
    this.container.querySelectorAll('.level-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.selection.level = btn.dataset.level;
        this.container.querySelectorAll('.level-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        this.updateNextButton();
      });
    });

    // Theme input
    const themeInput = this.container.querySelector('#theme-input');
    if (themeInput) {
      themeInput.addEventListener('input', (e) => {
        this.selection.theme = e.target.value;
        this.updateNextButton();
      });
    }

    // Theme suggestions
    this.container.querySelectorAll('.suggestion-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const themeInput = this.container.querySelector('#theme-input');
        if (themeInput) {
          themeInput.value = btn.dataset.theme;
          this.selection.theme = btn.dataset.theme;
          this.updateNextButton();
        }
      });
    });

    // Navigation (boutons haut et bas)
    this.container.querySelectorAll('.wizard-back').forEach(btn => {
      btn.addEventListener('click', () => this.prevStep());
    });
    this.container.querySelectorAll('.wizard-cancel').forEach(btn => {
      btn.addEventListener('click', () => this.onCancel());
    });
    this.container.querySelectorAll('.wizard-next').forEach(btn => {
      btn.addEventListener('click', () => this.nextStep());
    });
    this.container.querySelectorAll('.wizard-finish').forEach(btn => {
      btn.addEventListener('click', () => this.finish());
    });
    this.container.querySelectorAll('.wizard-skip').forEach(btn => {
      btn.addEventListener('click', () => this.skipStep());
    });

    this.updateNextButton();
  }

  /**
   * Passe l'étape courante en utilisant la valeur par défaut si disponible
   */
  skipStep() {
    const step = this.steps[this.currentStep];
    const settings = db.getSettings();

    // Appliquer la valeur par défaut si nécessaire
    if (step === 'level' && !this.selection.level && settings.defaultLevel) {
      this.selection.level = settings.defaultLevel;
    }

    this.nextStep();
  }

  updateNextButton() {
    const step = this.steps[this.currentStep];
    let isValid = false;

    switch (step) {
      case 'action':
        isValid = !!this.selection.action;
        break;
      case 'subject':
        isValid = !!this.selection.subject;
        break;
      case 'level':
        isValid = !!this.selection.level;
        break;
      case 'theme':
        isValid = true; // Le thème est optionnel
        break;
    }

    // Mettre à jour tous les boutons (haut et bas)
    this.container.querySelectorAll('.wizard-next').forEach(btn => {
      btn.disabled = !isValid;
    });
    this.container.querySelectorAll('.wizard-finish').forEach(btn => {
      btn.disabled = !isValid;
    });
  }

  nextStep() {
    if (this.currentStep < this.steps.length - 1) {
      this.currentStep++;
      this.render();
    }
  }

  prevStep() {
    if (this.currentStep > 0) {
      this.currentStep--;
      this.render();
    }
  }

  finish() {
    this.onComplete(this.selection);
  }

  /**
   * Récupère les labels pour l'affichage
   */
  getSelectionLabels() {
    const action = ACTIONS.find(a => a.id === this.selection.action);
    const subject = DEFAULT_SUBJECTS.find(s => s.id === this.selection.subject);
    const level = DEFAULT_LEVELS.find(l => l.id === this.selection.level);

    return {
      action: action ? `${action.emoji} ${action.label}` : '',
      subject: subject ? `${subject.emoji} ${subject.label}` : '',
      level: level ? level.label : '',
      theme: this.selection.theme || 'Non spécifié'
    };
  }
}

export { Wizard };
